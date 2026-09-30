# -*- coding: utf-8 -*-
"""E1 -- continuous limit of the finite-h solution family.

Report sections 4.3 and 6.1 (E1).

We compare the EXACT finite-h Gram reference U_h^* = (u_j, v_j) against the
continuous reference U^0 = (u^0, v^0) of report 4.3:

    continuous tau:  chi^j  ->  exp(y (1/P + 1/Q)),   gamma -> -P/Q
    u^0 = 2 d_x log(f/g),   v^0 = 2 d_x d_y log(f g)

  with P = p - a, Q = q + a.

Sampling rule (report 4.3): compare at the SAME physical position
y = (j + 1/2) h, fixed spectral parameters and continuous phase constants, in
the same physical region.

Established convention (verified by an explicit site-offset scan, see
`diag_e1c`/`offset_scan` below): the lattice fields u_j, v_j are marked at the
F site y = (j+1/2) h, and the continuous reference must be evaluated at that
same physical y.  Offsets of +-h/2 give errors that converge only at first
order; offset 0 gives clean second order.

Reported: E_inf and E_2 for u and v at h = 1/4, 1/8, 1/16, 1/32, 1/64, plus
the observed slopes.  Expected slope ~ 2 (this is MODEL error, not a time
solver test).
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef, ContRef, lam

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

A = 4.0
HS = [1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64]
CASES = {
    "A": ([1.0], [2.0], [3.0]),
    "B": ([2.0], [3.0], [5.0]),
    "C": ([1.0, 2.0], [1.0, 3.0], [3.0, 4.0]),
}
XS = np.linspace(-1.5, 1.5, 25)
DXW = XS[1] - XS[0]
# FIXED physical y-window.  The lattice sample points are y = (j+1/2)h, so as h
# shrinks we must take MORE j's to cover the same physical region.  Using a
# fixed j-range instead makes the integration region shrink with h, which
# spuriously inflates the L2 rate (sqrt(h * sum) picks up an extra sqrt(h)).
Y_LO, Y_HI = -1.5, 1.5
T = 0.0


def js_in_window(h, ylo=Y_LO, yhi=Y_HI):
    """Lattice sites whose F-site y=(j+1/2)h lies in the fixed window."""
    jmax = int(np.ceil((yhi / h) - 0.5)) + 2
    jmin = int(np.floor((ylo / h) - 0.5)) - 2
    js = np.arange(jmin, jmax + 1)
    y = (js + 0.5) * h
    return js[(y >= ylo) & (y <= yhi)]


JS = js_in_window(HS[0])          # kept for the offset-scan control only

res = {"experiment": "E1", "a": A, "hs": HS, "t": T,
       "sample_y_rule": "y = (j + 1/2) h  (the F site)",
       "l2_definition": "sqrt(dx * h * weighted_sum): trapezoid x endpoints, midpoint y",
       "y_window": [Y_LO, Y_HI],
       "cases": {}}

print("=" * 78)
print("E1  continuous limit of the finite-h Gram family (y semi-discrete model error)")
print("=" * 78)


def norms(eu, ev, h, xs, dxw=DXW):
    """Finite x interval: trapezoid endpoints; midpoint lattice y weights."""
    weights = np.ones(len(xs)); weights[[0,-1]] = .5
    dx = xs[1]-xs[0]
    return (np.max(np.abs(eu)), np.max(np.abs(ev)),
            np.sqrt(dx*h*np.sum(weights*eu**2)),
            np.sqrt(dx*h*np.sum(weights*ev**2)))


# ---------------------------------------------------------------- offset scan
print("\n--- control: site-offset scan (h=1/16, case A), confirms y=(j+1/2)h ---")
h0 = 1 / 16
G0 = GramRef(*CASES["A"], A, h0)
C0 = ContRef(*CASES["A"], A)
offs = [("(j+1/2)h  [F site, used]", 0.0),
        ("(j)h      [G site]", -h0 / 2),
        ("(j+1)h    [next G site]", +h0 / 2)]
offset_rows = []
for lbl, off in offs:
    mu = mv = 0.0
    for j in JS:
        y = (j + 0.5) * h0 + off
        for x in XS:
            mu = max(mu, abs(G0.u(int(j), float(x), T) - C0.u0(y, float(x), T)))
            mv = max(mv, abs(G0.v(int(j), float(x), T) - C0.v0(y, float(x), T)))
    print(f"   sample at {lbl:26s}  Einf(u)={mu:.4e}  Einf(v)={mv:.4e}")
    offset_rows.append({"rule": lbl, "offset": off, "Einf_u": mu, "Einf_v": mv})
res["offset_scan"] = offset_rows

# ---------------------------------------------------------------- main scan
for cname, (pp, qq, rr) in CASES.items():
    print(f"\n--- case {cname}:  p={pp} q={qq} rho={rr} ---")
    C = ContRef(pp, qq, rr, A)
    rows = []
    for h in HS:
        G = GramRef(pp, qq, rr, A, h)
        JJ = js_in_window(h)
        U = np.zeros((len(JJ), len(XS))); V = np.zeros_like(U)
        U0 = np.zeros_like(U); V0 = np.zeros_like(U)
        for a_, j in enumerate(JJ):
            y = (j + 0.5) * h
            for b_, x in enumerate(XS):
                U[a_, b_] = G.u(int(j), float(x), T)
                V[a_, b_] = G.v(int(j), float(x), T)
                U0[a_, b_] = C.u0(y, float(x), T)
                V0[a_, b_] = C.v0(y, float(x), T)
        ei_u, ei_v, e2_u, e2_v = norms(U - U0, V - V0, h, XS)
        rows.append((h, ei_u, ei_v, e2_u, e2_v))
        print(f"   h={h:<8.5f}  n_j={len(JJ):<5d} Einf(u)={ei_u:.4e}  Einf(v)={ei_v:.4e}"
              f"  E2(u)={e2_u:.4e}  E2(v)={e2_v:.4e}")
    print("   observed slope  log2(E(h)/E(h/2)):")
    obs = []
    for i in range(len(rows) - 1):
        h1, *e1 = rows[i]
        h2, *e2 = rows[i + 1]
        s = [np.log2(a / b) for a, b in zip(e1, e2)]
        obs.append({"h_pair": [h1, h2], "slope_Einf_u": s[0], "slope_Einf_v": s[1],
                    "slope_E2_u": s[2], "slope_E2_v": s[3]})
        print(f"     h {h1:.5f}->{h2:.5f}:  Einf(u) {s[0]:.3f}  Einf(v) {s[1]:.3f}"
              f"  E2(u) {s[2]:.3f}  E2(v) {s[3]:.3f}")
    res["cases"][cname] = {
        "rows": [{"h": r[0], "Einf_u": r[1], "Einf_v": r[2], "E2_u": r[3], "E2_v": r[4]}
                 for r in rows],
        "observed_slopes": obs}

# ---------------------------------------------------------------- expansions
print("\n--- report 4.3 expansions, verified numerically ---")
print("(1/h) log chi = 1/P + 1/Q + h^2/12 (P^-3+Q^-3) + O(h^4)")
p_, q_ = 1.0, 2.0
P, Q = p_ - A, q_ + A
exp1 = []
for h in HS:
    lhs = np.log(lam(P, h) * lam(Q, h)) / h
    o2 = 1 / P + 1 / Q + h ** 2 / 12 * (P ** -3 + Q ** -3)
    o4 = o2 + h ** 4 * (3 * P ** -5 + 3 * Q ** -5) / 240
    print(f"   h={h:<8.5f} lhs={lhs: .12f} O(h^2) |diff|={abs(lhs-o2):.3e}"
          f"   O(h^4) |diff|={abs(lhs-o4):.3e}")
    exp1.append({"h": h, "lhs": lhs, "diff_order2": abs(lhs - o2),
                 "diff_order4": abs(lhs - o4)})
res["chi_expansion"] = exp1

print("\nlog(gamma(a-d)/gamma(a)) = h/2 (P^-1+Q^-1) + h^2/8 (Q^-2-P^-2) + O(h^3)")
exp2 = []
g = lambda s: -(p_ - s) / (q_ + s)
for h in HS:
    lhs = np.log(g(A - h / 2) / g(A))
    o1 = h / 2 * (P ** -1 + Q ** -1)
    o2 = o1 + h ** 2 / 8 * (Q ** -2 - P ** -2)
    print(f"   h={h:<8.5f} lhs={lhs: .12f} O(h) |diff|={abs(lhs-o1):.3e}"
          f"   O(h^2) |diff|={abs(lhs-o2):.3e}")
    exp2.append({"h": h, "lhs": lhs, "diff_order1": abs(lhs - o1),
                 "diff_order2": abs(lhs - o2)})
res["gamma_expansion"] = exp2

# ------------------------------------------------- nonzero-time model error
# The review noted that the original E1 used only t=0, where a phase error is
# invisible.  Repeat the h-scan at t != 0 so the time phase is actually tested.
print("\n--- nonzero-time model error (case A), exposed to the time phase ---")
t_rows = []
for Tnz in (0.2, -0.35):
    C = ContRef(*CASES["A"], A)
    row = {"t": Tnz, "rows": []}
    print(f"   t = {Tnz}")
    prev = None
    for h in HS:
        G = GramRef(*CASES["A"], A, h)
        JJ = js_in_window(h)
        U = np.zeros((len(JJ), len(XS))); U0 = np.zeros_like(U)
        for a_, j in enumerate(JJ):
            y = (j + 0.5) * h
            for b_, x in enumerate(XS):
                U[a_, b_] = G.u(int(j), float(x), Tnz)
                U0[a_, b_] = C.u0(y, float(x), Tnz)
        ei = np.max(np.abs(U - U0))
        r = f"{prev/ei:.3f}" if prev else "  -"
        print(f"     h={h:<8.5f}  Einf(u)={ei:.4e}   ratio={r}")
        row["rows"].append({"h": h, "Einf_u": ei})
        prev = ei
    t_rows.append(row)
res["nonzero_time"] = t_rows

with open(os.path.join(OUT, "e1_continuum.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print("\n[E1] wrote out/e1_continuum.json")
