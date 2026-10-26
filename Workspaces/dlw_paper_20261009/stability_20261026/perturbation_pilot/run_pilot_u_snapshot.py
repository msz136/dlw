"""Small current-Centered-SD perturbation pilot, not a continuum certificate.

The physical initialization is u_eps=u_base+eps*psi(y)*cos(k*x), v_eps=v_base.
psi=sin^2(pi*(y-yL)/(yR-yL)); both psi and psi_y vanish at yL,yR.
The lower u trace is prescribed identically for the two trajectories.
An algebraically subtracted nonlinear difference system avoids losing a small
perturbation to cancellation. It is the same spatial system, without filtering.
"""
from pathlib import Path
import argparse, csv, hashlib, json, sys, time
import numpy as np

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
PROBE=PROJECT/'spatial_audit_20261023/separated/reconstruction_probe'
sys.path.insert(0,str(PROBE))
from probe import Model, invert, transform, HALF_WIDTHS
from rerun_20261024 import rhs
HERE.mkdir(parents=True,exist_ok=True)
EPS=1e-6; MX=4; T=.01

def setup(case,dx,h):
    m=Model(case,'Centered-SD',dx,h);m.gauge='local'
    # Fixed physical transverse endpoints across this refinement diagnostic.
    yl,yr=-m.half+.05,m.half-.05
    m.y=np.linspace(yl,yr,round((yr-yl)/h)+1);m.yv=m.y.copy();m.cache={}
    yv=(m.y[1:]+m.y[:-1])/2
    u=m.profile(m.y,0)[0];v=m.profile(yv,0)[1]
    _,g=m.G.tau(m.y[:1]/h-.5,m.x,0,False)
    w0=4*m.G.cov(g,0,2)[0]
    w,_,_=invert(m,u,v,w0)
    psi=np.sin(np.pi*(m.y-yl)/(yr-yl))**2
    psi[0]=psi[-1]=0.
    du=EPS*psi[:,None]*np.cos(2*np.pi*MX*m.x/(2*m.half))[None,:]
    dv=np.zeros_like(v)
    dw=np.empty_like(u);dw[0]=0.
    for j in range(1,len(u)):dw[j]=2*(dv[j-1]-(du[j]-du[j-1])/h)-dw[j-1]
    return m,np.array([u,w]),np.array([du,dw]),yv

def delta_rhs(m,z,d):
    u,w=z;du,dw=d;h=m.h
    # H(u,w)=u^2/2+2a*u+h^2*(w^2/32-w/4).
    dH=(u+2*m.a)*du+du*du/2+h*h*((w/16-.25)*dw+dw*dw/32)
    dv=np.diff(du,axis=0)/h+(dw[1:]+dw[:-1])/2
    r=-np.diff(m.d1(dH),axis=0)/h-m.d2(dv)
    dut=np.concatenate((np.zeros_like(du[:1]),h*np.cumsum(r,axis=0)))
    dwt=m.d2(dw)-m.d1((u+2*m.a)*dw+w*du+du*dw-4*du)
    return np.array([dut,dwt])

def pair_rhs(m,t,z,d):return rhs(m,t,z),delta_rhs(m,z,d)

def advance(m,t,z,d,dt):
    a,b=pair_rhs(m,t,z,d)
    c,e=pair_rhs(m,t+dt/2,z+dt*a/2,d+dt*b/2)
    f,g=pair_rhs(m,t+dt/2,z+dt*c/2,d+dt*e/2)
    i,j=pair_rhs(m,t+dt,z+dt*f,d+dt*g)
    return z+dt*(a+2*c+2*f+i)/6,d+dt*(b+2*e+2*g+j)/6

def measure(m,du,dv,yv):
    R=HALF_WIDTHS[m.case];ix=abs(m.x)<=R
    return [float(np.max(abs(du[abs(m.y)<R][:,ix]))),float(np.max(abs(dv[abs(yv)<R][:,ix])))]

def run(case='A',dx=.1,h=.1,dt=1e-4):
    tag=f'{case}_dx{dx:g}_h{h:g}_dt{dt:g}'
    dest=HERE/(tag+'.json')
    if dest.exists():print('Preserved',tag,flush=True);return
    tic=time.perf_counter();m,z,d,yv=setup(case,dx,h);z0=z.copy();d0=d.copy()
    dv0=transform(m,*d)
    initial_error=float(abs(dv0).max())
    direct=rhs(m,0,z+d)-rhs(m,0,z)
    algebra_error=float(abs(delta_rhs(m,z,d)-direct).max())
    assert initial_error<1e-18
    assert algebra_error<1e-10
    history=[];times=[];snaps=[];base_snaps=[];status='complete';reason=None
    def save(t):
        dv=transform(m,*d)
        amp=measure(m,d[0],dv,yv)
        history.append(amp);times.append(t)
        if len(times)==1 or abs(t/T*10-round(t/T*10))<1e-10:
            snaps.append(d.copy());base_snaps.append(z.copy())
    save(0.)
    reached=0.
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        for n in range(round(T/dt)):
            try:
                zn,dn=advance(m,n*dt,z,d,dt)
                if not np.isfinite(zn).all() or not np.isfinite(dn).all():raise FloatingPointError('nonfinite')
                if max(float(abs(zn).max()),float(abs(zn+dn).max()))>1e6:raise FloatingPointError('amplitude threshold 1e6')
            except FloatingPointError as exc:
                status='stopped';reason=str(exc);break
            z,d=zn,dn;reached=(n+1)*dt;save(reached)
    artifact=dest.with_suffix('.npz')
    np.savez_compressed(artifact,x=m.x,y=m.y,yv=yv,z0=z0,d0=d0,z=z,d=d,u=z[0],v=transform(m,*z),u_perturbed=z[0]+d[0],v_perturbed=transform(m,*z)+transform(m,*d),delta_u=d[0],delta_v=transform(m,*d),t=times,amplitudes=history,snapshots=snaps,base_snapshots=base_snaps)
    rec=dict(case=case,dx=dx,h=h,dt=dt,T=T,reached=reached,status=status,reason=reason,epsilon=EPS,x_mode=MX,x_wavenumber=2*np.pi*MX/(2*m.half),y_interval=[float(m.y[0]),float(m.y[-1])],x_interval=[-m.half,m.half],nx=m.nx,ny=len(m.y),initial_physical_perturbation='du=eps*sin(pi*(y-yL)/(yR-yL))^2*cos(2*pi*mx*x/Lx), dv=0',boundary='Identical unperturbed analytic lower u_t, lower w perturbation initially zero and then freely evolved',initial_amplitude=history[0],final_amplitude=history[-1],gain_from_u_initial=[v/history[0][0] for v in history[-1]],initial_v_perturbation_rounding=initial_error,algebraic_rhs_subtraction_check=algebra_error,reference_status='No perturbed continuum reference or error certificate; same-discrete-system trajectory separation only',filtering=False,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),seconds=time.perf_counter()-tic)
    dest.write_text(json.dumps(rec,indent=2),encoding='utf-8')
    with (HERE/(tag+'_history.csv')).open('w',newline='',encoding='utf-8') as f:
        wr=csv.writer(f);wr.writerow(['time','max_delta_u','max_delta_v']);wr.writerows(zip(times,*np.array(history).T))
    print(json.dumps(rec),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--case',default='A');ap.add_argument('--dx',type=float,default=.1);ap.add_argument('--h',type=float,default=.1);ap.add_argument('--dt',type=float,default=1e-4);a=ap.parse_args();run(a.case,a.dx,a.h,a.dt)
