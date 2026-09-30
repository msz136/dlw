# -*- coding: utf-8 -*-
"""
dlwcommon.py -- shared exact engine for the DLW semi-discrete nonlinear layer.

Conventions (fixed once and for all; see the workspace-root index.html,
C:/Users/msz/学术内容/index.html):

    d = h/2,   lam(z) = (z+d)/(z-d)  ~  e^{h/z}
    G_j = tau_0(j)                     (lattice site j)
    F_j = tau_1(j ; s = a-d)           (staggered;  F_j = tau_1(j+1 ; a+d) by (dagger))
    P_i = p_i - a,  Q_k = q_k + a

    tau_n(j; s) = det[ c_k delta_ik
                       + (1/(p_i+q_k)) (-(p_i-s)/(q_k+s))^n
                         * ( lam(p_i-a) lam(q_k+a) )^j
                         * exp( xi_i + eta_k ) ]
    xi_i  = p_i x - p_i^2 t ,   eta_k = q_k x + q_k^2 t
    (the y-dependence is carried entirely by the lattice index j)

Continuous reference tau (no lattice, genuine y):

    tau^c_n(y; s) = det[ c_k delta_ik
                         + (1/(p_i+q_k)) (-(p_i-s)/(q_k+s))^n
                           * exp( xi_i + eta_k + y(1/(p_i-a) + 1/(q_k+a)) ) ]

All numbers are exact sympy rationals; every zero test is an exact rational test.
"""

import itertools
import sympy as sp


# --------------------------------------------------------------------------
#  generic Gram determinant over an explicitly given entry function
# --------------------------------------------------------------------------
def _det_perm(N, entry_fn):
    tot = 0
    for perm in itertools.permutations(range(N)):
        sign = 1
        pl = list(perm)
        for ii in range(N):
            for jj in range(ii + 1, N):
                if pl[ii] > pl[jj]:
                    sign = -sign
        term = sp.Integer(sign)
        for i in range(N):
            term = term * entry_fn(i, perm[i])
        tot = tot + term
    return tot


class Base:
    def __init__(self, N, vals, h, a):
        self.N = N
        self.h = sp.nsimplify(h)
        self.d = self.h / 2
        self.a = sp.nsimplify(a)
        self.p = [sp.nsimplify(vals['p%d' % (i + 1)]) for i in range(N)]
        self.q = [sp.nsimplify(vals['q%d' % (k + 1)]) for k in range(N)]
        self.c = [sp.Integer(1)] * N
        self.x, self.t = sp.symbols('x t', real=True)

    def lam(self, z):
        return (z + self.d) / (z - self.d)

    # physical potentials ------------------------------------------------
    def alpha(self, j):
        """alpha_j = ln F_j"""
        return sp.log(self.F(j))

    def beta(self, j):
        """beta_j = ln G_j"""
        return sp.log(self.G(j))

    def theta(self, j):
        """theta_j = ln(F_j/G_j)"""
        return self.alpha(j) - self.beta(j)

    def Psi(self, j):
        """Psi_j = ln(F_j G_j)"""
        return self.alpha(j) + self.beta(j)

    def Theta(self, j):
        """Theta_j = ln(F_j/G_{j+1})"""
        return self.alpha(j) - self.beta(j + 1)

    def Phi(self, j):
        """Phi_j = ln(F_j G_{j+1})"""
        return self.alpha(j) + self.beta(j + 1)

    # physics variables --------------------------------------------------
    def u(self, j):
        """u_j = 2 (ln F_j/G_j)_x"""
        return 2 * sp.diff(self.theta(j), self.x)

    # residuals (N1)(N2) -------------------------------------------------
    def res_N1(self, j):
        return sp.diff(self.Psi(j), self.x, 2) + sp.diff(self.theta(j), self.x) ** 2 \
               + sp.diff(self.theta(j), self.t) + 2 * (self.a - self.d) * sp.diff(self.theta(j), self.x)

    def res_N2(self, j):
        return sp.diff(self.Phi(j), self.x, 2) + sp.diff(self.Theta(j), self.x) ** 2 \
               + sp.diff(self.Theta(j), self.t) + 2 * (self.a + self.d) * sp.diff(self.Theta(j), self.x)

    def bilinear_Eplus(self, j):
        """(7)_h = B_{a-d} F_j . G_j     (must vanish identically)"""
        return self.B(self.F(j), self.G(j), self.a - self.d)

    def bilinear_Eminus(self, j):
        """(6)_h = B_{a+d} F_j . G_{j+1}  (must vanish identically)"""
        return self.B(self.F(j), self.G(j + 1), self.a + self.d)

    def B(self, F, G, s):
        """B_s F.G = (D_x^2 + D_t + 2 s D_x) F.G  (Hirota)"""
        Dx2 = sp.diff(F, self.x, 2) * G - 2 * sp.diff(F, self.x) * sp.diff(G, self.x) + F * sp.diff(G, self.x, 2)
        Dt = sp.diff(F, self.t) * G - F * sp.diff(G, self.t)
        Dx = sp.diff(F, self.x) * G - F * sp.diff(G, self.x)
        return sp.expand(Dx2 + Dt + 2 * s * Dx)


class Lattice(Base):
    """Lattice (semi-discrete) tau: y is replaced by the index j."""

    def entry(self, n, i, k, j, s):
        p, q, a = self.p[i], self.q[k], self.a
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        if j:
            coef = coef * (self.lam(p - a) * self.lam(q + a)) ** j
        expo = (p * self.x - p ** 2 * self.t) + (q * self.x + q ** 2 * self.t)
        m = coef * sp.exp(expo)
        if i == k:
            m = m + self.c[k]
        return sp.expand(m)

    def tau(self, n, j, s):
        return sp.expand(_det_perm(self.N, lambda i, k: self.entry(n, i, k, j, s)))

    def F(self, j):
        return self.tau(1, j, self.a - self.d)

    def G(self, j):
        return self.tau(0, j, self.a)

    # ---- candidate v_j definitions (lattice differences of ln(FG)) -----
    def v_fwd(self, j):
        """v_j = (1/h) [ ln(F_{j+1}G_{j+1}) - ln(F_j G_j) ]_x"""
        return sp.diff(self.Psi(j + 1) - self.Psi(j), self.x) / self.h

    def v_bwd(self, j):
        """v_j = (1/h) [ ln(F_j G_j) - ln(F_{j-1}G_{j-1}) ]_x"""
        return sp.diff(self.Psi(j) - self.Psi(j - 1), self.x) / self.h

    def v_mid(self, j):
        """v_j = (1/(2h)) [ ln(F_{j+1}G_{j+1}) - ln(F_{j-1}G_{j-1}) ]_x"""
        return sp.diff(self.Psi(j + 1) - self.Psi(j - 1), self.x) / (2 * self.h)

    def v_cross(self, j):
        """v_j = (1/(2h)) [ ln(F_j G_{j+1}) + ln(F_j G_j) - ln(F_{j-1}G_j) - ln(F_{j-1}G_{j-1}) ]_x
             = (1/(2h)) [ (Phi_j - Phi_{j-1}) + (Psi_j - Psi_{j-1}) ]_x
        (uses both the vertex product and the cross product)"""
        s1 = self.Phi(j) - self.Phi(j - 1)
        s2 = self.Psi(j) - self.Psi(j - 1)
        return sp.diff(s1 + s2, self.x) / (2 * self.h)


class Cont(Base):
    """Continuous tau: genuine y coordinate."""

    def entry(self, n, i, k, y, s):
        p, q, a = self.p[i], self.q[k], self.a
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        expo = (p * self.x - p ** 2 * self.t) + (q * self.x + q ** 2 * self.t) \
               + y * (1 / (p - a) + 1 / (q + a))
        m = coef * sp.exp(expo)
        if i == k:
            m = m + self.c[k]
        return sp.expand(m)

    def tau(self, n, y, s):
        return sp.expand(_det_perm(self.N, lambda i, k: self.entry(n, i, k, y, s)))

    def F(self, y):
        return self.tau(1, y, self.a)

    def G(self, y):
        return self.tau(0, y, self.a)

    def theta(self, y):
        return sp.log(self.F(y) / self.G(y))

    def Psi(self, y):
        return sp.log(self.F(y) * self.G(y))

    def u_cont(self, y):
        return 2 * sp.diff(self.theta(y), self.x)

    def v_cont(self, y):
        return 2 * sp.diff(self.Psi(y), self.x, y)

    def res_N1_cont(self, y):
        th, Ps = self.theta(y), self.Psi(y)
        return sp.diff(Ps, self.x, 2) + sp.diff(th, self.x) ** 2 \
               + sp.diff(th, self.t) + 2 * self.a * sp.diff(th, self.x)

    def res_N2_cont(self, y):
        """continuous (6)|_{lambda=-2}:  Psi_{xxy} + 2 theta_x theta_xy + theta_{ty}
           + 2a theta_{xy} + 2 u_x = 0 ... (derived, checked numerically)"""
        raise NotImplementedError


# --------------------------------------------------------------------------
#  helpers
# --------------------------------------------------------------------------
def at(expr, M, x0, t0):
    return sp.simplify(expr.subs({M.x: x0, M.t: t0}))


def report_zero(name, expr, M, x0, t0):
    v = at(expr, M, x0, t0)
    ok = (v == 0)
    print("   %-22s : %s" % (name, "EXACT ZERO" if ok else "resid = %s" % v))
    return ok


DEFAULT = dict(p1=sp.Rational(5, 3), q1=sp.Rational(7, 4),
               p2=sp.Rational(3, 2), q2=sp.Rational(9, 5))


if __name__ == '__main__':
    print("smoke test")
    M = Lattice(1, {'p1': DEFAULT['p1'], 'q1': DEFAULT['q1']}, sp.Rational(1, 4), sp.Rational(3, 2))
    x0, t0 = sp.Rational(1, 5), sp.Rational(2, 7)
    for j in [0, 1, 2]:
        print("j=%d  (N1)=%s  (N2)=%s  (7)_h=%s  (6)_h=%s" % (
            j,
            at(M.res_N1(j), M, x0, t0),
            at(M.res_N2(j), M, x0, t0),
            at(M.bilinear_Eplus(j), M, x0, t0),
            at(M.bilinear_Eminus(j), M, x0, t0)))
