"""Predefined paired validation of the complete Rm ALE scheme against fixed grid.

Stages: develop -> freeze -> confirm -> summarize. Confirmation cases are
generated only after development checks pass, and each p is one statistical unit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import beta, binom, binomtest

from run_mesh_comparison import initial_grid, reference, run
from hs_exact import Soliton

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "statistical_validation"
OUT.mkdir(parents=True, exist_ok=True)

DEV_P = (3., 5., 8., 12.)
TIMES = (.1, .25, .5)
CONFIG = dict(n=400, dt=.0005, final_time=.5, halfwidth=4.,
              sample_times=TIMES, n_eval=4001)
SEED = 20260925
SAMPLE_SIZE = 60
MIN_P, MAX_P = 3., 12.
MIN_GAIN = .10
TARGET_PROBABILITY = .80
ALPHA = .05
RELIABILITY_FLOOR = 1e-10


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path: Path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def loaded(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def stripped(result):
    for key in ("final_mesh", "final_u", "final_rho"):
        result.pop(key)
    return result


def run_record(p, mode, config):
    try:
        result = stripped(run(p, mode, **config))
        if (result["path_min_h"] <= 0 or result["path_min_rho"] <= 0
                or result["path_min_Rm"] <= 0):
            raise FloatingPointError("nonpositive accepted-state spacing or density")
        return dict(status="ok", result=result)
    except Exception as exc:
        return dict(status="failed", error=f"{type(exc).__name__}: {exc}")


def exact_reference_check():
    x = np.linspace(-4, 4, 8001)
    worst_field = 0.
    worst_x = 0.
    for p in DEV_P:
        sol = Soliton((p,), shift=-(1 - 2 / p) / 2)
        for t in (0., *TIMES):
            u, rho, _, _ = reference(sol, x, t)
            u_old, rho_old, X_old = sol.continuous_x(x, t)
            worst_field = max(worst_field, float(np.max(np.abs(u-u_old))),
                              float(np.max(np.abs(rho-rho_old))))
            _, mapped, _ = sol.continuous_X(X_old, t)
            worst_x = max(worst_x, float(np.max(np.abs(mapped-x))))
    assert worst_field < 1e-11 and worst_x < 1e-11
    return dict(max_field_difference=worst_field, max_hodograph_roundtrip=worst_x)


def dev_specs():
    specs = []
    for p in DEV_P:
        for mode in ("fixed", "rm"):
            sol = Soliton((p,), shift=-(1 - 2 / p) / 2)
            core = initial_grid(sol, mode, 400, 4.)
            extended_x = np.r_[np.linspace(-5., -4., 51)[:-1], core,
                               np.linspace(4., 5., 51)[1:]]
            variants = {
                "base": {},
                "half_dt": {"dt": .00025},
                "double_eval": {"n_eval": 8001},
                "half_n": {"n": 200},
                "double_n": {"n": 800},
                "wide_domain": {"n": 500, "halfwidth": 5., "eval_halfwidth": 4.,
                                "initial_x": extended_x.tolist()},
            }
            for name, changes in variants.items():
                config = dict(CONFIG)
                config.update(changes)
                specs.append(dict(id=f"p{p:g}_{mode}_{name}", p=p, mode=mode,
                                  variant=name, config=config))
    return specs


def develop():
    path = OUT / "development.json"
    saved = loaded(path) or dict(reference=exact_reference_check(), runs={})
    if "reference" not in saved:
        saved["reference"] = exact_reference_check()
    for spec in dev_specs():
        if (spec["id"] in saved["runs"] and
                json.dumps(saved["runs"][spec["id"]]["spec"], sort_keys=True)
                == json.dumps(spec, sort_keys=True)):
            continue
        record = run_record(spec["p"], spec["mode"], spec["config"])
        saved["runs"][spec["id"]] = dict(spec=spec, **record)
        dump(path, saved)
        msg = "ok" if record["status"] == "ok" else record["error"]
        print(f"DEV {len(saved['runs']):02d}/48 {spec['id']}: {msg}", flush=True)
    audit = audit_development(saved)
    dump(OUT / "development_audit.json", audit)
    print(json.dumps(audit, indent=2), flush=True)


def audit_development(saved):
    checks = dict(reference=saved.get("reference"))
    records = saved["runs"]
    checks["complete"] = len(records) == 48
    checks["failures"] = [k for k, v in records.items() if v["status"] != "ok"]
    if not checks["complete"] or checks["failures"]:
        checks["pass"] = False
        return checks
    worst = dict(half_dt=0., double_eval=0., wide_domain=0.)
    domain_ratio_change = 0.
    domain_decisions = []
    orders = []
    minimum_errors = []
    for p in DEV_P:
        base_fixed = records[f"p{p:g}_fixed_base"]["result"]["snapshots"]
        base_rm = records[f"p{p:g}_rm_base"]["result"]["snapshots"]
        wide_fixed = records[f"p{p:g}_fixed_wide_domain"]["result"]["snapshots"]
        wide_rm = records[f"p{p:g}_rm_wide_domain"]["result"]["snapshots"]
        base_ratios = [r["full"][field]/f["full"][field]
                       for f, r in zip(base_fixed, base_rm)
                       for field in ("u_linf", "rho_linf")]
        wide_ratios = [r["full"][field]/f["full"][field]
                       for f, r in zip(wide_fixed, wide_rm)
                       for field in ("u_linf", "rho_linf")]
        domain_ratio_change = max(domain_ratio_change,
                                  max(abs(a-b) for a,b in zip(base_ratios, wide_ratios)))
        domain_decisions.append(dict(p=p, base_max_ratio=max(base_ratios),
                                     wide_max_ratio=max(wide_ratios),
                                     same_success_decision=(max(base_ratios) <= .9)
                                     == (max(wide_ratios) <= .9)))
        for mode in ("fixed", "rm"):
            prefix = f"p{p:g}_{mode}_"
            base = records[prefix + "base"]["result"]["snapshots"]
            for name in worst:
                other = records[prefix + name]["result"]["snapshots"]
                for b, o in zip(base, other):
                    for field in ("u_linf", "rho_linf"):
                        eb, eo = b["full"][field], o["full"][field]
                        worst[name] = max(worst[name], abs(eo-eb)/eb)
            coarse = records[prefix + "half_n"]["result"]["snapshots"]
            fine = records[prefix + "double_n"]["result"]["snapshots"]
            for a, b, c in zip(coarse, base, fine):
                for field in ("u_linf", "rho_linf"):
                    minimum_errors.extend([a["full"][field], b["full"][field],
                                           c["full"][field]])
                    orders.append(dict(p=p, mode=mode, time=b["time"], field=field,
                                       coarse_to_base=math.log2(a["full"][field]/b["full"][field]),
                                       base_to_fine=math.log2(b["full"][field]/c["full"][field])))
    checks["worst_relative_error_change"] = worst
    checks["domain_max_absolute_ratio_change"] = domain_ratio_change
    checks["domain_decisions"] = domain_decisions
    checks["observed_spatial_order_range"] = [min(min(o["coarse_to_base"],o["base_to_fine"]) for o in orders),
                                               max(max(o["coarse_to_base"],o["base_to_fine"]) for o in orders)]
    checks["minimum_error"] = min(minimum_errors)
    checks["orders"] = orders
    checks["pass"] = (worst["half_dt"] < .01 and worst["double_eval"] < .01
                      and all(item["same_success_decision"] for item in domain_decisions)
                      and min(minimum_errors) > RELIABILITY_FLOOR
                      and all(1.7 < o[key] < 2.3 for o in orders
                              for key in ("coarse_to_base", "base_to_fine")))
    return checks


def freeze():
    audit = loaded(OUT / "development_audit.json")
    if audit is None or not audit["pass"]:
        raise RuntimeError("Development checks did not pass; confirmation sample not generated")
    path = OUT / "frozen_manifest.json"
    current_hashes = {name: sha256(HERE / name) for name in ("run_mesh_comparison.py",)}
    current_hashes["hs_exact.py"] = sha256(HERE.parent / "hs_numerics_plan" / "hs_exact.py")
    if path.exists():
        manifest = loaded(path)
        if manifest["solver_hashes"] != current_hashes:
            raise RuntimeError("Frozen solver source hash changed")
        return manifest
    ps = np.random.default_rng(SEED).uniform(MIN_P, MAX_P, SAMPLE_SIZE)
    manifest = dict(config=CONFIG, solver_hashes=current_hashes, seed=SEED,
                    population="independent uniform p in [3,12]; centered smooth one-soliton; c=1",
                    p=[float(v) for v in ps], primary=dict(
                        times=TIMES, fields=("u_linf", "rho_linf"),
                        max_error_ratio=1-MIN_GAIN, target_probability=TARGET_PROBABILITY,
                        alpha=ALPHA, test="one-sided exact binomial", n=SAMPLE_SIZE,
                        required_successes=54, reliability_floor=RELIABILITY_FLOOR),
                    bootstrap=dict(seed=20260926, replicates=10000))
    dump(path, manifest)
    print("FROZEN 60 independent p values and solver hashes", flush=True)
    return manifest


def confirm():
    manifest = freeze()
    path = OUT / "confirmation.json"
    saved = loaded(path) or dict(cases=[])
    cases = saved["cases"]
    for index, p in enumerate(manifest["p"]):
        if index < len(cases):
            if cases[index]["index"] != index or cases[index]["p"] != p:
                raise RuntimeError("Saved case order differs from frozen manifest")
            continue
        pair = dict(index=index, p=p, fixed=run_record(p, "fixed", manifest["config"]),
                    rm=run_record(p, "rm", manifest["config"]))
        cases.append(pair)
        dump(path, saved)
        print(f"CONFIRM {index+1:02d}/60 p={p:.6f} "
              f"fixed={pair['fixed']['status']} rm={pair['rm']['status']}", flush=True)


def summarize():
    manifest = freeze()
    saved = loaded(OUT / "confirmation.json")
    if saved is None or len(saved["cases"]) != SAMPLE_SIZE:
        raise RuntimeError("Confirmation is incomplete")
    cases = []
    success_count = 0
    failure_counts = dict(fixed=0, rm=0, both=0)
    valid_E_ratios = []
    p_valid = []
    for raw in saved["cases"]:
        fixed, rm = raw["fixed"], raw["rm"]
        if fixed["status"] != "ok" or rm["status"] != "ok":
            if fixed["status"] != "ok": failure_counts["fixed"] += 1
            if rm["status"] != "ok": failure_counts["rm"] += 1
            if fixed["status"] != "ok" and rm["status"] != "ok": failure_counts["both"] += 1
            cases.append(dict(index=raw["index"], p=raw["p"], success=False,
                              status="failed_solver", fixed=fixed["status"], rm=rm["status"]))
            continue
        fs, rs = fixed["result"]["snapshots"], rm["result"]["snapshots"]
        ratios = {field: [r["full"][field]/f["full"][field] if f["full"][field] > RELIABILITY_FLOOR
                          and r["full"][field] > RELIABILITY_FLOOR else None
                          for f, r in zip(fs, rs)] for field in ("u_linf", "rho_linf")}
        reliable = all(value is not None and math.isfinite(value)
                       for values in ratios.values() for value in values)
        success = bool(reliable and all(value <= 1-MIN_GAIN
                                        for values in ratios.values() for value in values))
        success_count += int(success)
        s = 1-2/raw["p"]
        amplitudes = {"u_linf": s*s/4, "rho_linf": s*s}
        E_fixed = max(f["full"][field]/amplitudes[field]
                      for f in fs for field in amplitudes)
        E_rm = max(r["full"][field]/amplitudes[field]
                   for r in rs for field in amplitudes)
        E_ratio = E_rm/E_fixed if reliable else None
        if reliable:
            valid_E_ratios.append(E_ratio)
            p_valid.append(raw["p"])
        cases.append(dict(index=raw["index"], p=raw["p"], status="ok" if reliable else "unreliable_error",
                          success=success, ratios=ratios,
                          max_u_ratio=max(ratios["u_linf"]) if reliable else None,
                          max_rho_ratio=max(ratios["rho_linf"]) if reliable else None,
                          max_all_ratio=max(v for vs in ratios.values() for v in vs) if reliable else None,
                          E_ratio=E_ratio,
                          path_min_h=rm["result"]["path_min_h"],
                          path_min_rho=rm["result"]["path_min_rho"],
                          path_min_Rm=rm["result"]["path_min_Rm"]))
    k, n = success_count, SAMPLE_SIZE
    pvalue = float(binomtest(k, n, TARGET_PROBABILITY, alternative="greater").pvalue)
    lower = float(beta.ppf(ALPHA, k, n-k+1)) if k else 0.
    upper_two_sided = float(beta.ppf(1-ALPHA/2, k+1, n-k)) if k < n else 1.
    lower_two_sided = float(beta.ppf(ALPHA/2, k, n-k+1)) if k else 0.
    ratio_summary = None
    if valid_E_ratios:
        values = np.asarray(valid_E_ratios)
        rng = np.random.default_rng(manifest["bootstrap"]["seed"])
        index = rng.integers(0,len(values),size=(10000,len(values)))
        boot = np.exp(np.mean(np.log(values[index]),axis=1))
        ratio_summary = dict(n_valid=len(values), geometric_mean=float(np.exp(np.mean(np.log(values)))),
                             bootstrap_ci95=[float(v) for v in np.quantile(boot,[.025,.975])],
                             median=float(np.median(values)), quantile90=float(np.quantile(values,.9)),
                             worst=float(np.max(values)))
    completed = [case for case in cases if case["status"] == "ok"]
    modest = [case for case in completed if .9 < case["max_all_ratio"] < 1.]
    worse = [case for case in completed if case["max_all_ratio"] >= 1.]
    improving = k + len(modest)
    improving_ci = binomtest(improving, n).proportion_ci(.95, method="exact")
    worse_ci = binomtest(len(worse), n).proportion_ci(.95, method="exact")
    directional = dict(strong_improvement=k, modest_improvement=len(modest),
                       no_improvement_or_worse=len(worse),
                       all_six_strictly_improve=improving,
                       all_six_improve_cp95=[improving_ci.low, improving_ci.high],
                       no_improvement_or_worse_cp95=[worse_ci.low, worse_ci.high],
                       modest_worst_ratio_range=[min(c["max_all_ratio"] for c in modest),
                                                 max(c["max_all_ratio"] for c in modest)],
                       worse_worst_ratio_range=[min(c["max_all_ratio"] for c in worse),
                                                max(c["max_all_ratio"] for c in worse)],
                       worse_p_range=[min(c["p"] for c in worse),max(c["p"] for c in worse)])
    summary = dict(n=n, successes=k, success_fraction=k/n,
                   main_pvalue=pvalue, one_sided_lower95=lower,
                   two_sided_cp95=[lower_two_sided,upper_two_sided],
                   supports_probability_above_0_8=bool(pvalue<ALPHA),
                   failure_counts=failure_counts, E_ratio=ratio_summary,
                   directional_breakdown=directional,
                   cases=cases)
    dump(OUT / "summary.json", summary)
    print(f"RESULT {k}/{n} successes; one-sided p={pvalue:.6g}; "
          f"one-sided lower 95%={lower:.4f}", flush=True)
    print(f"E ratio: {ratio_summary}", flush=True)


def sensitivity():
    """Read-only to the frozen main result: rerun its cases under two numerical controls."""
    manifest = freeze()
    path = OUT / "sensitivity.json"
    saved = loaded(path) or dict(runs={})
    for index, p in enumerate(manifest["p"]):
        for variant in ("double_eval", "wide_domain"):
            for mode in ("fixed", "rm"):
                key = f"case{index:02d}_{variant}_{mode}"
                if key in saved["runs"]:
                    continue
                config = dict(manifest["config"])
                if variant == "double_eval":
                    config["n_eval"] = 8001
                else:
                    sol = Soliton((p,), shift=-(1 - 2 / p) / 2)
                    core = initial_grid(sol, mode, 400, 4.)
                    config.update(n=500, halfwidth=5., eval_halfwidth=4.,
                                  initial_x=np.r_[np.linspace(-5., -4., 51)[:-1], core,
                                                  np.linspace(4., 5., 51)[1:]].tolist())
                saved["runs"][key] = dict(index=index, p=p, variant=variant,
                                           mode=mode, record=run_record(p, mode, config))
                dump(path, saved)
            print(f"SENSITIVITY {index+1:02d}/60 {variant} complete", flush=True)
    main = loaded(OUT / "summary.json")
    assert main is not None and len(main["cases"]) == SAMPLE_SIZE
    out = {}
    for variant in ("double_eval", "wide_domain"):
        count = 0
        field_counts = {"u_linf": 0, "rho_linf": 0}
        changed = []
        worst_ratio_change = 0.
        failures = []
        for index, original in enumerate(main["cases"]):
            fixed = saved["runs"][f"case{index:02d}_{variant}_fixed"]["record"]
            rm = saved["runs"][f"case{index:02d}_{variant}_rm"]["record"]
            if fixed["status"] != "ok" or rm["status"] != "ok":
                failures.append(index)
                continue
            ratios = [r["full"][field]/f["full"][field]
                      for f, r in zip(fixed["result"]["snapshots"], rm["result"]["snapshots"])
                      for field in ("u_linf", "rho_linf")]
            for field in field_counts:
                field_counts[field] += int(all(
                    r["full"][field]/f["full"][field] <= .9
                    for f, r in zip(fixed["result"]["snapshots"], rm["result"]["snapshots"])))
            success = max(ratios) <= .9
            count += int(success)
            if success != original["success"]:
                changed.append(index)
            original_ratios = [original["ratios"][field][i]
                               for i in range(3) for field in ("u_linf", "rho_linf")]
            worst_ratio_change = max(worst_ratio_change,
                                     max(abs(a-b) for a,b in zip(ratios, original_ratios)))
        out[variant] = dict(successes=count, field_successes=field_counts,
                            changed_case_indices=changed,
                            solver_failures=failures,
                            max_absolute_component_ratio_change=worst_ratio_change)
    dump(OUT / "sensitivity_audit.json", out)
    print(json.dumps(out, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("develop", "freeze", "confirm", "summarize", "sensitivity"))
    args = parser.parse_args()
    globals()[args.stage]()


if __name__ == "__main__":
    main()
