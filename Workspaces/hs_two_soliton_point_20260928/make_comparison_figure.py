"""Plot the common portion of the two completed/failing time trajectories."""
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

data = json.loads((HERE / "results.json").read_text(encoding="utf-8"))["results"]["main"]
sol = Soliton((1.1, 1.25), phase=(np.log(6.5),)*2, shift=-(1/11+1/5))
grid = np.linspace(-2.5, 1.5, 16001)
fig, axes = plt.subplots(2, 3, figsize=(13, 6), layout="constrained")
for j, t in enumerate((-2.5, -2.0, 0.0)):
    ue, re, _ = sol.continuous_x(grid, t)
    for i, (field, exact) in enumerate((("u", ue), ("rho", re))):
        ax = axes[i, j]
        ax.plot(grid, exact, "k", lw=2, label="continuous exact")
        for kind, label, color in (("sd", "integrable SD", "#c44935"),
                                   ("fd", "ordinary moving FD", "#256caa")):
            if str(t) not in data[kind]["metrics"]:
                continue
            with np.load(HERE / data[kind]["profile"]) as z:
                x = z[f"t{t}_{'x' if field == 'u' else 'rho_x'}"]
                y = z[f"t{t}_{field}"]
                ax.plot(grid, np.interp(grid, x, y), lw=1.25, color=color, label=label)
        ax.set(xlabel="physical x", ylabel=field, title=f"t={t:g}")
        ax.grid(alpha=.2)
        ax.legend(fontsize=7)
fig.suptitle("Paper two-soliton point, common exact lattice initial state")
fig.savefig(HERE / "comparison_before_failure.png", dpi=180)
plt.close(fig)
