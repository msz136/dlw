# -*- coding: utf-8 -*-
"""dbg2.py -- 逐导数核对 J2 jet 与直接标量求值（N=1）。"""
import mpmath as mp
from itertools import permutations

import jet2
from jet2 import J2
import taujet2
taujet2.MX = 6
taujet2.MT = 4
jet2.MX = 6
jet2.MT = 4
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

for (n, s, mu, nm) in [(1, a - h / 2, a, 'F'), (0, a, a, 'G')]:
    jt = T.tau(n, j, s, mu, X0, T0)
    # 归一化：jet 的 tau = C * tau_true，C 为常数（= exp(-sum r - sum c) 部分）
    t0v = tau_scalar(n, j, s, mu, X0, T0)
    C = jt.coef(0, 0) / t0v
    print("%s : jet(0,0)=%s  true=%s  C=%s" %
          (nm, mp.nstr(jt.coef(0, 0), 12), mp.nstr(t0v, 12), mp.nstr(C, 12)))
    # 各偏导：jet 系数 * 阶乘 / C 应与真 tau 的偏导一致
    for (m, nn, name) in [(1, 0, 'x'), (2, 0, 'xx'), (0, 1, 't')]:
        jv = jt.coef(m, nn) * mp.factorial(m) * mp.factorial(nn) / C
        if (m, nn) == (1, 0):
            eps = mp.mpf('1e-15')
            dv = (tau_scalar(n, j, s, mu, X0 + eps, T0)
                  - tau_scalar(n, j, s, mu, X0 - eps, T0)) / (2 * eps)
        elif (m, nn) == (2, 0):
            eps = mp.mpf('1e-12')
            dv = (tau_scalar(n, j, s, mu, X0 + eps, T0)
                  - 2 * tau_scalar(n, j, s, mu, X0, T0)
                  + tau_scalar(n, j, s, mu, X0 - eps, T0)) / eps ** 2
        else:
            eps = mp.mpf('1e-15')
            dv = (tau_scalar(n, j, s, mu, X0, T0 + eps)
                  - tau_scalar(n, j, s, mu, X0, T0 - eps)) / (2 * eps)
        print("    d_%s : jet=%s   direct=%s" % (name, mp.nstr(jv, 15), mp.nstr(dv, 15)))
