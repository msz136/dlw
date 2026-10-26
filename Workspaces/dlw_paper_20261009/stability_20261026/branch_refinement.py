"""Refinement check of the growing branch: h = 0.1 versus h = 0.05."""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from linear_spectrum import modal_matrix, rest_model  # noqa: E402

MODES = (5, 10, 20, 30)


def main():
    out = {}
    for h in (0.1, 0.05):
        for method in ("Endpoint-SD", "Centered-SD"):
            m = rest_model(method, dx=0.1, h=h)
            rows = []
            for j in MODES:
                xi = 2 * np.pi * j / (2 * m.half)
                M = modal_matrix(m, xi)
                lam = np.linalg.eigvals(M)
                rows.append(dict(j=j, xi=float(xi), re_sigma=float(lam.real.max()),
                                 xi2=float(xi ** 2),
                                 ratio=float(lam.real.max() / xi ** 2),
                                 excess=float(lam.real.max() - xi ** 2)))
                print(h, method, rows[-1], flush=True)
            out[f"{method}_h{h}"] = rows
    (HERE / "branch_refinement.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
