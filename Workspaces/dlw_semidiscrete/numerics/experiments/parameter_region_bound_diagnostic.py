"""Check the analytic initial velocity sensitivity and scale of coarse bounds.

The finite differences and point residuals here are diagnostics, not interval
enclosures over time or parameter boxes. No holdout parameters are used.
"""

from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import math
import sys

import numpy as np
from scipy.special import expit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
from parametric import Parameters
from parametric_open import OpenModel

H = 0.125
L = 40.0
T = 0.01
CENTER = dict(S=3.0, g=3.0, nu=0.0, x_c=0.0)


def model(nx, nu=0.0):
    S, g, x_c = CENTER["S"], CENTER["g"], CENTER["x_c"]
    p, q = S * (1 + nu) / 2, S * (1 - nu) / 2
    pars = Parameters(a=g + p, p=p, q=q, rho=S * math.exp(-S * x_c))
    return OpenModel(pars, H, nx, L=L, yhalf=1.5, model="structure")


def exact_x_derivative(m):
    """Analytic x derivative of the finite-h Gram (P,W) initial state."""
    S = CENTER["S"]
    x = m.X.x[None, :]
    j = m.js[:, None]
    z = S * (x - CENTER["x_c"]) + j * m.G.chi
    slope = lambda w: expit(w) * expit(-w)
    ux = S * S * (2 * slope(z + m.G.gamma) - slope(z)
                    - slope(z + m.G.chi))
    wx = 4 * S * S / H * (slope(z + m.G.chi) - slope(z))
    return m.pack(np.diff(ux, axis=0) / H, wx)


def coarse_constant(nx):
    # PARAMETRIC_THEORY.md sections 7-8, whole design domain, extrapolated y.
    ell = (round(3 / H) - 1) * H
    dh = 1 / (0.5 - H / 2) + 1 / (2 - H / 2)
    B = Q = 5 * dh
    b = 22.0
    d = 1.5 / (L / nx)
    kp = d * (b + B * ell + H * (Q / 8 + 0.5)) + 4 * d * d
    kw = d * (b + (Q + 4) * ell) + d * d
    return max(kp, kw), max(ell / 1.5, 0.75)


def main():
    rows = []
    for nx in (64, 128, 256, 512):
        m = model(nx)
        z = m.exact(0)
        r = m.rhs(0, z) - m.exact(0, True)
        zx = exact_x_derivative(m)
        p, w = m.unpack(z)
        d1z = m.pack(m.X.d1(p), m.X.d1(w))
        analytic = CENTER["S"] * (zx - d1z)
        delta = 1e-4
        mp, mm = model(nx, delta), model(nx, -delta)
        rp = mp.rhs(0, mp.exact(0)) - mp.exact(0, True)
        rm = mm.rhs(0, mm.exact(0)) - mm.exact(0, True)
        secant = (rp - rm) / (2 * delta)
        k, output_factor = coarse_constant(nx)
        r0 = float(np.max(np.abs(r)))
        # This is the maximum *hypothetical uniform* residual bound allowed by
        # the scalar Gronwall formula at T, not an enclosure of the residual.
        allowed = 1e-3 * k / (output_factor * math.expm1(k * T))
        time_ceiling = math.log1p(1e-3 * k / (output_factor * r0)) / k
        rows.append(dict(nx=nx, K_global=k, exp_KT=math.exp(k * T),
                         initial_state_residual=r0,
                         initial_velocity_sensitivity=float(np.max(np.abs(analytic))),
                         velocity_identity_secant_gap=float(np.max(np.abs(secant - analytic))),
                         residual_cap_for_1e_minus_3_at_T=allowed,
                         cap_to_initial_residual_ratio=allowed / r0,
                         optimistic_time_ceiling_from_initial_residual=time_ceiling))
    data = dict(scope="rows diagnose a continuous-time semidiscrete ODE bound; separate real-arithmetic RK4 one-step proof below",
                identity="partial_nu r(0) = S*(partial_x-D1) Zbar(0)",
                center=CENTER, h=H, L=L, T=T,
                method="finite-h Gram, SD, quadratic extrapolated y ghost",
                rows=rows,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    # Arithmetic ledger for the separate, analytic, real-arithmetic RK4 proof
    # in PARAMETER_REGION_ERROR_REPORT.md section 9. The proof establishes the
    # inequalities; evaluating them here is a reproducibility check.
    tau = F(7, 10**9)
    h = F(1, 8)
    d = F(96, 5)
    ell = F(23, 8)
    p_max = F(1401, 100)
    dh = 1 / (F(1, 2) - h / 2) + 1 / (F(2) - h / 2)
    h_flux = F(1, 2) * 10**2 + 12 * 10 + h**2 * (p_max**2 / 32 + p_max / 4)
    f_p = 2 * d / h * h_flux + d**2 * (3 * p_max)
    f_w = d * (22 * p_max + 40) + d**2 * p_max
    kp = d * (22 + p_max * ell + h * (p_max / 8 + F(1, 2))) + 4 * d**2
    kw = d * (22 + (p_max + 4) * ell) + d**2
    c = d * ell + d * h / 16
    output_factor = ell / F(3, 2)
    assert 5 * dh < p_max
    assert h_flux < F(170151, 1000) and f_p < 68000 and f_w < 68000
    assert max(kp, kw) < 2700 and c < 56
    assert 68000 + 2700 * F(1, 1000) + 56 * F(1, 10**6) < 69000
    assert tau * (69000 + 1000) < F(1, 1000)
    assert output_factor * 70000 * tau < F(1, 1000)
    data["theoretical_one_step_certificate"] = dict(
        scope="real-arithmetic one-step RK4; whole design domain; h=1/8, nx=512, Lx=40",
        tau=float(tau), H_flux_bound=float(h_flux), F_P_bound=float(f_p), F_W_bound=float(f_w),
        K_bound=2700, C_bound=56, reference_time_derivative_bound=1000,
        stage_rhs_bound=69000, stage_tube_radius=1e-3,
        state_error_bound=float(70000 * tau),
        normalized_field_error_bound=float(output_factor * 70000 * tau),
        proof="PARAMETER_REGION_ERROR_REPORT.md section 9; certificate inequalities checked with exact rational arithmetic, analytic sigmoid bounds proved in report; does not enclose floating-point solver roundoff")
    out = ROOT / "design" / "parameter_region_bound_diagnostic.json"
    out.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    for row in rows:
        print(row)
    print(out)


if __name__ == "__main__":
    main()
