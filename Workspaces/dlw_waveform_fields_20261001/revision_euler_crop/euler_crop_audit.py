"""Independently check the Euler-only error figures cropped to [-1,1].

Reads the original fields and direct rational tau reference. No solver is
imported and no trajectory is run. Writes only euler_crop_audit.json here.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from audit_saved_fields import MANIFESTS, YY, continuous_tau_fields, sha

TIME = 0.01
ORIGINAL_XX = np.linspace(-10.0, 10.0, 4001)
MASK = (ORIGINAL_XX >= -1.0) & (ORIGINAL_XX <= 1.0)
XX = ORIGINAL_XX[MASK]
assert len(XX) == 401 and XX[0] == -1.0 and XX[-1] == 1.0
SOURCES = {key: MANIFESTS[key] for key in ("single", "corrected", "two_euler")}


def euler_runs() -> list:
    selected = []
    for kind, path in SOURCES.items():
        source = json.loads(path.read_text(encoding="utf-8"))
        for run in source["runs"]:
            spec = dict(run["spec"])
            spec.setdefault("method", "Euler" if kind == "two_euler" else "RK4")
            if spec["method"] != "Euler" or spec["variant"] != "main":
                continue
            if kind == "single":
                if spec["case"] not in ("fig1a", "fig1b"):
                    continue
            elif spec["case"] != "fig3" or (spec["model"] == "SD2") != (kind == "corrected"):
                continue
            selected.append((spec, run, path))
    keys = [tuple(s[k] for k in ("case", "method", "mesh", "model")) for s, _, _ in selected]
    assert len(keys) == len(set(keys)) == 18
    return selected


def main() -> None:
    validation_path = HERE / "euler_plot_validation.json"
    plotted = json.loads(validation_path.read_text(encoding="utf-8"))
    lookup = {}
    for record in plotted["records"]:
        assert record["method"] == "Euler"
        key = tuple(record[k] for k in ("case", "method", "mesh", "model", "field"))
        assert key not in lookup
        lookup[key] = record
    assert len(lookup) == 36
    checks = []
    for spec, run, manifest in euler_runs():
        profile = Path(run["profile"])
        digest = sha(profile)
        assert digest == run["profile_sha256"]
        with np.load(profile, allow_pickle=False) as saved:
            assert np.array_equal(saved["y"], YY)
            x = saved["t0.01_x"]
            assert x.shape == (256,) and np.all(np.diff(x) > 0)
            assert x[0] <= ORIGINAL_XX[0] and x[-1] >= ORIGINAL_XX[-1]
            exact = continuous_tau_fields(spec["case"], ORIGINAL_XX, YY, TIME)
            for field in ("u", "v"):
                native = saved["t0.01_" + field]
                assert native.shape == (24, 256) and np.all(np.isfinite(native))
                sampled = CubicSpline(x, native, axis=-1)(ORIGINAL_XX)
                signed = (sampled - exact[field])[:, MASK]
                error = np.abs(signed)
                maximum = float(error.max())
                j, i = np.unravel_index(np.argmax(error), error.shape)
                px, py = float(XX[i]), float(YY[j])
                key = tuple(spec[k] for k in ("case", "method", "mesh", "model")) + (field,)
                record = lookup[key]
                assert Path(record["profile"]) == profile
                assert record["profile_sha256"] == digest
                difference = abs(maximum - record["cropped_max"])
                dx, dy = abs(px - record["max_x"]), abs(py - record["max_y"])
                assert difference < 1e-12
                assert dx == dy == 0.0, key
                upper = float(record.get("color_upper", plotted["color_limits"][spec["case"]][field]))
                assert np.isfinite(upper) and upper > 0.0 and upper + 1e-12 >= maximum
                checks.append({
                    "case": spec["case"], "method": "Euler", "model": spec["model"], "mesh": spec["mesh"], "field": field,
                    "manifest": str(manifest), "profile": str(profile), "profile_sha256": digest, "hash_verified": True,
                    "cropped_max": maximum, "plotted_cropped_max": record["cropped_max"], "maximum_error_abs_difference": difference,
                    "max_x": px, "max_y": py, "maximum_x_difference": dx, "maximum_y_difference": dy,
                    "signed_error_range": [float(signed.min()), float(signed.max())],
                    "color_upper": upper, "color_upper_over_local_max": upper / maximum,
                })
    assert len(checks) == 36
    source_paths = [*SOURCES.values(), validation_path, Path(__file__), HERE.parent / "audit_saved_fields.py"]
    report = {
        "new_pde_trajectories": 0,
        "evaluation": {"time": TIME, "method": "Euler only", "original_x_interval": [-10.0, 10.0], "original_x_count": 4001, "cropped_x_interval": [-1.0, 1.0], "cropped_x_count": len(XX), "y_count": len(YY), "physical_y": YY.tolist(), "reference": "Independent direct rational positive tau derivatives", "interpolation": "Original 4001 physical x points, CubicSpline not-a-knot along x; retain the inclusive 401-point [-1,1] subset; no y interpolation", "error": "Maximum absolute total error on the cropped sampled physical grid"},
        "summary": {"source_runs": 18, "fields": len(checks), "source_profile_hashes_verified": 18, "all_records_Euler": True, "maximum_error_abs_difference": max(c["maximum_error_abs_difference"] for c in checks), "all_error_peak_x_y_match_exactly": True, "maximum_x_difference": 0.0, "maximum_y_difference": 0.0, "all_color_limits_cover_local_maximum": True},
        "sources": [{"path": str(path), "sha256": sha(path)} for path in source_paths],
        "records": checks,
    }
    destination = HERE / "euler_crop_audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"output": str(destination), **report["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
