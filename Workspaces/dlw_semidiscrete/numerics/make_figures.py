# -*- coding: utf-8 -*-
"""Generate the figures for REPORT.md from the result JSON artifacts.

Every figure is built from out/*.json, so the pictures cannot drift from the
numbers in the report.  Output: figures/*.png (matplotlib, no seaborn styling).
"""

import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)


def load(n):
    with open(os.path.join(OUT, n), encoding="utf-8") as f:
        return json.load(f)


plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 9,
    "axes.grid": True, "grid.alpha": 0.3, "axes.axisbelow": True,
    "figure.autolayout": True,
})

# ---------------------------------------------------------------- fig 1: E0/E1
fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.4))

d0 = load("e0_benchmark.json")
hs, ex, fd = [], [], []
for c in d0["checks"]:
    if c["kind"] == "bilinear_residual" and c.get("case") == "A":
        hs.append(c["h"]); ex.append(c["max_abs_exact_Rminus"])
        fd.append(c["max_abs_fd_Rminus"])
hs, ex, fd = map(np.array, (hs, ex, fd))
o = np.argsort(hs); hs, ex, fd = hs[o], ex[o], fd[o]
ax[0].loglog(hs, ex, "o-", label="exact lattice pair")
ax[0].loglog(hs, fd, "s-", label="naive difference quotient")
ax[0].loglog(hs, fd[0] * (hs / hs[0]) ** 2, "k--", lw=1, label=r"$O(h^2)$ reference")
ax[0].set_xlabel("h"); ax[0].set_ylabel(r"max $|$residual$|$")
ax[0].set_title("E0  exact identity vs difference quotient")
ax[0].legend(fontsize=7)

d1 = load("e1_continuum.json")
rows = d1["cases"]["A"]["rows"]
h1 = np.array([r["h"] for r in rows])
ax[1].loglog(h1, [r["Einf_u"] for r in rows], "o-", label=r"$E_\infty(u)$")
ax[1].loglog(h1, [r["E2_u"] for r in rows], "s-", label=r"$E_2(u)$")
ax[1].loglog(h1, rows[0]["Einf_u"] * (h1 / h1[0]) ** 2, "k--", lw=1,
             label=r"$O(h^2)$ ($E_\infty$)")
ax[1].loglog(h1, rows[0]["E2_u"] * (h1 / h1[0]) ** 2, "k:", lw=1,
             label=r"$O(h^2)$ ($E_2$)")
ax[1].set_xlabel("h"); ax[1].set_ylabel("error vs continuum")
ax[1].set_title("E1  continuum-limit order, case A")
ax[1].legend(fontsize=7)
fig.savefig(os.path.join(FIG, "fig1_e0_e1_convergence.png"))
plt.close(fig)

# ------------------------------------------------------------------- fig 2: E6
fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.4))
d6 = load("e6_growth.json")
bt = d6["branch_table"]
k = np.array([r["k"] for r in bt], dtype=float)
re = np.array([r["Re_growing"] for r in bt])
ax[0].loglog(k, re, "o-", label=r"$\mathrm{Re}\,\sigma$ (growing branch)")
ax[0].loglog(k, k ** 2, "k--", lw=1, label=r"$k^2$")
ax[0].set_xlabel("x-wavenumber k"); ax[0].set_ylabel(r"$\mathrm{Re}\,\sigma$")
ax[0].set_title("E6  growth rate follows $k^2$ (report eq. (S))")
ax[0].legend(fontsize=7)

gb = d6["grid_budget"]
nx = np.array([b["nx"] for b in gb], dtype=float)
Tb = np.array([b["T_budget"] for b in gb])
Tc = np.array([np.log(1e-6 / 1e-12) / b["g_max_continuous_nyq"] for b in gb])
ax[1].loglog(nx, Tb, "o-", label="open-chain modal estimate (zero background)")
ax[1].loglog(nx, Tc, "s--", label=r"continuous $k=\pi/dx$ estimate")
ax[1].set_xlabel("x-grid points nx"); ax[1].set_ylabel(r"modal amplification time $T$")
ax[1].set_title("E6  linear estimates, not nonlinear stability bounds")
ax[1].legend(fontsize=7)
fig.savefig(os.path.join(FIG, "fig2_e6_growth_budget.png"))
plt.close(fig)

# ------------------------------------------------------------------- fig 3: E4
fig, ax = plt.subplots(figsize=(4.8, 3.4))
d4 = load("e4_twosoliton.json")
ms = [m for m in d4["measured_vs_predicted"] if m.get("measured_dx") is not None]
lab = [f"soliton {m['i']}" for m in ms]
meas = [m["measured_dx"] for m in ms]
pred = [m["predicted_dx"] for m in ms]
x = np.arange(len(ms))
ax.bar(x - 0.18, pred, 0.36, label="predicted  $\\log 6/(p_i+q_i)$")
ax.bar(x + 0.18, meas, 0.36, label="measured (profile fit)")
ax.set_xticks(x); ax.set_xticklabels(lab)
ax.set_ylabel(r"phase shift $|\Delta x_i|$")
ax.set_title("E4  two-soliton phase shift")
ax.legend(fontsize=7)
fig.savefig(os.path.join(FIG, "fig3_e4_phase_shift.png"))
plt.close(fig)

# ------------------------------------------------ fig 4: actual solver time order
ds = load("e2_e3_self_convergence.json")
fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
for ax, h in zip(axes, (0.25, 0.125)):
    for study in [r for r in ds['studies'] if r['h']==h]:
        rows=study['successive_differences']
        steps=np.array([study['t_end']/r['coarse_n'] for r in rows])
        diffs=np.array([r['differences_Linf']['v'] for r in rows])
        order=rows[-1]['orders']['v']
        line,=ax.loglog(steps,diffs,'o-',label=f"{study['method']} (last p={order:.2f})")
        ax.loglog(steps,diffs[-1]*(steps/steps[-1])**study['expected_order'],
                  '--',color=line.get_color(),alpha=.65,linewidth=1)
    ax.set_xlabel('coarse time step')
    ax.set_ylabel(r'$\|v_{\Delta t}-v_{\Delta t/2}\|_\infty$')
    ax.set_title(f'E2/E3 fixed-grid time refinement, h={h}')
    ax.legend(fontsize=8)
    ax.grid(True,which='both',alpha=.2)
fig.suptitle('nx=256, T=0.05; dashed lines: orders 1/4/2 anchored at finest difference',fontsize=10)
fig.savefig(os.path.join(FIG,'fig4_e2_e3_time_order.png'))
plt.close(fig)

print("wrote:")
for f in sorted(os.listdir(FIG)):
    print("  figures/" + f)
