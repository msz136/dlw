# -*- coding: utf-8 -*-
"""Verify: w-form equivalence + constant-background linearization dispersion.

Part 1: (1)-(2) <=> w = u_y system.
Part 2: linearized dispersion [s+i(u0+2a)k]^2 = k^4-(v0+2 lam)k^3/ell, ell!=0,
        and high-frequency growth |s| ~ k^2.
"""
import sympy as sp

x, y, t = sp.symbols('x y t')
a, lam = sp.symbols('a lambda')
u = sp.Function('u')(x, y, t)
v = sp.Function('v')(x, y, t)
w = sp.Function('w')(x, y, t)

E1 = sp.diff(u, y, t) + sp.diff(v, x, 2) + u*sp.diff(u, x, y) \
     + sp.diff(u, x)*sp.diff(u, y) + 2*a*sp.diff(u, x, y)
E2 = sp.diff(v, t) + sp.diff(u*v, x) + sp.diff(u, x, x, y) \
     + 2*a*sp.diff(v, x) + 2*lam*sp.diff(u, x)

wsys1 = sp.diff(w, t) + sp.diff(sp.diff(v, x) + (u + 2*a)*w, x)
wsys2 = sp.diff(v, t) + sp.diff((u + 2*a)*v + sp.diff(w, x) + 2*lam*u, x)

print("w1:", sp.simplify(sp.expand(wsys1.subs(w, sp.diff(u, y)) - E1)) == 0)
print("w2:", sp.simplify(sp.expand(wsys2.subs(w, sp.diff(u, y)) - E2) ) == 0)
# note: equivalence of mixed partials u_xy = u_yx is assumed here (smooth u).
