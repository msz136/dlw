"""Matched continuous-data perturbation comparisons, including reference checks.

Reference acceptance is empirical and short-time, NOT a convergence theorem.
No future perturbed solution is supplied to any RHS.
"""
from parametric_study import ROOT,OUT,PARAMS,save,inf
from parametric import Model,Parameters,rk4
from dataclasses import asdict
import numpy as np
from scipy.interpolate import RectBivariateSpline
import time,json,hashlib


def seed(m,mode,eps):
    y=m.y[:,None];x=m.X.x[None,:]
    s=np.zeros_like(y);inside=abs(y[:,0])<.9
    s[inside]=np.exp(1-1/(1-(y[inside]/.9)**2))
    k={'low':2*np.pi/20,'high':16*2*np.pi/20,'vonly':4*2*np.pi/20}[mode]
    f=s*np.exp(-x*x/4)*np.cos(k*x)
    eta=eps*f if mode!='vonly' else np.zeros_like(f)
    nu=.3*eps*f if mode!='vonly' else eps*f
    P=np.diff(eta,axis=0)/m.h
    Q=nu-m.dy(eta,(np.zeros(m.X.n),np.zeros(m.X.n))) if m.model=='structure' else nu
    return m.pack(P,Q)


def simulate(pars,model,closure,balanced,h,nx,mode,eps,T=.01,dt=.000125,model_factory=Model):
    m=model_factory(pars,h,nx,model=model,closure=closure,continuous=True)
    e0=seed(m,mode,eps);z=e0.copy() if balanced else m.exact(0)+e0
    times=[];fields=[];history=[];complete=True
    def fun(t,z):return m.delta(t,m.exact(t),z) if balanced else m.rhs(t,z)
    start=time.perf_counter()
    for i in range(round(T/dt)):
        zz=rk4(fun,i*dt,z,dt)
        if not np.all(np.isfinite(zz)) or inf(zz)>1e3:complete=False;break
        z=zz
        if (i+1)%round(.005/dt)==0:
            t=(i+1)*dt;e=z if balanced else z-m.exact(t)
            uv=m.error_fields(e);times.append(t);fields.append(np.asarray(uv))
            history.append({'t':t,'u_response':inf(uv[0]),'v_response':inf(uv[1])})
    cfg={'pars':asdict(pars),'model':model,'closure':closure,'balanced':balanced,'h':h,'nx':nx,'mode':mode,'eps':eps,'dt':dt,'T':T}
    name='perturb_'+hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()[:12]+'.npz'
    np.savez_compressed(OUT/name,x=m.X.x,y=m.y,times=times,fields=fields)
    return dict(config=cfg,complete=complete,history=history,seconds=time.perf_counter()-start,file=name)


def compare(row,ref):
    a=np.load(OUT/row['file']);b=np.load(OUT/ref['file']);out=[]
    yy,xx=np.meshgrid(a['y'],a['x'],indexing='ij');pts=np.column_stack((yy.ravel(),xx.ravel()))
    for i,t in enumerate(a['times']):
        inds=np.flatnonzero(abs(b['times']-t)<1e-12)
        if not len(inds):continue
        vals=[]
        for f in range(2):
            # Direct spline solve: default iterative absolute tolerance can exceed
            # the small perturbation being measured and corrupt relative errors.
            interp=RectBivariateSpline(b['y'],b['x'],b['fields'][inds[0],f],s=0)
            target=interp(a['y'],a['x'])
            difference=a['fields'][i,f]-target
            error=inf(difference);amp=inf(target)
            peak=np.unravel_index(np.argmax(abs(difference)),difference.shape)
            vals.append({'error':error,'relative_response_error':error/max(amp,1e-30),
                         'interior_error':inf(difference[abs(a['y'])<=.75]),
                         'boundary_error':inf(difference[[0,-1]]),'peak_y':float(a['y'][peak[0]])})
        out.append({'t':float(t),'u':vals[0],'v':vals[1]})
    return out


def main():
    groups=[]
    # Broad dynamics scan is separate; here concentrate on three contrasting backgrounds.
    for pars in (PARAMS[0],PARAMS[1],PARAMS[-1]):
        for mode in ('low','high','vonly'):
            for eps in (.001,.0001):
                refs=[simulate(pars,'fd','original',True,h,n,mode,eps) for h,n in ((.125,256),(.0625,512),(.03125,1024))]
                # Independent model and time-step controls at the finest resolution.
                other=simulate(pars,'structure','compatible',True,.03125,1024,mode,eps)
                half=simulate(pars,'fd','original',True,.03125,1024,mode,eps,dt=.0000625)
                variants=[('structure','original',False),('structure','compatible',False),
                          ('structure','original',True),('structure','compatible',True),('fd','original',False),('fd','original',True)]
                rows=[simulate(pars,mo,cl,bal,.125,256,mode,eps) for mo,cl,bal in variants]
                for row in rows:row['comparison']=compare(row,half)
                controls={'coarse_vs_mid':compare(refs[0],refs[1]),'mid_vs_fine':compare(refs[1],half),
                          'model_agreement':compare(other,half),'dt_agreement':compare(refs[-1],half)}
                group={'pars':asdict(pars),'mode':mode,'eps':eps,'references':refs+[other,half], 'controls':controls,'variants':rows}
                groups.append(group);save('parametric_perturbations',groups)
                print('perturb groups',len(groups),'/18',flush=True)

if __name__=='__main__':main()
