"""Complete initial defects and time evolution of the full-potential reconstruction."""
from pathlib import Path
import sys,json,time
import numpy as np
from probe import Model,fields,HALF_WIDTHS,invert,transform,primitive,A,Ap
HERE=Path(__file__).resolve().parent
OUT=HERE/'rerun_20261024';OUT.mkdir(exist_ok=True)

def make(case,dx,h):
    m=Model(case,'Centered-SD',dx,h);m.gauge='mean'
    u=m.initial()[0];ye=(m.y[1:]+m.y[:-1])/2;v=m.profile(ye)[1]
    _,g=m.G.tau(m.y[:1]/h-.5,m.x,0,False)
    w0=4*m.G.cov(g,0,2)[0]
    w,it,res=invert(m,u,v,w0)
    return m,np.array([u,w]),dict(inverse_residual=res,inverse_iterations=it,map_residual=float(np.max(abs(transform(m,u,w)-v))))

def rhs(m,t,z):
    u,w=z;h=m.h
    coupling=np.diff(u,axis=0)/h+(w[1:]+w[:-1])/2
    r=-np.diff(m.d1(u*u/2+2*m.a*u+h*h*A(w)),axis=0)/h-m.d2(coupling)
    _,bt=m.boundary(t)
    ut=np.concatenate((bt[1:2],bt[1:2]+h*np.cumsum(r,axis=0)))
    wt=m.d2(w)-m.d1((u+2*m.a)*w-4*u)
    return np.array([ut,wt])

def physical_rates(m,z,dz):
    u,w=z;ut,wt=dz
    vt=np.diff(ut,axis=0)/m.h+(wt[1:]+wt[:-1])/2+m.h*primitive(m,np.diff(Ap(w)*wt,axis=0))
    return ut,vt

def norms(m,u,v):
    r=HALF_WIDTHS[m.case];ye=(m.y[1:]+m.y[:-1])/2
    xx=abs(m.x)<=r
    return [float(np.max(abs(u[abs(m.y)<r][:,xx]))),float(np.max(abs(v[abs(ye)<r][:,xx])))]

def spatial(case,dx,h):
    start=time.perf_counter();m,z,checks=make(case,dx,h)
    ye=(m.y[1:]+m.y[:-1])/2;dz=rhs(m,0,z);ut,vt=physical_rates(m,z,dz)
    truth=np.concatenate([fields(m,ye[i:i+32])[2][1] for i in range(0,len(ye),32)])
    v=transform(m,*z)
    endpoint=-np.diff(m.d1(z[0]*z[0]/2+2*m.a*z[0]),axis=0)/h-m.d2(v)
    checks['first_equation_identity']=float(np.max(abs(np.diff(ut,axis=0)/h-endpoint)))
    eps=1e-6
    push=(transform(m,*(z+eps*dz))-transform(m,*(z-eps*dz)))/(2*eps)
    checks['chain_rule_difference']=float(np.max(abs(push-vt)))
    assert checks['map_residual']<1e-9 and checks['first_equation_identity']<1e-7 and checks['chain_rule_difference']<1e-6,checks
    rec=dict(case=case,method='Centered-SD',dx=dx,h=h,t=0,total=norms(m,ut-m.ut(m.y,0),vt-truth),checks=checks,status='complete',seconds=time.perf_counter()-start)
    (OUT/f'spatial_{case}_{dx:g}_{h:g}.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec),flush=True)
    return m,z

def temporal(case,method,m,z0):
    start=time.perf_counter();z=z0.copy();dt=1e-4;T=.01;mr=0;mi=0;reached=0;status='complete'
    with np.errstate(over='raise',invalid='raise',divide='raise'):
      try:
       for i in range(100):
        t=i*dt
        if method=='Euler':z=z+dt*rhs(m,t,z)
        elif method=='RK4':
            k1=rhs(m,t,z);k2=rhs(m,t+dt/2,z+dt*k1/2);k3=rhs(m,t+dt/2,z+dt*k2/2);k4=rhs(m,t+dt,z+dt*k3)
            z=z+dt*(k1+2*k2+2*k3+k4)/6
        else:
            f=rhs(m,t,z);cand=z+dt*f
            for it in range(1,101):
                res=cand-z-dt*(f+rhs(m,t+dt,cand))/2;rn=float(np.max(abs(res)))
                if rn<1e-12:break
                cand-=res
            else:raise RuntimeError('implicit solve failed')
            mr=max(mr,rn);mi=max(mi,it);z=cand
        reached=(i+1)*dt
        if np.max(abs(z))>1e6:raise RuntimeError('amplitude threshold')
      except (FloatingPointError,RuntimeError) as exc:
       status=str(exc)
    rec=dict(case=case,method=method,spatial='Centered-SD full potential',state='U,w; w lower trace evolved by its equation',dx=.1,h=.1,dt=dt,T=T,reached=reached,status=status,cn_max_residual=mr,cn_max_iterations=mi,seconds=time.perf_counter()-start)
    if status=='complete':
        ye=(m.y[1:]+m.y[:-1])/2;v=transform(m,*z)
        rec['error']=norms(m,z[0]-m.profile(m.y,T)[0],v-m.profile(ye,T)[1])
        np.savez_compressed(OUT/f'time_{case}_{method}.npz',z=z,v=v)
    (OUT/f'time_{case}_{method}.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec),flush=True)

if __name__=='__main__':
    case=sys.argv[1]
    if len(sys.argv)>2 and sys.argv[2]=='time':
        m,z,_=make(case,.1,.1)
        for alg in ['Euler','RK4','CN']:temporal(case,alg,m,z)
    else:
        for dx,h in [(.1,.1),(.1,.05),(.1,.025),(.05,.1),(.025,.1)]:spatial(case,dx,h)
