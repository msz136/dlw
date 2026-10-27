"""Exact checks for analytic smoothing matching + Holder inverse counterexample."""
from pathlib import Path
import json
import sympy as s

p,q,lam=s.symbols('p q lam',real=True)
checks={}
checks['cubic_difference_factorization']=s.expand(p**3-q**3-(p-q)*(p*p+p*q+q*q))==0
checks['cubic_monotonicity_remainder']=s.expand(p*p+p*q+q*q-(p-q)**2/4-s.Rational(3,4)*(p+q)**2)==0
x,mu,cc=s.symbols('x mu cc',real=True)
poly=lam*x+x**3-cc*mu
# At x=mu=0 the scalar implicit derivative is cc/lam.
checks['implicit_derivative']=s.simplify((-s.diff(poly,mu)/s.diff(poly,x)).subs({x:0,mu:0})-cc/lam)==0
S,T,n,alpha=s.symbols('S T n alpha',positive=True)
lambda_n=s.exp(-S*n*n)
obs=s.exp(-(S-T)*n*n)
checks['observation_derivative']=s.simplify(obs*s.exp(-alpha*n)/lambda_n-s.exp(T*n*n-alpha*n))==0
checks['holder_exponent']=s.simplify(-(S-T)+S/3-(T-2*S/3))==0
checks['actual_padding_satisfies_holder_condition']=s.Rational(1,100)<=2*s.Rational(1,50)/3
# Critical values of beta*x+x^3 are the approaching complex branch points.
beta=s.symbols('beta',positive=True)
xc=s.I*s.sqrt(beta/3)
checks['complex_inverse_critical_point']=s.simplify((beta+3*x*x).subs(x,xc))==0
checks['critical_value_magnitude_factor']=s.simplify((beta*xc+xc**3)/(s.I*beta**s.Rational(3,2))-2/(3*s.sqrt(3)))==0
assert all(bool(v) for v in checks.values()),checks
result={'date':'2026-10-26','checks':{k:bool(v) for k,v in checks.items()},'all_passed':True,
        'parameters':{'S':'0.02','T':'0.01','alpha':'any positive'},
        'conclusion':'Analytic Gaussian-smoothing matching, derivative injectivity, bounded real lifts and interior Holder stability do not imply differentiability in the parameter.',
        'DLW_reference_certified':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
