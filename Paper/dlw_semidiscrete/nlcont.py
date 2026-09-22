# -*- coding: utf-8 -*-
"""
nlcont.py -- 连续极限核查（定稿）。

已精确验证（nlfinal.py）：
    (A)_h : Psi_{j,xx} + theta_{j,x}^2 + theta_{j,t} + 2(a-d) theta_{j,x} = 0
    (B)_h : 同形式（用 G_{j+1} 的移位变量，参数 a+d）

本文件核查：
    A. h -> 0 时 (A)_h 是否恢复连续 (7) 的非线性形式；
    B. 连续 tau 是否满足 DLW 双线性对 (7)、(6)；
    C. u = 2 th_x, v = 2 Psi_{xy} 是否满足 DLW 方程。
"""
import mpmath as mp

import jet3

mp.mp.dps = 90
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(0)
a = mp.mpf(4)
p = [mp.mpf(2) / 3]
q = [mp.mpf(-18) / 5]


def v3(dd, mx=0, mt=0, my=0):
    return jet3.ev(jet3.deriv(dd, mx, mt, my), X0, T0, Y0)


def L(dd, mx=0, mt=0, my=0):
    return v3(dd, mx, mt, my) / v3(dd)


print("=== A. (A)_h 残差：半离散 2(a-d) vs 连续 2a（后者应 O(h)）===")
prev = None
for k in range(1, 6):
    hh = mp.mpf(1) / 2 ** k
    d = hh / 2
    F = lambda j: jet3.tau3(1, a, p, q, hh, 1, a - d, a, j)
    G = lambda j: jet3.tau3(1, a, p, q, hh, 0, a, a, j)
    th = lambda j, mx=0, mt=0: L(F(j), mx, mt) - L(G(j), mx, mt)
    l2 = lambda dd: v3(dd, 2) / v3(dd) - L(dd, 1) ** 2
    base = (l2(F(0)) + l2(G(0))) + th(0, 1) ** 2 + th(0, 0, 1)
    sd = base + 2 * (a - d) * th(0, 1)
    ct = base + 2 * a * th(0, 1)
    ratio = '' if prev is None else '  ratio=%.3f' % (ct / prev)
    print("  h=%-10s  (A)_h=%-13s  (A)_cont=%-13s%s"
          % (mp.nstr(hh, 6), mp.nstr(sd, 4), mp.nstr(ct, 6), ratio))
    prev = ct

print()
print("=== B. 连续 tau 满足 DLW 双线性对 ===")
Fc = jet3.tau3(1, a, p, q, mp.mpf(0), 1, a, a, 0)
Gc = jet3.tau3(1, a, p, q, mp.mpf(0), 0, a, a, 0)
print("  (7)  B_a f.g            =", mp.nstr(jet3.ev(jet3.Bs3(Fc, Gc, a)), 5))
Gc1 = jet3.tau3(1, a, p, q, mp.mpf(0), 0, a, a, 1)
print("  (6)  B_a f.g_{j+1}      =", mp.nstr(jet3.ev(jet3.Bs3(Fc, Gc1, a)), 5))

print()
print("=== C. 连续解代入 DLW 方程 ===")
al = lambda mx=0, mt=0, my=0: L(Fc, mx, mt, my)
be = lambda mx=0, mt=0, my=0: L(Gc, mx, mt, my)
th = lambda mx=0, mt=0, my=0: al(mx, mt, my) - be(mx, mt, my)
ps = lambda mx=0, mt=0, my=0: al(mx, mt, my) + be(mx, mt, my)
u = 2 * th(1)
v = 2 * ps(1, 0, 1)
r1 = 2 * th(1, 1) + 2 * ps(2, 0, 1) + u * (2 * th(2, 0, 1)) \
    + (2 * th(2)) * (2 * th(1, 0, 1)) + 2 * a * (2 * th(2, 0, 1))
print("  u =", mp.nstr(u, 12), "  v =", mp.nstr(v, 12))
print("  DLW-1 残差 =", mp.nstr(r1, 8))
# 连续 (A) 的非线性形式
nl = ps(2) + th(1) ** 2 + th(0, 1) + 2 * a * th(1)
print("  连续 (A) 残差 =", mp.nstr(nl, 8))
print("  即 Psi_xx + theta_x^2 + theta_t + 2a theta_x")
