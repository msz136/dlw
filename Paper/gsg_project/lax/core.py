"""
core.py -- exact tau / derivative engine for the DLW (2+1) system and its
y-semidiscretisation, plus the spectral (epsilon-shift) family.

All computations are exact rational arithmetic at generic rational sample
points (a rational function that vanishes at sufficiently many generic
points vanishes identically).

tau_n(j; z)  :  the "spectral tau" obtained from the Gram matrix

        M_ik(n,j) = c_k d_ik + 1/(p_i+q_k) * (-(p_i-a)/(q_k+a))^n * (chi_i chi'_k)^j
                    * exp(xi_i + eta_k)
        xi_i  = p_i x - p_i^2 t + y/(p_i-a)
        eta_k = q_k x + q_k^2 t + y/(q_k+a)

by the RANK-ONE spectral perturbation   M -> M + z^{-1} u v^T   with
        u_i = u_i(z),  v_k = v_k(z)   as specified by the caller.

Because M(n+1) is related to M(n) by an exact similarity (row/column
scalings) plus a rank-one update, the ratio tau_{n+1}(z)/tau_n(z) is a
low-degree rational function of z -- this is the discrete Lax operator.

We use plain sympy expressions (not the monomial-key dict engine of
engine2.py) because the Lax identities involve DIVISION by tau and
derivatives of tau, which the monomial-key representation cannot do.
"""

import random
from itertools import permutations

import sympy as sp

x, y, t = sp.symbols('x y t', real=True)
z = sp.Symbol('z')


class Lattice:
    """DLW Gram tau on the y-lattice, with an optional spectral parameter."""

    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a = sp.nsimplify(a)
        self.h = sp.nsimplify(h)
        self.p = [sp.nsimplify(v) for v in p]
        self.q = [sp.nsimplify(v) for v in q]
        self.c = [sp.Integer(1)] * self.N if c is None else [sp.nsimplify(v) for v in c]
        self.P = [self.p[i] - self.a for i in range(self.N)]
        self.Q = [self.q[k] + self.a for k in range(self.N)]

    # ---------------------------------------------------------------- helpers
    def d(self):
        return self.h / 2

    def lam(self, u):
        dd = self.d()
        return (u + dd) / (u - dd)

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    def rate_x(self, n, m):
        return sum(n[i] * self.p[i] for i in range(self.N)) + \
               sum(m[k] * self.q[k] for k in range(self.N))

    def rate_t(self, n, m):
        return sum(m[k] * self.q[k] ** 2 for k in range(self.N)) - \
               sum(n[i] * self.p[i] ** 2 for i in range(self.N))

    def rate_y(self, n, m, s=None):
        s = self.a if s is None else s
        return sum(n[i] / (self.p[i] - s) for i in range(self.N)) + \
               sum(m[k] / (self.q[k] + s) for k in range(self.N))

    # ------------------------------------------------------------------- tau
    def entry(self, n, j, i, k, eps=0, extra=None):
        """The (i,k) matrix element of the Gram matrix, as a sympy expression
        in x,y,t (exponentials kept symbolic).

        eps  : shift of the spectral parameter,  p_i -> p_i + eps, q_k -> q_k + eps
               (this is the "generator of the discrete flow", see report)
        extra: optional multiplicative factor (for rank-one perturbations)
        """
        a = self.a
        p = self.p[i] + eps
        q = self.q[k] + eps
        P = p - a
        Q = q + a
        coef = sp.Integer(1) / (p + q) * (-P / Q) ** n
        if j:
            coef = coef * self.lam(self.P[i]) ** j * self.lam(self.Q[k]) ** j
        e = coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))
        if extra is not None:
            e = sp.expand(e * extra)
        return e

    def matrix(self, n, j, eps=0, pert=None):
        """Gram matrix M_ik(n,j).  `pert` = (u, v) adds u_i v_k (rank-one)."""
        M = sp.zeros(self.N, self.N)
        for i in range(self.N):
            for k in range(self.N):
                M[i, k] = self.entry(n, j, i, k, eps=eps)
        if pert is not None:
            u, v = pert
            for i in range(self.N):
                for k in range(self.N):
                    M[i, k] = M[i, k] + u[i] * v[k]
        return M

    def tau(self, n, j, eps=0, pert=None):
        return sp.expand(self.matrix(n, j, eps=eps, pert=pert).det())

    # ---------------------------------------------- rank-one spectral family
    def u_default(self, eps=0, power=1):
        """u_i(z) = (p_i + eps - a) * (q-normalised) -- default perturbation.

        Chosen so that M(n+1) = S M(n) S' + rank-one with z-independent
        rank-one data; see report section on the discrete Lax pair.
        """
        raise NotImplementedError
