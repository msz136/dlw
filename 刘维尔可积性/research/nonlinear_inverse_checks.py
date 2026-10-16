"""Exact algebra checks for the scalar-monodromy nonlinear inverse route.

This script does not establish inverse spectral completeness, a Banach inverse
function theorem, or existence of the physical time flow.  It checks finite Ore
algebra identities and records their exact outputs.  Run with SymPy 1.13.3.
"""

from __future__ import annotations

import json
import hashlib
from pathlib import Path

import sympy as sp


x = sp.Symbol("x", real=True)
c = sp.Symbol("c", nonzero=True, real=True)


def diff_product(left: dict[int, sp.Expr], right: dict[int, sp.Expr]):
    """Left-normal ordinary differential multiplication, by Leibniz rule."""
    out: dict[int, sp.Expr] = {}
    for i, f in left.items():
        assert i >= 0
        for j, g in right.items():
            for ell in range(i + 1):
                power = i + j - ell
                out[power] = out.get(power, 0) + (
                    f * sp.binomial(i, ell) * sp.diff(g, x, ell)
                )
    return {power: sp.simplify(value) for power, value in out.items()}


def qp_coefficient(q: list[sp.Expr], p: list[sp.Expr], power: int):
    """Extract one power of Q P from the independent Leibniz expansion.

    q[i] multiplies D**i; p[n] multiplies D**(-n), and p[0]=1.
    Only nonnegative differential powers occur on the left.
    """
    terms = []
    for i, qi in enumerate(q):
        for n, pn in enumerate(p):
            ell = i - n - power
            if 0 <= ell <= i:
                terms.append(qi * sp.binomial(i, ell) * sp.diff(pn, x, ell))
    return sp.expand(sum(terms))


def fraction_expansion(q: list[sp.Expr], r: list[sp.Expr], count: int):
    """Recursively solve Q P=R at descending powers; Q,R have monic order M."""
    m = len(q) - 1
    assert q[m] == r[m] == 1
    p = [sp.Integer(1)]
    for n in range(1, count + 1):
        # The only not-yet-known contribution at D**(M-n) is p[n].
        target = r[m - n] if n <= m else sp.Integer(0)
        known = qp_coefficient(q, p, m - n)
        p.append(sp.expand(target - known))
    return p


def finite_system(p: list[sp.Expr], m: int):
    a = sp.Matrix(
        m,
        m,
        lambda rr, ii: sum(
            sp.binomial(ii, ell) * sp.diff(p[rr + 1 + ii - ell], x, ell)
            for ell in range(ii + 1)
        ),
    )
    rhs = sp.Matrix(
        [
            -sum(
                sp.binomial(m, ell) * sp.diff(p[rr + m - ell], x, ell)
                for ell in range(m + 1)
            )
            for rr in range(1, m + 1)
        ]
    )
    return a, rhs


def check_exchange():
    a, b = sp.Function("a")(x), sp.Function("b")(x)
    theta = sp.diff(a - b, x) / (a - b)
    aa = {1: sp.Integer(1), 0: -a}
    bb = {1: sp.Integer(1), 0: -b}
    ee = {1: sp.Integer(1), 0: -b - theta}
    cc = {1: sp.Integer(1), 0: -a - theta}
    ea, cb = diff_product(ee, aa), diff_product(cc, bb)
    residual = {k: sp.simplify(ea.get(k, 0) - cb.get(k, 0)) for k in range(3)}
    assert all(value == 0 for value in residual.values())
    # A differential identity proves the full formal fractional identity,
    # since monic first-order factors have unique formal inverses.
    return {
        "identity": "(D-b-theta)(D-a)=(D-a-theta)(D-b)",
        "theta": "(a-b)'/(a-b)",
        "crossed_product_residuals": {str(k): str(v) for k, v in residual.items()},
        "common_D_coefficient": str(ea[1]),
        "constant_difference_before_theta_substitution": "-(a-b)' + theta*(a-b)",
        "real_periodic_gap_mean_preserved": "Integral(theta)=log|gap(L)|-log|gap(0)|=0",
        "complex_counterexample": "gap=exp(i*x), L=2*pi, theta=i, Integral(theta)=2*pi*i",
    }


def check_generic_matrix():
    output = []
    for m in range(1, 7):
        p = [sp.Integer(1)] + [sp.Function(f"p{n}")(x) for n in range(1, 2 * m + 1)]
        q = [sp.Function(f"q{i}")(x) for i in range(m)] + [sp.Integer(1)]
        a, rhs = finite_system(p, m)
        for rr in range(1, m + 1):
            extracted = qp_coefficient(q, p, -rr)
            proposed = sum(a[rr - 1, i] * q[i] for i in range(m)) - rhs[rr - 1]
            assert sp.expand(extracted - proposed) == 0
        assert max(n for n in range(1, len(p))) == 2 * m
        output.append({"M": m, "all_first_M_negative_coefficients_match": True, "max_p_index": 2 * m})
    return output


def check_uniform():
    output = []
    for m in range(1, 13):
        p = [sp.Integer(1)] + [sp.binomial(m, n) * (-c) ** n if n <= m else sp.Integer(0) for n in range(1, 2 * m + 1)]
        a, rhs = finite_system(p, m)
        determinant = sp.factor(a.det(method="domain-ge"))
        expected = (-1) ** (m * (m - 1) // 2) * (-c) ** (m * m)
        assert sp.expand(determinant - expected) == 0
        assert rhs == sp.zeros(m, 1)
        assert all(a[r - 1, i] == 0 for r in range(1, m + 1) for i in range(m) if r + i > m)
        assert all(a[r - 1, m - r] == (-c) ** m for r in range(1, m + 1))
        if m <= 6:
            assert a.inv() * rhs == sp.zeros(m, 1)
        output.append({
            "M": m,
            "determinant": str(determinant),
            "expected_sign": (-1) ** (m * (m + 1) // 2),
            "antidiagonal": str((-c) ** m),
            "below_antidiagonal_zero": True,
            "recovered_Q": f"D^{m}",
        })
    return output


def check_nonconstant_fractions():
    output = []
    eps, cc = sp.Rational(1, 100), sp.Rational(2, 3)
    for m in range(1, 5):
        q = [eps * (i + 1) * (1 + x) for i in range(m)] + [sp.Integer(1)]
        r = [sp.binomial(m, i) * (-cc) ** (m - i) + eps * (i + 2) * (1 + x**2) for i in range(m)] + [sp.Integer(1)]
        p = fraction_expansion(q, r, 2 * m)
        a, rhs = finite_system(p, m)
        residual = a * sp.Matrix(q[:m]) - rhs
        assert all(sp.expand(v) == 0 for v in residual)
        # Check QP=R at all powers determined by these 2M Laurent coefficients.
        for power in range(-m, m + 1):
            target = r[power] if power >= 0 else 0
            assert sp.expand(qp_coefficient(q, p, power) - target) == 0
        points = []
        for xx in [sp.Integer(0), sp.Rational(1, 3)]:
            ax, bx = a.subs(x, xx), rhs.subs(x, xx)
            det = sp.factor(ax.det())
            assert det != 0
            recovered = ax.inv() * bx
            expected = sp.Matrix([qi.subs(x, xx) for qi in q[:m]])
            assert recovered == expected
            points.append({"x": str(xx), "determinant": str(det), "recovered_q": [str(v) for v in recovered]})
        output.append({
            "M": m,
            "q_i": [str(v) for v in q[:m]],
            "r_i": [str(v) for v in r[:m]],
            "first_2M_Laurent_coefficients": [str(v) for v in p[1:]],
            "QP_equals_R_through_power_minus_M": True,
            "finite_system_polynomial_residual_zero": True,
            "exact_pointwise_recovery": points,
        })
    return output


def check_flags_and_wronskians():
    uniform = []
    lam = sp.Symbol("lambda", real=True)
    for m in range(1, 9):
        nilpotent = sp.zeros(m)
        for j in range(m - 1):
            nilpotent[j, j + 1] = 1
        # Unit-period monodromy after removal of its positive scalar multiplier.
        h = sum((nilpotent**j / sp.factorial(j) for j in range(m)), sp.zeros(m))
        for k in range(1, m + 1):
            polynomial = (h - sp.eye(m)) ** k
            assert polynomial.rank() == m - k
            assert all(polynomial[:, j] == sp.zeros(m, 1) for j in range(k))
        if m <= 6:
            fs = [sp.exp(lam * x) * x**j / sp.factorial(j) for j in range(m)]
            old_w = sp.Integer(1)
            for k in range(1, m + 1):
                w = sp.simplify(sp.wronskian(fs[:k], x))
                assert sp.simplify(w - sp.exp(k * lam * x)) == 0
                recovered = sp.simplify(sp.diff(w, x) / w - sp.diff(old_w, x) / old_w)
                assert recovered == lam
                old_w = w
        uniform.append({"M": m, "all_kernel_dimensions": list(range(1, m + 1)), "uniform_wronskians_checked": m <= 6})
    h = sp.diag(sp.Matrix([[2, 1], [0, 2]]), sp.Matrix([[3]]), sp.Matrix([[5, 1], [0, 5]]))
    marks = [5, 2, 5, 3, 2]
    polynomial = sp.eye(5)
    dimensions = []
    for k, mu in enumerate(marks, start=1):
        polynomial = polynomial * (h - mu * sp.eye(5))
        dimension = len(polynomial.nullspace())
        assert dimension == k
        assert polynomial * h == h * polynomial
        dimensions.append(dimension)
    return {
        "uniform_cyclic_monodromy": uniform,
        "mixed_single_Jordan_blocks": {"ordered_multipliers": marks, "kernel_dimensions": dimensions},
        "unique_marked_flag_formula": "V_k=ker(product_{j=1}^k(H-mu_j I)) for cyclic H",
        "uniform_Wk": "exp(k*lambda*x), basis f_j=exp(lambda*x)*x^(j-1)/(j-1)!",
        "noncyclic_counterexample": "H=I_2: every line is invariant; repeated marks (1,1) do not determine the flag",
        "unmarked_counterexample": "H=diag(2,3): ordering (2,3) and (3,2) gives two different full flags",
    }


def check_finite_data_counterexample():
    eps = sp.Symbol("epsilon", nonzero=True)
    p = [sp.Integer(1), -c, sp.Integer(0), eps]
    a, rhs = finite_system(p, 1)
    assert a == sp.Matrix([[-c]])
    assert rhs == sp.zeros(1, 1)
    q = [sp.Integer(0), sp.Integer(1)]
    first_residual = qp_coefficient(q, p, -1)
    next_residual = qp_coefficient(q, p, -2)
    assert first_residual == 0 and next_residual == eps
    return {
        "P": "1-c*D^-1+epsilon*D^-3 (c,epsilon nonzero constants)",
        "M": 1,
        "finite_system_determinant": "-c",
        "recovered_Q": "D",
        "first_negative_coefficient": str(first_residual),
        "next_negative_coefficient": str(next_residual),
        "conclusion": "Invertible first-M equations do not establish a differential fraction for arbitrary finite data.",
    }


def main():
    result = {
        "status": "all exact finite checks passed",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version": sp.__version__,
        "scope": "Ore differential identities and formal rational coefficients; no inverse spectral or time-flow theorem",
        "factor_exchange": check_exchange(),
        "generic_negative_part_matrix": check_generic_matrix(),
        "uniform_antitriangle": check_uniform(),
        "nonconstant_exact_fractions": check_nonconstant_fractions(),
        "marked_flags_and_wronskians": check_flags_and_wronskians(),
        "finite_data_counterexample": check_finite_data_counterexample(),
        "all_M_proof_basis": [
            "Crossed differential products have equal D^2,D^1,D^0 coefficients.",
            "Leibniz i-l-n=-r gives n=r+i-l, at most 2M.",
            "Uniform p_n=binom(M,n)(-c)^n and zero for n>M; reverse columns gives an upper triangular matrix with diagonal p_M.",
            "If a lower-order left denominator exists, two distinct monic order-M left denominators can be formed, contradicting nonsingular finite system.",
        ],
        "limitations": [
            "Finite generic coefficients need not satisfy all higher negative-part constraints.",
            "Mean preservation uses a real periodic nowhere-zero gap; complex gaps need zero winding.",
            "Invertible finite coefficient recovery alone does not recover ordered physical factors without flag and mean data.",
            "Function-space regularity and analytic/tame estimates require separate arguments.",
        ],
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": result["status"], "sympy_version": sp.__version__, "output": target.name, "uniform_M_range": [1, 12], "generic_M_range": [1, 6], "nonconstant_M_range": [1, 4]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
