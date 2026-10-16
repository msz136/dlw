"""New exact M2 nonlinear spectral-kernel checks. No previous scripts run."""
import hashlib
import json
from pathlib import Path
import sympy as sp

x = sp.symbols("x", real=True)
h, c, S, k, lam = sp.symbols("h c S k lam", nonzero=True, real=True)
u, v = sp.Function("u")(x), sp.Function("v")(x)
D = lambda f: sp.diff(f, x)
checks = []

def check(name, expr):
    assert sp.simplify(expr) == 0, (name, expr)
    checks.append(name)

ut = -D(D(u)) - 2*S*D(v) + 2*D(u*u*v)/S
vt = D(D(v)) - S*D(u)/2 + 2*D(u*v*v)/S
b = -2*u*v/S
s = 8*v/h
U0, U1 = b+u, b-u
w0, w1 = c+s, c-s
check("pointwise_physical_flux_zero",
      ((U0*w0+U1*w1)/2).subs(S,h*c/4))
beta = h*h/32
derived_ut = -D(D(u))-D((U0*U0-U1*U1)/4+beta*(w0*w0-w1*w1)/2)
check("original_projected_u_equation", (derived_ut-ut).subs(S,h*c/4))
derived_vt = h*(-D(U0*w0-U1*w1)/2+D(D(s)))/8
check("original_projected_v_equation", (derived_vt-vt).subs(S,h*c/4))
Gu = -16*D(v)+8*S*u-32*u*v*v/S
Gv = 16*D(u)+32*S*v-32*u*u*v/S
check("Hamilton_u", -D(Gv)/16-ut)
check("Hamilton_v", -D(Gu)/16-vt)
q = -S+u
r = ((S*S/4-v*v)*(1+u/S)-D(v))/S
Kd = 16*v*D(u)+4*S*u*u+16*S*v*v-16*u*u*v*v/S
check("C1_Hamilton_exact_total_derivative",
      Kd-16*S*q*r-4*S**3-16*D(u*v-S*v))
check("momentum_exact_total_derivative",
      ut*v+u*vt-D(-D(u)*v+u*D(v)-S*v*v-S*u*u/4+3*u*u*v*v/S))
A = sp.Matrix([[k*k,-2*sp.I*S*k],[-sp.I*S*k/2,-k*k]])
check("Fourier_dichotomy_scalar_11", (A*A)[0,0]-(k**4-S*S*k*k))
check("Fourier_dichotomy_scalar_22", (A*A)[1,1]-(k**4-S*S*k*k))
check("Fourier_dichotomy_offdiag_12", (A*A)[0,1])
check("Fourier_dichotomy_offdiag_21", (A*A)[1,0])
L0 = sp.Matrix([[0,(S+lam)/2],[(lam-S)/2,0]])
check("normalized_uniform_connection_square_11",
      (L0*L0)[0,0]-(lam*lam-S*S)/4)
check("normalized_uniform_connection_square_22",
      (L0*L0)[1,1]-(lam*lam-S*S)/4)
# sl2 conjugacy inversion: [G,B]=Z on tr(BZ)=0.
a0, b0, d0, p0, q0, r0 = sp.symbols("a0 b0 d0 p0 q0 r0")
B = sp.Matrix([[a0,b0],[d0,-a0]])
Z = sp.Matrix([[p0,q0],[r0,-p0]])
Delta = 4*(a0*a0+b0*d0)
G = -(B*Z-Z*B)/Delta
res = sp.simplify(G*B-B*G-Z)
# Exact identity equals the invariant component removed.
for i,j in [(0,0),(0,1),(1,0),(1,1)]:
    check(f"sl2_conjugacy_inverse_{i}{j}",
          res[i,j]+2*sp.trace(B*Z)*B[i,j]/Delta)

here = Path(__file__)
result = {
    "status": "all new M2 nonlinear kernel exact checks passed",
    "check_count": len(checks),
    "checks": checks,
    "script_sha256": hashlib.sha256(here.read_bytes()).hexdigest(),
    "sympy_version": sp.__version__,
    "previous_certificate_scripts_rerun": False,
    "not_proved_by_script": [
        "half-line nonlinear contraction and all-order persistence",
        "finite regular spectral quotient theorem",
        "infinite open-gap Hamiltonian gradient completeness",
        "strong coherent isospectral-fiber tangent equality"
    ]
}
here.with_suffix(".json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
