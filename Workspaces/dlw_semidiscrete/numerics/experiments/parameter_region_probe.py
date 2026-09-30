"""Local parameter-box diagnostic for actual fixed-grid RK4 error.

Finite differences and box corners here are empirical probes, not certified
derivative bounds. The holdout H001--H064 is deliberately not used.
"""

from itertools import product
from pathlib import Path
import hashlib
import json
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
from parametric import Parameters, rk4
from parametric_open import OpenModel

COORDS = ("S", "g", "nu", "x_c")
CENTER = {"S": 3.0, "g": 3.0, "nu": 0.0, "x_c": 0.0}
RADIUS = 0.01
H, NX, L, DT, T = 0.125, 256, 40.0, 0.00025, 0.01
OBSERVATIONS = (0.005, 0.01)
OUT = ROOT / "design" / "parameter_region_probe.json"


def norm(fields):
    return max(float(np.max(np.abs(f))) for f in fields)


def fields_at(coords):
    S, g, nu, x_c = (coords[k] for k in COORDS)
    p, q = S * (1 + nu) / 2, S * (1 - nu) / 2
    a = g + p
    assert 1.5 <= S <= 5 and 0.5 <= g <= 5
    assert -0.5 <= nu <= 0.5 and -1 <= x_c <= 1 and 2 <= a <= 6
    pars = Parameters(a=a, p=p, q=q, rho=S * np.exp(-S * x_c))
    model = OpenModel(pars, H, NX, L=L, yhalf=1.5, model="structure")
    z = model.exact(0.0)
    result = {}
    for k in range(1, round(T / DT) + 1):
        z = rk4(model.rhs, (k - 1) * DT, z, DT)
        if not np.all(np.isfinite(z)):
            raise FloatingPointError(f"nonfinite state at step {k}")
        t = round(k * DT, 12)
        if t in OBSERVATIONS:
            u, v = model.error_fields(z - model.exact(t))
            result[t] = (u / S, v / 4)
    assert len(result) == len(OBSERVATIONS)
    return result


def shifted(point, changes):
    result = dict(point)
    for k, delta in changes.items():
        result[k] += delta
    return result


def main():
    center = fields_at(CENTER)
    slopes = {}
    axis = []
    for name in COORDS:
        plus = fields_at(shifted(CENTER, {name: RADIUS}))
        minus = fields_at(shifted(CENTER, {name: -RADIUS}))
        slopes[name] = max(norm(tuple((a - b) / (2 * RADIUS)
                                      for a, b in zip(plus[t], minus[t])))
                           for t in OBSERVATIONS)
        axis.append({"coordinate": name,
                     "E_plus": {str(t): norm(plus[t]) for t in OBSERVATIONS},
                     "E_minus": {str(t): norm(minus[t]) for t in OBSERVATIONS},
                     "central_secant_slope": slopes[name]})
    corners = []
    for signs in product((-1, 1), repeat=4):
        point = shifted(CENTER, {k: RADIUS * s for k, s in zip(COORDS, signs)})
        fields = fields_at(point)
        corners.append({"signs": signs,
                        "error": {str(t): norm(fields[t]) for t in OBSERVATIONS}})
    center_error = {str(t): norm(center[t]) for t in OBSERVATIONS}
    secant_prediction = max(center_error.values()) + RADIUS * sum(slopes.values())
    max_corner_error = max(max(row["error"].values()) for row in corners)
    ell = (round(3 / H) - 1) * H
    Dh = 1 / (0.5 - H / 2) + 1 / (1.5 + 0.5 - H / 2)
    Q, B, b = 5 * Dh, 5 * Dh, 22.0
    data = {
        "scope": "diagnostic, not interval certificate",
        "equation": "finite-h SD, fixed x grid, background-relative quadratic y extrapolation",
        "method": "actual RK4; finite-h Gram reference; e0=0",
        "config": {"center": CENTER, "radius_each_coordinate": RADIUS,
                   "h": H, "nx": NX, "L": L, "dt": DT, "observations": OBSERVATIONS},
        "metric": "max(||e_u||_inf/S, ||e_v||_inf/4), same physical grid",
        "center_error": center_error, "axis": axis, "corners": corners,
        "max_corner_error": max_corner_error,
        "local_secant_prediction_not_bound": secant_prediction,
    }
    # The intentionally crude global K from PARAMETRIC_THEORY.md is reported
    # for the planned 512-point grid, separate from this 256-point probe.
    d512 = 3 / (2 * (40 / 512))
    data["global_norm_bound_diagnostic"] = {
        "h": H, "nx": 512, "L": 40,
        "K_P": d512 * (b + B * ell + H * (Q / 8 + 0.5)) + d512 * d512 * 4,
        "K_W": d512 * (b + (Q + 4) * ell) + d512 * d512,
        "scope": "uniform coarse upper bound over full parameter domain; not actual growth"
    }
    source = Path(__file__).read_bytes()
    manifest = ROOT / "design" / "manifest.json"
    data["source_sha256"] = hashlib.sha256(source).hexdigest()
    data["manifest_sha256"] = hashlib.sha256(manifest.read_bytes()).hexdigest()
    OUT.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print("center", center_error)
    print("max corner", max_corner_error, "secant prediction (not bound)", secant_prediction)
    print("global K at nx512", data["global_norm_bound_diagnostic"]["K_P"])
    print(OUT)


if __name__ == "__main__":
    main()
