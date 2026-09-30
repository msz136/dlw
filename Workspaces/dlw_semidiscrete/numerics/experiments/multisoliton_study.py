"""Two-soliton Gram manifold versus actual structure/FD dynamics.

The exact Gram field and actual time integration are reported separately.
Run from numerics/: python -u experiments/multisoliton_study.py
"""
from pathlib import Path
import sys, json, hashlib, time
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'lib'))
from gramtau import GramRef
from multigram import TwoGram
from parametric import Parameters, rk4
from parametric_open import OpenModel

OUT = ROOT/'out'
OUT.mkdir(exist_ok=True)


class TwoModel(OpenModel):
    def __init__(self, h, nx, model):
        super().__init__(Parameters(a=4.,p=1.,q=2.,rho=3.), h, nx,
                         L=20., yhalf=1.5, model=model)
        self.G = TwoGram(h=h)


def inf(a):
    return float(np.max(np.abs(a)))


def verify_reference():
    rows=[]
    for h in (.25,.125):
        fast=TwoGram(h=h)
        slow=GramRef([1,2],[1,3],[3,4],4,h)
        x=np.linspace(-7,7,19)
        for t in (-.03,0,.02):
            js=[-3,0,2]
            u,v=fast.uv(js,x,t)
            ut,vt=fast.uv(js,x,t,True)
            errs=[inf(u-slow.u_block(js,x,t)),inf(v-slow.v_block(js,x,t)),
                  inf(ut-np.asarray([[slow.u_t(j,float(xx),t) for xx in x] for j in js]))]
            # Independently verify the v tangent against a convergent time difference.
            eps=1e-4
            fd1=(fast.uv(js,x,t+eps)[1]-fast.uv(js,x,t-eps)[1])/(2*eps)
            fd2=(fast.uv(js,x,t+eps/2)[1]-fast.uv(js,x,t-eps/2)[1])/eps
            err_vt=inf(vt-fd2)
            if max(errs)>3e-11 or err_vt>3e-6 or err_vt>inf(vt-fd1)/2+2e-8:
                raise AssertionError((h,t,errs,err_vt))
            rows.append({'h':h,'t':t,'u_v_ut_max_error':max(errs),
                         'vt_fd_error':err_vt})
    return rows


def diagnostics(m,z,t):
    uv=m.fields(z,t);exact=m.G.uv(m.js,m.X.x,t)
    amp=[inf(a) for a in m.G.uv(m.js,m.X.x,0)]
    err=[inf(a-b) for a,b in zip(uv,exact)]
    return {'t':t,'u_inf':err[0],'v_inf':err[1],
            'u_relative':err[0]/amp[0],'v_relative':err[1]/amp[1],
            'passes_one_percent':bool(all(err[i]<=.01*amp[i] for i in range(2)))}


def advance(fun,z,dt,steps):
    rows=[]
    for k in range(steps):
        with np.errstate(over='ignore',invalid='ignore'):
            z=rk4(fun,k*dt,z,dt)
        if not np.all(np.isfinite(z)) or inf(z)>1e3:
            return z,rows,False
        if (k+1)*dt >= .005-1e-12 and (k+1)%round(.005/dt)==0:
            rows.append((round((k+1)*dt,10),z.copy()))
    return z,rows,True


def background(h,nx,model,dt=.00005,T=.01):
    m=TwoModel(h,nx,model)
    z0=m.exact(0)
    defect=m.rhs(0,z0)-m.exact(0,True)
    du,dv=m.error_fields(defect)
    start=time.perf_counter()
    _,traj,complete=advance(m.rhs,z0,dt,round(T/dt))
    observations=[diagnostics(m,z,t) for t,z in traj]
    return {'h':h,'nx':nx,'model':model,'dt':dt,'T':T,'complete':complete,
            'defect_state_inf':inf(defect),'defect_u_inf':inf(du),'defect_v_inf':inf(dv),
            'observations':observations,'seconds':time.perf_counter()-start}


def defect_only(h,nx,model):
    m=TwoModel(h,nx,model)
    residual=m.rhs(0,m.exact(0))-m.exact(0,True)
    du,dv=m.error_fields(residual)
    return {'h':h,'nx':nx,'model':model,'u_inf':inf(du),'v_inf':inf(dv)}


def seed(m,mode,eps):
    y=m.y[:,None]; x=m.X.x[None,:]
    envelope=np.where(abs(y)<.9, np.exp(1-1/np.maximum(1-(y/.9)**2,1e-30)),0)
    k=(2 if mode=='low' else 16)*2*np.pi/20
    f=envelope*np.exp(-x*x/4)*np.cos(k*x)
    eta=eps*f; nu=.3*eps*f
    p=np.diff(eta,axis=0)/m.h
    q=nu-m.dy(eta,(np.zeros(m.X.n),np.zeros(m.X.n))) if m.model=='structure' else nu
    return m.pack(p,q)


def perturb(h,nx,model,mode,eps=.0001,dt=.00005,T=.01):
    m=TwoModel(h,nx,model)
    e0=seed(m,mode,eps)
    linear=lambda t,e:m.delta(t,m.exact(t),e,True)
    nonlinear=lambda t,e:m.delta(t,m.exact(t),e,False)
    _,lin,lc=advance(linear,e0.copy(),dt,round(T/dt))
    _,non,nc=advance(nonlinear,e0.copy(),dt,round(T/dt))
    obs=[]
    for (t,el),(_,en) in zip(lin,non):
        ul,vl=m.error_fields(el);un,vn=m.error_fields(en)
        obs.append({'t':t,'linear_u_inf':inf(ul),'linear_v_inf':inf(vl),
                    'nonlinear_u_inf':inf(un),'nonlinear_v_inf':inf(vn),
                    'nonlinear_minus_linear_u':inf(un-ul),
                    'nonlinear_minus_linear_v':inf(vn-vl)})
    return {'h':h,'nx':nx,'model':model,'mode':mode,'eps':eps,
            'linear_complete':lc,'nonlinear_complete':nc,'observations':obs}


def main():
    verification=verify_reference()
    backgrounds=[]
    for h,nx in ((.25,64),(.25,128),(.125,128)):
        for model in ('structure','fd'):
            row=background(h,nx,model)
            backgrounds.append(row)
            print('background',h,nx,model,'complete',row['complete'],
                  'defect v',row['defect_v_inf'],
                  'last',row['observations'][-1] if row['observations'] else None,flush=True)
    # The x-refined check tests whether the manifold advantage survives an
    # actual (short) trajectory, not just a right-hand-side evaluation.
    for model in ('structure','fd'):
        row=background(.25,512,model,dt=.000025,T=.005)
        backgrounds.append(row)
        print('refined background',model,row['observations'][-1],flush=True)
    defects=[]
    for h in (.25,.125):
        for nx in (128,256,512):
            for model in ('structure','fd'):
                row=defect_only(h,nx,model)
                defects.append(row)
                print('defect',row,flush=True)
    step_controls=[]
    for model in ('structure','fd'):
        row=background(.25,128,model,dt=.000025)
        coarse=next(b for b in backgrounds if b['h']==.25 and b['nx']==128 and b['model']==model)
        step_controls.append({'model':model,'fine':row['observations'],
                              'coarse_minus_fine_u_error':abs(coarse['observations'][-1]['u_inf']-row['observations'][-1]['u_inf']),
                              'coarse_minus_fine_v_error':abs(coarse['observations'][-1]['v_inf']-row['observations'][-1]['v_inf'])})
        print('step control',step_controls[-1]['model'],
              step_controls[-1]['coarse_minus_fine_u_error'],
              step_controls[-1]['coarse_minus_fine_v_error'],flush=True)
    perturbations=[]
    for mode in ('low','high'):
        for model in ('structure','fd'):
            row=perturb(.25,128,model,mode)
            perturbations.append(row)
            print('perturb',mode,model,row['observations'][-1] if row['observations'] else None,flush=True)
    sources=[Path(__file__),ROOT/'lib/multigram.py',ROOT/'lib/parametric.py',
             ROOT/'lib/parametric_open.py',ROOT/'lib/gramtau.py']
    result={'scope':'finite-h N=2 Gram background; short-time open-chain actual and balanced dynamics',
            'verification':verification,'backgrounds':backgrounds,'defect_refinement':defects,
            'step_controls':step_controls,'perturbations':perturbations,
            'sources_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    (OUT/'multisoliton_study.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('wrote out/multisoliton_study.json',flush=True)


if __name__=='__main__':main()
