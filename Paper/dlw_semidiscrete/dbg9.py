# -*- coding: utf-8 -*-
"""dbg9.py -- 用 sympy 逐步拆解 B_lam F.G 的系数（N=1），彻底定位。"""
import sympy as sp

x, t = sp.symbols('x t', real=True)
pv = sp.Rational(2, 3)
qv = sp.Rational(-18, 5)
av = sp.Integer(4)
dv = sp.Rational(1, 8)
eta = (pv + qv) * x + (qv ** 2 - pv ** 2) * t


def coef(n, ss):
    return (-(pv - ss) / (qv + ss)) ** n / (pv + qv)


for (nm, lam, sF) in [('(a-d, a-d)', av - dv, av - dv), ('(a, a)', av, av),
                      ('(a, a-d)', av, av - dv)]:
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

    R = sp.expand(Dx2(F, G) + Dt(F, G) + 2 * lam * Dx(F, G))
    R = sp.expand(R)
    pol = sp.Poly(R, sp.exp(eta))
    print("\n=== lam=%s sF=%s ===" % (sp.nsimplify(lam), sp.nsimplify(sF)))
    print("  cF =", sp.nsimplify(cF), " cG =", sp.nsimplify(cG))
    print("  R =", R)
    print("  系数 e^0 :", sp.nsimplify(R.coeff(sp.exp(eta), 0)))
    print("  系数 e^1 :", sp.nsimplify(R.coeff(sp.exp(eta), 1)))
    print("  系数 e^2 :", sp.nsimplify(R.coeff(sp.exp(eta), 2)))
    print("  R(0,0) =", sp.nsimplify(R.subs({x: 0, t: 0})))
