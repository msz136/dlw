"""Exact rational checks for the first-order cross-D DLW Hamilton candidate.

No numerical near-zero criterion is used. The finite x derivative below is
only an algebraic check of the variational identities, not an existence proof
for the continuous x evolution.
"""
from pathlib import Path
import json
import sympy as sp


def zero(expr):
    if isinstance(expr, sp.MatrixBase):
        assert all(sp.simplify(x) == 0 for x in expr), expr
    else:
        assert sp.simplify(expr) == 0, expr


def lattice(n, h):
    eye = sp.eye(n)
    prev = sp.zeros(n)
    for j in range(n):
        prev[j, (j - 1) % n] = 1
    proj = sp.ones(n) / n
    complement = eye - proj
    d = (eye - prev) / h
    avg = (eye + prev) / 2
    delta = (prev.T - prev) / (2 * h)
    kernel = [sp.Integer(0)] + [h * (sp.Rational(1, 2) - sp.Rational(k, n)) for k in range(1, n)]
    inverse = sp.Matrix(n, n, lambda j, k: kernel[(j - k) % n])
    zero(inverse.T + inverse)
    zero(d * inverse - avg * complement)
    zero(inverse * proj)
    zero(delta.T + delta)
    zero(inverse * delta - delta * inverse)
    return d, avg, delta, proj, complement, inverse


h = sp.Rational(2, 3)
for lattice_n in (3, 4, 5, 6, 7, 8):
    lattice(lattice_n, h)

# Solve the nonlinear and linear Helmholtz conditions in J = - C D.
p, q0, r0, beta, u, w = sp.symbols("p q0 r0 beta u w", real=True)
metric_inverse = sp.Matrix([[p, q0], [q0, r0]])
flux_jacobian = sp.Matrix([[u, 2 * beta * w], [w, u]])
nonlinear_defect = metric_inverse * flux_jacobian
zero(nonlinear_defect[0, 1] - nonlinear_defect[1, 0] - (2 * beta * p - r0) * w)
xi, eta = sp.symbols("xi eta", real=True, nonzero=True)
linear_grad = sp.I * xi * metric_inverse * sp.Matrix([[1, sp.I * eta], [0, -1]])
conditions = list(linear_grad - linear_grad.conjugate().T)
linear_solution = sp.solve(conditions, [p, r0], dict=True)
assert linear_solution == [{p: 0, r0: 0}], linear_solution
zero(linear_grad.subs({p: 0, r0: 0}) - linear_grad.subs({p: 0, r0: 0}).conjugate().T)

# Exact identity for the reduced energy.
m, c, sigma, alpha = sp.symbols("m c sigma alpha", real=True, nonzero=True)
mean_energy = m * alpha ** 2 / 2 + alpha * sigma - c * alpha
zero(mean_energy.subs(alpha, (c - sigma) / m) + (c - sigma) ** 2 / (2 * m))

# Nontrivial finite-dimensional algebraic residual checks.
n, nx = 5, 3
d, avg, delta, proj, complement, inverse = lattice(n, h)
xprev = sp.zeros(nx)
for i in range(nx):
    xprev[i, (i - 1) % nx] = 1
dx = (xprev.T - xprev) / 2
zero(dx.T + dx)

def Dx(field):
    return field * dx.T

def Dxx(field):
    return Dx(Dx(field))

def product(a, b):
    return a.multiply_elementwise(b)

def summation(field):
    return sum(field)

def full_energy(U, W):
    return h * summation(product(product(U, U), W) / 2
                         + beta_value * product(product(W, W), W) / 3
                         + product(W, Dx(U))
                         + product(W, inverse * Dx(W)) / 2)

rawq = sp.Matrix(n, nx, lambda j, i: sp.Rational((j + 2) ** 2 + (i + 1) * (j - 2), 13))
rawr = sp.Matrix(n, nx, lambda j, i: sp.Rational((j + 1) * (i + 3) + i ** 2 - j ** 3, 17))
q = complement * rawq
r = complement * rawr
m_value, a_value = -4, sp.Rational(3, 5)
c_value = -8 * a_value
beta_value = h ** 2 / 32
sig = proj * product(q, r)
A = (sp.ones(n, nx) * c_value - sig) / m_value
U = A + q
W = sp.ones(n, nx) * m_value + r - delta * q
zero(proj * W - sp.ones(n, nx) * m_value)
zero(proj * product(U, W) - sp.ones(n, nx) * c_value)
gU = product(U, W) - Dx(W)
gW = product(U, U) / 2 + beta_value * product(W, W) + Dx(U) + inverse * Dx(W)
gu = gU + delta * gW - sp.ones(n, nx) * c_value
gv = gW
zero(proj * gu)
qt = -complement * Dx(gv)
rt = -complement * Dx(gu)
At = -proj * (product(r, qt) + product(q, rt)) / m_value
Ut = qt + At
Wt = rt - delta * qt
flux = product(U, U) / 2 + beta_value * product(W, W)
zero(d * (Ut + Dx(flux) + Dxx(U)) + avg * Dxx(W))
zero(Wt + Dx(product(U, W)) - Dxx(W))

# Directional derivatives of the pullback energy, independently differentiated.
epsilon = sp.symbols("epsilon", real=True)
for seed in (1, 2, 3):
    dq = complement * sp.Matrix(n, nx, lambda j, i: sp.Rational((j + seed) * (i + 2) - (j - i) ** 2, 7 + seed))
    dr = complement * sp.Matrix(n, nx, lambda j, i: sp.Rational(j ** 2 + seed * i * j - (i + 1) ** 3, 9 + seed))
    qe = q + epsilon * dq
    re = r + epsilon * dr
    Ae = (sp.ones(n, nx) * c_value - proj * product(qe, re)) / m_value
    Ue = qe + Ae
    We = sp.ones(n, nx) * m_value + re - delta * qe
    Ke = full_energy(Ue, We) - c_value * h * summation(Ue)
    direct_derivative = sp.diff(Ke, epsilon).subs(epsilon, 0)
    claimed_derivative = h * summation(product(gu, dq) + product(gv, dr))
    zero(direct_derivative - claimed_derivative)

# The finite-dimensional pushed bracket must be skew; Jacobi is proved by
# the coordinate pushforward in NOTES.md rather than inferred from skewness.
size = n * nx
DD = sp.kronecker_product(complement, dx)
JJ = sp.zeros(2 * size)
JJ[:size, size:] = -DD
JJ[size:, :size] = -DD
PP = sp.kronecker_product(proj, sp.eye(nx))
qdiag = sp.diag(*list(q))
rdiag = sp.diag(*list(r))
T = sp.eye(2 * size)
T[:size, :size] = sp.eye(size) - PP * rdiag / m_value
T[:size, size:] = -PP * qdiag / m_value
physical_J = T * JJ * T.T
zero(physical_J + physical_J.T)

result = {
    "arithmetic": "exact SymPy rational/symbolic",
    "periodic_kernel_N": [3, 4, 5, 6, 7, 8],
    "kernel_skew_and_dR_MQ": "PASS",
    "narrow_constant_first_order_Helmholtz": "PASS: p=r0=0",
    "reduced_energy_identity": "PASS",
    "reduced_physical_phase_mean_constraints": "PASS",
    "original_shifted_DLW_residuals": "identically zero",
    "pullback_energy_directional_derivatives": 3,
    "pushed_operator_skew": "PASS",
    "Jacobi": "analytic constant-bracket and diffeomorphism proof in NOTES.md",
    "Liouville_integrability": "not established",
}
output_path = Path(__file__).with_name("verification_result.json")
output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
