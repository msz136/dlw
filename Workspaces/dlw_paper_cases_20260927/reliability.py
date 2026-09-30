"""Unmodified DLW evolution to T=1, fixed and continuously moving x meshes."""
import json
import numpy as np
from scipy.interpolate import CubicSpline
import run as previous
from moving_mesh import MovingProblem
from parametric import rk4
OUT=previous.HERE/'reliability';OUT.mkdir(exist_ok=True)

def one(spec):
    p=MovingProblem(previous.CASES[spec['case']],h=spec['h'],nx=spec['nx'],L=spec['L'],model=spec['model'],continuous=True,yhalf=1.5)
    # Equal-mass initial grid for the same continuous monitor used in evolution.
    if spec['mesh']=='moving':
        dense=np.linspace(-spec['L']/2,spec['L']/2,40001);m=p.m
        uv=m.G.uv(m.js,dense,0.);ghost=m.G.uv([m.js[0]-1,m.js[-1]+1],dense,0.)[0]
        R=1-np.mean(uv[1]-m.dy(uv[0],ghost),axis=0)/4
        assert np.min(R)>0
        mass=np.r_[0,np.cumsum((R[1:]+R[:-1])*np.diff(dense)/2)]
        x=np.interp(np.arange(spec['nx'])/spec['nx']*mass[-1],mass,dense)
        p.set_s(x-p.X.xi)
    state=np.r_[p.m.exact(0.),p.X.s];nz=state.size-spec['nx'];s0=p.X.s.copy()
    def fun(t,z):
        dz,ds=p.rhs(t,(z[:nz],z[nz:]),balanced=False,mesh_mode=spec['mesh'])
        return np.r_[dz,ds]
    arrays={'y':p.m.y};history=[];last=0.;reason='';status='completed';dt=spec['dt'];move_steps=0
    def sample(t):
        p.set_s(state[nz:]);u,v=p.m.fields(state[:nz],t);xx=np.linspace(-10,10,4001)
        numerical=[CubicSpline(p.X.x,f,axis=-1)(xx) for f in (u,v)]
        ref=p.m.G.uv(p.m.js,xx,t)
        R,_=p.mesh_density_flux(t,state[:nz])
        e={f:float(np.max(abs(a-b))) for f,a,b in zip(('u','v'),numerical,ref)}
        nodal=p.m.G.uv(p.m.js,p.X.x,t)
        history.append(dict(t=t,errors=e,nodal_errors={f:float(np.max(abs(a-b))) for f,a,b in zip(('u','v'),(u,v),nodal)},min_J=float(min(p.X.J)),min_R=float(min(R)),max_displacement=float(max(abs(state[nz:]-s0)))))
        for k,a in (('x',p.X.x),('u',u),('v',v)):arrays[f't{t:g}_{k}']=a.copy()
    sample(0.)
    samples={round(t/dt):t for t in (.005,.01,.02,.05,.1,.25,.5,.75,1.)}
    for j in range(1,round(spec['T']/dt)+1):
        try:
            with np.errstate(over='raise',invalid='raise',divide='raise'):
                candidate=rk4(fun,(j-1)*dt,state,dt)
                if not np.all(np.isfinite(candidate)) or max(abs(candidate[:nz]))>1000:raise FloatingPointError('state magnitude >1000 or nonfinite')
                p.set_s(candidate[nz:]);R,_=p.mesh_density_flux(j*dt,candidate[:nz])
                if min(R)<=0:raise ValueError('nonpositive monitor density')
        except (ValueError,FloatingPointError,OverflowError) as exc:
            status='stopped';reason=str(exc);break
        move_steps+=int(max(abs(candidate[nz:]-state[nz:]))>1e-14)
        state=candidate;last=j*dt
        if j in samples:sample(samples[j])
    if abs(history[-1]['t']-last)>1e-10:sample(last)
    key='_'.join(str(spec[k]) for k in ('case','model','mesh','variant'))
    path=OUT/(key+'.npz');np.savez_compressed(path,**arrays)
    return dict(spec=spec,status=status,reached=last,reason=reason,moved_steps=move_steps,history=history,profile=str(path.resolve()),profile_sha256=previous.sha(path))

def main():
    variants={'base':(256,40.,.125,.000125,.05),
              'time_half':(256,40.,.125,.0000625,.05),
              'x_half':(512,40.,.125,.000125,.05),
              'y_half':(256,40.,.0625,.000125,.05),
              'y_quarter':(256,40.,.03125,.000125,.05),
              'domain_double':(512,80.,.125,.000125,1.)}
    plan=[dict(case=case,model=model,mesh=mesh,variant=name,nx=v[0],L=v[1],h=v[2],dt=v[3],T=v[4])
          for case in previous.CASES for model in ('structure','fd') for mesh in ('fixed','moving') for name,v in variants.items()]
    path=OUT/'results.json';d=json.loads(path.read_text()) if path.exists() else dict(plan=plan,driver_sha256=previous.sha(__file__),runs=[])
    assert d['plan']==plan and d['driver_sha256']==previous.sha(__file__)
    for spec in plan:
        if any(r['spec']==spec for r in d['runs']):continue
        r=one(spec);d['runs'].append(r);previous.dump(path,d)
        print(len(d['runs']),spec['case'],spec['model'],spec['mesh'],spec['variant'],r['status'],r['reached'],flush=True)

if __name__=='__main__':main()
