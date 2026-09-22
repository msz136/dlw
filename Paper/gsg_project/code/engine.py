"""
Exact exponential-monomial engine for Hirota bilinear identities on the DLW Gram tau.

Representation
--------------
The tau is built from exponentials  E_ik = exp(xi_i + eta_k)  with
    xi_i  = p_i x - p_i^2 t + y/P_i ,   P_i = p_i - a
    eta_k = q_k x + q_k^2 t + y/Q_k ,   Q_k = q_k + a

KEY POINT.  A product of such exponentials depends only on HOW MANY TIMES each
ROW index i and each COLUMN index k occur, not on how they were paired:
    E_00 E_11 = E_01 E_10 = exp(xi_0 + xi_1 + eta_0 + eta_1) .
So a monomial is represented by
    key = (n, m)   with n = (n_0,...,n_{N-1}) row multiplicities,
                        m = (m_0,...,m_{N-1}) column multiplicities.
Every operation respects this:

    d_x key = (sum_i n_i p_i + sum_k m_k q_k)        * key
    d_t key = (sum_k m_k q_k^2 - sum_i n_i p_i^2)    * key
    d_y key = (sum_i n_i/P_i + sum_k m_k/Q_k)        * key
    chi-product(key) = prod_i row_i^{n_i} * prod_k col_k^{m_k}

Bilinear operators use the standard expansion
    D_x^ax D_y^ay D_t^at F.G
      = sum (-1)^{p+q+r} C(ax,p)C(ay,q)C(at,r)
          (d_x^{ax-p} d_y^{ay-q} d_t^{at-r} F) (d_x^p d_y^q d_t^r G)

A residual is zero  <=>  its dict is empty.
"""
import random
from itertools import permutations
from math import comb

import sympy as sp


# --------------------------------------------------------------------------- #
#  keys
# --------------------------------------------------------------------------- #
def _add_keys(k1, k2):
    n1, m1 = k1
    n2, m2 = k2
    return (tuple(a + b for a, b in zip(n1, n2)),
            tuple(a + b for a, b in zip(m1, m2)))


def _zero_key(N):
    return ((0,) * N, (0,) * N)


def _unit_key(N, i, k):
    n = [0] * N
    m = [0] * N
    n[i] = 1
    m[k] = 1
    return (tuple(n), tuple(m))


# --------------------------------------------------------------------------- #
#  arithmetic
# --------------------------------------------------------------------------- #
def e_add(*ds):
    out = {}
    for d in ds:
        for k, v in d.items():
            if v == 0:
                continue
            if k in out:
                nv = sp.expand(out[k] + v)
                if nv == 0:
                    del out[k]
                else:
                    out[k] = nv
            else:
                out[k] = sp.expand(v)
    return out


def e_scale(d, s):
    if s == 0:
        return {}
    out = {}
    for k, v in d.items():
        nv = sp.expand(v * s)
        if nv != 0:
            out[k] = nv
    return out


def e_mul(d1, d2):
    out = {}
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            k = _add_keys(k1, k2)
            nv = sp.expand(v1 * v2)
            if k in out:
                nv = sp.expand(out[k] + nv)
            if nv == 0:
                out.pop(k, None)
            else:
                out[k] = nv
    return out


# --------------------------------------------------------------------------- #
#  the model
# --------------------------------------------------------------------------- #
class DLW:
    """
    Gram-type tau for the DLW bilinear system, with an optional lattice in y.

      kind 'none'   continuum          (no lattice)
      kind 'sym'    chi = (P+d)/(P-d),  d = h/2        central / staggered
      kind 'exp'    chi = P/(P-h)                      literal GSG (1-h/P)^{-1}
      kind 'expneg' chi = (P+h)/P
    """

    def __init__(self, N, a=None, h=None, c=None, kind='none', point=None):
        self.N = N
        self.a = a if a is not None else sp.Symbol('a', real=True)
        self.h = h
        self.kind = kind
        self.p = [sp.Symbol(f'p{i+1}') for i in range(N)]
        self.q = [sp.Symbol(f'q{k+1}') for k in range(N)]
        self.c = list(c) if c is not None else [sp.Integer(1)] * N
        self.P = [self.p[i] - self.a for i in range(N)]
        self.Q = [self.q[k] + self.a for k in range(N)]
        self.point = point
        self._xx = None

    # ---------------------------------------------------------------- point
    def set_point(self, pt):
        self.point = dict(pt)
        self.p = [v.subs(pt) for v in self.p]
        self.q = [v.subs(pt) for v in self.q]
        self.a = self.a.subs(pt)
        if self.h is not None:
            self.h = self.h.subs(pt)
        self.P = [v.subs(pt) for v in self.P]
        self.Q = [v.subs(pt) for v in self.Q]
        self._xx = None
        return self

    # ---------------------------------------------------------------- rates
    def rates(self):
        if self._xx is None:
            self._xx = (
                [self.p[i] for i in range(self.N)],
                [-self.p[i] ** 2 for i in range(self.N)],
                [1 / self.P[i] for i in range(self.N)],
                [self.q[k] for k in range(self.N)],
                [self.q[k] ** 2 for k in range(self.N)],
                [1 / self.Q[k] for k in range(self.N)],
            )
        return self._xx

    def _rate(self, key, var):
        px, ptt, py, qx, qt, qy = self.rates()
        n, m = key
        if var == 'x':
            return sum(a * b for a, b in zip(n, px)) + sum(a * b for a, b in zip(m, qx))
        if var == 't':
            return sum(a * b for a, b in zip(n, ptt)) + sum(a * b for a, b in zip(m, qt))
        if var == 'y':
            return sum(a * b for a, b in zip(n, py)) + sum(a * b for a, b in zip(m, qy))
        raise ValueError(var)

    def chi_factors(self):
        h = self.h
        if self.kind == 'none':
            row = [sp.Integer(1)] * self.N
            col = [sp.Integer(1)] * self.N
        elif self.kind == 'sym':
            d = h / 2
            row = [(self.P[i] + d) / (self.P[i] - d) for i in range(self.N)]
            col = [(self.Q[k] + d) / (self.Q[k] - d) for k in range(self.N)]
        elif self.kind == 'exp':
            row = [self.P[i] / (self.P[i] - h) for i in range(self.N)]
            col = [self.Q[k] / (self.Q[k] - h) for k in range(self.N)]
        elif self.kind == 'expx':
            # GSG device in x:  e^{p x} -> (1 - h p)^{-j}
            row = [1 / (1 - h * self.p[i]) for i in range(self.N)]
            col = [1 / (1 - h * self.q[k]) for k in range(self.N)]
        elif self.kind == 'expx2':
            # rank-one-preserving GSG device in x for the Gram tau:
            #   rows  e^{p x} -> (1 - h p)^{-j}
            #   cols  e^{q x} -> (1 + h q)^{ j}
            row = [1 / (1 - h * self.p[i]) for i in range(self.N)]
            col = [(1 + h * self.q[k]) for k in range(self.N)]
        elif self.kind == 'expneg':
            row = [(self.P[i] + h) / self.P[i] for i in range(self.N)]
            col = [(self.Q[k] + h) / self.Q[k] for k in range(self.N)]
        else:
            raise ValueError(self.kind)
        return row, col

    def _chi_pow(self, key, s):
        row, col = self.chi_factors()
        n, m = key
        v = sp.Integer(1)
        for i, ni in enumerate(n):
            if ni:
                v *= row[i] ** (s * ni)
        for k, mk in enumerate(m):
            if mk:
                v *= col[k] ** (s * mk)
        return v

    # ---------------------------------------------------------------- tau
    def tau(self, n, jshift=0, a_shift=0):
        """
        tau_n at lattice site j+jshift.  `a_shift` shifts a -> a + a_shift in the
        P_i, Q_k of the OFF-DIAGONAL entries only.
        """
        N = self.N
        a_ = self.a + a_shift
        P = [self.p[i] - a_ for i in range(N)]
        Q = [self.q[k] + a_ for k in range(N)]
        row, col = self.chi_factors()
        ent = {}
        for i in range(N):
            for k in range(N):
                coeff = (-P[i] / Q[k]) ** n / (self.p[i] + self.q[k])
                if self.h is not None and self.kind != 'none':
                    coeff = coeff * (row[i] * col[k]) ** jshift
                e = {_unit_key(N, i, k): sp.expand(coeff)}
                if i == k:
                    e = e_add(e, {_zero_key(N): sp.expand(self.c[k])})
                ent[(i, k)] = e
        total = {}
        zero = _zero_key(N)
        for perm in permutations(range(N)):
            pl = list(perm)
            sign = 1
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = {zero: sp.Integer(sign)}
            for i in range(N):
                term = e_mul(term, ent[(i, perm[i])])
            total = e_add(total, term)
        return total

    # ---------------------------------------------------------------- calculus
    def der(self, d, var):
        out = {}
        for key, coeff in d.items():
            r = self._rate(key, var)
            if r != 0:
                out[key] = sp.expand(out.get(key, 0) + coeff * r)
        return {k: v for k, v in out.items() if v != 0}

    def dern(self, F, var, k):
        for _ in range(k):
            F = self.der(F, var)
        return F

    def shift(self, d, s):
        if s == 0:
            return dict(d)
        out = {}
        for key, coeff in d.items():
            nv = sp.expand(coeff * self._chi_pow(key, s))
            if nv != 0:
                out[key] = nv
        return out

    # ---------------------------------------------------------------- bilinear
    def bilin(self, F, G, ax=0, ay=0, at=0):
        out = {}
        for p in range(ax + 1):
            for q in range(ay + 1):
                for r in range(at + 1):
                    coef = (-1) ** (p + q + r) * comb(ax, p) * comb(ay, q) * comb(at, r)
                    A = self.dern(self.dern(self.dern(F, 'x', ax - p), 'y', ay - q), 't', at - r)
                    B = self.dern(self.dern(self.dern(G, 'x', p), 'y', q), 't', r)
                    out = e_add(out, e_scale(e_mul(A, B), coef))
        return out

    def Dx(self, F, G, var='x'):
        return self.bilin(F, G, **{'x': dict(ax=1), 'y': dict(ay=1), 't': dict(at=1)}[var])

    def B(self, F, G, s=None):
        """B_s F.G = (D_x^2 + D_t + 2 s D_x) F.G"""
        s = self.a if s is None else s
        return e_add(self.bilin(F, G, ax=2), self.bilin(F, G, at=1),
                     e_scale(self.bilin(F, G, ax=1), 2 * s))

    def DyB(self, F, G, s=None):
        """D_y B_s F.G"""
        s = self.a if s is None else s
        return e_add(self.bilin(F, G, ax=2, ay=1), self.bilin(F, G, at=1, ay=1),
                     e_scale(self.bilin(F, G, ax=1, ay=1), 2 * s))

    def Dy(self, F, G):
        return self.bilin(F, G, ay=1)

    # ---------------------------------------------------------------- representation
    def to_expr(self, d, x, y, t):
        """Evaluate a residual dict as an explicit sympy expression (for display/tests)."""
        tot = 0
        for key, coef in d.items():
            n, m = key
            term = coef
            for i, ni in enumerate(n):
                if ni:
                    xi = self.p[i] * x - self.p[i] ** 2 * t + y / self.P[i]
                    term *= sp.exp(xi) ** ni
            for k, mk in enumerate(m):
                if mk:
                    eta = self.q[k] * x + self.q[k] ** 2 * t + y / self.Q[k]
                    term *= sp.exp(eta) ** mk
            tot += term
        return sp.expand(tot)


# --------------------------------------------------------------------------- #
#  helpers
# --------------------------------------------------------------------------- #
def random_point(model, seed=0, lo=2, hi=41):
    rng = random.Random(seed)
    syms = list(model.p) + list(model.q) + [model.a]
    if model.h is not None:
        syms = syms + [model.h]
    pt, used = {}, set()
    for s in syms:
        while True:
            v = sp.Rational(rng.randint(lo, hi), rng.randint(lo, 7))
            if v not in used:
                used.add(v)
                pt[s] = v
                break
    tries = 0
    while any(pt[model.a] == pt[p] for p in model.p) or \
          any(pt[model.a] == -pt[q] for q in model.q):
        tries += 1
        pt[model.a] += sp.Rational(1, 3 + tries)
    return pt


def point_is_regular(model):
    for v in list(model.P) + list(model.Q):
        if v == 0:
            return False
    for i in range(model.N):
        for k in range(model.N):
            if model.p[i] + model.q[k] == 0:
                return False
    if model.h is not None and model.kind == 'sym':
        d = model.h / 2
        for v in list(model.P) + list(model.Q):
            if v - d == 0 or v + d == 0:
                return False
    if model.h is not None and model.kind == 'exp':
        for v in list(model.P) + list(model.Q):
            if v - model.h == 0:
                return False
    if model.h is not None and model.kind in ('expx', 'expx2'):
        for v in list(model.p) + list(model.q):
            if 1 - model.h * v == 0 or 1 + model.h * v == 0:
                return False
    return True


def zero_at_points(build, N, trials=4, seed0=1, **kw):
    """(ok, detail): does build(model) vanish at `trials` generic exact points?"""
    good, attempts = 0, 0
    while good < trials and attempts < 40:
        attempts += 1
        m = DLW(N, **kw)
        m.set_point(random_point(m, seed=seed0 + 97 * attempts))
        if not point_is_regular(m):
            continue
        d = build(m)
        if any(v.is_finite is False for v in d.values()):
            continue
        good += 1
        if len(d) != 0:
            return False, (m.point, d)
    if good == 0:
        raise RuntimeError("no regular sample point found")
    return True, None
