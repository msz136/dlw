"""Sharpen the same-initial-physical-fields leading error velocity enclosure."""
from pathlib import Path
from fractions import Fraction
import json
import sympy as s
from single_bounds import CASES,fields,exp_positive_bounds,outward
from bernstein import abs_sup

HERE=Path(__file__).resolve().parent
z,q=s.symbols('s q',real=True)
result={}
for name,pars in CASES.items():
    _,ell,_,_,primitive,_=fields(*pars)
    elo,ehi=exp_positive_bounds(3*abs(ell))
    qlo=1/ehi;qhi=1/elo
    scale=10**16
    lower=s.Rational(s.floor(qlo*scale),scale)
    assert lower<qlo and lower+s.Rational(1,scale)>qhi
    sy=q*z/(1-z+q*z)
    for model,b in primitive.items():
        expr=s.cancel(b.subs(z,sy)-b)
        bound=abs_sup(expr,(z,q),[(0,1),(lower,1)],tolerance=Fraction(1,10**7),seconds=150)
        assert s.Rational(bound['witness'][1])>=qhi
        bound['bound']=[outward(s.Rational(bound['lower_exact']),places=9),outward(s.Rational(bound['upper_exact']),True,places=9)]
        bound['q_domain_outer']=[str(lower),'1']
        bound['physical_q_endpoint_exact_enclosure']=[str(qlo),str(qhi)]
        result[name+'_'+model+'_u']=bound
        (HERE/'velocity_bounds.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(name,model,bound['bound'],bound['subdivisions'],bound['tolerance_reached'],flush=True)

