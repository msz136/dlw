# -*- coding: utf-8 -*-
"""E4 -- two-soliton interaction and phase shift (report sections 6.1, 6.3).

Report 6.3 analytic predictions

    A_12 = (p1-p2)(q1-q2) / ((p1+q2)(p2+q1)),   |dx_i| = |log A_12| / (p_i+q_i)

For case C (a=4, p=(1,2), q=(1,3)):

    A_12 = 1/6,   |dx_1| = log 6 / 2 = 0.8958797,
                  |dx_2| = log 6 / 5 = 0.3583519.

MEASUREMENT METHOD
------------------
Report 6.3 insists on fitting the COMPLETE soliton profile or phase, and warns
against reading only the argmax when several peaks are present.

For this parameter set the two components have very different amplitudes
(|u| ~ 3.0 vs ~ 0.5) and move at different x-speeds, so we proceed in two steps:

  1. Identify each soliton's trajectory from the exact field, then
  2. For each soliton, extract its position as the offset from its own free
     trajectory (a constant-speed line), by a whole-profile least-squares match
     against a single-soliton reference on a window centred on that trajectory.

The phase shift is the CHANGE in that offset between the well-separated
asymptotic regimes t < 0 and t > 0.

The tall component travels at x-speed -1 (t=+-20 peak offsets agree, see the
log), which we determine from the field rather than assuming a formula.

The Gram exponentials overflow for |x| beyond ~120 at these parameters, which
is what bounds the usable |t| range; that bound is reported, not hidden.
"""

import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef, lam

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

A = 4.0
P = [1.0, 2.0]
Q = [1.0, 3.0]
RHO = [3.0, 4.0]
res = {"experiment": "E4", "a": A, "p": P, "q": Q, "rho": RHO}

A12 = (P[0] - P[1]) * (Q[0] - Q[1]) / ((P[0] + Q[1]) * (P[1] + Q[0]))
PRED = [np.log(6) / (P[i] + Q[i]) for i in range(2)]

print("=" * 78)
print("E4  two-soliton interaction: analytic phase shift vs measured")
print("=" * 78)
print(f"\nA_12 = (p1-p2)(q1-q2)/((p1+q2)(p2+q1)) = {A12:.12f}   (1/6 = {1/6:.12f})")
print(f"|log A_12| = {abs(np.log(A12)):.12f}   (log 6 = {np.log(6):.12f})")
for i in range(2):
    print(f"  predicted |dx_{i+1}| = log6/(p+q) = {np.log(6):.6f}/{P[i]+Q[i]:.1f}"
          f" = {PRED[i]:.10f}")
res.update({"A12": A12, "predicted_dx": [float(x) for x in PRED]})

# ---------------------------------------------- y-geometry / h dependence
print("\n--- y-direction geometric shift (NOT h-independent, report 6.3) ---")
print("    the y displacement is the x shift divided by the lattice phase rate")
print("    (1/h) log chi_ii, so unlike A_12 it DOES depend on h.\n")
print(f"    {'h':>8} {'rate_11':>14} {'rate_22':>14} {'dy_1':>12} {'dy_2':>12}")
yrows = []
for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32):
    r1 = float(np.log(lam(P[0] - A, h) * lam(Q[0] + A, h)) / h)
    r2 = float(np.log(lam(P[1] - A, h) * lam(Q[1] + A, h)) / h)
    dy1, dy2 = -np.log(A12) / r1, -np.log(A12) / r2
    print(f"    {h:>8.5f} {r1:>14.8f} {r2:>14.8f} {dy1:>12.6f} {dy2:>12.6f}")
    yrows.append({"h": h, "rate_1": r1, "rate_2": r2, "dy_1": dy1, "dy_2": dy2})
res["y_shift_vs_h"] = yrows
print("    continuous limits 1/P_i + 1/Q_i:")
for i in range(2):
    print(f"      i={i+1}: {1/(P[i]-A) + 1/(Q[i]+A):.8f}")

# --------------------------------------------- locate each soliton's track
h = 1 / 4
J = 0
G2 = GramRef(P, Q, RHO, A, h)
G1 = [GramRef([P[i]], [Q[i]], [RHO[i]], A, h) for i in range(2)]

print("\n--- step 1: identify each soliton's trajectory from the exact field ---")
print("    (parabolic refinement of the local |u| peak; used only to FIND the")
print("     track, the shift itself is measured in step 2)")


def peak_x(t, xlo, xhi, step=0.1):
    xg = np.arange(xlo, xhi + 1e-9, step)
    u = G2.u_row(J, xg, t)
    au = np.abs(np.nan_to_num(u, nan=0.0))
    i = int(np.argmax(au))
    if 0 < i < len(au) - 1:
        y0, y1, y2 = au[i - 1], au[i], au[i + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if abs(den) > 1e-300 else 0.0
        return float(xg[i] + np.clip(d, -1, 1) * step), float(au[i])
    return float(xg[i]), float(au[i])


# the tall soliton is found over the whole window; the shallow one sits near 0
tracks = {}
for t in (-20.0, -10.0, 10.0, 20.0):
    xt, at = peak_x(t, -60, 60)
    # the shallow soliton: search a narrow band around x = 0
    xs_, as_ = peak_x(t, -3, 3, 0.05)
    print(f"    t={t:+6.1f}:  tall |u|={at:.4f} at x={xt:+.4f}"
          f"   shallow |u|={as_:.4f} at x={xs_:+.4f}")
    tracks[str(t)] = {"tall_x": xt, "tall_amp": at, "shallow_x": xs_, "shallow_amp": as_}
res["tracks"] = tracks

# infer the speeds from the track itself
sp_tall = np.mean([(tracks["-10.0"]["tall_x"] - tracks["-20.0"]["tall_x"]) / 10.0,
                   (tracks["20.0"]["tall_x"] - tracks["10.0"]["tall_x"]) / 10.0])
sp_shallow = np.mean([(tracks["-10.0"]["shallow_x"] - tracks["-20.0"]["shallow_x"]) / 10.0,
                      (tracks["20.0"]["shallow_x"] - tracks["10.0"]["shallow_x"]) / 10.0])
print(f"\n    inferred speeds:  tall = {sp_tall:+.6f}   shallow = {sp_shallow:+.6f}")
res["inferred_speeds"] = {"tall": float(sp_tall), "shallow": float(sp_shallow)}
# which single-soliton component is the tall one?
amp1 = np.max(np.abs(G1[0].u_row(J, np.arange(-40, 40, 0.05), 0.0)))
amp2 = np.max(np.abs(G1[1].u_row(J, np.arange(-40, 40, 0.05), 0.0)))
print(f"    single-soliton amplitudes at t=0: comp1={amp1:.4f}  comp2={amp2:.4f}")
tall_is = 2 if amp2 > amp1 else 1
print(f"    => the TALL component is single-soliton {tall_is}")
res["tall_component"] = tall_is

# ------------------------------- step 2: whole-profile offset measurement
print("\n--- step 2: whole-profile offset from the free trajectory ---")
print("    for each soliton the free trajectory is x = v_i t; the fitted offset")
print("    is the shift s minimising || u_ref(x - v_i t - s) - u_2soliton(x) ||")
print("    over a window centred on the trajectory.\n")


def measure_offset(i, t, speed, halfwin=12.0):
    step = 0.05
    c = speed * t
    xl = np.arange(c - halfwin, c + halfwin + 1e-9, step)
    ul = G2.u_row(J, xl, t)
    if not np.all(np.isfinite(ul)):
        return None
    pad = 2 * halfwin
    full = np.arange(c - halfwin - pad, c + halfwin + pad + 1e-9, step)
    ref = G1[i].u_row(J, full, t)
    ok = np.isfinite(ref)
    if not np.all(ok):
        k0 = int(np.argmax(ok)); k1 = len(ok) - int(np.argmax(ok[::-1]))
        full, ref = full[k0:k1], ref[k0:k1]

    def err(s):
        idx = np.round((xl - s - full[0]) / step).astype(int)
        if idx[0] < 0 or idx[-1] >= len(full):
            return np.inf
        return float(np.sum((ref[idx] - ul) ** 2))

    coarse = np.arange(-halfwin, halfwin + 1e-9, 0.2)
    ce = np.array([err(s) for s in coarse])
    if not np.any(np.isfinite(ce)):
        return None
    b = coarse[int(np.argmin(ce))]
    fine = np.arange(b - 0.25, b + 0.25 + 1e-9, 0.002)
    fe = np.array([err(s) for s in fine])
    k = int(np.argmin(fe))
    if 0 < k < len(fine) - 1 and np.all(np.isfinite(fe[k - 1:k + 2])):
        y0, y1, y2 = fe[k - 1], fe[k], fe[k + 1]
        den = y0 - 2 * y1 + y2
        d = 0.5 * (y0 - y2) / den if abs(den) > 1e-300 else 0.0
        return float(fine[k] + np.clip(d, -1, 1) * 0.002), float(np.sqrt(y1 / len(xl)))
    return float(fine[k]), float(np.sqrt(fe[k] / len(xl)))


speed_of = {tall_is: sp_tall, (3 - tall_is): sp_shallow}
meas = []
for i in range(2):
    tm, tp = -20.0, 20.0
    om = measure_offset(i, tm, speed_of[i + 1])
    op = measure_offset(i, tp, speed_of[i + 1])
    pred = float(PRED[i])
    if om is None or op is None:
        print(f"    soliton {i+1}: fit unavailable at one end; predicted = {pred:.6f}")
        meas.append({"i": i + 1, "predicted_dx": pred, "measured_dx": None})
        continue
    (so, rm), (sp_, rp) = om, op
    d = abs(sp_ - so)
    rel = abs(d - pred) / pred
    print(f"    soliton {i+1} (speed {speed_of[i+1]:+.4f}):")
    print(f"      offset(t=-20) = {so:+.6f}  (rms {rm:.3e})")
    print(f"      offset(t=+20) = {sp_:+.6f}  (rms {rp:.3e})")
    print(f"      measured |dx| = {d:.6f}    predicted log6/(p+q) = {pred:.6f}"
          f"    rel.diff = {rel:.3e}")
    meas.append({"i": i + 1, "speed": float(speed_of[i + 1]),
                 "offset_minus": so, "offset_plus": sp_,
                 "rms_minus": rm, "rms_plus": rp,
                 "measured_dx": float(d), "predicted_dx": pred,
                 "rel_diff": float(rel)})
res["measured_vs_predicted"] = meas

with open(os.path.join(OUT, "e4_twosoliton.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, indent=2, ensure_ascii=False)
print(f"\n[E4] wrote out/e4_twosoliton.json")
