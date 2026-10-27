"""Exact algebra supporting the Gaussian physical L-infinity response obstruction.

The weak compactness, distribution estimates and complex-growth inequalities
are analytic arguments, not purportedly certified by these symbolic checks.
"""
from pathlib import Path
import json
import sympy as s

x,z,t=s.symbols('x z t')
eps=s.symbols('eps', real=True)
u=s.Function('u')(x,z,t); v=s.Function('v')(x,z,t)
w=s.Function('w')(x,z,t); q=s.Function('q')(x,z,t)

def eu(a,b):
    return s.diff(a,z,t)+s.diff(b,x,2)+s.diff(a*a/2,x,z)

def ev(a,b):
    return s.diff(b,t)+s.diff(a,x,2,z)+s.diff(a*b-4*a,x)

lu=s.diff(w,z,t)+s.diff(q,x,2)+s.diff(u*w,x,z)
lv=s.diff(q,t)+s.diff(w,x,2,z)+s.diff(u*q+(v-4)*w,x)
checks={
    'normalized_u_source':s.expand(eu(u+eps*w,v+eps*q)-eu(u,v)
                                 -eps*lu-eps**2*s.diff(w*w/2,x,z))==0,
    'normalized_v_source':s.expand(ev(u+eps*w,v+eps*q)-ev(u,v)
                                 -eps*lv-eps**2*s.diff(w*q,x))==0,
}

a=q+s.diff(w,z); bvar=q-s.diff(w,z)
abase=v-4+s.diff(u,z); bbase=v-4-s.diff(u,z)
checks['linearized_characteristic_a']=s.expand(s.diff(a,t)+s.diff(a,x,2)
    +s.diff(u*a+abase*w,x)-lv-lu)==0
checks['linearized_characteristic_b']=s.expand(s.diff(bvar,t)-s.diff(bvar,x,2)
    +s.diff(u*bvar+bbase*w,x)-lv+lu)==0

p=(v-4+s.diff(u,z))/4
b=-u/2-s.diff(p,x)/p
r=(v-4+3*s.diff(u,z))/4+s.diff(s.diff(p,x)/p,z)
identity=s.diff(r,t)+s.diff(r,x,2)-2*s.diff(b*r,x) \
         -(ev(u,v)+3*eu(u,v))/4-s.diff((ev(u,v)+eu(u,v))/(4*p),x,z)
checks['physical_inverse_defect_residual_identity']=s.cancel(s.expand(identity))==0

alpha,tau=s.symbols('alpha tau', positive=True)
gamma=tau/alpha
rate=tau*(2*alpha-1)/alpha
checks['holder_terminal_exponent']=s.simplify(tau-gamma*(1-alpha)-rate)==0
checks['holder_source_exponent']=s.simplify(gamma*(2*alpha-1)-rate)==0

Y,eta=s.symbols('Y eta', real=True)
xi=-Y/18+eta
checks['primitive_reciprocal_identity']=s.simplify(Y/(s.I*xi)-18*s.I
                                               +18*s.I*eta/xi)==0
checks['primitive_reciprocal_bound_constant']=18*36==648
checks['primitive_phase_bound_constant']=18*9==162
checks['gaussian_split_tail_exponent']=s.Rational(9,2)*s.Rational(1,36)**2==s.Rational(1,288)

result={
    'date':'2026-10-26',
    'checks':checks,
    'all_passed':all(checks.values()),
    'scope':'Exact residual/source algebra, Holder exponent balance, and complex-lemma constants only.',
    'analytic_proof_not_formalized':True,
    'isolated_nonzero_amplitude_nonexistence_proved':False,
    'perturbed_reference_error_certified':False,
}
assert result['all_passed']
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
