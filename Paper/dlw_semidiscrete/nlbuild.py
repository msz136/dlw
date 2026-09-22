# -*- coding: utf-8 -*-
"""
nlbuild.py -- 按「参数移位」离散化，把双线性 (7)_h / (6)_h 转化为非线性系统。

--------------------------------------------------------------------------------
离散化（沿用既有构造，不再改动）
    d = h/2 ,  lam(z) = (z+d)/(z-d)
    F_j := tau_1(j ; s = a-d) ,   G_j := tau_0(j)
    结构恒等式：F_j = tau_1(j; a-d) = tau_1(j+1; a+d)
--------------------------------------------------------------------------------
物理变量（本文件要确定的就是这两个）
    u_j := 2 (ln(F_j/G_j))_x
    v_j := 2 (ln(F_j G_j))_{xy}
    th_j := ln(F_j/G_j) ,  Psi_j := ln(F_j G_j)
    =>  th_{j,x} = u_j/2 ,  th_{j,t} = u_{j,t}/2 ,  Psi_{j,xx} = v_{j,x}/2
--------------------------------------------------------------------------------
由 (7)_h 得到的非线性恒等式（τ 级，精确）
    (A)_h :  Psi_{j,xx} + th_{j,x}^2 + th_{j,t} + 2(a-d) th_{j,x} = 0
等价物理形式
    (A')  :  v_{j,x} + u_j^2/2 + u_{j,t} + 2(a-d) u_j = 0
由 (6)_h 得到的非线性恒等式
    (B)_h :  Phi_{j,xx} + Th_{j,x}^2 + Th_{j,t} + 2(a+d) Th_{j,x} = 0
      Phi_j = ln(F_j G_{j+1}) ,  Th_j = ln(F_j/G_{j+1})
      Th_j = (Psi_j - Psi_{j+1})/2 + (th_j + th_{j+1})/2
      Phi_j = (Psi_j + Psi_{j+1})/2 + (th_j - th_{j+1})/2
--------------------------------------------------------------------------------
本脚本做三件事：
  [1] 验证 (A)_h、(B)_h 在 τ 级、多点、多 h 下成立（并给出残差真值，不用单点）
  [2] 给出 u_j, v_j 的显式表达，并检查 u_j - u_{j+1} 等结构关系
  [3] 检验离散非线性残差随 h 的标度
"""
import mpmath as mp

import jet3

mp.mp.dps = 120

PTS = [
    (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3),
    (mp.mpf(1) / 3, mp.mpf(1) / 5, mp.mpf(1) / 7),
    (mp.mpf(2) / 9, mp.mpf(3) / 11, mp.mpf(-5) / 13),
    (mp.mpf('1.234'), mp.mpf('0.567'), mp.mpf('0.891')),
]


def ev(d, pt):
    x0, t0, y0 = pt
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


def L(d, mx=0, mt=0, my=0, pt=None):
    """(d^m tau)/tau ，规范不变量。"""
    return ev(jet3.deriv(d, mx, mt, my), pt) / ev(d, pt)


def maxrel(res, parts, pts=PTS):
    """在多点上的最大相对残差。"""
    worst = mp.mpf(0)
    where = None
    for pt in pts:
        sc = max(abs(ev(dd, pt)) for dd in parts) or mp.mpf(1)
        r = abs(ev(res, pt)) / sc if not isinstance(res, tuple) else abs(res)
        if r > worst:
            worst, where = r, pt
    return worst, where


# ---------------------------------------------------------------- 构造
def build(a, p, q, h, j):
    d = h / 2
    F = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
    G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
    G1 = jet3.tau3(1, a, p, q, h, 0, a, a, j + 1)
    return F, G, G1


def A_res(F, G, s, pt):
    """(A)_h = Psi_xx + th_x^2 + th_t + 2s th_x ，直接用 tau 的对数导数算。"""
    lF2 = L(F, 2, 0, 0, pt) - L(F, 1, 0, 0, pt) ** 2
    lG2 = L(G, 2, 0, 0, pt) - L(G, 1, 0, 0, pt) ** 2
    th_x = L(F, 1, 0, 0, pt) - L(G, 1, 0, 0, pt)
    th_t = L(F, 0, 1, 0, pt) - L(G, 0, 1, 0, pt)
    return (lF2 + lG2) + th_x ** 2 + th_t + 2 * s * th_x


def B_res(F, G1, a, d, pt):
    lF2 = L(F, 2, 0, 0, pt) - L(F, 1, 0, 0, pt) ** 2
    lG2 = L(G1, 2, 0, 0, pt) - L(G1, 1, 0, 0, pt) ** 2
    Th_x = L(F, 1, 0, 0, pt) - L(G1, 1, 0, 0, pt)
    Th_t = L(F, 0, 1, 0, pt) - L(G1, 0, 1, 0, pt)
    return (lF2 + lG2) + Th_x ** 2 + Th_t + 2 * (a + d) * Th_x


print("=" * 80)
print("[1] (A)_h 与 (B)_h 在 τ 级、多点上的残差（真值，非单点）")
print("=" * 80)
CASES = [
    (mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5]),
    (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)]),
    (mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)]),
]
for (a, p, q) in CASES:
    for h in [mp.mpf(1) / 4, mp.mpf(1) / 8]:
        d = h / 2
        F, G, G1 = build(a, p, q, h, 1)
        ra = max(abs(A_res(F, G, a - d, pt)) for pt in PTS)
        rb = max(abs(B_res(F, G1, a, d, pt)) for pt in PTS)
        print("  a=%-7s h=%-6s  |(A)_h|max=%-12s |(B)_h|max=%-12s"
              % (mp.nstr(a, 6), mp.nstr(h, 5), mp.nstr(ra, 4), mp.nstr(rb, 4)))
    print()

print("=" * 80)
print("[2] 物理变量 u_j, v_j 与结构关系")
print("=" * 80)
a, p, q, h = mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4
d = h / 2
pt = PTS[0]
print("  a=%s h=%s 点=%s" % (mp.nstr(a, 6), mp.nstr(h, 5),
                            tuple(mp.nstr(z, 4) for z in pt)))
for j in (0, 1, 2):
    F, G, G1 = build(a, p, q, h, j)
    u = 2 * (L(F, 1, 0, 0, pt) - L(G, 1, 0, 0, pt))
    # v_j = 2 Psi_{j,xy} ; Psi_{j,xy} = (lnF + lnG)_{xy}
    v = 2 * ((L(F, 1, 1, 0, pt) - L(F, 1, 0, 0, pt) * L(F, 0, 1, 0, pt))
             + (L(G, 1, 1, 0, pt) - L(G, 1, 0, 0, pt) * L(G, 0, 1, 0, pt)))
    # (A') 残差
    r = (v * 0  # v_{j,x} 稍后单独算
         )
    print("  j=%d  u_j = %-22s v_j = %-22s" % (j, mp.nstr(u, 10), mp.nstr(v, 10)))
