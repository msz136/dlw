# -*- coding: utf-8 -*-
"""
derive1.py -- 严格重推：DLW-1 是否等价于 (7) 的 y 导数？

记 psi := ln(fg), th := ln(f/g)。
    u = 2 th_x ,  v = 2 psi_xy
D = D_x^2 + D_t + 2a D_x 作用在 f.g 上，用对数导数展开：
    (D_x^2 f.g)/(fg) = psi_xx + th_x^2
    (D_t   f.g)/(fg) = psi_t
    (D_x   f.g)/(fg) = th_x
故  (7) <=>  psi_xx + th_x^2 + psi_t + 2a th_x = 0      ... (E7)
本脚本用 sympy 在**一般**符号函数 th(x,t,y), psi(x,t,y) 上验证：
    DLW-1  ==  [∂_y(E7) 的展开] + 2 th_x * (E6 的对数形式) + 2a*∂_y(E7) 修正项?
即把 DLW-1 化成 (E7) 及其导数的组合。
"""
import sympy as sp

x, t, y, a, lam = sp.symbols('x t y a lam', real=True)
th = sp.Function('theta')(x, t, y)
ps = sp.Function('psi')(x, t, y)


def d(e, *v):
    for s, n in v:
        e = sp.diff(e, s, n)
    return e


thx = d(th, (x, 1))
thy = d(th, (y, 1))
tht = d(th, (t, 1))
thxx = d(th, (x, 2))
thxy = d(th, (x, 1), (y, 1))
thyy = d(th, (y, 2))
thxxt = d(th, (x, 2), (t, 1))
thxxy = d(th, (x, 2), (y, 1))
thxyy = d(th, (x, 1), (y, 2))
thxyt = d(th, (x, 1), (y, 1), (t, 1))

psxx = d(ps, (x, 2))
psxy = d(ps, (x, 1), (y, 1))
psxxy = d(ps, (x, 2), (y, 1))
psxxxy = d(ps, (x, 3), (y, 1))
psxyt = d(ps, (x, 1), (y, 1), (t, 1))

u = 2 * thx
v = 2 * psxy
uyt = 2 * thxyt
uxy = 2 * thxxy
ux = 2 * thxx
uy = 2 * thxy
vxx = 2 * psxxxy

DLW1 = uyt + vxx + u * uxy + ux * uy + 2 * a * uxy

# E7 := psi_xx + th_x^2 + psi_t + 2a th_x
E7 = psxx + thx ** 2 + d(ps, (t, 1)) + 2 * a * thx

print("DLW-1 =", sp.simplify(DLW1))
print()
print("∂_y(E7) =", sp.simplify(d(E7, (y, 1))))
print()
print("DLW-1 - 2 ∂_y(E7) =", sp.simplify(DLW1 - 2 * d(E7, (y, 1))))
print()
print("DLW-1 - ∂_y(E7) =", sp.simplify(DLW1 - d(E7, (y, 1))))
print()
# 猜测：DLW-1 = ∂_y(E7) + 2 th_x * (E7)_x  ?
print("DLW-1 - [∂_y(E7) + 2 th_x (E7)_x] =",
      sp.simplify(DLW1 - d(E7, (y, 1)) - 2 * thx * d(E7, (x, 1))))
print()
print("DLW-1 - [∂_y(E7) + 2 th_x ∂_x(psi_xx+psi_t) + ...] 试 2 th_x E7_x:")
print("   E7_x =", sp.simplify(d(E7, (x, 1))))
