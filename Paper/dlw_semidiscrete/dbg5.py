# -*- coding: utf-8 -*-
"""dbg5.py -- 从论文 Gram tau 直接推出 N=1 的 bilinear 条件，核对系数公式。"""
import sympy as sp

x, t, y = sp.symbols('x y t', real=True)
p, q, a, s, n = sp.symbols('p q a s n', real=True)


def tau_coef(nval, sval):
    """m_00 = 1 + coef * exp(eta)，eta = (p+q)x + (q^2-p^2)t + y(1/(p-a)+1/(q+a))"""
    return (-(p - sval) / (q + sval)) ** nval / (p + q)


eta = (p + q) * x + (q ** 2 - p ** 2) * t + y * (1 / (p - a) + 1 / (q + a))


def B(F, G, lam):
    return (sp.diff(F, x, 2) * G - 2 * sp.diff(F, x) * sp.diff(G, x) + F * sp.diff(G, x, 2)
            + sp.diff(F, t) * G - F * sp.diff(G, t) + 2 * lam * (sp.diff(F, x) * G - F * sp.diff(G, x)))


for (nF, nG, lam, sF, sG) in [
    (1, 0, a, s, a),
    (1, 0, (s + a) / 2, s, a),
]:
    cF = tau_coef(nF, sF)
    cG = tau_coef(nG, sG)
    F = 1 + cF * sp.exp(eta)
    G = 1 + cG * sp.exp(eta)
    R = sp.expand(B(F, G, lam))
    R = sp.collect(sp.expand(R), sp.exp(eta))
    print("\n--- nF=%s nG=%s  lam=%s  sF=%s ---" % (nF, nG, lam, sF))
    print("系数 of e^eta :", sp.simplify(R.coeff(sp.exp(eta), 1)))
    print("系数 of e^2eta:", sp.simplify(R.coeff(sp.exp(eta), 2)))
