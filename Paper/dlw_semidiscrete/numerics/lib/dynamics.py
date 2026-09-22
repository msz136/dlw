"""Controlled dynamics experiments: exact N=1 fields and matched FD models.

The stencil is the existing fourth-order periodic D1, D2=D1(D1).
No filtering, damping, or exact interior resetting is used.
"""
import numpy as np
from scipy.special import expit
from solver import Chain, DLWChainRHS

CASES = {'A': (1., 2., 3.), 'B': (2., 3., 5.)}


class Reference:
    """Stable closed N=1 version of GramRef / ContRef, independently checked."""
    def __init__(self, case='A', h=.25, continuum=False):
        self.p, self.q, self.rho = CASES[case]
        self.a, self.h, self.continuum = 4., h, continuum
        self.S = self.p+self.q
        P, Q = self.p-self.a, self.q+self.a
        self.ry = 1/P+1/Q
        self.logchi = np.log((P+h/2)/(P-h/2))+np.log((Q+h/2)/(Q-h/2))
        self.loggamma = np.log(-(P+h/2)/(Q-h/2))
        self.loggamma0 = np.log(-P/Q)

    def uv(self, js, x, t):
        js, x = np.asarray(js).reshape(-1, 1), np.asarray(x).reshape(1, -1)
        z = self.S*x+(self.q**2-self.p**2)*t+np.log(self.rho/self.S)
        if self.continuum:
            z = z+(js+.5)*self.h*self.ry
            f, g = expit(z+self.loggamma0), expit(z)
            return 2*self.S*(f-g), 2*self.S*self.ry*(f*(1-f)+g*(1-g))
        z = z+js*self.logchi
        def u(zz):
            return self.S*(2*expit(zz+self.loggamma)-expit(zz)-expit(zz+self.logchi))
        uu = u(z)
        vv = 4*self.S/self.h*(expit(z+self.logchi)-expit(z))
        vv += (u(z+self.logchi)-u(z-self.logchi))/(2*self.h)
        return uu, vv


class Grid:
    def __init__(self, n, L):
        self.n, self.L, self.dx = n, L, L/n
        self.x = -L/2+np.arange(n)*self.dx

    def d1(self, f):
        return (np.roll(f, 2, axis=-1)-8*np.roll(f, 1, axis=-1)
                +8*np.roll(f, -1, axis=-1)-np.roll(f, -2, axis=-1))/(12*self.dx)

    def d2(self, f):
        return self.d1(self.d1(f))


class StencilRHS(DLWChainRHS):
    def d1(self, f): return self.X.d1(f)
    def d2(self, f): return self.X.d2(f)
    def _tv(self, f): return self.d1(f)
    def _tv2(self, f): return self.d2(f)


class Problem:
    def __init__(self, case='A', h=.25, nx=256, L=20., model='structure',
                 continuous_data=False, yhalf=1.5):
        self.G = Reference(case, h, continuous_data)
        self.X = Grid(nx, L)
        # All h comparisons have the same midpoint cell domain [-yhalf,yhalf].
        n = int(round(yhalf/h))
        self.C = Chain(-n, n-1, h, 4.)
        self.js = np.arange(-n, n)
        self.model = model
        self.calls = 0
        row = lambda j, t: self.G.uv([j], self.X.x, t)[0][0]
        self.base = lambda t: row(self.C.jL, t)
        self.ghosts = lambda t: (row(self.C.jL-1, t), row(self.C.jR+1, t))
        self.op = StencilRHS(self.C, self.X, self.base,
                             lambda t:self.ghosts(t)[0], lambda t:self.ghosts(t)[1])
        self.op.use_ext = True
        self.op._ple = lambda t: (row(self.C.jL,t)-row(self.C.jL-1,t))/h
        self.op._pre = lambda t: (row(self.C.jR+1,t)-row(self.C.jR,t))/h

    def initial(self):
        u, v = self.G.uv(self.js, self.X.x, 0.)
        P = np.diff(u, axis=0)/self.C.h
        Q = v-self.dy(u,0.) if self.model=='structure' else v
        return P, Q

    def dy(self, u, t):
        gl, gr = self.ghosts(t)
        ext = np.concatenate((gl[None,:],u,gr[None,:]))
        return (ext[2:]-ext[:-2])/(2*self.C.h)

    def fields(self, P, Q, t):
        u = self.C.u_from_P(P,self.base(t))
        return u, Q+self.dy(u,t) if self.model=='structure' else Q

    def rhs(self,t,P,Q):
        self.calls += 1
        if self.model=='structure':
            return self.op(t,P,Q)
        # Conventional second-order staggered y finite differences on DLW.
        # P approximates u_y at the midpoint between adjacent u nodes.
        u, v = self.fields(P,Q,t)
        d1, d2 = self.X.d1,self.X.d2
        Pt = -np.diff(d1(.5*u*u+8*u),axis=0)/self.C.h-d2(.5*(v[1:]+v[:-1]))
        vt = -d1((u+8)*v)-d2(self.dy(u,t))+4*d1(u)
        return Pt,vt
