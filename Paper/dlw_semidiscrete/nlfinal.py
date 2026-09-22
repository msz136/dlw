# -*- coding: utf-8 -*-
"""
nlfinal.py -- DLW 半离散系统：双线性层 -> **非线性层**（权威验证，定稿）。

================================================================================
[0] 引擎 jet3.py
    tau 的精确三变量 (x,t,y) 指数单项式表示，任意阶导数精确。
    交错对称配对（d = h/2, mu = a）：
        F_j = tau_1(j ; s = a-d, mu = a) ,   G_j = tau_0(j ; s = a, mu = a)
    al := lnF_j, be := lnG_j（用 (d^m tau)/tau 的有理量，规避 ln 的分支）。

[1] 精确双线性恒等式（engine2.py / certify.py 独立验证；本文件复算 = 0）
        (7)_h :  B_{a-d} F_j . G_j     = 0
        (6)_h :  B_{a+d} F_j . G_{j+1} = 0 ,   B_s := D_x^2 + D_t + 2 s D_x

[2] Hirota 商恒等式（idcheck3.py 用 sympy 严格证明 (c1,c2,c3)=(1,1,1)）
        D_x^2 F.G/(FG) = (lnF)_{xx} + (lnG)_{xx} + [(lnF)_x - (lnG)_x]^2
        D_t  F.G/(FG) = (lnF)_t - (lnG)_t
        D_x  F.G/(FG) = (lnF)_x - (lnG)_x
    其中 (lnF)_{xx} = F_{xx}/F - (F_x/F)^2。交叉项系数为 **+1**。

[3] 势函数
        theta_j = al_j - be_j ,   Psi_j = al_j + be_j
    由 [2] 与 (7)_h/(F_jG_j)，参数 s := a - d：
        (A)  Psi_{j,xx} + theta_{j,x}^2 + theta_{j,t} + 2 s theta_{j,x} = 0
    由 (6)_h/(F_jG_{j+1})，Theta_j := al_j - be_{j+1}：
        (B)  Phi_{j,xx} + Theta_{j,x}^2 + Theta_{j,t} + 2(a+d) Theta_{j,x} = 0
    把 (B) 中的 j 换成 j-1（并注意 Theta_{j-1} = theta 与 G_j 配对）后，
    它与 (A) 是同一方程的两个位点取值。

[4] 物理变量
        u_j = 2 theta_{j,x} ,   w_j = 2 Psi_{j,x}
    (A) 乘 2：
        (A') u_{j,t} + w_{j,x} + u_j^2/2 + 2(a-d) u_j = 0

[5] 连续极限（nlcont.py）
    (A)_h 残差恒为 0；把 a-d 换成 a 后残差 = O(h)（比值 0.5/h 减半）
    => h -> 0 恢复连续非线性方程 Psi_xx + theta_x^2 + theta_t + 2a theta_x = 0
================================================================================
"""
import mpmath as mp

import jet3

mp.mp.dps = 90
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(0)


def val(dd, mx=0, mt=0, my=0, x0=X0, t0=T0, y0=Y0):
    return jet3.ev(jet3.deriv(dd, mx, mt, my), x0, t0, y0)


def L(dd, mx=0, mt=0):
    return val(dd, mx, mt) / val(dd)


def l2(dd):
    return val(dd, 2) / val(dd) - L(dd, 1) ** 2


CASES = [
    (1, mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4),
    (1, mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)], mp.mpf(1) / 4),
    (1, mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)], mp.mpf(1) / 8),
]


def verify(N, a, p, q, h, j0, show=True):
    d = h / 2
    F = lambda j: jet3.tau3(N, a, p, q, h, 1, a - d, a, j)
    G = lambda j: jet3.tau3(N, a, p, q, h, 0, a, a, j)
    al = lambda j, mx=0, mt=0: L(F(j), mx, mt)
    be = lambda j, mx=0, mt=0: L(G(j), mx, mt)
    th = lambda j, mx=0, mt=0: al(j, mx, mt) - be(j, mx, mt)
    Th = lambda j, mx=0, mt=0: al(j, mx, mt) - be(j + 1, mx, mt)
    s = a - d

    R = {}
    R['[1] (7)_h'] = jet3.ev(jet3.Bs3(F(j0), G(j0), a - d))
    R['[1] (6)_h'] = jet3.ev(jet3.Bs3(F(j0), G(j0 + 1), a + d))
    X, Y = F(j0), G(j0)
    D = (val(X, 2) * val(Y) - 2 * val(X, 1) * val(Y, 1) + val(X) * val(Y, 2)) \
        / (val(X) * val(Y))
    R['[2] 商恒等式'] = D - (l2(X) + l2(Y) + (L(X, 1) - L(Y, 1)) ** 2)
    R['[3] (A)'] = (l2(F(j0)) + l2(G(j0))) + th(j0, 1) ** 2 + th(j0, 0, 1) \
        + 2 * s * th(j0, 1)
    R['[4] (B)'] = (l2(F(j0)) + l2(G(j0 + 1))) + Th(j0, 1) ** 2 + Th(j0, 0, 1) \
        + 2 * (a + d) * Th(j0, 1)
    R["[5] (A') u_t+w_x+u^2/2+2(a-d)u"] = 2 * R['[3] (A)']
    if show:
        print("  N=%d a=%-7s h=%-6s j=%d" % (N, mp.nstr(a, 6), mp.nstr(h, 5), j0))
        for k, vv in R.items():
            flag = '' if abs(vv) < mp.mpf('1e-40') else '  <-- 非零'
            print("      %-28s = %s%s" % (k, mp.nstr(vv, 5), flag))
    return R


if __name__ == '__main__':
    for (N, a, p, q, h) in CASES:
        for j0 in (0, 1, 2):
            verify(N, a, p, q, h, j0)
        print()
