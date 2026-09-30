"""Parameter-dependent DLW study. Historical solvers remain unchanged.

The compatible closure derives exterior P from the SAME ghost u and current
interior u. Background balancing is a separately identified modified RHS.
"""
from dataclasses import dataclass, asdict
import numpy as np
from scipy.special import expit
from dynamics import Grid, StencilRHS
from solver import Chain


@dataclass(frozen=True)
class Parameters:
    a: float = 4.
    p: float = 1.
    q: float = 2.
    rho: float = 3.


class Exact:
    def __init__(self, pars, h, continuous=False):
        self.pars, self.h, self.continuous = pars, h, continuous
        a,p,q,rho = pars.a,pars.p,pars.q,pars.rho
        P,Q=p-a,q+a
        if not (p+q>0 and rho>0 and P < -h/2 and Q>h/2):
            raise ValueError('outside positive regular one-soliton sector')
        self.S=p+q; self.omega=q*q-p*p
        self.ry=1/P+1/Q
        self.chi=np.log((P+h/2)/(P-h/2))+np.log((Q+h/2)/(Q-h/2))
        self.gamma=np.log(-(P+h/2)/(Q-h/2))
        self.gamma0=np.log(-P/Q)

    def uv(self, js, x, t, derivative=False):
        j=np.asarray(js)[:,None]; x=np.asarray(x)[None,:]
        z=self.S*x+self.omega*t+np.log(self.pars.rho/self.S)
        if self.continuous:
            z=z+(j+.5)*self.h*self.ry
            f,g=expit(z+self.gamma0),expit(z)
            if derivative:
                return (2*self.S*self.omega*(f*(1-f)-g*(1-g)),
                        2*self.S*self.ry*self.omega*(f*(1-f)*(1-2*f)+g*(1-g)*(1-2*g)))
            return 2*self.S*(f-g),2*self.S*self.ry*(f*(1-f)+g*(1-g))
        z=z+j*self.chi
        def s(z):
            f=expit(z)
            return self.omega*f*(1-f) if derivative else f
        def u(z): return self.S*(2*s(z+self.gamma)-s(z)-s(z+self.chi))
        return u(z),4*self.S/self.h*(s(z+self.chi)-s(z))+(u(z+self.chi)-u(z-self.chi))/(2*self.h)


class Model:
    def __init__(self, pars=Parameters(), h=.25, nx=128, L=20., yhalf=1.5,
                 model='structure', closure='original', continuous=False):
        self.pars,self.h,self.model,self.closure=pars,h,model,closure
        self.X=Grid(nx,L); self.G=Exact(pars,h,continuous)
        n=round(yhalf/h); self.js=np.arange(-n,n); self.y=(self.js+.5)*h
        self.C=Chain(-n,n-1,h,pars.a); self.np=(2*n-1)*nx
        self.shape=(2*n,nx)
        row=lambda j,t:self.G.uv([j],self.X.x,t)[0][0]
        self.base=lambda t:row(-n,t)
        self.ghosts=lambda t:(row(-n-1,t),row(n,t))
        self.op=StencilRHS(self.C,self.X,self.base,lambda t:self.ghosts(t)[0],lambda t:self.ghosts(t)[1])
        self.op.use_ext=closure=='original'
        self.op._ple=lambda t:(row(-n,t)-row(-n-1,t))/h
        self.op._pre=lambda t:(row(n,t)-row(n-1,t))/h

    def pack(self,P,Q):return np.concatenate((P.ravel(),Q.ravel()))
    def unpack(self,z):return z[:self.np].reshape(self.shape[0]-1,-1),z[self.np:].reshape(self.shape)
    def dy(self,u,ghosts):
        ext=np.concatenate((ghosts[0][None,:],u,ghosts[1][None,:]))
        return (ext[2:]-ext[:-2])/(2*self.h)
    def fields(self,z,t):
        P,Q=self.unpack(z);u=self.C.u_from_P(P,self.base(t))
        return u,Q+self.dy(u,self.ghosts(t)) if self.model=='structure' else Q
    def error_fields(self,e):
        P,Q=self.unpack(e);u=np.concatenate((np.zeros((1,self.X.n)),self.h*np.cumsum(P,axis=0)))
        dy=self.dy(u,(np.zeros(self.X.n),np.zeros(self.X.n)))
        return u,Q+dy if self.model=='structure' else Q
    def exact(self,t,derivative=False):
        u,v=self.G.uv(self.js,self.X.x,t,derivative)
        ghost=self.G.uv([self.js[0]-1,self.js[-1]+1],self.X.x,t,derivative)[0]
        Q=v-self.dy(u,ghost) if self.model=='structure' else v
        return self.pack(np.diff(u,axis=0)/self.h,Q)
    def rhs(self,t,z):
        P,Q=self.unpack(z)
        if self.model=='structure':return self.pack(*self.op(t,P,Q))
        u,v=self.fields(z,t);d1,d2=self.X.d1,self.X.d2
        return self.pack(-np.diff(d1(.5*u*u+2*self.pars.a*u),axis=0)/self.h-d2(.5*(v[1:]+v[:-1])),
                         -d1((u+2*self.pars.a)*v)-d2(self.dy(u,self.ghosts(t)))+4*d1(u))
    def delta(self,t,z,e,linear=False):
        """Algebraically expanded F(z+e)-F(z); linear=True is exact Jacobian action."""
        P,Q=self.unpack(z);p,q=self.unpack(e)
        u,v=self.fields(z,t);eta,ev=self.error_fields(e)
        d1,d2=self.X.d1,self.X.d2;h=self.h;a=self.pars.a
        H=(u+2*a)*eta
        if not linear:H=H+.5*eta*eta
        if self.model=='structure':
            H=H+h*h*(Q/16-.25)*q
            if not linear:H=H+h*h*q*q/32
            # Exterior P perturbations are fixed zero in the original closure.
            left=np.zeros(self.X.n);right=-eta[-1]/h if self.closure=='compatible' else left
            pe=np.concatenate((left[None,:],p,right[None,:]))
            lap=(pe[2:]-2*pe[1:-1]+pe[:-2])/(h*h)
            pt=-np.diff(d1(H),axis=0)/h-d2(.5*(ev[1:]+ev[:-1])-h*h*lap/4)
            qt=-d1((u+2*a)*q+(Q-4)*eta+(0 if linear else eta*q))+d2(q)
        else:
            pt=-np.diff(d1(H),axis=0)/h-d2(.5*(q[1:]+q[:-1]))
            qt=-d1((u+2*a)*q+Q*eta+(0 if linear else eta*q))-d2(self.dy(eta,(np.zeros(self.X.n),np.zeros(self.X.n))))+4*d1(eta)
        return self.pack(pt,qt)


def rk4(fun,t,z,dt):
    k1=fun(t,z);k2=fun(t+dt/2,z+dt*k1/2);k3=fun(t+dt/2,z+dt*k2/2);k4=fun(t+dt,z+dt*k3)
    return z+dt*(k1+2*k2+2*k3+k4)/6


def evolve(fun,z,T,dt,observe=None):
    n=int(np.ceil(T/dt));dt=T/n;t=0.
    for i in range(n):
        zz=rk4(fun,t,z,dt)
        if not np.all(np.isfinite(zz)) or np.max(abs(zz))>1e3:return z,t,False
        z=zz;t=(i+1)*dt
        if observe is not None:observe(t,z)
    return z,t,True
