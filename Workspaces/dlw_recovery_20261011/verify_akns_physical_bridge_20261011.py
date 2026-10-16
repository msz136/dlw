"""New exact-algebra checks for the AKNS bridge; not a rerun of old certificates.

This checks finite symbolic identities only. It does not certify Banach IFT,
inverse spectral theorems, infinite-dimensional analytic factorization, or
physical nonlinear maximality. Outputs are written next to this script.
"""
from pathlib import Path
import json
import sympy as s

results = []


def check(name, expression):
    entries = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    residuals = [s.simplify(s.expand(e)) for e in entries]
    passed = all(e == 0 for e in residuals)
    results.append({"name": name, "passed": passed})
    if not passed:
        raise AssertionError((name, residuals))


S, u, v, vx, lam, eta = s.symbols("S u v vx lam eta", nonzero=True)
q = -S + u
V = -2*u*v/S
r = ((S**2/4-v**2)*(1+u/S)-vx)/S
H = s.diag(1, -1)
E = s.Matrix([[0, 1], [0, 0]])
F = E.T
split = (lam-V)*H/2+q*E+r*F
T = s.Matrix([[(S/2+v)/S, 1], [(S/2-v)/S, -1]])
Tx = T.diff(v)*vx
original = s.Matrix([
    [u/2+lam*v/S, (S/2+v)*(1+lam/S)],
    [(S/2-v)*(lam/S-1), -u/2-lam*v/S],
])
check("rank_one_to_split_full_connection", Tx*T.inv()+T*split*T.inv()-original)
check("rank_one_frame_determinant", T.det()+1)

t = s.symbols("t", nonzero=True)  # t = exp(theta/2)
G = s.diag(1/t, t)
Gx = s.diag(-(V-eta)/(2*t), (V-eta)*t/2)
gauged = G.inv()*split*G-G.inv()*Gx
target = (lam-eta)*H/2+(t**2*q)*E+(r/t**2)*F
check("periodic_diagonal_gauge_connection", gauged-target)
check("triangular_plus_S", original.subs(lam, S)-((u/2+v)*H+2*(S/2+v)*E))
check("triangular_minus_S", original.subs(lam, -S)-((u/2-v)*H-2*(S/2-v)*F))

d = s.symbols("d")  # formal derivative; formal adjoint d* = -d
Juv = -s.Matrix([[0, d], [d, 0]])/16
Lambda = s.Matrix([[1, 0], [s.Rational(1, 4), -d/S]])
Lambda_star = s.Matrix([[1, s.Rational(1, 4)], [0, d/S]])
Jbg = s.Matrix([[0, -d**2/(16*S)], [d**2/(16*S), 0]])
check("physical_pushforward_background", Lambda*Juv*Lambda_star-Jbg)

abar, bbar, h, k, meanA, meanB, Aosc, Bosc = s.symbols(
    "abar bbar h k meanA meanB Aosc Bosc"
)
tau = -meanA/S
sigma = meanB-meanA/4
k_inv = S*(Aosc/4-Bosc)/d
check("extended_chart_mean_inverse",
      s.Matrix([-S*tau-meanA, -S*tau/4+sigma-meanB]))
check("extended_chart_nonzero_mode_inverse",
      s.Matrix([Aosc-Aosc, Aosc/4-d*k_inv/S-Bosc]))
check("central_width_transverse_derivative",
      4*s.symbols("L")**2*(S*meanA/4-S*meanB)
      +4*S*s.symbols("L")**2*(meanB-meanA/4))

a, b, z, w = s.symbols("a b z w")
m11, m12, m21, m22, n11, n12, n21, n22 = s.symbols(
    "m11 m12 m21 m22 n11 n12 n21 n22"
)
Mz = s.Matrix([[m11, m12], [m21, m22]])
Mw = s.Matrix([[n11, n12], [n21, n22]])
Q = a*E+b*F
Uz = -s.I*z*H+Q
Uw = -s.I*w*H+Q
comm = lambda A, B: A*B-B*A
derivative = s.trace(comm(Uz, Mz)*Mw+Mz*comm(Uw, Mw))
check("canonical_monodromy_cross_identity",
      derivative+2*s.I*(z-w)*(m12*n21-m21*n12))

C = s.Matrix([[1, 1], [s.I, -s.I]])
JD = s.Matrix([[0, 1], [-1, 0]])
Omega = s.Matrix([[s.I*(b-a), a+b], [a+b, s.I*(a-b)]])/2
check("generic_Dirac_exact_operator", -C*s.I*H*Q*C.inv()-Omega)
check("generic_Dirac_principal_similarity", JD*C-C*s.I*H)

out = {
    "scope": "new finite exact identities only",
    "identity_count": len(results),
    "all_passed": all(r["passed"] for r in results),
    "checks": results,
}
destination = Path(__file__).with_name("akns_physical_bridge_symbolic_checks_20261011.json")
destination.write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print(json.dumps(out, ensure_ascii=False))
