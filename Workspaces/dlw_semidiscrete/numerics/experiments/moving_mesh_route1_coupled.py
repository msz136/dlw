"""Route-one coupled mesh experiment; never uses future exact fields to move nodes.

Fixed kernels skip monitor/flux calculation. Intermittent grids are rebuilt
from the current numerical density and the evolved P,Q state is remapped.
"""
from pathlib import Path
import sys, json, hashlib, time, argparse

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'lib'), str(ROOT/'experiments')]
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import brentq
from moving_mesh import MovingProblem, gram_mesh
from moving_mesh_study import ALL


def norm(a):
    return float(np.max(np.abs(a)))


def periodic_interpolate(old_x, values, new_x, length):
    """Periodic cubic remap, with the known left endpoint repeated at right."""
    x = np.r_[old_x, old_x[0] + length]
    y = np.concatenate([values, values[..., :1]], axis=-1)
    return CubicSpline(x, y, axis=-1, bc_type='periodic')(new_x)


def gradient_monitor(problem,z,t,alpha):
    u,_=problem.m.fields(z,t)
    g=np.mean(abs(problem.X.d1(u)),axis=0)
    x=problem.X.x
    fine=np.linspace(x[0],x[0]+problem.X.L,8*problem.X.n+1)
    gf=periodic_interpolate(x,g[None,:],fine,problem.X.L)[0]
    gf=gaussian_filter1d(gf,.08/(fine[1]-fine[0]),mode='wrap')
    return 1+alpha*np.maximum(gf,0)


def build_grid_from_fine(problem,fine_monitor):
    x=problem.X.x
    fine=np.linspace(x[0],x[0]+problem.X.L,8*problem.X.n+1)
    cumulative=np.r_[0,np.cumsum(np.diff(fine)*(fine_monitor[1:]+fine_monitor[:-1])/2)]
    return np.interp(np.arange(problem.X.n)*cumulative[-1]/problem.X.n,
                     cumulative,fine)


def remesh(problem, z, t, kind='gram', alpha=None):
    x=problem.X.x.copy()
    if kind=='gram':
        R,_=problem.mesh_density_flux(t,z)
        if not np.all(np.isfinite(R)) or R.min()<=0:
            raise ValueError('nonpositive remesh density')
        fine=np.linspace(x[0],x[0]+problem.X.L,8*problem.X.n+1)
        rf=periodic_interpolate(x,R[None,:],fine,problem.X.L)[0]
        if rf.min()<=0:raise ValueError('nonpositive interpolated remesh density')
        new_x=build_grid_from_fine(problem,rf)
    else:
        new_x=build_grid_from_fine(problem,gradient_monitor(problem,z,t,alpha))
    p,q=problem.m.unpack(z)
    p_new=periodic_interpolate(x,p,new_x,problem.X.L)
    q_new=periodic_interpolate(x,q,new_x,problem.X.L)
    problem.set_s(new_x-problem.X.xi)
    return problem.m.pack(p_new,q_new),norm(new_x-x),min(problem.X.spacing())


def fixed_rhs(problem, t, z):
    # Exactly the stationary-grid physical field RHS; avoids monitor work.
    return problem.m.rhs(t,z)


def moving_rhs(problem, t, z, s):
    return problem.rhs(t,(z,s),balanced=False,mesh_mode='moving')


def observe(problem,z,t,mode,remap_count,max_remap):
    e = z-problem.m.exact(t)
    eu,ev = problem.m.error_fields(e)
    u,v = problem.m.fields(z,t)
    ue,ve = problem.m.G.uv(problem.m.js,problem.X.x,t)
    # Physical-field error includes reconstruction and current x geometry.
    eps_u,eps_v = u-ue,v-ve
    target = np.linspace(-8,8,801)
    ui = periodic_interpolate(problem.X.x,u,target,problem.X.L)
    vi = periodic_interpolate(problem.X.x,v,target,problem.X.L)
    ut,vt = problem.m.G.uv(problem.m.js,target,t)
    return {'t':float(t),'mode':mode,'u_error':norm(eps_u),
            'v_error':norm(eps_v),'u_common_error':norm(ui-ut),
            'v_common_error':norm(vi-vt),'u_response':norm(eu),
            'v_response':norm(ev),'min_dx':float(min(problem.X.spacing())),
            'min_J':float(problem.X.J.min()),'remaps':remap_count,
            'max_remap_displacement':max_remap}


def run(pars, model, mode, T, dt, refresh=.01, nx=128):
    problem=MovingProblem(pars,h=.125,nx=nx,model=model)
    init='uniform' if mode in ('uniform','gradient_static','gradient_intermittent') else 'static_adaptive'
    z,s=problem.initial(init,balanced=False)
    alpha=None
    if mode.startswith('gradient'):
        gram=gram_mesh(pars,.125,problem.m.js,problem.X.xi)
        target_min=min(np.diff(np.r_[gram,gram[0]+problem.X.L]))
        def min_spacing(a):
            monitor=gradient_monitor(problem,z,0.,a)
            x=build_grid_from_fine(problem,monitor)
            return min(np.diff(np.r_[x,x[0]+problem.X.L]))
        alpha=brentq(lambda a:min_spacing(a)-target_min,0,1e5)
        new_x=build_grid_from_fine(problem,gradient_monitor(problem,z,0.,alpha))
        problem.set_s(new_x-problem.X.xi)
        z=problem.m.exact(0.)
    steps=round(T/dt)
    assert abs(steps*dt-T)<1e-11
    refresh_steps=round(refresh/dt)
    assert abs(refresh_steps*dt-refresh)<1e-11
    rows=[];remap_count=0;max_remap=0.;status='complete';stop=T
    start=time.perf_counter()
    for i in range(steps):
        t=i*dt
        try:
            if mode=='moving':
                # Same four-stage coupled RK4 as the existing implementation.
                state=np.r_[z,s];nz=z.size
                def fun(tt,y):
                    dz,ds=moving_rhs(problem,tt,y[:nz],y[nz:])
                    return np.r_[dz,ds]
                k1=fun(t,state);k2=fun(t+dt/2,state+dt*k1/2)
                k3=fun(t+dt/2,state+dt*k2/2);k4=fun(t+dt,state+dt*k3)
                state=state+dt*(k1+2*k2+2*k3+k4)/6
                z,s=state[:nz],state[nz:]
                problem.set_s(s)
            else:
                def f(tt,zz): return fixed_rhs(problem,tt,zz)
                k1=f(t,z);k2=f(t+dt/2,z+dt*k1/2)
                k3=f(t+dt/2,z+dt*k2/2);k4=f(t+dt,z+dt*k3)
                z=z+dt*(k1+2*k2+2*k3+k4)/6
                if mode in ('intermittent','gradient_intermittent') and (i+1)%refresh_steps==0:
                    kind='gradient' if mode=='gradient_intermittent' else 'gram'
                    z,displacement,_=remesh(problem,z,(i+1)*dt,kind,alpha)
                    remap_count+=1;max_remap=max(max_remap,displacement)
            if not np.all(np.isfinite(z)) or norm(z)>1e3:
                raise ValueError('state diverged')
            now=(i+1)*dt
            if (i+1)%max(1,round(.01/dt))==0 or i==steps-1:
                rows.append(observe(problem,z,now,mode,remap_count,max_remap))
        except ValueError as exc:
            status=str(exc);stop=t;break
    return {'model':model,'mode':mode,'T':T,'dt':dt,'nx':nx,
            'refresh':refresh if mode in ('intermittent','gradient_intermittent') else None,
            'gradient_alpha':alpha,
            'seconds':time.perf_counter()-start,'status':status,
            'stop_t':stop,'observations':rows}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--quick',action='store_true')
    ap.add_argument('--gradient-only',action='store_true')
    args=ap.parse_args()
    cases=(0,6) if args.quick else (0,1,6,9)
    horizons=(.02,.04) if args.quick else (.02,.04,.08)
    modes=('gradient_static','gradient_intermittent') if args.gradient_only else (
        'uniform','static_adaptive','moving','intermittent')
    output={'scope':{'h':.125,'nx':128,'dt':.000125,
                     'reference':'finite-h exact one-soliton',
                     'common_x':[-8,8,801],
                     'intermittent_refresh':.01,
                     'fixed_grid_monitor_calls':0},'runs':[]}
    for index in cases:
        pars=ALL[index]
        for model in ('structure','fd'):
            for T in horizons:
                for mode in modes:
                    row=run(pars,model,mode,T,.000125)
                    row['parameter_id']=f'P{index+1}'
                    output['runs'].append(row)
                    print(f'P{index+1} {model} {T} {mode}: {row["status"]}, '
                          f'{row["seconds"]:.2f}s',flush=True)
    output['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (Path(__file__),ROOT/'lib/moving_mesh.py')}
    dest=ROOT/'out'/'moving_mesh'/('route1_gradient.json' if args.gradient_only
                                  else 'route1_coupled.json')
    dest.write_text(json.dumps(output,indent=2,allow_nan=False),encoding='utf-8')


if __name__=='__main__':main()
