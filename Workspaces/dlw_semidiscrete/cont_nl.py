# -*- coding: utf-8 -*-
"""
cont_nl.py -- 连续层(h=0)核对：论文的 u = 2(ln f/g)_x , v = 2(ln fg)_{xy}
              是否满足 DLW 方程 (1)(2)？

若连连续层都不满足，则问题不在离散化，而在 u/v 定义或方程编号。
"""
import mpmath as mp

import jet3

mp.mp.dps = 120
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3
LAM = mp.mpf(-2)
A = mp.mpf(4)
P = [mp.mpf(2) / 3]
Q = [mp.mpf(-18) / 5]


def ev(d):
    return sum(v * mp.e ** (k[0] * X0 + k[1] * T0 + k[2] * Y0) for k, v in d.items())


def L(d, mx=0, mt=0, my=0):
    return ev(jet3.deriv(d, mx, mt, my)) / ev(d)


# 连续 tau：h=None, s=a, mu 任意
f = jet3.tau3(1, A, P, Q, None, 1, A, A, 0)
g = jet3.tau3(1, A, P, Q, None, 0, A, A, 0)
print("f 项数", len(f), " g 项数", len(g))

th = lambda mx, mt, my: L(f, mx, mt, my) - L(g, mx, mt, my)
Ps = lambda mx, mt, my: L(f, mx, mt, my) + L(g, mx, mt, my)

u = 2 * th(1, 0, 0)
ux = 2 * th(2, 0, 0)
uy = 2 * th(1, 0, 1)
ut = 2 * th(1, 1, 0)
uxy = 2 * th(2, 0, 1)
uyt = 2 * th(1, 1, 1)
uxxy = 2 * th(3, 0, 1)

v = 2 * Ps(1, 0, 1)
vx = 2 * Ps(2, 0, 1)
vxx = 2 * Ps(3, 0, 1)
vt = 2 * Ps(1, 1, 1)

print()
print("u   =", mp.nstr(u, 12))
print("v   =", mp.nstr(v, 12))
print()
print("--- 连续双线性方程 ---")
print("(7)  B_a f.g                =", mp.nstr(ev(jet3.Bs3(f, g, A)), 6))
r6 = jet3.add(jet3.Bs3(jet3.deriv(f, 0, 0, 1), g, A),
              jet3.scale(jet3.Bs3(f, g, A) if False else
                         {kk: 0 for kk in []}, 0) if False else {})
# (6): B_a f.g_y + 2 lam D_x f.g
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


def Bs(F, G, s):
    return jet3.add(jet3.add(bilin(F, G, 2, 0, 0), bilin(F, G, 0, 1, 0)),
                    jet3.scale(bilin(F, G, 1, 0, 0), 2 * s))


r6 = jet3.add(Bs(jet3.deriv(f, 0, 0, 1), g, A),
              jet3.scale(bilin(f, g, 1, 0, 0), 2 * LAM))
print("(6)  B_a f.g_y + 2lam D_x f.g =", mp.nstr(ev(r6), 6))
print()
print("--- 候选非线性方程残差 ---")
Ap = ut + vx + u * u / 2 + 2 * A * u
print("(A')  u_t + v_x + u^2/2 + 2a u            =", mp.nstr(Ap, 8))
D1 = uyt + vxx + u * uxy + ux * uy + 2 * A * uxy
print("DLW-1 u_yt+v_xx+u u_xy+u_x u_y+2a u_xy    =", mp.nstr(D1, 8))
D1b = uyt + vxx + u * uxy + 2 * A * uxy
print("DLW-1' u_yt+v_xx+u u_xy+2a u_xy (无u_xu_y) =", mp.nstr(D1b, 8))
D2 = vt + u * vx + ux * v + uxxy + 2 * A * vx + 2 * LAM * ux
print("DLW-2 v_t+(uv)_x+u_xxy+2a v_x+2lam u_x  =", mp.nstr(D2, 8))
print()
print("--- 关系核对 ---")
print("∂_y(A') =", mp.nstr(uyt + vxx + uy * u + u * uxy + 2 * A * uxy, 8))
print("u u_y/2 =", mp.nstr(u * uy / 2, 10))
