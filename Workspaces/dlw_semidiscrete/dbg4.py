# -*- coding: utf-8 -*-
"""dbg4.py -- 用"手工构造的精确 jet"复核 (7)_h，隔离 J2 引擎的问题。"""
import mpmath as mp
from itertools import product

import jet2
import taujet2
from jet2 import J2
jet2.MX = 6
jet2.MT = 6
taujet2.MX = 6
taujet2.MT = 6
from taujet2 import Tau2

mp.mp.dps = 60
X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7
N = 1
a = mp.mpf(5) / 3
p = [mp.mpf(1) / 5]
q = [mp.mpf(-1)]
h = mp.mpf(1) / 4
j = 1
d = h / 2
lp = (p[0] - a + d) / (p[0] - a - d)
lq = (q[0] + a + d) / (q[0] + a - d)
chi = lp * lq
cF = (-(p[0] - (a - d)) / (q[0] + (a - d))) / (p[0] + q[0]) * chi ** j
cG = (1 / (p[0] + q[0])) * chi ** j
wx = p[0] + q[0]
wt = q[0] ** 2 - p[0] ** 2


def jet_from(c):
    """tau = 1 + c exp(wx u + wt v) 的精确 jet"""
    mat = [[mp.mpc(0)] * (jet2.MT + 1) for _ in range(jet2.MX + 1)]
    mat[0][0] = 1 + c
    for m in range(jet2.MX + 1):
        for n in range(jet2.MT + 1):
            if m == 0 and n == 0:
                continue
            mat[m][n] = c * wx ** m / mp.factorial(m) * wt ** n / mp.factorial(n)
    return J2(mat)


Fh = jet_from(cF)
Gh = jet_from(cG)


def Dx2(A, B):
    return A.dxn(2) * B - 2 * A.dx() * B.dx() + A * B.dxn(2)


def Dt(A, B):
    return A.dt() * B - A * B.dt()


def Dx(A, B):
    return A.dx() * B - A * B.dx()


print("手工 jet (7)_h =", mp.nstr((Dx2(Fh, Gh) + Dt(Fh, Gh) + 2 * (a - d) * Dx(Fh, Gh)).maxabs(), 8))
print("手工 jet (6)_h =", mp.nstr((Dx2(Fh, Gh) + Dt(Fh, Gh) + 2 * (a + d) * Dx(Fh, Gh)).maxabs(), 8))

# 与 taujet2 产出的 jet 比较
T = Tau2(N, a, p, q, h)
Fj = T.F(j, X0, T0)
Gj = T.G(j, X0, T0)
C = Fj.coef(0, 0) / (1 + cF)
print("taujet2 F 的前几个系数:", [mp.nstr(v, 10) for v in [Fj.coef(i, 0) for i in range(4)]],
      "\n                  手工:", [mp.nstr(v, 10) for v in [Fh.coef(i, 0) for i in range(4)]])
print("taujet2 (7)_h =", mp.nstr((Dx2(Fj, Gj) + Dt(Fj, Gj) + 2 * (a - d) * Dx(Fj, Gj)).maxabs(), 8))
# 各项量级
print("各项: Dx2=", mp.nstr(Dx2(Fj, Gj).maxabs(), 6),
      " Dt=", mp.nstr(Dt(Fj, Gj).maxabs(), 6),
      " Dx=", mp.nstr(Dx(Fj, Gj).maxabs(), 6))
