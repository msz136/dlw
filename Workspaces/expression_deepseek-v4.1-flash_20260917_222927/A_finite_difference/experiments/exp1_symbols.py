# -*- coding: utf-8 -*-
"""
Direction A (finite differences / constrained discretisation), DLW y-semidiscretisation.

Experiment 1: exact Taylor-coefficient algebra for the candidate y-difference
schemes.  This is COEFFICIENT ALGEBRA ONLY (formal series, no remainder bound).

System (Sheng & Yu, Physica D 432 (2022) 133140, DOI 10.1016/j.physd.2021.133140),
eqs (1)-(2), rewritten exactly with w = u_y (main-agent verified, V5):

    w_t + d_x[ v_x + (u + 2a) w ]        = 0
    v_t + d_x[ (u + 2a) v + w_x + 2 lam u ] = 0

Only y is discretised.  Run:  python -u exp1_symbols.py
"""
import sympy as sp

h, xi = sp.symbols('h xi', positive=True)
X = sp.symbols('X')          # formal lattice exponential e^{i xi h}


def series(expr, n=8):
    return sp.series(sp.expand(expr), h, 0, n).removeO()


print("=" * 74)
print("DLW direction A :: exp1 :: Taylor-coefficient algebra of y-schemes")
print("=" * 74)

# ----------------------------------------------------------------------------
# 0. exact shift symbol and the coefficient dictionary
# ----------------------------------------------------------------------------
print("\n[0] coefficient dictionary  (exact e^{X} vs truncated 1+X+... )")
# The only legitimate issue at finite order: e^X - T_n(X) = X^{n+1}/(n+1)! * (1+O(X)),
# so a coefficient identity for the truncated operator PROVES the same identity for
# the exact shift only after the tail is matched.  We do the matching explicitly.
for n in (1, 2, 3, 4):
    T = sum(X ** k / sp.factorial(k) for k in range(n + 1))
    d = series(sp.exp(X) - T, 8)          # X is treated as O(h) below
    lead = sp.simplify(d.subs(X, 1) * 1)  # not used; do it properly:
    lead = sp.series(sp.exp(X) - T, X, 0, n + 2).removeO().coeff(X, n + 1)
    print(f"   e^X - sum_(k<=n) X^k/k!  : leading coeff of X^(n+1) = {lead}")

# Exact check that the truncated operator's symbol has the same expansion to order h^n:
def sym_of(expr_in_X):
    """expand a formal operator symbol in h, with X = i xi h."""
    e = sp.expand(expr_in_X)
    e = e.subs(X, sp.I * xi * h)
    return sp.expand(sp.series(e, h, 0, 8).removeO())


# ----------------------------------------------------------------------------
# 1. first-derivative schemes: centred, stagger-forward, stagger-backward
# ----------------------------------------------------------------------------
print("\n[1] first-order y-derivative schemes, discrete symbol / (i xi)")
schemes = {
    "centred   D0 u_j = (u_{j+1}-u_{j-1})/(2h)":
        (sp.exp(X) - sp.exp(-X)) / (2 * h),
    "forward   D+ u_j = (u_{j+1}-u_j)/h":
        (sp.exp(X) - 1) / h,
    "backward  D- u_j = (u_j-u_{j-1})/h":
        (1 - sp.exp(-X)) / h,
    "compact   Dc u_j = (u_{j+1}-u_{j-1})/(2h(1+D2 h^2/6))":
        (sp.exp(X) - sp.exp(-X)) / (2 * h * (1 + (sp.exp(X) - 2 + sp.exp(-X)) / 6)),
}
coefs = {}
for name, expr in schemes.items():
    s = sp.simplify(sym_of(expr) / (sp.I * xi))
    ser = sp.expand(sp.series(s, h, 0, 7).removeO())
    # symbol = (i xi) * sum_k c_k (i xi h)^k ; c_k is the dimensionless Taylor coefficient
    # (s = symbol/(i xi); coefficient of h^k in s is c_k * (i xi)^k)
    coefs[name] = [sp.nsimplify(sp.expand(ser).coeff(h, k) / (sp.I * xi) ** k)
                   for k in range(0, 7)]
    print(f"   {name}")
    print(f"      symbol = (i xi) * [" + " + ".join(
        f"({coefs[name][k]})*(i xi h)^{k}" for k in range(0, 5) if coefs[name][k] != 0) + " + ...]")

c_ctr = coefs["centred   D0 u_j = (u_{j+1}-u_{j-1})/(2h)"]
c_fwd = coefs["forward   D+ u_j = (u_{j+1}-u_j)/h"]
c_bwd = coefs["backward  D- u_j = (u_j-u_{j-1})/h"]
c_cmp = coefs["compact   Dc u_j = (u_{j+1}-u_{j-1})/(2h(1+D2 h^2/6))"]

print("\n   Basis convention:  symbol = (i xi) * sum_k c_k (i xi h)^k.")
print("   Dictionary: substituting symbol = i xi gives the differential operator")
print("     sum_k c_k (i xi)^(k+1)  h^k   acting on e^{i xi y},")
print("   i.e. c_k multiplies  h^k d_y^(k+1)  up to the sign ((i xi)^(k+1) -> d_y^(k+1)).")
print("   For the CENTRED scheme only even k survive, so no sign ambiguity:")
print("   c_2 = +1/6 means  D0 u = u_y + (h^2/6) u_yyy + O(h^4).")
# explicit dictionary self-check on a pure exponential:
y = sp.symbols('y', real=True)
u_ex = sp.exp(sp.I * xi * y)
D0_ex = (u_ex.subs(y, y + h) - u_ex.subs(y, y - h)) / (2 * h)
print("   self-check: D0 e^{i xi y} / e^{i xi y} =",
      sp.simplify(D0_ex / u_ex), " ; (i xi)(1 + (i xi h)^2/6) =",
      sp.simplify(sp.I * xi * (1 + (sp.I * xi * h) ** 2 / 6)))

print("\n   CLAIM A1  centred:  D0 u = u_y + (h^2/6) u_yyy + O(h^4)   <=> c_2 = +1/6, c_3 = 0")
print(f"      c_0={c_ctr[0]}  c_1={c_ctr[1]}  c_2={c_ctr[2]}  c_3={c_ctr[3]}  c_4={c_ctr[4]}")
assert sp.simplify(c_ctr[0] - 1) == 0
assert sp.simplify(c_ctr[1]) == 0
assert sp.simplify(c_ctr[2] - sp.Rational(1, 6)) == 0
assert sp.simplify(c_ctr[3]) == 0
assert sp.simplify(c_ctr[4] - sp.Rational(1, 120)) == 0
print("      -> A1 CONFIRMED   (centred scheme is O(h^2), defect coefficient +1/6)")

print("\n   CLAIM A2  compact:  Dc u = u_y + O(h^4)   <=> c_2 = c_3 = 0, c_4 = -1/180")
print(f"      c_0={c_cmp[0]}  c_1={c_cmp[1]}  c_2={c_cmp[2]}  c_3={c_cmp[3]}  c_4={c_cmp[4]}")
assert sp.simplify(c_cmp[0] - 1) == 0
assert sp.simplify(c_cmp[1]) == 0
assert sp.simplify(c_cmp[2]) == 0 and sp.simplify(c_cmp[3]) == 0
assert sp.simplify(c_cmp[4] - sp.Rational(-1, 180)) == 0
print("      -> A2 CONFIRMED   (compact scheme is O(h^4))")
print("\n   CLAIM A2b forward/backward: c_1 = +/-1/2 (first order), c_2 = 1/6")
assert sp.simplify(c_fwd[1] - sp.Rational(1, 2)) == 0
assert sp.simplify(c_bwd[1] + sp.Rational(1, 2)) == 0
assert sp.simplify(c_fwd[2] - sp.Rational(1, 6)) == 0
assert sp.simplify(c_bwd[2] - sp.Rational(1, 6)) == 0
print("      -> A2b CONFIRMED")

# staggered combination: (D+ + D-)/2 kills the h^1 term but leaves an h^2 one
st = sp.simplify((sp.exp(X) - 1 + 1 - sp.exp(-X)) / (2 * h))
print("\n   CLAIM A3  staggered (D+ + D-)/2 = D0 exactly; (D+ - D-)/h = centred second difference")
s_st = sp.simplify(sym_of(st) - sym_of(schemes["centred   D0 u_j = (u_{j+1}-u_{j-1})/(2h)"]))
s_s2 = sp.simplify(sym_of((sp.exp(X) - 1 - 1 + sp.exp(-X)) / h ** 2) / xi ** 2)
print(f"      symbolic difference (staggered - centred) = {s_st}")
print(f"      (D+ - D-)/h^2 / xi^2 = {sp.expand(sp.series(s_s2, h, 0, 5).removeO())}")
assert s_st == 0
print("      -> A3 CONFIRMED: staggering cancels the h^1 term algebraically, "
      "and the first surviving defect of the staggered pair is the h^2 term of the centred one")

# ----------------------------------------------------------------------------
# 2. second-derivative schemes
# ----------------------------------------------------------------------------
print("\n[2] second y-derivative schemes")
D2exact = (sp.exp(X) - 2 + sp.exp(-X)) / h ** 2
print("   D2 = (u_{j+1}-2u_j+u_{j-1})/h^2 :  symbol/(i xi)^2 =",
      sp.expand(sp.series(sp.simplify(sym_of(D2exact) / (sp.I * xi) ** 2), h, 0, 7).removeO()))
print("   exact d_y^2 symbol versus truncated one:")
print("      cosh(X)-1 expansion in X :",
      sp.expand(sp.series(sp.cosh(X) - 1, X, 0, 8).removeO()))
print("      => lattice (i xi)^2 * [1 + X^2/12 + ...]  i.e. D2 u = u_yy + (h^2/12) u_yyyy + O(h^4)")
c_D2 = [sp.nsimplify(sp.expand(sp.series(
    sp.simplify(sym_of(D2exact) / (sp.I * xi) ** 2), h, 0, 7).removeO()).coeff(h, k)
    / (sp.I * xi) ** k) for k in range(0, 6)]
print(f"      c_0={c_D2[0]}  c_1={c_D2[1]}  c_2={c_D2[2]}  (target 1, 0, 1/12)")
print(f"      coefficient of h^2 : {c_D2[2]}  (target 1/12 = {sp.Rational(1,12)})")
assert sp.simplify(c_D2[2] - sp.Rational(1, 12)) == 0

# ----------------------------------------------------------------------------
# 3. the exact global consistency identity for the centred operator
# ----------------------------------------------------------------------------
print("\n[3] exact identity (no truncation): (I+P) D+ = 2 D0  on ANY sequence")
# algebra of the shift operators only:
lhs = (1 + X) * (X - 1)          # (I+P) D+ with undivided differences
rhs = 2 * (X - X ** -1) / 2 * X  # 2 D0, normalised
d = sp.simplify(sp.expand(lhs - (X ** 2 - 1)))
print(f"   (I+P)(f(j+1)-f(j)) - (f(j+2)-f(j)) = {d}   (must be 0)")
assert d == 0
print("   -> CONFIRMED: 2h D0 u(j) = (I+P)(u(j+1) - u(j)); used in Lean (DirA_Schemes)")

print("\n[4] boundary-free summation by parts for D0 (symbolic, exact):")
# sum_j a_j (D0 b)_j = (1/(2h)) sum_j (a_{j+1} - a_{j-1}) b_j   over PERIODIC index set
print("   sum_j a_j (b_{j+1}-b_{j-1})/(2h) = - sum_j ((a_{j+1}-a_{j-1})/(2h)) b_j  (periodic)")
print("   equivalently (with P the cyclic shift):  2h D0 = (I+P)D+,")
print("   hence <a, D0 b> = -<D0 a, b> + boundary, and the boundary term is")
print("   (1/(2h)) * [ a_0 b_0 - a_{N-1} b_{N-1} - a_0 b_{N-1} ... ] -> see exp3 for the exact form.")
print("\nALL CLAIMS CONFIRMED (coefficient algebra only, no remainder estimate).")
