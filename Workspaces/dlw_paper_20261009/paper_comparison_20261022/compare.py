"""Independent comparison of PDF eqs (4)-(5) with the existing paper FD/PE.
No manuscript or notebook mutation. All fields start from the continuous solution.
"""
from pathlib import Path
import json, time, hashlib
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from scipy.sparse import coo_matrix
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
NB=ROOT/'notebook/DLW数值分析report.ipynb'
snapshot=HERE/'solver_snapshot.py'
exec(compile(snapshot.read_text(encoding='utf8'),str(snapshot),'exec'))

class PaperModel(PhysicalModel):
    def __init__(self,case,config,midpoint=False):
        super().__init__(case,'paper',config)
        self.offset=-.5 if midpoint else 0.
    def initial(self):
        u=self.G.uv(self.js,self.X.x,0)[0]
        v=self.G.uv(self.js+self.offset,self.X.x,0)[1]
        return self.pack(np.diff(u,axis=0)/self.h,v)
    def rhs(self,t,z):
        p,v=self.unpack(z);u=self.recover_u(p,t)
        lower=self.G.uv([self.js[0]-1],self.X.x,t)[0]
        prev=np.concatenate((lower,u[:-1]))
        du=(u-prev)/self.h; avg=(u+prev)/2
        d1,d2=self.X.d1,self.X.d2
        pt=-np.diff(d1(u*u/2+2*self.a*u),axis=0)/self.h-d2(v[1:])
        flux=(avg+2*self.a-2*self.h)*v+self.h*v*v/4-4*avg+d1(du)-self.h*du*du/4
        return self.pack(pt,-d1(flux))

class PaperExact(Exact):
    """N<=2 tau family matching our fixed p,q,a and continuous limit.
    E_i = exp(k_i*x+omega_i*t) r_i**(y/h)/(p_i+q_i),
    r_i=(1+h/(p_i-a))/(1-h/(q_i+a)); f coefficients c_i unchanged.
    """
    def __init__(self,case,h,a=2.):
        super().__init__(case,h,a)
        p,q=map(np.asarray,CASES[case])
        l=(np.log1p(h/(p-a))-np.log1p(-h/(q+a)))/h
        subsets=np.array([[0],[1]]) if len(p)==1 else np.array([[0,0],[1,0],[0,1],[1,1]])
        self.rates[:,2]=subsets@l
    def uv(self,js,x,t):
        _,f=self.tau(js,x,t,True);_,g=self.tau(js,x,t)
        _,fb=self.tau(np.asarray(js)-1,x,t,True);_,gb=self.tau(np.asarray(js)-1,x,t)
        return 2*(self.mean(f,0)-self.mean(g,0)),2/self.h*(self.mean(f,0)+self.mean(g,0)-self.mean(fb,0)-self.mean(gb,0))

def validation():
    checks={}
    for case in CASES:
        g=PaperExact(case,.1);js=np.arange(-3,4);x=np.linspace(-2,2,11);t=.003
        vals=[]
        for back,drift in [(0,2.),(1,1.9)]:
            _,f=g.tau(js,x,t,True);_,b=g.tau(js-back,x,t)
            z=g.cov(f,0,0)+g.cov(b,0,0)+(g.mean(f,0)-g.mean(b,0))**2+g.mean(f,1)-g.mean(b,1)+2*drift*(g.mean(f,0)-g.mean(b,0))
            vals.append(float(abs(z).max()))
        checks[case]=dict(normalized_bilinear_residual=vals)
    assert max(max(v['normalized_bilinear_residual']) for v in checks.values())<1e-10
    return checks

def evaluate(m,z,t,offset):
    u,v=m.fields(z,t)
    xx=np.linspace(-m.evalhalf,m.evalhalf,round(2*m.evalhalf/.01)+1)
    mask=abs(m.y)<m.evalhalf
    js=m.js[mask]
    spl=[CubicSpline(m.X.x,f[mask],axis=-1,extrapolate=False) for f in (u,v)]
    errors=np.zeros(2);gaps=np.zeros(2);remaining=np.zeros(2)
    profiles=[[],[]]
    for xb in np.array_split(xx,max(1,len(xx)//200)):
        refs=[m.G.uv(js,xb,t)[0],m.G.uv(js+offset,xb,t)[1]]
        lattice=m.PE.uv(js,xb,t)
        for k in range(2):
            num=spl[k](xb);err=abs(num-refs[k])
            errors[k]=max(errors[k],float(err.max()))
            gaps[k]=max(gaps[k],float(abs(lattice[k]-refs[k]).max()))
            remaining[k]=max(remaining[k],float(abs(num-lattice[k]).max()))
            profiles[k].extend(err.max(axis=0).tolist())
    return dict(errors=errors.tolist(),paper_exact_gap=gaps.tolist(),distance_to_paper_exact=remaining.tolist()),xx,np.array(profiles),(u,v)

def run(case,model,halfdt=False):
    cfg=case_config(case)
    if halfdt:cfg['dt']/=2
    name=f'{case}_{model}'+('_halfdt' if halfdt else '')
    dest=HERE/(name+'.json')
    if dest.exists():return json.loads(dest.read_text())
    t0=time.perf_counter()
    if model in ('paper_endpoint','paper_midpoint'):
        m=PaperModel(case,cfg,model=='paper_midpoint')
    else:m=(FDModel if model=='FD' else SDModel)(case,model,cfg)
    offset=getattr(m,'offset',0.)
    m.evalhalf=cfg['eval_half'];m.PE=PaperExact(case,cfg['h'],cfg['a'])
    z=m.initial();fields=m.fields(z,0)
    initial=max(float(abs(fields[k]-m.G.uv(m.js+(offset if k==1 else 0),m.X.x,0)[k]).max()) for k in range(2))
    n=round(cfg['T']/cfg['dt'])
    for i in range(n):
        z=step(m.rhs,i*cfg['dt'],z,cfg['dt'],'RK4')
        if not np.isfinite(z).all() or abs(z).max()>1000:raise RuntimeError(f'{name} failed at step {i}')
    metrics,xx,profiles,fields=evaluate(m,z,cfg['T'],offset)
    np.savez_compressed(HERE/(name+'.npz'),state=z,x=m.X.x,y=m.y,u=fields[0],v=fields[1],eval_x=xx,error_profiles=profiles)
    record=dict(case=case,model=model,config=cfg,v_y_offset_in_h=offset,initial_max_error=initial,**metrics,seconds=time.perf_counter()-t0)
    dest.write_text(json.dumps(record,indent=2),encoding='utf8')
    print(name,json.dumps(record['errors']),'seconds',round(record['seconds'],1),flush=True)
    return record

if __name__=='__main__':
    (HERE/'validation.json').write_text(json.dumps(validation(),indent=2))
    (HERE/'provenance.json').write_text(json.dumps(dict(notebook=str(NB),sha256=hashlib.sha256(NB.read_bytes()).hexdigest(),cells=['dlw-'+s for s in ('config','reference','spatial','sd_fd','sd','fd','time')]),indent=2))
    records=[]
    for case in CASES:
        for model in ('FD','PE','paper_endpoint','paper_midpoint'):
            records.append(run(case,model))
    for case in CASES:
        for model in ('paper_endpoint','paper_midpoint'):
            records.append(run(case,model,True))
    (HERE/'results.json').write_text(json.dumps(records,indent=2))
