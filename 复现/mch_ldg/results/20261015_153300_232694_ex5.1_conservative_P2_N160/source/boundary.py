"""Explicit stationary Dirichlet closure for alignment experiments.

u-hat equals the prescribed endpoint values; r,p,s traces are taken from
inside. Nonlinear boundary products use prescribed u and interior r.
This is OUR closure, not a claim about the authors' unpublished code.
"""
import numpy as np
from scipy.sparse import diags
from .ldg import LDG


class DirichletLDG(LDG):
    def __init__(self,*args,boundary_value=0.,**kwargs):
        self.boundary_value=float(boundary_value)
        super().__init__(*args,**kwargs)

    def _derivative_matrix(self,side):
        if side=='plus':
            w=np.tile(self.mass,self.n)
            return (-diags(1/w)@self.dm.T@diags(w)).tocsr()
        dm=super()._derivative_matrix(side).tolil()
        b=self.k+1
        for l in range(b):
            for m in range(b):
                dm[l,(self.n-1)*b+m]+=self.sign[l]/self.mass[l]
                dm[(self.n-1)*b+l,(self.n-1)*b+m]-=1/self.mass[l]
        return dm.tocsr()

    def deriv_minus(self,u):
        r=super().deriv_minus(u)
        r[0]-=self.boundary_value*self.sign/self.mass
        r[-1]+=self.boundary_value/self.mass
        return r

    def weak_boundary(self,values,right_flux,left_value,right_value):
        ff=right_flux.copy();ff[-1]=right_value
        ll=np.roll(ff,1);ll[0]=left_value
        return (-values@(self.w[:,None]*self.Vd)+ff[:,None]-ll[:,None]*self.sign)/self.mass

    def rhs(self,u):
        r=self.deriv_minus(u);uq=u@self.V.T;rq=r@self.V.T
        um,up=self.traces(u);rm,rp=self.traces(r)
        ur=.5*(um*rm+up*rp)
        g=self.boundary_value;rL=r[0]@self.sign;rR=r[-1].sum()
        p=self.weak_boundary(uq*uq*rq,ur*um,g*g*rL,g*g*rR)
        if self.flux=='conservative':
            ff=self.kappa**2*(um+up)+.25*(um+up)*(um*um+up*up)
            gg=(rm+rp)*(rm*rm+rp*rp)/12
        else:
            ff=2*self.kappa**2*um+um**3;gg=rp**3/3
        ss=self.weak_boundary(rq**3/3,gg,rL**3/3,rR**3/3)
        fg=2*self.kappa**2*g+g**3
        mt=(-self.weak_boundary(2*self.kappa**2*uq+uq**3,ff,fg,fg)
            +self.deriv_plus(p)-self.weak_boundary(rq*rq*uq,ur*rp,g*rL*rL,g*rR*rR)-self.deriv_plus(ss))
        return self.lu.solve(mt.ravel()).reshape(u.shape)

    def energy_rate(self,u,ut=None):
        if ut is None:ut=self.rhs(u)
        rt=(self.dm@ut.ravel()).reshape(u.shape)
        return float(2*np.sum((u*ut+self.deriv_minus(u)*rt)*self.mass))

    def predicted_energy_rate(self,u):
        # Periodic theorem does not automatically apply to this closure.
        return None
