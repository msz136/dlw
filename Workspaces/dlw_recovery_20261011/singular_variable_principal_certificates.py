"""Exact rational checks for the newly derived variable-background symbol.

The jets have q=q_x=0 and a nonzero Wronskian contribution to chi.  These are
local compatible first jets, not a construction of exact periodic curves.
Neither previous certificate script is rerun.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sympy as sp

checks = []
period_results = []


def exact(name, expression):
    if isinstance(expression, sp.MatrixBase):
        assert all(sp.simplify(value) == 0 for value in expression), (name, expression)
    else:
        assert sp.simplify(expression) == 0, (name, expression)
    checks.append(name)


def nonzero(name, expression):
    assert sp.simplify(expression) != 0, (name, expression)
    checks.append(name)


lam = sp.Symbol("lambda")
for M in range(3, 9):
    h = sp.Integer(4)
    beta = h**2 / 32
    ones = sp.ones(M, 1)
    average = ones * ones.T / M
    P0 = sp.eye(M) - average
    shift = sp.zeros(M)
    for j in range(M):
        shift[j, (j - 1) % M] = 1
    R = ((sp.eye(M) - shift) / h + average).inv() * (sp.eye(M) + shift) * P0 / 2
    p = sp.Matrix([2, -2] + [0] * (M - 2))
    S = sp.Matrix([1, 1, -2] + [0] * (M - 3))
    T = p + R * S / 2
    Tx = S
    Sx = -(S.dot(S) / T.dot(T)) * T
    V = sum(p[j]**2 * S[j] / 2 + beta * S[j]**3 / 3 for j in range(M)) / M
    omega = (T.dot(Sx) - S.dot(Tx)) / M
    kappa = -2 * V + omega
    c = P0 * sp.matrix_multiply_elementwise(p, S)
    e = P0 * sp.Matrix([p[j]**2 / 2 + beta * S[j]**2 for j in range(M)]) + R * c / 2
    HYY = P0 * sp.diag(*S) * P0
    HsY = P0 * sp.diag(*p) * P0 + R * HYY / 2
    HYs = HsY.T
    Hss = (P0 * sp.diag(*(2 * beta * S)) * P0
           - (P0 * sp.diag(*p) * R - R * sp.diag(*p) * P0) / 2
           - R * HYY * R / 4)
    exact(f"M{M}_q", T.dot(S))
    exact(f"M{M}_qx", Tx.dot(S) + T.dot(Sx))
    nonzero(f"M{M}_nonconstant_Wronskian", omega)
    nonzero(f"M{M}_kappa", kappa)
    exact(f"M{M}_Hessian_symmetry", Hss - Hss.T)

    # Extract the top two differential coefficients directly from A_chi dF0.
    Achi1 = (-S.T).row_join(T.T) / M
    Achi0 = (-2 * c + Sx).T.row_join((-2 * e - Tx).T) / M
    F2 = sp.diag(-sp.eye(M), sp.eye(M))
    F1 = -(HsY.row_join(Hss)).col_join(HYY.row_join(HYs))
    coefficient3 = Achi1 * F2
    coefficient2 = Achi1 * F1 + Achi0 * F2
    phi = S.T.row_join(T.T) / M
    phi_x = Sx.T.row_join(Tx.T) / M
    exact(f"M{M}_primary_third_order", coefficient3 - phi)
    ry = 4 * c - 2 * HYY * T - 4 * Sx
    rz = -2 * HsY * T - 4 * Tx
    exact(f"M{M}_primary_eliminated_second_order",
          coefficient2 - 3 * phi_x - ry.T.row_join(rz.T) / M)
    ell_y, ell_z = ry.T / (3 * M * kappa), rz.T / (3 * M * kappa)
    exact(f"M{M}_universal_minus_two_thirds", (ell_y * T)[0] + sp.Rational(2, 3))
    exact(f"M{M}_universal_plus_two_thirds", (ell_z * S)[0] - sp.Rational(2, 3))

    # Restrict to zero-lattice-mean leading paired-constraint tangent space.
    lattice_basis = sp.zeros(M, M - 1)
    for j in range(M - 1):
        lattice_basis[j, j], lattice_basis[M - 1, j] = 1, -1
    minus_basis = lattice_basis * sp.Matrix.hstack(*(S.T * lattice_basis).nullspace())
    plus_basis = lattice_basis * sp.Matrix.hstack(*(T.T * lattice_basis).nullspace())
    tangent_basis = sp.diag(minus_basis, plus_basis)
    effective = F2 - T.col_join(S) * ell_y.row_join(ell_z)
    left_inverse = (tangent_basis.T * tangent_basis).inv() * tangent_basis.T
    reduced = left_inverse * effective * tangent_basis
    exact(f"M{M}_paired_tangent_invariance", effective * tangent_basis - tangent_basis * reduced)
    polynomial = sp.factor(reduced.charpoly(lam).as_expr())
    expected = (lam**2 + sp.Rational(1, 3)) * (lam**2 - 1)**(M - 3)
    exact(f"M{M}_variable_symbol_characteristic", polynomial - expected)
    period_results.append({
        "M": M, "tangent_dimension": reduced.rows,
        "omega": str(omega), "kappa": str(kappa),
        "characteristic": str(polynomial),
    })

path = Path(__file__).resolve()
output = {
    "status": "all variable-background first-jet exact checks passed",
    "check_count": len(checks),
    "checks": checks,
    "period_results": period_results,
    "sympy_version": sp.__version__,
    "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    "old_certificate_scripts_rerun": False,
    "scope": "q=q_x=0 first jets with nonzero Wronskian, M=3..8; full-M algebra in report",
    "not_proved": [
        "exact periodic compatible high-frequency curves",
        "actual C1 ill-posedness",
        "full-M smooth local flow",
        "Liouville independence or completeness",
    ],
}
path.with_suffix(".json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: output[key] for key in ("status", "check_count", "script_sha256")}))
