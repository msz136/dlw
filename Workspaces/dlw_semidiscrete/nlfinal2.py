# -*- coding: utf-8 -*-
"""
nlfinal2.py -- 非线性层的**决定性检验**：离散非线性残差是否随 h 消失？

物理变量（按参数移位离散化）
    u_j := 2 th_{j,x} ,  th_j = ln(F_j/G_j)
    w_j := 2 Psi_{j,x} , Psi_j = ln(F_j G_j)
    v_j := w_{j,y} = 2 Psi_{j,xy}
离散非线性恒等式（τ 级精确）：
    (A')  u_{j,t} + w_{j,x} + u_j^2/2 + 2(a-d) u_j = 0
    (B')  Th_{j,t} + ...
本脚本测：
    R1 := u_{j,t} + v_{j,x} + u_j u_{j,x} + (u_{j,x} u_{j,y})? ...
两个候选：
    R1a = y 导数型：  (u_t + v_x + u^2/2 + 2(a-d)u)_y
    R1b = DLW-1 型：  u_{yt} + v_{xx} + u u_{xy} + u_x u_y + 2(a-d) u_{xy}
    R2  = DLW-2 型：  v_t + (u v)_x + u_{xxy} + 2(a-d) v_x + 2λ u_x
全部在固定物理点 Y=(j+1/2)h 上扫 h。
"""
import mpmath as mp

import jet3

mp.mp.dps = 120
X0, T0 = mp.mpf(1) / 5, mp.mpf(2) / 7
LAM = mp.mpf(-2)


def ev(d, x0, t0, y0):
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


def build(a, p, q, h, j):
    d = h / 2
    F = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
    G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
    return F, G


class Pt:
    """在固定物理点算 tau 的各阶对数导数。"""

    def __init__(self, F, G, x0, t0, y0):
        self.F, self.G = F, G
        self.p = (x0, t0, y0)

    def l(self, D, mx=0, mt=0, my=0):
        v0 = ev(D, *self.p)
        return ev(jet3.deriv(D, mx, mt, my), *self.p) / v0

    def th(self, mx=0, mt=0, my=0):
        return self.l(self.F, mx, mt, my) - self.l(self.G, mx, mt, my)

    def Ps(self, mx=0, mt=0, my=0):
        return self.l(self.F, mx, mt, my) + self.l(self.G, mx, mt, my)


def residuals(a, p, q, h, j):
    F, G = build(a, p, q, h, j)
    d = h / 2
    y0 = (j + mp.mpf(1) / 2) * h
    P = Pt(F, G, X0, T0, y0)

    u = 2 * P.th(1, 0, 0)
    ux = 2 * P.th(2, 0, 0)
    ut = 2 * P.th(1, 1, 0)
    uy = 2 * P.th(1, 0, 1)
    uxy = 2 * P.th(2, 0, 1)
    uyt = 2 * P.th(1, 1, 1)
    uxxy = 2 * P.th(3, 0, 1)

    v = 2 * P.Ps(1, 0, 1)
    vx = 2 * P.Ps(2, 0, 1)
    vxx = 2 * P.Ps(3, 0, 1)
    vt = 2 * P.Ps(1, 1, 1)

    # (A') 及其 y 导数
    Ap = ut + vx + u * u / 2 + 2 * (a - d) * u
    # DLW-1 型（含 u_x u_y）
    R1b = uyt + vxx + u * uxy + ux * uy + 2 * (a - d) * uxy
    # DLW-2 型
    R2 = vt + (u * v) * 0 + 0  # 先占位
    R2 = vt + (u * vx + ux * v) + uxxy + 2 * (a - d) * vx + 2 * LAM * ux
    return dict(Ap=Ap, R1b=R1b, R2=R2, u=u, v=v)


CASES = [
    (mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], 1),
    (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)], 1),
    (mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)], 1),
]

for (a, p, q, j) in CASES:
    print("=" * 84)
    print("a=%s p=%s q=%s j=%d,  固定物理点 (x,t,Y)=(1/5,2/7,(j+1/2)h)"
          % (mp.nstr(a, 6), [mp.nstr(z, 4) for z in p],
             [mp.nstr(z, 4) for z in q], j))
    print("%-10s %-20s %-20s %-20s" % ("h", "(A') 残差", "R1b (DLW-1型)", "R2 (DLW-2型)"))
    prev = {}
    for k in range(1, 9):
        h = mp.mpf(1) / 2 ** k
        R = residuals(a, p, q, h, j)
        row = "% -10s" % mp.nstr(h, 6)
        for key in ('Ap', 'R1b', 'R2'):
            v = abs(R[key])
            rat = "-" if key not in prev else mp.nstr(v / prev[key], 4)
            row += " %-20s" % (mp.nstr(v, 6) + " (" + rat + ")")
        print(row)
        prev = {key: abs(R[key]) for key in ('Ap', 'R1b', 'R2')}
    print()
