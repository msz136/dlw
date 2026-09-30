"""Parameter study, pointwise error attribution and forced tangent prediction."""
from pathlib import Path
import sys,json,hashlib,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'lib'))
import numpy as np
from dataclasses import asdict
from parametric import Parameters,Exact,Model,rk4
from dynamics import Problem
from gramtau import GramRef,ContRef

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'out'
PARAMS=[Parameters(),Parameters(p=2,q=3,rho=5),Parameters(a=3),Parameters(a=6),
        Parameters(p=.5,q=1,rho=1.5),Parameters(p=1,q=3,rho=4),
        Parameters(p=2,q=1,rho=3),Parameters(rho=.3),Parameters(rho=30),
        Parameters(a=2,p=1.5,q=2,rho=3.5)]

def save(name,data):
    paths=[Path(__file__),ROOT/'lib/parametric.py',ROOT/'lib/dynamics.py',ROOT/'lib/solver.py']
    (OUT/(name+'.json')).write_text(json.dumps({'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'data':data},indent=2,allow_nan=False),encoding='utf-8')

def inf(z):return float(np.max(abs(z)))

def verify():
    checks={};rng=np.random.default_rng(230923)
    for k,pars in enumerate(PARAMS):
        for cont in (False,True):
            m=Model(pars,nx=32,continuous=cont)
            slow=ContRef([pars.p],[pars.q],[pars.rho],pars.a) if cont else GramRef([pars.p],[pars.q],[pars.rho],pars.a,.25)
            u,v=m.G.uv([-2,0,2],m.X.x,.013)
            for i,j in enumerate([-2,0,2]):
                us=slow.u0_row((j+.5)*.25,m.X.x,.013) if cont else slow.u_row(j,m.X.x,.013)
                vs=slow.v0_row((j+.5)*.25,m.X.x,.013) if cont else slow.v_row(j,m.X.x,.013)
                assert max(inf(u[i]-us),inf(v[i]-vs))<2e-11
            d=m.exact(.013,True);eps=1e-5
            num=(m.exact(.013-2*eps)-8*m.exact(.013-eps)+8*m.exact(.013+eps)-m.exact(.013+2*eps))/(12*eps)
            assert inf(d-num)<3e-8
    checks['general_exact_and_analytic_time_derivatives']=True
    for model in ('structure','fd'):
        for closure in ('original','compatible'):
            m=Model(model=model,closure=closure,nx=32)
            z=m.exact(.01);e=rng.normal(size=z.size)*.001
            assert inf(m.delta(.01,z,e)-(m.rhs(.01,z+e)-m.rhs(.01,z)))<1e-12
            j=m.delta(.01,z,e,True)
            assert inf(j-(m.rhs(.01,z+e)-m.rhs(.01,z-e))/2)<1e-12
            fu,fv=m.fields(z+e,.01);bu,bv=m.fields(z,.01);eu,ev=m.error_fields(e)
            assert max(inf(fu-bu-eu),inf(fv-bv-ev))<1e-13
    checks['algebraic_delta_jacobian_and_physical_error_map']=True
    for model in ('structure','fd'):
        old=Problem(model=model,nx=64);m=Model(model=model,nx=64)
        z=m.exact(0);P,Q=m.unpack(z)
        assert inf(m.rhs(0,z)-m.pack(*old.rhs(0,P,Q)))<1e-12
    checks['historical_rhs_equivalence']=True
    # Endpoint identity: dy R p = adjacent mean inside; cumulative sum at right.
    m=Model(nx=32);p=rng.normal(size=(len(m.js)-1,32));q=np.zeros(m.shape)
    u,v=m.error_fields(m.pack(p,q))
    assert inf(v[1:-1]-(p[:-1]+p[1:])/2)<1e-14
    assert inf(v[-1]+np.sum(p[:-1],axis=0)/2)<1e-14
    checks['exact_interior_and_boundary_reconstruction_identity']=True
    save('parametric_verification',checks);print(checks,flush=True)

def diagnostics(m,t,z,lin):
    exact=m.exact(t);e=z-exact;eu,ev=m.error_fields(e);lu,lv=m.error_fields(lin)
    P,Q=m.unpack(e);n=len(m.js)
    dy=m.dy(eu,(np.zeros(m.X.n),np.zeros(m.X.n)))
    row={'t':t,'u':inf(eu),'v':inf(ev),'P':inf(P),'Q':inf(Q),
         'linear_u_relative_mismatch':inf(eu-lu)/max(inf(eu),1e-30),
         'linear_v_relative_mismatch':inf(ev-lv)/max(inf(ev),1e-30),
         'dy_eu':inf(dy),'boundary_v':inf(ev[[0,-1]]),
         'interior_v':inf(ev[abs(m.y)<=.75]),
         'u_bound':(n-1)*m.h*inf(P),
         'v_bound':inf(Q)+(max(1,(n-2)/2)*inf(P) if m.model=='structure' else 0)}
    idx=np.unravel_index(np.argmax(abs(ev)),ev.shape)
    row.update(v_peak_y=float(m.y[idx[0]]),v_peak_x=float(m.X.x[idx[1]]),
               Q_at_v_peak=float(Q[idx]),dy_at_v_peak=float(dy[idx]),v_at_peak=float(ev[idx]))
    if m.model=='structure':assert inf(ev-Q-dy)<1e-12
    assert row['u']<=row['u_bound']+1e-12 and row['v']<=row['v_bound']+1e-12
    return row

def run(pars,h,nx,model,closure,yhalf=1.5,T=.02):
    # Common continuous fields for comparing models; own exact finite-h background
    # is used in a separate scan to distinguish model defect from x truncation.
    m=Model(pars,h,nx,model=model,closure=closure,yhalf=yhalf,continuous=True)
    z=m.exact(0);lin=np.zeros_like(z);dt=.000125
    hist=[];complete=True;start=time.perf_counter()
    for i in range(round(T/dt)):
        t=i*dt
        def forced(t,e):
            bg=m.exact(t)
            return m.delta(t,bg,e,True)+m.rhs(t,bg)-m.exact(t,True)
        new=rk4(m.rhs,t,z,dt);nl=rk4(forced,t,lin,dt)
        if not np.all(np.isfinite(new)) or max(inf(new),inf(nl))>1e3:
            complete=False;break
        z,lin=new,nl
        if (i+1)%40==0:hist.append(diagnostics(m,(i+1)*dt,z,lin))
    cfg={'pars':asdict(pars),'h':h,'nx':nx,'model':model,'closure':closure,'yhalf':yhalf,'continuous_data':True}
    ident=hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()[:12]
    np.savez_compressed(OUT/('parametric_'+ident+'.npz'),state=z,linear=lin,exact=m.exact((i+1)*dt if complete else i*dt),x=m.X.x,y=m.y)
    return dict(config=cfg,history=hist,complete=complete,final_t=(i+1)*dt if complete else i*dt,
                seconds=time.perf_counter()-start,fields='parametric_'+ident+'.npz')

def main():
    verify();rows=[]
    configs=[(p,h,nx,mo,cl) for p in PARAMS for h in (.25,.125,.0625)
             for nx in (128,256) for mo,cl in [('structure','original'),('structure','compatible'),('fd','original')]]
    for i,args in enumerate(configs):
        rows.append(run(*args))
        if (i+1)%9==0:
            save('parametric_scan',rows);print('scan',i+1,'/',len(configs),flush=True)
    save('parametric_scan',rows)

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='verify':verify()
    else:main()
