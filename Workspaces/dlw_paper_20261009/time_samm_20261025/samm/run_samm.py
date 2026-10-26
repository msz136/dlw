"""Natural Centered-SD with matched fixed/frozen/moving mapped x differences.

The physical field is v=diff_y(u)+(w_k+w_{k-1})/2, w=4*omega/h.
SAMM uses the exact continuous-x conservation density rho=1-w/4.
No reference field enters the interior right-hand side.
"""
from pathlib import Path
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import sys, json, hashlib, time, argparse
import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
ROOT=PROJECT.parents[1]
AUDIT=PROJECT/'spatial_audit_20261023'
sys.path.insert(0,str(AUDIT))
from run import Model, HALF_WIDTHS

def physical_v(u,w,h):return np.diff(u,axis=0)/h+(w[1:]+w[:-1])/2

def initial_state(m,x):
    u=m.profile(m.y,0,x)[0]
    yv=(m.y[1:]+m.y[:-1])/2
    v=m.profile(yv,0,x)[1]
    _,g=m.G.tau(m.y[:1]/m.h-.5,x,0,False)
    w=np.empty_like(u);w[0]=4*m.G.cov(g,0,2)[0]
    r=2*(v-np.diff(u,axis=0)/m.h)
    for k in range(1,len(u)):w[k]=r[k-1]-w[k-1]
    return np.array([u,w])

class MappedGrid:
    def __init__(self,xi,L):
        self.xi=xi;self.L=L;self.dx=L/len(xi)
    def dxi(self,z):return (np.roll(z,-1,axis=-1)-np.roll(z,1,axis=-1))/(2*self.dx)
    def dxxi(self,z):return (np.roll(z,-1,axis=-1)-2*z+np.roll(z,1,axis=-1))/self.dx**2
    def set(self,s):
        self.x=self.xi+s;self.J=1+self.dxi(s);self.Jxi=self.dxi(self.J)
        self.spacing=np.diff(np.r_[self.x,self.x[0]+self.L])
        assert self.J.min()>0 and self.spacing.min()>0
    def d1(self,z):return self.dxi(z)/self.J
    def d2(self,z):return self.dxxi(z)/self.J**2-self.Jxi*self.dxi(z)/self.J**3

def initial_mesh(m,nfine=40001):
    fine=np.linspace(-m.half,m.half,nfine)
    density=[]
    for x in np.array_split(fine,80):
        w=initial_state(m,x)[1]
        density.append((1-w/4).mean(axis=0))
    rho=np.concatenate(density)
    assert rho.min()>0
    mass=np.r_[0,cumulative_trapezoid(rho,fine)]
    nodes=np.interp(np.arange(m.nx)/m.nx*mass[-1],mass,fine)
    return nodes,dict(dense_points=nfine,rho_min=float(rho.min()),rho_max=float(rho.max()),total_mass=float(mass[-1]))

def lower_rates(m,x,t):
    _,f=m.G.tau(m.y[:1]/m.h-.5,x,t,True)
    _,g=m.G.tau(m.y[:1]/m.h-.5,x,t,False)
    ut=2*(m.G.cov(f,0,1)-m.G.cov(g,0,1))[0]
    ux=2*(m.G.cov(f,0,0)-m.G.cov(g,0,0))[0]
    return ut,ux

def rhs(m,grid,t,state,mode):
    z,s=state;u,w=z;h=m.h
    grid.set(s)
    v=physical_v(u,w,h)
    F=u*u/2+2*m.a*u+h*h*(w*w/32-w/4)
    r=-np.diff(grid.d1(F),axis=0)/h-grid.d2(v)
    boundary,ux0=lower_rates(m,grid.x,t)
    ut=np.concatenate((boundary[None],boundary[None]+h*np.cumsum(r,axis=0)))
    wt=grid.d2(w)-grid.d1((u+2*m.a)*w-4*u)
    vel=np.zeros(m.nx)
    if mode=='moving':
        rho=1-w/4;rhobar=rho.mean(axis=0)
        assert rhobar.min()>0
        qbar=((u+2*m.a)*rho-grid.d1(rho)-2*m.a).mean(axis=0)
        vel=(qbar-qbar[0])/rhobar
        ut+=vel*grid.d1(u);wt+=vel*grid.d1(w)
        # The lower u trace is prescribed continuously on the moving nodes.
        ut[0]=boundary+vel*ux0
    return np.array([ut,wt]),vel

def plus(state,rate,factor):return tuple(a+factor*b for a,b in zip(state,rate))
def rk4(m,g,t,state,dt,mode):
    k1=rhs(m,g,t,state,mode)
    k2=rhs(m,g,t+dt/2,plus(state,k1,dt/2),mode)
    k3=rhs(m,g,t+dt/2,plus(state,k2,dt/2),mode)
    k4=rhs(m,g,t+dt,plus(state,k3,dt),mode)
    return tuple(z+dt*(a+2*b+2*c+d)/6 for z,a,b,c,d in zip(state,k1,k2,k3,k4))

def native_errors(m,x,u,v,t):
    r=HALF_WIDTHS[m.case];yv=(m.y[1:]+m.y[:-1])/2;mx=abs(x)<=r
    eu=m.profile(m.y,t,x)[0];ev=m.profile(yv,t,x)[1]
    error=[float(abs((u-eu)[abs(m.y)<r][:,mx]).max()),float(abs((v-ev)[abs(yv)<r][:,mx]).max())]
    return error,eu,ev

def mesh_diagnostics(m,g,state):
    z,s=state;g.set(s);rho=(1-z[1]/4).mean(axis=0)
    cell=(rho+np.roll(rho,-1))*g.spacing/2
    return dict(min_J=float(g.J.min()),min_spacing=float(g.spacing.min()),max_spacing=float(g.spacing.max()),rho_min=float(rho.min()),rho_max=float(rho.max()),mass=float(cell.sum()),max_cell_mass_deviation=float(abs(cell/cell.mean()-1).max()))

def run(case,mode,dt=1e-4):
    stem=f'{case}_{mode}_{dt:g}'
    dest=HERE/(stem+'.json')
    if dest.exists():print('Retained',dest.name,flush=True);return
    start=time.perf_counter();m=Model(case,'Centered-SD',.1,.1)
    grid=MappedGrid(m.x.copy(),2*m.half)
    meshfile=HERE/f'{case}_initial_mesh.npz'
    if not meshfile.exists():
        xadapt,meshmeta=initial_mesh(m)
        np.savez_compressed(meshfile,x=xadapt)
        (HERE/f'{case}_initial_mesh.json').write_text(json.dumps(meshmeta,indent=2))
    else:xadapt=np.load(meshfile)['x']
    x0=m.x.copy() if mode=='uniform' else xadapt
    z0=initial_state(m,x0);state=(z0.copy(),x0-grid.xi)
    initial_error,_,_=native_errors(m,x0,z0[0],physical_v(*z0,m.h),0)
    assert max(initial_error)<1e-11
    times=[0.];xs=[x0.copy()];diagnostics=[mesh_diagnostics(m,grid,state)]
    error_history=[initial_error];T=.01
    for i in range(round(T/dt)):
        state=rk4(m,grid,i*dt,state,dt,mode)
        assert np.isfinite(state[0]).all() and np.max(abs(state[0]))<1e6
        if (i+1)%max(1,round(.001/dt))==0:
            t=(i+1)*dt;times.append(t);xs.append(grid.xi+state[1]);diagnostics.append(mesh_diagnostics(m,grid,state))
            error_history.append(native_errors(m,xs[-1],state[0][0],physical_v(*state[0],m.h),t)[0])
    z,s=state;x=grid.xi+s;v=physical_v(*z,m.h)
    errors,exactu,exactv=native_errors(m,x,z[0],v,T)
    grid.set(s);rho=(1-z[1]/4).mean(axis=0)
    artifact=HERE/(stem+'.npz')
    np.savez_compressed(artifact,z=z,z0=z0,u=z[0],v=v,u_exact=exactu,v_exact=exactv,x=x,x0=x0,xi=grid.xi,y=m.y,yv=(m.y[1:]+m.y[:-1])/2,rho=rho,rho0=(1-z0[1]/4).mean(axis=0),times=times,xs=xs,error_history=error_history)
    saved=np.load(artifact);independent_v=np.diff(saved['u'],axis=0)/m.h+(saved['z'][1,1:]+saved['z'][1,:-1])/2
    reconstruction=float(abs(independent_v-saved['v']).max())
    rec=dict(case=case,mesh=mode,method='natural Centered-SD',integrator='RK4',h=.1,computational_dx=.1,dt=dt,T=T,status='complete',nx=m.nx,ny=len(m.y),compute_x=[-m.half,m.half],evaluation_half_width=HALF_WIDTHS[case],error=errors,initial_error=initial_error,initial_mesh_diagnostics=diagnostics[0],final_mesh_diagnostics=diagnostics[-1],min_J_all=min(d['min_J'] for d in diagnostics),min_spacing_all=min(d['min_spacing'] for d in diagnostics),max_initial_displacement=float(abs(x0-grid.xi).max()),max_evolution_displacement=float(abs(x-x0).max()),relative_mass_drift=float(abs(diagnostics[-1]['mass']/diagnostics[0]['mass']-1)),native_reconstruction_error=reconstruction,lower_u_boundary_error=float(abs(z[0,0]-m.profile(m.y[:1],T,x)[0,0]).max()),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),seconds=time.perf_counter()-start)
    dest.write_text(json.dumps(rec,indent=2),encoding='utf8');print(json.dumps(rec),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case',choices=['A','D']);p.add_argument('--mode',choices=['uniform','frozen','moving','all'],default='all');p.add_argument('--dt',type=float,default=1e-4);a=p.parse_args()
    for mode in (['uniform','frozen','moving'] if a.mode=='all' else [a.mode]):run(a.case,mode,a.dt)
