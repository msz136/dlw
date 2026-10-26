"""Audit the Endpoint v leading defect; not a positive-time certificate."""
import json
from pathlib import Path
import sympy as s
x,z,A,B,k,kappa = s.symbols('x z A B k kappa', real=True)
p = s.Function('p')(x,z)
results = {}
for sign in [-1,1]:
    v = 4+sign*p
    c = s.simplify(-s.diff((v-4)**2-p**2,x)/4)
    assert c == 0
    results[f'compatible_sign_{sign}'] = str(c)

u = A*s.sin(kappa*z)*s.cos(k*x)
v = B*s.sin(kappa*z)*s.sin(k*x)
c = -s.diff((v-4)**2-s.diff(u,z)**2,x)/4
mid = s.simplify(c.subs(z,s.pi/(2*kappa)))
assert s.simplify(mid-(2*B*k*s.cos(k*x)-B**2*k*s.sin(k*x)*s.cos(k*x)/2)) == 0
at_zero = s.simplify(mid.subs(x,0))
assert at_zero == 2*B*k
results['original_sine_at_y0_x0'] = str(at_zero)
results['original_sine_coefficient_value'] = float(at_zero.subs({B:s.Rational(2,100),k:s.pi/12}))

G = s.Function('G')(x)
u = A*s.sin(kappa*z)*G
v = B*s.sin(kappa*z)*G
c = -s.diff((v-4)**2-s.diff(u,z)**2,x)/4
mid = s.simplify(c.subs(z,s.pi/(2*kappa)))
assert s.simplify(mid-(2*B-B**2*G/2)*s.diff(G,x)) == 0
results['original_gaussian_at_y0'] = str(mid)
results['scope'] = 'Interior initial analytic-x Endpoint v RHS defect coefficient of h; not evolved error.'
results['positive_time_original_reference_certified'] = False
Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
