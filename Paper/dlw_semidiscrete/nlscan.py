# -*- coding: utf-8 -*-
"""
nlscan.py -- 用「固定物理点 Y=(j+1/2)h」的一致极限扫 h，测定各残差的真实标度。

固定 (x,t,y) 扫 h 是**错误**的比较方式：格点 j 的物理位置是 Y_j=(j+1/2)h，
h 变小时同一个 j 对应不同物理点。故必须固定 Y 再扫 h。
"""
import mpmath as mp

import jet3

mp.mp.dps = 120
X0, T0 = mp.mpf(1) / 5, mp.mpf(2) / 7


def ev(d, pt):
    x0, t0, y0 = pt
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


def build(a, p, q, h, j):
    d = h / 2
    F = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
    G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
    G1 = jet3.tau3(1, a, p, q, h, 0, a, a, j + 1)
    return F, G, G1


def Amax(a, p, q, h, j):
    """(A)_h 在固定物理点的绝对值（Y=(j+1/2)h）。"""
    F, G, _ = build(a, p, q, h, j)
    d = h / 2
    pt = (X0, T0, (j + mp.mpf(1) / 2) * h)
    lF1 = ev(jet3.deriv(F, 1), pt) / ev(F, pt)
    lF2 = ev(jet3.deriv(F, 2), pt) / ev(F, pt) - lF1 ** 2
    lF0 = ev(jet3.deriv(F, 0, 1), pt) / ev(F, pt)
    lG1 = ev(jet3.deriv(G, 1), pt) / ev(G, pt)
    lG2 = ev(jet3.deriv(G, 2), pt) / ev(G, pt) - lG1 ** 2
    lG0 = ev(jet3.deriv(G, 0, 1), pt) / ev(G, pt)
    th_x = lF1 - lG1
    th_t = lF0 - lG0
    return (lF2 + lG2) + th_x ** 2 + th_t + 2 * (a - d) * th_x


def bilin(F, G, mx=0, mt=0):
    from math import comb
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


print("固定物理点 (x,t,Y)=(1/5, 2/7, (j+1/2)h)，扫 h")
print("参数 a=4, p=2/3, q=-18/5, j=1")
print()
print("%-9s %-14s %-10s %-14s %-10s %-14s" %
      ("h", "|(A)_h|", "比值", "|(7)_h|", "比值", "|(6)_h|"))
a, p, q = mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]
prevA = prev7 = None
for k in range(1, 9):
    h = mp.mpf(1) / 2 ** k
    d = h / 2
    j = 1
    pt = (X0, T0, (j + mp.mpf(1) / 2) * h)
    F, G, G1 = build(a, p, q, h, j)
    rA = abs(Amax(a, p, q, h, j))
    r7 = abs(ev(Bs(F, G, a - d), pt))
    r6 = abs(ev(Bs(F, G1, a + d), pt))
    print("%-9s %-14s %-10s %-14s %-10s %-14s"
          % (mp.nstr(h, 6), mp.nstr(rA, 6),
             "-" if prevA is None else mp.nstr(rA / prevA, 5),
             mp.nstr(r7, 6),
             "-" if prev7 is None else mp.nstr(r7 / prev7, 5),
             mp.nstr(r6, 6)))
    prevA, prev7 = rA, r7

print()
print("对照：把 (A)_h 中的 a-d 换成连续 a 之后的残差")
prev = None
for k in range(1, 7):
    h = mp.mpf(1) / 2 ** k
    d = h / 2
    j = 1
    pt = (X0, T0, (j + mp.mpf(1) / 2) * h)
    F, G, _ = build(a, p, q, h, j)
    lF1 = ev(jet3.deriv(F, 1), pt) / ev(F, pt)
    lF2 = ev(jet3.deriv(F, 2), pt) / ev(F, pt) - lF1 ** 2
    lF0 = ev(jet3.deriv(F, 0, 1), pt) / ev(F, pt)
    lG1 = ev(jet3.deriv(G, 1), pt) / ev(G, pt)
    lG2 = ev(jet3.deriv(G, 2), pt) / ev(G, pt) - lG1 ** 2
    lG0 = ev(jet3.deriv(G, 0, 1), pt) / ev(G, pt)
    th_x = lF1 - lG1
    r = (lF2 + lG2) + th_x ** 2 + (lF0 - lG0) + 2 * a * th_x
    print("  h=%-9s 残差=%-16s 比值=%s"
          % (mp.nstr(h, 6), mp.nstr(abs(r), 6),
             "-" if prev is None else mp.nstr(abs(r) / prev, 5)))
    prev = abs(r)
