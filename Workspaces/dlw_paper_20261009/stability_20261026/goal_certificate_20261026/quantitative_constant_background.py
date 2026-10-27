"""Full nonlinear DLW small-residual counterexamples, with Arb parameter bounds.

The target here is the exact constant state (u,v)=(0,4). This is an explicit
impossibility example for residual-only certification, not an existence or
reference certificate for the independently perturbed nonzero backgrounds.
"""
from pathlib import Path
import json
import sympy as s
from flint import arb, ctx

ctx.prec = 256
theta = s.symbols('theta', real=True)
F = 25*s.sqrt(5)*theta**3*(1-theta)**3/3
f = s.diff(F, theta)
for endpoint in (0, 1):
    for derivative in range(3):
        assert s.diff(F, theta, derivative).subs(theta, endpoint) == 0
for sign in (-1, 1):
    p = (1+sign/s.sqrt(5))/2
    assert s.simplify(f.subs(theta, p)**2-1) == 0
    assert s.simplify(s.diff(f,theta).subs(theta,p)) == 0
critical = (1-1/s.sqrt(11))/2
C_exact = 9765625*s.sqrt(11)/170069856
assert s.simplify(s.diff(F*f,theta)-s.Rational(3125,3)*theta**4*(1-theta)**4*(5-22*theta+22*theta**2)) == 0
assert s.simplify((F*f).subs(theta, critical)-C_exact) == 0
assert s.simplify(s.diff(F*f, theta).subs(theta, critical)) == 0

X,z,t,zstar=s.symbols('X z t zstar', real=True)
M,delta,k,T=s.symbols('M delta k T', positive=True)
H=s.Function('H')(t)
zz=(z-zstar)/delta
FF=F.subs(theta,zz)
ff=f.subs(theta,zz)
u=M*delta*FF*H*s.cos(k*X)
v=4+s.diff(u,z)
R1=s.diff(u,z,t)+s.diff(v,X,2)+s.diff(u*s.diff(u,z),X)
R2=s.diff(v,t)+s.diff(u,X,X,z)+s.diff(u*v-4*u,X)
expected=M*ff*(s.diff(H,t)-k*k*H)*s.cos(k*X)-M*M*delta*k*FF*ff*H*H*s.sin(2*k*X)
assert s.simplify(s.expand_trig(R1-expected)) == 0
assert s.simplify(R2-R1) == 0
h=(s.exp(k*k*t)-1)/(s.exp(k*k*T)-1)
assert h.subs(t,0) == 0
assert s.simplify(h.subs(t,T)-1) == 0
assert s.simplify(s.diff(h,t)-k*k*h-k*k/(s.exp(k*k*T)-1)) == 0

C=arb(9765625)*arb(11).sqrt()/arb(170069856)
time=arb(1)/100
def parameters(index, amplitude):
    wave=arb.pi()*index/96
    width=(-wave*wave*time).exp()
    bound=width*(amplitude*wave*wave/(1-width)+amplitude*amplitude*wave*C)
    return wave,width,bound

records=[]
for amplitude_text in ['1e-6','1']:
    amplitude=arb(amplitude_text)
    for budget_text in ['1e-12','1e-30']:
        budget=arb(budget_text)
        index=1
        while True:
            wave,width,bound=parameters(index,amplitude)
            if bound < budget:
                break
            index+=1
        assert width < arb('0.1')
        assert not parameters(index-1,amplitude)[2] < budget
        # Rounded upward decimal display bounds, separately checked in Arb.
        exponent=int(budget_text.split('e')[1])
        display_upper=budget_text
        assert bound < arb(display_upper)
        records.append(dict(amplitude=amplitude_text,residual_budget=budget_text,
                            period_index=index,wavenumber_enclosure=str(wave),
                            strip_width_enclosure=str(width),residual_upper_enclosure=str(bound),
                            verified_strict_residual_upper=display_upper,
                            terminal_v_error_exact=amplitude_text,
                            terminal_u_error_upper_enclosure=str(amplitude*width*arb(25)*arb(5).sqrt()/192)))

result=dict(precision_bits=ctx.prec,T='0.01',period='192',z_interval=[0,4],
            target='exact continuous constant solution (u,v)=(0,4)',
            coordinates='X=x-4t; transverse strip [zstar,zstar+delta] placed inside any chosen open observation interval',
            shape_F='(25 sqrt(5)/3) theta^3 (1-theta)^3, zero outside [0,1]',
            shape_f='F prime; max absolute value exactly 1',
            nonlinear_shape_product_max_exact=str(C_exact),
            nonlinear_shape_product_max_enclosure=str(C),
            symbolic_checks='passed: glued bump jets, derivative normalization and nonlinear product maximum, complete R1 and R2, antiheat forcing and endpoint data',
            examples=records,
            theorem='For every residual budget r>0 and terminal error M>0, suitable k and delta give exact same initial data and lower boundary, full nonlinear residual below r, and terminal maximum v error M. Finite transverse sample points can be avoided by strip placement.',
            limitations=['Does not alone settle the actual independently perturbed nonzero IVP.',
                         'No uniform higher-derivative or unresolved-tail bound is imposed on the approximate fields.',
                         'No two distinct exact solutions with the same initial data are constructed.'],
            continuous_independent_reference_certified=False)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
