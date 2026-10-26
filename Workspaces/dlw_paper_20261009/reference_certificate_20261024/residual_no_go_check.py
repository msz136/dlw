"""Algebra and outward bounds for the full nonlinear residual obstruction.

This is not a continuum-reference error certificate. Example background bounds
are explicit hypotheses, not estimates proved for the actual unknown solution.
"""
from pathlib import Path
import json
import sympy as s
from flint import arb, ctx

x, z, t = s.symbols('x z t', real=True)
U = s.Function('U')(x,z,t)
V = s.Function('V')(x,z,t)
a, b = s.diff(U,z)+V, s.diff(U,z)-V
Ra = s.diff(a,t)+s.diff(a,x,2)+s.diff(U*a,x)-4*s.diff(U,x)
Rb = s.diff(b,t)-s.diff(b,x,2)+s.diff(U*b,x)+4*s.diff(U,x)
R1 = s.diff(U,z,t)+s.diff(V,x,2)+s.diff(U*s.diff(U,z),x)
R2 = s.diff(V,t)+s.diff(U,x,x,z)+s.diff(U*V-4*U,x)
assert s.simplify((Ra+Rb)/2-R1)==0
assert s.simplify((Ra-Rb)/2-R2)==0

A0=s.Function('A0')(x,z,t); B0=s.Function('B0')(x,z,t)
du=s.Function('du')(x,z,t); da=s.Function('da')(x,z,t)
base_a=s.diff(A0,t)+s.diff(A0,x,2)+s.diff(U*A0,x)-4*s.diff(U,x)
pert_a=s.diff(A0+da,t)+s.diff(A0+da,x,2)+s.diff((U+du)*(A0+da),x)-4*s.diff(U+du,x)
expected_a=s.diff(da,t)+s.diff(da,x,2)+s.diff(U*da+du*A0+du*da,x)-4*s.diff(du,x)
assert s.simplify(pert_a-base_a-expected_a)==0
base_b=s.diff(B0,t)-s.diff(B0,x,2)+s.diff(U*B0,x)+4*s.diff(U,x)
pert_b=s.diff(B0,t)-s.diff(B0,x,2)+s.diff((U+du)*B0,x)+4*s.diff(U+du,x)
assert s.simplify(pert_b-base_b-s.diff(du*B0,x)-4*s.diff(du,x))==0

r=s.symbols('r', real=True)
F=25*s.sqrt(5)/3*r**3*(1-r)**3
f=s.diff(F,r)
for endpoint in (0,1):
    for order in (0,1,2): assert s.diff(F,r,order).subs(r,endpoint)==0
for sign in (-1,1):
    point=(1+sign/s.sqrt(5))/2
    assert s.simplify(s.diff(f,r).subs(r,point))==0
    assert s.simplify(f.subs(r,point)**2)==1
assert s.factor(s.diff(f,r))==s.factor(50*s.sqrt(5)*r*(1-r)*(1-5*r+5*r*r))
assert s.simplify(F.subs(r,s.Rational(1,2))-25*s.sqrt(5)/192)==0
assert 25*s.sqrt(5)/192 < 1
k, T=s.symbols('k T', positive=True)
h=(s.exp(k*k*t)-1)/(s.exp(k*k*T)-1)
assert s.simplify(s.diff(h,t)-k*k*h-k*k/(s.exp(k*k*T)-1))==0
assert h.subs(t,0)==0 and s.simplify(h.subs(t,T))==1

# Test the principal cancellation used for the arbitrary-interior construction.
phi=s.Function('phi')(x,t); chi=s.Function('chi')(t)
Us=s.Function('Us')(x,t)
principal=s.diff(chi*phi,t)+s.diff(chi*phi,x,2)+s.diff(U*chi*phi,x)
principal=principal.subs(s.diff(phi,t),-s.diff(phi,x,2)-s.diff(Us*phi,x))
assert s.simplify(principal-(s.diff(chi,t)*phi+chi*s.diff((U-Us)*phi,x)))==0

ctx.prec=256
time=arb(1)/100; epsilon=arb(1)/1000
examples=[]
for n, upper in [(1024,'1.81e-5'),(2048,'1.55e-19'),(4096,'1.77e-77')]:
    wave=arb.pi()*n/96
    q=(-wave*wave*time).exp()
    bound=epsilon*q*(wave*wave/(1-q)+(6+wave*(14+4*epsilon))/2)
    assert bound < arb(upper)
    assert 2*q<4
    examples.append({'n':n,'strip_width_enclosure':str(q),
                     'full_physical_residual_difference_upper_enclosure':str(bound),
                     'rounded_strict_upper':upper,'terminal_v_difference_exact':'0.001'})
result={'symbolic_checks':'passed: physical residual identity, full nonlinear difference, bump extrema, exact initial values, antiheat forcing, background transport cancellation',
        'arb_precision_bits':ctx.prec,
        'example_assumptions':'P,Q,M_a,M_b,N_a,N_b <= 1; not established bounds on actual continuum solution',
        'examples':examples,
        'theorem_scope':'No residual-to-maximum-error modulus without extra regularity/tail constraints; preserves exact initialization and boundary',
        'does_not_prove':['nonexistence of all actual low-regularity solutions','two distinct exact solutions with the same initialization','impossibility of every future structural certificate'],
        'independently_reviewed':False,'continuum_reference_certified':False,
        'eta_u':None,'eta_v':None}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
