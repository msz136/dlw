"""Exact consistency checks for the independent mixed hierarchy review.

The all-order derivative filtration and analytic mixed-BVP arguments are in
mixed_independent_review_20261011.md. Finite checks do not replace them.
"""
from pathlib import Path
import json
import sympy as sp

h, c, q, z, r, k = sp.symbols('h c q z r k', nonzero=True, real=True)
checks = []

for m in range(2, 10):
    one = sp.ones(m, 1)
    pi = one * one.T / m
    p0 = sp.eye(m) - pi
    shift = sp.zeros(m)
    for j in range(m):
        shift[j, (j - 1) % m] = 1
    delta = (sp.eye(m) - shift) / h
    mean = (sp.eye(m) + shift) / 2
    R = (delta + pi).inv() * mean * p0
    H = sp.Matrix(m, m, lambda i, j: 1 if j < i else 0)
    A = sp.eye(m) + 2 * H
    Z = sp.Matrix(m, m - 1, lambda i, j: (1 if i == j else 0) - (1 if i == m - 1 else 0))
    E = sp.eye(m)[:m - 1, :]
    assert sp.simplify(R + R.T) == sp.zeros(m)
    assert sp.simplify(R - h * p0 * A * p0 / 2) == sp.zeros(m)
    assert sp.simplify(Z * E * p0 - p0) == sp.zeros(m)
    # q = (p^T Z)/2 - (h s^T A Z)/8 + constant.  Substituting
    # p = v - R s/2 cancels the projected s coefficient exactly.
    assert sp.simplify(p0 * (R / 4 - h * A / 8) * p0) == sp.zeros(m)
    checks.append({'M': m, 'R_skew': True, 'R_triangular_identity': True,
                   'ZE_identity': True, 'shear_top_density_cancellation': True})

for n in range(1, 12):
    m = sp.symbols('M', positive=True, integer=True)
    G = h * m * c / 4
    density_coefficient = (-1) ** (n + 1) / (2 * m * c)
    coeff_v = -density_coefficient * (-1) ** n / h
    coeff_s = -density_coefficient / h
    assert sp.simplify(coeff_v - 1 / (8 * G)) == 0
    assert sp.simplify(coeff_s - (-1) ** n / (8 * G)) == 0
    checks.append({'n': n, 'principal_v_coefficient': '1/(8G)',
                   'principal_s_coefficient': f'{(-1) ** n}/(8G)',
                   'smoothing_exponent': f'{n}/{n + 1}'})

# Closure difference, per h M integral: the mean-dependent part of H-qU.
b = (q - z) / c
mean_part = c * b**2 / 2 + b * z - q * b
mean_part_zero = -z**2 / (2 * c)
assert sp.simplify(mean_part - mean_part_zero - q * z / c + q**2 / (2*c)) == 0
checks.append({'closure_identity': 'K_q=K_0+(q/c)P-hML*q^2/(2c)', 'exact': True})

# Sheared constant-background symbol. R(theta)=-i*r, beta=h^2/32.
V = sp.symbols('V', real=True)
beta = h**2 / 32
Rtheta = -sp.I * r
L = sp.Matrix([
    [k**2 + sp.I*k*(-V-c*Rtheta/2), sp.I*k*(c*Rtheta**2/4-2*beta*c)],
    [-sp.I*c*k, -k**2 + sp.I*k*(c*Rtheta/2-V)]
])
centered = L + sp.I*V*k*sp.eye(2)
Delta = k**4-c*r*k**3-h**2*c**2*k**2/16
assert sp.simplify(centered**2-Delta*sp.eye(2)) == sp.zeros(2)
checks.append({'sheared_linear_discriminant': str(Delta), 'exact': True})

result = {'status': 'passed', 'checks': checks,
          'limits': 'Finite symbolic consistency checks; the manuscript supplies all-order proofs.'}
output = Path(__file__).with_name('mixed_hierarchy_symbol_checks.json')
output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'status': 'passed', 'check_groups': len(checks),
                  'output': str(output)}, ensure_ascii=False))
