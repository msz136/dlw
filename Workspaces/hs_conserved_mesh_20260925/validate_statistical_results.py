"""Independent readback of frozen paired cases and statistical endpoints."""
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import beta, binom, binomtest

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "statistical_validation"
read = lambda name: json.loads((OUT / name).read_text(encoding="utf-8"))
manifest = read("frozen_manifest.json")
dev = read("development.json")
dev_audit = read("development_audit.json")
confirmation = read("confirmation.json")["cases"]
summary = read("summary.json")
sensitivity = read("sensitivity.json")["runs"]
sensitivity_audit = read("sensitivity_audit.json")

assert len(dev["runs"]) == 48 and dev_audit["pass"]
assert len(manifest["p"]) == len(confirmation) == len(summary["cases"]) == 60
assert len(set(manifest["p"])) == 60
assert all(3 <= p <= 12 for p in manifest["p"])
for name, digest in manifest["solver_hashes"].items():
    path = HERE / name if name != "hs_exact.py" else HERE.parent / "hs_numerics_plan" / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest

success = 0
rho_success = 0
all_E = []
for index, row in enumerate(confirmation):
    assert row["index"] == index and row["p"] == manifest["p"][index]
    assert row["fixed"]["status"] == row["rm"]["status"] == "ok"
    a, b = row["fixed"]["result"], row["rm"]["result"]
    assert [s["time"] for s in a["snapshots"]] == [s["time"] for s in b["snapshots"]] == [.1,.25,.5]
    assert b["path_min_h"] > 0 and b["path_min_rho"] > 0 and b["path_min_Rm"] > 0
    ratios = {field: [bs["full"][field]/as_["full"][field]
                      for as_, bs in zip(a["snapshots"], b["snapshots"])]
              for field in ("u_linf", "rho_linf")}
    assert all(np.all(np.isclose(ratios[field],summary["cases"][index]["ratios"][field],rtol=1e-12))
               for field in ratios)
    joint = all(value <= .9 for values in ratios.values() for value in values)
    rho_only = all(value <= .9 for value in ratios["rho_linf"])
    success += int(joint)
    rho_success += int(rho_only)
    assert joint == summary["cases"][index]["success"]
    all_E.append(summary["cases"][index]["E_ratio"])

assert success == summary["successes"] == 43
assert rho_success == 60
assert summary["directional_breakdown"]["strong_improvement"] == 43
assert summary["directional_breakdown"]["modest_improvement"] == 9
assert summary["directional_breakdown"]["no_improvement_or_worse"] == 8
assert summary["directional_breakdown"]["all_six_strictly_improve"] == 52
assert len(sensitivity) == 60 * 2 * 2
assert all(e < 1 for e in all_E)
assert np.isclose(np.exp(np.mean(np.log(all_E))), summary["E_ratio"]["geometric_mean"])
assert np.isclose(summary["main_pvalue"],binomtest(43,60,.8,alternative="greater").pvalue)
assert np.isclose(summary["one_sided_lower95"],beta.ppf(.05,43,18))
assert binom.sf(53,60,.8) < .05 and binom.sf(52,60,.8) >= .05
assert all(sensitivity_audit[v]["successes"] == 43 and
           sensitivity_audit[v]["field_successes"]["rho_linf"] == 60 and
           sensitivity_audit[v]["changed_case_indices"] == []
           for v in ("double_eval", "wide_domain"))

record = dict(status="passed", development_trajectories=48,
              confirmation_trajectories=120, sensitivity_trajectories=240,
              independent_parameter_cases=60, joint_successes=43,
              all_six_improve_but_under_10_percent=9,
              late_u_worsening_cases=8,
              rho_only_successes=60, exact_main_pvalue=summary["main_pvalue"],
              frozen_solver_hashes_match=True,
              sensitivity_classifications_unchanged=True)
(OUT / "readback_validation.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
print(json.dumps(record,indent=2))
