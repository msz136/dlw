"""T03 independent exact algebra checks; no PDE runs or parameter scans.

The physical-field jets are expanded directly at all shifted tau arguments,
without using the continuum-plus-central-difference derivation in THEORY.md.
All comparisons use exact SymPy expressions; no floating-point zero tests.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path
import sys
import time

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
THEORY = HERE / "THEORY.md"
OUTPUT = HERE / "symbolic_validation.json"
SOURCES = [
    THEORY,
    ROOT / "Workspaces/dlw_semidiscrete/NONLINEAR_CLOSURE.md",
    ROOT / "Workspaces/dlw_semidiscrete/ALTERNATIVE_DISCRETIZATIONS.md",
    ROOT / "Workspaces/dlw_semidiscrete/numerics/MANIFOLD_SCATTERING_REPORT.md",
    ROOT / "Workspaces/dlw_factor_model_20260930/REPORT.md",
    ROOT / "Workspaces/dlw_h2_bounds_20260930/REPORT.md",
    ROOT / "Workspaces/dlw_semidiscrete/numerics/lib/dynamics.py",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


source_hashes = {str(path.relative_to(ROOT)): sha256(path) for path in SOURCES}
checks: list[dict] = []
started = time.perf_counter()


def normalized(expr):
    return sp.cancel(sp.together(expr))


def exact(name: str, residuals: dict, detail: str, values: dict | None = None):
    reduced = {key: normalized(value) for key, value in residuals.items()}
    passed = all(value == 0 for value in reduced.values())
    result = {
        "name": name,
        "passed": passed,
        "criterion": "Every exact symbolic residual is identically zero.",
        "detail": detail,
        "residuals": {key: str(value) for key, value in reduced.items()},
    }
    if values:
        result["exact_values"] = {key: str(value) for key, value in values.items()}
    checks.append(result)
    print(f"{name}: {'passed' if passed else 'FAILED'}", flush=True)
    if not passed:
        raise AssertionError(f"{name}: {reduced}")


h, P, Q, K, ell, c3, gam2, y = sp.symbols("h P Q K ell c3 gam2 y", nonzero=True)
E, G = sp.symbols("E Gamma", nonzero=True)
x, t, a, p, q = sp.symbols("x t a p q", real=True)
xi = sp.symbols("xi", real=True)
half = sp.Rational(1, 2)
d = h / 2
chi = (P + d) * (Q + d) / ((P - d) * (Q - d))
gamma = -(P + d) / (Q - d)
Gamma = -P / Q
L = 1 / P + 1 / Q
C3 = (P**-3 + Q**-3) / 12
GAM2 = (Q**-2 - P**-2) / 8


def dz(expr):
    """Derivative with respect to z at E=exp(z)."""
    return normalized(E * sp.diff(expr, E))


s = E / (1 + E)
f = G * E / (1 + G * E)
s1, f1 = dz(s), dz(f)
s2, f2 = dz(s1), dz(f1)
s3, f3 = dz(s2), dz(f2)
BU = 2 * K * y * c3 * (f1 - s1) + 2 * K * gam2 * f1 - K * ell**2 * s2 / 4
BV = (
    2 * K * c3 * (f1 + s1)
    + 2 * K * ell * y * c3 * (f2 + s2)
    + 2 * K * ell * gam2 * f2
    + K * ell**3 * (4 * f3 - 5 * s3) / 12
)

try:
    exact(
        "01_branch_algebra",
        {"ell_equals_K_over_PQ": (L - (P + Q) / (P * Q)),
         "Gamma_minus_one": Gamma - 1 + (P + Q) / Q},
        "K>0 and Gamma>0 imply PQ<0, ell<0 and Gamma!=1 by these exact identities.",
    )

    logchi = (
        sp.log(1 + h / (2 * P)) - sp.log(1 - h / (2 * P))
        + sp.log(1 + h / (2 * Q)) - sp.log(1 - h / (2 * Q))
    )
    lambda_jet = sp.series(logchi, h, 0, 7).removeO() / h
    C5 = (P**-5 + Q**-5) / 80
    exact(
        "02_lambda_series",
        {"through_h4": lambda_jet - (L + h**2 * C3 + h**4 * C5)},
        "Independent logarithm Taylor series through h^5 before dividing by h.",
        {"ell": L, "c3": C3, "c5": C5},
    )

    ratio = (1 - h**2 / (4 * P**2)) / (1 - h**2 / (4 * Q**2))
    exact(
        "03_epsilon_exact_log_identity",
        {"exp_twice_epsilon": gamma**2 / (Gamma**2 * chi) - ratio},
        "The rational squared identity yields the real logarithm identity on the positive regular branch.",
    )

    epsilon = (sp.log(1 - h**2 / (4 * P**2)) - sp.log(1 - h**2 / (4 * Q**2))) / 2
    epsilon_jet = sp.series(epsilon, h, 0, 6).removeO()
    GAM4 = (Q**-4 - P**-4) / 64
    exact(
        "04_epsilon_series",
        {"through_h4": epsilon_jet - h**2 * GAM2 - h**4 * GAM4},
        "Independent Taylor series of the centered F phase correction.",
        {"gamma2": GAM2, "gamma4": GAM4},
    )

    R, H = sp.symbols("R H", nonzero=True)  # R=e^delta, H=Gamma e^epsilon.
    tauF, tauM, tauP = 1 + H * E, 1 + E / R, 1 + R * E
    ux_from_tau = K * E * (2 * sp.diff(tauF, E) / tauF
                          - sp.diff(tauM, E) / tauM - sp.diff(tauP, E) / tauP)
    ux_sigmoid = K * (2 * H * E / (1 + H * E)
                     - (E / R) / (1 + E / R) - R * E / (1 + R * E))
    wx_from_tau = 4 * K * E / h * (sp.diff(tauP, E) / tauP - sp.diff(tauM, E) / tauM)
    wx_sigmoid = 4 * K / h * (R * E / (1 + R * E) - (E / R) / (1 + E / R))
    exact(
        "05_exact_physical_reconstruction",
        {"u_log_derivative": ux_from_tau - ux_sigmoid,
         "W_log_derivative": wx_from_tau - wx_sigmoid},
        "Direct tau logarithmic x derivatives with E_x=K E, at the F midpoint.",
    )

    # Independent formal jets at every argument of the exact shifted formulas.
    Sj = sp.symbols("s0:4")
    Fj = sp.symbols("f0:4")

    def jet(coefficients, shift):
        return sp.Poly(sp.expand(sum(coefficients[n] * shift**n / sp.factorial(n)
                                     for n in range(4))), h).as_dict()

    def jet_poly(coefficients, shift):
        entries = jet(coefficients, shift)
        return sp.expand(sum(value * h**power[0] for power, value in entries.items()
                             if power[0] <= 3))

    delta_jet = ell * h / 2 + c3 * h**3 / 2

    def midpoint_u_jet(offset):
        common = y * c3 * h**2 + offset * ell * h + offset * c3 * h**3
        return K * (2 * jet_poly(Fj, common + gam2 * h**2)
                    - jet_poly(Sj, common - delta_jet)
                    - jet_poly(Sj, common + delta_jet))

    ujet = sp.expand(midpoint_u_jet(0))
    predicted_bu_jet = 2 * K * y * c3 * (Fj[1] - Sj[1]) + 2 * K * gam2 * Fj[1] - K * ell**2 * Sj[2] / 4
    exact(
        "06_Bu_direct_shift_jets",
        {"h0": ujet.coeff(h, 0) - 2 * K * (Fj[0] - Sj[0]),
         "h1": ujet.coeff(h, 1),
         "h2": ujet.coeff(h, 2) - predicted_bu_jet,
         "h3": ujet.coeff(h, 3)},
        "Expand F and both G sigmoid jets at their three actual centered arguments.",
    )

    wjet = 4 * K / h * (jet_poly(Sj, y * c3 * h**2 + delta_jet)
                        - jet_poly(Sj, y * c3 * h**2 - delta_jet))
    vjet = sp.expand(wjet + (midpoint_u_jet(1) - midpoint_u_jet(-1)) / (2 * h))
    predicted_bv_jet = (
        2 * K * c3 * (Fj[1] + Sj[1]) + 2 * K * ell * y * c3 * (Fj[2] + Sj[2])
        + 2 * K * ell * gam2 * Fj[2] + K * ell**3 * (4 * Fj[3] - 5 * Sj[3]) / 12
    )
    exact(
        "07_Bv_direct_shift_jets",
        {"h0": vjet.coeff(h, 0) - 2 * K * ell * (Fj[1] + Sj[1]),
         "h1": vjet.coeff(h, 1),
         "h2": vjet.coeff(h, 2) - predicted_bv_jet},
        "Expand the exact v formula directly, including u(y+h) and u(y-h), to numerator order h^3.",
    )

    # P,Q are independent coordinates because a is fixed. This is exactly
    # partial_p=partial_P and partial_q=partial_Q, without expanded shifts
    # in the rational denominators.
    subs_spectra = {K: P + Q, ell: L, G: Gamma}
    U0 = (2 * K * (f - s)).subs(subs_spectra)
    V0 = (2 * K * ell * (f1 + s1)).subs(subs_spectra)
    z_p = x - y / P**2 - 2 * (P + a) * t
    z_q = x - y / Q**2 + 2 * (Q - a) * t
    TU = [
        (2 * (f - s) + 2 * K * ((f1 - s1) * z_p + f1 / P)).subs(subs_spectra),
        (2 * (f - s) + 2 * K * ((f1 - s1) * z_q - f1 / Q)).subs(subs_spectra),
        (2 * K * (f1 - s1)).subs(subs_spectra),
    ]
    TV = [
        (2 * (ell - K / P**2) * (f1 + s1)
         + 2 * K * ell * ((f2 + s2) * z_p + f2 / P)).subs(subs_spectra),
        (2 * (ell - K / Q**2) * (f1 + s1)
         + 2 * K * ell * ((f2 + s2) * z_q - f2 / Q)).subs(subs_spectra),
        (2 * K * ell * (f2 + s2)).subs(subs_spectra),
    ]

    def physical_derivatives(expr):
        return [sp.diff(expr, P) + E * z_p * sp.diff(expr, E),
                sp.diff(expr, Q) + E * z_q * sp.diff(expr, E),
                E * sp.diff(expr, E)]

    exact("08_full_u_tangents", dict(zip(["p", "q", "phi"],
          [left - right for left, right in zip(TU, physical_derivatives(U0))])),
          "Differentiate the rational continuous field directly, including the E=e^z chain rule.")
    exact("09_full_v_tangents", dict(zip(["p", "q", "phi"],
          [left - right for left, right in zip(TV, physical_derivatives(V0))])),
          "Differentiate all amplitude, ell, Gamma and phase dependencies of v0 directly.")

    v_exact = wx_sigmoid + (ux_sigmoid.subs(E, E * R**2) - ux_sigmoid.subs(E, E / R**2)) / (2 * h)
    exact(
        "10_exact_even_parity",
        {"u": ux_sigmoid.subs(R, 1 / R) - ux_sigmoid,
         "v": v_exact.subs({R: 1 / R, h: -h}, simultaneous=True) - v_exact,
         "chi_inverts": chi.subs(h, -h) * chi - 1,
         "lambda_even": logchi.subs(h, -h) + logchi,
         "epsilon_even": epsilon.subs(h, -h) - epsilon},
        "h reversal exchanges the two G arguments; centered H remains even by the exact epsilon identity.",
    )

    # Exact rational Laurent coefficients; E=-exp(xi) at an s pole.
    laurent_s = sp.series(s.subs(E, -sp.exp(xi)), xi, 0, 4).removeO()
    coef_s2 = sp.limit(xi**3 * s2.subs(E, -sp.exp(xi)), xi, 0)
    coef_s3 = sp.limit(xi**4 * s3.subs(E, -sp.exp(xi)), xi, 0)
    exact(
        "11_logistic_Laurent_coefficients",
        {"series": laurent_s - (1 / xi + half + xi / 12 - xi**3 / 720),
         "s_second_derivative": coef_s2 - 2,
         "s_third_derivative": coef_s3 + 6},
        "Laurent coefficients are evaluated by exact series and symbolic limits, not complex sampling.",
    )

    bu_cubic = -K * ell**2 * coef_s2 / 4
    bv_s_quartic = -5 * K * ell**3 * coef_s3 / 12
    bv_f_quartic = 4 * K * ell**3 * coef_s3 / 12
    exact(
        "12_irremovable_pole_coefficients",
        {"Bu_at_s": bu_cubic + K * ell**2 / 2,
         "Bv_at_s": bv_s_quartic - sp.Rational(5, 2) * K * ell**3,
         "Bv_at_f": bv_f_quartic + 2 * K * ell**3},
        "Gamma!=1 makes f regular at an s pole and s regular at an f pole.",
        {"Bu_cubic": bu_cubic, "Bv_s_quartic": bv_s_quartic, "Bv_f_quartic": bv_f_quartic},
    )

    dk, dl, dg, zz = sp.symbols("dK dell dg dz")
    generic_tu = 2 * dk * (f - s) + 2 * K * ((f1 - s1) * zz + f1 * dg)
    generic_tv = 2 * (dk * ell + K * dl) * (f1 + s1) + 2 * K * ell * ((f2 + s2) * zz + f2 * dg)
    tu_cleared = normalized(generic_tu * (1 + E)**2 * (1 + G * E)**2)
    tv_cleared = normalized(generic_tv * (1 + E)**3 * (1 + G * E)**3)
    # Polynomiality is checked exactly, and a reconstruction equality guards the multipliers.
    assert tu_cleared.is_polynomial(E) and tv_cleared.is_polynomial(E)
    exact(
        "13_tangent_pole_order_and_rank_identity",
        {"u_denominator_clearing": tu_cleared / ((1 + E)**2 * (1 + G * E)**2) - generic_tu,
         "v_denominator_clearing": tv_cleared / ((1 + E)**3 * (1 + G * E)**3) - generic_tv,
         "delta_g_at_delta_K_zero": sp.diff(Gamma, P) / Gamma - sp.diff(Gamma, Q) / Gamma - L},
        "Cleared u/v tangents are polynomials in E, so pole orders are at most 2/3. With delta_q=-delta_p, delta_g=ell delta_p.",
        {"u_pole_order_upper_bound": 2, "v_pole_order_upper_bound": 3},
    )

    exact(
        "14_finite_h_collision_identities",
        {"chi_minus_one": chi - 1 - h * (P + Q) / ((P - d) * (Q - d)),
         "gamma_minus_one": gamma - 1 + (P + Q) / (Q - d),
         "gamma_minus_chi": gamma - chi + (P + Q) * (P + d) / ((P - d) * (Q - d))},
        "On the regular branch all denominators and P+d are nonzero; every possible pole-family collision forces K=0.",
    )

    def x_residue(expr, pole_E):
        # dE/dx=K E; convert a rational E residue into the x residue.
        return sp.cancel(sp.limit((E - pole_E) * expr, E, pole_E) / (K * pole_E))

    finite_residues = [x_residue(ux_sigmoid, -1 / H),
                       x_residue(ux_sigmoid, -R), x_residue(ux_sigmoid, -1 / R)]
    continuous_residues = [x_residue(2 * K * (f - s), -1 / G),
                           x_residue(2 * K * (f - s), -1)]
    exact(
        "15_finite_and_continuous_x_residues",
        {"finite_F": finite_residues[0] - 2,
         "finite_Gminus": finite_residues[1] + 1,
         "finite_Gplus": finite_residues[2] + 1,
         "continuous_F": continuous_residues[0] - 2,
         "continuous_G": continuous_residues[1] + 2},
        "Symbolic x-residues at distinct finite-h pole families and their continuous counterparts.",
        {"finite_h": finite_residues, "continuous": continuous_residues},
    )

    frozen = {P: sp.Integer(2), Q: sp.Integer(-1)}
    frozen_values = {"K": (P + Q).subs(frozen), "ell": L.subs(frozen),
                     "Gamma": Gamma.subs(frozen), "c3": C3.subs(frozen), "gamma2": GAM2.subs(frozen)}
    exact(
        "16_frozen_rational_point",
        {"K": frozen_values["K"] - 1, "ell": frozen_values["ell"] + sp.Rational(1, 2),
         "Gamma": frozen_values["Gamma"] - 2, "c3": frozen_values["c3"] + sp.Rational(7, 96),
         "gamma2": frozen_values["gamma2"] - sp.Rational(3, 32),
         "centered_phase": -sp.log(2) / 2 + sp.log(frozen_values["Gamma"]) / 2},
        "Evaluate only the single rational spectral point frozen in THEORY.md §9.",
        frozen_values,
    )

    after_hashes = {str(path.relative_to(ROOT)): sha256(path) for path in SOURCES}
    if source_hashes != after_hashes:
        raise AssertionError("A hashed theory/source file changed during verification.")
    status = "passed"
    failure = None
except Exception as exc:
    status = "failed"
    failure = f"{type(exc).__name__}: {exc}"

record = {
    "scope": "Independent exact symbolic algebra for frozen T03 N=1 theory; no approximate-zero tests, PDE evolution, fitting or scans.",
    "status": status,
    "checks_count": len(checks),
    "passed_count": sum(item["passed"] for item in checks),
    "failure": failure,
    "theory_version": "THEORY.md frozen 2026-10-01 version 1",
    "python": platform.python_version(),
    "sympy": sp.__version__,
    "script_sha256": sha256(Path(__file__)),
    "source_sha256": source_hashes,
    "elapsed_seconds": round(time.perf_counter() - started, 6),
    "checks": checks,
    "proof_limits": [
        "The regular real branch and analytic identity theorem are mathematical hypotheses/proofs, not inferred from CAS outputs.",
        "Polynomial denominator clearing proves pole-order bounds; parameter factors affine in complex x do not add poles.",
        "These checks verify formulas; they do not replace the functional analytic local-distance proof or certify a decimal integral.",
        "The static family obstruction is not a common-initial-data evolution-error lower bound.",
    ],
}
OUTPUT.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": status, "checks": len(checks), "passed": record["passed_count"],
                  "failure": failure, "output": str(OUTPUT)}, ensure_ascii=False))
sys.exit(0 if status == "passed" else 1)
