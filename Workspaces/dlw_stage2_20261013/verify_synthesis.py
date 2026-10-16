"""Independent exact checks for the reduction-to-error synthesis."""
from pathlib import Path
import json
import sympy as s

p, z, c, q, a, b, v = s.symbols('p z c q A b v', nonzero=True, real=True)
F = (a*a-p*p)*(b*b-p*p)
V2 = (q*q-a*a)*(q*q-b*b)/(q*q)
profile_s = c*(z-v*p)/(p*p-q*q)
dx = lambda f: s.diff(f,p)*z+s.diff(f,z)*s.diff(F,p)/2


def reduce_on_curve(expr):
    num = s.together(expr).as_numer_denom()[0]
    num = s.rem(num, z*z-F, z)
    num = s.rem(num, v*v-V2, v)
    return s.factor(num)


checks = {
    'elliptic_profile_first_ode': s.simplify(z-v*p-(p*p-q*q)*profile_s/c) == 0,
    'elliptic_profile_second_ode': reduce_on_curve(dx(profile_s)-c*p+v*profile_s+p*profile_s**2/c) == 0,
}
t, w = s.symbols('t frequency_derivative', real=True)
M = s.Matrix([[1,t*w],[0,1]])
W = s.Matrix([[0,1],[-1,0]])
checks['symplectic_shear'] = M.T*W*M == W
checks['area_and_growth_are_distinct'] = s.simplify((M.T*M)[1,1]-(1+t*t*w*w)) == 0
result = {'passed': all(checks.values()), 'checks': checks,
          'scope': 'Exact algebra plus the analytic proofs in synthesis.md; no general-field stability claim.'}
(Path(__file__).parent/'synthesis_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
assert result['passed']
