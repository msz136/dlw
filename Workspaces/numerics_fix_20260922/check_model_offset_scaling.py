"""After the phase fix: is the residual on (u0,v0) genuinely O(h^2)?

The review correctly showed the O(1) residual was a phase bug.  But the
report's ORIGINAL claim was that (u0,v0) are only the LEADING terms of a
finite-h expansion, so a residual should remain that vanishes as h->0.

Now that the phase is fixed, the two explanations make DIFFERENT predictions:
  (A) phase bug only      -> residual should be ~0 (machine level) at all h
  (B) leading-term only   -> residual should be nonzero and -> 0 like h^2

So this is now a decidable question.  We compute, at shrinking h, the DLW
left-hand sides evaluated on the EXACT lattice fields (which we trust),
and look at the scaling.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.abspath(os.path.join(HERE, "..", "..", "Paper", "dlw_semidiscrete", "numerics"))
sys.path.insert(0, os.path.join(NUM, "lib"))

from gramtau import GramRef  # noqa: E402

A = 4.0
P = [1.0]
Q = [2.0]
RHO = [3.0]

print("=" * 78)
print("DLW left-hand side evaluated on the EXACT LATTICE fields, vs h")
print("(chain of open j, y = (j+1/2)h, all derivatives in x by FD)")
print("=" * 78)

xs = np.linspace(-8.0, 8.0, 161)
dx = xs[1] - xs[0]
t0 = 0.2
dtc = 1e-6


def dlw_lhs(u_of, v_of, x, t):
    """u_of(x,t), v_of(x,t) -> (L1, L2) arrays over x."""
    def U(xx, tt):
        return np.array([u_of(xi, tt) for xi in xx])

    def V(xx, tt):
        return np.array([v_of(xi, tt) for xi in xx])

    u = U(x, t)
    v = V(x, t)
    ut = (U(x, t + dtc) - U(x, t - dtc)) / (2 * dtc)
    vt = (V(x, t + dtc) - V(x, t - dtc)) / (2 * dtc)
    # 1D central differences in x
    d1 = np.gradient(u, dx)
    d2 = np.gradient(d1, dx)
    dv1 = np.gradient(v, dx)
    dv2 = np.gradient(dv1, dx)
    # DLW1 needs u_yt: for the lattice field y appears only through j, and we
    # sample a fixed j, so u_y must be taken along the lattice: use the
    # y-derivative implied by neighbouring j at the SAME physical y.
    return ut, vt, d1, d2, dv1, dv2


print(f"{'h':>8} {'max|L1|':>14} {'max|L2|':>14} {'ratio L1':>10} {'ratio L2':>10}")

prev1 = prev2 = None
for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64):
    ref = GramRef(P, Q, RHO, A, h)

    def u_of(x, t, _ref=ref, _h=h):
        return _ref.u(0, x, t)

    def v_of(x, t, _ref=ref, _h=h):
        return _ref.v(0, x, t)

    # Lambda_h(z) = (z+h/2)/(z-h/2) is the lattice rate renormalisation, so the
    # lattice soliton moves at a different speed than q^2-p^2; both fields are
    # still functions of (x, t) with a definite y-dependence through j.
    u = np.array([u_of(xi, t0) for xi in xs])
    v = np.array([v_of(xi, t0) for xi in xs])
    ut = np.array([(u_of(xi, t0 + dtc) - u_of(xi, t0 - dtc)) / (2 * dtc) for xi in xs])
    vt = np.array([(v_of(xi, t0 + dtc) - v_of(xi, t0 - dtc)) / (2 * dtc) for xi in xs])

    # u_y along the lattice at fixed physical sample: use j and j+1 at their
    # own y, mapped to a common y by shifting x -- approximate by using the
    # j-derivative, which is what the lattice actually provides.
    hh = h
    uy = np.array([(ref.u(1, xi, t0) - ref.u(-1, xi, t0)) / (2 * hh) for xi in xs])
    d1 = np.gradient(u, dx)
    d2 = np.gradient(d1, dx)
    dv1 = np.gradient(v, dx)
    dv2 = np.gradient(dv1, dx)
    uuy_x = np.gradient(u * uy, dx)
    d1_xy = np.gradient(uy, dx)

    L1 = ut * 0.0  # u_yt needs a y-derivative of u_t; use d/dj of ut
    uyt = np.array([((ref.u(1, xi, t0 + dtc) - ref.u(-1, xi, t0 + dtc))
                     - (ref.u(1, xi, t0 - dtc) - ref.u(-1, xi, t0 - dtc)))
                    / (4 * hh * dtc) for xi in xs])
    L1 = uyt + dv2 + uuy_x + 2 * A * d1_xy

    uv_x = np.gradient(u * v, dx)
    uxxy = np.gradient(np.gradient(
        np.array([(ref.u(1, xi, t0) - ref.u(-1, xi, t0)) / (2 * hh) for xi in xs]), dx), dx)
    L2 = vt + uv_x + uxxy + 2 * A * dv1 - 4 * d1

    m1, m2 = np.max(np.abs(L1)), np.max(np.abs(L2))
    r1 = f"{prev1/m1:.3f}" if prev1 else "     -"
    r2 = f"{prev2/m2:.3f}" if prev2 else "     -"
    print(f"{1/h:8.0f} {m1:14.4e} {m2:14.4e} {r1:>10} {r2:>10}")
    prev1, prev2 = m1, m2

print()
print("Reference scales at h=1/4:")
print(f"  max|u| = {np.max(np.abs(u)):.4e}   max|v| = {np.max(np.abs(v)):.4e}")
print("  (uuy_x etc. are the O(1) terms being balanced)")
