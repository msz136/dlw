"""New independent p cohort for transfer across four time integrators."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import beta, binomtest

from run_time_methods import METHODS, ROUTES, run_one

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "time_methods"
OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = OUT / "cohort_manifest.json"
RECORDS = OUT / "cohort_records.json"
SUMMARY = OUT / "cohort_summary.json"
SEED = 20260926
N_CASES = 60
N = 200
DT = .0125
T = .5
TIMES = (.25, .5)
CORE = np.linspace(-2., 2., 2001)


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def main():
    manifest = load(MANIFEST)
    if manifest is None:
        manifest = {"status":"frozen_before_runs", "seed":SEED,
                    "p":np.random.default_rng(SEED).uniform(3.,12.,N_CASES).tolist(),
                    "n":N,"dt":DT,"T":T,"times":TIMES,"core":[-2.,2.],
                    "methods":METHODS,"routes":ROUTES,
                    "predefined_event":"rho B/A <= 0.9 at both times for every method",
                    "solver_sha256":{
                        name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
                        for name in ("run_time_methods.py","run_mesh_comparison.py")}}
        dump(MANIFEST,manifest)
    for name, expected in manifest["solver_sha256"].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Frozen solver changed: {name}")
    saved = load(RECORDS) or {"manifest":"cohort_manifest.json", "rows":{}}
    total = N_CASES*len(ROUTES)*len(METHODS)
    for i,p in enumerate(manifest["p"]):
        for route in ROUTES:
            for method in METHODS:
                key = f"{i:02d}_{route}_{method}"
                if key in saved["rows"]:
                    continue
                try:
                    result = run_one(p,route,method,DT,N,T,4.,TIMES,CORE)
                except Exception as exc:
                    result = {"status":"failed","error":f"{type(exc).__name__}: {exc}"}
                saved["rows"][key] = {"index":i,"p":p,"route":route,"method":method,**result}
                dump(RECORDS,saved)
                print(f"{len(saved['rows'])}/{total} {key} {result['status']}",flush=True)
    cases = []
    for i,p in enumerate(manifest["p"]):
        ratios = {}
        failures = []
        for method in METHODS:
            fixed = saved["rows"][f"{i:02d}_difference_fixed_{method}"]
            moving = saved["rows"][f"{i:02d}_difference_rm_{method}"]
            for route in ROUTES:
                row = saved["rows"][f"{i:02d}_{route}_{method}"]
                if row["status"] != "completed":
                    failures.append(f"{route}_{method}")
            if fixed["status"] == moving["status"] == "completed":
                ratios[method] = {
                    field:[moving["snapshots"][str(t)][field]/fixed["snapshots"][str(t)][field]
                           for t in TIMES]
                    for field in ("u_linf","rho_linf")}
        success = (not failures and len(ratios)==len(METHODS) and
                   all(value <= .9 for method in METHODS
                       for value in ratios[method]["rho_linf"]))
        cases.append({"index":i,"p":p,"success_rho_all_methods":success,
                      "ratios":ratios,"failures":failures})
    k = sum(c["success_rho_all_methods"] for c in cases)
    summary = {"n":N_CASES,"successes_rho_all_methods":k,
               "fraction":k/N_CASES,
               "one_sided_cp_lower95":float(beta.ppf(.05,k,N_CASES-k+1)) if k else 0.,
               "one_sided_pvalue_vs_0_8":float(binomtest(k,N_CASES,.8,alternative="greater").pvalue),
               "cases":cases}
    dump(SUMMARY,summary)
    print("summary",k,"/",N_CASES,"p=",summary["one_sided_pvalue_vs_0_8"],flush=True)


if __name__ == "__main__":
    main()
