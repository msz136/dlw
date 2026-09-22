# -*- coding: utf-8 -*-
"""
Direction A, Experiment 6: the discrete dispersion relation computed MECHANICALLY.

We never guess the dispersion relation: we build the linearised operator of the
ORIGINAL (Sheng-Yu) equations on a periodic y-grid, with a continuum x-wavenumber
k, and extract the eigenvalues.  The original equations are

   (1)  u_yt + v_xx + u u_xy + u_x u_y + 2a u_xy = 0
   (2)  v_t + (u v)_x + u_xxy + 2a v_x + 2 lam u_x = 0

with the y-derivative discretised by the centred difference D0 (periodic grid, N
points, step h), and x, t continuous.  For a plane wave in x, amplitudes
u_j = u~ e^{i xi j} for the lattice mode xi (exact, since the grid is periodic and
the background is constant).

Unknowns per lattice mode: (u~, v~) with the y-derivative representation
    (D0 u)_j = i sin(xi)/h * u_j =: i s u_j .
All y-derivatives are D0 (the u_xxy term is (D0 u)_xx), so no choice of stencil is
made: this is the literal discretisation of the original equations.

Run:  python -u exp6_mechanical.py
"""
import sympy as sp

print("=" * 74)
print("DLW direction A :: exp6 :: mechanical derivation of the discrete spectrum")
print("=" * 74)

sg, k = sp.symbols('sigma k', real=False)
u0, v0, a, lam = sp.symbols('u0 v0 a lam')
s = sp.symbols('s', positive=True)          # s := sin(xi)/h  (real)
ut, vt = sp.symbols('ut vt')

# amplitudes:  u~, v~ ; the y-derivative acts as  d_y -> i s
# (1) sigma*(i s) u~ + (i k)^2 v~ + u0*(i k)(i s) u~ + (i k) u0 (i s) u~ + 2a (i k)(i s) u~
#     NOTE: u u_xy with u = u0 + u~ linearises as u0*(u~)_xy ; (u_x u_y) as
#     (u~)_x * (u0)_y = 0 since u0 is constant.  So the ONLY u~ contributions of the
#     nonlinear terms are u0*(u~)_xy.
eq1 = sp.expand(sg * (sp.I * s) * ut + (sp.I * k) ** 2 * vt + u0 * (sp.I * k) * (sp.I * s) * ut
                + 2 * a * (sp.I * k) * (sp.I * s) * ut)
# (2) sigma v~ + (i k)(u0 v~ + v0 u~) + (i k)^2 (i s) u~ + 2a (i k) v~ + 2 lam (i k) u~
eq2 = sp.expand(sg * vt + (sp.I * k) * (u0 * vt + v0 * ut)
                + (sp.I * k) ** 2 * (sp.I * s) * ut + 2 * a * (sp.I * k) * vt
                + 2 * lam * (sp.I * k) * ut)

print("\n[1] linearised symbol equations (unknowns u~, v~):")
print("    eq1 =", sp.collect(eq1, sg))
print("    eq2 =", sp.collect(eq2, sg))

M = sp.Matrix([[sp.diff(eq1, ut), sp.diff(eq1, vt)],
               [sp.diff(eq2, ut), sp.diff(eq2, vt)]])
det = sp.expand(M.det())
print("\n[2] determinant:", sp.collect(det, sg))

# solve for the bracket (sigma + i c k)^2 with c = u0 + 2a
c = u0 + 2 * a
sols = sp.solve(sp.Eq(det, 0), sg)
print("\n[3] sigma roots:")
for sol in sols:
    print("     ", sp.simplify(sp.expand(sol)))

print("\n[4] put the relation in the standard shape, for the two branches:")
# sigma = -i c k +- sqrt( ... ) ; solve for the square of (sigma + i c k)
X = sp.symbols('X')
# det is quadratic in sigma: A sigma^2 + B sigma + D
A = sp.Poly(det, sg).coeff_monomial(sg ** 2)
B = sp.Poly(det, sg).coeff_monomial(sg)
D = sp.Poly(det, sg).coeff_monomial(1)
print("    A =", sp.simplify(A), "   B =", sp.simplify(B), "   D =", sp.simplify(D))
print("    B - 2 i A c k =", sp.simplify(B - 2 * sp.I * A * c * k))
print("    so sigma = -i c k +- sqrt( (B^2 - 4 A D)/(4 A^2) - 0 ) with")
disc = sp.simplify(sp.expand(B ** 2 - 4 * A * D))
print("       (sigma + i c k)^2 = (B^2 - 4 A D)/(4 A^2) =", sp.simplify(sp.expand(disc / (4 * A ** 2))))

rhs = sp.simplify(sp.expand(disc / (4 * A ** 2)))
print("\n[5] substitute s = sin(xi)/h, i.e. s^2 = f^2 with f = sin(xi)/h:")
f = sp.symbols('f', positive=True)
rhs_f = sp.simplify(sp.expand(rhs.subs(s ** 2, f ** 2)))
print("    (sigma + i c k)^2 =", sp.simplify(rhs_f))

print("\n[6] continuum limit: s -> ell (so f -> ell):")
ell = sp.symbols('ell', positive=True)
rhs_cont = sp.simplify(sp.expand(rhs.subs(s ** 2, ell ** 2)))
print("    (sigma + i c k)^2 =", sp.simplify(rhs_cont))
print("    V6 (shared spec)  : k^4 - (v0 + 2 lam) k^3/ell")
print("    difference        :", sp.simplify(sp.expand(rhs_cont - (k ** 4 - (v0 + 2 * lam) * k ** 3 / ell))))

print("\n[7] growth order for large real k (s fixed, f fixed):")
print("    (sigma + i c k)^2 =", sp.simplify(rhs_f))
print("    -> leading term in k is k^4 times the coefficient:",
      sp.simplify(sp.expand(rhs_f).coeff(k, 4)))
print("    -> next term:", sp.simplify(sp.expand(rhs_f).coeff(k, 3)),
      " ;  so |Re sigma| ~ k^2 exactly when the k^4 coefficient is 1")
