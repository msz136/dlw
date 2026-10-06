"""Strict rational-interval certificate for the frozen T03 subdomain bound.

No floating-point value participates in certification.  SymPy derives the
rational primitives; Fraction encloses logarithms via a positive atanh series;
integer square roots enclose the final square root.  The only output is the
adjacent quantitative_bound.json file.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path

import sympy as sp


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        assert self.lo <= self.hi

    @staticmethod
    def point(value):
        value = F(value)
        return Interval(value, value)

    def __add__(self, other):
        other = as_interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-as_interval(other))

    def __rsub__(self, other):
        return as_interval(other) - self

    def __mul__(self, other):
        other = as_interval(other)
        values = [self.lo * other.lo, self.lo * other.hi,
                  self.hi * other.lo, self.hi * other.hi]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_interval(other)
        assert not (other.lo <= 0 <= other.hi), "zero in divisor interval"
        return self * Interval(1 / other.hi, 1 / other.lo)

    def square(self):
        upper = max(self.lo * self.lo, self.hi * self.hi)
        lower = 0 if self.lo <= 0 <= self.hi else min(
            self.lo * self.lo, self.hi * self.hi)
        return Interval(F(lower), upper)


def as_interval(value):
    return value if isinstance(value, Interval) else Interval.point(value)


def sympy_fraction(value):
    assert value.is_Rational
    return F(int(value.p), int(value.q))


def rational_text(value):
    return f"{value.numerator}/{value.denominator}"


def decimal_enclosure(value, places=80):
    """Directed decimal rounding by integer division, valid also for negatives."""
    scale = 10 ** places
    lower = value.lo.numerator * scale // value.lo.denominator
    upper = -((-value.hi.numerator * scale) // value.hi.denominator)
    return [scaled_text(lower, places), scaled_text(upper, places)]


def scaled_text(integer, places):
    sign = "-" if integer < 0 else ""
    digits = str(abs(integer)).rjust(places + 1, "0")
    return sign + digits[:-places] + "." + digits[-places:]


def interval_record(value):
    return {
        "lower_rational": rational_text(value.lo),
        "upper_rational": rational_text(value.hi),
        "outward_decimal_80_places": decimal_enclosure(value),
    }


def log_interval(argument, terms=96):
    """For x>1, log x=2 sum t^(2k+1)/(2k+1), t=(x-1)/(x+1).

    The omitted positive tail is at most
    2*t^(2N+1)/((2N+1)*(1-t^2)).  Every quantity is rational.
    """
    argument = F(argument)
    assert argument > 1 and terms >= 1
    t = (argument - 1) / (argument + 1)
    partial = F(0)
    term_power = t
    for k in range(terms):
        partial += 2 * term_power / (2 * k + 1)
        term_power *= t * t
    tail = 2 * term_power / ((2 * terms + 1) * (1 - t * t))
    enclosure = Interval(partial, partial + tail)
    return enclosure, {
        "argument": rational_text(argument),
        "terms": terms,
        "atanh_t": rational_text(t),
        "formula": "log(x)=2*sum(k>=0,t^(2*k+1)/(2*k+1))",
        "tail_upper_formula": "2*t^(2*N+1)/((2*N+1)*(1-t^2))",
        "tail_upper_rational": rational_text(tail),
        "enclosure": interval_record(enclosure),
    }


def sqrt_interval(value, places=90):
    assert value.lo >= 0
    scale = 10 ** places
    lo_integer = isqrt(value.lo.numerator * scale * scale // value.lo.denominator)
    hi_integer = isqrt(value.hi.numerator * scale * scale // value.hi.denominator) + 1
    result = Interval(F(lo_integer, scale), F(hi_integer, scale))
    assert result.lo * result.lo <= value.lo
    assert result.hi * result.hi >= value.hi
    return result


def derive_integrals():
    r = sp.symbols("q", positive=True)
    A = 2 * r / (1 + 2 * r) ** 2 - r / (1 + r) ** 2
    C = 2 * r * (1 - 2 * r) / (1 + 2 * r) ** 3 + r * (1 - r) / (1 + r) ** 3
    assert sp.cancel(A.subs(r, 1 / (2 * r)) + A) == 0
    assert sp.cancel(C.subs(r, 1 / (2 * r)) + C) == 0
    integrands = {"IA": A * A / r, "IC": C * C / r, "IAC": A * C / r}
    log_coefficients = {"IA": -12, "IC": -300, "IAC": 52}
    J = sp.symbols("J")
    exact = {
        "IA": sp.Rational(2397371, 1093500) - 12 * J,
        "IC": sp.Rational(201987058109, 3690562500) - 300 * J,
        "IAC": -sp.Rational(1242427391, 131220000) + 52 * J,
    }
    evidence = {}
    for name, integrand in integrands.items():
        raw = sp.integrate(sp.factor(integrand), r)
        rational_part = raw.xreplace({atom: sp.Integer(0) for atom in raw.atoms(sp.log)})
        primitive = sp.apart(rational_part, r) + log_coefficients[name] * (
            sp.log(2 * r + 1) - sp.log(r + 1))
        derivative_difference = sp.cancel(sp.diff(primitive, r) - integrand)
        assert derivative_difference == 0
        endpoint_value = sp.expand(sp.expand_log(
            primitive.subs(r, 4) - primitive.subs(r, 1), force=True))
        # The positive rational identity log(6/5)=log(2)+log(3)-log(5)
        # avoids asking symbolic simplification to factor integer logarithms.
        expected = sp.expand(exact[name].subs(J, sp.log(2) + sp.log(3) - sp.log(5)))
        assert sp.expand(endpoint_value - expected) == 0
        evidence[name] = {
            "integrand": sp.sstr(sp.factor(integrand)),
            "sympy_raw_primitive": sp.sstr(raw),
            "clean_primitive": sp.sstr(primitive),
            "derivative_difference_exact": "0",
            "endpoint_value_rational_and_logs": sp.sstr(endpoint_value),
            "endpoint_value_using_J": sp.sstr(exact[name]),
            "endpoint_identity_exact": True,
        }
    determinant = sp.expand(exact["IA"] * exact["IC"] - exact["IAC"] ** 2)
    expected_determinant = 896 * J ** 2 - sp.Rational(405694238711, 1230187500) * J + sp.Rational(
        7836839262487208881, 258280326000000000)
    assert determinant == expected_determinant
    return exact, J, evidence, determinant


def main():
    exact, J_symbol, evidence, determinant_exact = derive_integrals()
    log_J, log_evidence = log_interval(F(6, 5))
    intervals = {}
    for name, expression in exact.items():
        constant = sympy_fraction(expression.subs(J_symbol, 0))
        coefficient = sympy_fraction(sp.diff(expression, J_symbol))
        intervals[name] = constant + coefficient * log_J
    IA, IC, IAC = (intervals[name] for name in ("IA", "IC", "IAC"))
    assert IA.lo > 0 and IC.lo > 0 and IAC.lo > 0
    determinant = IA * IC - IAC.square()
    residual = IC - IAC.square() / IA
    assert determinant.lo > 0 and residual.lo > 0
    radicand = residual / 8
    square_root = sqrt_interval(radicand)
    bound = square_root / 32

    # The reported decimal is strictly below an exact certified lower endpoint.
    reported_places = 30
    scale = 10 ** reported_places
    reported_integer = bound.lo.numerator * scale // bound.lo.denominator
    reported_fraction = F(reported_integer, scale)
    if reported_fraction == bound.lo:
        reported_integer -= 1
        reported_fraction = F(reported_integer, scale)
    assert reported_fraction > 0
    assert reported_fraction < bound.lo
    assert 32 ** 2 * reported_fraction ** 2 < radicand.lo

    # Independent rational check of the frozen subdomain and measure factor.
    log_2, log_2_evidence = log_interval(2)
    x_abs_upper = F(1, 2) + F(5, 2) * log_2.hi
    assert x_abs_upper < 8
    K, ell, gamma2 = F(1), F(-1, 2), F(3, 32)
    odd_C_coefficient = K * ell * ell / 8
    measure_factor = F(2 * 2, 32) / K
    assert odd_C_coefficient == F(1, 32)
    assert measure_factor == F(1, 8)
    domain_evidence = {
        "z": "x-y/2-log(2)/2",
        "positive_half": "0<=z<=log(4), -1<=y<=1",
        "other_half": "reflection (x,y)->(-x,-y); z->-z-log(2)",
        "positive_half_x_range": "[log(2)/2-1/2, (5/2)*log(2)+1/2]",
        "two_halves_disjoint_up_to_null_boundaries": True,
        "reflection_A_and_C_exactly_odd": True,
        "x_absolute_upper_rational": rational_text(x_abs_upper),
        "x_absolute_upper_strictly_less_than_8_exact": True,
        "y_containment": "[-1,1]",
        "D_subset_Omega": True,
        "dx_dz": "1/K=1",
        "two_halves_times_y_length_over_Omega_area": "2*2/32=1/8",
        "RMS_integrals_on_D": "<A,A>_D=IA/8, <C,C>_D=IC/8, <A,C>_D=IAC/8",
        "odd_Bu": "(3*A-C)/32",
        "odd_C_coefficient": rational_text(odd_C_coefficient),
        "measure_factor": rational_text(measure_factor),
        "log_2_certificate": log_2_evidence,
    }
    script = Path(__file__).resolve()
    output = {
        "date": "2026-10-01",
        "status": "strict_lower_bound_certified",
        "comparison": "d_theta >= d_u > reported_strict_lower_bound",
        "parameters": {"a": "0", "p": "2", "q": "-1", "phi": "-log(2)/2", "t": "0"},
        "Omega": "[-8,8] x [-1,1]",
        "norm": "RMS: integral divided by |Omega|=32; two physical fields equally weighted",
        "bound_formula": "(1/32)*sqrt((IC-IAC^2/IA)/8)",
        "J_definition": "log(6/5)",
        "exact_integral_evidence": evidence,
        "exact_determinant_using_J": sp.sstr(determinant_exact),
        "log_certificate": log_evidence,
        "intervals": {**{name: interval_record(value) for name, value in intervals.items()},
                      "determinant_IA_IC_minus_IAC_squared": interval_record(determinant),
                      "residual_IC_minus_IAC_squared_over_IA": interval_record(residual),
                      "radicand_residual_over_8": interval_record(radicand),
                      "sqrt_radicand": interval_record(square_root),
                      "subdomain_lower_bound_expression": interval_record(bound)},
        "reported_strict_lower_bound": scaled_text(reported_integer, reported_places),
        "reported_bound_rational": rational_text(reported_fraction),
        "reported_bound_strict_squared_inequality_exact": True,
        "square_root_method": "integer isqrt on exact scaled Fraction; 90 decimal places, outward enclosure",
        "arithmetic": "all certificate arithmetic uses exact Python Fraction integers; no binary or high-precision float certificate",
        "domain_and_coefficient_evidence": domain_evidence,
        "sympy_version": sp.__version__,
        "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "PDE_evolutions": 0,
        "parameter_scans": 0,
    }
    script.with_suffix(".json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": output["status"],
                      "reported_strict_lower_bound": output["reported_strict_lower_bound"],
                      "bound_outward_decimal": decimal_enclosure(bound, 55),
                      "determinant_outward_decimal": decimal_enclosure(determinant, 55),
                      "output": str(script.with_suffix(".json"))}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
