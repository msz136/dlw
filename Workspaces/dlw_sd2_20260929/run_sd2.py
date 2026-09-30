import json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
from sd2 import SD2,previous,BASE
from parametric import rk4
HERE=Path(__file__).resolve().parent
OUT=HERE/'out';OUT.mkdir(exist_ok=True)

def one(s):
    m=SD2(previous.CASES[s['case']],s['h'],s['nx'],s['L'])
    if s['mesh']=='moving':
        xx=np.linspace(-s['L']/2,s['L']/2,40001)
        u,v=m.G.uv(m.js,xx,0.)
        gh=m.G.uv([m.js[0]-1,m.js[-1]+1],xx,0.)[0]
        den=1-np.mean(v-m.dy(u,gh),axis=0)/4
        mass=np.r_[0,np.cumsum((den[1:]+den[:-1])*np.diff(xx)/2)]
        x=np.interp(np.arange(s['nx'])/s['nx']*mass[-1],mass,xx)
        m.X.set_s(x-m.X.xi)
    state=np.r_[m.initial(),m.X.s];s0=m.X.s.copy()
    history=[];arrays={'y':m.y};last=0.;reason='';status='completed';moved=0
    def sample(t):
        m.X.set_s(state[-m.X.n:]);z=state[:-m.X.n]
        uv=m.fields(z,t);xx=np.linspace(-10,10,4001)
        ref=m.G.uv(m.js,xx,t);nod=m.G.uv(m.js,m.X.x,t)
        err={f:float(np.max(abs(CubicSpline(m.X.x,v,axis=-1)(xx)-e))) for f,v,e in zip(('u','v'),uv,ref)}
        q,r=m.unpack(z,t);den,_=m.monitor(t,z)
        history.append(dict(t=t,errors=err,nodal_errors={f:float(np.max(abs(v-e))) for f,v,e in zip(('u','v'),uv,nod)},min_J=float(min(m.X.J)),min_R=float(min(den)),min_Q=float(q.min()),max_displacement=float(max(abs(m.X.s-s0)))))
        for k,a in zip(('x','u','v','Q','R'),(m.X.x,*uv,q,r)):arrays[f't{t:g}_{k}']=a.copy()
    sample(0.)
    dt=s['dt'];samples={round(t/dt):t for t in np.arange(1,41)*.0005}
    for j in range(1,round(.02/dt)+1):
        try:
            with np.errstate(over='raise',invalid='raise',divide='raise'):
                cand=rk4(lambda t,z:m.rhs(t,z,s['mesh']),(j-1)*dt,state,dt)
                if not np.all(np.isfinite(cand)) or max(abs(cand))>1000:raise ValueError('nonfinite or magnitude>1000')
                m.X.set_s(cand[-m.X.n:]);q,r=m.unpack(cand[:-m.X.n],j*dt)
                if q.min()<=0:raise ValueError('nonpositive Q')
                if s['mesh']=='moving' and m.monitor(j*dt,cand[:-m.X.n])[0].min()<=0:raise ValueError('nonpositive monitor')
        except (ValueError,FloatingPointError,OverflowError) as ex:
            status='stopped';reason=str(ex);break
        moved+=int(max(abs(cand[-m.X.n:]-state[-m.X.n:]))>1e-14)
        state=cand;last=j*dt
        if j in samples:sample(samples[j])
    if abs(history[-1]['t']-last)>1e-12:sample(last)
    path=OUT/('_'.join(s[k] for k in ('case','model','mesh','variant'))+'.npz')
    np.savez_compressed(path,**arrays)
    return dict(spec=s,status=status,reached=last,reason=reason,moved_steps=moved,history=history,profile=str(path),profile_sha256=previous.sha(path))

def main():
    variants={'main':(256,40.,.125,.000125),'time_half':(256,40.,.125,.0000625),'x_half':(512,40.,.125,.0000625),'y_half':(256,40.,.0625,.000125),'domain_double':(512,80.,.125,.000125)}
    plan=[dict(case=c,model='SD2',mesh=mesh,variant=k,nx=n,L=L,h=h,dt=dt,T=.02) for c in previous.CASES for mesh in ('fixed','moving') for k,(n,L,h,dt) in variants.items()]
    sources={str(p):previous.sha(p) for p in (Path(__file__),HERE/'sd2.py',BASE/'gsg_project/dlw_report/_src/Report.md',BASE/'dlw_semidiscrete/numerics/lib/moving_mesh.py',BASE/'dlw_paper_cases_20260927/run.py')}
    dest=OUT/'results.json'
    d=json.loads(dest.read_text()) if dest.exists() else dict(plan=plan,sources=sources,runs=[])
    assert d['sources']==sources and d['plan']==plan
    for s in plan:
        if any(r['spec']==s for r in d['runs']):continue
        r=one(s);d['runs'].append(r);previous.dump(dest,d)
        print(len(d['runs']),s['case'],s['mesh'],s['variant'],r['status'],r['reached'],r['history'][-1]['errors'],flush=True)

if __name__=='__main__':main()
