"""Reproduce the Centered-SD physical perturbation response figure and table.

Layout: paired, aligned line panels from oa-tech-pone-0116670-f16.
Color: blue solid for u-only input; orange dashed for v-only input.
Typography: STIX serif, consistent with the DLW paper.
Data: native maxima at all 101 saved times, divided by epsilon (no smoothing).
The table's L2 pair gain has a different, explicitly stated denominator.
"""
from pathlib import Path
import hashlib
import html
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "four_case_kappa_pi_over_2"
OUT = ROOT / Path(__file__).stem
CASES = ("A", "D", "Gaussian", "Sinusoidal")
NAMES = {"A": "One-soliton", "D": "Two-soliton", "Gaussian": "Gaussian", "Sinusoidal": "Sinusoidal"}
COLORS = ("#5070a6", "#c97932")
STYLES = ("-", (0, (4.2, 2.4)))
EPSILON = 1e-6

plt.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 10, "axes.labelsize": 11, "axes.titlesize": 10.5,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 10,
    "axes.linewidth": .65, "lines.linewidth": 1.65,
    "savefig.facecolor": "white", "pdf.fonttype": 42, "ps.fonttype": 42,
})

endpoint = json.loads((DATA / "endpoint_norms.json").read_text(encoding="utf-8"))
endpoint_lookup = {(r["case"], r["perturbed_field"]): r for r in endpoint["records"]}
records = []
checks = []
fig, axes = plt.subplots(4, 2, figsize=(7.2, 8.8), sharex=True, sharey=True)
fig.subplots_adjust(left=.10, right=.955, top=.915, bottom=.07, hspace=.36, wspace=.20)
fig.legend(
    handles=[Line2D([], [], color=COLORS[i], linestyle=STYLES[i], label=label)
             for i, label in enumerate((r"$u$-only input", r"$v$-only input"))],
    loc="upper center", bbox_to_anchor=(.535, .993), ncol=2, frameon=False,
    handlelength=3.1, columnspacing=2.7,
)
fig.text(.295, .945, r"$\|\delta u_h(t)\|_\infty/\varepsilon$", ha="center", va="center", fontsize=13)
fig.text(.76, .945, r"$\|\delta v_h(t)\|_\infty/\varepsilon$", ha="center", va="center", fontsize=13)

for row, case in enumerate(CASES):
    meta = json.loads((DATA / f"{case}.json").read_text(encoding="utf-8"))
    npz_path = DATA / f"{case}.npz"
    digest = hashlib.sha256(npz_path.read_bytes()).hexdigest()
    assert digest == meta["artifact_sha256"], case
    assert meta["epsilon"] == EPSILON and meta["reached"] == .01, case
    with np.load(npz_path) as data:
        t = data["t"]
        values = data["delta_max"] / EPSILON
    assert t.shape == (101,) and values.shape == (101, 2, 2), case
    assert np.all(np.isfinite(values)) and np.all(values >= 0), case
    assert np.allclose(t, np.linspace(0, .01, 101), rtol=0, atol=1e-16), case
    assert np.allclose(values[-1], np.asarray(meta["final_delta_max"]) / EPSILON, rtol=1e-14, atol=0), case
    for col in range(2):
        ax = axes[row, col]
        for input_id in range(2):
            ax.plot(t, values[:, input_id, col], color=COLORS[input_id], linestyle=STYLES[input_id])
        ax.set_title(f"({chr(97 + 2*row + col)}) {NAMES[case]}", loc="left", pad=6)
        ax.set_xlim(0, .01)
        ax.set_ylim(-.035, 1.10)
        ax.set_xticks([0, .0025, .005, .0075, .01])
        ax.set_xticklabels(["0", "0.0025", "0.0050", "0.0075", "0.0100"])
        ax.set_yticks([0, .25, .5, .75, 1])
        ax.set_yticklabels(["0", "0.25", "0.50", "0.75", "1.00"])
        ax.tick_params(direction="in", top=True, right=True, length=3.2, width=.6)
        if row == 3:
            ax.set_xlabel(r"$t$", labelpad=4)
    for input_id, input_field in enumerate(("u", "v")):
        e = endpoint_lookup[(case, input_field)]
        assert e["source_sha256"] == digest, case
        records.append({
            "case": case, "case_label": NAMES[case], "input_field": input_field,
            "T": .01, "epsilon": EPSILON,
            "native_max_delta_u_over_epsilon": float(values[-1, input_id, 0]),
            "native_max_delta_v_over_epsilon": float(values[-1, input_id, 1]),
            "L2_pair_gain": e["L2_pair_gain"],
            "fourier_8x_max_delta_u_over_epsilon": e["fourier_interpolant_max"]["8"]["final"][0] / EPSILON,
            "fourier_8x_max_delta_v_over_epsilon": e["fourier_interpolant_max"]["8"]["final"][1] / EPSILON,
            "source_sha256": digest,
        })
    checks.append({"case": case, "sha256": digest, "curves": 4, "points_per_curve": 101,
                   "global_plotted_max": float(values.max()), "global_plotted_min": float(values.min())})

fig.savefig(OUT.with_suffix(".png"), dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"Title": "Centered-SD physical perturbation responses", "Author": "", "Subject": "Native maximum-norm response to independent physical-field inputs"})
plt.close(fig)

definitions = {
    "native_max_response": "max over the experiment's native evaluation nodes divided by epsilon=1e-6, as plotted",
    "L2_pair_gain": "sqrt(||delta u(T)||_2,h^2+||delta v(T)||_2,h^2)/sqrt(||delta u(0)||_2,h^2+||delta v(0)||_2,h^2)",
    "L2_domain": "full periodic x interval, native y evaluation region; squared norm uses h*dx*sum(q^2)",
    "fourier_8x_max": "finite-grid Fourier interpolant evaluated on eightfold denser x nodes, same y rows; divided by epsilon",
    "scope": "finite-grid nonlinear sensitivity of the natural Centered-SD method",
    "continuous_certificate": False,
}
(ROOT / "perturbation_endpoint_table.json").write_text(json.dumps({"definitions": definitions, "records": records}, indent=2), encoding="utf-8")

rows = []
for i, r in enumerate(records):
    case_cell = f'<th scope="rowgroup" rowspan="2">{html.escape(r["case_label"])}</th>' if i % 2 == 0 else ""
    row_class = ' class="case-start"' if i % 2 == 0 else ""
    rows.append(f'<tr{row_class}>{case_cell}<td>\\({r["input_field"]}_0\\) only</td><td>{r["native_max_delta_u_over_epsilon"]:.5f}</td><td>{r["native_max_delta_v_over_epsilon"]:.5f}</td><td>{r["L2_pair_gain"]:.5f}</td></tr>')
fragment = r'''<table class="paper-table perturbation-table">
<caption>Centered-SD perturbation responses at \(T=0.01\). Each experiment adds \(\varepsilon\phi\), \(\varepsilon=10^{-6}\), to one initial physical field.</caption>
<thead><tr><th>Background</th><th>Perturbed field</th><th>\(\|\delta u_h(T)\|_\infty/\varepsilon\)</th><th>\(\|\delta v_h(T)\|_\infty/\varepsilon\)</th><th>Pair \(L^2_h\) gain</th></tr></thead>
<tbody>
''' + "\n".join(rows) + r'''
</tbody></table>
<p class="table-note">The maximum norms use the native evaluation nodes. The pair gain is \(\left(\|\delta u_h(T)\|_{2,h}^2+\|\delta v_h(T)\|_{2,h}^2\right)^{1/2}/\left(\|\delta u_h(0)\|_{2,h}^2+\|\delta v_h(0)\|_{2,h}^2\right)^{1/2}\), evaluated over the full periodic \(x\) interval and the specified interior \(y\) nodes.</p>
'''
(ROOT / "perturbation_endpoint_table.html").write_text(fragment, encoding="utf-8")

manifest = {"figure": OUT.name, "layout": "four rows by two columns", "normalization": "epsilon=1e-6", "interpolation_or_smoothing": "none", "curve_count": 16, "checks": checks, "definitions": definitions}
(ROOT / "figure_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps({"outputs": [str(OUT.with_suffix(s)) for s in (".png", ".pdf", ".py")], "table": str(ROOT / "perturbation_endpoint_table.html"), "curves": 16, "points_each": 101}, indent=2))
