"""Plot the current S1-S4 results at one locked paper two-soliton point."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "hs_numerics_plan"))
from hs_exact import Soliton

results = json.loads((HERE / "four_schemes_results.json").read_text(encoding="utf-8"))["results"]
sol = Soliton((1.1, 1.25), phase=(np.log(6.5),)*2, shift=-(1/11+1/5))
grid = np.linspace(-2.5, 1.5, 16001)
fig, axes = plt.subplots(2, 3, figsize=(13, 6), layout="constrained")
colors = {"S1":"#bd3f32", "S2":"#db8d2b", "S3":"#36739b", "S4":"#368b6f"}
for col, t in enumerate((-2.5, 0.0, 3.0)):
    ue, re, _ = sol.continuous_x(grid, t)
    for row, (field, exact) in enumerate((("u", ue), ("rho", re))):
        ax = axes[row, col]
        ax.plot(grid, exact, color="black", lw=2, label="continuous exact")
        for scheme, result in results.items():
            if str(t) not in result["metrics"]:
                continue
            with np.load(HERE / result["profile"]) as z:
                x = z[f"t{t}_{'x' if field == 'u' else 'rho_x'}"]
                y = z[f"t{t}_{field}"]
                ax.plot(grid, np.interp(grid, x, y), lw=1.2,
                        color=colors[scheme], label=scheme)
        ax.set(xlabel="physical x", ylabel=field, title=f"t={t:g}")
        ax.grid(alpha=.2)
        ax.legend(fontsize=8)
fig.suptitle("One paper two-soliton point: current S1-S4, common continuous initial data")
fig.savefig(HERE / "four_schemes_line.png", dpi=180)
plt.close(fig)
