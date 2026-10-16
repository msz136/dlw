"""Fresh order-two c=0, nonzero-Gamma cKP audit; no previous script rerun."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as sp

x = sp.Symbol("x", real=True)
u, f, g = (sp.Function(name)(x) for name in ("u", "f", "g"))
checks = []


def exact(name, expression):
    assert sp.simplify(sp.expand(expression)) == 0, (name, expression)
    checks.append(name)


def product(left, right, lower=-7):
    result = {}
    for degree, coefficient in left.items():
        for order, value in right.items():
            for derivative in range(max(0, degree + order - lower) + 1):
                if degree >= 0 and derivative > degree:
                    break
                power = degree + order - derivative
                if power >= lower:
                    result[power] = result.get(power, 0) + (
                        coefficient * sp.binomial(degree, derivative)
                        * sp.diff(value, x, derivative)
                    )
    return result


W = {2: 1, 0: u}
for j in range(9):
    W[-1-j] = (-1)**j * f * sp.diff(g, x, j)
B = {2: 1, 0: u}
WB, BW = product(W, B), product(B, W)
Wt = {degree: WB.get(degree, 0) - BW.get(degree, 0) for degree in set(WB) | set(BW)}
for degree in range(5):
    exact(f"order2_positive_D{degree}",
          Wt.get(degree, 0) - (-2 * sp.diff(f * g, x) if degree == 0 else 0))
ft, gt = -sp.diff(f, x, 2) - u * f, sp.diff(g, x, 2) + u * g
for j in range(5):
    target = (-1)**j * (ft * sp.diff(g, x, j) + f * sp.diff(gt, x, j))
    exact(f"order2_negative_D{-1-j}", Wt.get(-1-j, 0) - target)
exact("n0_center_is_static", Wt[0].subs(f, 0).doit())

# Newton identities detect the original Gamma sign from a monic R-Q jump.
q1, q2, a, h, M = sp.symbols("q1 q2 a h M", nonzero=True, real=True)
sum_alpha_squared = q1**2 - 2 * q2
sum_beta_squared = q1**2 - 2 * (q2 + a)
exact("order2_Newton_second_moment_jump",
      sum_beta_squared - sum_alpha_squared + 2 * a)
Gamma = 4 * (sum_beta_squared - sum_alpha_squared) / (h * M)
exact("original_a2_Gamma_normalization", -h * M * Gamma / 8 - a)

path = Path(__file__).resolve()
output = {
    "status": "all new order-two cKP exact checks passed",
    "check_count": len(checks),
    "checks": checks,
    "sympy_version": sp.__version__,
    "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "previous_certificate_scripts_rerun": False,
    "scope": [
        "order-two cKP positive coefficients and five negative coefficients",
        "no-source n=0 static center",
        "Newton second-moment and original Gamma sign normalization",
    ],
    "not_proved_by_script": [
        "actual mixed contraction (analytic proof in the report)",
        "flagged physical inverse and finite-jet Bezout bridge",
        "arbitrary physical Cauchy flow or Liouville completeness",
    ],
}
path.with_suffix(".json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: output[key] for key in ("status", "check_count", "script_sha256")}))
