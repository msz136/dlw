# -*- coding: utf-8 -*-
"""dbg10.py -- 用已验证的泰勒系数直接算 B_lam F.G（不做任何符号化简）。"""
import sympy as sp

x, t = sp.symbols('x t', real=True)
pv = sp.Rational(2, 3)
qv = sp.Rational(-18, 5)
av = sp.Integer(4)
dv = sp.Rational(1, 8)
s = pv + qv
r = qv ** 2 - pv ** 2
lam = av - dv
sF = av - dv


def coef(n, ss):
    return (-(pv - ss) / (qv + ss)) ** n / (pv + qv)


cF = coef(1, sF)
cG = coef(0, av)
print("s =", s, " r =", r, " lam =", lam, " sF =", sF)
print("cF =", cF, " cG =", cG)
print("cF+cG+2cFcG =", sp.nsimplify(cF + cG + 2 * cF * cG))
P1 = s ** 2 + r + 2 * lam * s
print("P1 = s^2+r+2 lam s =", sp.nsimplify(P1))
print("P1*(1+cF)*(1+cG) =", sp.nsimplify(P1 * (1 + cF) * (1 + cG)))

# 直接按定义算：B = (d_x^2 + d_t + 2 lam d_x)(F G)
FG = (1 + cF * sp.exp(s * x + r * t)) * (1 + cG * sp.exp(s * x + r * t))
B = sp.diff(FG, x, 2) + sp.diff(FG, t) + 2 * lam * sp.diff(FG, x)
print("\nB(FG) =", sp.simplify(B))
print("B(FG) at 0 =", sp.nsimplify(B.subs({x: 0, t: 0})))
print("B(FG) expanded =", sp.expand(B))

# 手写 Hirota 形式
Dx2 = sp.diff(1 + cF * sp.exp(s * x + r * t), x, 2) * (1 + cG * sp.exp(s * x + r * t)) \
    - 2 * sp.diff(1 + cF * sp.exp(s * x + r * t), x) * sp.diff(1 + cG * sp.exp(s * x + r * t), x) \
    + (1 + cF * sp.exp(s * x + r * t)) * sp.diff(1 + cG * sp.exp(s * x + r * t), x, 2)
print("\nHirota Dx2 =", sp.simplify(Dx2))
