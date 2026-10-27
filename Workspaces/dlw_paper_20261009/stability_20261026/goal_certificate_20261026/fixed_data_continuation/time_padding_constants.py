"""Outward constants for a conditional time-padding matching reduction."""
from pathlib import Path
import json
from flint import arb, ctx

ctx.prec=256
R=arb(2)/5;rho=arb(1)/10;Z=arb(4)
S=arb(1)/50;s=arb(3)/200;T=arb(1)/100
one=arb(1);e=one.exp()
a1=1/(e*rho);a2=4/(e*e*rho*rho)
c1=R*(Z/2+arb(2).sqrt()*Z/arb.pi())
c0=c1*a1;c=4*c1*c1+1;K=8*c1**4+4*c0*c0
lmin=2*K*(c*S).exp()/c
phiT=(-c*T).exp();phis=(-c*s).exp()
theta=(phiT-phis)/(1-phis)
Hchi=3/(2*(S-s));M=2*R
Lw=2*(a2*R+Z*a1*R*R)
assert theta>0 and theta<1
rows=[]
for exponent in [12,20,40]:
    delta=arb(10)**(-exponent)
    lam=(M/delta).log()/(1-phis)
    assert lam>lmin
    Q=(c*S).exp()*(4*Hchi*Hchi*(S-s)/(lam*c)+2)*((2*(1-theta))*M.log()+2*theta*delta.log()).exp()
    alt=4*(c*S).exp()*Hchi*Hchi*(S-s)/(lam*c)*M*M*(-2*lam*(phiT-phis)).exp()+2*(c*S).exp()*delta*delta*(2*lam*(1-phiT)).exp()
    assert Q.overlaps(alt)
    first=2*(Q/T).sqrt();second=(8*Lw*Q).root(3)
    endpoint=first if first>second else second
    rows.append(dict(initial_matching_error=f'1e-{exponent}',lambda_enclosure=str(lam),time_integrated_pair_error_squared_upper_enclosure=str(Q),endpoint_normalized_H_error_upper_enclosure=str(endpoint)))

result=dict(date='2026-10-26',precision_bits=ctx.prec,meaning='conditional theorem for two exact mixed solutions; no actual target certificate',
            parameters=dict(R=str(R),rho=str(rho),Z=str(Z),S=str(S),s=str(s),T=str(T)),
            constants=dict(c1=str(c1),c0=str(c0),c=str(c),K=str(K),lambda_min=str(lmin),theta=str(theta),Lw=str(Lw)),
            rows=rows,actual_independent_reference_certified=False,eta_u=None,eta_v=None)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
