# -*- coding: utf-8 -*-
"""
idcheck3.py -- sympy 严格判定 Hirota 商恒等式的交叉项系数。

对任意符号 F(x), G(x)，令 A = (lnF)_x, B = (lnG)_x，
    D := (F_xx G - 2 F_x G_x + F G_xx)/(F G)
解出唯一的 (c1,c2,c3)，使
    D = c1 (lnF)_xx + c2 (lnG)_xx + c3 (A - B)^2 .
结论： (c1,c2,c3) = (1,1,1)。
"""
import sympy as sp

x = sp.symbols('x')
F = sp.Function('F')(x)
G = sp.Function('G')(x)
Fx, Gx = sp.diff(F, x), sp.diff(G, x)
Fxx, Gxx = sp.diff(F, x, 2), sp.diff(G, x, 2)

A, B = Fx / F, Gx / G
lnF_xx = Fxx / F - A ** 2
lnG_xx = Gxx / G - B ** 2
D = (Fxx * G - 2 * Fx * Gx + F * Gxx) / (F * G)

c1, c2, c3 = sp.symbols('c1 c2 c3')
num = sp.together(D - (c1 * lnF_xx + c2 * lnG_xx + c3 * (A - B) ** 2)).as_numer_denom()[0]
poly = sp.Poly(sp.expand(num), Fxx, Gxx)
print("按 (F_xx, G_xx) 的系数：")
for mono, coef in zip(poly.monoms(), poly.coeffs()):
    print("   ", mono, "->", sp.simplify(coef))
sol = sp.solve(poly.coeffs(), [c1, c2, c3], dict=True)
print("唯一解 (c1,c2,c3) =", sol)

# 直接验证
print("D - [(lnF)_xx+(lnG)_xx+(A-B)^2] =",
      sp.simplify(D - lnF_xx - lnG_xx - (A - B) ** 2))
print("D - [(lnF)_xx+(lnG)_xx]         =",
      sp.simplify(D - lnF_xx - lnG_xx))
