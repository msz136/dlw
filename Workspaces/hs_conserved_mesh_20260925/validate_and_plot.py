"""Check saved ALE runs and visualize the measured mesh/field tradeoff."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
rows = json.loads((OUT / "results.json").read_text(encoding="utf-8"))
long_rows = json.loads((OUT / "long_results.json").read_text(encoding="utf-8"))
long_cross = json.loads((OUT / "long_crossovers.json").read_text(encoding="utf-8"))


def row(p, n, dt, mode, grid_mode=None):
    grid_mode = mode if grid_mode is None else grid_mode
    selected = [r for r in rows if (r["p"], r["n"], r["dt"], r["mode"], r["grid_mode"])
                == (p, n, dt, mode, grid_mode)]
    assert len(selected) == 1
    return selected[0]


for r in rows + long_rows + long_cross:
    assert r["initial"]["node"]["u_linf"] < 1e-10
    assert r["initial"]["node"]["rho_linf"] < 1e-10
    for snapshot in (r["initial"], *r["snapshots"]):
        assert snapshot["min_rho"] > 0 and snapshot["min_Rm"] > 0
        assert snapshot["min_h"] > 0
        for region in ("full", "node", "reconstruction"):
            assert all(np.isfinite(list(snapshot[region].values())))
    if r["mode"] == r["grid_mode"] and r["mode"] != "fixed":
        assert r["snapshots"][-1]["cell_mass_max_rel_drift"] < .004

# Time error is already far below space error at the two selected RK4 steps.
for mode in ("fixed", "rho", "rm"):
    a = np.load(OUT / f"profile_p5_{mode}_n200_dt0.001.npz")
    b = np.load(OUT / f"profile_p5_{mode}_n200_dt0.0005.npz")
    assert max(np.max(np.abs(a[field] - b[field])) for field in ("x", "u", "rho")) < 1e-10

# Full errors exhibit second-order grid refinement to a useful tolerance.
orders = {}
for p in (5, 12):
    orders[str(p)] = {}
    for mode in ("fixed", "rho", "rm"):
        coarse = row(p, 200, .0005 if p == 12 else .001, mode)["snapshots"][-1]["full"]
        fine = row(p, 400, .0005, mode)["snapshots"][-1]["full"]
        orders[str(p)][mode] = {}
        for field in ("u_linf", "rho_linf"):
            rate = float(np.log2(coarse[field] / fine[field]))
            orders[str(p)][mode][field] = rate
            assert 1.8 < rate < 2.2, (p, mode, field, rate)

fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
colors = {"fixed": "#52616b", "rho": "#e69f00", "rm": "#0072b2"}
labels = {"fixed": "uniform fixed", "rho": "rho moving", "rm": "Rm moving"}
for ridx, p in enumerate((5, 12)):
    T = .25 if p == 5 else .1
    x = np.arange(3)
    ax = axes[ridx, 0]
    for j, field in enumerate(("u_linf", "rho_linf")):
        values = [row(p, 400, .0005, m)["snapshots"][-1]["full"][field]
                  for m in ("fixed", "rho", "rm")]
        ax.bar(x + (j - .5) * .32, values, width=.3,
               color="#0072b2" if j == 0 else "#d55e00",
               label="u" if j == 0 else "rho")
    ax.set(yscale="log", xticks=x, xticklabels=[labels[m] for m in ("fixed", "rho", "rm")],
           title=f"p={p}, T={T}: common-x total error", ylabel="L-infinity error")
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=.2)
    ax = axes[ridx, 1]
    for mode in ("fixed", "rho", "rm"):
        data = np.load(OUT / f"profile_p{p}_{mode}_n400_dt0.0005.npz")
        xc = (data["x"][1:] + data["x"][:-1]) / 2
        ax.plot(xc, np.diff(data["x"]), color=colors[mode], label=labels[mode])
    ax.set(xlim=(-1.5, 1.5), title=f"p={p}: final cell widths",
           xlabel="physical x", ylabel="cell width")
    ax.grid(alpha=.2)
    ax.legend(fontsize=8)
fig.savefig(OUT / "mesh_comparison.png", dpi=180)
plt.close(fig)

(OUT / "validation.json").write_text(json.dumps({"status": "passed", "spatial_orders": orders,
    "time_step_check": "p=5, N=200, dt=.001 versus .0005: all saved fields differ <1e-10",
    "positivity_and_spacing": "all saved runs positive and untangled"}, indent=2) + "\n",
    encoding="utf-8")
print("PASSED: positivity, untangled meshes, RK4 time control, and near-second-order spatial convergence")
print(json.dumps(orders, indent=2))
