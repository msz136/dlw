"""Independently check the tau derivatives used for the FD boundary."""
from hashlib import sha256
import json
from pathlib import Path

import numpy as np

from hs_two_soliton_cells import TWO_REFERENCE

HERE = Path(__file__).resolve().parent
namespace = {"np": np}
exec(TWO_REFERENCE, namespace)
exact = namespace["hs_two_exact_X"]
physical = namespace["hs_two_exact_physical"]
beta = np.array([0, 1.1-11, 1.25-5, 1.1-11+1.25-5])[:, None]
omega = np.array([0, 1/1.1-1/11, 1/1.25-1/5,
                  1/1.1-1/11+1/1.25-1/5])[:, None]
phase = np.array([0, np.log(6.5), np.log(6.5),
                  2*np.log(6.5)+np.log(12/507)])[:, None]


def independent(X, t):
    weights = np.exp(beta*X+omega*t+phase)
    weights /= weights.sum(axis=0)
    mean = (weights*omega).sum(axis=0)
    mean2 = (weights*omega**2).sum(axis=0)
    b, b2 = (weights*beta).sum(axis=0), (weights*beta**2).sum(axis=0)
    ob, ob2 = (weights*omega*beta).sum(axis=0), (weights*omega*beta**2).sum(axis=0)
    o2b = (weights*omega**2*beta).sum(axis=0)
    o2b2 = (weights*omega**2*beta**2).sum(axis=0)
    mean_x = ob-mean*b
    mean_xx = ob2-2*ob*b-mean*b2+2*mean*b*b
    uX = o2b-mean2*b-2*mean*mean_x
    uXX = o2b2-2*o2b*b-mean2*b2+2*mean2*b*b-2*mean_x**2-2*mean*mean_xx
    J = 1-mean_x
    return dict(x=X-mean-1/11-1/5, u=mean2-mean**2, rho=1/J,
                m=2+uXX/J**2+uX*mean_xx/J**3)


differences, finite_differences, jacobians, inverse_errors = [], [], [], []
for t in (0, 0.25, 0.5):
    X = np.linspace(-4, 4, 1601)
    current, reference = exact(X, t), independent(X, t)
    diff = {k: float(np.max(np.abs(current[k]-reference[k]))) for k in reference}
    assert max(diff.values()) < 1e-12, diff
    differences.append({"t": t, "max_difference": diff})
    jacobians.append(float(current["J"].min()))
    assert jacobians[-1] > 0 and np.all(np.diff(current["x"]) > 0)
    x = np.linspace(-1, 1, 401)
    inv = physical(x, t)
    inverse_errors.append(float(np.max(np.abs(inv["x"]-x))))
    assert inverse_errors[-1] < 2e-12
    sample = np.linspace(-1, 1, 41)
    delta = 2e-4
    f = [exact(sample+k*delta, t) for k in (-2, -1, 0, 1, 2)]
    first = (f[0]["u"]-8*f[1]["u"]+8*f[3]["u"]-f[4]["u"])/(12*delta)
    second = (-f[0]["u"]+16*f[1]["u"]-30*f[2]["u"]
              +16*f[3]["u"]-f[4]["u"])/(12*delta**2)
    j_first = (f[0]["J"]-8*f[1]["J"]+8*f[3]["J"]-f[4]["J"])/(12*delta)
    errors = {"uX": float(np.max(np.abs(first-f[2]["uX"]))),
              "uXX": float(np.max(np.abs(second-f[2]["uXX"]))),
              "JX": float(np.max(np.abs(j_first-f[2]["JX"])))}
    assert errors["uX"] < 1e-8 and errors["JX"] < 1e-8 and errors["uXX"] < 3e-7, errors
    finite_differences.append({"t": t, "errors": errors})

record = {"status": "passed", "source_sha256": sha256(TWO_REFERENCE.encode()).hexdigest(),
          "comparison": "Independent raw tau moments, with the original two-soliton parameters.",
          "raw_moment_comparison": differences, "five_point_derivative_checks": finite_differences,
          "sampled_minimum_J": min(jacobians), "maximum_inverse_error": max(inverse_errors),
          "parameters": {"p": [1.1,1.25], "q": [11,5], "phase": float(np.log(6.5)), "A12": 12/507},
          "tested_times": [0,0.25,0.5], "finite_difference_step": 2e-4}
(HERE/"hs_two_reference_validation.json").write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"status": record["status"], "sampled_minimum_J": min(jacobians),
                  "max_inverse_error": max(inverse_errors), "checks": finite_differences}, ensure_ascii=False))
