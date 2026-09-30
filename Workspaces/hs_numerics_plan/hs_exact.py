"""One- and two-soliton reference fields in a common tau gauge.

The formulas use positive normalized tau coefficients and shifted phase constants.
Node values of u and x use k=0,...,M; edge density uses k=1,...,M.
"""
from dataclasses import dataclass
import numpy as np
from scipy.special import logsumexp


@dataclass(frozen=True)
class Soliton:
    p: tuple[float, ...]
    c: float = 1.0
    phase: tuple[float, ...] = ()
    shift: float = 0.0

    def __post_init__(self):
        if len(self.p) not in (1, 2):
            raise ValueError("The explicit normalized tau implementation supports N=1 or N=2")
        if self.phase and len(self.phase) != len(self.p):
            raise ValueError("There must be one phase per soliton")
        if any(r <= 1/self.c or abs(r-2/self.c) < 1e-12 for r in self.p):
            raise ValueError("Use smooth nondegenerate p > 1/c and p != 2/c")
        if len(self.p) == 2 and not self.interaction > 0:
            raise ValueError("The selected two-soliton tau must have positive interaction")

    @property
    def q(self):
        p = np.asarray(self.p)
        return p/(self.c*p-1)

    @property
    def omega(self):
        return 1/np.asarray(self.p)-1/self.q

    @property
    def beta(self):
        return np.asarray(self.p)-self.q

    @property
    def interaction(self):
        if len(self.p) == 1:
            return 1.0
        p, q = np.asarray(self.p), self.q
        return float((p[1]-p[0])*(q[1]-q[0])/((q[1]-p[0])*(p[1]-q[0])))

    def sigma(self, a):
        p, q = np.asarray(self.p), self.q
        if a <= 0 or np.max(a*np.r_[p,q]) >= 1:
            raise ValueError("Require a > 0 and a*max(p,q) < 1")
        return np.log1p(-a*q)-np.log1p(-a*p)

    def _weights(self, coordinate, t, lattice_a=None):
        coordinate = np.asarray(coordinate, dtype=float)
        phase = np.asarray(self.phase if self.phase else (0.,)*len(self.p))
        beta = self.beta if lattice_a is None else self.sigma(lattice_a)
        theta = beta[:,None]*coordinate.reshape(1,-1)+self.omega[:,None]*t+phase[:,None]
        if len(self.p) == 1:
            logs = np.vstack([np.zeros(coordinate.size), theta[0]])
            om = np.array([0.,self.omega[0]])
            spatial = np.array([0.,beta[0]])
        else:
            logs = np.vstack([np.zeros(coordinate.size),theta[0],theta[1],
                              np.log(self.interaction)+theta[0]+theta[1]])
            om = np.array([0.,self.omega[0],self.omega[1],sum(self.omega)])
            spatial = np.array([0.,beta[0],beta[1],sum(beta)])
        weights = np.exp(logs-logsumexp(logs,axis=0))
        return weights, om[:,None], spatial[:,None]

    @staticmethod
    def _fields(coordinate, weights, om, spatial, shift):
        omt = np.sum(weights*om,axis=0)
        betat = np.sum(weights*spatial,axis=0)
        dom = om-omt
        dbeta = spatial-betat
        u = np.sum(weights*dom**2,axis=0)
        lx = np.sum(weights*dom*dbeta,axis=0)
        x = coordinate-lx*0-omt+shift
        rho = 1/(1-lx)
        return u,x,rho

    def lattice(self, k, a, t):
        k=np.asarray(k,dtype=float)
        weights,om,spatial=self._weights(k,t,a)
        u,x0,_=self._fields(k*a,weights,om,spatial,self.shift)
        # _fields uses the physical base coordinate supplied by the caller.
        return u,x0

    def lattice_state(self, k, a, t):
        u,x=self.lattice(k,a,t)
        d=np.diff(x)
        if np.any(d <= 0):
            raise ValueError("Exact lattice has a nonpositive edge")
        return {'u':u,'x':x,'v':np.diff(u),'d':d,'rho':a/d}

    def continuous_X(self, X, t):
        X=np.asarray(X,dtype=float)
        weights,om,spatial=self._weights(X,t)
        return self._fields(X,weights,om,spatial,self.shift)

    def continuous_x(self, x, t, iterations=12):
        x=np.asarray(x,dtype=float)
        X=x-self.shift+np.mean(self.omega)
        for _ in range(iterations):
            u,physical,rho=self.continuous_X(X,t)
            X=X-(physical-x)*rho
        u,physical,rho=self.continuous_X(X,t)
        if np.max(np.abs(physical-x)) > 2e-10:
            raise RuntimeError("Continuous hodograph inversion did not converge")
        return u,rho,X

    def continuous_density_cell_mean(self, left, right, t):
        _,_,XL=self.continuous_x(left,t)
        _,_,XR=self.continuous_x(right,t)
        return (XR-XL)/(np.asarray(right)-np.asarray(left))
