#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN-AGENT INDEPENDENT VERIFICATION of the DLW / staggered-tau core mathematics.

Run:  python -u common/MAIN_verify_core.py [section ...]
      sections: v2 v3 v4 v5 v6 v7 v8 v9 v10   (default: all)
Deps: sympy only.

Fast-algebra conventions used here:
  * bilinear residuals are always reduced by clearing denominators
    (together -> fraction -> expand numerator) instead of `simplify`;
  * exponentials of linear forms with NUMERIC coefficients are replaced by
    fresh symbols keyed on their (kx, wy, wt, const) data, so that a residual
    which is a finite sum of exponentials becomes an ordinary polynomial
    identity -- this is exact, not a numerical sample.
"""

import itertools
import random
import sys

import sympy as sp

FAIL = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""), flush=True)
    if not ok:
        FAIL.append(name)


def is_zero(expr, syms=()):
    """Exact zero test for rational expressions in syms (clear denominators)."""
    e = sp.together(sp.expand(expr))
    num, den = sp.fraction(e)
    num = sp.expand(num)
    if num == 0:
        return True
    if syms:
        try:
            return sp.Poly(num, *syms).is_zero
        except Exception:
            pass
    return num == 0


# ----------------------------------------------------------------------------
# V1/V2  Hirota bilinear operators and the key operator identity
# ----------------------------------------------------------------------------
def bilinear(f, g, xs, powers):
    x, y, t = xs
    a, b, c = powers
    total = 0
    for p in range(a + 1):
        for q in range(b + 1):
            for r in range(c + 1):
                coef = (-1) ** (p + q + r) * sp.binomial(a, p) * sp.binomial(b, q) * sp.binomial(c, r)
                total += coef * sp.diff(f, x, a - p, y, b - q, t, c - r) \
                    * sp.diff(g, x, p, y, q, t, r)
    return sp.expand(total)


def Bop(f, g, xs, ac):
    return sp.expand(bilinear(f, g, xs, (2, 0, 0)) + bilinear(f, g, xs, (0, 0, 1))
                     + 2 * ac * bilinear(f, g, xs, (1, 0, 0)))


def DyB(f, g, xs, ac):
    return sp.expand(bilinear(f, g, xs, (2, 1, 0)) + bilinear(f, g, xs, (0, 1, 1))
                     + 2 * ac * bilinear(f, g, xs, (1, 1, 0)))


def v2():
    x, y, t = sp.symbols("x y t")
    xs = (x, y, t)
    f = sp.Function("f")(x, y, t)
    g = sp.Function("g")(x, y, t)
    ok = True
    for powers in [(0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 0, 1), (1, 1, 0), (0, 1, 0)]:
        lhs = bilinear(f, g, xs, (powers[0], powers[1] + 1, powers[2]))
        inner = bilinear(f, g, xs, powers)
        rhs = sp.expand(sp.diff(inner, y) - 2 * bilinear(f, sp.diff(g, y), xs, powers))
        if sp.expand(lhs - rhs) != 0:
            ok = False
            print("   mismatch at powers", powers, lhs - rhs, flush=True)
    check("V2  D_y(P f.g) = d_y(P f.g) - 2 P(f.g_y)  for all tested P "
          "(P = 1,Dx,Dx^2,Dt,DxDy,Dy)", ok)
    return ok


def v3():
    x, y, t = sp.symbols("x y t")
    xs = (x, y, t)
    ac = sp.Integer(2)
    f = sp.Function("f")(x, y, t)
    g = sp.Function("g")(x, y, t)
    lhs = sp.expand(DyB(f, g, xs, ac) - 4 * bilinear(f, g, xs, (1, 0, 0)))
    C = sp.expand(Bop(f, sp.diff(g, y), xs, ac) + 2 * bilinear(f, g, xs, (1, 0, 0)))
    ident = sp.expand(lhs + 2 * C - sp.diff(Bop(f, g, xs, ac), y))
    check("V3  (D_yB-4D_x)f.g + 2[B f.g_y + 2 D_x f.g] = d_y(B f.g)  "
          "=> on {B f.g=0}: (paper eq.6, lam=-2) <=> [B f.g_y + 2 D_x f.g = 0]", ident == 0)
    return ident == 0


# ----------------------------------------------------------------------------
# V4  Sheng-Yu tau functions
# ----------------------------------------------------------------------------
def exp_to_symbols(expr, xs):
    """Replace every exp(linear in xs) by a fresh symbol keyed on its data."""
    x, y, t = xs
    subs = {}
    for at in expr.atoms(sp.exp):
        arg = sp.expand(at.args[0])
        key = tuple(sp.expand(sp.diff(arg, v)) for v in xs) + (arg.subs({x: 0, y: 0, t: 0}),)
        sym = sp.Symbol("E_" + "_".join(str(sp.nsimplify(k)) for k in key).replace("-", "m").replace("/", "d"))
        subs[at] = sym
    return sp.expand(expr.subs(subs, simultaneous=True))


def tau(n, ps, qs, cs, a, x, y, t, xis, etas):
    N = len(ps)
    M = sp.zeros(N, N)
    for i in range(N):
        for j in range(N):
            xi = ps[i] * x - ps[i] ** 2 * t + y / (ps[i] - a) + xis[i]
            eta = qs[j] * x + qs[j] ** 2 * t + y / (qs[j] + a) + etas[j]
            M[i, j] = cs[j] * (1 if i == j else 0) \
                + (-(ps[i] - a) / (qs[j] + a)) ** n * sp.exp(xi + eta) / (ps[i] + qs[j])
    return sp.expand(M.det())


def v4():
    x, y, t = sp.symbols("x y t")
    xs = (x, y, t)
    a, lam = sp.Integer(2), sp.Integer(-2)
    rng = random.Random(20260917)
    allok = True
    for N in (1, 2, 3):
        # GUARD (added after a false negative): the paper's Gram data (13) contains the
        # SINGULAR SHIFTS p_i - a and q_j + a (the paper itself calls them "the singular
        # shift" in Remark 2.1).  A draw with p_i = a makes y/(p_i - a) a division by zero
        # and gamma = -(p_i-a)/(q_j+a) = 0, so tau degenerates and (6) legitimately fails.
        # The first version of this check had NO guard: the N=1 draw (p=[5]) was fine but
        # the N=2 draw (p=[1,2], a = 2) hit p_2 = a and produced a spurious failure.
        # Likewise q_j = -a must be excluded.
        def draw_p():
            while True:
                v = sp.Integer(rng.randint(1, 5))
                if v != a:
                    return v

        def draw_q():
            while True:
                v = sp.Integer(rng.randint(1, 6))
                if v != -a:
                    return v

        ps = [draw_p() for _ in range(N)]
        qs = [draw_q() for _ in range(N)]
        cs = [sp.Integer(1)] * N
        xis = [sp.Rational(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(N)]
        etas = [sp.Rational(rng.randint(-3, 3), rng.randint(1, 4)) for _ in range(N)]
        f = tau(1, ps, qs, cs, a, x, y, t, xis, etas)
        g = tau(0, ps, qs, cs, a, x, y, t, xis, etas)
        e6 = exp_to_symbols(sp.expand(DyB(f, g, xs, a) - 4 * bilinear(f, g, xs, (1, 0, 0))), xs)
        e7 = exp_to_symbols(sp.expand(Bop(f, g, xs, a)), xs)
        u = 2 * sp.diff(sp.log(f / g), x)
        v = 2 * sp.diff(sp.log(f * g), x, y)
        n1 = sp.expand(sp.diff(u, y, t) + sp.diff(v, x, 2) + u * sp.diff(u, x, y)
                       + sp.diff(u, x) * sp.diff(u, y) + 2 * a * sp.diff(u, x, y))
        n2 = sp.expand(sp.diff(v, t) + sp.diff(u * v, x) + sp.diff(u, x, 2, y)
                       + 2 * a * sp.diff(v, x) + 2 * lam * sp.diff(u, x))
        ok = is_zero(e6) and is_zero(e7) and is_zero(n1) and is_zero(n2)
        allok &= bool(ok)
        print(f"      N={N} p={ps} q={qs}: eq6={is_zero(e6)} eq7={is_zero(e7)} "
              f"eq1={is_zero(n1)} eq2={is_zero(n2)}", flush=True)
    check("V4  tau_n (n=0,1) solve paper (6),(7) and (u,v) solve (1),(2)  [N=1,2,3]", allok)
    return allok


# ----------------------------------------------------------------------------
# V5  w = u_y reformulation
# ----------------------------------------------------------------------------
def v5():
    x, y, t = sp.symbols("x y t")
    a, lam = sp.symbols("a lambda")
    u = sp.Function("u")(x, y, t)
    v = sp.Function("v")(x, y, t)
    w = sp.diff(u, y)
    n1 = (sp.diff(u, y, t) + sp.diff(v, x, 2) + u * sp.diff(u, x, y)
          + sp.diff(u, x) * sp.diff(u, y) + 2 * a * sp.diff(u, x, y))
    r1 = sp.diff(w, t) + sp.diff(sp.diff(v, x) + (u + 2 * a) * w, x)
    n2 = (sp.diff(v, t) + sp.diff(u * v, x) + sp.diff(u, x, 2, y)
          + 2 * a * sp.diff(v, x) + 2 * lam * sp.diff(u, x))
    r2 = sp.diff(v, t) + sp.diff((u + 2 * a) * v + sp.diff(w, x) + 2 * lam * u, x)
    ok1 = sp.expand(n1 - r1) == 0
    ok2 = sp.expand(n2 - r2) == 0
    check("V5  w=u_y: (1) == w_t + d_x[v_x+(u+2a)w]", ok1)
    check("V5  w=u_y: (2) == v_t + d_x[(u+2a)v+w_x+2*lam*u]", ok2)
    return ok1 and ok2


# ----------------------------------------------------------------------------
# V6  Linearisation about a constant background
# ----------------------------------------------------------------------------
def v6():
    u0, v0, a, lam, k, l, s = sp.symbols("u0 v0 a lambda k ell sigma")
    uh, vh = sp.symbols("uh vh")
    E1 = sp.expand(uh * (s * sp.I * l + u0 * (sp.I * k) * (sp.I * l) + 2 * a * (sp.I * k) * (sp.I * l))
                   + vh * (sp.I * k) ** 2)
    E2 = sp.expand(uh * (sp.I * k * v0 - sp.I * k ** 2 * l + 2 * lam * sp.I * k)
                   + vh * (s + sp.I * k * u0 + 2 * a * sp.I * k))
    sol = sp.solve(sp.Eq(E1, 0), vh)[0]
    disp = sp.factor(sp.expand(E2.subs(vh, sol) * k ** 2 / (sp.I * uh * l)))
    expected = (s + sp.I * k * (u0 + 2 * a)) ** 2 - k ** 4 + (v0 + 2 * lam) * k ** 3 / l
    ok = sp.expand(disp - expected) == 0
    check("V6  linearisation gives [sigma + i(u0+2a)k]^2 = k^4 - (v0+2*lam) k^3/ell", ok,
          "" if ok else f"got {sp.simplify(disp)}")
    br = sp.solve(sp.Eq((s + sp.I * k * (u0 + 2 * a)) ** 2, k ** 4 - (v0 + 2 * lam) * k ** 3 / l), s)
    print("      two branches sigma =", [sp.simplify(b + sp.I * k * (u0 + 2 * a)) for b in br], flush=True)
    print("      => for real k,ell != 0 and |k| large: |Re(sigma)| ~ k^2  (Hadamard ill-posedness)", flush=True)
    # ell = 0 sector
    E1_0 = sp.expand(E1.subs(l, 0))
    E2_0 = sp.expand(E2.subs(l, 0))
    sols = sp.solve([sp.Eq(E1_0, 0), sp.Eq(E2_0, 0)], [uh, vh], dict=True)
    print("      ell=0 sector solution set:", sols, flush=True)
    return ok


def v7():
    x, y, t = sp.symbols("x y t")
    a, lam = sp.symbols("a lambda")
    U = sp.Function("U")(x, t)
    u, v = U, -2 * lam
    n1 = (sp.diff(u, y, t) + sp.diff(v, x, 2) + u * sp.diff(u, x, y)
          + sp.diff(u, x) * sp.diff(u, y) + 2 * a * sp.diff(u, x, y))
    n2 = (sp.diff(v, t) + sp.diff(u * v, x) + sp.diff(u, x, 2, y)
          + 2 * a * sp.diff(v, x) + 2 * lam * sp.diff(u, x))
    ok = sp.expand(n1) == 0 and sp.expand(n2) == 0
    check("V7  v == -2*lam and u = U(x,t) arbitrary (u_y = 0) is an EXACT solution "
          "=> y-independent zero mode / non-uniqueness", ok)
    return ok


# ----------------------------------------------------------------------------
# V8  Staggered tau system, general-parameter two-soliton coefficients
# ----------------------------------------------------------------------------
def v8():
    p1, p2, q1, q2, a, h = sp.symbols("p1 p2 q1 q2 a h", positive=True)
    d = h / 2
    P = {1: p1 - a, 2: p2 - a}
    Q = {1: q1 + a, 2: q2 + a}
    k = {1: p1 + q1, 2: p2 + q2}
    w = {1: q1 ** 2 - p1 ** 2, 2: q2 ** 2 - p2 ** 2}
    rho = {i: ((P[i] + d) * (Q[i] + d)) / ((P[i] - d) * (Q[i] - d)) for i in (1, 2)}
    rr = {i: -(P[i] + d) / (Q[i] - d) for i in (1, 2)}
    Gamma = ((p1 - p2) * (q1 - q2)) / ((p1 + q1) * (p1 + q2) * (p2 + q1) * (p2 + q2))
    F = {(): sp.Integer(1), (1,): rr[1] / k[1], (2,): rr[2] / k[2], (1, 2): Gamma * rr[1] * rr[2]}
    G0 = {(): sp.Integer(1), (1,): 1 / k[1], (2,): 1 / k[2], (1, 2): Gamma}
    G1 = {(): sp.Integer(1), (1,): rho[1] / k[1], (2,): rho[2] / k[2],
          (1, 2): Gamma * rho[1] * rho[2]}

    def K(S):
        return sum(k[i] for i in S)

    def W(S):
        return sum(w[i] for i in S)

    syms = (p1, p2, q1, q2, a, h)
    allok = True
    for s, G, tag in ((a - d, G0, "eq1: (B-hDx) F_j.G_j"), (a + d, G1, "eq2: (B+hDx) F_j.G_{j+1}")):
        acc = {}
        for SF, cF in F.items():
            for SG, cG in G.items():
                m = tuple(sorted(SF + SG))
                key = (m.count(1), m.count(2))
                dk = K(SF) - K(SG)
                dw = W(SF) - W(SG)
                acc[key] = acc.get(key, 0) + sp.together(cF * cG * (dk ** 2 + dw + 2 * s * dk))
        bad = []
        for key, val in sorted(acc.items()):
            if not is_zero(val, syms):
                bad.append((key, sp.simplify(val)))
        allok &= (len(bad) == 0)
        print(f"      {tag}: 9 monomials E1^m E2^n, nonvanishing = {len(bad)}", flush=True)
        for key, val in bad[:8]:
            print(f"         E1^{key[0]}E2^{key[1]} -> {val}", flush=True)
    check("V8  staggered tau: ALL general-parameter 2-soliton coefficients vanish "
          "(symbolic in p1,p2,q1,q2,a,h)", allok)
    return allok


# ----------------------------------------------------------------------------
# V9  Staggered tau family, exact rational N=1..5
# ----------------------------------------------------------------------------
def v9(trials=4, nmax=5):
    rng = random.Random(4242)
    allok = True
    total = 0
    for _ in range(trials):
        a = sp.Integer(rng.randint(1, 3))
        h = sp.Rational(1, rng.randint(2, 7))
        ps = [sp.Rational(rng.randint(2, 9), rng.randint(1, 3)) for _ in range(nmax)]
        qs = [sp.Rational(rng.randint(2, 9), rng.randint(1, 3)) for _ in range(nmax)]
        for N in range(1, nmax + 1):
            pN, qN = ps[:N], qs[:N]
            xis = [sp.Symbol(f"x{N}_{i}") for i in range(N)]
            etas = [sp.Symbol(f"e{N}_{i}") for i in range(N)]
            d = h / 2
            P = {i: pN[i] - a for i in range(N)}
            Q = {i: qN[i] + a for i in range(N)}
            rho_i = {i: ((P[i] + d) * (Q[i] + d)) / ((P[i] - d) * (Q[i] - d)) for i in range(N)}
            rr_i = {i: -(P[i] + d) / (Q[i] - d) for i in range(N)}
            k = {i: pN[i] + qN[i] for i in range(N)}
            w = {i: qN[i] ** 2 - pN[i] ** 2 for i in range(N)}

            def Gamma(S):
                # The claimed C_S (lean-toda/dlw_staggered_construction.md section 4) is
                #     C_S = prod_{i in S} 1/(p_i+q_i)  *  prod_{i<k} Gamma_{ik},
                #     Gamma_{ik} = (p_i-p_k)(q_i-q_k) / ((p_i+q_k)(p_k+q_i)).
                # The 1/(p_i+q_i) factors are supplied by coef_side below, so this
                # function must return ONLY prod_{i<k} Gamma_{ik}.  An earlier version
                # of this check additionally divided by (p_i+q_i)(p_k+q_k) here, i.e.
                # double-counted, giving an extra prod_i (p_i+q_i)^(|S|-1).  That is why
                # N=1 passed while every N>=2 interaction term failed -- a bug in this
                # checker, not in the construction.  (For |S|=2 the two agree because
                # the claimed Gamma in section 3 already contains both 1/(p_i+q_i).)
                g = sp.Integer(1)
                for i, kk in itertools.combinations(sorted(S), 2):
                    g *= (pN[i] - pN[kk]) * (qN[i] - qN[kk]) / (
                        (pN[i] + qN[kk]) * (pN[kk] + qN[i]))
                return g

            def coef_side(extra, shift):
                out = {}
                for m in range(N + 1):
                    for S in itertools.combinations(range(N), m):
                        S = tuple(sorted(S))
                        c = Gamma(S)
                        for i in S:
                            c /= k[i]
                            c *= extra(i)
                            if shift:
                                c *= rho_i[i]
                        out[S] = c
                return out

            F = coef_side(lambda i: rr_i[i], 0)
            G0 = coef_side(lambda i: sp.Integer(1), 0)
            G1 = coef_side(lambda i: sp.Integer(1), 1)
            for G, sgn, tag in ((G0, -1, "eq1"), (G1, +1, "eq2")):
                s = a + sgn * h / 2
                acc = {}
                for SF, cF in F.items():
                    for SG, cG in G.items():
                        dk = sum(k[i] for i in SF) - sum(k[i] for i in SG)
                        dw = sum(w[i] for i in SF) - sum(w[i] for i in SG)
                        # GROUP BY THE UNION MONOMIAL E_1^m1 ... E_N^mN, NOT by (dk, dw).
                        # Each monomial of the bilinear expansion must vanish separately, and
                        # several (SF,SG) pairs feed the SAME monomial with DIFFERENT dk
                        # (e.g. dk = -k_0 from ((),(0,)) and dk = +k_0 from ((0,),())).
                        # Grouping by (dk,dw) splits one monomial into pieces and manufactures
                        # spurious "nonzero" reports.  This was a genuine bug in the first
                        # version of this check; V8 already groups by the union monomial.
                        key = tuple(sorted(SF + SG))
                        acc[key] = acc.get(key, 0) + cF * cG * (dk ** 2 + dw + 2 * s * dk)
                for key, val in acc.items():
                    total += 1
                    if sp.expand(sp.together(val)) != 0:
                        allok = False
                        print(f"      NONZERO N={N} {tag} key={key} val={sp.simplify(val)}", flush=True)
    check(f"V9  staggered tau family: exact rational N=1..5 x {trials} parameter sets, "
          f"{total} coefficients, all zero, arbitrary theta constants a=1..3, h in (0,1/2)", allok)
    return allok


# ----------------------------------------------------------------------------
# V10  O(h^2) continuum expansion of the normalised centred equations
# ----------------------------------------------------------------------------
def v10():
    h = sp.Symbol("h", positive=True)
    Y = sp.Symbol("Y")
    b = [sp.Function(f"b{i}")(Y) for i in range(6)]
    dl = [sp.Function(f"d{i}")(Y) for i in range(6)]

    def ev(ser, s):
        return sum(ser[i] * s ** i / sp.factorial(i) for i in range(len(ser)))

    Bp, Bm = ev(b, h / 2), ev(b, -h / 2)
    Dp, Dm = ev(dl, h / 2), ev(dl, -h / 2)
    A = sp.expand((Bp + Bm) / 2 + h * (Dp - Dm) / 2)
    C = sp.expand((Bp - Bm) / h + (Dp + Dm))
    # compare order by order up to h^3 (the truncation of the generic Taylor data
    # is itself O(h^4), so only h^0..h^3 are meaningful here)
    A_stated = b[0] + h ** 2 * (b[2] / 8 + dl[1] / 2)
    C_stated = b[1] + 2 * dl[0] + h ** 2 * (b[3] / 24 + dl[2] / 4)
    okA = all(sp.expand(sp.diff(A - A_stated, h, m).subs(h, 0)) == 0 for m in range(4))
    okC = all(sp.expand(sp.diff(C - C_stated, h, m).subs(h, 0)) == 0 for m in range(4))
    check("V10  A_h = Bf.g + h^2(1/8 Bf.g_yy + 1/2 Dx f.g_y) + O(h^4)   (no h^1 term)", okA)
    check("V10  C_h = Bf.g_y + 2 Dx f.g + h^2(1/24 Bf.g_yyy + 1/4 Dx f.g_yy) + O(h^4)", okC)
    return okA and okC


SECTIONS = {"v2": v2, "v3": v3, "v4": v4, "v5": v5, "v6": v6,
            "v7": v7, "v8": v8, "v9": v9, "v10": v10}

if __name__ == "__main__":
    want = sys.argv[1:] or list(SECTIONS)
    print("=" * 78, flush=True)
    print("MAIN-AGENT INDEPENDENT VERIFICATION (DLW y-discretisation programme)", flush=True)
    print("=" * 78, flush=True)
    for name in want:
        print(f"--- {name} ---", flush=True)
        SECTIONS[name]()
    print("-" * 78, flush=True)
    print("FAILURES: " + str(FAIL) if FAIL else "ALL REQUESTED CHECKS PASSED", flush=True)
