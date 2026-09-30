"""Fixed-physical-h DLW family, with common (P=delta_- u, v) time state.

All schemes use the same continuous boundary and quadratic extrapolation of
the right boundary perturbation. Historical solvers remain unchanged.
"""
from pathlib import Path
import sys
import numpy as np
from scipy.special import expit

LIB=Path(__file__).resolve().parents[1]/'dlw_semidiscrete/numerics/lib'
sys.path.insert(0,str(LIB))
from parametric import Parameters,Exact
from parametric_open import OpenModel

class FamilyModel(OpenModel):
    def __init__(self,pars,h=.125,nx=256,L=20.,yhalf=1.5,route='sd',c=0.,kappa=0.):
        super().__init__(pars,h,nx,L,yhalf,model='structure' if route=='sd' else 'fd',continuous=True)
        self.route,self.c,self.kappa=route,c,kappa
        self.A=pars.a+c*h*h
        self.r=1+kappa*h*h
        self.H=h*self.r
        self.sminus=self.A-self.H/2
        self.splus=self.A+self.H/2
        if route=='sd' and not (self.H>0 and pars.p<self.sminus and pars.q+self.sminus>0):
            raise ValueError('Parameter family leaves regular positive one-soliton branch')

    def exact(self,t,derivative=False):
        u,v=self.G.uv(self.js,self.X.x,t,derivative)
        return self.pack(np.diff(u,axis=0)/self.h,v)

    def fields(self,z,t):
        P,v=self.unpack(z)
        return self.C.u_from_P(P,self.base(t)),v

    def right_ghost_derivative(self,ut,t):
        # Differentiate the same explicit boundary rule used in reconstruction.
        glt,grt=self.G.uv([self.js[0]-1,self.js[-1]+1],self.X.x,t,True)[0]
        bgt=self.G.uv(self.js[-3:],self.X.x,t,True)[0]
        eta=ut[-3:]-bgt
        return glt,grt+3*eta[-1]-3*eta[-2]+eta[-3]

    def rhs(self,t,z):
        P,v=self.unpack(z);u=self.C.u_from_P(P,self.base(t))
        ghosts=self.state_ghosts(u,t)
        d1,d2=self.X.d1,self.X.d2
        uy=self.dy(u,ghosts)
        if self.route=='fd':
            H=.5*u*u+2*self.pars.a*u
            Pt=-np.diff(d1(H),axis=0)/self.h-d2((v[1:]+v[:-1])/2)
            vt=-d1((u+2*self.pars.a)*v-4*u)-d2(uy)
        else:
            w=v-uy
            flux=.5*u*u+2*self.A*u+self.h**2*(w*w/32-self.r*w/4)
            # Exact short closure: delta_- u + M_- w = M_- v - h² Delta_h P/4.
            Pt=-np.diff(d1(flux),axis=0)/self.h-d2(P+(w[1:]+w[:-1])/2)
            wt=-d1((u+2*self.A)*w-4*self.r*u)+d2(w)
            bt=self.G.uv([self.js[0]],self.X.x,t,True)[0][0]
            ut=self.C.u_from_P(Pt,bt)
            vt=wt+self.dy(ut,self.right_ghost_derivative(ut,t))
        return self.pack(Pt,vt)

    def finite_fields(self,js,x,t):
        """Exact member of this finite-h family, for independent identity checks."""
        p,q,rho=self.pars.p,self.pars.q,self.pars.rho
        k=p+q;om=q*q-p*p
        chi=(p-self.sminus)*(q+self.splus)/((p-self.splus)*(q+self.sminus))
        gamma=-(p-self.sminus)/(q+self.sminus)
        if chi<=0 or gamma<=0:raise ValueError('Invalid real logarithm branch')
        lc=np.log(chi);lg=np.log(gamma)
        z=k*np.asarray(x)[None,:]+om*t+np.log(rho/k)+np.asarray(js)[:,None]*lc
        U=lambda zz:k*(2*expit(zz+lg)-expit(zz)-expit(zz+lc))
        return U(z),4*k/self.h*(expit(z+lc)-expit(z))+(U(z+lc)-U(z-lc))/(2*self.h)
