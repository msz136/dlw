# -*- coding: utf-8 -*-
"""verdict7.py -- 符号判定 (7) 对 N=1 tau 是否恒成立。"""
import sympy as sp

x, t, y = sp.symbols('x t y', real=True)


def bilin(F, G, mx=0, mt=0):
    tot = 0
    for i in range(mx + 1):
        for j in range(mt + 1):
            tot += (-1) ** (i + j) * sp.binomial(mx, i) * sp.binomial(mt, j) \
                * sp.diff(F, x, mx - i, t, mt - j) * sp.diff(G, x, i, t, j)
    return sp.expand(tot)


def run(a, p, q, label):
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (p - a) + 1 / (q + a)
    cF = (-(p - a) / (q + a)) / (p + q)
    cG = 1 / (p + q)
    E = sp.exp(S * x + R * t + T * y)
    F = 1 + cF * E
    G = 1 + cG * E
    B = sp.expand(bilin(F, G, 2, 0) + bilin(F, G, 0, 1) + 2 * a * bilin(F, G, 1, 0))
    ratio = sp.simplify(B / E)
    print("--- %s" % label)
    print("    S=%s  R=%s" % (S, R))
    print("    cF=%s  cG=%s  cF+cG=%s" % (cF, cG, sp.simplify(cF + cG)))
    print("    S^2+R+2aS = %s" % sp.simplify(S ** 2 + R + 2 * a * S))
    print("    B_a(F,G)/E = %s" % sp.simplify(ratio))
    print("    B_a(F,G) 恒为 0 ? %s" % (sp.simplify(B) == 0))
    print()


run(sp.Integer(4), sp.Rational(2, 3), sp.Rational(-18, 5), "a=4 p=2/3 q=-18/5")
run(sp.Integer(-2), sp.Integer(1), sp.Integer(-2), "a=-2 p=1 q=-2")
run(sp.Integer(1), sp.Rational(1, 2), sp.Rational(-3, 2), "a=1 p=1/2 q=-3/2")
run(sp.Integer(4), sp.Rational(2, 3), sp.Rational(2, 3) + sp.Integer(8),
    "a=4 p=2/3 q=2/3+8 (=q+2a)")
