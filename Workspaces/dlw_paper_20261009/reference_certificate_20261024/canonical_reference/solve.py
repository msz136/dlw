"""Nonlinear DLW candidate continuum references; NOT an error certificate.

Fourier-Galerkin in x (quadratic products exactly dealiased), Chebyshev
collocation in y. Evolves the exact integral formulation, with no upper ghost.
u_t=-u_xx-(u*u/2+4*u)_x-I(w_xx), w_t=w_xx-((u+4)*w-4*u)_x.
v=u_y+w. I integrates from -2 to y. Fourier projection is explicit below.
"""
from pathlib import Path
import json,sys,time
import numpy as np
from numpy.polynomial import chebyshev as ch
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent

class Solver:
    def __init__(self,case,M,ny):
        self.case,self.M,self.ny=case,M,ny
        self.P=24. if case=='Sinusoidal' else 192.
        self.N=2*M+1
        self.modes=np.rint(np.fft.fftfreq(self.N)*self.N).astype(int)
        self.xi=2*np.pi*self.modes/self.P
        self.Npad=3*M+1
        self.ix=self.modes%self.Npad
        self.y=-2*np.cos(np.pi*np.arange(ny+1)/ny)
        z=self.y/2
        V=ch.chebvander(z,ny)
        self.C=np.linalg.inv(V)
        I=np.zeros_like(V);D=np.zeros_like(V)
        for j in range(ny+1):
            b=np.zeros(j+1);b[-1]=1
            p=ch.chebint(b)
            I[:,j]=2*(ch.chebval(z,p)-ch.chebval(-1,p))
            D[:,j]=ch.chebval(z,ch.chebder(b))/2
        self.I=I@self.C;self.I[0]=0
        self.D=D@self.C
    def initial(self):
        e=np.sin(np.pi*(self.y+2)/4)
        ey=np.pi/4*np.cos(np.pi*(self.y+2)/4)
        f=np.zeros(self.N,dtype=complex);g=f.copy()
        if self.case=='Sinusoidal':
            f[1]=f[-1]=.5;g[1]=-.5j;g[-1]=.5j
            au,av=.03,.02
        else:
            f=6*np.sqrt(np.pi)/self.P*np.exp(-9*self.xi**2)
            g=f.copy();au,av=.05,.03
        u=au*e[:,None]*f
        w=av*e[:,None]*g-au*ey[:,None]*f
        u[0]=0
        return np.array([u,w],dtype=complex)
    def product(self,a,b):
        ap=np.zeros((self.ny+1,self.Npad),complex);bp=ap.copy()
        ap[:,self.ix]=a;bp[:,self.ix]=b
        vals=np.fft.ifft(ap*self.Npad,axis=-1)*np.fft.ifft(bp*self.Npad,axis=-1)
        return (np.fft.fft(vals,axis=-1)/self.Npad)[:,self.ix]
    def rhs(self,t,z):
        u,w=z.reshape(2,self.ny+1,self.N)
        dx=1j*self.xi;dxx=-self.xi**2
        ut=-dxx*u-dx*(self.product(u,u)/2+4*u)-self.I@(dxx*w)
        wt=dxx*w-dx*(self.product(u,w)+4*w-4*u)
        ut[0]=0
        return np.array([ut,wt]).ravel()
    def sample(self,z,x,y):
        u,w=z.reshape(2,self.ny+1,self.N)
        vy=self.D@u+w
        interp=ch.chebvander(np.asarray(y)/2,self.ny)@self.C
        expo=np.exp(1j*np.outer(self.xi,np.asarray(x)))
        return np.array([(interp@u@expo).real,(interp@vy@expo).real])
    def boundary(self,x,t):
        if self.case=='Sinusoidal':
            xi=np.pi/12
            p=.03*np.pi/4*np.cos(xi*(x-4*t))*np.cosh(xi*xi*t)
            v=.03*np.pi/4*np.cos(xi*(x-4*t))*np.sinh(xi*xi*t)
        else:
            def heat(s):
                return 6/np.sqrt(36+4*s)*sum(np.exp(-(x-4*t+192*m)**2/(36+4*s)) for m in [-1,0,1])
            p=.05*np.pi/8*(heat(-t)+heat(t))
            v=.05*np.pi/8*(heat(-t)-heat(t))
        return p,v

def run(case,M,ny,dt):
    start=time.time();s=Solver(case,M,ny);z=s.initial().ravel()
    times=np.linspace(0,.01,11);states=[z.copy()]
    count=round(.01/dt);assert abs(count*dt-.01)<1e-14
    stride=count//10;assert stride*10==count
    for j in range(count):
        t=j*dt
        k1=s.rhs(t,z);k2=s.rhs(t+dt/2,z+dt*k1/2)
        k3=s.rhs(t+dt/2,z+dt*k2/2);k4=s.rhs(t+dt,z+dt*k3)
        z+=dt/6*(k1+2*k2+2*k3+k4)
        if (j+1)%stride==0:states.append(z.copy())
    # A common comparison grid includes both y boundaries, x=0, and all fine
    # physical-wave nodes needed for comparisons. It is not an error enclosure.
    x=np.linspace(-s.P/2,s.P/2,769)[:-1];y=np.linspace(-2,2,161)
    field=s.sample(z,x,y);initial=s.sample(states[0],x,y)
    uc,wc=z.reshape(2,ny+1,s.N)
    expo=np.exp(1j*np.outer(s.xi,x))
    pcalc=(s.D@uc@expo).real[0];vcalc=field[1,0]
    pexact,vexact=s.boundary(x,.01)
    name=f'{case}_M{M}_Y{ny}_dt{dt:.1e}'
    out=dict(case=case,M=M,ny=ny,dt=dt,T=.01,period=s.P,
       physical_cutoff=float(np.max(np.abs(s.xi))),
       maximum_u=float(abs(field[0]).max()),maximum_v=float(abs(field[1]).max()),
       change_u=float(abs(field[0]-initial[0]).max()),change_v=float(abs(field[1]-initial[1]).max()),
       boundary_p_error=float(abs(pcalc-pexact).max()),boundary_v_error=float(abs(vcalc-vexact).max()),
       final_fourier_edge_u=float(abs(uc[:,abs(s.modes)>=M-2]).max()),
       final_fourier_edge_w=float(abs(wc[:,abs(s.modes)>=M-2]).max()),
       seconds=time.time()-start,certificate=False,eta_u=None,eta_v=None,
       method='Fourier-Galerkin dealiased; Chebyshev-y integration; RK4; float64')
    np.savez_compressed(HERE/(name+'.npz'),x=x,y=y,field=field,times=times,
        coefficients=np.array(states).reshape(-1,2,ny+1,s.N),y_cheb=s.y,modes=s.modes,period=s.P)
    (HERE/(name+'.json')).write_text(json.dumps(out,indent=2))
    print(json.dumps(out),flush=True)
    return out

if __name__=='__main__':
    run(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),float(sys.argv[4]))
