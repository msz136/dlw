# -*- coding: utf-8 -*-
"""
audit_gauge.py -- 对 N=1 单孤子，把 tau 的相位常数 xi0, eta0 作为未知量，
                  同时要求 (7) 与 (6) 成立，解出规范约束。

tau_f: n=1 分量   tau_g: n=0 分量
   f = 1 + cF e^{kF.z + s0},  g = 1 + cG e^{kG.z + s0},   s0 = xi0 + eta0
(7):  B_a f.g = 0
(6):  [D_y B_a + 2λ D_x] f.g = B_a f.g_y + 2λ D_x f.g = 0
"""
import sympy as sp

x, t, y = sp.symbols('x t y', real=True)
A = sp.symbols('A', real=True)      # a
E0 = sp.symbols('E0', positive=True)   # e^{s0}
lam = sp.Integer(-2)

p, q = sp.symbols('p q', real=True)
n = 1


def keys_and_coef(sgn):
    """sgn = -1 -> f (n=1, 用 p-a / q+a) ;  sgn 用于 g (n=0)"""
    raise SystemExit


def make(nval, aa, pp, qq):
    P = pp - aa
    Q = qq + aa
    c = (-P / Q) ** nval / (pp + qq)
    S = pp + qq
    R = qq ** 2 - pp ** 2
    T = 1 / P + 1 / Q
    return c, (S, R, T)


def bilin(F, G, mx=0, mt=0, my=0):
    tot = 0
    for i in range(mx + 1):
        for j in range(mt + 1):
            for l in range(my + 1):
                co = (-1) ** (i + j + l) * sp.binomial(mx, i) * sp.binomial(mt, j) \
                    * sp.binomial(my, l)
                tot += co * sp.diff(F, x, mx - i, t, mt - j, y, my - l) \
                    * sp.diff(G, x, i, t, j, y, l)
    return sp.expand(tot)


def audit(aa, pp, qq, name):
    cF, kF = make(1, aa, pp, qq)
    cG, kG = make(0, aa, pp, qq)
    EF = sp.exp(kF[0] * x + kF[1] * t + kF[2] * y)
    EG = sp.exp(kG[0] * x + kG[1] * t + kG[2] * y)
    f = 1 + cF * E0 * EF
    g = 1 + cG * E0 * EG
    r7 = sp.expand(bilin(f, g, 2, 0) + bilin(f, g, 0, 1) + 2 * aa * bilin(f, g, 1, 0))
    r6 = sp.expand(bilin(f, sp.diff(g, y), 2, 0) + bilin(f, sp.diff(g, y), 0, 1)
                   + 2 * aa * bilin(f, sp.diff(g, y), 1, 0)
                   + 2 * lam * bilin(f, g, 1, 0))
    # 化到基 {1, EF, EG, EF*EG}
    Fs, Gs = sp.symbols('Fs Gs')
    def to_basis(expr):
        e = sp.expand(expr)
        e = e.subs({EF: Fs, EG: Gs})
        e = e.subs({sp.exp(2 * (kF[0] * x + kF[1] * t + kF[2] * y)): Fs ** 2,
                    sp.exp(2 * (kG[0] * x + kG[1] * t + kG[2] * y)): Gs ** 2,
                    sp.exp((kF[0] + kG[0]) * x + (kF[1] + kG[1]) * t
                           + (kF[2] + kG[2]) * y): Fs * Gs})
        return sp.expand(e)
    e7, e6 = to_basis(r7), to_basis(r6)
    print("=" * 72)
    print(name, "  a=%s p=%s q=%s" % (aa, pp, qq))
    print("  cF =", sp.simplify(cF), "  cG =", sp.simplify(cG))
    for nm, e in (("(7)", e7), ("(6)", e6)):
        c1 = sp.simplify(e.subs({Fs: 0, Gs: 0}))
        cF_ = sp.simplify(e.coeff(Fs).subs(Gs, 0))
        cG_ = sp.simplify(e.coeff(Gs).subs(Fs, 0))
        cFG = sp.simplify(e.coeff(Fs * Gs))
        print("  %s 系数: 1->%s  F->%s  G->%s  FG->%s"
              % (nm, c1, cF_, cG_, cFG))
        if nm == "(6)":
            # 对 E0 解 F 分量 = 0
            s = sp.solve(sp.numer(sp.together(cF_)), E0)
            print("      使 F 分量=0 的 E0 解:", [sp.simplify(z) for z in s])


audit(sp.Integer(4), sp.Rational(2, 3), sp.Rational(-18, 5), "N=1 算例A")
audit(sp.Integer(-2), sp.Integer(1), sp.Integer(-2), "N=1 算例B")
audit(sp.Integer(1), sp.Rational(1, 2), sp.Rational(-3, 2), "N=1 算例C (a=1)")
