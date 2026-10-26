"""Checks constants of CONDITIONAL_ERROR_MODULUS.md, not IVP existence."""
from pathlib import Path
import json
import sympy as s
from flint import arb, ctx

G,V,c1,c0=s.symbols('G V c1 c0', nonnegative=True)
assert s.expand(G**2/2+8*c1**4*V**2-4*c1**2*G*V-(G-4*c1**2*V)**2/2)==0
ctx.prec=256
T=arb(1)/100
r=arb(9)/1000
c=arb(1601)
K=arb(1280676)
m=c*(-c*T).exp()
lam=2*K/m
gap=1-(-c*r).exp()
log_eps=(lam*m/(8*T)).log()/2-lam*gap
log10_eps=log_eps/arb(10).log()
assert lam>1
assert 1/(2*lam)-gap<0  # derivative of the C4 bound; stays negative
assert log10_eps < -10**9
assert 2*arb(2).sqrt() > arb('2.82842712474619')
out={
 'proof_status':'self-reviewed draft; algebra and constants checked only',
 'lambda_min':str(lam),
 'log10_epsilon_required_for_first_term_le_one':str(log10_eps),
 'monotone_threshold_checked':True,
 'original_initial_value_problem_certified':False,
 'eta_u':None,'eta_v':None,
 'meaning':'The stated upper bound is unusable at ordinary residual scales; not an actual-error lower bound.'
}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
