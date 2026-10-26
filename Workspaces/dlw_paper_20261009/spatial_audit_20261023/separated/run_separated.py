"""Initial operator defects and Centered-SD time comparisons; no fitted references."""
from pathlib import Path
import sys, json, math, time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from run import Model, CASES, HALF_WIDTHS, step
HERE=Path(__file__).resolve().parent

def fields(m,y,t=0):
    """u,v x-jets (value, first, second derivative), and exact time rates.
    Derivatives are analytic exponential-sum moments, not x finite differences.
    """
    logs=[]; ratios=[]; times=[]
    for isf in (True,False):
        _,w=m.G.tau(np.asarray(y)/m.h-.5,m.x,t,isf)
        s,o,e=[m.G.rates[:,i,None,None] for i in range(3)]
        E=lambda f:np.sum(w*f,axis=0)
        T=[E(s**n)/math.factorial(n) for n in range(4)]
        L=[np.zeros_like(T[0])]; R=[]
        for n in range(4):
            R.append(E(e*s**n)/math.factorial(n)-sum(T[k]*R[n-k] for k in range(1,n+1)))
            if n:L.append(T[n]-sum(k*L[k]*T[n-k] for k in range(1,n))/n)
        logs.append(np.array([math.factorial(n+1)*L[n+1] for n in range(3)]))
        ratios.append(np.array([math.factorial(n+1)*R[n+1] for n in range(3)]))
        ut=E(s*o)-E(s)*E(o)
        vt=E(s*e*o)-E(s*e)*E(o)-E(s*o)*E(e)-E(e*o)*E(s)+2*E(s)*E(e)*E(o)
        times.append((ut,vt))
    return 2*(logs[0]-logs[1]),2*(ratios[0]+ratios[1]),np.array([2*(times[0][0]-times[1][0]),2*(times[0][1]+times[1][1])])

def mul(a,b):return np.array([a[0]*b[0],a[1]*b[0]+a[0]*b[1],a[2]*b[0]+2*a[1]*b[1]+a[0]*b[2]])

def analytic_rhs(m,u,v):
    h,a=m.h,m.a
    ub,_,tb=fields(m,[m.y[0]-h,m.y[0],m.y[-1]+h])
    cent=lambda f,left,right: (np.concatenate((f[:,1:],right[:,None]),axis=1)-np.concatenate((left[:,None],f[:,:-1]),axis=1))/(2*h)
    du=np.diff(u,axis=1)/h
    if m.method=='Centered-SD':
        w=v-cent(u,ub[:,0],ub[:,-1]); H=mul(u,u)/2+2*a*u+h*h*(mul(w,w)/32-w/4)
        r=-np.diff(H[1],axis=0)/h-(du[2]+(w[2,1:]+w[2,:-1])/2)
    else:
        H=mul(u,u)/2+2*a*u
        r=-np.diff(H[1],axis=0)/h-(v[2,1:] if m.method=='Endpoint-SD' else (v[2,1:]+v[2,:-1])/2)
    ut=np.concatenate((tb[0,1:2],tb[0,1:2]+h*np.cumsum(r,axis=0)))
    if m.method=='Centered-SD':
        # Time derivative of the same background-plus-perturbation ghost rule.
        _,bt=m.boundary(0)
        vt=-(mul(u,w)+2*a*w-4*u)[1]+w[2]+m.centered(ut,bt)
    elif m.method=='FD':vt=-(mul(u,v)+2*a*v-4*u)[1]-cent(u,ub[:,0],ub[:,-1])[2]
    else:
        prev=np.concatenate((ub[:,0:1],u[:,:-1]),axis=1); avg=(u+prev)/2;p=(u-prev)/h
        vt=-(mul(avg,v)+(2*a-2*h)*v+h*mul(v,v)/4-4*avg-h*mul(p,p)/4)[1]-p[2]
    return np.array([ut,vt])

def norm(m,z):
    return [float(np.max(abs(z[j][(abs(yy)<HALF_WIDTHS[m.case])][:,abs(m.x)<=HALF_WIDTHS[m.case]]))) for j,yy in enumerate((m.y,m.yv))]

def spatial():
    oldpath=HERE/'spatial.json'
    old=json.loads(oldpath.read_text()) if oldpath.exists() else []
    if old:
        import shutil,datetime
        archive=HERE/'backups'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        archive.mkdir(parents=True,exist_ok=True)
        shutil.copy2(oldpath,archive/oldpath.name)
    records=[]
    for case in CASES:
      for method in ('Endpoint-SD','Centered-SD','FD'):
       for dx,h in ((.1,.1),(.1,.05),(.1,.025),(.05,.1),(.025,.1)):
        cached=next((r for r in old if r['case']==case and r['method']==method and r['dx']==dx and r['h']==h),None)
        if cached is not None:
            records.append(cached);continue
        m=Model(case,method,dx,h)
        u,_,tu=fields(m,m.y); _,v,tv=fields(m,m.yv)
        z=np.array([u[0],v[0]]); truth=np.array([tu[0],tv[1]])
        ya=analytic_rhs(m,u,v); full=m.rhs(0,z)
        ey=ya-truth; ex=full-ya; total=full-truth
        rec=dict(case=case,method=method,dx=dx,h=h,t=0,Y=norm(m,ey),X=norm(m,ex),total=norm(m,total))
        records.append(rec); print(json.dumps(rec),flush=True)
    (HERE/'spatial.json').write_text(json.dumps(records,indent=2))

def temporal(case,method,dt=1e-4):
    dest=HERE/f'time_{case}_{method}_{dt:g}.json'
    if dest.exists():return
    m=Model(case,'Centered-SD',.1,.1);z=m.initial();start=time.perf_counter();maxres=0;maxiter=0;iterations=0
    status='complete';done=0
    with np.errstate(over='ignore',invalid='ignore'):
      for i in range(round(.01/dt)):
        t=i*dt
        if method=='Euler':z=z+dt*m.rhs(t,z)
        elif method=='RK4':z=step(m,t,z,dt)
        else:
            f=m.rhs(t,z);candidate=z+dt*f
            for it in range(1,101):
                res=candidate-z-dt*(f+m.rhs(t+dt,candidate))/2
                rn=float(abs(res).max())
                if rn<1e-12:break
                candidate-=res
            else:
                status='implicit_solve_failed';break
            maxres=max(maxres,rn);maxiter=max(maxiter,it);iterations+=it;z=candidate
        done=(i+1)*dt
        if not np.isfinite(z).all() or np.max(abs(z))>1e6:status='nonfinite_or_threshold';break
    rec=dict(case=case,method=method,dx=.1,h=.1,dt=dt,T=.01,reached=done,status=status,seconds=time.perf_counter()-start,cn_max_residual=maxres,cn_max_iterations=maxiter,cn_total_iterations=iterations)
    if status=='complete':
        rec['error']=norm(m,z-m.profile(m.y,.01))
        np.savez_compressed(dest.with_suffix('.npz'),z=z)
    dest.write_text(json.dumps(rec,indent=2));print(json.dumps(rec),flush=True)

def validate():
    m=Model('A','Centered-SD',.2,.1); u,v,tt=fields(m,m.y)
    assert np.max(abs(np.array([u[0],v[0]])-m.initial()))<1e-12
    eps=1e-5
    td=(m.profile(m.y,eps)-m.profile(m.y,-eps))/(2*eps)
    err=float(np.max(abs(td-tt)));assert err<1e-7,err
    # Check exact x-jets against centered evaluation of the analytic formula.
    xp=m.profile(m.y,0,m.x+eps);xm=m.profile(m.y,0,m.x-eps)
    errx=float(np.max(abs((xp-xm)/(2*eps)-np.array([u[1],v[1]]))))
    assert errx<1e-7,errx
    (HERE/'validation.json').write_text(json.dumps(dict(time_derivative_check=err,x_derivative_check=errx),indent=2))

if __name__=='__main__':
    if sys.argv[1]=='spatial':validate();spatial()
    else:temporal(sys.argv[1],sys.argv[2],float(sys.argv[3]) if len(sys.argv)>3 else 1e-4)
