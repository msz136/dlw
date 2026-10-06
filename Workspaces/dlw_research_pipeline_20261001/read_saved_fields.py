"""Re-evaluate existing DLW snapshots; no PDE solver or new trajectory is run.

Writes only paired_fields.json next to this script. Source NPZ files, their
manifest, and historical CSV tables are read without modification.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.interpolate import CubicSpline
from scipy.special import expit


HERE = Path(__file__).resolve().parent
BASE = HERE.parent
SOURCE = BASE / "dlw_single_aligned_20260929" / "out"
TIME = 0.01
FIELDS = ("u", "v")
MODELS = ("SD", "SD2", "FD")
VARIANTS = ("main", "x_half", "y_half")
CASES = {
    "fig1a": {"a": 2.0, "p": 1.0, "q": 2.0},
    "fig1b": {"a": 2.0, "p": 4.0, "q": -3.0},
}
XX = np.linspace(-10.0, 10.0, 4001)
YY = (np.arange(-12, 12) + 0.5) * 0.125


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_record(path: Path) -> dict:
    return {"path": str(path.resolve()), "sha256": sha256(path)}


def table(name: str) -> list[dict]:
    with (SOURCE / name).open(encoding="utf-8-sig", newline="") as handle:
        return [dict(row, source_line=line) for line, row in enumerate(csv.DictReader(handle), 2)]


def reference(case: str, x: np.ndarray, y: np.ndarray, t: float) -> dict[str, np.ndarray]:
    """Continuous zero-phase, c1=1 one-soliton from direct tau derivatives."""
    a, p, q = (CASES[case][k] for k in ("a", "p", "q"))
    S, omega, ell = p + q, q * q - p * p, 1 / (p - a) + 1 / (q + a)
    gamma = -(p - a) / (q + a)
    zeta = S * x[None, :] + omega * t + ell * y[:, None] - np.log(S)
    sf, sg = expit(zeta + np.log(gamma)), expit(zeta)
    return {
        "u": 2 * S * (sf - sg),
        "v": 2 * S * ell * (sf * (1 - sf) + sg * (1 - sg)),
    }


def direct_tau_reference(case: str) -> dict[str, np.ndarray]:
    a, p, q = (CASES[case][k] for k in ("a", "p", "q"))
    S, omega, ell = p + q, q * q - p * p, 1 / (p - a) + 1 / (q + a)
    gamma = -(p - a) / (q + a)
    E = np.exp(S * XX[None, :] + omega * TIME + ell * YY[:, None]) / S
    F, G = 1 + gamma * E, 1 + E
    return {
        "u": 2 * S * (gamma * E / F - E / G),
        "v": 2 * S * ell * (gamma * E / F**2 + E / G**2),
    }


def infinity(array: np.ndarray) -> float:
    return float(np.max(np.abs(array)))


def main() -> None:
    manifest_path = SOURCE / "results.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    comparison, controls, fine_time = (table(name) for name in (
        "comparison.csv", "control_comparisons.csv", "fine_time_checks.csv"
    ))
    sources = [source_record(path) for path in (
        manifest_path, SOURCE / "comparison.csv", SOURCE / "control_comparisons.csv",
        SOURCE / "fine_time_checks.csv", BASE / "dlw_single_aligned_20260929" / "audit.py",
        BASE / "dlw_paper_cases_20260927" / "run.py", Path(__file__),
    )]
    result = {
        "date": "2026-10-01",
        "role": "内部历史审查；不以这些后验排名或小幅差距作为研究立题。后续研究应理论先行、先给预测，最后验证；优化收益至少达到数量级才值得研究。",
        "scope": "旧轨道重处理：只读取既有 NPZ 与历史表格，无新 PDE 演化，无参数优化。",
        "runtime": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "evaluation": {
            "t": TIME, "x_interval": [-10.0, 10.0], "x_count": 4001,
            "common_y": YY.tolist(), "norm": "sampled maximum absolute value",
            "interpolation": "SciPy CubicSpline default not-a-knot in x; fine y additionally interpolated to the same 24 main-grid y layers",
            "physical_name_mapping": {"SD2": "SDR"},
        },
        "analytic_formula": {
            "definitions": "S=p+q; omega=q^2-p^2; ell=1/(p-a)+1/(q+a); gamma=-(p-a)/(q+a); zeta=S*x+omega*t+ell*y-log(S)",
            "u": "2*S*(sigmoid(zeta+log(gamma))-sigmoid(zeta))",
            "v": "2*S*ell*(sf*(1-sf)+sg*(1-sg)); sf=sigmoid(zeta+log(gamma)); sg=sigmoid(zeta)",
            "fig1a": "zeta=3*x+3*t-3*y/4-log(3); gamma=1/4; u=6*(sf-sg); v=-4.5*(sf*(1-sf)+sg*(1-sg))",
            "fig1b": "zeta=x-7*t-y/2; gamma=2; u=2*(sf-sg); v=-(sf*(1-sf)+sg*(1-sg))",
            "source": str(BASE / "dlw_paper_cases_20260927" / "run.py"),
            "source_lines": [71, 80],
            "check": "Sigmoid evaluation checked against direct rational tau derivatives and historical stored error norms; this is an implementation cross-check, not a new PDE proof.",
        },
        "sources": sources,
        "cases": {},
        "limitations": [
            "Only two x resolutions and two y resolutions are present; near-16 reduction is evidence consistent with k^4, not an asymptotic-order proof.",
            "Differences of error norms are not norms of differences of physical fields; both quantities are recorded separately.",
            "The x_half trajectory also halves dt. Existing separate time controls are recorded, but this is not a newly run strict single-factor trajectory.",
            "The y_half native-grid historical errors use 48 y layers. Common-y errors here instead use the same 24 main layers after cubic interpolation.",
            "Common-point errors still contain interpolation error and initial representation error. No initial error is subtracted.",
            "Observed ranking changes and near-k^4 field differences do not identify interior product defects, boundary defects, lifting, or reconstruction as a unique cause.",
            "All comparisons are fixed-grid RK4 at T=0.01 in the named cases. They do not certify long-time behavior or independent transfer to an unseen spectral family.",
            "Historical pass thresholds scale with the initial field peak; they do not certify a method ranking or a mathematical error bound.",
        ],
    }
    maximum_csv_difference = 0.0
    maximum_history_difference = 0.0
    profiles_checked = 0
    for case, parameters in CASES.items():
        exact = reference(case, XX, YY, TIME)
        tau = direct_tau_reference(case)
        formula_check = {f: infinity(exact[f] - tau[f]) for f in FIELDS}
        assert max(formula_check.values()) < 1e-12
        entry = {"parameters": dict(parameters, c1=1.0, phase=0.0), "formula_check_max_abs_difference": formula_check, "runs": {}, "variants": {}}
        common_fields = {}
        for variant in VARIANTS:
            entry["runs"][variant] = {}
            for model in MODELS:
                filters = dict(method="RK4", case=case, mesh="fixed", variant=variant, model=model)
                matches = [r for r in manifest["runs"] if all(r["spec"][k] == v for k, v in filters.items())]
                assert len(matches) == 1, filters
                run = matches[0]
                profile = Path(run["profile"])
                profile_source = source_record(profile)
                assert profile_source["sha256"] == run["profile_sha256"], profile
                profiles_checked += 1
                history = next(h for h in run["history"] if abs(h["t"] - TIME) < 1e-12)
                with np.load(profile, allow_pickle=False) as saved:
                    x, y = saved["t0.01_x"], saved["y"]
                    assert np.all(np.diff(x) > 0) and x[0] <= XX[0] and x[-1] >= XX[-1]
                    native_exact = reference(case, XX, y, TIME)
                    native_error, fields = {}, {}
                    for field in FIELDS:
                        sampled = CubicSpline(x, saved["t0.01_" + field], axis=-1)(XX)
                        native_error[field] = infinity(sampled - native_exact[field])
                        if not np.array_equal(y, YY):
                            assert y.min() <= YY.min() and y.max() >= YY.max()
                            sampled = CubicSpline(y, sampled, axis=0)(YY)
                        fields[field] = sampled
                common_fields[variant, model] = fields
                common_error = {f: infinity(fields[f] - exact[f]) for f in FIELDS}
                stored_errors = history["errors"]
                history_diff = max(abs(native_error[f] - stored_errors[f]) for f in FIELDS)
                maximum_history_difference = max(maximum_history_difference, history_diff)
                if variant == "main":
                    row = next(r for r in comparison if r["method"] == "RK4" and r["case"] == case and r["mesh"] == "fixed" and float(r["t"]) == TIME)
                    csv_error = {f: float(row[model + "_" + f]) for f in FIELDS}
                    csv_evidence = {"file": str(SOURCE / "comparison.csv"), "lines": [row["source_line"]]}
                else:
                    rows = [r for r in controls if all(r[k] == v for k, v in filters.items()) and float(r["t"]) == TIME]
                    assert len(rows) == 2
                    csv_error = {r["field"]: float(r["control_error"]) for r in rows}
                    csv_evidence = {"file": str(SOURCE / "control_comparisons.csv"), "lines": [r["source_line"] for r in rows]}
                csv_diff = max(abs(native_error[f] - csv_error[f]) for f in FIELDS)
                maximum_csv_difference = max(maximum_csv_difference, csv_diff)
                assert max(csv_diff, history_diff) < 1e-12
                entry["runs"][variant][model] = {
                    "spec": run["spec"], "profile": profile_source,
                    "manifest_profile_sha256_verified": True,
                    "native_y_count": int(len(y)), "native_y_error": native_error,
                    "common_y_error": common_error,
                    "stored_native_error": stored_errors,
                    "stored_history_max_abs_difference": history_diff,
                    "csv_native_error": csv_error, "csv_evidence": csv_evidence,
                    "csv_max_abs_difference": csv_diff,
                }
            errors = {m: entry["runs"][variant][m]["common_y_error"] for m in MODELS}
            entry["variants"][variant] = {
                "SDR_minus_SD_field_norm": {f: infinity(common_fields[variant, "SD2"][f] - common_fields[variant, "SD"][f]) for f in FIELDS},
                "SDR_error_norm_minus_SD_error_norm": {f: errors["SD2"][f] - errors["SD"][f] for f in FIELDS},
                "SD_over_FD_common_error_ratio": {f: errors["SD"][f] / errors["FD"][f] for f in FIELDS},
                "SD_error_norm_minus_FD_error_norm": {f: errors["SD"][f] - errors["FD"][f] for f in FIELDS},
            }
        gaps = {v: entry["variants"][v]["SDR_minus_SD_field_norm"] for v in VARIANTS}
        entry["SDR_SD_x_refinement_reduction_factor"] = {f: gaps["main"][f] / gaps["x_half"][f] for f in FIELDS}
        entry["SDR_SD_y_half_over_main_field_difference"] = {f: gaps["y_half"][f] / gaps["main"][f] for f in FIELDS}
        entry["existing_time_control_evidence"] = {
            "main": [r for r in controls if r["method"] == "RK4" and r["case"] == case and r["mesh"] == "fixed" and r["variant"] == "time_half" and float(r["t"]) == TIME],
            "x_half": [r for r in fine_time if r["method"] == "RK4" and r["case"] == case and r["mesh"] == "fixed" and float(r["t"]) == TIME],
        }
        result["cases"][case] = entry
    result["validation"] = {
        "profile_count": profiles_checked, "all_profile_hashes_match_manifest": True,
        "native_error_max_abs_difference_from_csv": maximum_csv_difference,
        "native_error_max_abs_difference_from_saved_history": maximum_history_difference,
        "new_pde_trajectories": 0,
    }
    destination = HERE / "paired_fields.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(destination), "validation": result["validation"], "summary": {
        c: {"x_reduction": v["SDR_SD_x_refinement_reduction_factor"], "y_difference_ratio": v["SDR_SD_y_half_over_main_field_difference"],
            "SD_over_FD_u": {k: vv["SD_over_FD_common_error_ratio"]["u"] for k, vv in v["variants"].items()}}
        for c, v in result["cases"].items()
    }}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
