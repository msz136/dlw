"""Restrict C to the current y strip and short observation interval."""
from pathlib import Path
from fractions import Fraction
import json
import sympy as s
from single_bounds import exp_positive_bounds,outward
from bernstein import abs_sup

HERE=Path(__file__).resolve().parent
r,t=s.symbols('r t',real=True)
lam=s.symbols('lam',real=True)
old=json.loads((HERE/'two_bounds.json').read_text(encoding='utf-8'))
# theta_2-theta_1 = 4t - 5y/12; y in [-3/2,3/2], t in [0,1/100].
elo,ehi=exp_positive_bounds(s.Rational(5,8))
lminlo,lminhi=1/ehi,1/elo
lmaxlo,lmaxhi=exp_positive_bounds(s.Rational(133,200))
scale=10**14
lo=s.Rational(s.floor(lminlo*scale),scale)
hi=s.Rational(s.ceiling(lmaxhi*scale),scale)
out={'domain':'x in R, y in [-3/2,3/2], time in [0,1/100]',
     'phase_ratio_domain_outer':[str(lo),str(hi)],'bounds':{}}
for key,row in old['bounds'].items():
    expr=s.sympify(row['expression'],locals={'r':r,'t':t})
    expr=s.cancel(expr.subs(t,lam*r/(1-r+lam*r)))
    print('bounding strip',key,flush=True)
    b=abs_sup(expr,(r,lam),[(0,1),(lo,hi)],tolerance=Fraction(1,10**6),seconds=120)
    assert lminhi<=s.Rational(b['witness'][1])<=lmaxlo
    b['bound']=[outward(s.Rational(b['lower_exact']),places=9),outward(s.Rational(b['upper_exact']),True,places=9)]
    out['bounds'][key]=b
    (HERE/'two_strip_bounds.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(key,b['bound'],b['subdivisions'],b['tolerance_reached'],flush=True)

