# -*- coding: utf-8 -*-
"""One-screen summary of every result artifact, for a final consistency check."""

import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def load(n):
    with open(os.path.join(OUT, n), encoding="utf-8") as f:
        return json.load(f)


d = load("e0_benchmark.json")
print("E0  bilinear residual, exact vs finite-difference")
for c in d["checks"]:
    if c["kind"] == "bilinear_residual" and c.get("case") == "A":
        print(f"    N={c['N']} h={c['h']:8.5f}  exact={c['max_abs_exact_Rminus']:.3e}"
              f"   fd={c['max_abs_fd_Rminus']:.6e}")

d = load("e1_continuum.json")
print("\nE1  continuum-limit order (case A)")
for r in d["cases"]["A"]["observed_slopes"]:
    print(f"    h{r['h_pair']}:  Einf_u {r['slope_Einf_u']:.4f}   E2_u {r['slope_E2_u']:.4f}")

d = load("e2_e3_solver.json")
print("\nE2/E3  budgets  (left: report-7 continuous pi/dx estimate;")
print("                 right: zero-background open-chain modal estimate)")
for b in d["budget_table"]:
    print(f"    nx={b['nx']:5d}  g(cont)={b['g_max']:9.3f} T={b['T_budget']:.4f}   "
          f"g(disc)={b.get('g_max_discrete', float('nan')):9.3f} "
          f"T={b.get('T_budget_discrete', float('nan')):.4f}")
for r in d["time_refinement"]:
    print(f"    h={r['h']:.4f} {r['method']:>10} dt={r['dt']:.2e} "
          f"Einf_u={r['Einf_u']:.4e}  slope={r['slope_Einf_u']}")

d = load("e2_e3_self_convergence.json")
print("\nE2/E3 same-grid time self-convergence (separate from spatial error)")
for r in d['studies']:
    p=r['successive_differences'][-1]['orders']
    print(f"    h={r['h']:.3f} {r['method']:>10} orders: " +
          " ".join(f"{k}={v:.4f}" for k,v in p.items()))

d = load("e4_twosoliton.json")
print("\nE4  two-soliton phase shift")
print(f"    A12 = {d['A12']:.12f}  (1/6 = {1/6:.12f})")
for m in d["measured_vs_predicted"]:
    print(f"    soliton {m['i']}: measured={m['measured_dx']:.6f} "
          f"predicted={m['predicted_dx']:.6f}  rel={m['rel_diff']:.3e}")

d = load("e5_conservation.json")
print("\nE5  conservation")
print(f"    exact mass  u_diff={d['exact_mass']['u_diff']:.3e}  "
      f"v_diff={d['exact_mass']['v_diff']:.3e}")
for r in d["local_divergence"][:1]:
    print(f"    local rel residual  W={r['rel_W']:.3e}  v={r['rel_v']:.3e}")
print(f"    max integral drift  W={max(abs(x['dI_W']) for x in d['integral_drift']):.3e}  "
      f"v={max(abs(x['dI_v']) for x in d['integral_drift']):.3e}")

d = load("e6_growth.json")
print("\nE6  high-wavenumber growth  (model law (S), continuous k)")
for r in d["branch_table"][:3] + d["branch_table"][-2:]:
    print(f"    k={r['k']:5d}  Re sigma={r['Re_growing']:.6e}  Re/k^2={r['Re_over_k2']:.6f}")
print("    modal amplification estimates (not nonlinear stability bounds):")
for b in d["grid_budget"]:
    print(f"    nx={b['nx']:5d} maxKeff={b['max_Keff']:8.3f} "
          f"g_max={b['g_max_discrete']:11.4f}  T_budget={b['T_budget']:.6e}")
print("    (continuous pi/dx formula gives a DIFFERENT, larger value:")
for b in d["grid_gmax"][:3]:
    print(f"     nx={b['nx']:5d}  discrete={b['g_max_discrete']:.4f}  "
          f"continuous={b['g_max_continuous_nyq']:.4f})")
for s in d.get("solver_growth", []):
    gm = s["g_measured"]
    print(f"    measured nx={s['nx']:4d} Keff={s['k_pert_eff']:.3f}  "
          f"g_meas={gm if gm is None else format(gm, '.4e')}  "
          f"g_pred={s['g_predicted']:.4e}")

d = load("e7_fd_baseline.json")
print("\nE7  conventional FD baseline")
d7 = d.get("lhs_on_exact") or d.get("model_offset") or {}
print(f"    FD probe LHS on the exact (u0,v0): DLW1={d7.get('DLW1_lhs'):.4e}  "
      f"DLW2={d7.get('DLW2_lhs'):.4e}  (dx^4 probe floor, NOT a model offset)")
for r in d.get("dt_refinement", []):
    if r.get("diverged"):
        print(f"    dt={r['dt']:.2e} DIVERGED")
    else:
        print(f"    dt={r['dt']:.2e}  Einf_v={r['Einf_v']:.4e}  slope={r['slope_v']}")
