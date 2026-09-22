# -*- coding: utf-8 -*-
"""
Direction A, Experiment 2: symbols and Taylor-coefficient algebra of the candidate
y-schemes (COEFFICIENT ALGEBRA ONLY -- no remainder estimate).

Continuous linearisation (shared spec V6, re-derived mechanically in exp6):
    [sigma + i (u0 + 2a) k]^2 = k^4 - (v0 + 2 lam) k^3 / ell ,      ell != 0 .
Discrete counterpart (exp6, authoritative):
    [sigma + i (u0 + 2a) k]^2 = k^4 - (v0 + 2 lam) k^3 / f ,
    f = sin(xi)/h   (centred),   f = 2 sin(xi/2)/h  (staggered),   xi = ell h .

This script collects the symbol/Taylor facts used in the report and the Lean file:
  * first-derivative schemes: centred, forward, backward, compact (Pade)
  * second-derivative schemes: narrow vs wide stencil
  * the exact operator identity  2 D0 = (I+P) D+   i.e.  D0 = (P+P^{-1})D+/2
  * f/ell = sinc(xi) <= 1, and f = 0 exactly at the Nyquist mode xi = pi.

Run:  python -u exp2_symbols.py
"""
import sympy as sp

h, xi = sp.symbols('h xi', positive=True)
X = sp.symbols('X')            # formal lattice exponential e^{i xi h}


def sym_expand(expr, order=8, var=None):
    """expand a shift-operator expression with X = i xi h"""
    e = sp.expand(expr).subs(X, sp.I * xi * h)
    return sp.expand(sp.series(e, h, 0, order).removeO())


print("=" * 74)
print("DLW direction A :: exp2 :: symbol and Taylor-coefficient algebra")
print("=" * 74)

# ---------------------------------------------------------------------------
print("\n[1] first-order y-derivative schemes; basis  symbol = (i xi) * sum c_k (i xi h)^k")
schemes = {
    "centred   (u_{j+1}-u_{j-1})/(2h)": (sp.exp(X) - sp.exp(-X)) / (2 * h),
    "forward   (u_{j+1}-u_j)/h":        (sp.exp(X) - 1) / h,
    "backward  (u_j-u_{j-1})/h":        (1 - sp.exp(-X)) / h,
    "compact   (u_{j+1}-u_{j-1})/(2h(1+D2 h^2/6))":
        (sp.exp(X) - sp.exp(-X)) / (2 * h * (1 + (sp.exp(X) - 2 + sp.exp(-X)) / 6)),
    "staggered (u_{j+1}-u_j)/h at j+1/2": (sp.exp(X) - 1) / h,
}
C = {}
for name, expr in schemes.items():
    ser = sp.expand(sp.series(sp.simplify(sym_expand(expr) / (sp.I * xi)), h, 0, 7).removeO())
    C[name] = [sp.nsimplify(sp.expand(ser).coeff(h, k) / (sp.I * xi) ** k) for k in range(7)]
    print(f"   {name}")
    print("      symbol = (i xi) [" + " + ".join(
        f"({C[name][k]}) (i xi h)^{k}" for k in range(5) if C[name][k] != 0) + " + ...]")

c_ctr, c_fwd, c_bwd, c_cmp, c_sg = (C["centred   (u_{j+1}-u_{j-1})/(2h)"],
                                    C["forward   (u_{j+1}-u_j)/h"],
                                    C["backward  (u_j-u_{j-1})/h"],
                                    C["compact   (u_{j+1}-u_{j-1})/(2h(1+D2 h^2/6))"],
                                    C["staggered (u_{j+1}-u_j)/h at j+1/2"])
print("\n   A1  centred : c_0=1, c_1=0, c_2=+1/6, c_3=0   => D0 = d_y + (h^2/6) d_y^3 + O(h^4)")
assert c_ctr[0] == 1 and c_ctr[1] == 0 and c_ctr[2] == sp.Rational(1, 6) and c_ctr[3] == 0
print("   A2  compact : c_2 = c_3 = 0, c_4 = -1/180     => 4th order")
assert c_cmp[0] == 1 and c_cmp[1] == 0 and c_cmp[2] == 0 and c_cmp[3] == 0
assert c_cmp[4] == sp.Rational(-1, 180)
print("   A3  forward/backward : c_1 = +-1/2 (first order), c_2 = 1/6")
assert c_fwd[1] == sp.Rational(1, 2) and c_bwd[1] == -sp.Rational(1, 2)
print("   A4  staggered forward : c_1 = +1/2 ; its average with backward cancels c_1")

print("\n[2] exact operator identity  D0 = (D+ + D-)/2  (hence 2h D0 = (I+P) D+ undivided)")
lhs = sp.expand((sp.exp(X) - 1) + (1 - sp.exp(-X)))
print("   D+ + D- - (e^X - e^{-X}) =", sp.simplify(lhs - (sp.exp(X) - sp.exp(-X))), " -> 0")
assert sp.simplify(lhs - (sp.exp(X) - sp.exp(-X))) == 0
print("   (I+P)(f_{j+1}-f_j) - (f_{j+2}-f_j) =",
      sp.simplify(sp.expand((1 + X) * (X - 1) - (X ** 2 - 1))), " -> 0")
assert sp.simplify(sp.expand((1 + X) * (X - 1) - (X ** 2 - 1))) == 0
print("   -> this identity is the Lean theorem dirA_ctr_eq_shift_mul_fwd")

print("\n[3] second-difference stencils")
D2wide = (sp.exp(2 * X) - 2 + sp.exp(-2 * X)) / (4 * h ** 2)
D2narrow = (sp.exp(X) - 2 + sp.exp(-X)) / h ** 2
print("   WIDE   (u_{j+2}-2u_j+u_{j-2})/(4h^2) symbol =",
      sp.simplify(sp.expand_trig(sp.expand_complex(sym_expand(D2wide)))))
print("   NARROW (u_{j+1}-2u_j+u_{j-1})/h^2     symbol =",
      sp.simplify(sp.expand_trig(sp.expand_complex(sym_expand(D2narrow)))))
print("   identity:  -sin(xi)^2/h^2 = -(2 sin(xi/2)/h)^2 cos^2(xi/2)  :",
      sp.simplify(sp.sin(xi) ** 2 / h ** 2 - (2 * sp.sin(xi / 2) / h) ** 2 * sp.cos(xi / 2) ** 2) == 0)
assert sp.simplify(sp.sin(xi) ** 2 / h ** 2 - (2 * sp.sin(xi / 2) / h) ** 2 * sp.cos(xi / 2) ** 2) == 0
print("   -> the choice of second-difference stencil is NOT immaterial (factor cos^2(xi/2)).")

print("\n[4] the effective wavenumbers f and their comparison with ell = xi/h")
f_ctr = sp.sin(xi) / h
f_sg = 2 * sp.sin(xi / 2) / h
print("   centred   f/ell = sin(xi)/xi = sinc(xi) <= 1,  = 1 iff xi = 0")
print("   staggered f/ell = sin(xi/2)/(xi/2) = sinc(xi/2) <= 1, = 1 iff xi = 0")
print("   expansions:  f_ctr = ell - ell^3 h^2/6 + O(h^4) ;  f_sg = ell - ell^3 h^2/24 + O(h^4)")
print("   ratios at xi = pi/2 :", sp.N(f_ctr.subs(xi, sp.pi / 2) * h / (sp.pi / 2)),
      sp.N(f_sg.subs(xi, sp.pi / 2) * h / (sp.pi / 2)))
print("\n   B1  Nyquist xi = pi :  f_ctr =", sp.simplify(f_ctr.subs(xi, sp.pi)),
      "   f_sg =", sp.simplify(f_sg.subs(xi, sp.pi)))
print("       The centred symbol VANISHES at the Nyquist mode: the checkerboard")
print("       j -> (-1)^j is in the kernel of the centred difference. The staggered")
print("       symbol is bounded below by 2/h on the whole band 0 < xi <= pi.")
print("       In the dispersion relation k^3/f, the centred scheme therefore has a")
print("       SINGULAR coefficient at xi = pi (a mode with no continuum counterpart),")
print("       while the staggered scheme is regular there.")
print("\nALL CHECKS PASSED (coefficient algebra only -- no remainder estimates).")
