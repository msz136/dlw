"""Symbolic coefficients and triangular cancellation for the robust IVP theorem."""
from pathlib import Path
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
z,alpha,eta,H=sp.symbols('z alpha eta H', real=True)
phi=sp.sin(alpha*z)**2
perturbations={
    'u_only':(-eta*phi*H,sp.Integer(0)),
    'v_only':(sp.Integer(0),-eta*phi*H),
}
result={'date':'2026-10-26','meaning':'Exact algebra check, not a PDE existence calculation','cases':{}}
for label,(du,dv) in perturbations.items():
    dA=sp.diff(du,z)+dv
    dB=dv-sp.diff(du,z)
    jetsA=[sp.simplify(sp.diff(dA,z,j).subs(z,0)/sp.factorial(j)) for j in range(3)]
    jetsB=[sp.simplify(sp.diff(dB,z,j).subs(z,0)/sp.factorial(j)) for j in range(3)]
    if label=='u_only':
        expectedA=[0,-2*eta*alpha**2*H,0]
        expectedB=[0,2*eta*alpha**2*H,0]
    else:
        expectedA=[0,0,-eta*alpha**2*H]
        expectedB=[0,0,-eta*alpha**2*H]
    assert all(sp.simplify(x-y)==0 for x,y in zip(jetsA,expectedA))
    assert all(sp.simplify(x-y)==0 for x,y in zip(jetsB,expectedB))
    result['cases'][label]={'delta_a_0_to_2':[str(v) for v in jetsA],
                           'delta_b_0_to_2':[str(v) for v in jetsB],
                           'passed':True}
a0,a1,a2,b0,b1,b2=sp.symbols('a0 a1 a2 b0 b1 b2')
da0,da1,da2,db0,db1,db2=sp.symbols('da0 da1 da2 db0 db1 db2')
fa1=(a0-b0)*a0/2
fb1=(a0-b0)*b0/2
fa2=(a0-b0)*a1/2+(a1-b1)*a0/4
fb2=(a0-b0)*b1/2+(a1-b1)*b0/4
shift={a0:a0+da0,a1:a1+da1,a2:a2+da2,b0:b0+db0,b1:b1+db1,b2:b2+db2}
checks={}
for name,flux,zero_changes in [
    ('u_only_first_a_flux',fa1,{da0:0,db0:0}),
    ('u_only_first_b_flux',fb1,{da0:0,db0:0}),
    ('v_only_second_a_flux',fa2,{da0:0,db0:0,da1:0,db1:0}),
    ('v_only_second_b_flux',fb2,{da0:0,db0:0,da1:0,db1:0}),
]:
    residual=sp.simplify((flux.xreplace(shift)-flux).subs(zero_changes))
    assert residual==0
    checks[name]=str(residual)
result['nonlinear_flux_cancellation']=checks
w,z1,z2,r=sp.symbols('w z1 z2 r',nonzero=True)
factor=(2-w/z1-z1/w)/4
factorized=-(w-z1)**2/(4*w*z1)
assert sp.simplify(factor-factorized)==0
P=sp.expand(factor*(2-w/z2-z2/w)/4)
coefficients={ell:sp.expand(P).coeff(w,ell) for ell in range(-2,3)}
tail=sp.simplify(sum(coefficients[ell]*r**(4-ell)/2 for ell in coefficients))
tail_expected=sp.simplify(r**4*P.subs(w,1/r)/2)
assert sp.simplify(tail-tail_expected)==0
result['finite_sample_mask']={'sine_square_laurent_factorization':'0',
                             'two_sample_high_frequency_tail_identity':'0',
                             'passed':True}
result['all_passed']=True
(HERE/'robust_same_envelope_check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
