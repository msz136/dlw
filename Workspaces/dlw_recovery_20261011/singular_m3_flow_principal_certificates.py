"""New exact M=3 identities; old singular-zero-flux certificates are not rerun.

This finite symbolic audit supports the separate analytic local-flow proof.
It does not prove physical inverse existence or Liouville completeness.
All-M frozen-principal independent evidence lives in the companion agent's
singular_principal_independent_certificates.py/.json.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


x = sp.Symbol("x", real=True)
u, v, z = (sp.Function(name)(x) for name in ("u", "v", "z"))
A, B, C = (sp.Function(name)(x) for name in ("A", "B", "C"))
checks: list[str] = []


def exact(name, expression):
    expression = sp.simplify(sp.expand(expression))
    assert expression == 0, (name, expression)
    checks.append(name)


def mul(left, right):
    """Compose scalar differential operators in left-coefficient convention."""
    result = {}
    for power, coefficient in left.items():
        for order, value in right.items():
            for derivative in range(power + 1):
                degree = power + order - derivative
                result[degree] = result.get(degree, 0) + (
                    coefficient * sp.binomial(power, derivative)
                    * sp.diff(value, x, derivative)
                )
    return {degree: sp.expand(value) for degree, value in result.items()}


def add(left, right, sign=1):
    result = dict(left)
    for degree, value in right.items():
        result[degree] = result.get(degree, 0) + sign * value
    return result


def power(operator, exponent):
    result = {0: sp.Integer(1)}
    for _ in range(exponent):
        result = mul(result, operator)
    return result


# Exact periodic scalar depression, including derivative signs.
E = {1: sp.Integer(1), 0: -A / 3}
depressed = add(add(add(power(E, 3), mul({0: A}, power(E, 2))),
                    mul({0: B}, E)), {0: C})
depression_target = {
    3: sp.Integer(1), 2: sp.Integer(0),
    1: B - sp.diff(A, x) - A**2 / 3,
    0: C - A * B / 3 + 2 * A**3 / 27 - sp.diff(A, x, 2) / 3,
}
for degree in range(4):
    exact(f"scalar_depression_D{degree}",
          depressed.get(degree, 0) - depression_target[degree])

# Negative t2 and constant-translation drift.
drift = sp.Symbol("drift", real=True)
Q = {3: sp.Integer(1), 1: u, 0: v}
K = {2: sp.Integer(1), 1: drift, 0: 2 * u / 3}
Q_t = add(mul(Q, K), mul(K, Q), -1)  # -[K,Q]
ut = sp.diff(u, x, 2) - 2 * sp.diff(v, x) - drift * sp.diff(u, x)
vt = (-sp.diff(v, x, 2) + sp.Rational(2, 3) * sp.diff(u, x, 3)
      + sp.Rational(2, 3) * u * sp.diff(u, x) - drift * sp.diff(v, x))
for degree in range(5):
    target = {1: ut, 0: vt}.get(degree, 0)
    exact(f"negative_t2_D{degree}", Q_t.get(degree, 0) - target)

# Depressed real Boussinesq variables and complex semilinear representation.
v_as_z = z + sp.diff(u, x) / 2
ut_z = sp.expand(ut.subs(v, v_as_z).doit())
zt_z = sp.expand(vt.subs(v, v_as_z).doit() - sp.diff(ut_z, x) / 2)
exact("real_Boussinesq_u",
      ut_z + 2 * sp.diff(z, x) + drift * sp.diff(u, x))
exact("real_Boussinesq_z",
      zt_z - sp.diff(u, x, 3) / 6 - 2 * u * sp.diff(u, x) / 3
      + drift * sp.diff(z, x))
alpha = 1 / (2 * sp.sqrt(3))
Psi = z + sp.I * alpha * sp.diff(u, x)
Psi_t = zt_z + sp.I * alpha * sp.diff(ut_z, x)
exact("semilinear_Schrodinger_identity",
      Psi_t + sp.I * sp.diff(Psi, x, 2) / sp.sqrt(3)
      + drift * sp.diff(Psi, x) - 2 * u * sp.diff(u, x) / 3)

# Energy derivative is a periodic total derivative.
ut0 = -2 * sp.diff(z, x)
zt0 = sp.diff(u, x, 3) / 6 + 2 * u * sp.diff(u, x) / 3
energy_t = 2 * z * zt0 + sp.diff(u, x) * sp.diff(ut0, x) / 6 - u**2 * ut0 / 3
flux = (z * sp.diff(u, x, 2) - sp.diff(u, x) * sp.diff(z, x)) / 3 + 2 * u**2 * z / 3
exact("energy_total_derivative", energy_t - sp.diff(flux, x))

# Finite-dimensional actual Floquet transport; no backward-heat extension.
space = sp.Matrix([[0, 1, 0], [0, 0, 1], [-v, -u, 0]])
time = sp.Matrix([
    [-2 * u / 3, 0, -1],
    [v - 2 * sp.diff(u, x) / 3, u / 3, 0],
    [sp.diff(v, x) - 2 * sp.diff(u, x, 2) / 3,
     v - sp.diff(u, x) / 3, u / 3],
])
ut0_v = sp.diff(u, x, 2) - 2 * sp.diff(v, x)
vt0_v = (-sp.diff(v, x, 2) + 2 * sp.diff(u, x, 3) / 3
         + 2 * u * sp.diff(u, x) / 3)
space_t = sp.zeros(3)
space_t[2, 0], space_t[2, 1] = -vt0_v, -ut0_v
curvature = space_t - time.diff(x) - (time * space - space * time)
for row in range(3):
    for column in range(3):
        exact(f"Floquet_zero_curvature_{row}{column}", curvature[row, column])

# The labelled bubble identity as a genuine differential-operator equality.
a, b = (sp.Function(name)(x) for name in ("a", "b"))
theta = (sp.diff(a, x) - sp.diff(b, x)) / (a - b)
left = mul({1: 1, 0: -b - theta}, {1: 1, 0: -a})
right = mul({1: 1, 0: -a - theta}, {1: 1, 0: -b})
for degree in range(3):
    exact(f"legal_bubble_cross_product_D{degree}",
          left.get(degree, 0) - right.get(degree, 0))

# Direct original-PDE factor bridge on the c=0 M=3 chart. The unprojected s
# equation is used exactly as in the compatible primary q_x=0 layer.
grid_count = 3
grid_h = sp.Integer(4)
grid_beta = grid_h**2 / 32
ones = sp.ones(grid_count, 1)
grid_average = ones * ones.T / grid_count
grid_zero = sp.eye(grid_count) - grid_average
shift_minus = sp.zeros(grid_count)
for j in range(grid_count):
    shift_minus[j, (j - 1) % grid_count] = 1
delta_minus = (sp.eye(grid_count) - shift_minus) / grid_h
grid_R = (delta_minus + grid_average).inv() * (sp.eye(grid_count) + shift_minus) * grid_zero / 2
p0, p1, s0, s1 = (sp.Function(name)(x) for name in ("p0", "p1", "s0", "s1"))
pfield = sp.Matrix([p0, p1, -p0 - p1])
sfield = sp.Matrix([s0, s1, -s0 - s1])
quadratic_flux = sp.Matrix([
    pfield[j]**2 / 2 + grid_beta * sfield[j]**2 for j in range(grid_count)
])
p_time = (-sp.Matrix([sp.diff(b * pfield[j], x) for j in range(grid_count)])
          - (grid_zero * quadratic_flux).diff(x) - pfield.diff(x, 2)
          - grid_R * sfield.diff(x, 2))
s_time = (sfield.diff(x, 2) - sp.Matrix([
    sp.diff(b * sfield[j] + pfield[j] * sfield[j], x)
    for j in range(grid_count)
]))
nu_common = -sum(
    pfield[j]**2 / 4 + grid_beta * sfield[j]**2 / 2
    for j in range(grid_count)
) / grid_count
nu_grid = sp.Matrix([
    nu_common + (grid_R * sfield.diff(x))[j] / 2
    - grid_h * sp.diff(sfield[j], x) / 4
    for j in range(grid_count)
])
for j in range(grid_count):
    next_j = (j + 1) % grid_count
    exact(f"direct_PDE_potential_difference_grid{j}",
          nu_grid[next_j] - nu_grid[j] - grid_h * sp.diff(sfield[j], x) / 2)
    for sign, label, nu in ((1, "plus", nu_grid[j]),
                           (-1, "minus", nu_grid[next_j])):
        local_a = pfield[j] / 2 + sign * grid_h * sfield[j] / 8
        local_at = p_time[j] / 2 + sign * grid_h * s_time[j] / 8
        exact(f"direct_PDE_Riccati_{label}_grid{j}",
              local_at + sp.diff(nu, x) + sp.diff(local_a, x, 2)
              + sp.diff(b * local_a + local_a**2, x))

# General intertwiner identity for either first-order factor.
nu_in = sp.Function("nu_in")(x)
nu_out = nu_in + sp.diff(b, x) + 2 * sp.diff(a, x)
first_factor = {1: 1, 0: -a}
L_in = {2: 1, 1: b, 0: nu_in}
L_out = {2: 1, 1: b, 0: nu_out}
factor_time = add(mul(first_factor, L_in), mul(L_out, first_factor), -1)
minus_at = sp.diff(nu_in, x) + sp.diff(a, x, 2) + sp.diff(b * a + a**2, x)
for degree in range(4):
    exact(f"general_first_factor_intertwiner_D{degree}",
          factor_time.get(degree, 0) - (minus_at if degree == 0 else 0))

# Explicit nonresonant real constant graph and normalization.
symbol_D, amplitude, d = sp.symbols("D amplitude d", real=True)
a3 = d * (-amplitude**2 + 4 * d**2)
Q_constant = (symbol_D - amplitude / 2 + d) * (symbol_D + amplitude / 2 + d) * (symbol_D - 2 * d)
R_constant = (symbol_D + 2 * d) * (symbol_D + amplitude / 2 - d) * (symbol_D - amplitude / 2 - d)
exact("constant_R_minus_Q_is_a3", R_constant - Q_constant - a3)
exact("constant_depressed_Q",
      Q_constant - (symbol_D**3 + (-amplitude**2 / 4 - 3 * d**2) * symbol_D - a3 / 2))
h, r = sp.symbols("h r", nonzero=True, real=True)
kappa = 2 * r * (-amplitude**2 + h**2 * r**2 / 16) / 3
exact("a3_kappa_normalization",
      a3.subs(d, h * r / 8) - 3 * h * kappa / 16)

# Scalar Fourier dispersion, including lower-order real-background term.
frequency, lam, ustar = sp.symbols("frequency lambda ustar", real=True)
linear_symbol = sp.Matrix([
    [-sp.I * drift * frequency, -2 * sp.I * frequency],
    [sp.I * frequency * (2 * ustar / 3 - frequency**2 / 6),
     -sp.I * drift * frequency],
])
exact("real_scalar_Fourier_dispersion",
      (lam * sp.eye(2) - linear_symbol).det()
      - ((lam + sp.I * drift * frequency)**2
         - 4 * ustar * frequency**2 / 3 + frequency**4 / 3))

path = Path(__file__).resolve()
output = {
    "status": "all new exact checks passed",
    "check_count": len(checks),
    "checks": checks,
    "sympy_version": sp.__version__,
    "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "old_33_check_script_rerun": False,
    "all_M_independent_evidence": "singular_principal_independent_certificates.json",
    "scope": [
        "M=3 exact scalar depression and negative t2 coefficients",
        "real Boussinesq/semilinear Schrodinger identity and conserved energy flux",
        "actual 3x3 zero-curvature and legal scalar bubble equality",
        "direct original PDE Riccati and factor-intertwiner bridge",
        "explicit nonresonant constant normalization and Fourier dispersion",
    ],
    "not_certified_by_this_script": [
        "analytic local existence (proved separately in the report)",
        "static/dynamic labelled Floquet physical inverse (proved separately)",
        "regular nonconstant full-M principal symbol",
        "Liouville functional independence or completeness",
    ],
}
path.with_suffix(".json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: output[key] for key in ("status", "check_count", "script_sha256")}, ensure_ascii=False))
