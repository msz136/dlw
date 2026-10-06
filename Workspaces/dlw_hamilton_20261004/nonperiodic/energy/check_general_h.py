"""Exact all-admissible-h energy integrals for original paper A/B/C arms."""
import json
from pathlib import Path
import sympy as s

y,h=s.symbols('y h', positive=True)
a=s.Integer(2)
out={}
for name,p,q,K in [('A',1,2,s.Integer(8)),('B',4,-3,s.Rational(296,3)),
                   ('C_component_1',6,-5,s.Rational(728,3))]:
    P=s.Integer(p)-a;Q=s.Integer(q)+a;S=s.Integer(p+q)
    rho=s.factor(-(P+h/2)/(Q-h/2))
    mu=s.factor((P+h/2)/(P-h/2)*(Q+h/2)/(Q-h/2))
    # Use denominator factors with polynomial h coefficients, so no generic
    # parameter-field integration or multivariate residue simplification runs.
    domain=s.QQ.frac_field(h)
    poly=lambda expr:s.Poly(expr,y,domain=domain)
    A=(2*P-h)*(2*Q-h);B=(2*P+h)*(2*Q+h)
    C=2*Q-h;D=-(2*P+h)
    l1=poly(1+y);l2=poly(A+B*y);lf=poly(C+D*y);yp=poly(y)
    un=2*a*l1*l2*lf+S*yp*(2*D*l1*l2-l2*lf-B*l1*lf)
    wn=-4*l1*l2+16*S*S*yp
    uxn=S*S*yp*(2*C*D*l1*l1*l2*l2-l2*l2*lf*lf-A*B*l1*l1*lf*lf)
    rn=2*S*S*yp*(l2*l2+A*B*l1*l1)
    numerator=un*un*wn/2+h*h*wn**3*lf*lf/96+wn*uxn+wn*rn*lf*lf/2
    numerator+=(8*a*a+s.Rational(2,3)*h*h)*l1**3*l2**3*lf**2
    integrated_numerator,rem=divmod(numerator,S*yp)
    assert rem.is_zero
    remainder_num=integrated_numerator-4*K*S*l1*l1*l2*l2*lf*lf
    # Rational primitive Q/T has deg Q<=4, T=l1^2*l2^2*lf.
    # Solve its coefficients descending using the top five coefficients.
    T=l1*l1*l2*l2*lf
    target=remainder_num*l1*l2
    primitive_num=poly(0)
    leading=T.nth(5)
    for i in range(4,-1,-1):
        current=primitive_num.diff()*T-primitive_num*T.diff()
        qi=domain.to_sympy((domain.from_sympy(target.nth(i+4))-
                            domain.from_sympy(current.nth(i+4)))/
                           (domain.from_sympy((i-5)*leading)))
        primitive_num+=poly(qi*y**i)
    assert primitive_num.diff()*T-primitive_num*T.diff()==target
    assert primitive_num.nth(0)==0
    out[name]={'rho':str(rho),'mu':str(mu),'energy_formula':f'({K})/h * log(mu)',
               'remainder_log_part_zero':True,'rational_endpoint_jump_zero':True,
               'primitive_identity_exact':True,
               'rational_primitive_numerator':str(primitive_num.as_expr()),
               'rational_primitive_denominator':str(T.as_expr())}
    print(name,'passed',flush=True)
Path(__file__).with_name('general_h_energy_checks.json').write_text(
    json.dumps(out,indent=2),encoding='utf-8')
