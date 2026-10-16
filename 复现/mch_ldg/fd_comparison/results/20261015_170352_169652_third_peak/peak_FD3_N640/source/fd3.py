"""Third-order upwind finite difference of the original momentum flux.

Use fourth-order centered r=D1u and m=(I-D2)u, and a third-order
Lax--Friedrichs split derivative of F=2*kappa^2*u+(u^2-r^2)*m.
At every RK stage alpha=max|u^2-r^2| is frozen as a spatial constant.
This makes the full spatial RHS third order, not fourth order.
No limiter, filtering or state-dependent parameter fitting is applied.
"""
import numpy as np
from fd import DirectFD


class ThirdOrderFD(DirectFD):
    def __init__(self,n,left,right,kappa=0.,order=3,offset=0.):
        if order!=3:raise ValueError(order)
        super().__init__(n,left,right,kappa=kappa,order=4,offset=offset)
        self.order=3

    def upwind_left(self,f):
        return (np.roll(f,2)-6*np.roll(f,1)+3*f+2*np.roll(f,-1))/(6*self.h)

    def upwind_right(self,f):
        return (-2*np.roll(f,1)-3*f+6*np.roll(f,-1)-np.roll(f,-2))/(6*self.h)

    def rhs(self,u):
        m=self.momentum(u);r=self.d1(u);a=u*u-r*r
        F=2*self.kappa**2*u+a*m
        speed=np.max(abs(a))
        mt=-.5*(self.upwind_left(F+speed*m)+self.upwind_right(F-speed*m))
        return self.helmholtz(mt)
