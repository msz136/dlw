"""Amplification budget of the measured t=0 defect.

For each case and formulation we take the production initial state, form the
time-derivative defect (numerical RHS minus the exact continuous rate) at the
native locations, transform it in x, and compare its modal amplitude with the
linear growth factor exp(xi^2 T) of the x-wavenumber.
"""
import json
import sys
from pathlib import Path

import numpy as np

PROJECT = Path(r"C:\Users\msz\aca\Workspaces\dlw_paper_20261009")
SPATIAL = PROJECT / "spatial_audit_20261023"
sys.path.insert(0, str(SPATIAL))
sys.path.insert(0, str(SPATIAL / "separated"))
from run import Model, HALF_WIDTHS  # noqa: E402
from run_separated import fields  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = PROJECT / "report_refresh_20261024" / "rk4_spatial"
T = 0.01


def defect_spectrum(case, method, dx=0.1, h=0.1):
    m = Model(case, method, dx, h)
    z0 = m.initial()
    num = m.rhs(0.0, z0)
    u, _, tu = fields(m, m.y)
    _, v, tv = fields(m, m.yv)
    exact = np.array([tu[0], tv[1]])
    defect = num - exact
    out = {}
    freq = 2 * np.pi * np.fft.rfftfreq(m.nx, m.dx)
    for j, name in enumerate(("u", "v")):
        amp = np.abs(np.fft.rfft(defect[j], axis=-1)) / m.nx
        # restrict to the region used in the paper
        yy = (m.y, m.yv)[j]
        mask = np.abs(yy) < HALF_WIDTHS[case]
        prof = amp[mask].max(axis=0)
        out[name] = prof
    rec = {"case": case, "method": method, "nx": m.nx, "dx": m.dx,
           "defect_max": [float(np.max(np.abs(defect[0]))), float(np.max(np.abs(defect[1])))],
           "growth_envelope": (np.exp(freq ** 2 * T)).tolist(),
           "freq": freq.tolist()}
    for name in ("u", "v"):
        budget = out[name] * np.exp(freq ** 2 * T)
        k = int(np.argmax(budget))
        rec[name] = {"modal_amplitude": out[name].tolist(),
                     "amplified_budget": budget.tolist(),
                     "worst_xi": float(freq[k]), "worst_budget": float(budget[k]),
                     "raw_max": float(out[name].max())}
    return rec


def main():
    rows = []
    for case in ("A", "B", "C", "D", "Gaussian", "Sinusoidal"):
        for method in ("Endpoint-SD", "Centered-SD", "FD"):
            rec = defect_spectrum(case, method)
            rows.append(rec)
            print("%-11s %-12s defect %.3e / %.3e   worst budget %.3e at xi=%.2f" % (
                case, method, rec["defect_max"][0], rec["defect_max"][1],
                max(rec["u"]["worst_budget"], rec["v"]["worst_budget"]),
                rec["v"]["worst_xi"] if rec["v"]["worst_budget"] > rec["u"]["worst_budget"] else rec["u"]["worst_xi"]),
                flush=True)
    (HERE / "defect_budget.json").write_text(json.dumps(rows), encoding="utf-8")


if __name__ == "__main__":
    main()
