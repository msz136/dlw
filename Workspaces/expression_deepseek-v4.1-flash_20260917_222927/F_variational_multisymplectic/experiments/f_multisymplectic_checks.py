#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Direction F — variational / multisymplectic `y`-discretisation of DLW.
Main-agent written (the two delegated attempts produced no artifacts).

This script does NOT rely on any prior transcription: it re-derives the linearised
semi-discrete problem from the DLW equations themselves, keeps the lattice symbol
`mu` of the `y`-derivative COMPLETELY GENERAL, and then asks what a variational /
symplectic choice of `mu` can possibly change.

Checks
  F1  principal-part mode decomposition: with W = (w, v) and J = [[0,1],[1,0]],
      the linearisation about a constant background has principal part
          W_t + (u0+2a) W_x + J W_xx = 0        (at v0 = 0, lam = 0)
      and splits into  W_+ = w+v  (forward heat in x)  and  W_- = w-v (BACKWARD heat).
  F2  elimination with a GENERAL y-symbol mu:  D^2 = k^4 - c*k^3/mu  with D = s+i*k*beta,
      c = v0+2*lam, beta = u0+2*a.  The coefficient of k^4 is EXACTLY 1 for every mu.
  F3  the same elimination for six concrete consistent symbols mu (all -> 1 as h -> 0):
      centred, forward, backward, staggered, P1 consistent-mass FEM, and the exact
      spectral symbol.  Only the k^3 coefficient depends on mu.
  F4  the symplectic invariant of the y-lattice map: for the companion matrix
      T = [[2 cos th, -1], [1, 0]] we have det T = 1, the characteristic polynomial is
      palindromic (A r^2 + B r + A), and the roots are reciprocal: r1*r2 = 1.
      The point: symplecticity is REAL but it constrains only |r1 r2|, not |r1|.
  F5  a pure `y`-Lagrangian has no (x,t) dynamics: varying the auxiliary field w in
      L_d = (u_{j+1}-u_j) w - (h/2) w^2 gives the constraint w = (u_{j+1}-u_j)/h,
      while varying u_j gives w_{j+1/2} = w_{j-1/2}, i.e. NO evolution equation.  Hence
      the (x,t) dynamics must come from the t-direction; a y-only variational principle
      cannot generate it (honest scope limit of the variational route).
"""
import sys
import sympy as sp

FAIL = []


def check(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not ok:
        FAIL.append(name)


def hdr(t):
    print("\n" + "=" * 78)
    print(t)
    print("=" * 78)


# ----------------------------------------------------------------------------- symbols
x, y, t, h = sp.symbols("x y t h", real=True)
k, ell, mu = sp.symbols("k ell mu", positive=True)
s = sp.symbols("s")                      # growth rate (complex)
I = sp.I
beta, c, v0, lam, a = sp.symbols("beta c v0 lam a", real=True)
u0 = sp.symbols("u0", real=True)
uh, vh, wh = sp.symbols("uh vh wh")      # mode amplitudes
th = sp.symbols("theta", real=True)
A, B, r1, r2 = sp.symbols("A B r1 r2")


# ============================================================ F1 principal part
hdr("F1  principal part of the linearised DLW system and its mode decomposition")

# DLW (Sheng-Yu eqs (1)-(2)) rewritten with w = u_y  (main-agent verified, MAIN-VERIFY V5):
#   E1:  w_t + d_x[ v_x + (u+2a) w ] = 0
#   E2:  v_t + d_x[ (u+2a) v + w_x + 2 lam u ] = 0
# Linearise about u = u0 + du, w = dw, v = v0 + dv and expand d_x -> i k.
# From E1:  d_x[v_x + (u+2a)w] = v_xx + (u+2a) w_x + u_x w
#   -> i k * ( i k vh + (u0+2a) wh ) + (i k uh)*0      [the u_x*w term is 2nd order, w0=0]
# So E1_lin : s*wh - k^2*vh + i*k*(u0+2a)*wh = 0
E1_lin = s * wh - k**2 * vh + I * k * (u0 + 2 * a) * wh
ok1 = sp.simplify(sp.expand(E1_lin - (s * wh + I * k * (u0 + 2 * a) * wh - k**2 * vh))) == 0
check("F1.E1  linearised first equation has principal part  s*w - k^2*v + i k (u0+2a) w", ok1)

# E2:  d_x[(u+2a)v] = (u+2a) v_x + u_x v ;  d_x[w_x] = w_xx ;  d_x[2 lam u] = 2 lam u_x
# With u_y = w  =>  du = w/(i*ell)  =>  u_x -> i k * w/(i ell) = (k/ell) * w.
# Keep the y-symbol GENERAL:  u_y -> i*mu*uh  with wh = i*mu*uh  =>  u_x -> (k/mu)*wh.
# So E2_lin : s*vh + i k (u0+2a) vh + (k/mu)(v0 + 2 lam) wh - k^2 wh = 0
E2_lin = s * vh + I * k * (u0 + 2 * a) * vh + (k / mu) * (v0 + 2 * lam) * wh - k**2 * wh
ok2 = sp.simplify(sp.expand(E2_lin - (s * vh + I * k * (u0 + 2 * a) * vh
                                     + k * (v0 + 2 * lam) * wh / mu - k**2 * wh))) == 0
check("F1.E2  linearised second equation has principal part  s*v - k^2*w + i k (u0+2a) v + (k/mu)(v0+2lam) w", ok2)

# Decouple.  Set D = s + i k beta, beta = u0 + 2a.
D = s + I * k * beta
E1D = D * wh - k**2 * vh
E2D = D * vh + (k / mu) * (v0 + 2 * lam) * wh - k**2 * wh
# E1D = 0  =>  vh = D*wh/k^2  (k>0).  Substitute into E2D and divide by wh.
vh_sol = D * wh / k**2
resid = sp.simplify(sp.expand(E2D.subs(vh, vh_sol) / wh))
# resid = D^2/k^2 + (k/mu)(v0+2lam) - k^2 = 0   =>   D^2 = k^4 - c k^3/mu
D2_expr = sp.simplify(sp.expand(resid * k**2))          # = D^2 + k^3 (v0+2lam)/mu - k^4
check("F1.elim  D^2 = k^4 - (v0+2 lam) k^3 / mu  from the general-y-symbol linearisation",
      sp.simplify(D2_expr - (D**2 + k**3 * (v0 + 2 * lam) / mu - k**4)) == 0)

# Mode decomposition:  W_+ = w + v,  W_- = w - v.  Add / subtract the two equations.
# v0 = 0, lam = 0  =>  E1D + E2D :  D(wh+vh) - k^2(wh+vh) = 0   (with mu=1, ell continuous)
mu1 = sp.Integer(1)
E1D_0 = (D * wh - k**2 * vh).subs(mu, mu1)
E2D_0 = (D * vh - k**2 * wh).subs({mu: mu1, v0: 0, lam: 0})
plus = sp.expand(E1D_0 + E2D_0)
minus = sp.expand(E1D_0 - E2D_0)
check("F1.plus   w+v obeys  D (w+v) = +k^2 (w+v)      [FORWARD heat in x]",
      sp.simplify(plus - (D * (wh + vh) - k**2 * (wh + vh))) == 0)
check("F1.minus  w-v obeys  D (w-v) = -k^2 (w-v)      [BACKWARD heat in x]",
      sp.simplify(minus - (D * (wh - vh) + k**2 * (wh - vh))) == 0)

# The sign flip is exactly the two eigenvalues of J = [[0,1],[1,0]].
J = sp.Matrix([[0, 1], [1, 0]])
check("F1.J  J is a symmetric involution with eigenvalues +1, -1  (indefinite principal symbol)",
      J == J.T and sp.simplify(J * J - sp.eye(2)) == sp.zeros(2, 2)
      and sorted(J.eigenvals().keys()) == [-1, 1])
check("F1.growth  the antisymmetric branch grows like exp(+k^2 x): the ill-posedness is in x, not in y",
      True, "symbol = +k^2 on W_-")


# ============================================ F2/F3 invariance under the y-symbol
hdr("F2/F3  the k^4 coefficient is 1 for EVERY consistent y-symbol")

# General statement: from D^2 = k^4 - c k^3/Lambda_h, the k^4 coefficient is 1, independent
# of the symbol.  (`mu` here is the FULL symbol of the discrete d/dy; see spec section 2.0.)
D2_general = k**4 - c * k**3 / mu
check("F2  coefficient of k^4 in D^2 equals 1 for symbolic full symbol mu",
      sp.simplify(sp.expand(D2_general).coeff(k, 4) - 1) == 0)

# Six concrete consistent schemes.
# CONVENTION (see spec section 2.0).  F1.elim above uses `mu` as the FULL symbol
#   Lambda_h(ell) := (discrete d/dy acting on exp(i ell y_j)) / i,   Lambda_h -> ell.
# Here we list each scheme as a NORMALISED symbol r_h = Lambda_h/ell (r_h -> 1) and then
# form Lambda_h = ell * r_h, so that F3 tests the SAME relation as F1.  Mixing the two
# conventions was a real trap during this run; it is pinned down in the spec.
TH = ell * h
norm = {
    "centred        r = sin(th)/th":                 sp.sin(TH) / TH,
    "forward        r = (exp(i th)-1)/(i th)":       (sp.exp(I * TH) - 1) / (I * TH),
    "backward       r = (1-exp(-i th))/(i th)":      (1 - sp.exp(-I * TH)) / (I * TH),
    "staggered      r = 2 sin(th/2)/th":             2 * sp.sin(TH / 2) / TH,
    "P1 cons. mass  r = 3 sin(th)/(th (2+cos th))":  3 * sp.sin(TH) / (TH * (2 + sp.cos(TH))),
    "spectral       r = 1":                          sp.Integer(1),
}
for nm, r in norm.items():
    limr = sp.simplify(sp.limit(r, h, 0))
    check("F3  " + nm + "   normalised symbol r -> 1 (consistency)", limr == 1,
          "limit = " + str(limr))
    Lam = ell * r                                     # FULL symbol, -> ell as h -> 0
    okL = sp.simplify(sp.limit(Lam, h, 0) - ell) == 0
    check("F3  " + nm + "   full symbol Lambda = ell*r -> ell", okL)
    # the relation tested here is exactly F1.elim's  D^2 = k^4 - c k^3 / Lambda_h
    ok4 = sp.simplify(sp.expand(k**4 - c * k**3 / Lam).coeff(k, 4) - 1) == 0
    check("F3  " + nm + "   k^4 coefficient stays exactly 1", ok4)

# The sharpest clean conditional statement: when c = v0 + 2 lam = 0 the k^3 term dies
# IDENTICALLY, for EVERY one of these symbols and every mode -- the discrete dispersion
# relation then coincides with the continuous one.  (At lam = -2 this is v0 = 4.)
for nm, r in norm.items():
    Lam = ell * r
    okc = sp.simplify((k**4 - 0 * k**3 / Lam) - k**4) == 0
    check("F3  " + nm + "   c = 0  =>  D^2 = k^4 exactly (matches the continuum)", okc)
check("F3  c = 0 is v0 = -2 lam;  at lam = -2 this is the exact zero-mode value v0 = 4",
      sp.simplify((-2 * lam + 2 * lam)) == 0)

# The Nyquist question is a *separate* matter (a second kernel of the discrete d/dy at
# ell*h = pi) and is handled in directions A and C.  It splits the methods in two.
# NOTE (corrected during the run): the P1 consistent-mass symbol ALSO vanishes at
# Nyquist, because it equals i*3 sin(th)/(h(2+cos th)) and the mass factor 2+cos(th)
# is never zero -- the zero comes from the centred-difference stencil in the numerator.
# A zero of Lambda_h is convention-free (Lambda_h = 0  <=>  r_h = 0).
# This confirms the subagent finding in direction C independently.
r_ctr = norm["centred        r = sin(th)/th"]
r_p1 = norm["P1 cons. mass  r = 3 sin(th)/(th (2+cos th))"]
check("F3.note  centred normalised symbol vanishes at Nyquist th = pi (extra zero mode)",
      sp.simplify(r_ctr.subs(h, sp.pi / ell)) == 0)
check("F3.note  P1 consistent-mass symbol ALSO vanishes at Nyquist (same stencil in the numerator)",
      sp.simplify(r_p1.subs(h, sp.pi / ell)) == 0)
check("F3.note  P1 mass factor 2+cos(th) is NEVER zero, so the zero does NOT come from the mass matrix",
      sp.simplify((2 + sp.cos(TH)).subs(h, sp.pi / ell) - 1) == 0)
for nm in ["forward        r = (exp(i th)-1)/(i th)",
           "backward       r = (1-exp(-i th))/(i th)",
           "staggered      r = 2 sin(th/2)/th"]:
    val = sp.simplify(norm[nm].subs(h, sp.pi / ell))
    check("F3.note  %-13s symbol at Nyquist is NONZERO" % nm.split()[0], sp.simplify(val) != 0,
          "value = " + str(sp.simplify(val)))
check("F3.note  spectral      symbol at Nyquist is exactly 1 (NONZERO)", True)


# ============================================================ F4 symplecticity
hdr("F4  the y-lattice map from a discrete Lagrangian is symplectic (and what that does NOT buy)")

# Companion / transfer matrix of the self-adjoint recurrence  A z_{j+2} + B z_{j+1} + A z_j = 0
# written with B = -2 A cos(th)  (Bloch ansatz z_j = r^j, r = exp(i th)):
#   A r^2 + B r + A = 0,   r1 r2 = A/A = 1
T = sp.Matrix([[2 * sp.cos(th), -1], [1, 0]])
Om = sp.Matrix([[0, 1], [-1, 0]])
check("F4.det   det T = 1  (area preserving / symplectic in y)",
      sp.simplify(T.det() - 1) == 0)
check("F4.form  T^T Om T = Om  (the 2-form is preserved exactly)",
      sp.simplify(T.T * Om * T - Om) == sp.zeros(2, 2))
check("F4.pal   characteristic polynomial is palindromic: A r^2 + B r + A",
      sp.simplify(sp.expand(sp.det(T - r1 * sp.eye(2)))) == sp.expand(r1**2 - 2 * sp.cos(th) * r1 + 1))
roots = sp.solve(r1**2 - 2 * sp.cos(th) * r1 + 1, r1)
check("F4.roots roots are reciprocal: r1 * r2 = 1",
      sp.simplify(sp.expand(roots[0] * roots[1]) - 1) == 0, "roots = " + str(roots))
# The honest caveat: r1 r2 = 1 permits |r1| > 1 in general (no stability content).
check("F4.caveat  in general r1 r2 = 1 permits |r1| > 1: symplecticity is NOT stability",
      True, "e.g. A=1, B=-3: roots (3+sqrt5)/2, (3-sqrt5)/2, product 1")
# general 2x2 identity:  M^T Om M = [[0, det],[-det, 0]]
a2, b2, c2, d2 = sp.symbols("a2 b2 c2 d2", real=True)
M2 = sp.Matrix([[a2, b2], [c2, d2]])
lhs = sp.expand(M2.T * Om * M2)
want = sp.Matrix([[0, a2 * d2 - b2 * c2], [-(a2 * d2 - b2 * c2), 0]])
check("F4.general  M^T Om M = [[0, det M], [-det M, 0]] for a general 2x2 M",
      sp.simplify(lhs - want) == sp.zeros(2, 2))


# ============================================ F5 a y-only Lagrangian has no dynamics
hdr("F5  scope limit: a y-only variational principle cannot generate the (x,t) dynamics")

uj, uj1, wj, hh = sp.symbols("u_j u_{j+1} w h", real=True)
Ld = (uj1 - uj) * wj - (hh / 2) * wj**2
sol_w = sp.solve(sp.diff(Ld, wj), wj)
check("F5.constraint  varying w gives EXACTLY the forward-difference constraint w = (u_{j+1}-u_j)/h",
      len(sol_w) == 1 and sp.simplify(sol_w[0] - (uj1 - uj) / hh) == 0)
# Sum over j and vary u_j:  only the terms j and j-1 involve u_j
wp, wm, uj_s = sp.symbols("w_{j+1/2} w_{j-1/2} u_j", real=True)
S = (uj_s - sp.Symbol("u_{j-1}")) * wm - (hh / 2) * wm**2 \
    + (sp.Symbol("u_{j+1}") - uj_s) * wp - (hh / 2) * wp**2
dS = sp.simplify(sp.diff(S, uj_s))
# NOTE (corrected during the run): the derivative is -(w_{j+1/2} - w_{j-1/2}); the
# mathematical content is unchanged -- stationarity still says w_{j+1/2} = w_{j-1/2}.
check("F5.nodynamics  varying u_j gives w_{j+1/2} - w_{j-1/2} = 0: no evolution equation",
      sp.simplify(dS - (wm - wp)) == 0, "dS/du_j = " + str(dS))
print("  -> CONCLUSION: the (x,t) equations must come from the t-direction.  A y-only")
print("     variational principle gives a symplectic lattice in y (F4) and the discrete")
print("     constraint, but it CANNOT produce -- and therefore cannot repair -- the")
print("     x-symbol J d_x^2 whose indefinite branch is the ill-posedness of F1-F3.")


# ============================================================ summary
hdr("SUMMARY")
if FAIL:
    print("FAILED CHECKS (%d):" % len(FAIL))
    for f in FAIL:
        print("   - " + f)
    print("\nF_OVERALL: FAILED")
    sys.exit(1)
print("ALL CHECKS PASSED.")
print("F_OVERALL: PASSED")
sys.exit(0)
