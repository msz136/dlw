# -*- coding: utf-8 -*-
"""
nlaudit.py -- 对先前声明的每一条"判零"，在**多点**上重测。

每条恒等式报告 maxrel = max over 测试点 |残差|/尺度。
  maxrel < 1e-40 -> 数值上成立
  否则           -> 非恒等式（打印反例点）
并单独列出 Y0=0 那条特殊线上的值，以说明单点检验为何会误判。
"""
from math import comb

import mpmath as mp

import jet3

mp.mp.dps = 120

PTS = [
    ("Y0=0特殊线", (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(0))),
    ("一般点1", (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3)),
    ("一般点2", (mp.mpf(1) / 3, mp.mpf(1) / 5, mp.mpf(1) / 7)),
]

CASES = [
    (mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4),
    (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)], mp.mpf(1) / 4),
    (mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)], mp.mpf(1) / 8),
]


def ev(d, pt):
    x0, t0, y0 = pt
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


def bilin(F, G, mx=0, mt=0):
    tot = {}
    for i in range(mx + 1):
        for j in range(mt + 1):
            co = (-1) ** (i + j) * comb(mx, i) * comb(mt, j)
            tot = jet3.add(tot, jet3.scale(jet3.mul(
                jet3.deriv(F, mx - i, mt - j), jet3.deriv(G, i, j)), co))
    return tot


def Bs(F, G, s):
    return jet3.add(jet3.add(bilin(F, G, 2, 0), bilin(F, G, 0, 1)),
                    jet3.scale(bilin(F, G, 1, 0), 2 * s))


def build(a, p, q, h, j):
    d = h / 2
    F = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
    G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
    G1 = jet3.tau3(1, a, p, q, h, 0, a, a, j + 1)
    s = a - d
    Fx, Fxx = jet3.deriv(F, 1), jet3.deriv(F, 2)
    Gx, Gxx = jet3.deriv(G, 1), jet3.deriv(G, 2)
    Ft, Gt = jet3.deriv(F, 0, 1), jet3.deriv(G, 0, 1)
    FG = jet3.mul(F, G)
    A1 = jet3.add(jet3.mul(Fxx, F), jet3.scale(jet3.mul(Fx, Fx), -1))
    A2 = jet3.add(jet3.mul(Gxx, G), jet3.scale(jet3.mul(Gx, Gx), -1))
    cr = jet3.add(jet3.mul(Fx, G), jet3.scale(jet3.mul(F, Gx), -1))
    dxx = bilin(F, G, 2, 0)
    H1 = jet3.add(jet3.mul(dxx, FG),
                  jet3.scale(jet3.add(jet3.add(jet3.mul(jet3.mul(G, G), A1),
                                               jet3.mul(jet3.mul(F, F), A2)),
                                      jet3.mul(cr, cr)), -1))
    # (A)_h 的通分残差（见 nlexact.py 的推导）
    th_t = jet3.add(jet3.mul(Ft, G), jet3.scale(jet3.mul(F, Gt), -1))
    th_x = cr
    Ares = jet3.add(jet3.add(jet3.mul(dxx, FG), jet3.mul(th_t, FG)),
                    jet3.add(jet3.scale(jet3.mul(th_x, FG), 2 * s),
                             jet3.mul(th_x, th_x)))
    tests = {
        '(7)_h': (Bs(F, G, s), [F, G, Fx, Fxx, Ft, FG]),
        '(6)_h': (Bs(F, G1, a + d), [F, G1, FG]),
        '(H1)商恒等式': (H1, [F, G, FG, cr, jet3.mul(F, F), jet3.mul(G, G)]),
        '(A)_h': (Ares, [F, G, FG, cr]),
    }
    return tests


print("多点体检（dps=120；相对残差 <1e-40 视为成立）")
for (a, p, q, h) in CASES:
    print("=" * 80)
    print("a=%s h=%s" % (mp.nstr(a, 6), mp.nstr(h, 5)))
    for j in (0, 1, 2):
        for name, (res, parts) in build(a, p, q, h, j).items():
            row = []
            for label, pt in PTS:
                r = ev(res, pt)
                sc = max(abs(ev(dd, pt)) for dd in parts) or mp.mpf(1)
                row.append((label, abs(r) / sc))
            worst = max(v for _, v in row)
            if worst < mp.mpf('1e-40'):
                verdict = "成立"
            else:
                bad = [l for l, v in row if v > mp.mpf('1e-40')][0]
                verdict = "**不成立** max_rel=%s (反例:%s)" % (mp.nstr(worst, 4), bad)
            at0 = [v for l, v in row if l == 'Y0=0特殊线'][0]
            print("  j=%d %-14s %-44s [Y0=0处rel=%s]"
                  % (j, name, verdict, mp.nstr(at0, 3)))
    print()
