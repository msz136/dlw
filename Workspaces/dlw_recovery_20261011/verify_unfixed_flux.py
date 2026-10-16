"""Exact independent checks for unfixed-flux identities; no PDE run."""
from pathlib import Path
import hashlib
import json
import sympy as S

checks = []
def certify(name, expression):
    residual = S.factor(expression)
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append({"name": name, "residual": "0"})

c, gamma, z, f = S.symbols("c gamma z f", nonzero=True)
b = (gamma-z)/c
certify("mean_Hamilton_density", c*b*b/2+b*z-gamma*b+(gamma-z)**2/(2*c))
certify("Hamilton_flux_split", -(gamma-z)**2/(2*c)+z*z/(2*c)-gamma*z/c+gamma*gamma/(2*c))

# General M: substitute arbitrary p,s with lattice zero averages.
for M in range(2, 7):
    pv = list(S.symbols(f"p0:{M-1}"))
    sv = list(S.symbols(f"s0:{M-1}"))
    pv.append(-sum(pv))
    sv.append(-sum(sv))
    zm = sum(p*s for p,s in zip(pv,sv))/M
    bm = (gamma-zm)/c
    full = sum((bm+p)**2*(c+s)/2-gamma*(bm+p) for p,s in zip(pv,sv))/M
    reduced = sum(p*p*(c+s)/2 for p,s in zip(pv,sv))/M-(gamma-zm)**2/(2*c)
    certify(f"full_mean_reduction_M{M}", full-reduced)

center = S.symbols("A1:10")
original = {}
for n in range(1, 10):
    original[n] = sum(S.binomial(n-1,r-1)*f**(n-r)*center[r-1] for r in range(1,n+1))
    recovered = sum(S.binomial(n-1,r-1)*(-f)**(n-r)*original[r] for r in range(1,n+1))
    certify(f"trace_binomial_inverse_n{n}", recovered-center[n-1])
    expected = (n-1)*original[n-1] if n>1 else 0
    certify(f"unfixed_trace_drift_n{n}", S.diff(original[n],f)-expected)

# Independent PDO residue calculation at constant symbolic coefficients:
# res of a Laurent symbol equals its D^-1 coefficient. Shifting D->D-f
# implements e^(fx) A e^(-fx). This verifies the triangular identity using
# operator powers, rather than only its binomial coefficients.
t = S.symbols("t")
ell = S.symbols("l1:8")
symbol0 = 1/t + sum(ell[r-1]*t**r for r in range(1,8))
shifted = S.series(symbol0.subs(t,t/(1-f*t))+f,t,0,8).removeO()
for n in range(1,6):
    centered_res = S.expand(S.series((shifted-f)**n,t,0,2).removeO()).coeff(t,1)
    original_res = S.expand(symbol0**n).coeff(t,1)
    certify(f"quasiperiodic_conjugacy_residue_n{n}",centered_res-original_res)

output = {
    "status": "PASS", "checks": checks,
    "count": len(checks), "method": "exact SymPy rational/polynomial identities",
    "scope": "finite checks supplement the all-M/all-order written proof; not spectral completeness",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
Path(__file__).with_name("unfixed_flux_checks.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":output["status"],"count":output["count"]}))
