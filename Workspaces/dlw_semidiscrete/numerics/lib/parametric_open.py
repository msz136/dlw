"""Background-relative quadratic ghost extrapolation: explicit NEW boundary problem.

The exact background ghost remains analytic; perturbations extrapolate from
three right interior nodes. This replaces fixed perturbation ghost=0.
"""
import numpy as np
from parametric import Model


class OpenModel(Model):
    def __init__(self,*args,**kwargs):
        kwargs['closure']='extrapolated'
        super().__init__(*args,**kwargs)

    def error_fields(self,e):
        P,Q=self.unpack(e)
        eta=np.concatenate((np.zeros((1,self.X.n)),self.h*np.cumsum(P,axis=0)))
        right=3*eta[-1]-3*eta[-2]+eta[-3]
        dy=self.dy(eta,(np.zeros(self.X.n),right))
        return eta,Q+dy if self.model=='structure' else Q

    def state_ghosts(self,u,t):
        gl,gr=self.ghosts(t)
        bg=self.G.uv(self.js[-3:],self.X.x,t)[0]
        eta=u[-3:]-bg
        return gl,gr+3*eta[-1]-3*eta[-2]+eta[-3]

    def fields(self,z,t):
        P,Q=self.unpack(z);u=self.C.u_from_P(P,self.base(t))
        return u,Q+self.dy(u,self.state_ghosts(u,t)) if self.model=='structure' else Q

    def rhs(self,t,z):
        P,Q=self.unpack(z);u=self.C.u_from_P(P,self.base(t));gl,gr=self.state_ghosts(u,t)
        if self.model=='structure':return self.pack(*self.op.rhs(t,P,Q,gl,gr))
        d1,d2=self.X.d1,self.X.d2
        return self.pack(-np.diff(d1(.5*u*u+2*self.pars.a*u),axis=0)/self.h-d2(.5*(Q[1:]+Q[:-1])),
                         -d1((u+2*self.pars.a)*Q)-d2(self.dy(u,(gl,gr)))+4*d1(u))

    def delta(self,t,z,e,linear=False):
        result=super().delta(t,z,e,linear)
        pt,qt=self.unpack(result);p,q=self.unpack(e);eta,_=self.error_fields(e)
        if self.model=='structure':
            # Parent with closure='extrapolated' uses zero exterior P delta.
            pt[-1]+=self.X.d2((2*p[-1]-p[-2])/4)
        else:
            # Parent FD Jacobian uses fixed ghost; replace by extrapolated ghost.
            right=3*eta[-1]-3*eta[-2]+eta[-3]
            qt[-1]-=self.X.d2(right/(2*self.h))
        return self.pack(pt,qt)
