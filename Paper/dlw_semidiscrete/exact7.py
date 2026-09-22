# -*- coding: utf-8 -*-
"""
exact7.py -- 用 sympy 精确算出 B_a(F,G) 的闭式（不代换 exp，保留符号）。
F = 1 + cF E, G = 1 + cG E, E = exp(Sx+Rt+Ty)。
"""
import sympy as sp

x, t, y = sp.symbols('x t y', real=True)
S, R, T = sp.symbols('S R T', real=True)
a = sp.Integer(4)
cF, cG = sp.symbols('cF cG', real=True)

E = sp.exp(S * x + R * t + T * y)
F = 1 + cF * E
G = 1 + cG * E


def bilin(F, G, mx=0, mt=0):
    tot = 0
    for i in range(mx + 1):
        for j in range(mt + 1):
            tot += (-1) ** (i + j) * sp.binomial(mx, i) * sp.binomial(mt, j) \
                * sp.diff(F, x, mx - i, t, mt - j) * sp.diff(G, x, i, t, j)
    return sp.expand(tot)


B = sp.expand(bilin(F, G, 2, 0) + bilin(F, G, 0, 1) + 2 * a * bilin(F, G, 1, 0))
print("B_a(F,G) 展开（作为 E 的多项式）:")
print("  ", sp.collect(B, E))
print()
# 用符号 dE 替换 exp 与 exp^2 太麻烦；直接看 E 的幂次结构
E2 = sp.exp(2 * (S * x + R * t + T * y))
poly = sp.Poly(B, E, E2) if False else None
# 手写：按 E^2, E 分组
c2 = sp.simplify(B.coeff(E2) * 1 if False else 0)
Bsub = B.subs({E2: sp.Symbol('EE2'), E: sp.Symbol('EE')})
print()
print("按 E^2 / E 分组：")
EE2, EE = sp.symbols('EE2 EE')
Bsub2 = sp.expand(B.subs({sp.exp(2 * (S * x + R * t + T * y)): EE2,
                          sp.exp(S * x + R * t + T * y): EE}))
print("  [E^2] =", sp.simplify(Bsub2.coeff(EE2)))
print("  [E]   =", sp.simplify(Bsub2.coeff(EE).subs(EE2, 0)))
print()
print("代入 cF, cG, S, R 的具体值：")
subs = {cF: sp.Rational(-125, 44), cG: sp.Rational(-15, 44),
        S: sp.Rational(-44, 15), R: sp.Rational(2816, 225),
        T: sp.Rational(11, 5)}
print("  [E^2] =", sp.simplify(Bsub2.coeff(EE2).subs(subs)))
print("  [E]   =", sp.simplify(Bsub2.coeff(EE).subs(EE2, 0).subs(subs)))
