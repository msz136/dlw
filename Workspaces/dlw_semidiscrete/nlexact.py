# -*- coding: utf-8 -*-
"""
nlexact.py -- 精确有理数（jet4.py）+ 指数和恒零判定（exactexp.py）
              重新复核 DLW 半离散非线性层的全部恒等式。

判零不依赖浮点噪声：每项都是 Fraction，恒零 = 逐方向系数和精确为 0。
"""
from fractions import Fraction as Fr

import exactexp as EX
import jet4 as J


def Z(name, items):
    ok, info = EX.is_identically_zero(items)
    print("  %-40s %s" % (name, "== 0  (精确)" if ok else "非零: %s" % (info,)))
    return ok


CASE = dict(a=Fr(4), p=[Fr(2, 3)], q=[Fr(-18, 5)], h=Fr(1, 4))


def mk(a, p, q, h, j):
    d = h / 2
    return (J.tau3(1, a, p, q, h, 1, a - d, a, j),
            J.tau3(1, a, p, q, h, 0, a, a, j),
            J.tau3(1, a, p, q, h, 0, a, a, j + 1))


print("=" * 78)
print("A. 双线性方程 (7)_h, (6)_h")
print("=" * 78)
ok = True
for j in (0, 1, 2, 3):
    F, G, G1 = mk(CASE['a'], CASE['p'], CASE['q'], CASE['h'], j)
    ok &= Z("j=%d  (7)_h = B_{a-d} F_j.G_j" % j,
            J.Bs3(F, G, CASE['a'] - CASE['h'] / 2).items())
    ok &= Z("j=%d  (6)_h = B_{a+d} F_j.G_{j+1}" % j,
            J.Bs3(F, G1, CASE['a'] + CASE['h'] / 2).items())

print()
print("=" * 78)
print("B. Hirota 商恒等式，通分后 (H1)：  F^2G^2(H1) = 0")
print("=" * 78)
print("  (H1): D_x^2 F.G/(FG) = (lnF)_xx+(lnG)_xx+[(lnF)_x-(lnG)_x]^2")
for j in (0, 1, 2):
    F, G, _ = mk(CASE['a'], CASE['p'], CASE['q'], CASE['h'], j)
    Fx, Fxx = J.deriv(F, 1), J.deriv(F, 2)
    Gx, Gxx = J.deriv(G, 1), J.deriv(G, 2)
    FG = J.mul(F, G)
    lhs = J.mul(J.bilin(F, G, 2, 0), FG)
    t1 = J.mul(J.mul(G, G), J.add(J.mul(Fxx, F), J.scale(J.mul(Fx, Fx), -1)))
    t2 = J.mul(J.mul(F, F), J.add(J.mul(Gxx, G), J.scale(J.mul(Gx, Gx), -1)))
    cr = J.add(J.mul(Fx, G), J.scale(J.mul(F, Gx), -1))
    rhs = J.add(J.add(t1, t2), J.mul(cr, cr))
    ok &= Z("j=%d  F^2G^2 (H1)" % j, J.add(lhs, J.scale(rhs, -1)).items())

print()
print("=" * 78)
print("C. 势函数方程 (A)_h：(FG)^2 通分后 = 0")
print("=" * 78)
print("  (A)_h: Psi_xx + theta_x^2 + theta_t + 2(a-d) theta_x = 0")
print("  用 (H1)(H2) 的推论: D_x^2 F.G/(FG) + theta_t + 2(a-d) theta_x  [注:(H1) 已含 theta_x^2]")
for j in (0, 1, 2):
    F, G, _ = mk(CASE['a'], CASE['p'], CASE['q'], CASE['h'], j)
    Ft, Gt = J.deriv(F, 0, 1), J.deriv(G, 0, 1)
    Fx, Gx = J.deriv(F, 1), J.deriv(G, 1)
    FG = J.mul(F, G)
    # (A)_h 的 (FG) 形式：分母 FG
    #   (A)_h * (FG)^2 = (FG)*[D_x^2 F.G]  +  (FG)*[G Ft - F Gt]*? ...
    # 直接：theta_t = Ft/F - Gt/G = (Ft G - F Gt)/(FG)
    #      theta_x = (Fx G - F Gx)/(FG)
    #  故 (A)_h*(FG)^2 = [D_x^2 F.G/(FG)]*(FG)^2 + theta_x^2*(FG)^2
    #                   + theta_t*(FG)^2 + 2s theta_x*(FG)^2
    # 而 D_x^2 F.G/(FG) 需要 (H1) 的右端；用 A 部分已证的等价无分母式：
    #   D_x^2 F.G = (1/(FG))*[G^2(Fxx F - Fx^2)+F^2(Gxx G - Gx^2)+(Fx G - F Gx)^2]
    # 这里我们改写为：判 (A)_h 等价于判
    #   N := D_x^2 F.G * (FG)  +  (Ft G - F Gt)*(FG)
    #        + 2s (Fx G - F Gx)*(FG)  + (Fx G - F Gx)^2
    # （因为 theta_x^2*(FG)^2 = (Fx G - F Gx)^2）
    s = CASE['a'] - CASE['h'] / 2
    DxxFG = J.mul(J.bilin(F, G, 2, 0), FG)
    th_t = J.add(J.mul(Ft, G), J.scale(J.mul(F, Gt), -1))
    th_x = J.add(J.mul(Fx, G), J.scale(J.mul(F, Gx), -1))
    N = J.add(J.add(DxxFG, J.mul(th_t, FG)),
              J.add(J.scale(J.mul(th_x, FG), 2 * s), J.mul(th_x, th_x)))
    ok &= Z("j=%d  (A)_h 的通分残差" % j, N.items())

print()
print("=" * 78)
print("D. 结论")
print("=" * 78)
print("  全部恒零（精确）" if ok else "  存在非零项 —— 需要检查上面的定义")
