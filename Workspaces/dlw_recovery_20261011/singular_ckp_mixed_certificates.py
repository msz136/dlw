"""Fresh cKP algebra checks; no prior singular certificate is rerun."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as sp

x = sp.Symbol("x", real=True)
u, v, z, f, g, potential = (
    sp.Function(name)(x) for name in ("u", "v", "z", "f", "g", "potential")
)
checks = []


def exact(name, expression):
    assert sp.simplify(sp.expand(expression)) == 0, (name, expression)
    checks.append(name)


def compose(left, right, lower):
    result = {}
    for p, a in left.items():
        for q, b in right.items():
            for j in range(max(0, p + q - lower) + 1):
                if p >= 0 and j > p:
                    break
                order = p + q - j
                if order >= lower:
                    result[order] = result.get(order, 0) + a * sp.binomial(p, j) * sp.diff(b, x, j)
    return result


def subtract(left, right):
    result = dict(left)
    for order, value in right.items():
        result[order] = result.get(order, 0) - value
    return result


drift = sp.Symbol("drift", real=True)
K0 = {2: 1, 1: drift, 0: 2 * u / 3}
W = {3: 1, 1: u, 0: v}
for j in range(9):
    W[-1-j] = (-1)**j * f * sp.diff(g, x, j)
Wtime = subtract(compose(W, K0, -7), compose(K0, W, -7))
ut = sp.diff(u, x, 2) - 2 * sp.diff(v, x) - drift * sp.diff(u, x)
vt = (-sp.diff(v, x, 2) + 2 * sp.diff(u, x, 3) / 3
      + 2 * u * sp.diff(u, x) / 3 - 2 * sp.diff(f * g, x)
      - drift * sp.diff(v, x))
for order in range(5):
    exact(f"cKP_positive_D{order}",
          Wtime.get(order, 0) - {1: ut, 0: vt}.get(order, 0))

ft = -sp.diff(f, x, 2) - drift * sp.diff(f, x) - 2 * u * f / 3
gt = sp.diff(g, x, 2) - drift * sp.diff(g, x) + 2 * u * g / 3
for j in range(5):
    target = (-1)**j * (ft * sp.diff(g, x, j) + f * sp.diff(gt, x, j))
    exact(f"cKP_negative_D{-1-j}", Wtime.get(-1-j, 0) - target)

v_as_z = z + sp.diff(u, x) / 2
ut_z = ut.subs(v, v_as_z).doit()
zt_z = vt.subs(v, v_as_z).doit() - sp.diff(ut_z, x) / 2
alpha = 1 / (2 * sp.sqrt(3))
Psi = z + sp.I * alpha * sp.diff(u, x)
Psi_t = zt_z + sp.I * alpha * sp.diff(ut_z, x)
exact("cKP_Schrodinger_heat_source",
      Psi_t + sp.I * sp.diff(Psi, x, 2) / sp.sqrt(3)
      + drift * sp.diff(Psi, x) - 2 * u * sp.diff(u, x) / 3
      + 2 * sp.diff(f * g, x))

mu = sp.Symbol("mu", real=True)
phi = sp.exp(mu * x) * f
psi = sp.exp(-mu * x) * g
exact("dual_twist_product", phi * psi - f * g)
exact("dual_twist_source_derivative", sp.diff(phi * psi, x) - sp.diff(f * g, x))
exact("twisted_backward_heat",
      sp.exp(-mu * x) * (-sp.diff(phi, x, 2) - drift * sp.diff(phi, x) - potential * phi)
      + sp.diff(f, x, 2) + (2 * mu + drift) * sp.diff(f, x)
      + (mu**2 + drift * mu + potential) * f)
exact("twisted_forward_heat",
      sp.exp(mu * x) * (sp.diff(psi, x, 2) - drift * sp.diff(psi, x) + potential * psi)
      - sp.diff(g, x, 2) - (-2 * mu - drift) * sp.diff(g, x)
      - (mu**2 + drift * mu + potential) * g)

# n=1 Darboux quotient identity, with the correct output generator.
r = sp.Function("r")(x)
K = {1: 1, 0: -r}
input_time = {2: 1, 0: potential}
output_time = {2: 1, 0: potential + 2 * sp.diff(r, x)}
Kt = subtract(compose(K, input_time, 0), compose(output_time, K, 0))
target_Kt = sp.diff(r, x, 2) + 2 * r * sp.diff(r, x) + sp.diff(potential, x)
for order in range(4):
    exact(f"kernel_Darboux_output_D{order}",
          Kt.get(order, 0) - (target_Kt if order == 0 else 0))

# Symbolic finite-dimensional algebra P=Q^{-1}R and W=K^{-1}Q:
# the actual all-order identities are proved in the report; noncommutative
# cancellation below records their numerator form without a truncated inverse.
q, rr, kk, aa, ll = sp.symbols("Q R K A L", commutative=False)
qtime = q * ll - aa * q
rtime = rr * ll - aa * rr
exact("same_left_output_P_commutator_numerator",
      -qtime * sp.Symbol("P", commutative=False) + rtime
      - (-q * ll * sp.Symbol("P", commutative=False)
         + rr * ll + aa * (q * sp.Symbol("P", commutative=False) - rr)))

path = Path(__file__).resolve()
output = {
    "status": "all new cKP mixed algebra checks passed",
    "check_count": len(checks),
    "checks": checks,
    "sympy_version": sp.__version__,
    "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "previous_certificate_scripts_rerun": False,
    "scope": [
        "positive differential part and five negative coefficients of exact rank-one cKP",
        "real Schrodinger variable and heat-source derivative",
        "opposite Floquet twists",
        "n=1 Darboux output generator and noncommutative numerator cancellation",
    ],
    "not_proved_by_script": [
        "general finite-rank identity (proved by variation of constants)",
        "mixed Banach contraction and common smooth time window",
        "flagged physical inverse and its actual-vector pullback",
        "arbitrary physical initial-state Cauchy flow",
        "Liouville independence or completeness",
    ],
}
path.with_suffix(".json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: output[key] for key in ("status", "check_count", "script_sha256")}))
