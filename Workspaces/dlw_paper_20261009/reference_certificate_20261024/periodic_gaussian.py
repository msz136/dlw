"""Approved periodic-Gaussian definition and certified exact boundary samples.

Gaussian sum is the exact newly selected initial profile. Finite evaluation
retains m=-1,0,1 and bounds the infinite omitted sum uniformly by a geometric
majorant. The certificate is only for the exact lower-boundary trace.
"""
from pathlib import Path
import json
from flint import arb,ctx
HERE=Path(__file__).resolve().parent
ctx.dps=120
P=arb(192);L=arb(96);t=arb(1)/100
def heat_gaussian(x,time):
    S=36+4*time
    scale=6/S.sqrt()
    value=scale*sum((-(x+P*m)**2/S).exp() for m in [-1,0,1])
    # For |x|<=96.04, omitted terms |m|>=2 start at distance d.
    d=2*P-(L+4*t)
    ratio=(-(2*d*P+P*P)/S).exp()
    tail=2*scale*(-d*d/S).exp()/(1-ratio)
    return value,tail

initial_difference=2*arb(-256).exp()/(1-arb(-2048).exp())
assert initial_difference<arb('1.324e-111')
trace=[]
worst_tail=arb(0)
for j in range(1921):
    x=-96+arb(j)/10
    back,rb=heat_gaussian(x-4*t,-t)
    forward,rf=heat_gaussian(x-4*t,t)
    value=arb(5)/100*arb.pi()/8*(back-forward)
    tail=arb(5)/100*arb.pi()/8*(rb+rf)
    assert tail<arb('1e-998')
    rounded=value.mid().str(80,radius=False)
    # Triangle inequality: evaluate retained terms in Arb plus exact tail bound.
    assert abs(arb(rounded)-value)+tail<arb('1e-80')
    trace.append(rounded)
(HERE/'exact_periodic_gaussian_boundary_T001.txt').write_text('\n'.join(trace),encoding='utf8')
r=dict(profile='G_per(x)=sum_{m in Z} exp(-((x+192m)/6)^2)',
    initial_u='.05 e(y) G_per(x)',initial_v='.03 e(y) G_per(x)',
    envelope='e(y)=sin(pi*(y+2)/4)',a=2,lambda_value=-2,
    user_approved=True,old_profile_uniform_difference_upper='1.324e-111',
    boundary_v_formula='(.05*pi/8)*(H_{-t}G_per(x-4t)-H_t G_per(x-4t))',
    heat_formula='H_s G_per(x)=6/sqrt(36+4s)*sum_m exp(-(x+192m)^2/(36+4s))',
    boundary_trace_time_condition='0<=t<9',T='.01',
    omitted_sum_boundary_v_uniform_upper='1e-998',
    rounded_trace_sample_error_upper='1e-80',
    sample_scope='1921 points x=-96+j/10, j=0,...,1920, y=-2, T=.01',
    full_domain_upper=None,continuum_reference_certified=False,
    note='Exact nonlinear boundary trace and its evaluation only; no interior solution certificate')
(HERE/'periodic_gaussian_certificate.json').write_text(json.dumps(r,indent=2),encoding='utf8')
print(json.dumps(r,indent=2))
