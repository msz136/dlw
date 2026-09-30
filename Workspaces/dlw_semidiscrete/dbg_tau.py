# -*- coding: utf-8 -*-
"""dbg_tau.py -- 校验 taujet 的 jet 求值与直接标量求值一致。"""
import mpmath as mp
from itertools import permutations
from jet import Jet
from taujet import Tau

mp.mp.dps = 60
X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7


def tau_scalar(N, a, p, q, h, n, j, s, mu, x0, t0):
    ent = {}
    for i in range(N):
        for k in range(N):
            coef = (-(p[i] - s) / (q[k] + s)) ** n / (p[i] + q[k])
            if j:
                d = h / 2
                lp = (p[i] - a + d) / (p[i] - a - d)
                lq = (q[k] + a + d) / (q[k] + a - d)
                coef = coef * (lp * lq) ** j
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
            for jj in range(ii + 1, N):
                if pl[ii] > pl[jj]:
                    sign = -sign
        t = mp.mpf(sign)
        for i in range(N):
            t *= ent[(i, perm[i])]
        tot += t
    return tot


def jet_eval(jt, u):
    return mp.polyval(jt.a[::-1], mp.mpc(u))


for (N, a, p, q, h, j) in [
    (1, mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4, 1),
    (1, mp.mpf(1), [mp.mpf(1) / 2], [mp.mpf(-1) / 6], mp.mpf(1) / 4, 1),
    (2, mp.mpf(1), [mp.mpf(13) / 5, mp.mpf(4) / 3], [mp.mpf(-12), mp.mpf(-15)], mp.mpf(1) / 4, 1),
]:
    T = Tau(N, a, p, q, h)
    for (n, s, mu, nm) in [(1, a - h / 2, a, 'F'), (0, a, a, 'G')]:
        jt = T.tau(n, j, s, mu, X0, T0)
        direct = tau_scalar(N, a, p, q, h, n, j, s, mu, X0, T0)
        # jet 的常数项 = 归一化后的 tau（差一个常数因子），比值应与 u 无关
        const = jt.a[0]
        u = mp.mpf('0.01')
        # 直接算归一化后的比值：用 u=0.01 的 tau 与 u=0 的 tau 之比
        # 通过与 jet 比值比较来判定 jet 是否正确
        print("N=%d %s j=%d : jet(0)=%s  direct=%s" %
              (N, nm, j, mp.nstr(const, 12), mp.nstr(direct, 12)))
        # 数值微分检验： (tau(x0+u)-tau(x0-u))/(2u) 与 jet 的 a_1
        eps = mp.mpf('1e-8')
        # 直接标量求值需要把 x0 平移
        def tau_at(dx):
            return tau_scalar(N, a, p, q, h, n, j, s, mu, X0 + dx, T0)
        # 归一化因子随基点变化 -> 需用 log 比较
        num = (mp.log(tau_at(eps)) - mp.log(tau_at(-eps))) / (2 * eps)
        jetv = jt.dx().a[0] * 0 + (jt.dx().a[0])
        # jet 的 (ln tau)_x 系数
        lx = jt.log().dx().a[0]
        print("      (ln tau)_x :  jet = %s   direct = %s" %
              (mp.nstr(lx, 15), mp.nstr(num, 15)))
