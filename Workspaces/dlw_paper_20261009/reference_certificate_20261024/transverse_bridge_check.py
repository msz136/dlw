"""Check the partial-system counterexample, not a solution of the DLW IVP."""
from pathlib import Path
import json
import sympy as s
x,z,t=s.symbols('x z t',real=True)
h=s.Function('h')(z)
q=s.exp(t**2*h*s.sin(x)-t**5*h**2/10)
V=(2*t-t**2)*h*s.sin(x)+t**4*h**2*s.cos(2*x)/2
w=4+2*(2*t-t**2)*s.diff(h,z)*s.cos(x)-t**4*h*s.diff(h,z)*s.sin(2*x)
r=(w-4)/q
backward=s.trigsimp(s.expand((s.diff(q,t)+s.diff(q,x,2))/q-V))
constraint=s.trigsimp(s.diff(V,z)+s.diff(w,x)/2)
assert backward==0 and constraint==0
assert s.integrate(V,(x,-s.pi,s.pi))==0
assert q.subs(t,0)==1 and r.subs(t,0)==0
defect=s.simplify((s.diff(r,t)-s.diff(r,x,2)+V*r).subs(t,0))
assert s.simplify(defect-4*s.diff(h,z)*s.cos(x))==0
# Verify the exponent interpolation algebra used in A1.
k2,m,theta,sigma,T=s.symbols('k2 m theta sigma T',real=True)
exponent=s.expand((1-theta)*(k2*t-sigma*m)+theta*(-k2*(T-t)))
assert s.expand(exponent+sigma*(1-theta)*m+(theta*T-t)*k2)==0
out={'status':'symbolic checks only; full nonlinear analyticity bridge unproved',
     'backward_q_equation':True,'primitive_constraint':True,'potential_zero_mean':True,
     'analytic_initial_q_r':True,'forward_r_defect_at_zero':str(defect),
     'linear_interpolation_exponent':True,
     'original_initial_value_problem_certified':False,'eta_u':None,'eta_v':None}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
