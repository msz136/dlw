"""Fresh exact checks for the physical fixed-lambda / AKNS trace bridge."""
import hashlib
import json
from pathlib import Path
import sympy as sp

S, lam, eta, hbar, Rbar = sp.symbols("S lam eta hbar Rbar", nonzero=True)
u, u1, u2, v, v1, v2 = sp.symbols("u u1 u2 v v1 v2")
E, F, h = sp.symbols("E F h")
q = u - S
A = sp.Rational(1, 4) - v*v/(S*S)
B = -2*v*(S+u)/(S*S)
r = A*(S+u) - v1/S
V = -2*u*v/S
hx = q*F - r*E
Ex = (lam-V)*E - 2*q*h
Fx = (V-lam)*F + 2*r*h

jet_rules = {u: u1, u1: u2, v: v1, v1: v2, E: Ex, F: Fx, h: hx}
def D(expr):
    return sp.expand(sum(sp.diff(expr, var)*dvar for var, dvar in jet_rules.items()))

checks = []
def check(name, expr):
    result = sp.cancel(sp.expand(expr))
    assert result == 0, (name, result)
    checks.append(name)

zeta = lam-eta
thetax = V-eta
check("adjoint_E_after_periodic_gauge", (zeta-thetax)*E-2*q*h-Ex)
check("adjoint_F_after_periodic_gauge", (-zeta+thetax)*F+2*r*h-Fx)
gu = F+A*E+2*v*h/S
gv = (lam-2*v)*E/S+2*h
raw_gu = F+A*E+2*v*(h-hbar)/S
raw_gv = B*E+Ex/S+2*u*(h-hbar)/S
check("fixed_lambda_holonomy_cancels_u_zero_mode", raw_gu+2*v*hbar/S-gu)
check("fixed_lambda_holonomy_cancels_v_zero_mode", raw_gv+2*u*hbar/S-gv)
check("r_u_derivative", sp.diff(r, u)-A)
check("r_v_derivative", sp.diff(r, v)-B)
check("r_vx_derivative", sp.diff(r, v1)+1/S)
ut = -D(gv)/16
vt = -D(gu)/16
check("physical_trace_ut_has_no_vx", sp.diff(ut, v1))
check("physical_trace_vt_has_no_vx", sp.diff(vt, v1))
check("physical_trace_ut_has_no_ux", sp.diff(ut, u1))
check("physical_trace_vt_has_no_ux", sp.diff(vt, u1))
R0 = S*F+(lam*v/S-v*v/S-S/4)*E+(2*v-lam)*h
Vt = -2*(v*ut+u*vt)/S
check("Vt_exact_spatial_derivative", Vt-D(R0)/(8*S))
weight = (S*S-lam*lam)/(16*S)
check("AKNS_a_trace_flow_local_part", ut+q*R0/(8*S)-weight*E)
rt = A*ut+B*vt-D(vt)/S
check("AKNS_b_trace_flow_local_part", rt-r*R0/(8*S)+weight*F)
thetat = (R0-Rbar)/(8*S)
check("AKNS_a_complete_constant_gauge", ut+q*thetat-(weight*E-Rbar*q/(8*S)))
check("AKNS_b_complete_constant_gauge", rt-r*thetat-(-weight*F+Rbar*r/(8*S)))

path = Path(__file__).resolve()
out = {
    "purpose": "New independent physical fixed-lambda trace Poisson bridge",
    "checks_passed": len(checks),
    "checks": checks,
    "script_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
}
path.with_suffix(".json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps({"checks_passed": len(checks), "script_sha256": out["script_sha256"]}))
