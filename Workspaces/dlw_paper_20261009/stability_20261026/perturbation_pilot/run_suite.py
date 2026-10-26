"""Four benchmark backgrounds, independent u/v perturbations at kappa=pi/2.

Exploratory nonlinear sensitivity of the current finite grid, not certified
perturbed continuous solutions. One baseline is shared by both perturbations.
"""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, sys, time
import numpy as np

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
sys.path.insert(0,str(HERE))
from run_pilot import delta_rhs
spec=importlib.util.spec_from_file_location('current_time_setup',PROJECT/'time_samm_20261025/time/run_time.py')
current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current)
from probe import transform
from rerun_20261024 import rhs

OUT=HERE/'four_case_kappa_pi_over_2';OUT.mkdir(exist_ok=True)
KAPPA=np.pi/2;EPS=1e-6;DT=1e-4;T=.01

def initial_difference(m,yv,component):
    yl,yr=m.y[[0,-1]]
    phi=lambda yy:np.sin(np.pi*(yy-yl)/(yr-yl))**2
    carrier=np.cos(KAPPA*m.x)[None,:]
    du=EPS*phi(m.y)[:,None]*carrier if component=='u' else np.zeros((len(m.y),m.nx))
    du[0]=0.;du[-1]=0.
    dv=EPS*phi(yv)[:,None]*carrier if component=='v' else np.zeros((len(yv),m.nx))
    dw=np.empty_like(du);dw[0]=0.
    for j in range(1,len(du)):dw[j]=2*(dv[j-1]-(du[j]-du[j-1])/m.h)-dw[j-1]
    d=np.array([du,dw]);map_error=float(abs(transform(m,*d)-dv).max())
    assert map_error<1e-18
    return d,map_error

def vector_field(m,t,state):
    return np.array([rhs(m,t,state[0]),delta_rhs(m,state[0],state[1]),delta_rhs(m,state[0],state[2])])

def advance(m,t,z):
    a=vector_field(m,t,z);b=vector_field(m,t+DT/2,z+DT*a/2)
    c=vector_field(m,t+DT/2,z+DT*b/2);d=vector_field(m,t+DT,z+DT*c)
    return z+DT*(a+2*b+2*c+d)/6

def run(case):
    dest=OUT/(case+'.json')
    if dest.exists():print('Preserved',case,flush=True);return
    tic=time.perf_counter();m,base,yv=current.setup(case)
    du,mu=initial_difference(m,yv,'u');dv,mv=initial_difference(m,yv,'v')
    z=np.array([base,du,dv]);z0=z.copy()
    history=[];times=[];base_errors=[];base_times=[]
    reached=0.;status='complete';reason=None
    def save(t):
        times.append(t)
        history.append([current.measure(m,d[0],transform(m,*d),yv) for d in z[1:]])
        if abs(t/.001-round(t/.001))<1e-9:
            ur,vr=current.reference_fields(m,yv,t)
            base_errors.append(current.measure(m,z[0,0]-ur,transform(m,*z[0])-vr,yv));base_times.append(t)
    save(0.)
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for n in range(100):
            try:
                nxt=advance(m,n*DT,z)
                if not np.isfinite(nxt).all() or abs(nxt).max()>1e6:raise FloatingPointError('state threshold')
            except FloatingPointError as e:status='stopped';reason=str(e);break
            z=nxt;reached=(n+1)*DT;save(reached)
            if (n+1)%20==0:print(case,'step',n+1,'elapsed',round(time.perf_counter()-tic,1),flush=True)
    hist=np.asarray(history)
    payload=dict(x=m.x,y=m.y,yv=yv,z0=z0,final_state=z,t=times,delta_max=hist,base_t=base_times,base_exact_errors=base_errors)
    for i,c in enumerate(['u','v'],start=1):
        payload['delta_u_from_'+c]=z[i,0]
        payload['delta_v_from_'+c]=transform(m,*z[i])
    artifact=dest.with_suffix('.npz');np.savez_compressed(artifact,**payload)
    prior=np.load(PROJECT/'report_refresh_20261024/natural_edge_rk4_20261024'/(case+'.npz'))
    repro=float(abs(z[0]-prior['z']).max()) if status=='complete' else None
    if status=='complete':assert repro<2e-13,('baseline reproduction',case,repro)
    rec=dict(case=case,status=status,reason=reason,T=T,reached=reached,epsilon=EPS,kappa=KAPPA,x_mode=int(round(KAPPA*2*m.half/(2*np.pi))),h=m.h,dx=m.dx,dt=DT,x_interval=[-m.half,m.half],y_interval=[float(m.y[0]),float(m.y[-1])],nx=m.nx,ny=len(m.y),perturbation='Independent u-only / v-only epsilon*sin(pi*(y-yL)/(yR-yL))^2*cos(pi*x/2), sampled at each physical field native sites',lower_boundary='Identical analytic lower u_t for baseline and perturbed trajectories; lower w perturbation starts at zero and evolves',initial_delta_max=hist[0].tolist(),final_delta_max=hist[-1].tolist(),gain_relative_to_initial_max=[(hist[-1,i]/max(hist[0,i])).tolist() for i in range(2)],initial_physical_v_map_errors=[mu,mv],initial_w_max=[float(abs(z0[i,1]).max()) for i in [1,2]],initial_checkerboard_w_projection_max=[float(abs(np.sum((-1.)**np.arange(len(m.y))[:,None]*z0[i,1],axis=0)/len(m.y)).max()) for i in [1,2]],baseline_exact_error=base_errors[-1],baseline_reproduces_published_rk4_maxdiff=repro,certificate=False,reference_bound_u=None,reference_bound_v=None,reference_scope='Numerical discrete baseline and nonlinear perturbation trajectories; no continuous perturbed-solution certificate.',source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'run_pilot.py',PROJECT/'time_samm_20261025/time/run_time.py']},artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),seconds=time.perf_counter()-tic)
    dest.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    rows=[]
    for n,t in enumerate(times):
        for i,c in enumerate(['u','v']):rows.append([case,c,t,*hist[n,i]])
    with (OUT/(case+'_history.csv')).open('w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(['case','perturbed_field','time','max_delta_u','max_delta_v']);wr.writerows(rows)
    print(json.dumps(rec),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('case',choices=['A','D','Gaussian','Sinusoidal']);run(ap.parse_args().case)
