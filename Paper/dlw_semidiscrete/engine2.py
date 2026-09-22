"""
engine2.py -- INDEPENDENT re-implementation of the exact exponential-monomial
calculus for the DLW Gram tau function.

Written from scratch for the purpose of cross-checking the results in
`gsg_project/` (different code path, different data layout), and for the new
investigations in this folder.

--------------------------------------------------------------------------
Representation
--------------------------------------------------------------------------
An exponential monomial of the tau function has the form

      E = exp( sum_i n_i*xi_i + sum_k m_k*eta_k )

with

      xi_i  = p_i x - p_i^2 t + y/(p_i - s) ,
      eta_k = q_k x + q_k^2 t + y/(q_k + s) ,

where `s` is the ("Baecklund") parameter carried by the tau function.
Because xi and eta are additive, E depends only on the ROW multiplicity
vector n and the COLUMN multiplicity vector m:

      exp(xi_0+eta_0) * exp(xi_1+eta_1) = exp(xi_0+eta_1) * exp(xi_1+eta_0)
      --> both are keyed by n = (1,1), m = (1,1).

So a linear combination of such monomials is a dict { (n, m) : coefficient }.

Differentiation:
      d_x (n,m) = ( sum_i n_i p_i + sum_k m_k q_k )                * (n,m)
      d_t (n,m) = ( sum_k m_k q_k^2 - sum_i n_i p_i^2 )            * (n,m)
      d_y (n,m) = ( sum_i n_i/(p_i-s) + sum_k m_k/(q_k+s) )        * (n,m)

Bilinear operators (Hirota):
      D_x^a D_y^b D_t^c F . G
        = sum_{p<=a,q<=b,r<=c} (-1)^{p+q+r} C(a,p)C(b,q)C(c,r)
              (d_x^{a-p} d_y^{b-q} d_t^{c-r} F) * (d_x^p d_y^q d_t^r G)

A residual is identically zero  <=>  its dict is empty.
"""

import random
from itertools import permutations
from math import comb

import sympy as sp


# --------------------------------------------------------------------- keys
def k_add(k1, k2):
    return (tuple(u + v for u, v in zip(k1[0], k2[0])),
            tuple(u + v for u, v in zip(k1[1], k2[1])))


def k_zero(N):
    return ((0,) * N, (0,) * N)


def k_unit(N, i, j):
    n = [0] * N
    m = [0] * N
    n[i] = 1
    m[j] = 1
    return (tuple(n), tuple(m))


# ---------------------------------------------------------------- arithmetic
def eadd(*ds):
    out = {}
    for d in ds:
        for k, v in d.items():
            if v == 0:
                continue
            nv = sp.expand(out[k] + v) if k in out else sp.expand(v)
            if nv == 0:
                out.pop(k, None)
            else:
                out[k] = nv
    return out


def escale(d, s):
    if s == 0:
        return {}
    out = {}
    for k, v in d.items():
        nv = sp.expand(v * s)
        if nv != 0:
            out[k] = nv
    return out


def emul(d1, d2):
    out = {}
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            k = k_add(k1, k2)
            nv = sp.expand(v1 * v2)
            nv = sp.expand(out[k] + nv) if k in out else nv
            if nv == 0:
                out.pop(k, None)
            else:
                out[k] = nv
    return out


# ------------------------------------------------------------------- model
class Model:
    """DLW Gram tau with an optional lattice in y.

    Parameters
    ----------
    N : int          size of the Gram determinant
    a : sympy expr   the DLW parameter
    h : sympy expr or None      lattice spacing
    c : list         the constants c_k (default all 1)
    """

    def __init__(self, N, a=None, h=None, c=None):
        self.N = N
        self.a = sp.Symbol('a', real=True) if a is None else a
        self.h = h
        self.c = list(c) if c is not None else [sp.Integer(1)] * N
        self.p = [sp.Symbol('p%d' % (i + 1)) for i in range(N)]
        self.q = [sp.Symbol('q%d' % (i + 1)) for i in range(N)]
        self._subs = {}

    # ------------------------------------------------------------- helpers
    def _sym(self, v):
        return v.subs(self._subs) if self._subs else v

    def subs_point(self, pt):
        self._subs = dict(pt)
        self.a = self._sym(self.a)
        if self.h is not None:
            self.h = self._sym(self.h)
        self.p = [self._sym(v) for v in self.p]
        self.q = [self._sym(v) for v in self.q]
        self.c = [self._sym(v) for v in self.c]
        return self

    def lam(self, z, h=None):
        """lattice exponential  lambda(z) = (z + h/2)/(z - h/2)  ~ e^{h/z}."""
        h = self.h if h is None else h
        d = h / 2
        return (z + d) / (z - d)

    # ----------------------------------------------------------------- tau
    def tau(self, n, j=0, s=None, mu=None, N=None):
        """tau_n at lattice site j.

        s  : parameter in the OFF-DIAGONAL coefficient  (-(p-s)/(q+s))^n
             and in the exponent denominators 1/(p-s), 1/(q+s)
        mu : parameter used to build the lattice multiplier (defaults to s);
             site j multiplies the (i,k) entry by (lam(p_i-mu) lam(q_k+mu))^j.

        mu != s allows the "hybrid" objects used in gsg_project.
        """
        N = self.N if N is None else N
        a = self.a
        s = a if s is None else s
        mu = s if mu is None else mu
        ent = {}
        row, col = [], []
        for i in range(N):
            Pi = self.p[i] - mu
            row.append(self.lam(Pi) if self.h is not None else sp.Integer(1))
        for k in range(N):
            Qk = self.q[k] + mu
            col.append(self.lam(Qk) if self.h is not None else sp.Integer(1))

        for i in range(N):
            for k in range(N):
                Pi = self.p[i] - s
                Qk = self.q[k] + s
                coef = (-Pi / Qk) ** n / (self.p[i] + self.q[k])
                if j:
                    coef *= (row[i] * col[k]) ** j
                e = {k_unit(N, i, k): sp.expand(coef)}
                if i == k:
                    e = eadd(e, {k_zero(N): sp.expand(self.c[k])})
                ent[(i, k)] = e

        total = {}
        zero = k_zero(N)
        for perm in permutations(range(N)):
            sign = 1
            pl = list(perm)
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = {zero: sp.Integer(sign)}
            for i in range(N):
                term = emul(term, ent[(i, perm[i])])
            total = eadd(total, term)
        return total

    # -------------------------------------------------------------- calculus
    def rate(self, key, var, s=None):
        N = self.N
        n, m = key
        s = self.a if s is None else s
        if var == 'x':
            return sum(ni * self.p[i] for i, ni in enumerate(n)) + \
                   sum(mk * self.q[k] for k, mk in enumerate(m))
        if var == 't':
            return sum(mk * self.q[k] ** 2 for k, mk in enumerate(m)) - \
                   sum(ni * self.p[i] ** 2 for i, ni in enumerate(n))
        if var == 'y':
            return sum(ni / (self.p[i] - s) for i, ni in enumerate(n)) + \
                   sum(mk / (self.q[k] + s) for k, mk in enumerate(m))
        raise ValueError(var)

    def der(self, d, var, s=None):
        out = {}
        for k, v in d.items():
            r = self.rate(k, var, s)
            if r != 0:
                out[k] = sp.expand(out.get(k, 0) + v * r)
        return dict((k, v) for k, v in out.items() if v != 0)

    def dern(self, F, var, m, s=None):
        for _ in range(m):
            F = self.der(F, var, s)
        return F

    def bilin(self, F, G, ax=0, ay=0, at=0, s=None):
        out = {}
        for pp in range(ax + 1):
            for qq in range(ay + 1):
                for rr in range(at + 1):
                    co = (-1) ** (pp + qq + rr) * comb(ax, pp) * comb(ay, qq) * comb(at, rr)
                    A = self.dern(self.dern(self.dern(F, 'x', ax - pp, s), 'y', ay - qq, s), 't', at - rr, s)
                    B = self.dern(self.dern(self.dern(G, 'x', pp, s), 'y', qq, s), 't', rr, s)
                    out = eadd(out, escale(emul(A, B), co))
        return out

    def B(self, F, G, s=None):
        """B_s F.G = (D_x^2 + D_t + 2 s D_x) F.G"""
        s = self.a if s is None else s
        return eadd(self.bilin(F, G, ax=2),
                    self.bilin(F, G, at=1),
                    escale(self.bilin(F, G, ax=1), 2 * s))


# ------------------------------------------------------------------ sampling
def rand_point(m, seed=0, lo=2, hi=41):
    rng = random.Random(seed)
    syms = list(m.p) + list(m.q) + [m.a]
    if m.h is not None:
        syms = syms + [m.h]
    pt, used = {}, set()
    for s in syms:
        while True:
            v = sp.Rational(rng.randint(lo, hi), rng.randint(lo, 7))
            if v not in used:
                used.add(v)
                pt[s] = v
                break
    while any(pt[m.a] == pt[p] for p in m.p) or any(pt[m.a] == -pt[q] for q in m.q):
        pt[m.a] += sp.Rational(1, 3)
    return pt


def is_regular(m, kind):
    if any(v == 0 for v in [m.p[i] - m.a for i in range(m.N)]):
        return False
    if any(v == 0 for v in [m.q[k] + m.a for k in range(m.N)]):
        return False
    if any(m.p[i] + m.q[k] == 0 for i in range(m.N) for k in range(m.N)):
        return False
    if m.h is not None and kind == 'sym':
        d = m.h / 2
        vals = [m.p[i] - m.a for i in range(m.N)] + [m.q[k] + m.a for k in range(m.N)]
        if any(v == d or v == -d for v in vals):
            return False
    return True


def vanishes(build, N, trials=3, h=None, seed0=11, max_try=60):
    """True/False: does build(Model) vanish at `trials` generic exact points?"""
    good, att = 0, 0
    while good < trials and att < max_try:
        att += 1
        m = Model(N, h=h)
        m.subs_point(rand_point(m, seed=seed0 + 101 * att))
        if not is_regular(m, 'sym'):
            continue
        d = build(m)
        if any(v.is_finite is False for v in d.values()):
            continue
        good += 1
        if len(d) != 0:
            return False, (m, d)
    if good == 0:
        raise RuntimeError('no regular point')
    return True, None
