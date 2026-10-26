"""Natural Centered-SD: Euler, RK4, and Crank--Nicolson error histories.

Current physical reconstruction v=diff(u)/h+avg(w), with m.gauge='local'.
The same rhs and boundary data are used by all three integrators. Every
integer time-step is compared to the time-dependent continuous solution.
"""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, sys, time
import numpy as np

HERE=Path(__file__).resolve().parent
HERE.mkdir(parents=True,exist_ok=True)
PROJECT=HERE.parents[1]
ROOT=PROJECT.parents[1]
PROBE=PROJECT/'spatial_audit_20261023/separated/reconstruction_probe'
PRIOR=PROJECT/'report_refresh_20261024/natural_edge_rk4_20261024'
REF=PROJECT/'report_refresh_20261024/nondegenerate_rk4_20261024'
sys.path.insert(0,str(PROBE))
from probe import Model, invert, transform, HALF_WIDTHS
from rerun_20261024 import rhs, norms
spec=importlib.util.spec_from_file_location('nondegenerate_time_source',REF/'run.py')
reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
METHODS=['Euler','RK4','CN'];T=.01;DT=1e-4;CN_TOL=2e-14

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def setup(case,allow_quarter_steps=False):
    if case in ('A','D'):
        m=Model(case,'Centered-SD',.1,.1);m.gauge='local'
        u=m.initial()[0];yv=(m.y[1:]+m.y[:-1])/2;v=m.profile(yv,0)[1]
        _,g=m.G.tau(m.y[:1]/m.h-.5,m.x,0,False)
        lower=4*m.G.cov(g,0,2)[0]
    else:
        m=reference.NondegenerateModel(case,'Centered-SD');m.gauge='local'
        u=m.profile(m.y,0)[0];yv=(m.y[1:]+m.y[:-1])/2;v=m.profile(yv,0)[1]
        dat=reference.initial_data(case,m.x,m.y[:1]);lower=(dat['v']-dat['uy'])[0]
        if allow_quarter_steps:
            cache={}
            def boundary(t):
                if t not in cache:
                    yy=np.r_[m.y[0]-m.h,m.y[0],m.y[-3:],m.y[-1]+m.h]
                    cache[t]=(m.profile(yy,t)[0],m.ut(yy,t))
                    if len(cache)>16:cache.pop(next(iter(cache)))
                return cache[t]
            m.boundary=boundary
    w,_,_=invert(m,u,v,lower)
    return m,np.array([u,w]),yv

def reference_fields(m,yv,t):
    return m.profile(m.y,t)[0],m.profile(yv,t)[1]

def measure(m,du,dv,yv):
    if m.case in ('A','D'):return norms(m,du,dv)
    return [reference.measured(m,du,m.y)[0],reference.measured(m,dv,yv)[0]]

def step(m,z,t,dt,method,tolerance=CN_TOL):
    if method=='Euler':return z+dt*rhs(m,t,z),0.,0
    if method=='RK4':
        k1=rhs(m,t,z);k2=rhs(m,t+dt/2,z+dt*k1/2)
        k3=rhs(m,t+dt/2,z+dt*k2/2);k4=rhs(m,t+dt,z+dt*k3)
        return z+dt*(k1+2*k2+2*k3+k4)/6,0.,0
    f=rhs(m,t,z);candidate=z+dt*f
    for iteration in range(1,101):
        residual=candidate-z-dt*(f+rhs(m,t+dt,candidate))/2
        rn=float(np.max(abs(residual)))
        if rn<tolerance:return candidate,rn,iteration
        candidate-=residual
    raise RuntimeError(f'CN solve did not converge: residual={rn}, t={t}')

def run(case):
    dest=HERE/(case+'_time.json')
    if dest.exists():print('Preserved completed result',case,flush=True);return
    started=time.perf_counter();m,z0,yv=setup(case)
    states={method:z0.copy() for method in METHODS}
    history={method:[] for method in METHODS};residuals={method:[] for method in METHODS};iterations={method:[] for method in METHODS}
    ur,vr=reference_fields(m,yv,0.)
    for method in METHODS:history[method].append(measure(m,z0[0]-ur,transform(m,*z0)-vr,yv))
    times=np.arange(101,dtype=float)*DT
    elapsed_evolve={method:0. for method in METHODS}
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for i in range(100):
            for method in METHODS:
                before=time.perf_counter()
                states[method],rn,it=step(m,states[method],i*DT,DT,method)
                elapsed_evolve[method]+=time.perf_counter()-before
                residuals[method].append(rn);iterations[method].append(it)
                assert np.isfinite(states[method]).all() and np.max(abs(states[method]))<1e6
            ur,vr=reference_fields(m,yv,times[i+1])
            for method in METHODS:
                z=states[method];history[method].append(measure(m,z[0]-ur,transform(m,*z)-vr,yv))
            if (i+1)%20==0:print(case,'main step',i+1,'elapsed',round(time.perf_counter()-started,1),flush=True)
    payload=dict(x=m.x,y=m.y,yv=yv,z0=z0,t=times,u_ref=ur,v_ref=vr)
    for method in METHODS:
        payload['z_'+method]=states[method];payload['u_'+method]=states[method][0]
        payload['v_'+method]=transform(m,*states[method]);payload['errors_'+method]=np.asarray(history[method])
        payload['cn_residual_'+method]=np.asarray(residuals[method]);payload['cn_iterations_'+method]=np.asarray(iterations[method])
    npz=dest.with_suffix('.npz');np.savez_compressed(npz,**payload)
    prior=np.load(PRIOR/(case+'.npz'))
    prior_record=json.loads((PRIOR/(case+'.json')).read_text())
    assert sha(PRIOR/(case+'.npz'))==prior_record['artifact_sha256']
    reproduction=max(float(np.max(abs(states['RK4']-prior['z']))),float(np.max(abs(payload['v_RK4']-prior['v']))))
    error_reproduction=max(abs(a-b) for a,b in zip(history['RK4'][-1],prior_record['error']))
    assert reproduction<2e-13 and error_reproduction<2e-13,(reproduction,error_reproduction)
    rows=[dict(case=case,integrator=method,time=float(t),error_u=history[method][j][0],error_v=history[method][j][1]) for method in METHODS for j,t in enumerate(times)]
    with (HERE/(case+'_history.csv')).open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    record=dict(case=case,spatial='Current natural Centered-SD',h=.1,dx=.1,dt=DT,T=T,status='complete',a=2.,samples=101,
        integrators={method:dict(error=history[method][-1],cn_max_residual=max(residuals[method]),cn_max_iterations=max(iterations[method]),evolution_seconds=elapsed_evolve[method]) for method in METHODS},
        state='u,w with v=diff(u)/h+adjacent_average(w); omega=h*w/4',
        boundary='Exact continuous lower u_t; all w nodes including lower trace evolved by the same natural auxiliary equation',
        metric='Maximum absolute error at native physical-field sites, same region as the spatial comparison',
        region=('abs(x)<=R, abs(y)<R, R='+str(HALF_WIDTHS[case]) if case in ('A','D') else 'all periodic x nodes [-96,96); native sites abs(y)<=1.8'),
        reference='Continuous analytic soliton' if case in ('A','D') else 'Continuous heat/Laplace reference evaluated separately at every recorded time',
        reference_certificate_scope='For Gaussian/Sinusoidal the previous 1e-13 certificate covers stored t=0 and T=.01 samples; intermediate-time values use the same analytic evaluator and are not relabelled as newly certified.',
        cn_solver='Fixed-point solution of trapezoidal residual in the complete u,w state',cn_absolute_tolerance=CN_TOL,
        initial_error=history['RK4'][0],rk4_saved_state_max_difference=reproduction,rk4_published_error_difference=error_reproduction,
        source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),PROBE/'probe.py',PROBE/'rerun_20261024.py',REF/'run.py',REF/'reference_grid.py']},
        artifact=str(npz.relative_to(ROOT)),artifact_sha256=sha(npz),seconds=time.perf_counter()-started)
    dest.write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record),flush=True)

def controls(case):
    dest=HERE/(case+'_controls.json')
    if dest.exists():print('Preserved controls',case,flush=True);return
    saved=np.load(HERE/(case+'_time.npz'));started=time.perf_counter();records=[]
    for method,dt,tol,label in [('Euler',DT/2,CN_TOL,'half_step'),('RK4',DT/2,CN_TOL,'half_step'),('CN',DT,2e-15,'tight_solve')]:
        m,z,yv=setup(case,allow_quarter_steps=dt<DT);mr=0.;mi=0
        for i in range(round(T/dt)):
            z,rn,it=step(m,z,i*dt,dt,method,tol);mr=max(mr,rn);mi=max(mi,it)
            assert np.isfinite(z).all() and np.max(abs(z))<1e6
        v=transform(m,*z)
        delta=measure(m,z[0]-saved['u_'+method],v-saved['v_'+method],yv)
        errs=measure(m,z[0]-saved['u_ref'],v-saved['v_ref'],yv)
        record=dict(integrator=method,control=label,dt=dt,tolerance=tol,physical_field_difference_from_main=delta,error=errs,cn_max_residual=mr,cn_max_iterations=mi)
        records.append(record)
        np.savez_compressed(HERE/(case+'_'+method+'_'+label+'.npz'),z=z,u=z[0],v=v,x=m.x,y=m.y,yv=yv)
        print(case,label,method,delta,flush=True)
    out=dict(case=case,status='complete',controls=records,seconds=time.perf_counter()-started)
    dest.write_text(json.dumps(out,indent=2),encoding='utf-8')

def collect():
    main=[json.loads((HERE/(c+'_time.json')).read_text()) for c in ['A','D','Gaussian','Sinusoidal']]
    control=[json.loads((HERE/(c+'_controls.json')).read_text()) for c in ['A','D','Gaussian','Sinusoidal']]
    rows=[]
    for rec in main:
        for method in METHODS:
            rows.append(dict(case=rec['case'],spatial='Centered-SD',integrator=method,h=.1,dx=.1,dt=DT,T=T,error_u=rec['integrators'][method]['error'][0],error_v=rec['integrators'][method]['error'][1]))
    with (HERE/'terminal_errors.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (HERE/'results.json').write_text(json.dumps(dict(main=main,controls=control),indent=2),encoding='utf-8')
    print(json.dumps(rows,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('case');ap.add_argument('--controls',action='store_true');args=ap.parse_args()
    if args.case=='collect':collect()
    elif args.controls:controls(args.case)
    else:run(args.case)
