# -*- coding: utf-8 -*-
"""
settle.py -- 用 sympy 把 B_a(F,G) 对单孤子 tau 精确算出来（保留 (x,t,y) 符号）。

F = 1 + cF E ,  G = 1 + cG E ,  E = exp(Sx + Rt + Ty)
B_a = D_x^2 + D_t + 2a D_x
精确结果应为 (cF + cG)(S^2 + R + 2aS) E。
"""
import sympy as sp

x, t, y, a, S, R, T = sp.symbols('x t y a S R T', real=True)
cF, cG = sp.symbols('cF cG', real=True)

E = sp.exp(S * x + R * t + T * y)
F = 1 + cF * E
G = 1 + cG * E


def bilin(F, G, mx=0, mt=0):
    tot = 0
    for i in range(mx + 1):
        for j in range(mt + 1):
            tot += (-1) ** (i + j) * sp.binomial(mx, i) * sp.binomial(mt, j) \
                * sp.diff(F, x, mx - i, t, mt - j) * sp.diff(G, x, i, t, j)
    return sp.expand(tot)


B = sp.expand(bilin(F, G, 2, 0) + bilin(F, G, 0, 1) + 2 * a * bilin(F, G, 1, 0))
Esub = {sp.exp(S * x + R * t + T * y): E}
Bs = sp.expand(B.subs(Esub))
print("B_a(F,G) =", sp.simplify(Bs))
print()
print("因子形式:", sp.factor(sp.simplify(Bs / E)))
print()
print("=> 当 cF + cG = 0 时恒为零。")
print("   但 (S^2+R+2aS) = (p+q)(p-q+2a):",
      sp.factor(S ** 2 + R + 2 * a * S))
print()

# 代入论文参数
p, q, aa = sp.symbols('p q aa', real=True)
Ssub = p + q
Rsub = q ** 2 - p ** 2
expr = sp.expand((S ** 2 + R + 2 * a * S).subs({S: Ssub, R: Rsub}))
print("S^2+R+2aS 代入 S=p+q, R=q^2-p^2 :", sp.factor(expr))
print("=> 除非 p-q+2a=0 或 p+q=0，否则需要 cF + cG = 0。")
print()
cFv = (-(p - aa) / (q + aa)) / (p + q)
cGv = 1 / (p + q)
print("cF =", sp.simplify(cFv))
print("cG =", sp.simplify(cGv))
print("cF + cG =", sp.simplify(cFv + cGv))
print("cF + cG = 0  <=>", sp.simplify(sp.solve(sp.numer(sp.together(cFv + cGv)),
                                                 aa)))
