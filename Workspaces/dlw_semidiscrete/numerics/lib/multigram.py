"""Batched, guarded N=2 finite-h Gram fields and their time tangents.

This is an independent evaluation path for numerical experiments.  It leaves
the original arbitrary-N GramRef and production solvers untouched.
"""
import numpy as np
from gramtau import lam


class TwoGram:
    def __init__(self, p=(1., 2.), q=(1., 3.), rho=(3., 4.), a=4., h=.25):
        self.p, self.q, self.rho = map(lambda z: np.asarray(z, dtype=float), (p, q, rho))
        self.a, self.h = float(a), float(h)
        if any(len(z) != 2 for z in (self.p, self.q, self.rho)):
            raise ValueError('TwoGram requires exactly two spectral pairs')
        P, Q = self.p[:, None], self.q[None, :]
        self.rate = P + Q
        self.omega = Q**2 - P**2
        self.chi = lam(P-self.a, h)*lam(Q+self.a, h)
        self.gamma = -(P-(self.a-h/2))/(Q+(self.a-h/2))
        if not (np.all(self.p-self.a < -h/2) and np.all(self.q+self.a > h/2)
                and np.all(self.rho > 0) and np.all(self.chi > 0)
                and np.all(self.gamma > 0)):
            raise ValueError('parameters outside the positive Gram sector')

    def _block(self, j, x, t, is_f, derivative):
        coef = self.rho[:, None]/self.rate * self.chi**int(j)
        if is_f:
            coef = coef*self.gamma
        exponent = self.rate[None]*x[:, None, None] + self.omega[None]*t
        if not np.all(np.isfinite(exponent)) or np.max(exponent) > 650:
            raise FloatingPointError('Gram exponent outside safe double-precision range')
        E = coef[None]*np.exp(exponent)
        a, b, c, d = E[:, 0, 0], E[:, 0, 1], E[:, 1, 0], E[:, 1, 1]
        cross = b*c
        D = (1+a)*(1+d)-cross
        if not np.all(np.isfinite(D)) or np.any(D <= 0):
            raise FloatingPointError('nonpositive or nonfinite Gram determinant')
        # For a 2x2 matrix, ||M||_F ||M^{-1}||_F = ||M||_F^2 / |det M|.
        # This bounds the spectral condition number and detects cancellation.
        frob_cond = ((1+a)**2+b**2+c**2+(1+d)**2)/D
        if not np.all(np.isfinite(frob_cond)) or np.max(frob_cond) > 1e14:
            raise FloatingPointError('ill-conditioned Gram matrix')
        r, w = self.rate, self.omega
        N = (1+d)*r[0,0]*a+(1+a)*r[1,1]*d-(r[0,1]+r[1,0])*cross
        value = N/D
        if not derivative:
            return value
        Dt = w[0,0]*a*(1+d)+w[1,1]*d*(1+a)-(w[0,1]+w[1,0])*cross
        Nt = (w[1,1]*d*r[0,0]*a+(1+d)*r[0,0]*w[0,0]*a
              +w[0,0]*a*r[1,1]*d+(1+a)*r[1,1]*w[1,1]*d
              -(r[0,1]+r[1,0])*(w[0,1]+w[1,0])*cross)
        return (Nt*D-N*Dt)/D**2

    def uv(self, js, x, t, derivative=False):
        js = np.asarray(js, dtype=int)
        x = np.atleast_1d(np.asarray(x, dtype=float))
        lo, hi = int(js.min())-1, int(js.max())+2
        G = {j:self._block(j,x,t,False,derivative) for j in range(lo,hi+1)}
        F = {j:self._block(j,x,t,True,derivative) for j in range(lo,hi+1)}
        u = {j:2*F[j]-G[j]-G[j+1] for j in range(lo,hi)}
        U = np.asarray([u[int(j)] for j in js])
        V = np.asarray([4/self.h*(G[int(j)+1]-G[int(j)])
                        +(u[int(j)+1]-u[int(j)-1])/(2*self.h) for j in js])
        if not (np.all(np.isfinite(U)) and np.all(np.isfinite(V))):
            raise FloatingPointError('nonfinite Gram field')
        return U, V
