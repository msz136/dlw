"""Exact symbolic checks of the reduced physical-flow obstruction."""
import json
from pathlib import Path
import sympy as s

k, h, c, r, u, lam = s.symbols('k h c r u lam', real=True)
beta = h**2/32
A = s.Matrix([[k**2, -s.I*(2*beta*c*k+r*k**2)], [-s.I*c*k, -k**2]])
delta = k**4-c*r*k**3-h**2*c**2*k**2/16
assert s.simplify(A**2-delta*s.eye(2)) == s.zeros(2)
M = A-s.I*u*k*s.eye(2)
assert s.expand((lam*s.eye(2)-M).det()-((lam+s.I*u*k)**2-delta)) == 0
assert s.limit(delta/k**4, k, s.oo) == 1
# Conjugate modes define real fields.
assert s.simplify(s.conjugate(M)-M.subs({k:-k,r:-r}, simultaneous=True)) == s.zeros(2)
# Even N Nyquist mode: R=0, and the instability survives.
assert s.expand(delta.subs(r,0)-k**2*(k**2-h**2*c**2/16)) == 0
# Exact reduced reconstruction m=(gamma-Pi ps)/c has no linear correction.
eps, gam, ps = s.symbols('eps gamma ps')
assert s.diff((gam-eps**2*ps)/c,eps).subs(eps,0) == 0
out={'passed':True,'exact_checks':6,'discriminant':str(delta),
     'conclusion':'No bounded positive-time linearized propagator H^r -> H^(r-d) for finite d; therefore no differentiable local physical flow at the constant equilibrium in that category.',
     'scope':'General proof in THEORY.md. No nonlinear discontinuity or global nonintegrability claim.'}
Path(__file__).with_name('flow_obstruction_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
