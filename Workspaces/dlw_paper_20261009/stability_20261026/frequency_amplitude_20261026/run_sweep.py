"""Independent nonlinear physical-field perturbations: frequency/amplitude sweep.

The evolved differences are divided by epsilon. Quadratic terms retain the
epsilon factors, so these are full nonlinear differences, not linearization.
"""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, sys, time
import numpy as np
from scipy.signal import resample

HERE=Path(__file__).resolve().parent
STABILITY=HERE.parent
PROJECT=STABILITY.parent
PILOT=STABILITY/'perturbation_pilot'
sys.path.insert(0,str(PILOT))
from run_pilot import delta_rhs
spec=importlib.util.spec_from_file_location('current_time_setup',PROJECT/'time_samm_20261025/time/run_time.py')
current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current)
from probe import transform
from rerun_20261024 import rhs

KAPPAS=[np.pi/2,np.pi,2*np.pi]
EPSILONS=[1e-7,1e-6,1e-5]
T=.01
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def parameters(control=False):
    return [dict(kappa=float(k),epsilon=e,component=c,k_index=i,epsilon_index=j)
            for i,k in enumerate(KAPPAS) for j,e in enumerate(EPSILONS) for c in ['u','v']
            if not control or (i==2 and j==2)]

def masks(m,yv):
    if m.case in ['A','D']:
        R=5 if m.case=='A' else 30
        return abs(m.x)<=R,abs(m.y)<R,abs(yv)<R
    return np.ones(m.nx,dtype=bool),abs(m.y)<=1.8+1e-12,abs(yv)<=1.8+1e-12

def physical(m,D):
    r,s=D[:,0],D[:,1]
    return r,np.diff(r,axis=1)/m.h+(s[:,1:]+s[:,:-1])/2

def normalized_rhs(m,base,D,eps):
    u,w=base;r,s=D[:,0],D[:,1];h=m.h;e=eps[:,None,None]
    dH=(u+2*m.a)*r+e*r*r/2+h*h*((w/16-.25)*s+e*s*s/32)
    q=np.diff(r,axis=1)/h+(s[:,1:]+s[:,:-1])/2
    dr=-np.diff(m.d1(dH),axis=1)/h-m.d2(q)
    rt=np.concatenate((np.zeros_like(r[:,:1]),h*np.cumsum(dr,axis=1)),axis=1)
    st=m.d2(s)-m.d1((u+2*m.a)*s+(w-4)*r+e*r*s)
    return np.stack((rt,st),axis=1)

def advance(m,t,z,D,eps,dt):
    a=rhs(m,t,z);A=normalized_rhs(m,z,D,eps)
    z2=z+dt*a/2;D2=D+dt*A/2
    b=rhs(m,t+dt/2,z2);B=normalized_rhs(m,z2,D2,eps)
    z3=z+dt*b/2;D3=D+dt*B/2
    c=rhs(m,t+dt/2,z3);C=normalized_rhs(m,z3,D3,eps)
    z4=z+dt*c;D4=D+dt*C
    d=rhs(m,t+dt,z4);DD=normalized_rhs(m,z4,D4,eps)
    return z+dt*(a+2*b+2*c+d)/6,D+dt*(A+2*B+2*C+DD)/6

def run(case,control=False):
    tag=case+('_half_step' if control else '')
    dest=HERE/(tag+'.json')
    if dest.exists():print('PRESERVED',tag,flush=True);return
    tic=time.perf_counter();pars=parameters(control);eps=np.array([p['epsilon'] for p in pars]);dt=5e-5 if control else 1e-4
    m,z,yv=current.setup(case,allow_quarter_steps=control)
    ix,mu,mv=masks(m,yv);z0=z.copy()
    yl,yr=m.y[[0,-1]]
    env=np.sin(np.pi*(m.y-yl)/(yr-yl))**2;env[0]=env[-1]=0
    envv=np.sin(np.pi*(yv-yl)/(yr-yl))**2
    D=np.zeros((len(pars),2,len(m.y),m.nx));map_errors=[]
    for n,p in enumerate(pars):
        carrier=np.cos(p['kappa']*m.x)[None,:]
        r=env[:,None]*carrier if p['component']=='u' else np.zeros_like(z[0])
        q=envv[:,None]*carrier if p['component']=='v' else np.zeros((len(yv),m.nx))
        s=np.zeros_like(r)
        for j in range(1,len(s)):s[j]=2*(q[j-1]-(r[j]-r[j-1])/m.h)-s[j-1]
        D[n]=[r,s]
        map_errors.append(float(abs(transform(m,r,s)-q).max()))
    D0=D.copy()
    # Independent check against the existing algebraic subtraction code.
    normrhs=normalized_rhs(m,z,D,eps)
    residual=[]
    for i,p in enumerate(pars):
        check=delta_rhs(m,z,p['epsilon']*D[i])/p['epsilon']
        residual.append(float(np.max(abs(check-normrhs[i]))))
    assert max(map_errors)<2e-13 and max(residual)<1e-8,(map_errors,residual)
    times=[];maxima=[];l2=[];amplitude_difference=[];baseline_max=[]
    reached=0.;status='complete';reason=None
    def save(t):
        times.append(float(t));u,v=physical(m,D)
        pairs=[u[:,mu],v[:,mv]]
        maxima.append(np.array([np.max(abs(a[:,:,ix]),axis=(1,2)) for a in pairs]).T)
        l2.append(np.array([np.sqrt(m.h*m.dx*np.sum(a*a,axis=(1,2))) for a in pairs]).T)
        if not control:
            diff=np.zeros((3,3,2,2))
            for ki in range(3):
                for ej in range(3):
                    for ci in range(2):
                        j=ki*6+ej*2+ci;ref=ki*6+2+ci
                        diff[ki,ej,ci]=[float(abs((a[j]-a[ref])[:,ix]).max()) for a in pairs]
            amplitude_difference.append(diff)
        baseline_max.append(float(abs(z).max()))
    save(0)
    print(tag,'initialized',D.shape,'seconds',round(time.perf_counter()-tic,2),flush=True)
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for step in range(round(T/dt)):
            try:
                nz,nD=advance(m,step*dt,z,D,eps,dt)
                if not np.isfinite(nz).all() or not np.isfinite(nD).all():raise FloatingPointError('nonfinite')
                if abs(nz).max()>1e6 or np.max(abs(nD)*eps[:,None,None,None])>1e6:raise FloatingPointError('state threshold 1e6')
            except FloatingPointError as e:
                status='stopped';reason=str(e);break
            z,D=nz,nD;reached=(step+1)*dt;save(reached)
            if (step+1)%20==0:print(tag,'step',step+1,'of',round(T/dt),'seconds',round(time.perf_counter()-tic,1),flush=True)
    arrmax=np.asarray(maxima);arrl2=np.asarray(l2);ad=np.asarray(amplitude_difference)
    peak8=[]
    for n,p in enumerate(pars):
        uf,vf=physical(m,D[n:n+1]);ui,vi=physical(m,D0[n:n+1])
        fin=[float(abs(resample(a[0,mask],m.nx*8,axis=-1)).max()) for a,mask in [(uf,mu),(vf,mv)]]
        ini=max(float(abs(a[0,mask]).max()) for a,mask in [(ui,mu),(vi,mv)])
        peak8.append(dict(final_normalized=fin,initial_max_normalized=ini,gain_relative_initial=[a/ini for a in fin]))
    # Stored stages use the production baseline RHS with identical arithmetic.
    prior=np.load(PROJECT/'report_refresh_20261024/natural_edge_rk4_20261024'/(case+'.npz'))
    baseline_repro=float(abs(z-prior['z']).max()) if not control and status=='complete' else None
    if baseline_repro is not None:assert baseline_repro<2e-13,(case,baseline_repro)
    old= None
    if not control and status=='complete':
        old_data=np.load(PILOT/'four_case_kappa_pi_over_2'/(case+'.npz'))
        old=[]
        for ci in range(2):
            j=2+ci;pu,pv=physical(m,D[j:j+1]);ou,ow=old_data['final_state'][ci+1]
            ov=transform(m,ou,ow)
            old.append([float(abs((pu[0]*1e-6-ou)[mu][:,ix]).max()),float(abs((pv[0]*1e-6-ov)[mv][:,ix]).max())])
        assert max(max(r) for r in old)<1e-11,(case,old)
    artifact=HERE/(tag+'.npz')
    np.savez_compressed(artifact,x=m.x,y=m.y,yv=yv,baseline_initial=z0,baseline_final=z,normalized_initial=D0,normalized_final=D,t=np.array(times),max_normalized=arrmax,l2_normalized=arrl2,amplitude_difference=ad,baseline_global_max=baseline_max)
    records=[]
    for j,p in enumerate(pars):
        denom=np.linalg.norm(arrl2[0,j]);gain=np.linalg.norm(arrl2[:,j],axis=1)/denom
        rec=dict(**p,status=status,reached=reached,initial_max_normalized=arrmax[0,j].tolist(),final_max_normalized=arrmax[-1,j].tolist(),l2_pair_gain=float(gain[-1]),fourier8=peak8[j])
        if not control:
            ki,ej=p['k_index'],p['epsilon_index'];ci=0 if p['component']=='u' else 1;ref=ki*6+2+ci
            dmax=ad[:,ki,ej,ci].max(axis=0);dend=ad[-1,ki,ej,ci]
            refmax=float(arrmax[:,ref].max());refend=float(arrmax[-1,ref].max())
            rec.update(normalized_field_difference_from_eps1e6_all_time=dmax.tolist(),normalized_field_difference_from_eps1e6_terminal=dend.tolist(),relative_pair_max_difference_all_time=float(dmax.max()/refmax),relative_pair_max_difference_terminal=float(dend.max()/refend))
        records.append(rec)
    record=dict(case=case,status=status,reason=reason,reached=reached,T=T,dt=dt,h=m.h,dx=m.dx,nx=m.nx,ny=len(m.y),parameters=pars,records=records,initial_physical_map_max=max(map_errors),normalized_rhs_versus_existing_delta_rhs_max=max(residual),baseline_reproduction_max=baseline_repro,legacy_pi_over_2_eps1e6_physical_differences=old,normalization='physical differences divided by prescribed epsilon; L2 pair gain divided by measured initial pair norm',amplitude_comparison='Full normalized physical fields versus epsilon=1e-6, at every recorded time; maxima use paper observation windows; relative denominator is the largest reference pair maximum over the corresponding time interval.',l2_region='full periodic x interval and native interior y observation region',difference_evolution='exact normalized nonlinear difference: epsilon multiplies quadratic difference terms',filtering=False,continuous_certificate=False,eta_u=None,eta_v=None,artifact_sha256=sha(artifact),source_sha256={p.name:sha(p) for p in [Path(__file__),PILOT/'run_pilot.py',PROJECT/'time_samm_20261025/time/run_time.py']},seconds=time.perf_counter()-tic)
    dest.write_text(json.dumps(record,indent=2),encoding='utf-8')
    with (HERE/(tag+'_history.csv')).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['case','kappa','epsilon','component','time','max_u_over_epsilon','max_v_over_epsilon','l2_pair_gain'])
        for ti,t in enumerate(times):
            for j,p in enumerate(pars):w.writerow([case,p['kappa'],p['epsilon'],p['component'],t,*arrmax[ti,j],np.linalg.norm(arrl2[ti,j])/np.linalg.norm(arrl2[0,j])])
    print(tag,'COMPLETE',round(record['seconds'],1),'baseline reproduction',baseline_repro,'legacy',old,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('case',choices=['A','D','Gaussian','Sinusoidal']);ap.add_argument('--control',action='store_true');a=ap.parse_args();run(a.case,a.control)
