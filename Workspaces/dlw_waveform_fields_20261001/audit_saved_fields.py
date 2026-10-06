"""Independently audit saved DLW fields at T=.01; do not evolve a PDE.

This file deliberately imports no solver or experiment module. Analytic fields
are evaluated from direct rational tau derivatives, independently of the
production reference's log-sum evaluation. The source files are read only.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from bs4 import BeautifulSoup
from scipy.interpolate import CubicSpline

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / "Workspaces"
TIME = 0.01
XX = np.linspace(-10.0, 10.0, 4001)
YY = (np.arange(-12, 12) + 0.5) * 0.125
MANIFESTS = {
    "single": BASE / "dlw_single_aligned_20260929/out/results.json",
    "corrected": BASE / "dlw_sd2_uv_init_20260929/out/results.json",
    "two_rk": BASE / "dlw_two_soliton_20260929/out/results.json",
    "two_euler": BASE / "dlw_two_soliton_euler_20260929/out/results.json",
}
TABLES = [
    BASE / "dlw_single_aligned_20260929/out/index_t001.csv",
    BASE / "dlw_sd2_uv_init_20260929/out/comparison.csv",
]
CASE_LABELS = {"单孤子 A": "fig1a", "单孤子 B": "fig1b", "二孤子 C": "fig3"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def continuous_tau_fields(case: str, x: np.ndarray, y: np.ndarray, t: float) -> dict:
    """Direct F/G derivatives, with physical continuous y and zero phases."""
    if case in ("fig1a", "fig1b"):
        p, q = (1.0, 2.0) if case == "fig1a" else (4.0, -3.0)
        s, omega, ell = p + q, q * q - p * p, 1 / (p - 2) + 1 / (q + 2)
        gamma = -(p - 2) / (q + 2)
        e = np.exp(s * x[None, :] + omega * t + ell * y[:, None]) / s
        f, g = 1 + gamma * e, 1 + e
        return {
            "u": 2 * s * (gamma * e / f - e / g),
            "v": 2 * s * ell * (gamma * e / f**2 + e / g**2),
        }
    assert case == "fig3", case
    p, q = np.array([6.0, 4.0]), np.array([-5.0, -3.0])
    s, omega, ell = p + q, q * q - p * p, 1 / (p - 2) + 1 / (q + 2)
    cross = (p[0] - p[1]) * (q[0] - q[1]) / (
        (p[0] + q[0]) * (p[0] + q[1]) * (p[1] + q[0]) * (p[1] + q[1])
    )
    z = s[:, None, None] * x[None, None, :] + omega[:, None, None] * t + ell[:, None, None] * y[None, :, None]
    terms = np.stack((np.ones_like(z[0]), np.exp(z[0]), np.exp(z[1]), np.exp(z[0] + z[1])))
    gamma = -(p - 2) / (q + 2)
    cg = np.array([1.0, 1 / s[0], 1 / s[1], cross])
    cf = cg * np.array([1.0, gamma[0], gamma[1], np.prod(gamma)])
    sx = np.array([0.0, s[0], s[1], sum(s)])[:, None, None]
    sy = np.array([0.0, ell[0], ell[1], sum(ell)])[:, None, None]
    ux, xy = [], []
    for coeff in (cf, cg):
        a = coeff[:, None, None] * terms
        tau = np.sum(a, axis=0)
        tx, ty, txy = (np.sum(a * rate, axis=0) for rate in (sx, sy, sx * sy))
        ux.append(tx / tau)
        xy.append((txy * tau - tx * ty) / tau**2)
    return {"u": 2 * (ux[0] - ux[1]), "v": 2 * (xy[0] + xy[1])}


def selected_runs() -> list:
    selected = []
    for kind, path in MANIFESTS.items():
        manifest = json.loads(path.read_text(encoding="utf-8"))
        for run in manifest["runs"]:
            spec = dict(run["spec"])
            spec.setdefault("method", "Euler" if kind == "two_euler" else "RK4")
            if spec["variant"] != "main":
                continue
            if kind == "single":
                if spec["case"] not in ("fig1a", "fig1b"):
                    continue
            elif spec["case"] != "fig3" or (spec["model"] == "SD2") != (kind == "corrected"):
                continue
            selected.append((spec, run, path))
    keys = [tuple(s[k] for k in ("case", "method", "mesh", "model")) for s, _, _ in selected]
    assert len(keys) == len(set(keys)) == 36
    return selected


def main() -> None:
    rows = []
    for path in TABLES:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows.extend(dict(row, source_path=str(path), source_line=line) for line, row in enumerate(csv.DictReader(handle), 2))
    errors, records = {}, []
    largest_history, largest_csv = 0.0, 0.0
    for spec, run, manifest_path in selected_runs():
        path = Path(run["profile"])
        digest = sha(path)
        assert digest == run["profile_sha256"]
        history = next(h for h in run["history"] if abs(h["t"] - TIME) < 1e-12)
        row = next(r for r in rows if r["method"] == spec["method"] and r["case"] == spec["case"] and r["mesh"] == spec["mesh"] and float(r["t"]) == TIME)
        rec = {"spec": spec, "manifest": str(manifest_path), "profile": str(path), "profile_sha256": digest, "hash_verified": True, "csv": {"path": row["source_path"], "line": row["source_line"]}, "fields": {}}
        with np.load(path, allow_pickle=False) as saved:
            x, y = saved["t0.01_x"], saved["y"]
            assert np.array_equal(y, YY)
            assert np.all(np.diff(x) > 0) and x[0] <= XX[0] and x[-1] >= XX[-1]
            assert x.shape == (256,) and spec["nx"] == 256 and spec["dt"] == 0.000125 and spec["h"] == 0.125
            reference = continuous_tau_fields(spec["case"], XX, YY, TIME)
            for field in ("u", "v"):
                native = saved["t0.01_" + field]
                assert native.shape == (24, 256) and np.all(np.isfinite(native))
                sampled = CubicSpline(x, native, axis=-1)(XX)
                signed = sampled - reference[field]
                norm = float(np.max(np.abs(signed)))
                location = np.unravel_index(np.argmax(np.abs(signed)), signed.shape)
                a, b = abs(norm - history["errors"][field]), abs(norm - float(row[spec["model"] + "_" + field]))
                largest_history, largest_csv = max(largest_history, a), max(largest_csv, b)
                assert max(a, b) < 1e-12
                errors[spec["case"], spec["method"], spec["mesh"], spec["model"], field] = norm
                rec["fields"][field] = {"maximum_absolute_error": norm, "history_error": history["errors"][field], "csv_error": float(row[spec["model"] + "_" + field]), "history_abs_difference": a, "csv_abs_difference": b, "signed_error_range": [float(signed.min()), float(signed.max())], "numerical_range": [float(sampled.min()), float(sampled.max())], "maximum_location": {"x": float(XX[location[1]]), "y": float(YY[location[0]]), "signed_error": float(signed[location])}}
        records.append(rec)

    def err(case, method, mesh, model, field):
        return errors[case, method, mesh, model, field]

    page_path = ROOT / "index.html"
    page = BeautifulSoup(page_path.read_text(encoding="utf-8"), "html.parser")
    ratios = []
    for table in page.find_all("table")[2:]:
        for row in table.select("tbody tr"):
            cells = [c.get_text(strip=True).replace("†", "") for c in row.find_all("td")]
            case = CASE_LABELS[cells[0]]
            if table["id"] == "table-3":
                values = [err(case, "RK4", "fixed", model, f) / err(case, "RK4", "fixed", "FD", f) for model in ("SD", "SD2") for f in ("u", "v")]
                shown = cells[1:]
            elif table["id"] == "table-4":
                values = [err(case, "Euler", "fixed", cells[1], f) / err(case, "RK4", "fixed", cells[1], f) for f in ("u", "v")]
                shown = cells[2:]
            else:
                assert table["id"] == "table-5"
                values = [err(case, "RK4", "moving", cells[1], f) / err(case, "RK4", "fixed", cells[1], f) for f in ("u", "v")]
                shown = cells[2:]
            for i, (value, display) in enumerate(zip(values, shown)):
                assert abs(value - float(display)) < 0.001
                ratios.append({"table": table["id"], "case": case, "scheme": "SD/SD2" if table["id"] == "table-3" else cells[1], "numeric_column": i + 1, "actual": value, "shown": display, "correct_rounding": f"{value:.3f}", "rounding_match": f"{value:.3f}" == display})
    plot_path = HERE / "plot_validation.json"
    plot_check = None
    if plot_path.exists():
        plotted = json.loads(plot_path.read_text(encoding="utf-8"))
        independent = {
            tuple(r["spec"][k] for k in ("case", "method", "mesh", "model")) + (field,): (r, value)
            for r in records for field, value in r["fields"].items()
        }
        field_checks = []
        for plotted_field in plotted["records"]:
            key = tuple(plotted_field[k] for k in ("case", "method", "mesh", "model", "field"))
            run_record, field_record = independent[key]
            difference = abs(field_record["maximum_absolute_error"] - plotted_field["full_max"])
            assert difference < 1e-12
            assert plotted_field["profile_sha256"] == run_record["profile_sha256"]
            location = field_record["maximum_location"]
            dx, dy = abs(location["x"] - plotted_field["max_x"]), abs(location["y"] - plotted_field["max_y"])
            assert dx == dy == 0.0, key
            field_checks.append({"case": key[0], "method": key[1], "mesh": key[2], "model": key[3], "field": key[4], "maximum_error_abs_difference": difference, "maximum_x_difference": dx, "maximum_y_difference": dy, "source_profile_hash_match": True})
        assert len(field_checks) == 72
        plot_check = {
            "path": str(plot_path), "sha256": sha(plot_path), "field_count": len(field_checks),
            "maximum_error_abs_difference": max(c["maximum_error_abs_difference"] for c in field_checks),
            "all_error_peak_x_y_match_exactly": True,
            "maximum_x_difference": 0.0, "maximum_y_difference": 0.0,
            "field_checks": field_checks,
        }
    report = {
        "date": "2026-10-01", "new_pde_trajectories": 0,
        "reference_method": "Independent direct positive tau rational derivatives; imports no solver or experiment module.",
        "evaluation": {"time": TIME, "x_interval": [-10.0, 10.0], "x_count": len(XX), "physical_y": YY.tolist(), "interpolation": "SciPy CubicSpline default not-a-knot on saved physical x, axis=-1; no y interpolation", "norm": "sampled maximum absolute error including initial representation error"},
        "summary": {"combinations": len(records), "field_norms": len(errors), "profile_hashes_verified": len(records), "max_abs_error_difference_history": largest_history, "max_abs_error_difference_csv": largest_csv, "index_ratio_cells": len(ratios), "index_ratio_rounding_mismatches": sum(not r["rounding_match"] for r in ratios)},
        "sources": [{"path": str(p), "sha256": sha(p)} for p in [*MANIFESTS.values(), *TABLES, page_path, Path(__file__)]],
        "runs": records, "index_ratios": ratios, "plot_crosscheck": plot_check,
        "notes": ["No Q/R reconstruction is needed: saved physical u/v are the original evaluation fields.", "A/SD2/fixed carries the existing spatial-control limitation; a plotted field does not remove that limitation.", "Use all 4001 x points to compute labels even if rendering is downsampled.", "For a heatmap on 24 y midpoint layers, use cell edges [-1.5,1.5] and avoid claiming sampled error bounds on an interpolated continuous y mesh."]
    }
    destination = HERE / "data_audit.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"output": str(destination), **report["summary"], "rounding_mismatches": [r for r in ratios if not r["rounding_match"]], "plot_crosscheck": {k: v for k, v in plot_check.items() if k != "field_checks"} if plot_check else None}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
