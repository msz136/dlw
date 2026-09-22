# -*- coding: utf-8 -*-
"""
Direction A, Experiment 3: the constraint w = D0 u.

The constraint is discretised FIRST, so its kernel determines both the solvability
of the semidiscrete problem and the extra (non-continuum) zero modes.  On the
periodic grid Z/N (N even) the centred difference D0 has

    ker D0 = { f : f(j+1) = f(j-1) for all j }  =  2-periodic sequences,
           = span{ 1 , alpha } ,   alpha(j) := (-1)^j ,    dim = 2,

whereas the continuum operator d/dy on the circle has a 1-dimensional kernel.  The
extra dimension is span{alpha}: the CHECKERBOARD mode.

Consequences verified here:
  (a) dim ker D0 = 2 and ran D0 = { w : sum_j w_j = 0  and  sum_j alpha_j w_j = 0 };
  (b) the discrete solvability condition is STRICTLY STRONGER than the continuum
      zero-mean condition: w = alpha has zero mean but is NOT in ran D0;
  (c) u -> u + c*alpha is an exact residual gauge mode of the semidiscrete system
      (w, v unchanged), because D0 alpha = 0 and D0^2 alpha = 0.

Run:  python -u exp3_constraint.py
"""
import numpy as np

N = 12
print("=" * 74)
print("DLW direction A :: exp3 :: the discrete constraint w = D0 u")
print("=" * 74)
print(f"periodic grid N = {N} (even)")

# ---------------------------------------------------------------------------
# (a) kernel and range
# ---------------------------------------------------------------------------
D = np.zeros((N, N))
for m in range(N):
    D[m, (m + 1) % N] += 0.5
    D[m, (m - 1) % N] -= 0.5
# undivided centred difference (h factored out): kernel and range are scale-free
rk = np.linalg.matrix_rank(D, tol=1e-10)
print(f"\n[a] undivided centred difference on Z/{N}: rank = {rk}, so dim ker = {N - rk}")
assert N - rk == 2, "kernel dimension must be 2 for even N"

one = np.ones(N)
alpha = np.array([(-1.0) ** j for j in range(N)])
print(f"    D @ 1     = {np.max(np.abs(D @ one)):.3e}   (constants are in the kernel)")
print(f"    D @ alpha = {np.max(np.abs(D @ alpha)):.3e}   (the checkerboard is in the kernel)")
assert np.max(np.abs(D @ one)) < 1e-12 and np.max(np.abs(D @ alpha)) < 1e-12

# left null space: the two conditions characterising ran D
# ran D = { w : <1,w> = 0 and <alpha,w> = 0 }
rng = np.linalg.svd(D)[0][:, :rk]          # orthonormal basis of ran D
# check that both conditions hold on ran D
for v in rng.T:
    assert abs(one @ v) < 1e-10 and abs(alpha @ v) < 1e-10
print("    every vector in ran D satisfies  sum_j w_j = 0  and  sum_j alpha_j w_j = 0")
# and the conditions cut out exactly ran D (codimension 2)
w_test = np.random.default_rng(0).normal(size=N)
w_test -= one * (one @ w_test) / N
w_test -= alpha * (alpha @ w_test) / N
resid = w_test - D @ np.linalg.lstsq(D, w_test, rcond=None)[0]
print(f"    a random zero-mean, alpha-orthogonal w: |w - D lstsq(D,w)| = {np.max(np.abs(resid)):.3e}")
assert np.max(np.abs(resid)) < 1e-9
print("    -> ran D = { w : sum_j w_j = 0 and sum_j alpha_j w_j = 0 }, codimension 2")

# ---------------------------------------------------------------------------
# (b) strictness versus the continuum condition
# ---------------------------------------------------------------------------
print("\n[b] the discrete condition is STRICTLY stronger than zero-mean:")
print(f"    sum_j (alpha)_j      = {alpha.sum():.1f}   (zero mean: passes the continuum test)")
print(f"    sum_j alpha_j alpha_j = {alpha @ alpha:.1f}  (fails the discrete test)")
assert abs(alpha.sum()) < 1e-12 and abs(alpha @ alpha) > 0.5
# explicit zero-mean vector NOT in ran D:
w = alpha - one * (one @ alpha) / N
print(f"    w = alpha - mean(alpha)*1 : sum w = {w.sum():.1e}, sum alpha*w = {w @ alpha:.4f}")
resid = w - D @ np.linalg.lstsq(D, w, rcond=None)[0]
print(f"    |w - D lstsq(D,w)| = {np.max(np.abs(resid)):.4f}  != 0  -> w not in ran D")
assert np.max(np.abs(resid)) > 1e-3
print("    (the checkerboard is the obstruction: it is exactly the extra kernel mode)")

# ---------------------------------------------------------------------------
# (c) what the checkerboard does to the semidiscrete system
# ---------------------------------------------------------------------------
print("\n[c] the checkerboard direction in the semidiscrete system")
h = 0.1
Dd = D / h
D2 = Dd @ Dd           # WIDE second difference
print(f"    D0 alpha   = {np.max(np.abs(Dd @ alpha)):.3e}")
print(f"    D0^2 alpha = {np.max(np.abs(D2 @ alpha)):.3e}   (so alpha is killed by BOTH)")
assert np.max(np.abs(Dd @ alpha)) < 1e-10 and np.max(np.abs(D2 @ alpha)) < 1e-10
print("    The constraint w = D0 u therefore ADMITS u -> u + c*alpha with w unchanged,")
print("    for every c and every admissible (u, w).  The question is what happens to the")
print("    EVOLUTION equations, whose u-dependence is bilinear ((u+2a)w and (u+2a)v).")
rng2 = np.random.default_rng(1)
u = rng2.normal(size=N)
w = Dd @ u                          # enforce w = D0 u
v = rng2.normal(size=N)
a_par = 0.37


def residuals(u, v, w):
    """the two semidiscrete fluxes (x-derivatives act linearly and commute with the
       y-discretisation, so dropping them changes nothing about the c-dependence)"""
    r1 = D2 @ w + (u + 2 * a_par) * w
    r2 = (u + 2 * a_par) * v + D2 @ u + 2 * (-2.0) * u
    return r1, r2


r1a, r2a = residuals(u, v, w)
print("\n    Perturbing u -> u + c*alpha with w = D0 uc = w unchanged:")
print("    bilinearity + the explicit 2 lam u term predict, componentwise,")
print("       r1(u+c*alpha) - r1(u) = c*alpha*w")
print("       r2(u+c*alpha) - r2(u) = c*alpha*v + 2*lam*c*alpha")
lam_par = -2.0
for cval in (1.0, -3.7):
    uc = u + cval * alpha
    wc = Dd @ uc
    r1b, r2b = residuals(uc, v, wc)
    d1 = np.max(np.abs((r1b - r1a) - cval * alpha * w))
    d2 = np.max(np.abs((r2b - r2a) - (cval * alpha * v + 2 * lam_par * cval * alpha)))
    print(f"      c = {cval:6.1f} : |Delta r1| = {np.max(np.abs(r1b-r1a)):10.4f},"
          f" residual of prediction = {d1:.2e}")
    print(f"                 |Delta r2| = {np.max(np.abs(r2b-r2a)):10.4f},"
          f" residual of prediction = {d2:.2e}")
    assert np.max(np.abs(wc - w)) < 1e-10
    assert d1 < 1e-9 and d2 < 1e-9
print("    -> the residual DOES change (by c*alpha*w and c*(alpha*v + 2*lam*alpha)).")
print("       So the checkerboard is NOT an exact symmetry of the semidiscrete system.")

print("\n    Is the checkerboard a LINEARISED mode?  Put delta u = c*alpha with the")
print("    constraint maintained, i.e. delta w = D0(c*alpha) = 0, and delta v = 0.")
print("    Then, with D0^2 alpha = 0 and (u + 2a)*delta w = 0,")
print("      delta r1 = delta[(u + 2a) w] = c*alpha*w   and")
print("      delta r2 = c*alpha*v + 2*lam*c*alpha .")
print("    (The (u+2a)*delta w term cancels because delta w = 0, and no c^2 term")
print("     survives since w is held fixed.)  Verified below.")
for cval in (1.0, -3.7):
    uc = u + cval * alpha
    wc = Dd @ uc
    r1b, r2b = residuals(uc, v, wc)
    d1 = np.max(np.abs((r1b - r1a) - cval * alpha * w))
    d2 = np.max(np.abs((r2b - r2a) - (cval * alpha * v + 2 * lam_par * cval * alpha)))
    print(f"      c = {cval:6.1f} : |dr1 - c*alpha*w| = {d1:.2e} ;"
          f" |dr2 - c*(alpha*v + 2*lam*alpha)| = {d2:.2e}")
    assert np.max(np.abs(wc - w)) < 1e-10
    assert d1 < 1e-9 and d2 < 1e-9
print("    -> the residual changes: the checkerboard is NOT an exact symmetry.")
print("\n    Both closed forms vanish for all c iff  alpha*w = 0  and  alpha*v = 0.")
print("    Now alpha*w = 0 means w_j = 0 for every EVEN j.  Testing the admissible data")
print("    that satisfy it, and asking whether any nontrivial such state exists:")
u4 = np.zeros(N)
u4[0::2] = -2 * a_par                # alpha*(u+2a) = 0 on even sites
u4[1::2] = rng2.normal(size=N // 2)
w4 = Dd @ u4
print(f"      try u = -2a on even sites: max|w4[even]| = {np.max(np.abs(w4[0::2])):.3e}"
      f" ; max|w4[odd]| = {np.max(np.abs(w4[1::2])):.3e}")
print("      w4[odd] != 0, so alpha*w4 != 0 -- the condition fails.")
# The rigorous reason: on the periodic lattice (D0 u)_j = (u_{j+1}-u_{j-1})/(2h).
# alpha*w = 0 <=> w_j = 0 for all even j <=> u_{j+1} = u_{j-1} for all even j
#             <=> u is constant on the ODD sublattice.
# w_j = 0 for all odd j would give u constant on the EVEN sublattice.
# Both together give u = const, hence w = 0, hence D0 u = 0 -> u = const.
u5 = np.zeros(N)
u5[1::2] = 7.0                       # u constant on the odd sublattice
w5 = Dd @ u5
print(f"      try u constant on odd sites only: max|w5[odd]| = {np.max(np.abs(w5[1::2])):.3e}"
      f" ; max|w5[even]| = {np.max(np.abs(w5[0::2])):.3e}")
w6 = Dd @ np.ones(N)
print(f"      try u = const: max|w6| = {np.max(np.abs(w6)):.3e}  (w = 0, the trivial kernel)")
print("    -> the only state killing both increments is u = const, already a continuum mode.")
print("    -> REFUTATION, recorded as a result: the checkerboard is an extra mode of the")
print("       CONSTRAINT's kernel and it does enlarge the solvability obstruction, but it")
print("       is NOT an extra symmetry or an extra zero mode of the semidiscrete evolution")
print("       system on the periodic grid.  The genuinely discrete defect therefore sits in")
print("       the CONSTRAINT (solvability / well-posedness), not in a hidden evolution mode.")
print("\nSUMMARY OF exp3:")
print("  * ker D0 = span{1, alpha}: dimension 2; the continuum kernel is only span{1}.")
print("  * ran D0 = { w : sum_j w_j = 0 and sum_j alpha_j w_j = 0 }: codimension 2.")
print("  * the discrete constraint is strictly stronger than the continuous zero-mean")
print("    condition; alpha is the witness (zero mean, alternating sum N != 0).")
print("  * refuted: the checkerboard does NOT generate an extra semidiscrete symmetry")
print("    (the closed-form residuals above are never simultaneously zero nontrivially).")
print("\nALL CHECKS PASSED.")
