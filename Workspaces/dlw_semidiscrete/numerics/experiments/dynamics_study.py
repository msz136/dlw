"""Reproducible extension requested in the 2026-09-23 research discussion.

Run: python -u experiments/dynamics_study.py [verify|propagation|compare|sensitivity|all]
Scientific failures are retained; verification failures raise exceptions.
"""
from pathlib import Path
import sys, os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'lib'))
import json, time, hashlib
import numpy as np
from scipy.optimize import minimize_scalar
from dynamics import Problem, Reference, Grid
from solver import integrate, XGrid, DLWChainRHS
from gramtau import GramRef, ContRef

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out'
THRESHOLD=.01  # one percent of each exact initial peak, fixed before runs


def norm(e, dx, h):
    return {'inf':float(np.max(np.abs(e))), 'l2':float(np.sqrt(dx*h*np.sum(e*e)))}


def verify():
    checks={}
    x=np.linspace(-3,3,31)
    for case,pars in [('A',([1.],[2.],[3.])),('B',([2.],[3.],[5.]))]:
        for h in (.25,.125):
            for cont in (False,True):
                fast=Reference(case,h,cont)
                slow=ContRef(*pars,4.) if cont else GramRef(*pars,4.,h)
                for t in (0.,.07):
                    u,v=fast.uv([-3,0,2],x,t)
                    for k,j in enumerate([-3,0,2]):
                        us=slow.u0_row((j+.5)*h,x,t) if cont else slow.u_row(j,x,t)
                        vs=slow.v0_row((j+.5)*h,x,t) if cont else slow.v_row(j,x,t)
                        err=max(np.max(abs(u[k]-us)),np.max(abs(v[k]-vs)))
                        assert err<2e-12,err
                checks[f'exact_{case}_{h}_{cont}']=True
    p=Problem(nx=64)
    dense=XGrid(64,20.,4)
    rng=np.random.default_rng(20260923)
    f=rng.normal(size=(12,64))
    assert np.max(abs(p.X.d1(f)-f@dense.D1.T))<1e-13
    assert np.max(abs(p.X.d2(f)-f@dense.D2.T))<1e-12
    old=DLWChainRHS(p.C,dense,p.base,lambda t:p.ghosts(t)[0],lambda t:p.ghosts(t)[1])
    old.use_ext=True; old._ple=p.op._ple; old._pre=p.op._pre
    P,Q=p.initial(); P+=rng.normal(size=P.shape)*1e-4
    for a,b in zip(p.rhs(.03,P,Q),old(.03,P,Q)):
        assert np.max(abs(a-b))<1e-11
    checks['production_RHS_and_stencil_equivalence']=True
    # Independent synthetic translation validates sign and sub-grid fitting.
    ref=Reference(); target=ref.uv([0],x-.037,.1)[0][0]
    fit=minimize_scalar(lambda s:np.sum((target-ref.uv([0],x-s,.1)[0][0])**2),
                        bounds=(-.2,.2),method='bounded',options={'xatol':1e-12})
    assert abs(fit.x-.037)<1e-8
    checks['translation_fit']=True
    # At t=0 both model states reconstruct the IDENTICAL continuous fields.
    for model in ('structure','fd'):
        p=Problem(model=model,continuous_data=True)
        P,Q=p.initial()
        for a,b in zip(p.fields(P,Q,0),p.G.uv(p.js,p.X.x,0)):
            assert np.max(abs(a-b))<1e-13
    checks['common_initial_data']=True
    # Continuous baseline local residual: jointly refine y and x, dt probe fixed.
    residual=[]
    for h,nx in ((.25,128),(.125,256),(.0625,512)):
        p=Problem(h=h,nx=nx,model='fd',continuous_data=True)
        P,Q=p.initial(); rp,rv=p.rhs(0,P,Q); eps=1e-5
        up,vp=p.G.uv(p.js,p.X.x,eps); um,vm=p.G.uv(p.js,p.X.x,-eps)
        exactp=np.diff((up-um)/(2*eps),axis=0)/h
        exactv=(vp-vm)/(2*eps)
        residual.append(max(np.max(abs(rp-exactp)),np.max(abs(rv-exactv))))
    assert residual[0]/residual[1]>3 and residual[1]/residual[2]>3,residual
    checks['fd_consistency_residuals']=residual
    yres=[]
    for h in (.5,.25,.125):
        p=Problem(h=h,nx=1024,model='fd',continuous_data=True)
        P,Q=p.initial(); rp,rv=p.rhs(0,P,Q); eps=1e-5
        up,vp=p.G.uv(p.js,p.X.x,eps);um,vm=p.G.uv(p.js,p.X.x,-eps)
        yres.append(max(float(np.max(abs(rp-np.diff((up-um)/(2*eps),axis=0)/h))),
                        float(np.max(abs(rv-(vp-vm)/(2*eps))))))
    assert yres[0]/yres[1]>3.5 and yres[1]/yres[2]>3.5,yres
    checks['fd_y_only_residuals']=yres
    # Fixed-grid temporal convergence of the new continuous-data FD baseline.
    states=[]
    for n in (4,8,16):
        p=Problem(nx=64,model='fd',continuous_data=True)
        P,Q=p.initial(); P,Q,info=integrate(p.rhs,0,.03,P,Q,.03/n)
        states.append(np.concatenate((P.ravel(),Q.ravel())))
    order=np.log2(np.max(abs(states[0]-states[1]))/np.max(abs(states[1]-states[2])))
    assert order>3.5,order
    checks['fd_time_order']=float(order)
    write('dynamics_verification',checks)
    print('VERIFIED',checks,flush=True)


def write(name,data):
    sources=[Path(__file__).resolve(),ROOT/'lib/dynamics.py',ROOT/'lib/solver.py',ROOT/'lib/gramtau.py']
    payload={'date':'2026-09-23','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'data':data}
    (OUT/(name+'.json')).write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n',encoding='utf-8')


def run(case='A',h=.25,nx=256,L=20.,T=.05,dt=.00025,model='structure',
        continuous_data=False,yhalf=1.5,fit=True):
    p=Problem(case,h,nx,L,model,continuous_data,yhalf)
    P,Q=p.initial(); amp=[float(np.max(abs(z))) for z in p.G.uv(p.js,p.X.x,0)]
    hist=[]; snapshots=[]; evolution_seconds=0.; valid=0.; first_failure=None
    t=0.; stopped=None
    def measure(t,P,Q):
        nonlocal valid,first_failure
        uv=p.fields(P,Q,t); exact=p.G.uv(p.js,p.X.x,t)
        row={'t':float(t)}
        for key,z,zstar,a in zip(('u','v'),uv,exact,amp):
            err=z-zstar; row[key]=norm(err,p.X.dx,h)
            common=(abs((p.js+.5)*h)<1.5)
            xcommon=(p.X.x>=-10)&(p.X.x<10)
            row[key]['common_region_inf']=float(np.max(abs(err[np.ix_(common,xcommon)])))
            row[key]['relative_inf']=row[key]['inf']/a
            fft=np.fft.rfft(err,axis=-1)
            cut=int(.75*(fft.shape[-1]-1))
            row[key]['high_frequency_rms']=float(np.sqrt(np.sum(abs(fft[:,cut:])**2)/err.size)/nx)
            if fit:
                # Fit complete central profile, retain global unaligned errors.
                k=np.argmin(abs((p.js+.5)*h))
                ind=0 if key=='u' else 1
                opt=minimize_scalar(lambda s:np.sum((z[k]-p.G.uv([p.js[k]],p.X.x-s,t)[ind][0])**2),
                                    bounds=(-.5,.5),method='bounded',options={'xatol':1e-10})
                row[key]['shift']=float(opt.x)
                row[key]['fit_interpretable']=bool(abs(opt.x)<.49 and row[key]['relative_inf']<.1)
                row[key]['aligned_profile_inf']=float(np.max(abs(z[k]-p.G.uv([p.js[k]],p.X.x-opt.x,t)[ind][0])))
        passed=all(row[z]['relative_inf']<=THRESHOLD for z in ('u','v'))
        if first_failure is None:
            if passed: valid=t
            else: first_failure=t
        # Same physical endpoints, exact periodic mismatch (not neighboring-node difference).
        ends=p.G.uv(p.js,[-L/2,L/2],t)
        row['exact_endpoint_mismatch']=max(float(np.max(abs(z[:,0]-z[:,1]))) for z in ends)
        row['exact_edge_amplitude']=max(float(np.max(abs(z))) for z in ends)
        hist.append(row)
        k=np.argmin(abs((p.js+.5)*h))
        snapshots.append({'t':t,'j':int(p.js[k]),'u':uv[0][k].tolist(),'v':uv[1][k].tolist(),
                          'exact_u':exact[0][k].tolist(),'exact_v':exact[1][k].tolist()})
        return uv
    uv=measure(0,P,Q)
    # All runs use the same observation spacing, including failures.
    for target in np.linspace(0,T,int(round(T/.005))+1)[1:]:
        def stop(t,P,Q):
            if not np.isfinite(P).all() or not np.isfinite(Q).all():return 'nonfinite state'
            if max(np.max(abs(P)),np.max(abs(Q)))>1e3:return 'state magnitude exceeds 1000'
        start=time.perf_counter()
        with np.errstate(over='ignore',invalid='ignore'):
            P,Q,info=integrate(p.rhs,t,float(target),P,Q,dt,stop_fn=stop)
        evolution_seconds+=time.perf_counter()-start
        t=info['final_t']
        if info['stopped']:
            stopped=info['stopped']; break
        uv=measure(t,P,Q)
    complete=stopped is None and abs(t-T)<1e-12
    last=hist[-1]['t']
    finite=Reference(case,h,False).uv(p.js,p.X.x,last)
    cont=Reference(case,h,True).uv(p.js,p.X.x,last)
    decomp={}
    for key,z,zh,z0 in zip(('u','v'),uv,finite,cont):
        a,b,c=z-zh,zh-z0,z-z0
        decomp[key]={'solver':norm(a,p.X.dx,h),'model':norm(b,p.X.dx,h),'total':norm(c,p.X.dx,h),
                     'identity_residual':float(np.max(abs(c-a-b)))}
    cfg=dict(case=case,h=h,nx=nx,L=L,T=T,dt=dt,model=model,continuous_data=continuous_data,yhalf=yhalf)
    array_name='dynamics_field_'+hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()[:12]+'.npz'
    np.savez_compressed(OUT/array_name,u=uv[0],v=uv[1],x=p.X.x,y=(p.js+.5)*h,
                        exact_u=p.G.uv(p.js,p.X.x,last)[0],exact_v=p.G.uv(p.js,p.X.x,last)[1],t=last)
    row=dict(config=cfg,complete=complete,stopped=stopped,final_t=t,history=hist,
             initial_peak=amp,valid_through=valid,first_failed_observation=first_failure,
             threshold_relative=THRESHOLD,evolution_seconds=evolution_seconds,rhs_calls=p.calls,
             steps=p.calls//4,precision='float64',decomposition=decomp,
             x=p.X.x.tolist(),snapshots=snapshots,field_array=array_name)
    print('RUN',cfg,'complete',complete,'valid',valid,'end errors',
          [hist[-1][z]['relative_inf'] for z in ('u','v')],flush=True)
    return row


def propagation():
    rows=[]
    # Common T for refinement; fixed y cell region. Time halving isolates its effect.
    for case in ('A','B'):
        for nx in (128,256,512):
            rows.append(run(case=case,nx=nx))
        rows.append(run(case=case,nx=256,dt=.000125))
        for h in (.125,.0625):
            rows.append(run(case=case,h=h,nx=256))
        for nx in (128,256):
            rows.append(run(case=case,nx=nx,T=.4))
        # Enlarge x at unchanged dx, and y at unchanged h. Interior compare later.
        rows.append(run(case=case,nx=384,L=30.))
        rows.append(run(case=case,nx=256,yhalf=2.5))
        write('dynamics_propagation',rows)
    return rows


def compare():
    rows=[]
    for case in ('A','B'):
        for h in (.25,.125,.0625):
            for nx in (128,256):
                for model in ('structure','fd'):
                    rows.append(run(case=case,h=h,nx=nx,model=model,continuous_data=True))
        # Paired time check, identical continuous initial/boundary data.
        for model in ('structure','fd'):
            rows.append(run(case=case,model=model,continuous_data=True,dt=.000125))
        write('dynamics_comparison',rows)
    return rows


def sensitivity():
    rows=[]
    for case in ('A','B'):
        for mode in (2,16):
            for eps in (1e-5,5e-6):
                for dt in (.00025,.000125):
                    responses=[]; failures=[]
                    times=[.005,.01,.02,.03,.05,.075,.1]
                    for sign in (-1,1):
                        p=Problem(case=case,nx=256)
                        P,Q=p.initial()
                        # Perturb u with zero values at both chain ends; derive P.
                        du=np.sin(np.linspace(0,np.pi,p.C.nj))[:,None]**2*np.cos(2*np.pi*mode*p.X.x/20)[None,:]
                        dP=np.diff(du,axis=0)/p.C.h
                        dQ=np.zeros_like(Q)
                        scale=np.sqrt(np.sum(dP*dP)); dP/=scale
                        states=[]
                        t=0.
                        for target in times:
                            if t==0:P=P+sign*eps*dP
                            def stop(t,P,Q):
                                if not np.isfinite(P).all() or not np.isfinite(Q).all():return 'nonfinite'
                                if max(np.max(abs(P)),np.max(abs(Q)))>1e3:return 'state magnitude exceeds 1000'
                            with np.errstate(over='ignore',invalid='ignore'):
                                P,Q,info=integrate(p.rhs,t,target,P,Q,dt,stop_fn=stop)
                            if info['stopped']:
                                failures.append(dict(sign=sign,**info));break
                            states.append(np.concatenate((P.ravel(),Q.ravel())))
                            t=target
                        responses.append(np.array(states))
                    count=min(len(z) for z in responses)
                    assert count>0, 'No finite paired response'
                    response=(responses[1][:count]-responses[0][:count])/(2*eps)
                    # Save response arrays for amplitude/step invariance checking.
                    name=f'response_{case}_{mode}_{eps}_{dt}.npz'
                    np.savez_compressed(OUT/name,response=response)
                    row=dict(case=case,mode=mode,k=2*np.pi*mode/20,eps=eps,dt=dt,
                             times=times[:count],gain=np.linalg.norm(response,axis=1).tolist(),array=name,
                             complete=count==len(times),failures=failures)
                    rows.append(row);print('RESPONSE',row,flush=True)
        write('dynamics_sensitivity',rows)
    return rows


if __name__=='__main__':
    cmd=sys.argv[1] if len(sys.argv)>1 else 'all'
    if cmd in ('verify','all'):verify()
    if cmd in ('propagation','all'):propagation()
    if cmd in ('compare','all'):compare()
    if cmd in ('sensitivity','all'):sensitivity()
