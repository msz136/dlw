"""Exact algebra/Arb checks for the selfadjoint indefinite energy proof.

These checks supplement the functional-analytic argument; they do not prove
existence and do not turn uniqueness into a stability estimate.
"""
from pathlib import Path
import json
import sympy as s
from flint import arb,ctx

t=s.symbols('t',real=True)
lam=s.symbols('lambda',positive=True)
a11,a12,a22=s.symbols('a11 a12 a22',real=True)
A=s.Matrix([[a11,a12],[a12,a22]])
Y=s.Matrix([s.Function('y1')(t),s.Function('y2')(t)])
phi=s.Function('phi')(t)
D=A+lam*s.diff(phi,t)*s.eye(2)
res=s.diff(Y,t)-D*Y
identity=(res.dot(res)-s.diff(Y,t).dot(s.diff(Y,t))-(D*Y).dot(D*Y)
          -lam*s.diff(phi,t,2)*Y.dot(Y)+s.diff(Y.dot(D*Y),t))
assert s.simplify(identity)==0
G,V,c1,c0=s.symbols('G V c1 c0',nonnegative=True)
assert s.expand(G**2/2+8*c1**4*V**2-4*c1**2*G*V-(G-4*c1**2*V)**2/2)==0
c=4*c1**2+1
weight=s.exp(-c*t)
assert s.expand(s.diff(weight,t,2)-4*c1**2*c*weight-c*weight)==0

ctx.prec=256
rho=arb(1)/10;R=arb(7)/10;T=arb(1)/100
bound_c1=2*R+2*arb(2).sqrt()*R+16
bound_c0=(2+2*arb(2).sqrt())*R/(arb(1).exp()*rho)
assert bound_c1<20 and bound_c0<13
chosen_c=4*20**2+1
K=8*20**4+4*13**2
assert chosen_c==1601 and K==1280676
mT=chosen_c*(-chosen_c*T).exp()
lambda_threshold=2*K/mT
assert lambda_threshold<arb('1.5e10')
assert arb('1.5e10')*mT/2>K
result={'proof':'Initial-value uniqueness for the explicitly stated strong-solution class',
        'symbolic_checks':'indefinite symmetric operator integration identity, Young square, decreasing convex weight: passed',
        'rho':'.1','mixed_solution_radius':'.7',
        'c1_enclosure':str(bound_c1),'c0_enclosure':str(bound_c0),
        'chosen_c1':20,'chosen_c0':13,'weight_c':chosen_c,'K':K,
        'lambda_threshold_enclosure':str(lambda_threshold),
        'rounded_sufficient_lambda':'15000000000',
        'initial_matching_map_injective_in_proved_class':True,
        'matching_map_surjectivity_proved':False,
        'original_initial_value_existence_proved':False,
        'continuum_reference_certified':False,'eta_u':None,'eta_v':None,
        'review_status':'self-reviewed draft; not independent or formal verification'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
