# -*- coding: utf-8 -*-
"""idcheck.py -- 用 sympy 与数值双重确定 Hirota 商恒等式。"""
import sympy as sp

x = sp.symbols('x')
F = sp.Function('F')(x)
G = sp.Function('G')(x)
lnF, lnG = sp.log(F), sp.log(G)

lhs = sp.diff(F, x, 2) * G - 2 * sp.diff(F, x) * sp.diff(G, x) + F * sp.diff(G, x, 2)
lhs_div = sp.simplify(lhs / (F * G))

A = sp.diff(lnF, x)          # (lnF)_x
B = sp.diff(lnG, x)
Axx = sp.diff(lnF, x, 2)     # (lnF)_xx
Bxx = sp.diff(lnG, x, 2)

print("lhs_div        =", sp.simplify(lhs_div))
print("A              =", sp.simplify(A))
print("B              =", sp.simplify(B))
print("Axx            =", sp.simplify(Axx))
print("Bxx            =", sp.simplify(Bxx))
print()
print("Axx+Bxx        =", sp.simplify(Axx + Bxx))
print("Axx+Bxx+A^2+B^2=", sp.simplify(Axx + Bxx + A**2 + B**2))
print("lhs_div-(Axx+Bxx+A^2+B^2) =", sp.simplify(lhs_div - (Axx + Bxx + A**2 + B**2)))
print()
# 关键： (lnF)_xx 的两种写法
print("Axx - (Fxx/F-(Fx/F)^2) =", sp.simplify(Axx - (sp.diff(F, x, 2) / F - (sp.diff(F, x) / F)**2)))
print("Axx - Fxx/F             =", sp.simplify(Axx - sp.diff(F, x, 2) / F))
