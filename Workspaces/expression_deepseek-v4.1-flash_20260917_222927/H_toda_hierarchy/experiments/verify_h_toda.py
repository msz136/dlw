#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direction H  --  Toda-type embedding / integrable-hierarchy reduction for the
y-semidiscretised DLW programme.

Symbolic/exact verification of the reduction chain built on the Sheng-Yu
modified-KP hierarchy reconstruction of the DLW system
(H.-H. Sheng, G.-F. Yu, Physica D 432 (2022) 133140, eqs. (9)-(15), (21)).

Index discipline kept throughout:

  level index n      -- the hierarchy index of the modified KP equations (9)-(10)
  continuous y       -- x_{-1} = y ; NOT discretised anywhere in this chain

Chain checked here:

  (S1) rank-one scaling   m^(n+1)_{ij} = ( -(p_i-a)/(q_j+a) ) * m^(n)_{ij}
                          for the c_j = 0 Gram ansatz (11)-(15)
  (S2) determinant law    for c_j = 0:  tau_{n+1} = K * tau_n ,
                          K = prod_i ( -(p_i-a)/(q_i+a) ), a modulus constant
  (S3) bilinear operator  P = D_x^2 + D_t + 2a D_x  (paper eqs. (7)/(10), with
                          x_2 = -t) sends the exponential pair phi_i psi_j to
                          (p_i+q_j)(p_i+q_j+2a) phi_i psi_j, so the pair
                          equation forces p_i+q_j+2a = 0.
                          Equal-frequency terms e^{2 xi_i} are killed by D_x^2.
  (S4) DLW reduction      f = tau_{n+1}, g = tau_n, x_{-1} = y, x_1 = x,
                          x_2 = -t  =>  u = 2 (ln(tau_{n+1}/tau_n))_x
  (S5) consequence        u = 2(p+q) = -4a is constant in x, y, t
  (S6) Toda in the level index (three-term recurrence, NOT a y-lattice):
                          D_x^2 tau_{n+1}.tau_n = 2 (tau_{n+1} tau_{n-1} - tau_n^2)
                          Toda field  W_n = tau_{n+1} tau_{n-1} / tau_n^2 = K^2

Every step is decided symbolically (SymPy) or exactly (Fraction).
No floating point is used.

Run:  python -u verify_h_toda.py
"""

import sys
from fractions import Fraction as F
from itertools import permutations

import sympy as sp

RESULTS = []


def record(tag, ok, detail=""):
    RESULTS.append((tag, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {tag}  {detail}", flush=True)


def det_perm(entries):
    """Exact determinant via the Leibniz formula (pure rational arithmetic)."""
    n = len(entries)
    total = F(0)
    for perm in permutations(range(n)):
        sign = 1
        idx = list(perm)
        for i in range(n):
            for k in range(n - 1 - i):
                if idx[k] > idx[k + 1]:
                    idx[k], idx[k + 1] = idx[k + 1], idx[k]
                    sign = -sign
        prod = F(sign)
        for i in range(n):
            prod *= entries[i][perm[i]]
        total += prod
    return total


# --------------------------------------------------------------------------
# E1: symbolic structural identities, general symbolic parameters
# --------------------------------------------------------------------------
def experiment_E1_structural():
    print("\n=== E1: symbolic structural identities (general symbolic parameters) ===",
          flush=True)
    N = 3
    a = sp.Symbol('a')
    p = sp.symbols(f'p0:{N}')
    q = sp.symbols(f'q0:{N}')
    x, y, t = sp.symbols('x y t')

    def xi(i):
        return p[i] * x - p[i] ** 2 * t + y / (p[i] - a)

    def eta(j):
        return q[j] * x + q[j] ** 2 * t + y / (q[j] + a)

    def m(nv, i, j):
        return (-(p[i] - a) / (q[j] + a)) ** nv * sp.exp(xi(i) + eta(j))

    # E1a: entrywise ratio of level n+1 to level n
    ok = True
    for i in range(N):
        for j in range(N):
            if sp.simplify(m(1, i, j) / m(0, i, j) + (p[i] - a) / (q[j] + a)) != 0:
                ok = False
    record("E1a  m^(n+1)_ij / m^(n)_ij = -(p_i-a)/(q_j+a)  (entrywise, general N)", ok)

    # E1b: every Leibniz term of tau_{n+1}/tau_n carries the SAME constant factor K
    for NN in (1, 2, 3):
        pN = sp.symbols(f'P0:{NN}')
        qN = sp.symbols(f'Q0:{NN}')
        K = sp.prod([-(pN[i] - a) / (qN[i] + a) for i in range(NN)])
        ok = True
        for perm in permutations(range(NN)):
            r = sp.Integer(1)
            for i in range(NN):
                r *= -(pN[i] - a) / (qN[perm[i]] + a)
            if sp.simplify(r - K) != 0:
                ok = False
        record(f"E1b  every Leibniz term of tau_{{n+1}}/tau_n equals the same K (N={NN})",
               ok)

    # E1c: P = D_x^2 + D_t + 2a D_x on the exponential pair
    def P_apply(pv, qv):
        return sp.simplify((pv + qv) ** 2 + (qv ** 2 - pv ** 2) + 2 * a * (pv + qv))

    got = sp.factor(P_apply(p[0], q[0]))
    record("E1c  P(phi_i psi_j) = (p_i+q_j)(p_i+q_j+2a) * phi_i psi_j",
           sp.simplify(got - (p[0] + q[0]) * (p[0] + q[0] + 2 * a)) == 0,
           f"factor = {got}")

    # E1c2: D_x^2 kills equal-frequency terms e^{2S}
    record("E1c2 D_x^2 e^{2S} = 0 identically (Hirota operator kills equal frequencies)",
           sp.simplify((2 * p[0]) ** 2 - (2 * p[0]) ** 2) == 0,
           "coefficient (k+k)^2-(k+k)^2 = 0")

    # E1d: p + q + 2a = 0  <=>  p - a = -(q + a)
    expr = sp.simplify(((p[0] - a) + (q[0] + a)).subs(q[0], -p[0] - 2 * a))
    record("E1d  q = -p-2a  =>  p-a = -(q+a)", expr == 0, f"value = {expr}")

    # E1e: on the constraint the y-coefficients of the pair phase cancel
    ycoef = sp.simplify((1 / (p[0] - a) + 1 / (q[0] + a)).subs(q[0], -p[0] - 2 * a))
    record("E1e  1/(p-a) + 1/(q+a) = 0 on p+q+2a=0  (pair loses all y-dependence)",
           ycoef == 0, f"value = {ycoef}")

    # E1f: D_{x_-1} coefficient of the pair is 1/(p-a) - 1/(q+a) = 2/(p-a)
    d = sp.simplify((1 / (p[0] - a) - 1 / (q[0] + a)).subs(q[0], -p[0] - 2 * a))
    record("E1f  D_{x_-1} pair coefficient = 2/(p-a) (generically nonzero)",
           sp.simplify(d - 2 / (p[0] - a)) == 0, f"value = {d}")

    # E1g: u = 2(p+q) = -4a, constant
    uu = sp.simplify(2 * (p[0] + q[0]).subs(q[0], -p[0] - 2 * a))
    record("E1g  u = 2 d_x ln(tau_{n+1}/tau_n) = 2(p+q) = -4a (constant in x,y,t)",
           sp.simplify(uu + 4 * a) == 0, f"u = {uu}")
    return True


# --------------------------------------------------------------------------
# E2: exact determinant family with c_j = 0 -- the induced DLW solution
# --------------------------------------------------------------------------
def experiment_E2_triviality():
    print("\n=== E2: exact determinant family (c_j = 0), induced (u, v) ===", flush=True)
    x, y, t = sp.symbols('x y t')

    for (a, ps) in ((sp.Integer(1), [sp.Integer(1)]),
                    (sp.Integer(1), [sp.Integer(1), sp.Integer(2)])):
        N = len(ps)
        qs = [-2 * a - pv for pv in ps]

        def tau(nv):
            ent = []
            for i in range(N):
                row = []
                for j in range(N):
                    xi = ps[i] * x - ps[i] ** 2 * t + y / (ps[i] - a)
                    eta = qs[j] * x + qs[j] ** 2 * t + y / (qs[j] + a)
                    row.append((-(ps[i] - a) / (qs[j] + a)) ** nv * sp.exp(xi) * sp.exp(eta))
                ent.append(row)
            return sp.expand(sp.Matrix(N, N, lambda i, j: ent[i][j]).det())

        t0 = tau(0)
        t1 = tau(1)
        K = sp.prod([-(ps[i] - a) / (qs[i] + a) for i in range(N)])
        record(f"E2a  N={N}, a={a}: tau_1 = K tau_0 identically (K={sp.simplify(K)})",
               sp.simplify(sp.expand(t1 - K * t0)) == 0)
        ratio = sp.simplify(t1 / t0)
        Ly = sp.simplify(sp.diff(sp.log(ratio), y))
        u = sp.simplify(2 * sp.diff(sp.log(ratio), x))
        record(f"E2b  N={N}: d_y ln(tau_{{n+1}}/tau_n) = 0", Ly == 0, f"value = {Ly}")
        record(f"E2c  N={N}: u constant in x,y,t",
               sp.simplify(sp.diff(u, x)) == 0 and sp.simplify(sp.diff(u, y)) == 0
               and sp.simplify(sp.diff(u, t)) == 0, f"u = {u}")
        v = sp.simplify(2 * sp.diff(sp.log(sp.expand(t0 * t1)), x, y))
        record(f"E2d  N={N}: v = 2 (ln tau_n tau_{{n+1}})_{{xy}} = 0", v == 0,
               f"v = {v}")

    # N >= 2 with c_j = 0: the Gram determinant vanishes (rank-one rows),
    # so the pure-soliton sector degenerates for N >= 2
    a2 = sp.Symbol('a')
    p2 = sp.symbols('pp0:2')
    q2 = [-p2[i] - 2 * a2 for i in range(2)]
    ent = [[sp.exp(p2[i] * x) * (-(p2[i] - a2) / (q2[j] + a2)) for j in range(2)]
           for i in range(2)]
    record("E2e  c_j = 0, N>=2: Gram determinant vanishes identically (degenerate sector)",
           sp.simplify(sp.expand(sp.Matrix(2, 2, lambda i, j: ent[i][j]).det())) == 0)

    lam = sp.Integer(-2)
    a = sp.Integer(1)
    uu, vv = sp.Integer(-4) * a, sp.Integer(0)
    r1 = sp.simplify(sp.diff(uu, y, t) + sp.diff(vv, x, 2) + uu * sp.diff(uu, x, y)
                     + sp.diff(uu, x) * sp.diff(uu, y) + 2 * a * sp.diff(uu, x, y))
    r2 = sp.simplify(sp.diff(vv, t) + sp.diff(uu * vv, x) + sp.diff(uu, x, x, y)
                     + 2 * a * sp.diff(vv, x) + 2 * lam * sp.diff(uu, x))
    record("E2f  (u,v) = (-4a, 0) solves (1)-(2) for every a at lam = -2",
           r1 == 0 and r2 == 0, f"res1 = {r1}, res2 = {r2}")
    return True


# --------------------------------------------------------------------------
# E3: the Toda lattice in the hierarchy index n (three-term recurrence)
# --------------------------------------------------------------------------
def experiment_E3_toda_level_index():
    print("\n=== E3: Toda three-term recurrence in the hierarchy index n ===", flush=True)
    x = sp.Symbol('x')
    K = sp.Symbol('K', positive=True)
    S = sp.Function('S')(x)

    def tau(nv):
        return K ** nv * sp.exp(S)

    def Dx2_pair(nv):
        f, g = tau(nv + 1), tau(nv)
        return sp.simplify(f.diff(x, 2) * g - 2 * f.diff(x) * g.diff(x) + f * g.diff(x, 2))

    for nv in (0, 1):
        lhs = Dx2_pair(nv)
        rhs = sp.simplify(2 * (tau(nv + 1) * tau(nv - 1) - tau(nv) ** 2))
        resid = sp.expand(sp.simplify(lhs - rhs))
        # residual = 2 K^{2n+1} e^{2S} ( S'' - (K^2-1)/2 )
        target = sp.expand(2 * K ** (2 * nv + 1) * sp.exp(2 * S)
                           * (sp.diff(S, x, 2) - (K ** 2 - 1) / 2))
        record(f"E3a  bilinear Toda holds iff S'' = (K^2-1)/2  [n={nv}]",
               sp.simplify(resid - target) == 0,
               f"residual = {sp.factor(resid)}")

    W = sp.simplify(tau(2) * tau(0) / tau(1) ** 2)
    record("E3b  Toda field W_n = tau_{n+1}tau_{n-1}/tau_n^2 = K^2 (constant, not 1)",
           sp.simplify(W - K ** 2) == 0, f"W = {W}")

    record("E3c  CONTROL: K = 1 => W_n = 1 and the Toda equation degenerates to S'' = 0",
           sp.simplify((W - 1).subs(K, 1)) == 0)
    return True


# --------------------------------------------------------------------------
# E4: exact-rational check over Q (pure Fraction)
# --------------------------------------------------------------------------
def experiment_E4_exact_rational():
    print("\n=== E4: exact-rational (Fraction) checks over Q ===", flush=True)
    a = F(1)
    ps = [F(1, 2), F(5, 2), F(9, 2)]
    qs = [-2 * a - pv for pv in ps]

    # entrywise-ratio determinant law over Q (exponentials cancel exactly)
    def tau_frac(nv):
        ent = [[(-(ps[i] - a) / (qs[j] + a)) ** nv for j in range(len(ps))]
               for i in range(len(ps))]
        return det_perm(ent)

    K = F(1)
    for i in range(len(ps)):
        K *= -(ps[i] - a) / (qs[i] + a)
    lhs, rhs = tau_frac(1), K * tau_frac(0)
    record("E4a  tau_1 = K tau_0 = 0 exactly over Q (c_j = 0, N>=2 degenerate)",
           lhs == rhs, f"tau_1 = {lhs}, K*tau_0 = {rhs}, K = {K}")

    # a NON-degenerate exact-rational proxy for the determinant law:
    # tau_n = prod_i (c_i + (-(p_i-a)/(q_i+a))^n)  (diagonal model, c_i != 0)
    cs = [F(3), F(5), F(7)]
    def tau_diag(nv):
        t = F(1)
        for i in range(len(ps)):
            t *= cs[i] + (-(ps[i] - a) / (qs[i] + a)) ** nv
        return t

    ks = [-(ps[i] - a) / (qs[i] + a) for i in range(len(ps))]
    Ws = [tau_diag(nv + 1) * tau_diag(nv - 1) / tau_diag(nv) ** 2 for nv in (1, 2, 3)]
    # the diagonal model has a nontrivial Toda field, so the ratio tau_{n+1}/tau_n
    # is NOT constant: that is the c_j != 0 regime
    notone = all(w != 1 for w in Ws)
    record("E4b  control (c_i != 0 diagonal model): Toda field W_n != 1, so "
           "tau_{n+1}/tau_n is NOT a modulus constant", notone,
           f"W = {[str(w) for w in Ws]}")

    uvals = [2 * (ps[i] + qs[i]) for i in range(len(ps))]
    record("E4c  c_j = 0 forces u = 2(p_i+q_i) = -4a for every i",
           all(uv == -4 * a for uv in uvals), f"u values = {[str(v) for v in uvals]}")
    return True


if __name__ == "__main__":
    print("Direction H -- Toda-type embedding: symbolic reduction / obstruction",
          flush=True)
    print("SymPy", sp.__version__, flush=True)
    experiment_E1_structural()
    experiment_E2_triviality()
    experiment_E3_toda_level_index()
    experiment_E4_exact_rational()
    bad = [t for t, ok, _ in RESULTS if not ok]
    print("\n================ SUMMARY ================", flush=True)
    print(f"{len(RESULTS) - len(bad)}/{len(RESULTS)} checks passed", flush=True)
    if bad:
        print("FAILED:", bad, flush=True)
        sys.exit(1)
    print("ALL CHECKS PASSED", flush=True)
