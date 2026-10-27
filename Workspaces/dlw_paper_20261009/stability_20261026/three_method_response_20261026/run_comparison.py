"""Same physical perturbation under Endpoint-SD, natural Centered-SD and FD.

The exact nonlinear difference equations are evolved in normalized variables
delta/epsilon alongside each numerical background, using common RK4 stages.
"""
from pathlib import Path
import argparse, csv, hashlib, importlib.util, json, sys, time
import numpy as np
from scipy.interpolate import CubicSpline

HERE=Path(__file__).resolve().parent
STABILITY=HERE.parent
PROJECT=STABILITY.parent
PILOT=STABILITY/'perturbation_pilot'
sys.path.insert(0,str(PILOT))
from run_pilot import delta_rhs as previous_centered_delta_rhs
spec=importlib.util.spec_from_file_location('current_time_setup',PROJECT/'time_samm_20261025/time/run_time.py')
current=importlib.util.module_from_spec(spec);spec.loader.exec_module(current)
from probe import Model,invert,transform
from rerun_20261024 import rhs as centered_rhs

METHODS=['Endpoint-SD','Centered-SD','FD']
COMPONENTS=['u','v']
PAIRS=[(0,1),(0,2),(1,2)]
EPS=1e-6;KAPPA=np.pi/2;H=DX=.1;T=.01

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def setup(case,method,half_step=False):
    if method=='Centered-SD':
        m,z,yv=current.setup(case,allow_quarter_steps=half_step)
        return m,z,yv,lambda t,z:centered_rhs(m,t,z)
    if case in ['A','D']:
        m=Model(case,method,DX,H)
    else:
        m=current.reference.NondegenerateModel(case,method)
        if half_step:
            cache={}
            def boundary(t):
                if t not in cache:
                    yy=np.r_[m.y[0]-m.h,m.y[0],m.y[-3:],m.y[-1]+m.h]
                    cache[t]=(m.profile(yy,t)[0],m.ut(yy,t))
                    if len(cache)>16:cache.pop(next(iter(cache)))
                return cache[t]
            m.boundary=boundary
    z=m.initial()
    return m,z,m.yv,m.rhs

def initial_difference(m,yv,method):
    yl,yr=m.y[[0,-1]]
    phi=lambda y:np.sin(np.pi*(y-yl)/(yr-yl))**2
    carrier=np.cos(KAPPA*m.x)[None,:]
    r=phi(m.y)[:,None]*carrier;r[0]=r[-1]=0.
    q=phi(yv)[:,None]*carrier
    differences=[];map_errors=[]
    for component in COMPONENTS:
        u=r.copy() if component=='u' else np.zeros_like(r)
        v=q.copy() if component=='v' else np.zeros_like(q)
        if method=='Centered-SD':
            w=np.zeros_like(u)
            for j in range(1,len(w)):w[j]=2*(v[j-1]-(u[j]-u[j-1])/m.h)-w[j-1]
            d=np.array([u,w]);map_errors.append(float(abs(transform(m,*d)-v).max()))
        else:d=np.array([u,v]);map_errors.append(0.)
        differences.append(d)
    return np.array(differences),map_errors

def centered_difference(m,r):
    """Linear difference of the production centered ghost closure."""
    right=3*r[:,-1]-3*r[:,-2]+r[:,-3]
    ext=np.concatenate((np.zeros_like(r[:,:1]),r,right[:,None]),axis=1)
    return (ext[:,2:]-ext[:,:-2])/(2*m.h)

def normalized_delta_rhs(m,method,z,D):
    u,v=z;r,s=D[:,0],D[:,1];h=m.h;a=m.a
    if method=='Centered-SD':
        w=v
        dH=(u+2*a)*r+EPS*r*r/2+h*h*((w/16-.25)*s+EPS*s*s/32)
        q=np.diff(r,axis=1)/h+(s[:,1:]+s[:,:-1])/2
        source=-np.diff(m.d1(dH),axis=1)/h-m.d2(q)
        rt=np.concatenate((np.zeros_like(r[:,:1]),h*np.cumsum(source,axis=1)),axis=1)
        st=m.d2(s)-m.d1((u+2*a)*s+(w-4)*r+EPS*r*s)
    else:
        dH=(u+2*a)*r+EPS*r*r/2
        source=-np.diff(m.d1(dH),axis=1)/h-m.d2(s[:,1:] if method=='Endpoint-SD' else (s[:,1:]+s[:,:-1])/2)
        rt=np.concatenate((np.zeros_like(r[:,:1]),h*np.cumsum(source,axis=1)),axis=1)
        if method=='FD':
            st=-m.d1((u+2*a)*s+(v-4)*r+EPS*r*s)-m.d2(centered_difference(m,r))
        else:
            # Exact lower ghost is common, hence its perturbation is zero.
            b,_=m.boundary(_CURRENT_STAGE_TIME)
            prev=np.concatenate((b[:1],u[:-1]))
            avg=(u+prev)/2;p=(u-prev)/h
            rp=np.concatenate((np.zeros_like(r[:,:1]),r[:,:-1]),axis=1)
            ar=(r+rp)/2;pr=(r-rp)/h
            flux=(avg+2*a-2*h)*s+(v-4)*ar+EPS*ar*s+h*(2*v*s+EPS*s*s)/4-h*(2*p*pr+EPS*pr*pr)/4
            st=-m.d1(flux)-m.d2(pr)
    return np.stack((rt,st),axis=1)

def vf(m,method,fun,t,z,D):
    global _CURRENT_STAGE_TIME
    _CURRENT_STAGE_TIME=t
    return fun(t,z),normalized_delta_rhs(m,method,z,D)

def advance(m,method,fun,t,z,D,dt):
    a,A=vf(m,method,fun,t,z,D)
    b,B=vf(m,method,fun,t+dt/2,z+dt*a/2,D+dt*A/2)
    c,C=vf(m,method,fun,t+dt/2,z+dt*b/2,D+dt*B/2)
    d,DD=vf(m,method,fun,t+dt,z+dt*c,D+dt*C)
    return z+dt*(a+2*b+2*c+d)/6,D+dt*(A+2*B+2*C+DD)/6

def fields(m,method,D):
    u=D[:,0]
    v=np.diff(u,axis=1)/m.h+(D[:,1,1:]+D[:,1,:-1])/2 if method=='Centered-SD' else D[:,1]
    return u,v

def run(case,half_step=False):
    HERE.mkdir(exist_ok=True)
    tag=case+('_half_step' if half_step else '')
    dest=HERE/(tag+'.json')
    if dest.exists():print('PRESERVED',tag,flush=True);return
    tic=time.perf_counter();dt=5e-5 if half_step else 1e-4
    models=[];states=[];diffs=[];yv_all=[];funs=[];initial_checks=[]
    for method in METHODS:
        m,z,yv,fun=setup(case,method,half_step);D,me=initial_difference(m,yv,method)
        _,dr=vf(m,method,fun,0.,z,D)
        checks=[]
        for j in range(2):checks.append(float(abs(EPS*dr[j]-(fun(0,z+EPS*D[j])-fun(0,z))).max()))
        assert max(checks)<2e-8,(case,method,checks)
        if method=='Centered-SD':
            exactcheck=max(float(abs(dr[j]-previous_centered_delta_rhs(m,z,EPS*D[j])/EPS).max()) for j in range(2))
            assert exactcheck<1e-8
        else:exactcheck=None
        initial_checks.append(dict(method=method,physical_map_error_normalized=me,delta_rhs_physical_subtraction_residual=checks,previous_centered_delta_rhs_normalized_residual=exactcheck))
        models.append(m);states.append(z);diffs.append(D);yv_all.append(yv);funs.append(fun)
    x=models[0].x;y=models[0].y;ye=yv_all[1]
    assert all(np.max(abs(m.x-x))==0 and np.max(abs(m.y-y))==0 for m in models)
    assert np.max(abs(yv_all[0][1:]-ye))<1e-12
    if case in ['A','D']:
        R=5 if case=='A' else 30;ix=abs(x)<=R;mu=abs(y)<R;mv=abs(ye)<R
    else:ix=np.ones(len(x),bool);mu=abs(y)<=1.8+1e-12;mv=abs(ye)<=1.8+1e-12
    xobs=x[ix];yuobs=y[mu];yvobs=ye[mv]
    initial_states=[s.copy() for s in states];initial_diffs=[d.copy() for d in diffs]
    times=[];maxima=[];native_maxima=[];pair_diff=[];relative_pair_diff=[];baseline_global=[]
    l2=[];snaps_u=[];snaps_v=[];snap_t=[];checkpoints={}
    status='complete';reason=None;reached=0.
    def common_fields():
        us=[];vs=[];nmax=[]
        for i,method in enumerate(METHODS):
            u,v=fields(models[i],method,diffs[i])
            vm=(abs(yv_all[i])<R) if case in ['A','D'] else (abs(yv_all[i])<=1.8+1e-12)
            nmax.append(np.stack([np.max(abs(u[:,mu][:,:,ix]),axis=(1,2)),np.max(abs(v[:,vm][:,:,ix]),axis=(1,2))],axis=1))
            if method=='Endpoint-SD':vc=v[:,1:]
            elif method=='FD':vc=CubicSpline(y,v,axis=1)(ye)
            else:vc=v
            us.append(u[:,mu][:,:,ix]);vs.append(vc[:,mv][:,:,ix])
        return np.asarray(us),np.asarray(vs),np.asarray(nmax)
    def record(t):
        times.append(float(t));u,v,nmax=common_fields()
        mx=np.stack([np.max(abs(u),axis=(2,3)),np.max(abs(v),axis=(2,3))],axis=2)
        maxima.append(mx);native_maxima.append(nmax)
        dd=np.array([[np.max(abs(u[a]-u[b]),axis=(1,2)),np.max(abs(v[a]-v[b]),axis=(1,2))] for a,b in PAIRS]).transpose(0,2,1)
        denom=np.maximum(1.,np.max(mx,axis=(0,2)))
        pair_diff.append(dd);relative_pair_diff.append(np.max(dd,axis=2)/denom[None,:])
        l2.append(np.sqrt(H*DX*(np.sum(u*u,axis=(2,3))+np.sum(v*v,axis=(2,3)))))
        baseline_global.append([float(abs(z).max()) for z in states])
        if abs(t/.0025-round(t/.0025))<1e-8:
            snaps_u.append(u);snaps_v.append(v);snap_t.append(t)
        if abs(t-.01)<1e-12:
            for i,method in enumerate(METHODS):
                if method=='Centered-SD':old=PROJECT/'report_refresh_20261024/natural_edge_rk4_20261024'/(case+'.npz');key='z'
                elif case in ['A','D']:old=PROJECT/'report_refresh_20261024/rk4_spatial'/(case+'_'+method+'_RK4.npz');key='z'
                else:old=PROJECT/'report_refresh_20261024/nondegenerate_rk4_20261024'/(case+'_'+method+'_RK4.npz');key='z'
                olddata=np.load(old);repro=float(abs(states[i]-olddata[key]).max())
                if not half_step:assert repro<2e-12,(case,method,repro)
                uu,vv=fields(models[i],method,states[i][None])
                eu=uu[0]-models[i].profile(y,t)[0];ev=vv[0]-models[i].profile(yv_all[i],t)[1]
                vnmask=(abs(yv_all[i])<R) if case in ['A','D'] else (abs(yv_all[i])<=1.8+1e-12)
                er=[float(abs(eu[mu][:,ix]).max()),float(abs(ev[vnmask][:,ix]).max())]
                checkpoints[method]=dict(baseline_reproduction_max=repro,baseline_continuous_reference_error=er,source=str(old))
    record(0.)
    print(tag,'initialized','seconds',round(time.perf_counter()-tic,2),flush=True)
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for step in range(round(T/dt)):
            newz=[];newd=[]
            try:
                for i,method in enumerate(METHODS):
                    z,D=advance(models[i],method,funs[i],step*dt,states[i],diffs[i],dt)
                    if not np.isfinite(z).all() or not np.isfinite(D).all() or abs(z).max()>1e6 or EPS*abs(D).max()>1e6:raise FloatingPointError(method+' nonfinite/threshold')
                    newz.append(z);newd.append(D)
            except FloatingPointError as exc:status='stopped';reason=str(exc);break
            states,diffs=newz,newd;reached=(step+1)*dt;record(reached)
            if (step+1)%20==0:print(tag,'step',step+1,'of',round(T/dt),'seconds',round(time.perf_counter()-tic,1),flush=True)
    maxima=np.asarray(maxima);pd=np.asarray(pair_diff);rd=np.asarray(relative_pair_diff);l2=np.asarray(l2)
    windows=[]
    for ci,component in enumerate(COMPONENTS):
        discrepancy=rd[:,:,ci].max(axis=1)
        for threshold in [.01,.05,.1]:
            hit=np.flatnonzero(discrepancy>threshold)
            first=float(times[hit[0]]) if len(hit) else None
            last=float(times[hit[0]-1]) if len(hit) and hit[0]>0 else (0. if len(hit) else reached)
            windows.append(dict(input=component,threshold=threshold,first_exceedance=first,last_prefix_time_within=last,right_censored=not len(hit),max_discrepancy=float(discrepancy.max()),terminal_discrepancy=float(discrepancy[-1])))
    payload=dict(x=x,y=y,common_v_y=ye,x_observation=xobs,u_observation_y=yuobs,v_observation_y=yvobs,t=np.array(times),max_common_normalized=maxima,max_native_normalized=native_maxima,pairwise_absolute_normalized=pd,pairwise_relative=rd,paired_l2_observation=l2,snapshot_t=snap_t,common_u_snapshots=snaps_u,common_v_snapshots=snaps_v,baseline_global_max=baseline_global)
    for i,method in enumerate(METHODS):
        key=['endpoint','centered','fd'][i]
        payload[key+'_initial']=initial_states[i];payload[key+'_final']=states[i]
        payload[key+'_delta_initial']=initial_diffs[i];payload[key+'_delta_final']=diffs[i]
    npz=dest.with_suffix('.npz');np.savez_compressed(npz,**payload)
    initialfloor=float(pd[0].max());l2gain=l2[-1]/l2[0]
    rec=dict(case=case,methods=METHODS,inputs=COMPONENTS,pairs=[[METHODS[a],METHODS[b]] for a,b in PAIRS],status=status,reason=reason,reached=reached,T=T,dt=dt,h=H,dx=DX,epsilon=EPS,kappa=KAPPA,
        spatial_x='Fourier derivatives with zero first-derivative Nyquist multiplier; no filtering',initial_checks=initial_checks,checkpoints=checkpoints,
        physical_grid='u common native nodes; v common centered midpoint edges. Endpoint v[1:] matches; FD v reconstructed by cubic spline in y.',
        observation='|x|<=R, |y|<R, R=5 (A),30(D)' if case in ['A','D'] else 'full periodic x, |y|<=1.8',
        normalization='max absolute numerical perturbed-minus-unperturbed physical response divided by prescribed epsilon',
        agreement_metric='For each input and time: maximum pairwise common-grid physical-field discrepancy divided by max(epsilon, largest response component among all methods); initial interpolation discrepancy included.',
        initial_interpolation_floor_normalized=initialfloor,initial_interpolation_floor_physical=EPS*initialfloor,
        initial_response_normalized=maxima[0].tolist(),terminal_response_normalized=maxima[-1].tolist(),terminal_l2_gain_common_observation=l2gain.tolist(),
        terminal_pairwise_relative=rd[-1].tolist(),agreement_windows=windows,
        boundary='Identical prescribed lower u trace; Endpoint lower exact ghost; FD upper exact-background plus quadratic perturbation extrapolation; Centered auxiliary lower trace freely evolves from its matched initial value.',
        continuous_certificate=False,artifact_sha256=sha(npz),source_sha256=sha(Path(__file__)),seconds=time.perf_counter()-tic)
    dest.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    with (HERE/(tag+'_history.csv')).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f);w.writerow(['case','method','input','time','u_response_over_epsilon','v_response_over_epsilon'])
        for ti,t in enumerate(times):
            for mi,method in enumerate(METHODS):
                for ci,comp in enumerate(COMPONENTS):w.writerow([case,method,comp,t,*maxima[ti,mi,ci]])
    print(tag,'COMPLETE',round(rec['seconds'],1),'initial_floor',initialfloor,'terminal_max_agreement',rd[-1].max(),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('case',choices=['A','D','Gaussian','Sinusoidal']);ap.add_argument('--half-step',action='store_true');args=ap.parse_args();run(args.case,args.half_step)
