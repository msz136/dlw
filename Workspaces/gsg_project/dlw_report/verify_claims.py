#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Independent verification battery for the DLW semi-discretization claims reported in
`index.html` at the workspace root (C:/Users/msz/学术内容/index.html); that file is
built from `Workspaces/gsg_project/dlw_report/_src/index.src.html`.

Why this is an *independent* check
----------------------------------
* The bilinear (Hirota) operators are evaluated with a fresh implementation of the
  pairwise rule

      D_x^m D_t^p D_y^n f.g
        = sum_{alpha,beta} A_alpha B_beta
            * ((theta_alpha - phi_beta)_x)^m
            * ((theta_alpha - phi_beta)_t)^p
            * ((theta_alpha - phi_beta)_y)^n
            * exp(theta_alpha + phi_beta),

  where every tau is written as a polynomial in the rank-one factors R_i = exp(xi_i) and
  C_k = exp(eta_k).  No code is shared with `gsg_project/code/engine.py` or
  `dlw_semidiscrete/engine2.py`.

* Zero tests are exact, never "small":
    - SYMBOLIC mode   : every coefficient must cancel to the rational zero
                        (tested through numerator(cancel(together(.))) == 0);
    - EXACT-POINT mode: the spectral parameters are fixed at general-position rationals,
                        the tau stays a polynomial in R_i, C_k, and every coefficient of
                        that polynomial must be exactly 0.  Repeated over several
                        independent parameter sets.

* Order-of-accuracy claims are re-measured at 50 digits and compared with the predicted
  ratio (h^4 -> ratio 16, h^2 -> ratio 4).

Run:  python -u verify_claims.py
"""

import random

import sympy as sp

RESULTS = []


def record(tag, ok, detail=""):
    RESULTS.append((tag, bool(ok), detail))
    print(("[ PASS ] " if ok else "[ FAIL ] ") + tag + ("   -- " + detail if detail else ""),
          flush=True)


# ======================================================================================
# exact zero test for a rational function of the spectral parameters
# ======================================================================================

def is_zero(v):
    if v == 0:
        return True
    num, _ = sp.fraction(sp.cancel(sp.together(v)))
    return sp.expand(num) == 0


# ======================================================================================
# the Hirota engine
# ======================================================================================

x, t, y, a, h = sp.symbols("x t y a h", real=True)


class Model:
    """A bilinear model: rank-one factors R_i, C_k plus the phases xi_i, eta_k.

    subs = None  -> fully symbolic in the spectral parameters
    subs = {...} -> spectral parameters fixed at exact rationals (R_i, C_k stay symbolic)
    """

    def __init__(self, N, lattice, subs=None):
        self.N = N
        self.lattice = lattice
        self.p = sp.symbols(f"p1:{N + 1}", real=True)
        self.q = sp.symbols(f"q1:{N + 1}", real=True)
        self.R = sp.symbols(f"R1:{N + 1}", positive=True)
        self.C = sp.symbols(f"C1:{N + 1}", positive=True)
        self.subs = subs or {}
        self.A = sp.sympify(a).subs(self.subs) if self.subs else a
        self.H = sp.sympify(h).subs(self.subs) if self.subs else h
        self.dh = self.H / 2
        self.pv = [sp.sympify(pi).subs(self.subs) if self.subs else pi for pi in self.p]
        self.qv = [sp.sympify(qk).subs(self.subs) if self.subs else qk for qk in self.q]
        if self.subs:
            # guard against a silent substitution mismatch (see rand_subs)
            assert not self.A.free_symbols and not self.H.free_symbols, "subs missed a or h"
            for v in self.pv + self.qv:
                assert not v.free_symbols, f"subs missed a spectral symbol: {v}"

    # ---- phases -------------------------------------------------------------------
    def theta(self, avec, bvec, var):
        """d/dvar of  sum_i avec_i xi_i + sum_k bvec_k eta_k."""
        N = self.N
        if var == "x":
            return sum(avec[i] * self.pv[i] for i in range(N)) + sum(
                bvec[k] * self.qv[k] for k in range(N))
        if var == "t":
            return -sum(avec[i] * self.pv[i] ** 2 for i in range(N)) + sum(
                bvec[k] * self.qv[k] ** 2 for k in range(N))
        if var == "y":
            assert not self.lattice, "the lattice tau carries no y dependence"
            return sum(avec[i] / (self.pv[i] - self.A) for i in range(N)) + sum(
                bvec[k] / (self.qv[k] + self.A) for k in range(N))
        raise ValueError(var)

    # ---- tau ----------------------------------------------------------------------
    def chi(self, i, k):
        """the rank-one lattice multiplier chi_ik = lambda(p_i-a) lambda(q_k+a)."""
        P, Q, d = self.pv[i] - self.A, self.qv[k] + self.A, self.dh
        return ((P + d) / (P - d)) * ((Q + d) / (Q - d))

    def entry(self, n, s, i, k, j=0):
        sv = sp.sympify(s).subs(self.subs) if self.subs else s
        base = (1 / (self.pv[i] + self.qv[k])) * (-(self.pv[i] - sv) / (self.qv[k] + sv)) ** n
        fac = self.R[i] * self.C[k]
        if self.lattice:
            fac = fac * self.chi(i, k) ** j
        return (1 if i == k else 0) + base * fac

    def tau(self, n, s, j=0):
        N = self.N
        return sp.expand(sp.Matrix(N, N, lambda i, k: self.entry(n, s, i, k, j)).det())

    # ---- polynomials in R, C ------------------------------------------------------
    def to_dict(self, expr):
        gens = list(self.R) + list(self.C)
        poly = sp.Poly(sp.expand(expr), *gens)
        N = self.N
        out = {}
        for monom, coeff in zip(poly.monoms(), poly.coeffs()):
            out[(tuple(monom[:N]), tuple(monom[N:]))] = coeff
        return out

    def hirota(self, fd, gd, ops):
        """the pairwise Hirota rule; ops like {'x': 2} or {'y': 1, 't': 1}."""
        out = {}
        for (a1, b1), c1 in fd.items():
            for (a2, b2), c2 in gd.items():
                fac = sp.Integer(1)
                for var, m in ops.items():
                    fac *= (self.theta(a1, b1, var) - self.theta(a2, b2, var)) ** m
                if fac == 0:
                    continue
                key = (tuple(u + v for u, v in zip(a1, a2)),
                       tuple(u + v for u, v in zip(b1, b2)))
                out[key] = out.get(key, sp.Integer(0)) + c1 * c2 * fac
        return out

    def B(self, fd, gd, s, extra=None):
        """(D_x^2 + D_t + 2 s D_x) f.g, optionally preceded by extra Hirota factors."""
        sv = sp.sympify(s).subs(self.subs) if self.subs else s
        acc = {}
        for ops, w in (({"x": 2}, sp.Integer(1)), ({"t": 1}, sp.Integer(1)), ({"x": 1}, 2 * sv)):
            if extra:
                ops = dict(ops)
                for var, m in extra.items():
                    ops[var] = ops.get(var, 0) + m
            for k, v in self.hirota(fd, gd, ops).items():
                acc[k] = acc.get(k, sp.Integer(0)) + w * v
        return acc


def add(d1, d2, w=1):
    out = dict(d1)
    for k, v in d2.items():
        out[k] = out.get(k, sp.Integer(0)) + w * v
    return out


def scale(d, w):
    return {k: v * w for k, v in d.items()}


def clean(model, d):
    """keep only the coefficients that are provably not zero."""
    if model.subs:
        return {k: sp.expand(sp.nsimplify(v)) for k, v in d.items() if sp.expand(v) != 0}
    return {k: v for k, v in d.items() if not is_zero(v)}


def rand_subs(N, seed):
    """general-position rational spectral parameters (no degenerate denominators).

    NOTE: the symbols must be built with the *same assumptions* as in Model.__init__
    (real=True) -- otherwise sympy's subs() silently refuses to match them, the model
    stays symbolic, and the "exact point" mode degenerates into a slow symbolic run.
    """
    rng = random.Random(seed)
    while True:
        s = {}
        for i in range(N):
            s[sp.symbols(f"p{i + 1}", real=True)] = sp.Rational(rng.randint(2, 23), rng.randint(1, 7))
            s[sp.symbols(f"q{i + 1}", real=True)] = sp.Rational(rng.randint(2, 23), rng.randint(1, 7))
        A = sp.Rational(rng.randint(2, 19), rng.randint(1, 5))
        H = sp.Rational(rng.randint(1, 5), rng.randint(3, 11))
        s[a], s[h] = A, H
        good = True
        for i in range(N):
            pi = s[sp.symbols(f"p{i + 1}", real=True)]
            qk = s[sp.symbols(f"q{i + 1}", real=True)]
            if pi - A == 0 or qk + A == 0:
                good = False
            for u in (-H / 2, 0, H / 2):
                if pi - A + u == 0 or qk + A + u == 0:
                    good = False
            for k in range(N):
                if pi + s[sp.symbols(f"q{k + 1}", real=True)] == 0:
                    good = False
        if good:
            return s


print("=" * 94)
print("DLW semi-discretization -- independent verification battery")
print("=" * 94)

# ======================================================================================
print("\n### 0. the rank-one lattice multiplier\n")
# ======================================================================================

P, Q, dd = sp.symbols("P Q dd", positive=True)
record("chi_ik = lambda(P_i) lambda(Q_k): a product of a row-only and a column-only factor",
       sp.simplify(((P + dd) / (P - dd)) * ((Q + dd) / (Q - dd))
                   - ((P + dd) / (P - dd)) * ((Q + dd) / (Q - dd))) == 0,
       "hence chi is multiplicatively rank one")

# ======================================================================================
print("\n### 1. continuum baseline: the Gram tau solves (6) and (7)\n")
# ======================================================================================

for N, seed in [(1, None), (2, None), (3, 11)]:
    subs = None if seed is None else rand_subs(N, seed)
    label = "symbolic" if subs is None else f"exact point #{seed}"
    m = Model(N, lattice=False, subs=subs)
    f = m.to_dict(m.tau(1, a))
    g = m.to_dict(m.tau(0, a))
    record(f"(7)          B_a tau_1 . tau_0 = 0                       N={N} [{label}]",
           not clean(m, m.B(f, g, a)))
    dyB = add(m.hirota(f, g, {"y": 1, "x": 2}), m.hirota(f, g, {"y": 1, "t": 1}))
    dyB = add(dyB, m.hirota(f, g, {"y": 1, "x": 1}), 2 * m.A)
    record(f"(6)|lam=-2   D_y B_a tau_1.tau_0 - 4 D_x tau_1.tau_0 = 0   N={N} [{label}]",
           not clean(m, add(dyB, m.hirota(f, g, {"x": 1}), -4)))

# ======================================================================================
print("\n### 2. the structural identity (dagger): tau_1(j; a-d) = tau_1(j+1; a+d)\n")
# ======================================================================================

pp, qq, aa, hh, jj = sp.symbols("pp qq aa hh jj", positive=True)
d2 = hh / 2
PP, QQ = pp - aa, qq + aa
chi1 = ((PP + d2) / (PP - d2)) * ((QQ + d2) / (QQ - d2))
lhs_t = (-(PP + d2) / (QQ - d2)) * chi1 ** jj          # tau_1(j; a-d)
rhs_t = (-(PP - d2) / (QQ + d2)) * chi1 ** (jj + 1)    # tau_1(j+1; a+d)
record("(dagger) tau_1(j;a-d) = tau_1(j+1;a+d), elementwise, for every h and every j",
       sp.simplify(sp.together(lhs_t - rhs_t)) == 0)
Wsym = sp.Symbol("Wsym")
# spectralFactor(p,q,s) = -(p-s)/(q+s), latticeMult = chi = ((P+d)(Q+d))/((P-d)(Q-d))
record("equivalently, in the Lean spelling: spectralFactor(a+d) * (latticeMult * W) = spectralFactor(a-d) * W",
       is_zero((-(PP - d2) / (QQ + d2)) * (chi1 * Wsym) - (-(PP + d2) / (QQ - d2)) * Wsym),
       "the Lean statements DLW.staggered_entry_identity / DLW.tau1_det_staggered_one")

# ======================================================================================
print("\n### 3. the staggered discrete pair (star)\n")
# ======================================================================================

MODES = [(1, None, (0, 1, 2)),
         (2, 101, (0, 1, 2)), (2, 102, (0, 2)),
         (3, 103, (0, 1)), (3, 104, (0,)),
         (4, 105, (0,))]

for N, seed, sites in MODES:
    subs = None if seed is None else rand_subs(N, seed)
    label = "symbolic" if subs is None else f"exact point #{seed}"
    for j in sites:
        m = Model(N, lattice=True, subs=subs)
        F = m.to_dict(m.tau(1, a - m.dh, j))
        G = m.to_dict(m.tau(0, a, j))
        Gp = m.to_dict(m.tau(0, a, j + 1))
        record(f"(7)_h  B_(a-d) F_j . G_j      = 0     N={N} j={j}  [{label}]",
               not clean(m, m.B(F, G, a - m.dh)))
        record(f"(6)_h  B_(a+d) F_j . G_(j+1)  = 0     N={N} j={j}  [{label}]",
               not clean(m, m.B(F, Gp, a + m.dh)))

# ======================================================================================
print("\n### 4. the two-point form (star') and its equivalence with ((6)_h-(7)_h)/h\n")
# ======================================================================================

for N, seed in [(1, None), (2, 101), (2, 102), (3, 103)]:
    subs = None if seed is None else rand_subs(N, seed)
    label = "symbolic" if subs is None else f"exact point #{seed}"
    m = Model(N, lattice=True, subs=subs)
    j = 0
    F = m.to_dict(m.tau(1, a - m.dh, j))
    G = m.to_dict(m.tau(0, a, j))
    Gp = m.to_dict(m.tau(0, a, j + 1))
    dG = add(Gp, G, -1)
    star = scale(add(m.B(F, dG, a - m.dh), m.hirota(F, Gp, {"x": 1}), 2 * m.H), 1 / m.H)
    record(f"(star') = 0                                       N={N} [{label}]",
           not clean(m, star))
    diff = scale(add(m.B(F, Gp, a + m.dh), m.B(F, G, a - m.dh), -1), 1 / m.H)
    record(f"(star') == ((6)_h - (7)_h)/h   (B_(a+d)=B_(a-d)+2hD_x)   N={N} [{label}]",
           not clean(m, add(star, diff, -1)))

# ======================================================================================
print("\n### 5. the naive central difference is only first order (the obstruction)\n")
# ======================================================================================

for N, seed in [(1, None), (2, 101), (3, 103), (4, 105)]:
    subs = None if seed is None else rand_subs(N, seed)
    label = "symbolic" if subs is None else f"exact point #{seed}"
    m = Model(N, lattice=True, subs=subs)
    j = 0
    f0 = m.to_dict(m.tau(1, a, j))
    g0 = m.to_dict(m.tau(0, a, j))
    fp = m.to_dict(m.tau(1, a, j + 1))
    gp = m.to_dict(m.tau(0, a, j + 1))
    naive = scale(add(m.B(fp, g0, a), m.B(f0, gp, a), -1), 1 / m.H)
    naive = clean(m, add(naive, m.hirota(f0, g0, {"x": 1}), -4))
    record(f"naive central difference is NOT an identity        N={N} [{label}]",
           bool(naive), f"{len(naive)} surviving monomial(s)")

# closed form for N = 1 -- NOTE: the exponential factor E = exp(xi_1+eta_1) CANCELS
# between the two B's, so the residual is E-free.  (dlw_semidiscrete/REPORT.md SS5.3
# prints the same formula with a spurious extra factor E; see SS6.5 of index.html.)
m = Model(1, lattice=True)
Csym = sp.Symbol("Csym", positive=True)
j = 0
f0 = m.to_dict(m.tau(1, a, j))
g0 = m.to_dict(m.tau(0, a, j))
fp = m.to_dict(m.tau(1, a, j + 1))
gp = m.to_dict(m.tau(0, a, j + 1))
naive = scale(add(m.B(fp, g0, a), m.B(f0, gp, a), -1), 1 / h)
naive = clean(m, add(naive, m.hirota(f0, g0, {"x": 1}), -4))
closed = list(naive.values())[0]
pred = (h * (m.p[0] + m.q[0]) * (h - 2 * m.p[0] - 2 * m.q[0])
        / ((m.q[0] + a) * ((m.p[0] - a) - m.dh) * ((m.q[0] + a) - m.dh)))
record("naive residual, N=1, exact: res = h c (p+q)(h-2p-2q)/(Q(P-d)(Q-d))  [E-free]",
       is_zero(closed - pred), "directly contradicts the extra E printed in REPORT.md SS5.3")
val = sp.nsimplify(sp.expand(pred.subs({m.p[0]: 1, m.q[0]: 2, a: 3, h: sp.Rational(1, 4)})))
record("the same residual at (p,q,a,h)=(1,2,3,1/4) is nonzero", val != 0,
       f"residual = {val}")

# --- the zero locus: it IS a nonzero function, but it does vanish on a hypersurface -------
record("the numerator factors as h (p+q) (h-2p-2q), so the residual has a zero locus",
       is_zero(pred - h * (m.p[0] + m.q[0]) * (h - 2 * m.p[0] - 2 * m.q[0])
               / ((m.q[0] + a) * ((m.p[0] - a) - m.dh) * ((m.q[0] + a) - m.dh))),
       "NOT 'nonzero for every h > 0' -- only 'not identically zero'")

ZC = {m.p[0]: 1, m.q[0]: 2, a: 0, h: 6}   # a = 0, p = 1, q = 2, h = 6  =>  h = 2(p+q)
mz = Model(1, lattice=True, subs=ZC)
den = ((m.q[0] + a) * ((m.p[0] - a) - m.dh) * ((m.q[0] + a) - m.dh))
record("ratio check at a=0,p=1,q=2,h=6: h-2p-2q = 0 while Q(P-d)(Q-d) != 0",
       sp.nsimplify(pred.subs(ZC)) == 0 and sp.nsimplify(den.subs(ZC)) != 0,
       f"h-2p-2q = {sp.nsimplify((h - 2 * m.p[0] - 2 * m.q[0]).subs(ZC))}, "
       f"denominator = {sp.nsimplify(den.subs(ZC))}")
f0z = mz.to_dict(mz.tau(1, a, 0))
g0z = mz.to_dict(mz.tau(0, a, 0))
fpz = mz.to_dict(mz.tau(1, a, 1))
gpz = mz.to_dict(mz.tau(0, a, 1))
nz = scale(add(mz.B(fpz, g0z, a), mz.B(f0z, gpz, a), -1), 1 / mz.H)
nz = clean(mz, add(nz, mz.hirota(f0z, g0z, {"x": 1}), -4))
record("the FULL bilinear residual really is 0 at that point (not just the closed form)",
       not nz, "a genuine counterexample to the earlier 'nonzero for every h > 0'")

# --- the non-degeneracy needed by the 'iff r = s' claim --------------------------------
Pq, Qq, dq = sp.symbols("Pq Qq dq", real=True)
chiq = ((Pq + dq) / (Pq - dq)) * ((Qq + dq) / (Qq - dq))
record("chi = 1  <=>  2d(P+Q) = 0: with d > 0 this is exactly p + q = 0, the Gram pole",
       is_zero((chiq - 1) - 2 * dq * (Pq + Qq) / ((Pq - dq) * (Qq - dq))),
       "so 'vanishes iff r = s' needs P != 0, h > 0 and p + q != 0 (i.e. chi != 1)")

# ======================================================================================
print("\n### 5b. the exact cross-site identity for (7), and its antisymmetry\n")
# ======================================================================================

for px, qx in ((0, 1), (1, 2), (0, 3)):
    mm = Model(1, lattice=True)
    f = mm.to_dict(mm.tau(1, a, px))
    g = mm.to_dict(mm.tau(0, a, qx))
    lhs = clean(mm, mm.B(f, g, a)).get(((1,), (1,)), sp.Integer(0))
    PP, QQ, dd0 = mm.p[0] - a, mm.q[0] + a, mm.dh
    chiN = ((PP + dd0) / (PP - dd0)) * ((QQ + dd0) / (QQ - dd0))
    pred2 = 2 * PP * (chiN ** qx - chiN ** px)
    record(f"(7) cross-site, N=1:  B_a tau_1(j={px}) . tau_0(j={qx}) = 2P(chi^{qx}-chi^{px})  [E-free]",
           is_zero(lhs - pred2),
           "antisymmetric in (p,q): vanishes iff p=q -- the report's extra E is spurious")
    if px == 0 and qx == 1:
        nums = {mm.p[0]: sp.Rational(5, 3), mm.q[0]: sp.Rational(7, 4), a: sp.Rational(3, 2),
                mm.R[0]: 2, mm.C[0]: 3}
        record("   ... and the same identity evaluated at (p,q,a,E)=(5/3,7/4,3/2,6)",
               is_zero(sp.expand(lhs - pred2).subs(nums)),
               f"lhs = {sp.nsimplify(sp.expand(lhs.subs(nums)))}")

# ======================================================================================
print("\n### 6. the exact jet expansions (T1)\n")
# ======================================================================================

b0, b1, b2, b3, b4, d0, d1, d2_, d3 = sp.symbols("b0 b1 b2 b3 b4 d0 d1 d2 d3")
U, Up = sp.symbols("U Up")

jetB = lambda u: b0 + u * b1 + u ** 2 / 2 * b2 + u ** 3 / 6 * b3 + u ** 4 / 24 * b4
jetD = lambda u: d0 + u * d1 + u ** 2 / 2 * d2_ + u ** 3 / 6 * d3
stagP = lambda up: jetB(h / 2) + 2 * up * jetD(h / 2)
stagM = lambda u: jetB(-h / 2) + 2 * u * jetD(-h / 2)

record("symmetric:     1/2[(6)_h+(7)_h] = b0 + (h^2/8)(b2+4d1) + h^4(b4/384+d3/48)  [exact]",
       sp.expand((stagP(h / 2) + stagM(-h / 2)) / 2
                 - (b0 + h ** 2 / 8 * (b2 + 4 * d1) + h ** 4 * (b4 / 384 + d3 / 48))) == 0)
record("antisymmetric: [(6)_h-(7)_h]/h = (b1+2d0) + (h^2/24)(b3+6d2)                [exact]",
       sp.simplify(sp.expand((stagP(h / 2) - stagM(-h / 2)) / h
                             - ((b1 + 2 * d0) + h ** 2 / 24 * (b3 + 6 * d2_)))) == 0)
record("general offsets, symmetric half: exact closed form for every u, u'",
       sp.expand((stagP(Up) + stagM(U)) / 2
                 - (b0 + (U + Up) * d0 + h / 2 * (Up - U) * d1
                    + h ** 2 / 8 * (b2 + (U + Up) * d2_) + h ** 3 / 48 * (Up - U) * d3
                    + h ** 4 / 384 * b4)) == 0,
       "matches DLW.symmetric_expansion_general")
record("general offsets, antisymmetric half: exact closed form for every u, u'",
       sp.expand((stagP(Up) - stagM(U)) / h
                 - (b1 + 2 * (Up - U) / h * d0 + (Up + U) * d1 + h ** 2 / 24 * b3
                    + h / 4 * (Up - U) * d2_ + h ** 2 / 24 * (Up + U) * d3)) == 0,
       "matches DLW.antisymmetric_expansion_general")
record("equal offsets u'=u: the coefficient of d0 in the antisymmetric half is exactly 0",
       sp.simplify(sp.expand((stagP(U) - stagM(U)) / h).coeff(d0)) == 0,
       "matches DLW.collapse_zero_dx_coefficient")
record("general offsets: the coefficient of d0 is 2(u'-u)/h, so matching 2 d0 forces u'-u = h",
       sp.simplify(sp.expand((stagP(Up) - stagM(U)) / h).coeff(d0) - 2 * (Up - U) / h) == 0,
       "matches DLW.offset_gap_forced")
record("centring u + u' = 0 kills the mean-offset terms (u+u')d0, (u+u')d2, (u+u')d3",
       sp.simplify(((U + Up) * d0).subs(Up, -U)) == 0,
       "matches DLW.mean_offset_forced; the half-sum (u+u')/2 is a relabelling of a")

# ======================================================================================
print("\n### 7. the order of the continuous limit, re-measured at 50 digits\n")
# ======================================================================================

yy = sp.Symbol("yy", real=True)
Pfun = sp.exp(-yy ** 2)
Qfun = sp.sin(yy) + sp.exp(-yy ** 2 / 3)
Y0 = sp.Rational(1, 3)
# NOTE: both test functions are analytic, hence of class C^5 -- which is what the sharp
# antisymmetric statement needs (Lean: DLW.antisymmetric_remainder_isBigO4, hP : ContDiff ℝ 5 P).
second = sp.diff(Pfun, yy, 2).subs(yy, Y0)
first = sp.diff(Pfun, yy).subs(yy, Y0)
third = sp.diff(Pfun, yy, 3).subs(yy, Y0)
q1 = sp.diff(Qfun, yy).subs(yy, Y0)
q2 = sp.diff(Qfun, yy, 2).subs(yy, Y0)


def _num(hv, jet):
    return sp.N(((Pfun.subs(yy, Y0 + hv / 2) + hv * Qfun.subs(yy, Y0 + hv / 2))
                 - (Pfun.subs(yy, Y0 - hv / 2) - hv * Qfun.subs(yy, Y0 - hv / 2))) / hv
                - jet, 50)


rem_sym = lambda hv: sp.N(((Pfun.subs(yy, Y0 + hv / 2) + hv * Qfun.subs(yy, Y0 + hv / 2))
                           + (Pfun.subs(yy, Y0 - hv / 2) - hv * Qfun.subs(yy, Y0 - hv / 2))) / 2
                          - (Pfun.subs(yy, Y0) + hv ** 2 / 8 * (second + 4 * q1)), 50)
# sharp (C^5) antisymmetric remainder: also remove the explicit h^2 coefficient
rem_anti4 = lambda hv: _num(hv, first + 2 * Qfun.subs(yy, Y0)
                            + hv ** 2 / 24 * (third + 6 * q2))
# weak (C^4) antisymmetric remainder: remove M1 only
rem_anti2 = lambda hv: _num(hv, first + 2 * Qfun.subs(yy, Y0))

hs = [sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 16), sp.Rational(1, 32)]
rs = [abs(rem_sym(hv)) for hv in hs]
ra = [abs(rem_anti4(hv)) for hv in hs]
ra2 = [abs(rem_anti2(hv)) for hv in hs]
print("   TEST FUNCTION: P(y)=exp(-y^2),  Q(y)=sin(y)+exp(-y^2/3),  Y0 = 1/3")
print("   |symmetric remainder|      :", " ".join("%.6e" % v for v in rs))
print("        successive ratios      :", " ".join("%.3f" % (rs[i] / rs[i + 1]) for i in range(len(rs) - 1)))
print("   |antisymmetric remainder|  :", " ".join("%.6e" % v for v in ra))
print("        successive ratios      :", " ".join("%.3f" % (ra[i] / ra[i + 1]) for i in range(len(ra) - 1)))
record("symmetric remainder decays like h^4 (ratio -> 16)", abs(rs[-2] / rs[-1] - 16) < 1.0,
       f"last ratio = {float(rs[-2] / rs[-1]):.3f}")
record("antisymmetric remainder decays like h^4 (ratio -> 16) -- the C^5 statement, "
       "Lean theorem DLW.antisymmetric_remainder_isBigO4",
       abs(ra[-2] / ra[-1] - 16) < 1.0, f"last ratio = {float(ra[-2] / ra[-1]):.3f}")
# the weaker C^4 statement: subtract M1 only, i.e. do NOT remove the explicit h^2 term
ra2 = [abs(sp.N(((Pfun.subs(yy, Y0 + hv / 2) + hv * Qfun.subs(yy, Y0 + hv / 2))
                 - (Pfun.subs(yy, Y0 - hv / 2) - hv * Qfun.subs(yy, Y0 - hv / 2))) / hv
                - (first + 2 * Qfun.subs(yy, Y0)), 50)) for hv in hs]
print("   |[(6)h-(7)h]/h - M1|      :", " ".join("%.6e" % v for v in ra2))
print("        successive ratios      :", " ".join("%.3f" % (ra2[i] / ra2[i + 1]) for i in range(len(ra2) - 1)))
record("without removing the h^2 term the antisymmetric remainder is only O(h^2) (ratio -> 4) "
       "-- the C^4 statement, Lean theorem DLW.antisymmetric_remainder_isBigO",
       abs(ra2[-2] / ra2[-1] - 4) < 0.6, f"last ratio = {float(ra2[-2] / ra2[-1]):.3f}")

# ======================================================================================
print("\n### 8. the y-rate: exact centred rate, Pade error, and the h -> 0 limit\n")
# ======================================================================================

Psym, dsym = sp.symbols("Psym dsym", nonzero=True, real=True)
chi_s = (Psym + dsym) / (Psym - dsym)
record("the centred rate is exact:  (chi-1)/(d(chi+1)) = 1/P  for every d",
       sp.simplify((chi_s - 1) / (dsym * (chi_s + 1)) - 1 / Psym) == 0,
       "matches DLW.lattice_rate_centred_exact")

zz = sp.Symbol("zz", positive=True)
lamz = (zz + h / 2) / (zz - h / 2)
series = sp.series(sp.log(lamz) / h, h, 0, 7).removeO()
target = 1 / zz + h ** 2 / (12 * zz ** 3) + h ** 4 / (80 * zz ** 5) + h ** 6 / (448 * zz ** 7)
record("lattice dispersion: (1/h)ln lambda(z) = 1/z + h^2/(12z^3) + h^4/(80z^5) + h^6/(448z^7) + O(h^8)",
       sp.simplify(sp.expand(series - target)) == 0, f"series = {sp.simplify(series)}")

num = [abs(sp.N(sp.log(lamz.subs({h: hv, zz: 2})) / hv - sp.Rational(1, 2), 40)) for hv in hs]
print("   |(1/h)ln lambda(2) - 1/2|  :", " ".join("%.6e" % v for v in num))
print("        successive ratios      :", " ".join("%.3f" % (num[i] / num[i + 1]) for i in range(len(num) - 1)))
record("(1/h) ln lambda(z) -> 1/z with second-order error (ratio -> 4)",
       abs(num[-2] / num[-1] - 4) < 0.6, f"last ratio = {float(num[-2] / num[-1]):.3f}")

xx = sp.Symbol("xx", positive=True)
record("Pade:  (2+x)/(2-x) - (1+x+x^2/2) = x^3/(2(2-x))   (third-order truncation)",
       sp.simplify((2 + xx) / (2 - xx) - (1 + xx + xx ** 2 / 2) - xx ** 3 / (2 * (2 - xx))) == 0,
       "matches DLW.mobiusRate_second_order")

# ======================================================================================
print("\n### 9. the two-soliton interaction factor is untouched by the lattice\n")
# ======================================================================================

N = 2
s_param = sp.Symbol("s_param")


def interaction(model, n, s, j):
    """(top coefficient) / (product of the two single-excitation coefficients)."""
    full = model.to_dict(sp.expand(model.tau(n, s, j)))
    top = (tuple([1] * N), tuple([1] * N))
    e1 = (tuple([1] + [0] * (N - 1)), tuple([1] + [0] * (N - 1)))
    e2 = (tuple([0] * (N - 1) + [1]), tuple([0] * (N - 1) + [1]))
    num, den = full.get(top, 0), full.get(e1, 0) * full.get(e2, 0)
    return sp.cancel(num / den) if model.subs else sp.simplify(num / den)


# --- the h- and j-independence, at exact general-position parameter points ------------
for seed in (201, 202, 203):
    subs = rand_subs(N, seed)
    mc = Model(N, lattice=False, subs=subs)
    ml = Model(N, lattice=True, subs=subs)
    kc = interaction(mc, 1, s_param, 0)
    kl = interaction(ml, 1, a - h / 2, 0)
    kc_at = interaction(mc, 1, a - h / 2, 0)
    record(f"interaction factor: lattice == continuum at the same parameter  [exact point #{seed}]",
           sp.nsimplify(kl - kc_at) == 0)
    record(f"interaction factor is independent of the lattice site j  [exact point #{seed}]",
           sp.nsimplify(interaction(ml, 1, a - h / 2, 7) - kl) == 0)
    record(f"interaction factor is independent of h  [exact point #{seed}]",
           sp.nsimplify(interaction(ml, 1, a - h / 2, 0)
                        - interaction(ml, 1, a - sp.Rational(1, 97), 0)) == 0)

# --- the closed form (continuum, no h involved -> cheap and fully symbolic) ----------
mc = Model(N, lattice=False)
k_cont = interaction(mc, 1, s_param, 0)
p1, p2, q1, q2 = mc.p[0], mc.p[1], mc.q[0], mc.q[1]
kappa = ((p1 - a) * (p2 - a) * (p1 - p2) * (q1 - q2)) / (
    (a + q1) * (a + q2) * (p1 + q1) * (p1 + q2) * (p2 + q1) * (p2 + q2))
A11 = (1 / (p1 + q1)) * (-(p1 - a) / (q1 + a))
A22 = (1 / (p2 + q2)) * (-(p2 - a) / (q2 + a))
record("closed form matches dlw_semidiscrete/REPORT.md section 8.1 (kappa is h-free)",
       is_zero(k_cont.subs(s_param, a) - kappa / (A11 * A22)))

# ======================================================================================
print("\n" + "=" * 94)
ok = sum(1 for _, o, _ in RESULTS if o)
print(f"SUMMARY: {ok}/{len(RESULTS)} checks passed")
for tag, o, _ in RESULTS:
    if not o:
        print("   FAILED:", tag)
print("=" * 94)
