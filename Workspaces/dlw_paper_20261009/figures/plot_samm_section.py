"""Selected spacing layout C, from saved real coupled-mesh data."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
P = Path(__file__).resolve().parent
ROOT = P.parent
plt.rcParams.update({"font.family": "STIXGeneral", "mathtext.fontset": "stix",
                     "font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False})
def save(fig, name):
    fig.savefig(P / (name + ".png"), dpi=300, bbox_inches="tight")
    fig.savefig(P / (name + ".pdf"), bbox_inches="tight")
    plt.close(fig)
d = np.load(ROOT / "mesh_preview_20261020/case_C_mesh.npz")
spacing = np.mean(np.diff(d["uniform"]))
fig, ax = plt.subplots(figsize=(8, 3.5), layout="constrained")
for key, color, ls, label in [
    ("xf", "#0072B2", "-", "SAMM at $T=0.01$"),
    ("x0", "#767676", "--", "Adaptive initial mesh")]:
    x = d[key]
    ax.plot((x[:-1]+x[1:])/2, np.diff(x)/spacing, color=color,
            ls=ls, lw=1.7, label=label)
ax.axhline(1, color="#D55E00", ls=":", label="Uniform mesh")
ax.set(xlim=(-30,30), xlabel="$x$", ylabel="Local spacing / uniform spacing")
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(.5,1.02), ncol=3)
ax.grid(alpha=.15)
save(fig, "SAMM_spacing_C")
