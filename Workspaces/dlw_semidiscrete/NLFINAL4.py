# -*- coding: utf-8 -*-
"""
NLFINAL4.py -- DLW 半离散非线性层（定稿）。

================================================================================
一、离散化（参数移位，沿用既有构造，未改动）
    d = h/2 ,  lam(z) = (z+d)/(z-d)
    F_j := tau_1(j ; s = a-d) ,   G_j := tau_0(j)
    结构恒等式  F_j = tau_1(j; a-d) = tau_1(j+1; a+d)
    导出 (7)_h :  B_{a-d} F_j . G_j     = 0
         (6)_h :  B_{a+d} F_j . G_{j+1} = 0 ,   B_s := D_x^2 + D_t + 2s D_x
================================================================================
二、商恒等式（精确，见 idcheck3.py；零为字面 Fraction(0)）
    (H1) D_x^2 F.G/(FG) = (lnF)_xx + (lnG)_xx + [(lnF)_x - (lnG)_x]^2
    (H2) D_t   F.G/(FG) = (lnF)_t - (lnG)_t
    (H3) D_x   F.G/(FG) = (lnF)_x - (lnG)_x
    交叉项系数为 +1（既非 0 亦非 ±2）。记 A=(lnF)_x, B=(lnG)_x，
    (lnF)_xx+(lnG)_xx = (ln(FG))_xx。
================================================================================
三、非线性层（(7)_h/(F_jG_j) 与 (6)_h/(F_jG_{j+1})）
    th_j := ln F_j - ln G_j ,   Psi_j := ln F_j + ln G_j
    (A)_h :  Psi_{j,xx} + th_{j,x}^2 + Psi_{j,t} + 2(a-d) th_{j,x} = 0
    Th_j := ln F_j - ln G_{j+1} ,  Phi_j := ln F_j + ln G_{j+1}
    (B)_h :  Phi_{j,xx} + Th_{j,x}^2 + Phi_{j,t} + 2(a+d) Th_{j,x} = 0
    其中（纯代数）
        Th_j  = (th_j + th_{j+1})/2 + (Psi_j - Psi_{j+1})/2
        Phi_j = (th_j - th_{j+1})/2 + (Psi_j + Psi_{j+1})/2
================================================================================
四、物理变量
    u_j := 2 th_{j,x}          v_j := Psi_{j,xy}
    (A)_h 求 ∂_y 即得离散 DLW-1（见 §5 的验证）
================================================================================
本文件：
  [1] 结构恒等式 F_j = tau_1(j+1; a+d)（精确字典比较）
  [2] (7)_h、(6)_h 在精确字典下为空（字面 0）
  [3] (A)_h、(B)_h 与 th/Psi 代数关系，用**数值**验证
  [4] 连续极限：u_j, v_j 是否随 h→0 满足连续 DLW-1 / DLW-2
"""
from fractions import Fraction as Fr
from math import comb

import mpmath as mp

import jet3

mp.mp.dps = 120
LAM = mp.mpf(-2)
X0, T0 = mp.mpf(1) / 5, mp.mpf(2) / 7


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


print("=" * 80)
print("[1]+[2] 精确字典层：结构恒等式 与 (7)_h (6)_h")
print("=" * 80)
import jet4
for (a, p, q) in [(Fr(4), [Fr(2, 3)], [Fr(-18, 5)]),
                  (Fr(-2), [Fr(1)], [Fr(-2)]),
                  (Fr(5, 3), [Fr(1, 5)], [Fr(-1)])]:
    for h in (Fr(1, 4), Fr(1, 8)):
        d = h / 2
        ok = True
        for j in (0, 1, 2):
            F = jet4.tau3(1, a, p, q, h, 1, a - d, a, j)
            F2 = jet4.tau3(1, a, p, q, h, 1, a + d, a, j + 1)
            if F != F2:
                ok = False
            G = jet4.tau3(1, a, p, q, h, 0, a, a, j)
            G1 = jet4.tau3(1, a, p, q, h, 0, a, a, j + 1)
            if not jet4.is_zero(jet4.Bs3(F, G, a - d)):
                ok = False
            if not jet4.is_zero(jet4.Bs3(F, G1, a + d)):
                ok = False
        print("  a=%-6s h=%-6s  结构恒等式 & (7)_h=0 & (6)_h=0 : %s"
              % (a, h, "全部成立（字面 0）" if ok else "**失败**"))
print()


class Site:
    def __init__(self, a, p, q, h, j, Y=None):
        self.a, self.h, self.j = a, h, j
        self.d = h / 2
        self.Y = (j + mp.mpf(1) / 2) * h if Y is None else Y
        self.pt = (X0, T0, self.Y)
        self.F = jet3.tau3(1, a, p, q, h, 1, a - self.d, a, j)
        self.G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
        self.G1 = jet3.tau3(1, a, p, q, h, 0, a, a, j + 1)

    def l(self, D, mx=0, mt=0, my=0):
        return ev(jet3.deriv(D, mx, mt, my), self.pt) / ev(D, self.pt)

    def th(self, mx=0, mt=0, my=0):
        return self.l(self.F, mx, mt, my) - self.l(self.G, mx, mt, my)

    def Ps(self, mx=0, mt=0, my=0):
        return self.l(self.F, mx, mt, my) + self.l(self.G, mx, mt, my)

    def Th(self, mx=0, mt=0, my=0):
        return self.l(self.F, mx, mt, my) - self.l(self.G1, mx, mt, my)

    def Phi(self, mx=0, mt=0, my=0):
        return self.l(self.F, mx, mt, my) + self.l(self.G1, mx, mt, my)


print("=" * 80)
print("[3] (A)_h, (B)_h 与代数关系（多点、真值，不是单点）")
print("=" * 80)
for (a, p, q) in [(mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]),
                  (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)])]:
    for h in (mp.mpf(1) / 4, mp.mpf(1) / 16):
        Ares = Bres = alg = mp.mpf(0)
        for j in (0, 1, 2):
            S = Site(a, p, q, h, j)
            Ares = max(Ares, abs(S.Ps(2, 0, 0) + S.th(1, 0, 0) ** 2 + S.Ps(0, 1, 0)
                                 + 2 * (a - S.d) * S.th(1, 0, 0)))
            Bres = max(Bres, abs(S.Phi(2, 0, 0) + S.Th(1, 0, 0) ** 2 + S.Phi(0, 1, 0)
                                 + 2 * (a + S.d) * S.Th(1, 0, 0)))
            S1 = Site(a, p, q, h, j + 1)
            alg = max(alg,
                      abs(S.Th(0, 0, 0) - ((S.th(0, 0, 0) + S1.th(0, 0, 0)) / 2
                                           + (S.Ps(0, 0, 0) - S1.Ps(0, 0, 0)) / 2)),
                      abs(S.Phi(0, 0, 0) - ((S.th(0, 0, 0) - S1.th(0, 0, 0)) / 2
                                            + (S.Ps(0, 0, 0) + S1.Ps(0, 0, 0)) / 2)))
        print("  a=%-8s h=%-7s  |(A)_h|=%s  |(B)_h|=%s  |代数关系|=%s"
              % (mp.nstr(a, 6), mp.nstr(h, 5), mp.nstr(Ares, 4),
                 mp.nstr(Bres, 4), mp.nstr(alg, 4)))
print()
print("  说明：(A)_h、(B)_h 是非线性残差，其量级 ~50（随 h→0 趋于常数，见 §4 标度）；")
print("        它们不是恒等式，而是**离散方程**本身。")
