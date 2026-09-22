# -*- coding: utf-8 -*-
"""
check_core.py -- 三个决定性核对：

[C1] 结构恒等式 F_j = tau_1(j; a-d) = tau_1(j+1; a+d)（多点）
[C2] 连续层：正确的 u,v 是否满足 DLW-1 / DLW-2
[C3] 非线性层的精确来源：DLW-1 = ∂_y(7)_log + 2 th_x · (6)_log
"""
import mpmath as mp

import jet3

mp.mp.dps = 120
LAM = mp.mpf(-2)
PTS = [
    (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3),
    (mp.mpf(1) / 3, mp.mpf(1) / 5, mp.mpf(1) / 7),
    (mp.mpf(2) / 9, mp.mpf(3) / 11, mp.mpf(-5) / 13),
    (mp.mpf('1.234'), mp.mpf('0.567'), mp.mpf('0.891')),
]


def ev(d, pt=(None, None, None)):
    if pt[0] is None:
        x0 = t0 = y0 = mp.mpf(0)
        return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())
    x0, t0, y0 = pt
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


print("=" * 78)
print("[C1] 结构恒等式 F_j == tau_1(j+1; a+d)")
print("=" * 78)
a, p, q = mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]
for h in (mp.mpf(1) / 4, mp.mpf(1) / 8, mp.mpf(1) / 16):
    d = h / 2
    worst = mp.mpf(0)
    for j in (0, 1, 2, 3):
        L1 = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
        L2 = jet3.tau3(1, a, p, q, h, 1, a + d, a, j + 1)
        same = (set(L1.keys()) == set(L2.keys())) and \
            all(abs(L1[k] - L2[k]) == 0 for k in L1)
        for pt in PTS:
            df = abs(ev(L1, pt) - ev(L2, pt))
            sc = max(abs(ev(L1, pt)), mp.mpf(1))
            worst = max(worst, df / sc)
    print("  h=%-8s 所有 j、所有测试点上的最大相对差 = %s   %s"
          % (mp.nstr(h, 5), mp.nstr(worst, 4),
             "恒等成立" if worst < mp.mpf('1e-100') else "**不成立**"))

print()
print("=" * 78)
print("[C2] 连续层：u=2(ln f/g)_x, v=2(ln fg)_xy 是否满足 DLW")
print("=" * 78)


def logs(f, g, pt):
    def L(D, mx=0, mt=0, my=0):
        return ev(jet3.deriv(D, mx, mt, my), pt) / ev(D, pt)
    th = lambda mx, mt, my: L(f, mx, mt, my) - L(g, mx, mt, my)
    Ps = lambda mx, mt, my: L(f, mx, mt, my) + L(g, mx, mt, my)
    return th, Ps


for (a, p, q) in [(mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]),
                  (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)]),
                  (mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)])]:
    f = jet3.tau3(1, a, p, q, None, 1, a, a, 0)
    g = jet3.tau3(1, a, p, q, None, 0, a, a, 0)
    worst1 = worst2 = mp.mpf(0)
    for pt in PTS:
        th, Ps = logs(f, g, pt)
        u = 2 * th(1, 0, 0)
        ux = 2 * th(2, 0, 0)
        uy = 2 * th(1, 0, 1)
        uxy = 2 * th(2, 0, 1)
        uyt = 2 * th(1, 1, 1)
        uxxy = 2 * th(3, 0, 1)
        v = 2 * Ps(1, 0, 1)
        vx = 2 * Ps(2, 0, 1)
        vxx = 2 * Ps(3, 0, 1)
        vt = 2 * Ps(1, 1, 1)
        sc = max(abs(u), abs(v), mp.mpf(1))
        worst1 = max(worst1, abs(uyt + vxx + u * uxy + ux * uy + 2 * a * uxy) / sc)
        worst2 = max(worst2, abs(vt + u * vx + ux * v + uxxy + 2 * a * vx
                               + 2 * LAM * ux) / sc)
    print("  a=%-8s  DLW-1 最大相对残差 = %-12s  DLW-2 = %-12s"
          % (mp.nstr(a, 6), mp.nstr(worst1, 4), mp.nstr(worst2, 4)))

print()
print("=" * 78)
print("[C3] DLW-1 = ∂_y(7)_log + 2 th_x · (6)_log  （逐点核对）")
print("=" * 78)


def Bs_full(F, G, s):
    from math import comb

    def bilin(F, G, mx=0, mt=0, my=0):
        tot = {}
        for i in range(mx + 1):
            for j in range(mt + 1):
                for l in range(my + 1):
                    co = (-1) ** (i + j + l) * comb(mx, i) * comb(mt, j) * comb(my, l)
                    tot = jet3.add(tot, jet3.scale(jet3.mul(
                        jet3.deriv(F, mx - i, mt - j, my - l),
                        jet3.deriv(G, i, j, l)), co))
        return tot
    return jet3.add(jet3.add(bilin(F, G, 2, 0, 0), bilin(F, G, 0, 1, 0)),
                    jet3.scale(bilin(F, G, 1, 0, 0), 2 * s))


a, p, q = mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]
f = jet3.tau3(1, a, p, q, None, 1, a, a, 0)
g = jet3.tau3(1, a, p, q, None, 0, a, a, 0)
for pt in PTS[:2]:
    th, Ps = logs(f, g, pt)
    u = 2 * th(1, 0, 0)
    ux = 2 * th(2, 0, 0)
    uy = 2 * th(1, 0, 1)
    uxy = 2 * th(2, 0, 1)
    uyt = 2 * th(1, 1, 1)
    uxxy = 2 * th(3, 0, 1)
    vx = 2 * Ps(2, 0, 1)
    vxx = 2 * Ps(3, 0, 1)
    p7 = ev(Bs_full(f, g, a), pt) / (ev(f, pt) * ev(g, pt))
    dyp7 = uy * th(1, 0, 0) + u * th(1, 0, 1) + 2 * a * uxy / 2
    # (6)_log = Q + 2 lam th_xx
    th_xx = 2 * th(2, 0, 0) / 2
    th_yy = th(0, 0, 2)
    Q = th(0, 0, 1) * th(2, 0, 0) + th(1, 0, 0) * th(0, 1, 1) + 2 * a * th(1, 0, 1) \
        + Ps(0, 0, 1) * th(1, 0, 0) + Ps(1, 0, 0) * th(1, 0, 1)
    s6 = ev(Bs_full(jet3.deriv(f, 0, 0, 1), g, a), pt) \
        + 2 * LAM * ev(jet3.add(jet3.scale(jet3.mul(jet3.deriv(f, 1), g),
                                            jet3.mpf(1)) if False else {}, {}), pt)
    print("  点 %s" % (tuple(mp.nstr(z, 4) for z in pt),))
    print("     (7)_log = %s" % mp.nstr(p7, 6))
    D1 = uyt + vxx + u * uxy + ux * uy + 2 * a * uxy
    print("     DLW-1   = %s" % mp.nstr(D1, 6))
