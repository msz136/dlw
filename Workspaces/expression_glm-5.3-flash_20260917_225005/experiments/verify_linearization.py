# -*- coding: utf-8 -*-
"""Linearization of DLW (1)-(2) about constant background (u0, v0).

Perturbation: eps*U*exp(s t + i k x + i ell y), eps*V*exp(...).
Goal: derive exactly
  eq1: i*ell*s*U - k^2*V - (u0+2a)*k*ell*U = 0
  eq2: (s+i(u0+2a)k)*V + i*k*(v0+2*lam - k*ell)*U = 0
and hence (ell != 0):
  [s+i(u0+2a)k]^2 = k^4 - (v0+2*lam)*k^3/ell.
"""
import sympy as sp

s, k, el = sp.symbols('s k ell')
u0, v0, a, lam, U, V = sp.symbols('u0 v0 a lambda U V')

# first-order coefficient extraction done symbolically by substitution of
# u = u0 + U*E, v = v0 + V*E with E = exp(s t + i k x + i ell y) and linearization:
# d/dt u = s U E ; d/dy d/dt u = i ell s U E ; d2/dx2 v = -k^2 V E
# u u_xy -> u0 * (i k)(i ell) U E = -u0 k ell U E ; u_x u_y -> O(eps^2) drop
# 2 a u_xy -> -2 a k ell U E
L1 = sp.I*el*s*U - k**2*V - (u0 + 2*a)*k*el*U
# v_t = s V E ; (uv)_x = i k (u0 V + v0 U) E ; u_xxy = (i k)^3 ell U E = -i k^2 ell U E
# 2a v_x = 2a i k V E ; 2 lam u_x = 2 lam i k U E
L2 = s*V + sp.I*k*(u0*V + v0*U) - sp.I*k**2*el*U + 2*a*sp.I*k*V + 2*lam*sp.I*k*U
L2c = sp.simplify(sp.expand(L2 - ((s + sp.I*(u0 + 2*a)*k)*V + sp.I*k*(v0 + 2*lam - k*el)*U)))
print("eq2 collected form:", L2c == 0)

# dispersion: from L1 (ell != 0): U = k^2 V / (ell (i s - (u0+2a) k))
Uv = k**2*V/(el*(sp.I*s - (u0 + 2*a)*k))
# L2/V = 0 multiplied by (i s - (u0+2a)k)/i gives the dispersion identity
disc_lhs = sp.simplify(sp.expand(((sp.I*s - (u0 + 2*a)*k)/sp.I) * (L2.subs(U, Uv)/V)))
disc_rhs = (s + sp.I*(u0 + 2*a)*k)**2 - k**4 + (v0 + 2*lam)*k**3/el
disc = sp.simplify(sp.expand(disc_lhs - disc_rhs))
print("dispersion identity:", disc == 0)

# high-frequency: s/k^2 -> +/- 1 (ell fixed) => |s| ~ k^2 growth
sh = sp.solve(sp.Eq((s + sp.I*(u0 + 2*a)*k)**2, k**4 - (v0 + 2*lam)*k**3/el), s)
lims = [sp.simplify(sp.limit(si/k**2, k, sp.oo)) for si in sh]
print("s/k^2 ->", lims)

# numeric sanity with lambda = -2: solve dispersion for s, check L1=L2=0
val = {k: 1.3, el: -2.1, u0: 0.4, v0: 1.1, a: 2.0, lam: -2.0, V: -0.6}
sh_num = [si.subs(val) for si in sh]
for si in sh_num:
    Uv_num = complex(Uv.subs(val).subs(s, si).evalf())   # U from eq1 at this s
    r1 = complex(L1.subs(val).subs(s, si).subs(U, Uv_num).evalf())
    r2 = complex(L2.subs(val).subs(s, si).subs(U, Uv_num).evalf())
    print("s =", complex(si.evalf()), " U =", Uv_num,
          " L1 resid =", abs(r1), " L2 resid =", abs(r2))
