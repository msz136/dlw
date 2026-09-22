# -*- coding: utf-8 -*-
"""E5 -- local conservation balance (report sections 6.1 E5, 6.3).

Report 6.3 gives the local conservation laws of the closed system:

    W_t + d_x J_W = 0,   J_W = (u + 2a) W - 4u - W_x
    v_t + d_x J_v = 0,   J_v = delta_0 H + (u+2a) W - 4u
                               + d_x( delta_0 u + (h^2/4) Delta_h W )

with

    H_j = (1/2) u_j^2 + 2 a u_j + h^2 ( W_j^2/32 - W_j/4 ),
    W_j = v_j - delta_0 u_j,

and the balance defect

    D_z(t) = I_z(t) - I_z(0) + int_0^t [ J_z(x_R,s) - J_z(x_L,s) ] ds,
    I_z(t) = int_{x_L}^{x_R} z(x,t) dx.

Report 6.3 warns that I(t)-I(0) may only be read directly as drift when the
flux difference vanishes at periodic / endpoint-equal boundaries, and "do not
presuppose machine-zero".

This experiment reports three separate things:
  (a) the total integral drift, with the endpoint flux printed alongside so the
      reader can see WHY it is (or is not) zero;
  (b) the LOCAL divergence residual W_t + d_x J_W and v_t + d_x J_v on the
      exact solution -- this tests the conservation laws themselves, and should
      sit at the FD truncation level (NOT machine zero);
  (c) the exact mass integrals (C3) against numerical quadrature.
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef, lam

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

A = 4.0
h = 1 / 4
J = 0
XL, XR = -25.0, 25.0
NX = 4001
res = {"experiment": "E5", "a": A, "h": h, "j": J, "window": [XL, XR], "nx": NX}
DT = 1e-5

print("=" * 78)
print("E5  local conservation balance (report 6.3)")
print("=" * 78)
print(f"chain site j={J}, h={h}, x window [{XL},{XR}], nx={NX}, dx={2*XR/(NX-1):.5f}\n")

G = GramRef([1.0], [2.0], [3.0], A, h)
xs = np.linspace(XL, XR, NX)
dx = xs[1] - xs[0]


def trap(f):
    return np.trapezoid(f, xs)


def Wrow(m, xv, t):
    return G.v_row(m, xv, t) - (G.u_row(m + 1, xv, t) - G.u_row(m - 1, xv, t)) / (2 * h)


def Hrow(m, xv, t):
    u = G.u_row(m, xv, t)
    W = Wrow(m, xv, t)
    return 0.5 * u ** 2 + 2 * A * u + h ** 2 * (W ** 2 / 32 - W / 4)


def JW(t):
    """J_W = (u + 2a) W - 4u - W_x  on the site j."""
    u = G.u_row(J, xs, t)
    W = Wrow(J, xs, t)
    dWdx = (Wrow(J, xs + dx, t) - Wrow(J, xs - dx, t)) / (2 * dx)
    return (u + 2 * A) * W - 4 * u - dWdx


def inner(m, xv, t):
    """delta_0 u + (h^2/4) Delta_h W, evaluated on an arbitrary x array."""
    d0u = (G.u_row(m + 1, xv, t) - G.u_row(m - 1, xv, t)) / (2 * h)
    DlW = (Wrow(m + 1, xv, t) - 2 * Wrow(m, xv, t) + Wrow(m - 1, xv, t)) / h ** 2
    return d0u + h ** 2 / 4 * DlW


def Jv(t):
    """J_v = d0 H + (u+2a)W - 4u + d_x( d0 u + (h^2/4) Delta_h W )  on site j."""
    u = G.u_row(J, xs, t)
    W = Wrow(J, xs, t)
    d0H = (Hrow(J + 1, xs, t) - Hrow(J - 1, xs, t)) / (2 * h)
    dinner = (inner(J, xs + dx, t) - inner(J, xs - dx, t)) / (2 * dx)
    return d0H + (u + 2 * A) * W - 4 * u + dinner


# ---------------------------------------------------- (a) integral drift
print("--- (a) total integral drift, with the endpoint flux shown alongside ---")
print("    d_x J = 0 identically is NOT claimed; the flux at the window ends is")
print("    what makes I(t)-I(0) nonzero.  Both are printed.\n")
print(f"    {'t':>6} {'I_W(t)-I_W(0)':>16} {'I_v(t)-I_v(0)':>16} "
      f"{'J_W(xR)-J_W(xL)':>18} {'J_v(xR)-J_v(xL)':>18}")
IW0 = trap(Wrow(J, xs, 0.0))
Iv0 = trap(G.v_row(J, xs, 0.0))
rows = []
for t in (0.0, 0.25, 0.5, 1.0, 2.0):
    IW = trap(Wrow(J, xs, t))
    Iv = trap(G.v_row(J, xs, t))
    jw, jv = JW(t), Jv(t)
    fw, fv = jw[-1] - jw[0], jv[-1] - jv[0]
    print(f"    {t:>6.2f} {IW-IW0:>16.6e} {Iv-Iv0:>16.6e} {fw:>18.6e} {fv:>18.6e}")
    rows.append({"t": t, "dI_W": float(IW - IW0), "dI_v": float(Iv - Iv0),
                 "flux_W": float(fw), "flux_v": float(fv)})
res["integral_drift"] = rows

# ------------------------------------------- (b) local divergence residual
print("\n--- (b) LOCAL divergence residual on the exact solution ---")
print("    W_t + d_x J_W = 0  and  v_t + d_x J_v = 0  pointwise; the residual is")
print("    at the FD truncation level, not machine zero (report 6.3).\n")
print(f"    {'t':>6} {'max|W_t+d_x J_W|':>18} {'scale W_t':>12} {'rel':>10} "
      f"{'max|v_t+d_x J_v|':>18} {'scale v_t':>12} {'rel':>10}")
loc = []
for t in (0.0, 0.5, 1.0):
    Wt = (Wrow(J, xs, t + DT) - Wrow(J, xs, t - DT)) / (2 * DT)
    vt = (G.v_row(J, xs, t + DT) - G.v_row(J, xs, t - DT)) / (2 * DT)
    rW = Wt + np.gradient(JW(t), dx)
    rv = vt + np.gradient(Jv(t), dx)
    aW, av = np.max(np.abs(rW)), np.max(np.abs(rv))
    sW, sv = np.max(np.abs(Wt)), np.max(np.abs(vt))
    print(f"    {t:>6.2f} {aW:>18.6e} {sW:>12.6e} {aW/sW:>10.3e} "
          f"{av:>18.6e} {sv:>12.6e} {av/sv:>10.3e}")
    loc.append({"t": t, "res_W": float(aW), "scale_W": float(sW),
                "rel_W": float(aW / sW), "res_v": float(av),
                "scale_v": float(sv), "rel_v": float(av / sv)})
res["local_divergence"] = loc

# ------------------------------------------------- (c) exact mass integrals
print("\n--- (c) exact mass integrals (C3) vs numerical quadrature ---")
d = h / 2
P1, Q1 = 1.0 - A, 2.0 + A
u_pred = np.log((P1 ** 2 - d ** 2) / (Q1 ** 2 - d ** 2))
v_pred = 4.0 / h * np.log(lam(P1, h) * lam(Q1, h))
u_num = trap(G.u_row(J, xs, 0.0))
v_num = trap(G.v_row(J, xs, 0.0))
print(f"    int u_j dx = sum_i log((P_i^2-d^2)/(Q_i^2-d^2))")
print(f"      predicted = {u_pred:.12f}   quadrature = {u_num:.12f}"
      f"   diff = {u_num-u_pred:.3e}")
print(f"    int v_j dx = (4/h) sum_i log chi_ii")
print(f"      predicted = {v_pred:.12f}   quadrature = {v_num:.12f}"
      f"   diff = {v_num-v_pred:.3e}")
res["exact_mass"] = {"u_pred": float(u_pred), "u_num": float(u_num),
                     "u_diff": float(u_num - u_pred),
                     "v_pred": float(v_pred), "v_num": float(v_num),
                     "v_diff": float(v_num - v_pred)}

# ============================================ (d) SOLVER-BASED conservation
# The review correctly observed that (a)-(c) above only exercise the ANALYTIC
# Gram field.  They verify the theory, but they say nothing about whether the
# time integrator preserves anything.  This section runs the actual solver
# (same construction as E2/E3/E6) and measures the invariants of the NUMERICAL
# orbit.
print("\n--- (d) conservsation of the NUMERICAL orbit (actual time integration) ---")
print("    This is the part the review asked for: the analytic checks (a)-(c)")
print("    cannot establish that the integrator itself preserves anything.\n")

from solver import XGrid, Chain, DLWChainRHS, integrate  # noqa: E402

NXS = 256
LG = 60.0
H_S = 1 / 4
J_L, J_R = -6, 6
T_S = 5e-3
Xg = XGrid(NXS, LG, 4)
Gs = GramRef([1.0], [2.0], [3.0], A, H_S)
Cs = Chain(J_L, J_R, H_S, A)
rhs_s = DLWChainRHS(chain=Cs, X=Xg,
                    b_fun=lambda t: Gs.u_row(J_L, Xg.x, t),
                    ghost_left=lambda t: Gs.u_row(J_L - 1, Xg.x, t),
                    ghost_right=lambda t: Gs.u_row(J_R + 1, Xg.x, t))
rhs_s.use_ext = True
rhs_s._ple = lambda t: (Gs.u_row(J_L, Xg.x, t) - Gs.u_row(J_L - 1, Xg.x, t)) / H_S
rhs_s._pre = lambda t: (Gs.u_row(J_R + 1, Xg.x, t) - Gs.u_row(J_R, Xg.x, t)) / H_S

Ub = Gs.u_block(range(J_L - 1, J_R + 2), Xg.x, 0.0)
Vb = Gs.v_block(range(J_L, J_R + 1), Xg.x, 0.0)
Ps0 = np.array([(Ub[j - (J_L - 1)] - Ub[j - 1 - (J_L - 1)]) / H_S
                for j in range(J_L + 1, J_R + 1)])
Ws0 = np.array([Vb[j - J_L] - (Ub[j + 1 - (J_L - 1)] - Ub[j - 1 - (J_L - 1)]) / (2 * H_S)
                for j in range(J_L, J_R + 1)])


print(f"    grid nx={NXS} L={LG} h={H_S} chain j=[{J_L},{J_R}]  T={T_S}")
MID = (J_L + J_R) // 2          # a well-interior site for the invariant probe


def integrate_full(rhs, P0, W0, T, dt, method):
    """integrate() advances only (P, W); record the interior site's u and v too."""
    cap = []

    def rec(t, PP, WW):
        u = Cs.u_from_P(PP, rhs.b_fun(t))
        # W_j and u_j are enough: v_j = W_j + delta_0 u_j (interior only)
        k = MID - J_L          # index in u and W (both start at J_L)
        v_mid = WW[k] + (u[k + 1] - u[k - 1]) / (2 * H_S)
        cap.append((t, u[k].copy(), v_mid.copy(), WW[k].copy()))

    rec(0.0, P0, W0)
    Pout, Wout, info = integrate(rhs, 0.0, T, P0, W0, dt, method=method, record=rec)
    assert info["stopped"] is None and abs(info["final_t"]-T)<1e-12
    assert np.all(np.isfinite(Pout)) and np.all(np.isfinite(Wout))
    return cap, info, Pout


for method, dt in (("rk4", T_S / 16), ("rk4", T_S / 64), ("euler", T_S / 64)):
    cap, info, Pout = integrate_full(rhs_s, Ps0, Ws0, T_S, dt, method)
    if not cap:
        print(f"    {method:>6} dt={dt:.2e}: no captures")
        continue
    Iv = np.array([Xg.dx*np.sum(c[2]) for c in cap])
    IW = np.array([Xg.dx*np.sum(c[3]) for c in cap])
    dIW = float(np.max(np.abs(IW - IW[0])))
    dIv = float(np.max(np.abs(Iv - Iv[0])))
    print(f"    {method:>6} dt={dt:.2e} steps={info['steps']:>3}  "
          f"max|dI_W|={dIW:.4e}  max|dI_v|={dIv:.4e}  "
          f"finite={np.all(np.isfinite(Pout))}")
    res.setdefault("solver_conservation", []).append(
        {"method": method, "dt": dt, "steps": info["steps"],
         "site": int(MID), "initial_t": cap[0][0], "final_t": info["final_t"],
         "stopped": info["stopped"], "quadrature": "periodic dx sum", "max_dI_W": dIW, "max_dI_v": dIv,
         "finite": bool(np.all(np.isfinite(Pout)))})
print("\n    These are periodic x-integrals at a fixed interior lattice site,")
print("    measured from t=0; conservation alone does not establish solution accuracy.")

with open(os.path.join(OUT, "e5_conservation.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print(f"\n[E5] wrote out/e5_conservation.json")
