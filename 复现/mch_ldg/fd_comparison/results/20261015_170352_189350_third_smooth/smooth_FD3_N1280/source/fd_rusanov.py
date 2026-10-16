"""Local Lax--Friedrichs/Rusanov flux on the original momentum equation.

Freeze a_i=u_i^2-(D1u_i)^2 to set the local advective speed. This is a
consistent dissipative baseline, not a proof of a nonlinear entropy property.
"""
import numpy as np
from fd import DirectFD


class RusanovFD(DirectFD):
    def rhs(self,u):
        m=self.momentum(u);r=self.d1(u);a=u*u-r*r
        f=2*self.kappa**2*u+a*m
        speed=np.maximum(abs(a),abs(np.roll(a,-1)))
        ff=.5*(f+np.roll(f,-1))-.5*speed*(np.roll(m,-1)-m)
        return self.helmholtz(-(ff-np.roll(ff,1))/self.h)
