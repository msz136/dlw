# -*- coding: utf-8 -*-
"""dbg3.py -- 用 J2 jet 逐项与真 tau 比较，定位 (7)_h 的残差来源。"""
import mpmath as mp
from itertools import permutations

import jet2
import taujet2
from jet2 import J2
jet2.MX = 6
jet2.MT = 4
taujet2.MX = 6
taujet2.MT = 4
from taujet2 import Tau2

mp.mp.dps = 60
X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7

N = 1
a = mp.mpf(6)
p = [mp.mpf(1)]
q = [mp.mpf(-11) / 2]
h = mp.mpf(1) / 4
j = 1


def tau_scalar(n, jj, s, mu, x0, t0):
    ent = {}
    for i in range(N):
        for k in range(N):
            coef = (-(p[i] - s) / (q[k] + s)) ** n / (p[i] + q[k])
            if jj:
                d = h / 2
                lp = (p[i] - a + d) / (p[i] - a - d)
                lq = (q[k] + a + d) / (q[k] + a - d)
                coef = coef * (lp * lq) ** jj
            c0 = (p[i] * x0 - p[i] ** 2 * t0) + (q[k] * x0 + q[k] ** 2 * t0)
            e = coef * mp.e ** c0
            if i == k:
                e = e + 1
            ent[(i, k)] = e
    tot = mp.mpf(0)
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for ii in range(N):
            for jj2 in range(ii + 1, N):
                if pl[ii] > pl[jj2]:
                    sign = -sign
        t = mp.mpf(sign)
        for i in range(N):
            t *= ent[(i, perm[i])]
        tot += t
    return tot


T = Tau2(N, a, p, q, h)


def jet_derivs(n, s, mu, jj, order_x, order_t):
    """返回真 tau 的偏导 (d/dx)^mx (d/dt)^mt tau（由 jet 反推）。"""
    jt = T.tau(n, jj, s, mu, X0, T0)
    t0v = tau_scalar(n, jj, s, mu, X0, T0)
    C = jt.coef(0, 0) / t0v
    return jt, C


# F 与 G
Fj, Cf = jet_derivs(1, a - h / 2, a, j, 0, 0)
Gj, Cg = jet_derivs(0, a, a, j, 0, 0)
G1j, Cg1 = jet_derivs(0, a, a, j + 1, 0, 0)


def deriv(J, C, mx, mt):
    return J.coef(mx, mt) * mp.factorial(mx) * mp.factorial(mt) / C


F = lambda mx, mt: deriv(Fj, Cf, mx, mt)
G = lambda mx, mt: deriv(Gj, Cg, mx, mt)
G1 = lambda mx, mt: deriv(G1j, Cg1, mx, mt)

print("F   =", mp.nstr(F(0, 0), 12), " F_x =", mp.nstr(F(1, 0), 12),
      " F_xx =", mp.nstr(F(2, 0), 12), " F_t =", mp.nstr(F(0, 1), 12))
print("G   =", mp.nstr(G(0, 0), 12), " G_x =", mp.nstr(G(1, 0), 12),
      " G_xx =", mp.nstr(G(2, 0), 12), " G_t =", mp.nstr(G(0, 1), 12))

Dx2 = F(2, 0) * G(0, 0) - 2 * F(1, 0) * G(1, 0) + F(0, 0) * G(2, 0)
Dt = F(0, 1) * G(0, 0) - F(0, 0) * G(0, 1)
Dx = F(1, 0) * G(0, 0) - F(0, 0) * G(1, 0)
s7 = a - h / 2
print("\nDx2 =", mp.nstr(Dx2, 12))
print("Dt  =", mp.nstr(Dt, 12))
print("2sDx=", mp.nstr(2 * s7 * Dx, 12))
print("(7)_h =", mp.nstr(Dx2 + Dt + 2 * s7 * Dx, 12))

s6 = a + h / 2
Dx2b = F(2, 0) * G1(0, 0) - 2 * F(1, 0) * G1(1, 0) + F(0, 0) * G1(2, 0)
Dtb = F(0, 1) * G1(0, 0) - F(0, 0) * G1(0, 1)
Dxb = F(1, 0) * G1(0, 0) - F(0, 0) * G1(1, 0)
print("(6)_h =", mp.nstr(Dx2b + Dtb + 2 * s6 * Dxb, 12))

# 直接用真 tau 的解析式（N=1 显式）做同一计算
import sympy as sp
x, t = sp.symbols('x t', real=True)
P = sp.Rational(1) - sp.Rational(6)
Q = sp.Rational(-11, 2) + sp.Rational(6)
d = sp.Rational(1, 8)
lp = (sp.Rational(1) - 6 + d) / (sp.Rational(1) - 6 - d)
lq = (sp.Rational(-11, 2) + 6 + d) / (sp.Rational(-11, 2) + 6 - d)
chi = lp * lq
SO = (sp.Rational(1) - sp.Rational(11, 2)) * x - (sp.Rational(1) ** 2 - sp.Rational(-11, 2) ** 2) * t
# 注意：相位 = (p+q)x + (q^2-p^2)t
SO = (sp.Rational(1) + sp.Rational(-11, 2)) * x + (sp.Rational(-11, 2) ** 2 - 1) * t
cF = (-(sp.Rational(1) - (sp.Rational(6) - d)) / (sp.Rational(-11, 2) + (sp.Rational(6) - d))) / (sp.Rational(1) + sp.Rational(-11, 2)) * chi ** j
cG = (1 / (sp.Rational(1) + sp.Rational(-11, 2))) * chi ** j
Fs = 1 + cF * sp.exp(SO)
Gs = 1 + cG * sp.exp(SO)
Dx2s = sp.diff(Fs, x, 2) * Gs - 2 * sp.diff(Fs, x) * sp.diff(Gs, x) + Fs * sp.diff(Gs, x, 2)
Dts = sp.diff(Fs, t) * Gs - Fs * sp.diff(Gs, t)
Dxs = sp.diff(Fs, x) * Gs - Fs * sp.diff(Gs, x)
res = sp.simplify(Dx2s + Dts + 2 * (sp.Rational(6) - d) * Dxs)
print("\n符号 (7)_h =", res)
print("数值 (7)_h at (x0,t0) =", sp.N(res.subs({x: sp.Rational(1, 5), t: sp.Rational(2, 7)}), 20))
