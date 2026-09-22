# -*- coding: utf-8 -*-
"""
diag.py -- 定位 (A)_h 的计算矛盾：
  (7)_h/FG 按定义 = (D_x^2 F.G + D_t F.G + 2s D_x F.G)/(FG)
  而商恒等式说它 = Psi_xx + th_x^2 + th_t + 2s th_x
两者必须相等。若不等，说明商恒等式或对数导数算错了。
"""
from fractions import Fraction as Fr
from math import comb

import mpmath as mp

import jet3

mp.mp.dps = 120
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3


def ev(d):
    return sum(v * mp.e ** (k[0] * X0 + k[1] * T0 + k[2] * Y0) for k, v in d.items())


def bilin(F, G, mx=0, mt=0):
    tot = {}
    for i in range(mx + 1):
        for j in range(mt + 1):
            co = (-1) ** (i + j) * comb(mx, i) * comb(mt, j)
            tot = jet3.add(tot, jet3.scale(jet3.mul(
                jet3.deriv(F, mx - i, mt - j), jet3.deriv(G, i, j)), co))
    return tot


a = mp.mpf(4)
p = [mp.mpf(2) / 3]
q = [mp.mpf(-18) / 5]
h = mp.mpf(1) / 4
d = h / 2
s = a - d
j = 1

F = jet3.tau3(1, a, p, q, h, 1, s, a, j)
G = jet3.tau3(1, a, p, q, h, 0, a, a, j)

FG = jet3.mul(F, G)
d2 = bilin(F, G, 2, 0)
dt = bilin(F, G, 0, 1)
dx = bilin(F, G, 1, 0)
num = jet3.add(jet3.add(d2, dt), jet3.scale(dx, 2 * s))

print("(7)_h 的字典（应为空）:", len(num), "项")
print("FG 值 =", mp.nstr(ev(FG), 12))
print("num 值 =", mp.nstr(ev(num), 12))
print("num/FG =", mp.nstr(ev(num) / ev(FG), 12))
print()

# 商恒等式右侧
lF_x = ev(jet3.deriv(F, 1)) / ev(F)
lG_x = ev(jet3.deriv(G, 1)) / ev(G)
lF_xx = ev(jet3.deriv(F, 2)) / ev(F) - lF_x ** 2
lG_xx = ev(jet3.deriv(G, 2)) / ev(G) - lG_x ** 2
lF_t = ev(jet3.deriv(F, 0, 1)) / ev(F)
lG_t = ev(jet3.deriv(G, 0, 1)) / ev(G)

th_x = lF_x - lG_x
th_t = lF_t - lG_t
Psi_xx = lF_xx + lG_xx

print("(H1) 检验：D_x^2/(FG) vs Psi_xx + th_x^2")
D2 = ev(d2) / ev(FG)
print("   D_x^2/(FG)      =", mp.nstr(D2, 12))
print("   Psi_xx + th_x^2 =", mp.nstr(Psi_xx + th_x ** 2, 12))
print("   差              =", mp.nstr(D2 - (Psi_xx + th_x ** 2), 6))
print()
print("(H2) 检验：D_t/(FG) vs th_t")
print("   D_t/(FG) =", mp.nstr(ev(dt) / ev(FG), 12))
print("   th_t     =", mp.nstr(th_t, 12))
print()
print("(H3) 检验：D_x/(FG) vs th_x")
print("   D_x/(FG) =", mp.nstr(ev(dx) / ev(FG), 12))
print("   th_x     =", mp.nstr(th_x, 12))
print()
print("=>  (A)_h = num/FG =", mp.nstr(ev(num) / ev(FG), 12))
print("    (Psi_xx+th_x^2+th_t+2s th_x) =",
      mp.nstr(Psi_xx + th_x ** 2 + th_t + 2 * s * th_x, 12))
print()
print("    th_x =", mp.nstr(th_x, 12), " th_t =", mp.nstr(th_t, 12))
print("    Psi_xx =", mp.nstr(Psi_xx, 12), " th_x^2 =", mp.nstr(th_x ** 2, 12))
