"""Long-distance moving-grid field test on a controlled transport equation.

The evolved fields solve z_t+c*z_x=0 for the exact finite-h Gram profile at
t=0. This isolates grid/field discretization over one to two pulse widths.
It is deliberately NOT an integration of the nonlinear DLW equations.
"""
from pathlib import Path
import sys, json, hashlib, argparse

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'lib'),str(ROOT/'experiments')]
import numpy as np
from scipy.interpolate import CubicSpline
from moving_mesh import MovingGrid,gram_mesh
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import periodic_interpolate,norm
from parametric import Exact


def density(u,v,h):
    left=3*u[0]-3*u[1]+u[2]
    right=3*u[-1]-3*u[-2]+u[-3]
    ext=np.concatenate([left[None],u,right[None]])
    dy=(ext[2:]-ext[:-2])/(2*h)
    return np.mean(1-(v-dy)/4,axis=0)


def redistribute(X,u,v,h):
    old=X.x.copy();R=density(u,v,h)
    if not np.all(np.isfinite(R)) or R.min()<=0:
        raise ValueError('nonpositive monitor')
    fine=np.linspace(old[0],old[0]+X.L,8*X.n+1)
    rf=periodic_interpolate(old,R[None],fine,X.L)[0]
    if rf.min()<=0:raise ValueError('nonpositive interpolated monitor')
    mass=np.r_[0,np.cumsum(np.diff(fine)*(rf[1:]+rf[:-1])/2)]
    new=np.interp(np.arange(X.n)*mass[-1]/X.n,mass,fine)
    uu=periodic_interpolate(old,u,new,X.L)
    vv=periodic_interpolate(old,v,new,X.L)
    X.set_s(new-X.xi)
    return uu,vv


def run(pars,width,D_targets,nx=128,dt=.001,mode='moving',refresh=.1):
    h=.125;js=np.arange(-12,12);L=20.
    c=pars.p-pars.q
    exact=Exact(pars,h)
    X=MovingGrid(nx,L)
    if mode!='uniform':
        x=gram_mesh(pars,h,js,X.xi)
        X.set_s(x-X.xi)
    u,v=exact.uv(js,X.x,0.)
    initial=(u.copy(),v.copy())
    target=np.linspace(-8,8,801)
    snapshots=[];status='complete';stop=None
    final_D=max(D_targets)
    T=final_D*width/abs(c)
    n=round(T/dt);step=T/n
    def metrics(now):
        xt=X.x
        x0=((target-c*now+L/2)%L)-L/2
        truth=exact.uv(js,x0,0.)
        node_x0=((xt-c*now+L/2)%L)-L/2
        node_truth=exact.uv(js,node_x0,0.)
        fields=(periodic_interpolate(xt,u,target,L),
                periodic_interpolate(xt,v,target,L))
        return {'t':now,'D':abs(c)*now/width,
                'u_common_error':norm(fields[0]-truth[0]),
                'v_common_error':norm(fields[1]-truth[1]),
                'u_node_error':norm(u-node_truth[0]),
                'v_node_error':norm(v-node_truth[1]),
                'min_dx':float(min(X.spacing())),
                'min_J':float(min(X.J)),
                'min_R':float(min(density(u,v,h)))}
    snapshots.append(metrics(0.))
    for i in range(n):
        t=i*step
        try:
            def rhs(state):
                xstate=state[-nx:]
                X.set_s(xstate)
                U=state[:len(js)*nx].reshape(len(js),nx)
                V=state[len(js)*nx:-nx].reshape(len(js),nx)
                if mode=='moving':
                    R=density(U,V,h)
                    if not np.all(np.isfinite(R)) or R.min()<=0:
                        raise ValueError('nonpositive monitor')
                    velocity=c*(R-R[0])/R
                else:velocity=np.zeros(nx)
                du=-(c-velocity)*X.d1(U)
                dv=-(c-velocity)*X.d1(V)
                return np.r_[du.ravel(),dv.ravel(),velocity]
            z=np.r_[u.ravel(),v.ravel(),X.s]
            k1=rhs(z);k2=rhs(z+step*k1/2)
            k3=rhs(z+step*k2/2);k4=rhs(z+step*k3)
            z=z+step*(k1+2*k2+2*k3+k4)/6
            u=z[:len(js)*nx].reshape(len(js),nx)
            v=z[len(js)*nx:-nx].reshape(len(js),nx)
            X.set_s(z[-nx:])
            if mode=='intermittent' and (i+1)%max(1,round(refresh/step))==0:
                u,v=redistribute(X,u,v,h)
            if not (np.all(np.isfinite(u)) and np.all(np.isfinite(v))):
                raise ValueError('nonfinite state')
            now=(i+1)*step
            if any(abs(now-D*width/abs(c))<step/2 for D in D_targets):
                snapshots.append(metrics(now))
        except ValueError as exc:
            status=str(exc);stop=t;break
    return {'mode':mode,'nx':nx,'dt_nominal':dt,'actual_dt':step,
            'status':status,'stop_t':stop,'observations':snapshots}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--quick',action='store_true')
    args=ap.parse_args()
    geom=json.loads((ROOT/'out/moving_mesh/route1_geometry.json').read_text())
    widths={r['parameter_id']:r['width'] for r in geom['cases']}
    cases=(0,6) if args.quick else (0,1,6,9)
    resolutions=(128,) if args.quick else (64,128,256)
    modes=('uniform','static_adaptive','moving','intermittent')
    data={'scope':{'equation':'z_t+c*z_x=0, c=p-q, separately for u and v',
                   'not_DLW':True,'h':.125,'x_length':20,
                   'common_x':[-8,8,801],'D_targets':[0,.5,1,2],
                   'refresh':.1},'runs':[]}
    for index in cases:
        pid=f'P{index+1}'
        for nx in resolutions:
            for mode in modes:
                row=run(ALL[index],widths[pid],[.5,1,2],nx=nx,mode=mode)
                row['parameter_id']=pid
                data['runs'].append(row)
                print(pid,nx,mode,row['status'],flush=True)
    paths=[Path(__file__),ROOT/'lib/moving_mesh.py',
           ROOT/'experiments/moving_mesh_route1_coupled.py']
    data['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in paths}
    dest=ROOT/'out/moving_mesh'/('route1_transport_quick.json' if args.quick
                                 else 'route1_transport.json')
    dest.write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
