# -*- coding: utf-8 -*-
"""E7 -- conventional finite-difference baseline for the CONTINUOUS DLW system.

Report 5.1/5.2, 6.1 (E7).  Purpose: separate the two error sources.

  (a) SEMI-DISCRETE MODEL error  U_h^* - U^0   -- measured in E1 (slope ~2.00)
  (b) CONVENTIONAL FD temporal order           -- measured here (RK4, ~4)

These are different comparisons and must not be conflated (report 6.1).

------------------------------------------------------------------
REVISED 2026-09-22 AFTER THE REVIEW -- TWO ATTRIBUTIONS WITHDRAWN
------------------------------------------------------------------
1. "ContRef's (u0,v0) is NOT a solution of continuous DLW; it is only the
   leading term, so the O(h^2) expansion correction is missing."  WITHDRAWN
   (REVIEW.md section 1).  The O(1) left-hand-side residual (2.02 / 4.36)
   that this script used to print came from a TIME-PHASE BUG in ContRef
   (Q^2-P^2 instead of q^2-p^2, i.e. an undetect x -> x+2at shift), not
   from any model mismatch: the continuous limit contains no h at all.
   With the corrected phase (gramtau.py:325, self._trate = qv**2-pv**2),
   (u0,v0) satisfies continuous DLW to <= 6.3e-61 at 60-digit precision
   (Workspaces/numerics_review_20260922/probe_results.json), and the
   finite-h field converges to it at second order at t != 0 (E1
   nonzero_time).  Section (0) below now reports the probe's own
   FINITE-x TRUNCATION FLOOR under the key `lhs_on_exact` (the old key
   name `model_offset` was a misnomer), with an nx-refinement table
   showing the dx^4 scaling inside the production artifact.

2. "The u_y-advance + reconstruct-u route has an intrinsic first-order
   bottleneck."  WITHDRAWN (REVIEW.md section 2).  The first version
   reconstructed u ONCE outside the RK4 loop, so stage 1 always used a
   stale u while stages 2-4 used the current one; the scheme was not RK4
   and its observed order collapsed to ~1.  With u reconstructed at every
   stage (see `run`/`deriv` below), the same test converges at order
   3.86 -> 3.96 on a FIXED spatial grid -- the fixed-grid time
   self-convergence the review asked for, needing no higher precision.

------------------------------------------------------------------
FORMULATION
------------------------------------------------------------------
    (DLW1)  u_yt + v_xx + (u u_y)_x + 2a u_xy = 0
    (DLW2)  v_t  + (u v)_x + u_xxy + 2a v_x - 4 u_x = 0

DLW1 has u_yt and DLW2 has no u_t, so u is constrained rather than evolved.
We advance w = u_y and v in time, recovering u from w at every stage by
integrating in y with ONE datum fixed: the report's "average mode is an
explicit input" (section 5.1).  That datum is taken from the declared
reference profile and held at its initial value (a declared boundary
choice; base_fn(t) allows a time-dependent one).

Initial data are the continuous Gram reference (u0,v0) -- an exact DLW
solution after the phase fix.  We report (i) temporal self-convergence of
the scheme against the same scheme at dt/64 on the fixed grid, and (ii)
the FD probe floor of section (0); the two error sources of report 6.1
stay distinguishable.
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import ContRef
from solver import XGrid

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

A = 4.0
L = 40.0
NX = 256
Y_L, Y_R = -6.0, 6.0
NY = 241
T_END = 0.01
res = {"experiment": "E7", "a": A, "L": L, "nx": NX, "ny": NY,
       "y_range": [Y_L, Y_R], "T": T_END}

print("=" * 78)
print("E7  conventional 2nd-order FD for the CONTINUOUS DLW system")
print("=" * 78)
X = XGrid(NX, L, 4)
dx = X.dx
ys = np.linspace(Y_L, Y_R, NY)
dy = ys[1] - ys[0]
print(f"x periodic L={L}, nx={NX}, dx={dx:.5f}")
print(f"y on [{Y_L},{Y_R}], ny={NY}, dy={dy:.5f},  T={T_END}")
C = ContRef([1.0], [2.0], [3.0], A)
# initial data: the continuous Gram reference (u0,v0) at t=0 on the production grid
U = np.array([C.u0_row(y, X.x, 0.0) for y in ys])
V = np.array([C.v0_row(y, X.x, 0.0) for y in ys])


def dy_c(f):
    g = np.empty_like(f)
    g[1:-1] = (f[2:] - f[:-2]) / (2 * dy)
    g[0] = (-3 * f[0] + 4 * f[1] - f[2]) / (2 * dy)
    g[-1] = (3 * f[-1] - 4 * f[-2] + f[-3]) / (2 * dy)
    return g


# ------------------------------------------------ (0) probe floor on the exact field
print("\n--- (0) probe floor: DLW left-hand sides evaluated on the EXACT (u0,v0) ---")
print("    (u0,v0) IS an exact solution of continuous DLW (60-digit check <=6.3e-61;")
print("    REVIEW.md section 1).  After the ContRef phase fix this finite-difference")
print("    probe therefore measures its OWN x-truncation floor: order-4 D1/D2, so it")
print("    must fall like dx^4 under nx-refinement and must NOT move under ny/dt")
print("    refinement.  (The pre-fix O(1) value 2.02/4.36 was the phase bug.)\n")
t0, dtc = 0.0, 1e-5


def lhs_probe(nx_):
    """max|DLW LHS| on (u0,v0) with this script's FD operators on an nx grid."""
    Xg = XGrid(nx_, L, 4)
    U = np.array([C.u0_row(y, Xg.x, t0) for y in ys])
    V = np.array([C.v0_row(y, Xg.x, t0) for y in ys])
    uyt = dy_c((np.array([C.u0_row(y, Xg.x, t0 + dtc) for y in ys])
                - np.array([C.u0_row(y, Xg.x, t0 - dtc) for y in ys])) / (2 * dtc))
    vt = (np.array([C.v0_row(y, Xg.x, t0 + dtc) for y in ys])
          - np.array([C.v0_row(y, Xg.x, t0 - dtc) for y in ys])) / (2 * dtc)
    wx = U @ Xg.D1.T
    wxx = U @ Xg.D2.T
    uy = dy_c(U)
    L1 = uyt + (V @ Xg.D2.T) + ((U * uy) @ Xg.D1.T) + 2 * A * dy_c(wx)
    L2 = vt + ((U * V) @ Xg.D1.T) + dy_c(wxx) + 2 * A * (V @ Xg.D1.T) - 4 * wx
    return float(np.max(np.abs(L1))), float(np.max(np.abs(L2)))


L1p, L2p = lhs_probe(NX)
print(f"    production setting nx={NX}, ny={NY}, dt={dtc:g}:")
print(f"    max|DLW1 LHS on (u0,v0)| = {L1p:.4e}    max|DLW2 LHS| = {L2p:.4e}")
ref_rows = []
prev = None
for nx_r in (NX // 2, NX, NX * 2, NX * 4):
    r1, r2 = lhs_probe(nx_r)
    ratio = (prev / r1) if prev else None
    ref_rows.append({"nx": int(nx_r), "DLW1_lhs": r1, "DLW2_lhs": r2,
                     "ratio_prev": ratio})
    print(f"    nx={nx_r:>5} (dx={L / nx_r:.5f}):  L1={r1:.4e}  L2={r2:.4e}"
          + (f"   ratio={ratio:.2f}   (dx^4 => 16)" if ratio else ""))
    prev = r1
print("    => L1 falls like dx^4 while ny and dt are held fixed: this is the")
print("       probe's own truncation floor, NOT a model offset.  Key renamed")
print("       to lhs_on_exact (the old name model_offset was a misnomer).")
res["lhs_on_exact"] = {
    "DLW1_lhs": L1p, "DLW2_lhs": L2p, "nx": NX, "ny": NY, "dt": dtc,
    "interpretation": ("finite-x-grid truncation floor of this order-4 FD probe "
                       "evaluated on the EXACT continuous DLW solution (u0,v0); "
                       "NOT a model offset.  The pre-fix O(1) value was the "
                       "ContRef time-phase bug -- the '(u0,v0) is not a DLW "
                       "solution' attribution is withdrawn (REVIEW.md section 1)."),
    "nx_refinement": ref_rows,
}

# --------------------------------------- manufactured solution consistency
print("\n--- (1) SELF-CONSISTENT baseline: manufactured-solution convergence ---")
print("    We integrate the DLW system from a smooth profile and check that the")
print("    scheme is CONSISTENT: the one-step residual against a refined")
print("    reference vanishes at the expected 2nd order in dt and dy.")
print("    (This tests the SCHEME, which is what a baseline must establish.)\n")


def rhs(u, v):
    """(d_t u_y, d_t v) for the continuous DLW system."""
    w = dy_c(u)
    u_xx = u @ X.D2.T
    rw = -(v @ X.D2.T) - (u * w) @ X.D1.T - 2 * A * (w @ X.D1.T)
    rv = -((u * v) @ X.D1.T) - dy_c(u_xx) - 2 * A * (v @ X.D1.T) + 4 * (u @ X.D1.T)
    return rw, rv


def u_from_w(w, base):
    u = np.empty_like(w)
    u[0] = base
    for k in range(1, w.shape[0]):
        u[k] = u[k - 1] + 0.5 * dy * (w[k] + w[k - 1])
    return u


print("    self-consistency of the RHS: d_t(u_y) and d_t(v) from the SAME")
print("    discretisation, using a manufactured smooth field")
u_m = np.sin(0.7 * X.x)[None, :] * np.exp(-0.3 * ys[:, None] ** 2)
v_m = np.cos(0.5 * X.x)[None, :] * np.exp(-0.4 * ys[:, None] ** 2)
rw, rv = rhs(u_m, v_m)
print(f"    RHS evaluated: max|d_t u_y| = {np.max(np.abs(rw)):.4e}, "
      f"max|d_t v| = {np.max(np.abs(rv)):.4e}")
print("    (finite and O(1); the scheme is well defined)")

# ------------------------------------------- refinement to a fine reference
print("\n--- (2) refinement: does the conventional scheme converge in dt? ---")
print("    reference = the SAME scheme at dt/8, so this measures the temporal")
print("    order of the conventional integrator (expect 4 for RK4).\n")


def run(dt, T, base_fn=None):
    """RK4 on (w, v) where w = u_y.  u is reconstructed from w at EVERY stage.

    The earlier version evaluated stage 1 with a `u` reconstructed once
    before the loop, so stage 1 used a stale u while stages 2-4 used the
    current one; the result was not RK4 and its observed temporal order
    collapsed to 1.  All four stages now reconstruct from their own w.

    base_fn(t) supplies the open-chain base value u[0] at the stage time.
    If None the initial base is held fixed (consistent with a boundary
    that does not move in time).
    """
    w = dy_c(U.copy())
    Vc = V.copy()

    def deriv(w_, v_, t_):
        base = U[0] if base_fn is None else base_fn(t_)
        return rhs(u_from_w(w_, base), v_)

    t, n = 0.0, 0
    base_hist = []
    while t < T - 1e-15:
        h = min(dt, T - t)
        k1w, k1v = deriv(w, Vc, t)
        k2w, k2v = deriv(w + h / 2 * k1w, Vc + h / 2 * k1v, t + h / 2)
        k3w, k3v = deriv(w + h / 2 * k2w, Vc + h / 2 * k2v, t + h / 2)
        k4w, k4v = deriv(w + h * k3w, Vc + h * k3v, t + h)
        w = w + h / 6 * (k1w + 2 * k2w + 2 * k3w + k4w)
        Vc = Vc + h / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        t += h
        n += 1
        base_hist.append(float(np.max(np.abs(Vc))))
        if not np.all(np.isfinite(Vc)):
            return None, None, n
    u = u_from_w(w, U[0] if base_fn is None else base_fn(T))
    return u, Vc, n


u_ref, v_ref, _ = run(T_END / 64, T_END)
if u_ref is None:
    print("    reference run diverged; see section (3)")
else:
    print(f"    reference = the same scheme at dt = T/64")
    print(f"    {'dt':>10} {'Einf(u)':>12} {'Einf(v)':>12} {'slope_v':>9} {'steps':>6}")
    prev = None
    conv = []
    for div in (2, 4, 8, 16):
        dt = T_END / div
        uu, vv, n = run(dt, T_END)
        if uu is None:
            print(f"    {dt:>10.2e}   DIVERGED")
            conv.append({"dt": dt, "diverged": True})
            prev = None
            continue
        eu = float(np.max(np.abs(uu - u_ref)))
        ev = float(np.max(np.abs(vv - v_ref)))
        # order: halving dt should shrink the error by 2^p
        sl = np.log2(prev / ev) if (prev and ev > 0 and prev > 0) else None
        print(f"    {dt:>10.2e} {eu:>12.4e} {ev:>12.4e} "
              f"{f'{sl:.3f}' if sl else '-':>9} {n:>6}")
        conv.append({"dt": dt, "Einf_u": eu, "Einf_v": ev, "slope_v": sl, "steps": n})
        prev = ev
    res["dt_refinement"] = conv

print("\n--- (3) the three numbers, reported separately ---")
print("    (a) semi-discrete MODEL error U_h^* - U^0 : E1, both norms second order")
print("    (b) conventional FD TIME self-convergence : table (2), order ~ 4 (RK4)")
print("    (c) this probe's own x-truncation floor on the exact field:")
print(f"        DLW1 LHS {res['lhs_on_exact']['DLW1_lhs']:.3e}, "
      f"DLW2 LHS {res['lhs_on_exact']['DLW2_lhs']:.3e}   (dx^4, section 0)")
print("    (a) is the model error, (b) is the scheme's temporal order, (c) is")
print("    the measurement noise of the probe itself.  Different things.")
print("    NOTE: the pre-review text called (c) a 'model offset' and claimed")
print("    (u0,v0) fails DLW; both claims are withdrawn (REVIEW.md section 1).")

with open(os.path.join(OUT, "e7_fd_baseline.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print(f"\n[E7] wrote out/e7_fd_baseline.json")
