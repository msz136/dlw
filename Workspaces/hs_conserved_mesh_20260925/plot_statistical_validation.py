"""Render the frozen confirmation data without refitting or changing tests."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "out" / "statistical_validation"
summary = json.loads((OUT / "summary.json").read_text(encoding="utf-8"))
cases = summary["cases"]
p = np.asarray([case["p"] for case in cases])
success = np.asarray([case["success"] for case in cases])
u = np.asarray([case["max_u_ratio"] for case in cases])
rho = np.asarray([case["max_rho_ratio"] for case in cases])
E = np.asarray([case["E_ratio"] for case in cases])
modest = (~success) & (u < 1)
worse = u >= 1

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), constrained_layout=True)
ax = axes[0]
ax.scatter(p[success], u[success], color="#0072b2", label="both fields: >=10% better (43)", s=30)
ax.scatter(p[modest], u[modest], color="#e69f00", label="all six better, but <10% (9)", s=36)
ax.scatter(p[worse], u[worse], color="#c44e52", label="u worse at t=.5 (8)", s=36)
ax.scatter(p, rho, color="#009e73", marker="x", label="rho: worst of 3 times", s=29)
ax.axhline(.9, color="#333333", linewidth=1.2, linestyle="--", label="10% improvement threshold")
ax.axhline(1., color="#888888", linewidth=.8, linestyle=":")
ax.set(xlabel="soliton parameter p", ylabel="largest Rm/fixed error ratio over t=.1,.25,.5",
       title="Paired total-error ratios", xlim=(2.8,12.2))
ax.grid(alpha=.2)
ax.legend(fontsize=7, loc="upper left")

ax = axes[1]
ax.scatter(p, E, c=np.where(success,"#0072b2",np.where(modest,"#e69f00","#c44e52")), s=32)
ax.axhline(1., color="#333333", linewidth=1.2, linestyle="--")
ax.axhline(summary["E_ratio"]["geometric_mean"], color="#0072b2", linewidth=1.,
           linestyle=":", label="geometric mean")
ax.set(xlabel="soliton parameter p", ylabel="normalized worst-error ratio E_Rm / E_fixed",
       title="Secondary combined error", xlim=(2.8,12.2))
ax.grid(alpha=.2)
ax.legend(fontsize=8)
fig.savefig(OUT / "confirmation.png", dpi=180)
plt.close(fig)
print(OUT / "confirmation.png")
