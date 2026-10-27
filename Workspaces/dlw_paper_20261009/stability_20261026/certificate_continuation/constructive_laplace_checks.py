"""Symbolic checks for the data-specific finite-Laplace-chain obstruction.

This does not certify a perturbed PDE trajectory or establish its nonexistence.
"""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent

def main():
    x,z=s.symbols('x z',real=True)
    Q=s.Function('Q')(x,z);P=s.Function('P')(x,z)
    P1=P-s.diff(Q,z);Q1=Q-s.diff(P1,x)/P1
    P2=P1-s.diff(Q1,z)
    recurrence=2*P1-P+s.diff(s.diff(P1,x)/P1,z)
    assert s.simplify(P2-recurrence)==0

    A,kap,eu,ev=s.symbols('A kappa epsilon_u epsilon_v',real=True,nonzero=True)
    F=s.Function('F')(x);C=s.Function('C')(x)
    w=s.symbols('w',nonzero=True)
    sin=(w-1/w)/(2*s.I);cos=(w+1/w)/2
    phi=(2-w*w-w**-2)/4
    Dz=lambda a:s.I*kap*w*s.diff(a,w)
    ub=A*sin*F;vb=4-3*A*kap*cos*F
    u=ub+eu*phi*C;v=vb+ev*phi*C
    p0=s.expand((v-4-Dz(u))/4)
    p1=s.expand((v-4+Dz(u))/4)
    l0=s.expand(w*w*p0);l1=s.expand(w*w*p1)
    c0=s.simplify(l0.subs(w,0))
    c1=s.simplify(l1.subs(w,0))
    assert s.simplify(c0-C*(-ev/16-s.I*kap*eu/8))==0
    assert s.simplify(c1-C*(-ev/16+s.I*kap*eu/8))==0

    b0=s.simplify(p0.subs({eu:0,ev:0}))
    b1=s.simplify(p1.subs({eu:0,ev:0}))
    crosslog=lambda a:Dz(s.diff(a,x)/a)
    assert s.simplify(2*b1-b0+crosslog(b1))==0

    # Exact one-step check: no third-or-higher negative w power appears,
    # and the expected nonzero w^-2 coefficient survives the log derivative.
    # Write p1=w^-2*l1. The cross-log derivative has an explicit factor w
    # and denominator l1^2, nonzero at w=0. Avoid a large generic limit.
    logterm=s.I*kap*w*(s.diff(l1,x,w)*l1-s.diff(l1,x)*s.diff(l1,w))/(l1*l1)
    assert s.simplify(l1.subs(w,0)-c1)==0
    assert s.simplify(logterm.subs(w,0))==0
    c2=s.simplify(2*c1-c0)
    assert s.simplify(c2-C*(-ev/16+3*s.I*kap*eu/8))==0

    j=s.symbols('j',integer=True)
    cj=lambda a:C*(-ev/16+(2*a-1)*s.I*kap*eu/8)
    assert s.simplify(cj(j+1)-2*cj(j)+cj(j-1))==0
    gamma_a=[s.Rational(1,1-2)+s.Rational(1,2+2)]
    gamma_d=[s.Rational(1,1-2)+s.Rational(1,2+2),s.Rational(1,4-2)+s.Rational(1,-3+2)]
    for gamma in gamma_a+gamma_d:
        assert s.simplify(s.exp(8*s.pi*s.I*gamma)-1)==0
    checks={
      'inverse_laplace_recurrence':True,
      'physical_to_BLP_initial_invariants':True,
      'unperturbed_P2_identically_zero':True,
      'first_log_term_has_no_negative_leading_power':True,
      'all_integer_leading_coefficient_recurrence':True,
      'A_transverse_exponents':[str(a) for a in gamma_a],
      'D_transverse_exponents':[str(a) for a in gamma_d],
      'A_D_tau_imaginary_period_8_pi':True,
      'leading_coefficient':str(cj(j)),
      'scope':'finite termination of the specified Laplace chain for current sine/Gaussian and A/D independent perturbations; A/D extension uses verified imaginary periods',
      'nonexistence_of_full_PDE_proved':False,
      'full_reference_certified':False,'eta_u':None,'eta_v':None}
    (HERE/'constructive_laplace_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf8')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
