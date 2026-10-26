"""Six-case fixed-grid audit. Physical u,v state, Fourier x derivatives.
No filtering; fixed analytical background plus quadratic perturbation extrapolation
at the upper ghost site for Centered-SD/FD. Endpoint-SD is backward/open-chain.
"""
from pathlib import Path
import sys, json, time, hashlib
import numpy as np
import pandas as pd
from scipy.special import logsumexp
from scipy.sparse import coo_matrix
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'paper_comparison_20261022/solver_snapshot.py'
exec(compile(SOURCE.read_text(encoding='utf8').split('# spatial')[0],str(SOURCE),'exec'))

class Model:
    def __init__(self,case,method,dx=.2,h=.1):
        self.case,self.method,self.h=case,method,h
        self.exact=case in CASES
        self.a=2. if self.exact else 1/3
        self.half=COMPUTE_HALF_WIDTHS[case] if self.exact else 96.
        self.nx=round(2*self.half/dx); self.nx+=self.nx%2
        self.x=np.linspace(-self.half,self.half,self.nx,endpoint=False)
        self.dx=2*self.half/self.nx
        self.y=np.arange(round(-self.half/h),round(self.half/h))*h+h/2 if self.exact else np.arange(round(4/h)+1)*h-2
        self.yv=self.y-h/2 if method=='Endpoint-SD' else self.y.copy()
        self.freq=2*np.pi*np.fft.rfftfreq(self.nx,self.dx)
        self.m1=1j*self.freq; self.m1[-1]=0
        self.m2=-self.freq**2
        self.G=Exact(case,h,self.a) if self.exact else None
        self.cache={}
    def d1(self,f):return np.fft.irfft(np.fft.rfft(f,axis=-1)*self.m1,n=self.nx,axis=-1)
    def d2(self,f):return np.fft.irfft(np.fft.rfft(f,axis=-1)*self.m2,n=self.nx,axis=-1)
    def profile(self,y,t=0.,x=None):
        x=self.x if x is None else x
        if self.exact:return np.array(self.G.uv(np.asarray(y)/self.h-.5,x,t))
        e=np.sin(np.pi*(np.asarray(y)+2)/4)[:,None]
        if self.case=='Gaussian':return np.array([.05*e*np.exp(-(x/6)**2),.03*e*np.exp(-(x/6)**2)])
        return np.array([.03*e*np.cos(2*np.pi*x/24),.02*e*np.sin(2*np.pi*x/24)])
    def ut(self,y,t):
        if not self.exact:return np.zeros((len(y),self.nx))
        _,f=self.G.tau(np.array(y)/self.h-.5,self.x,t,True)
        _,g=self.G.tau(np.array(y)/self.h-.5,self.x,t)
        return 2*(self.G.cov(f,0,1)-self.G.cov(g,0,1))
    def boundary(self,t):
        if t not in self.cache:
            yy=np.r_[self.y[0]-self.h,self.y[0],self.y[-3:],self.y[-1]+self.h]
            self.cache[t]=(self.profile(yy,t)[0],self.ut(yy,t))
            if len(self.cache)>12:self.cache.pop(next(iter(self.cache)))
        return self.cache[t]
    def initial(self):return np.array([self.profile(self.y)[0],self.profile(self.yv)[1]])
    def centered(self,u,b):
        right=b[-1]+3*(u[-1]-b[-2])-3*(u[-2]-b[-3])+(u[-3]-b[-4])
        ext=np.concatenate((b[:1],u,right[None]))
        return (ext[2:]-ext[:-2])/(2*self.h)
    def rhs(self,t,z):
        u,v=z; h=self.h; a=self.a
        b,bt=self.boundary(t)
        du=np.diff(u,axis=0)/h
        if self.method=='Centered-SD':
            w=v-self.centered(u,b)
            H=u*u/2+2*a*u+h*h*(w*w/32-w/4)
            r=-np.diff(self.d1(H),axis=0)/h-self.d2(du+(w[1:]+w[:-1])/2)
        else:
            r=-np.diff(self.d1(u*u/2+2*a*u),axis=0)/h-self.d2(v[1:] if self.method=='Endpoint-SD' else (v[1:]+v[:-1])/2)
        ut=np.concatenate((bt[1:2],bt[1:2]+h*np.cumsum(r,axis=0)))
        if self.method=='Centered-SD':
            vt=-self.d1((u+2*a)*w-4*u)+self.d2(w)+self.centered(ut,bt)
        elif self.method=='FD':vt=-self.d1((u+2*a)*v-4*u)-self.d2(self.centered(u,b))
        else:
            prev=np.concatenate((b[:1],u[:-1])); avg=(u+prev)/2; p=(u-prev)/h
            vt=-self.d1((avg+2*a-2*h)*v+h*v*v/4-4*avg-h*p*p/4)-self.d2(p)
        return np.array([ut,vt])

def step(m,t,z,dt):
    k1=m.rhs(t,z);k2=m.rhs(t+dt/2,z+dt*k1/2)
    k3=m.rhs(t+dt/2,z+dt*k2/2);k4=m.rhs(t+dt,z+dt*k3)
    return z+dt*(k1+2*k2+2*k3+k4)/6

def run(case,method,variant):
    exact=case in CASES
    dx=(.2 if exact else .5)/(2 if variant in ('x_refined','x_halfdt') else 1)
    if variant.startswith('main'):dx=.1
    h=.05 if variant in ('y_refined','main_y_refined') else .1
    dt=(.0001 if exact else .001)/(2 if variant in ('halfdt','x_halfdt','main_halfdt') else 1)
    T=.01 if exact else .1
    name=f'{case}_{method}_{variant}'; dest=HERE/(name+'.json')
    if dest.exists():return
    # Reuse already-computed identical settings, retaining explicit provenance.
    reuse='x_refined' if variant=='main' and exact else ('x_halfdt' if variant=='main_halfdt' and exact else None)
    if reuse and (HERE/f'{case}_{method}_{reuse}.json').exists():
        import shutil
        old=HERE/f'{case}_{method}_{reuse}'
        rec=json.loads(old.with_suffix('.json').read_text()); rec['variant']=variant;rec['reused_from']=old.name
        if old.with_suffix('.npz').exists():shutil.copy2(old.with_suffix('.npz'),HERE/(name+'.npz'))
        dest.write_text(json.dumps(rec,indent=2));print('reused',name,flush=True);return
    m=Model(case,method,dx,h);z=m.initial();z0=z.copy();start=time.time()
    failed=None
    with np.errstate(over='ignore',invalid='ignore'):
        for i in range(round(T/dt)):
            z=step(m,i*dt,z,dt)
            if not np.isfinite(z).all() or np.max(abs(z))>1e6:
                failed=(i+1)*dt;break
    rec=dict(case=case,method=method,variant=variant,nx=m.nx,ny=len(m.y),dx=m.dx,h=h,dt=dt,T=T,a=m.a,failed_at=failed,seconds=time.time()-start)
    if not failed:
        rec['change_max']=[float(abs(z[j]-z0[j]).max()) for j in range(2)]
        if exact:
            xx=np.linspace(-HALF_WIDTHS[case],HALF_WIDTHS[case],round(2*HALF_WIDTHS[case]/.02)+1)
            errors=[]
            for j,yy in enumerate((m.y,m.yv)):
                mask=abs(yy)<HALF_WIDTHS[case]
                num=CubicSpline(m.x,z[j,mask],axis=-1)(xx)
                ref=m.profile(yy[mask],T,xx)[j]
                errors.append(float(abs(num-ref).max()))
            rec['errors']=errors
        np.savez_compressed(HERE/(name+'.npz'),z=z,z0=z0,x=m.x,y=m.y,yv=m.yv)
    dest.write_text(json.dumps(rec,indent=2),encoding='utf8')
    print(json.dumps(rec),flush=True)

def validate():
    m=Model('A','Centered-SD')
    f=np.sin(2*np.pi*m.x/(2*m.half))[None]
    err1=float(abs(m.d1(f)-2*np.pi/(2*m.half)*np.cos(2*np.pi*m.x/(2*m.half))).max())
    err2=float(abs(m.d2(f)+(2*np.pi/(2*m.half))**2*f).max())
    # Linear transform identity: v_t = w_t + delta_0 u_t, including ghost derivative.
    z=m.initial();t=.003;b,bt=m.boundary(t);ut=m.rhs(t,z)[0]
    eps=1e-6
    num=(m.centered(z[0]+eps*ut,b+eps*bt)-m.centered(z[0]-eps*ut,b-eps*bt))/(2*eps)
    identity=float(abs(num-m.centered(ut,bt)).max())
    out=dict(fourier_d1_error=err1,fourier_d2_error=err2,ghost_chain_rule_error=identity,reference_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
    assert err1<1e-12 and err2<1e-11 and identity<1e-7,out
    (HERE/'validation.json').write_text(json.dumps(out,indent=2))
    print(out,flush=True)

if __name__=='__main__':
    if len(sys.argv)==1:validate()
    else:
        case=sys.argv[1]
        for variant in ('base','halfdt','x_refined','y_refined'):
            for method in ('Endpoint-SD','Centered-SD','FD'):run(case,method,variant)
