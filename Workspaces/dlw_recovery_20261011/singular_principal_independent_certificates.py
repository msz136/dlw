"""New exact constant-stage certificates; no old scripts are imported or run."""
from pathlib import Path
import hashlib
import json
import sympy as sp

count = 0
records = []

def check(predicate):
    global count
    assert predicate
    count += 1

def had(a, b):
    return sp.Matrix([u * v for u, v in zip(a, b)])

lam = sp.Symbol("lambda")
h = sp.Integer(2)
beta = h**2 / 32
for m in range(3, 11):
    ones = sp.ones(m, 1)
    pr = sp.eye(m) - ones * ones.T / m
    half_primitive = sp.Matrix(m, m, lambda i, j: 1 if i > j else sp.Rational(1, 2) if i == j else 0)
    r_op = h * pr * half_primitive * pr
    s = sp.Matrix([1, 1, -2] + [0] * (m - 3))
    t = sp.Matrix([1, -1, 0] + [0] * (m - 3))
    r = r_op * s
    p = t - r / 2
    inner = lambda a, b: (a.T * b)[0] / m
    kappa = -inner(s, had(p, p)) - 2 * beta * inner(s, had(s, s)) / 3
    check(r_op.T == -r_op)
    check(inner(s, had(r, r)) == -h**2 * inner(s, had(s, s)) / 12)
    check(inner(t, s) == 0 and kappa == -(2 + h) / m)
    c = pr * had(s, p)
    h_yy_t = pr * had(s, t)
    h_sy_t = pr * (had(p, t) + r_op * had(s, t) / 2)
    ell = ((4 * c - 2 * h_yy_t).T).row_join((-2 * h_sy_t).T) / (3 * kappa * m)
    w = t.col_join(s)
    operator = sp.diag(-sp.eye(m), sp.eye(m)) - w * ell
    a = (ell[:, :m] * t)[0]
    b = (ell[:, m:] * s)[0]
    check(a == -sp.Rational(2, 3) and b == sp.Rational(2, 3))
    zero = sp.zeros(1, m)
    constraints = sp.Matrix.vstack(ones.T.row_join(zero), zero.row_join(ones.T), s.T.row_join(zero), zero.row_join(t.T))
    basis = sp.Matrix.hstack(*constraints.nullspace())
    check(basis.cols == 2 * m - 4 and constraints * operator * basis == sp.zeros(4, basis.cols))
    reduced = (basis.T * basis).inv() * basis.T * operator * basis
    expected = (lam**2 + sp.Rational(1, 3)) * (lam - 1)**(m - 3) * (lam + 1)**(m - 3)
    check(sp.expand(reduced.charpoly(lam).as_expr() - expected) == 0)
    check((reduced**2 - sp.eye(reduced.rows)) * (reduced**2 + sp.eye(reduced.rows) / 3) == sp.zeros(reduced.rows))
    records.append({"M": m, "kappa": str(kappa), "constraint_dimension": basis.cols, "checks": 7, "expected_spectrum": "-1,+1 each M-3; +/- i/sqrt(3)"})

source = Path(__file__)
result = {"status": "all new independent constant-stage principal checks passed", "sympy": sp.__version__, "assert_count": count, "checks": records, "script_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "scope": "Exact rational compatible constant backgrounds M=3..10. All-M proof and constant-background limitations are in singular_branch_independent_audit.md section 8."}
source.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
