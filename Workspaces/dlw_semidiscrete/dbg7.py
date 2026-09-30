# -*- coding: utf-8 -*-
"""dbg7.py -- 显式打印 N=1 双线性恒等式的每个中间量。"""
import sympy as sp

x, t = sp.symbols('x t', real=True)
pv = sp.Rational(2, 3)
qv = sp.Rational(-18, 5)
av = sp.Integer(4)
dv = sp.Rational(1, 8)
eta = (pv + qv) * x + (qv ** 2 - pv ** 2) * t
s = (pv + qv)
r = (qv ** 2 - pv ** 2)


def coef(n, ss):
    return (-(pv - ss) / (qv + ss)) ** n / (pv + qv)


for (lam, sF) in [(av - dv, av - dv)]:
    cF = coef(1, sF)
    cG = coef(0, av)
    F = 1 + cF * sp.exp(eta)
    G = 1 + cG * sp.exp(eta)

    def Dx2(Fa, Ga):
        return sp.diff(Fa, x, 2) * Ga - 2 * sp.diff(Fa, x) * sp.diff(Ga, x) + Fa * sp.diff(Ga, x, 2)

    def Dt(Fa, Ga):
        return sp.diff(Fa, t) * Ga - Fa * sp.diff(Ga, t)

    def Dx(Fa, Ga):
        return sp.diff(Fa, x) * Ga - Fa * sp.diff(Ga, x)

    print("cF =", cF, " cG =", cG)
    print("Dx2 at origin =", sp.simplify(Dx2(F, G).subs({x: 0, t: 0})))
    print("Dt  at origin =", sp.simplify(Dt(F, G).subs({x: 0, t: 0})))
    print("Dx  at origin =", sp.simplify(Dx(F, G).subs({x: 0, t: 0})))
    print("R   at origin =", sp.simplify((Dx2(F, G) + Dt(F, G) + 2 * lam * Dx(F, G)).subs({x: 0, t: 0})))
    # 解析预测
    print("\n s =", sp.nsimplify(s), " r =", sp.nsimplify(r), " lam =", lam)
    print(" P1 = s^2 + r + 2 lam s =", sp.nsimplify(s ** 2 + r + 2 * lam * s))
    print(" cF+cG+2cFcG =", sp.nsimplify(cF + cG + 2 * cF * cG))
    print(" P1*(...) =", sp.nsimplify((s ** 2 + r + 2 * lam * s) * (cF + cG + 2 * cF * cG)))
    print(" 展开 (Dx2+Dt+2lamDx) 的 e^eta 与 e^2eta 系数：")
    R = sp.expand(Dx2(F, G) + Dt(F, G) + 2 * lam * Dx(F, G))
    print("   R =", R)
