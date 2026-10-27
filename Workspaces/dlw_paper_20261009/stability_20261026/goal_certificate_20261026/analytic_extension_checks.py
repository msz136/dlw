"""Exact algebra checks for the analytic transverse counterexample."""
from pathlib import Path
import json
import sympy as s

x,z,t,k,M,c=s.symbols('X z t k M C',positive=True)
F=s.Function('F')(z); h=s.Function('h')(t)
u=M*F*h*s.cos(k*x)/c
v=4+s.diff(u,z)
r1=s.diff(u,z,t)+s.diff(v,x,2)+s.diff(u*s.diff(u,z),x)
r2=s.diff(v,t)+s.diff(u,x,2,z)+s.diff(u*v-4*u,x)
expected=(M*s.diff(F,z)*(s.diff(h,t)-k*k*h)*s.cos(k*x)/c
          -M*M*k*F*s.diff(F,z)*h*h*s.sin(2*k*x)/c**2)
checks={
    'analytic_R1':s.simplify(s.expand_trig(r1-expected))==0,
    'analytic_R2':s.simplify(s.expand_trig(r2-expected))==0,
}
T=s.symbols('T',positive=True)
for m in range(5):
    num=s.exp(k*k*t)-sum((k*k*t)**j/s.factorial(j) for j in range(m+1))
    den=s.exp(k*k*T)-sum((k*k*T)**j/s.factorial(j) for j in range(m+1))
    hh=num/den
    checks[f'time_jet_defect_{m}']=s.simplify(
        s.diff(hh,t)-k*k*hh-k*k*(k*k*t)**m/s.factorial(m)/den)==0
    checks[f'initial_jets_{m}']=all(s.simplify(s.diff(hh,t,j).subs(t,0))==0
                                         for j in range(m+1))
checks['all_passed']=all(checks.values())
Path(__file__).with_suffix('.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
assert checks['all_passed']
