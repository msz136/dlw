# -*- coding: utf-8 -*-
"""dbg6.py -- 数值代入核对 N=1 的 bilinear 条件（排除符号化简的假象）。"""
import sympy as sp

x, t, y = sp.symbols('x y t', real=True)

# 参数（与 dbg4 一致）
pv = sp.Rational(2, 3)
qv = sp.Rational(-18, 5)
av = sp.Rational(4)
hv = sp.Rational(1, 4)
dv = hv / 2
jv = 1
# (7)_h： lam = a-d, sF = a-d, sG = a
lam = av - dv
sF = av - dv
sG = av


def coef(n, s):
    return (-(pv - s) / (qv + s)) ** n / (pv + qv)


eta = (pv + qv) * x + (qv ** 2 - pv ** 2) * t
cF = coef(1, sF)
cG = coef(0, sG)
F = 1 + cF * sp.exp(eta)
G = 1 + cG * sp.exp(eta)


def B(F, G, lam):
    return (sp.diff(F, x, 2) * G - 2 * sp.diff(F, x) * sp.diff(G, x) + F * sp.diff(G, x, 2)
            + sp.diff(F, t) * G - F * sp.diff(G, t) + 2 * lam * (sp.diff(F, x) * G - F * sp.diff(G, x)))


R = sp.expand(B(F, G, lam))
print("cF =", sp.nsimplify(cF), "=", sp.N(cF, 10))
print("cG =", sp.nsimplify(cG), "=", sp.N(cG, 10))
print("P1 = s^2+r+2 lam s =",
      sp.nsimplify((pv + qv) ** 2 + (qv ** 2 - pv ** 2) + 2 * lam * (pv + qv)))
print("R =", sp.simplify(R))
print("R 的 e^eta 系数 =", sp.simplify(R.coeff(sp.exp(eta), 1)))
print("R 的 e^2eta 系数 =", sp.simplify(R.coeff(sp.exp(eta), 2)))
print("常数项 =", sp.simplify(R.coeff(sp.exp(eta), 0)))
print("P1*(cF+cG+2cFcG) =", sp.nsimplify(
    ((pv + qv) ** 2 + (qv ** 2 - pv ** 2) + 2 * lam * (pv + qv)) * (cF + cG + 2 * cF * cG)))
