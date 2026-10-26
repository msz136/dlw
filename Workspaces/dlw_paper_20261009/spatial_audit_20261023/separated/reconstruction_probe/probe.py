"""Exact staggered field map of Centered-SD; exploratory initial tests."""
from pathlib import Path
import sys,json,time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run_separated import Model,fields,HALF_WIDTHS
HERE=Path(__file__).resolve().parent

def primitive(m,f):
    if getattr(m,'gauge','mean')=='local':return np.zeros_like(f)
    mult=np.zeros_like(m.freq,dtype=complex);mult[1:]=-1j/m.freq[1:];mult[-1]=0
    result=np.fft.irfft(np.fft.rfft(f,axis=-1)*mult,n=m.nx,axis=-1)
    return result-result[...,:1] if getattr(m,'gauge','mean')=='left' else result
def A(w):return w*w/32-w/4
def Ap(w):return w/16-.25
def transform(m,u,w):
    return np.diff(u,axis=0)/m.h+(w[1:]+w[:-1])/2+m.h*primitive(m,np.diff(A(w),axis=0))
def rates(m,u,w):
    _,bt=m.boundary(0);h=m.h
    r=-np.diff(m.d1(u*u/2+2*m.a*u+h*h*A(w)),axis=0)/h-m.d2(np.diff(u,axis=0)/h+(w[1:]+w[:-1])/2)
    ut=np.concatenate((bt[1:2],bt[1:2]+h*np.cumsum(r,axis=0)))
    wt=-m.d1((u+2*m.a)*w-4*u)+m.d2(w)
    Vt=np.diff(ut,axis=0)/h+(wt[1:]+wt[:-1])/2+h*primitive(m,np.diff(Ap(w)*wt,axis=0))
    return ut,wt,Vt

def invert(m,u,V,w0):
    w=np.empty_like(u);w[0]=w0;maxit=0;maxres=0
    for k in range(1,len(u)):
        rhs=2*(V[k-1]-(u[k]-u[k-1])/m.h)-w[k-1]+2*m.h*primitive(m,A(w[k-1]))
        if getattr(m,'gauge','mean')=='local':
            w[k]=rhs;maxit=1;continue
        cand=w[k-1].copy()
        for it in range(200):
            nxt=rhs-2*m.h*primitive(m,A(cand))
            # Damping allows a wider range than undamped fixed-point iteration.
            res=float(np.max(abs(nxt-cand)))
            if res<2e-12:break
            cand=.5*cand+.5*nxt
            if not np.isfinite(cand).all() or np.max(abs(cand))>1e5:raise ValueError('inverse diverged')
        else:raise ValueError(f'inverse did not converge at row {k}, residual {res}')
        w[k]=cand;maxit=max(maxit,it+1);maxres=max(maxres,res)
    return w,maxit,maxres

def test(case,h,gauge='mean'):
    m=Model(case,'Centered-SD',.1,h);m.gauge=gauge;start=time.perf_counter()
    u=m.initial()[0];ye=(m.y[1:]+m.y[:-1])/2
    V=m.profile(ye)[1]
    # Boundary w equals continuous v-u_y=4(log g)_xy.
    _,g=m.G.tau(m.y[:1]/h-.5,m.x,0,False)
    w0=4*m.G.cov(g,0,2)[0]
    row=dict(case=case,h=h,dx=.1,boundary='w0=continuous v-u_y',primitive=gauge+' gauge; Fourier Nyquist zero')
    try:
        w,it,res=invert(m,u,V,w0)
        row.update(inverse_iterations_max=it,inverse_residual=res,map_residual=float(np.max(abs(transform(m,u,w)-V))))
        ut,wt,vt=rates(m,u,w)
        eu=m.ut(m.y,0)
        # Analytic vt from exponential-sum mixed moments, in small y blocks.
        ev=np.concatenate([fields(m,ye[i:i+64])[2][1] for i in range(0,len(ye),64)])
        maskx=abs(m.x)<=HALF_WIDTHS[case];mu=abs(m.y)<HALF_WIDTHS[case];mv=abs(ye)<HALF_WIDTHS[case]
        row['defects']=[float(np.max(abs((ut-eu)[mu][:,maskx]))),float(np.max(abs((vt-ev)[mv][:,maskx])))]
        # Exact algebraic identity under the actual Fourier operators.
        endpoint=-np.diff(m.d1(u*u/2+2*m.a*u),axis=0)/h-m.d2(V)
        if gauge=='local':endpoint-=h*np.diff(m.d1(A(w)),axis=0)
        row['first_equation_identity']=float(np.max(abs(np.diff(ut,axis=0)/h-endpoint)))
        eps=1e-6
        fd=(transform(m,u+eps*ut,w+eps*wt)-transform(m,u-eps*ut,w-eps*wt))/(2*eps)
        row['pushforward_check']=float(np.max(abs(fd-vt)))
        row['status']='complete'
    except ValueError as exc:row.update(status='failed',reason=str(exc))
    row['seconds']=time.perf_counter()-start
    suffix='' if gauge=='mean' else '_'+gauge
    (HERE/f'{case}_{h:g}{suffix}.json').write_text(json.dumps(row,indent=2));print(json.dumps(row),flush=True)

if __name__=='__main__':
    for case in 'ABCD':
      for h in [.1,.05,.025]:test(case,h,sys.argv[1] if len(sys.argv)>1 else 'mean')
