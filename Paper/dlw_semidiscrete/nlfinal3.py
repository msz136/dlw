# -*- coding: utf-8 -*-
"""
nlfinal3.py -- 离散非线性系统（定稿版）。

离散化（参数移位，不再改动）：d = h/2, F_j = tau_1(j; a-d), G_j = tau_0(j)。

双线性层（τ 级、已由精确字典引擎验证）：
    (7)_h : B_{a-d} F_j . G_j        = 0 ,   B_s = D_x^2 + D_t + 2s D_x
    (6)_h : B_{a+d} F_j . G_{j+1}    = 0

商恒等式（H1）D_x^2 F.G/(FG) = (lnF)_xx + (lnG)_xx + [(lnF)_x-(lnG)_x]^2
            （H2）D_t   F.G/(FG) = (lnF)_t - (lnG)_t
            （H3）D_x   F.G/(FG) = (lnF)_x - (lnG)_x

非线性层 —— 由 (7)_h 除以 F_jG_j：
    (A)_h :  Psi_{j,xx} + th_{j,x}^2 + Psi_{j,t} + 2(a-d) th_{j,x} = 0
     其中 th_j = ln F_j - ln G_j ,  Psi_j = ln F_j + ln G_j
由 (6)_h 除以 F_jG_{j+1}：
    (B)_h :  Phi_{j,xx} + Th_{j,x}^2 + Phi_{j,t} + 2(a+d) Th_{j,x} = 0
     其中 Th_j = ln F_j - ln G_{j+1} ,  Phi_j = ln F_j + ln G_{j+1}
     且 Th_j = (th_j + th_{j+1})/2 + (Psi_j - Psi_{j+1})/2
        Phi_j = (th_j - th_{j+1})/2 + (Psi_j + Psi_{j+1})/2

物理变量：
    u_j := 2 th_{j,x}      （=> u_{j,y} = 2(∂_y th_j)_x）
    v_j := Psi_{j,xy}      （注意：v = 2(ln fg)_{xy} 的离散类比取 Psi_{j,xy}）
本脚本：
  [1] 验证 (A)_h、(B)_h 在多点上的值（真值）
  [2] 验证 (A)_h 的 y 导数给出的离散 DLW-1 是否正确
  [3] 扫 h 看标度
"""
import mpmath as mp

import jet3

mp.mp.dps = 120

PTS = [
    (mp.mpf(1) / 5, mp.mpf(2) / 7),
    (mp.mpf(1) / 3, mp.mpf(1) / 5),
    (mp.mpf(2) / 9), 
]


def ev(d, pt):
    x0, t0, y0 = pt
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


class Site:
    """在格点 j、固定物理点 Y=(j+1/2)h 上的 tau 对数导数。"""

    def __init__(self, a, p, q, h, j, X0, T0):
        self.d = h / 2
        self.j = j
        self.Y = (j + mp.mpf(1) / 2) * h
        self.p = (X0, T0, self.Y)
        self.F = jet3.tau3(1, a, p, q, h, 1, a - self.d, a, j)
        self.G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
        self.a = a
        self.h = h

    def lF(self, mx=0, mt=0, my=0):
        return ev(jet3.deriv(self.F, mx, mt, my), self.p) / ev(self.F, self.p)

    def lG(self, mx=0, mt=0, my=0):
        return ev(jet3.deriv(self.G, mx, mt, my), self.p) / ev(self.G, self.p)

    def th(self, mx=0, mt=0, my=0):
        return self.lF(mx, mt, my) - self.lG(mx, mt, my)

    def Ps(self, mx=0, mt=0, my=0):
        return self.lF(mx, mt, my) + self.lG(mx, mt, my)

    def A_res(self):
        """(A)_h = Psi_xx + th_x^2 + Psi_t + 2(a-d)th_x"""
        return self.Ps(2, 0, 0) + self.th(1, 0, 0) ** 2 + self.Ps(0, 1, 0) \
            + 2 * (self.a - self.d) * self.th(1, 0, 0)


def Bhat(a, p, q, h, j, X0, T0):
    """(B)_h = Phi_xx + Th_x^2 + Phi_t + 2(a+d) Th_x ，用 F_j 与 G_{j+1}。"""
    d = h / 2
    Y = (j + mp.mpf(1) / 2) * h
    pt = (X0, T0, Y)
    F = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
    G1 = jet3.tau3(1, a, p, q, h, 0, a, a, j + 1)

    def l(D, mx=0, mt=0, my=0):
        return ev(jet3.deriv(D, mx, mt, my), pt) / ev(D, pt)

    Th = lambda mx, mt, my: l(F, mx, mt, my) - l(G1, mx, mt, my)
    Phi = lambda mx, mt, my: l(F, mx, mt, my) + l(G1, mx, mt, my)
    return Phi(2, 0, 0) + Th(1, 0, 0) ** 2 + Phi(0, 1, 0) \
        + 2 * (a + d) * Th(1, 0, 0)


X0, T0 = mp.mpf(1) / 5, mp.mpf(2) / 7
CASES = [
    (mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]),
    (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)]),
    (mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)]),
]

print("=" * 84)
print("[1] (A)_h 与 (B)_h 在固定物理点上的值（j=0,1,2）")
print("=" * 84)
for (a, p, q) in CASES:
    for h in (mp.mpf(1) / 4, mp.mpf(1) / 16):
        row = []
        for j in (0, 1, 2):
            S = Site(a, p, q, h, j, X0, T0)
            row.append((abs(S.A_res()), abs(Bhat(a, p, q, h, j, X0, T0))))
        print("  a=%-8s h=%-7s  |(A)_h|: %s   |(B)_h|: %s"
              % (mp.nstr(a, 6), mp.nstr(h, 6),
                 " ".join("%-10s" % mp.nstr(r[0], 4) for r in row),
                 " ".join("%-10s" % mp.nstr(r[1], 4) for r in row)))
    print()

print("=" * 84)
print("[2] 标度：a=4, j=1, 固定 (x,t)=(1/5,2/7), Y=(j+1/2)h")
print("=" * 84)
a, p, q = mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]
print("%-10s %-16s %-12s %-16s %-12s" % ("h", "|(A)_h|", "比值", "|(B)_h|", "比值"))
pA = pB = None
for k in range(1, 9):
    h = mp.mpf(1) / 2 ** k
    S = Site(a, p, q, h, 1, X0, T0)
    rA = abs(S.A_res())
    rB = abs(Bhat(a, p, q, h, 1, X0, T0))
    print("%-10s %-16s %-12s %-16s %-12s"
          % (mp.nstr(h, 6), mp.nstr(rA, 6),
             "-" if pA is None else mp.nstr(rA / pA, 5),
             mp.nstr(rB, 6),
             "-" if pB is None else mp.nstr(rB / pB, 5)))
    pA, pB = rA, rB
print()
print("注意：若残差 ~ h^2，则 (A)_h、(B)_h 是**二阶精确**的离散化。")
