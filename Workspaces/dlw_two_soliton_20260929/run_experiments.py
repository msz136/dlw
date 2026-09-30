"""Three original zero-background cases, six methods, controlled short time."""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import numpy as np
from scipy.interpolate import CubicSpline
from models import Problem,previous,BASE
from reference import CASES
from dataclasses import asdict
from parametric import rk4
HERE=Path(__file__).resolve().parent
OUT=HERE/'out';OUT.mkdir(exist_ok=True)

def one(s):
    p=Problem(s);m=p.m;n=p.X.n;state=p.initial();s0=p.X.s.copy()
    arrays={'y':m.y};hist=[];last=0.;status='completed';reason='';moved=0
    neval=8001 if s['case']=='fig5' else 4001
    xx=np.linspace(-s['eval_half'],s['eval_half'],neval)
    def sample(t):
        u,v=p.fields(state,t);exact=m.G.uv(m.js,xx,t);nodal=m.G.uv(m.js,p.X.x,t)
        errors={f:float(abs(CubicSpline(p.X.x,a,axis=-1)(xx)-e).max()) for f,a,e in zip(('u','v'),(u,v),exact)}
        den,_=p.monitor(t,state[:-n])
        row=dict(t=float(t),errors=errors,nodal_errors={f:float(abs(a-e).max()) for f,a,e in zip(('u','v'),(u,v),nodal)},min_J=float(p.X.J.min()),min_monitor=float(den.min()),max_displacement=float(abs(p.X.s-s0).max()))
        hist.append(row)
        for k,a in (('x',p.X.x),('u',u),('v',v)):arrays[f't{t:g}_{k}']=a.copy()
        if p.sd2 and t in (0.,.01,.02):
            q,r=m.unpack(state[:-n],t)
            arrays[f't{t:g}_Q']=q.copy();arrays[f't{t:g}_R']=r.copy()
    sample(0.)
    dt=s['dt'];times=np.arange(1,41)*.0005 if s['variant']=='main' else np.array([.001,.005,.01,.02])
    samples={round(t/dt):float(t) for t in times}
    for j in range(1,round(.02/dt)+1):
        try:
            with np.errstate(over='raise',invalid='raise',divide='raise'):
                cand=rk4(p.rhs,(j-1)*dt,state,dt)
                if not np.all(np.isfinite(cand)) or abs(cand).max()>1000:raise ValueError('nonfinite state or magnitude >1000')
                p.X.set_s(cand[-n:])
                if p.sd2 and m.unpack(cand[:-n],j*dt)[0].min()<=0:raise ValueError('nonpositive Q')
                if s['mesh']=='moving' and p.monitor(j*dt,cand[:-n])[0].min()<=0:raise ValueError('nonpositive monitor')
        except (ValueError,FloatingPointError,OverflowError) as ex:
            status='stopped';reason=str(ex);break
        moved+=int(abs(cand[-n:]-state[-n:]).max()>1e-14)
        state=cand;last=j*dt
        if j in samples:sample(samples[j])
    if abs(hist[-1]['t']-last)>1e-12:sample(last)
    path=OUT/('_'.join(s[k] for k in ('case','model','mesh','variant'))+'.npz')
    np.savez_compressed(path,**arrays)
    return dict(spec=s,status=status,reached=float(last),reason=reason,moved_steps=moved,history=hist,profile=str(path),profile_sha256=previous.sha(path))

def make_plan():
    plan=[]
    for variant in ('main','time_half','x_half','y_half','domain_double'):
        for name in CASES:
            n,L,ev=(1024,640.,100.) if name=='fig5' else (256,40.,10.)
            h=.125;dt=.000125
            if variant=='time_half':dt/=2
            if variant=='x_half':n*=2;dt/=2
            if variant=='y_half':h/=2
            if variant=='domain_double':L*=2;n*=2
            for model in ('SD','SD2','FD'):
                for mesh in ('fixed','moving'):
                    plan.append(dict(case=name,model=model,mesh=mesh,variant=variant,nx=n,L=L,h=h,dt=dt,T=.02,eval_half=ev))
    return plan

def main():
    plan=make_plan()
    sources={str(p):previous.sha(p) for p in (Path(__file__),HERE/'reference.py',HERE/'models.py',BASE/'dlw_sd2_20260929/sd2.py',BASE/'dlw_semidiscrete/numerics/lib/parametric.py',BASE/'dlw_semidiscrete/numerics/lib/parametric_open.py',BASE/'dlw_semidiscrete/numerics/lib/moving_mesh.py',BASE/'dlw_semidiscrete/numerics/lib/dynamics.py',BASE/'dlw_semidiscrete/numerics/lib/solver.py',BASE.parents[0]/'Paper/sources/PhysD-published.pdf')}
    dest=OUT/'results.json'
    d=json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else dict(plan=plan,parameters={k:asdict(v) for k,v in CASES.items()},sources=sources,runs=[])
    assert d['plan']==plan and d['sources']==sources
    remaining=[s for s in plan if not any(r['spec']==s for r in d['runs'])]
    with ProcessPoolExecutor(max_workers=2) as pool:
        futures={pool.submit(one,s):s for s in remaining}
        for future in as_completed(futures):
            r=future.result();s=r['spec'];d['runs'].append(r);previous.dump(dest,d)
            print(len(d['runs']),s['case'],s['model'],s['mesh'],s['variant'],r['status'],r['reached'],r['history'][-1]['errors'],flush=True)
    print('DONE',len(d['runs']),flush=True)

if __name__=='__main__':main()
