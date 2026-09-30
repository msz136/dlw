"""Exact Jacobian action and quadratic remainder in the shared P/v variables."""
from scan import FamilyModel,Parameters,norm
import numpy as np
from numpy.polynomial import Polynomial
from scipy.special import expit

POLY=[Polynomial([0.,1.])]
for _ in range(3):POLY.append(Polynomial([0.,1.,-1.])*POLY[-1].deriv())
class ErrorModel(FamilyModel):
    def linear_u(self,P):return self.C.u_from_P(P,np.zeros(self.X.n))
    def linear_dy(self,u):return self.dy(u,(np.zeros(self.X.n),3*u[-1]-3*u[-2]+u[-3]))
    def jac(self,t,z,e):
        P,v=self.unpack(z);p,q=self.unpack(e);u,_=self.fields(z,t)
        eta=self.linear_u(p);eta_y=self.linear_dy(eta);d1,d2=self.X.d1,self.X.d2
        if self.route=='fd':
            pt=-np.diff(d1((u+2*self.pars.a)*eta),axis=0)/self.h-d2((q[1:]+q[:-1])/2)
            vt=-d1((u+2*self.pars.a)*q+(v-4)*eta)-d2(eta_y)
        else:
            w=v-self.dy(u,self.state_ghosts(u,t));dw=q-eta_y
            df=(u+2*self.A)*eta+self.h**2*(w/16-self.r/4)*dw
            pt=-np.diff(d1(df),axis=0)/self.h-d2(p+(dw[1:]+dw[:-1])/2)
            wt=-d1((u+2*self.A)*dw+(w-4*self.r)*eta)+d2(dw)
            vt=wt+self.linear_dy(self.linear_u(pt))
        return self.pack(pt,vt)
    def quadratic(self,e):
        p,q=self.unpack(e);eta=self.linear_u(p)
        if self.route=='fd':
            pt=-np.diff(self.X.d1(.5*eta**2),axis=0)/self.h
            vt=-self.X.d1(eta*q)
        else:
            dw=q-self.linear_dy(eta)
            pt=-np.diff(self.X.d1(.5*eta**2+self.h**2*dw**2/32),axis=0)/self.h
            wt=-self.X.d1(eta*dw)
            vt=wt+self.linear_dy(self.linear_u(pt))
        return self.pack(pt,vt)
    def ref_x_derivatives(self,t):
        js=np.concatenate(([self.js[0]-1],self.js,[self.js[-1]+1]))[:,None]
        k=self.pars.p+self.pars.q;ell=self.G.ry
        z=k*self.X.x[None,:]+self.G.omega*t+np.log(self.pars.rho/k)+(js+.5)*self.h*ell
        f,g=expit(z+self.G.gamma0),expit(z)
        u=[2*k*k**i*(POLY[i](f)-POLY[i](g)) for i in range(3)]
        v=[2*k*ell*k**i*(POLY[i+1](f)+POLY[i+1](g)) for i in range(3)]
        return u,v
    def analytic_x_rhs(self,t):
        U,V=self.ref_x_derivatives(t);u,ux,uxx=[z[1:-1] for z in U];v,vx,vxx=[z[1:-1] for z in V]
        Y=[(z[2:]-z[:-2])/(2*self.h) for z in U]
        if self.route=='fd':
            pt=-np.diff((u+2*self.pars.a)*ux,axis=0)/self.h-(vxx[1:]+vxx[:-1])/2
            vt=-((u+2*self.pars.a)*vx+(v-4)*ux)-Y[2]
        else:
            w,wx,wxx=[z-y for z,y in zip((v,vx,vxx),Y)]
            hx=(u+2*self.A)*ux+self.h**2*(w/16-self.r/4)*wx
            pt=-np.diff(hx,axis=0)/self.h-(np.diff(uxx,axis=0)/self.h+(wxx[1:]+wxx[:-1])/2)
            wt=-((u+2*self.A)*wx+(w-4*self.r)*ux)+wxx
            bt=self.G.uv([self.js[0]],self.X.x,t,True)[0][0]
            ut=self.C.u_from_P(pt,bt)
            vt=wt+self.dy(ut,self.right_ghost_derivative(ut,t))
        return self.pack(pt,vt)

