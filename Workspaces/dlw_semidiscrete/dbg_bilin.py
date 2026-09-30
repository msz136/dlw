# -*- coding: utf-8 -*-
"""dbg_bilin.py -- 手工核对 (7)_h 与 (N1) 的精确性（N=1 显式公式）。"""
import mpmath as mp
from itertools import permutations
from sympy import symbols, Rational, exp, diff, simplify, expand, nsimplify, log, Symbol, S

mp.mp.dps = 40

N = 1
a = Rational(4)
p = Rational(2, 3)
q = Rational(-18, 5)
h = Rational(1, 4)
d = h / 2
x0 = Rational(1, 5)
t0 = Rational(2, 7)

x, t = symbols('x t', real=True)
lam_p = (p - a + d) / (p - a - d)
lam_q = (q + a + d) / (q + a - d)
chi = lam_p * lam_q
print("lam_p =", lam_p, " lam_q =", lam_q, " chi =", chi, " = ", nsimplify(chi))

# tau 的显式（j 为格点）:  m_00 = 1 + coef * chi^j * exp((p+q)x + (q^2-p^2)t)
def tau(n, j, s, mu):
    coef = (-(p - s) / (q + s)) ** n / (p + q)
    lp = (p - a + d) / (p - a - d)
    lq = (q + a + d) / (q + a - d)
    coef = coef * (lp * lq) ** j
    return 1 + coef * exp((p + q) * x + (q ** 2 - p ** 2) * t)

j = 1
F = tau(1, j, a - d, a)
G = tau(0, j, a, a)
print("\nF =", F)
print("G =", G)

Dx2 = lambda A, B: diff(A, x, 2) * B - 2 * diff(A, x) * diff(B, x) + A * diff(B, x, 2)
Dt = lambda A, B: diff(A, t) * B - A * diff(B, t)
Dx = lambda A, B: diff(A, x) * B - A * diff(B, x)

E7 = Dx2(F, G) + Dt(F, G) + 2 * (a - d) * Dx(F, G)
print("\n(7)_h =", simplify(E7))

G1 = tau(0, j + 1, a, a)
E6 = Dx2(F, G1) + Dt(F, G1) + 2 * (a + d) * Dx(F, G1)
print("(6)_h =", simplify(E6))
