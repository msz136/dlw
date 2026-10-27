"""Outward-rounded checks of the actual Gaussian complex-growth direction.

The all-Y statement is proved analytically in GAUSSIAN_COMPLEX_GROWTH_LEMMA.md.
Finite Fourier sums here include an explicit bound for every omitted mode.
"""
from pathlib import Path
import json
import sympy as sp
from flint import arb, acb, ctx

ctx.prec=256
xi,Y,eta=sp.symbols('xi Y eta',real=True)
assert sp.expand((-9*xi**2-xi*Y)-(-9*(xi+Y/18)**2+Y**2/36))==0
assert sp.simplify((xi*9*sp.pi/Y).subs(xi,-Y/18+eta)+sp.pi/2-9*sp.pi*eta/Y)==0

d=arb.pi()/96
C=arb.pi().sqrt()/32
alpha=arb.pi()/4
kappa=arb.pi()/2
lam=arb(1)/20
fmin=(alpha*arb(9)/10).sin()
fmax=(alpha*arb(11)/10).sin()
cosmin=(alpha*arb(11)/10).cos()
smin=lam*fmin/2
amin_u=3*alpha*(2*alpha*arb(11)/10).sin()/4
amin_v=fmin*fmin/4
Bu=2/(3*lam*fmin)
Bv=4/(lam*fmin)+2*fmax/(lam*cosmin*cosmin)
assert Bu<200 and Bv<200 and smin>0 and amin_u>0 and amin_v>0

rows=[]
for yint in (20,40,80):
    y=arb(yint)
    w=acb(9*arb.pi()/y,y)
    N=int(float(y/(18*d)))+100
    F=acb(C); J=C*w; Fx=acb(0)
    for n in range(1,N+1):
        kn=d*n
        coef=2*C*(-9*kn*kn).exp()
        F+=coef*(kn*w).cos()
        J+=coef*(kn*w).sin()/kn
        Fx-=coef*kn*(kn*w).sin()
    first=d*(N+1)
    ratio=(-9*d*d*(2*N+3)+d*y).exp()
    firsttail=(-9*first*first+first*y).exp()
    assert ratio<1 and ratio*arb(N+2)/(N+1)<1
    tailF=2*C*firsttail/(1-ratio)
    tailJ=tailF/first
    tailFx=2*C*first*firsttail/(1-ratio*arb(N+2)/(N+1))
    Flower=abs(F)-tailF
    Fupper=abs(F)+tailF
    Jreal=J.real-tailJ
    Jupper=abs(J)+tailJ
    Fxupper=abs(Fx)+tailFx
    carrier=(kappa*w).cos()
    carrierprime=-kappa*(kappa*w).sin()
    ratioE=(abs(carrierprime)/abs(carrier)+Fxupper/Flower)/Flower
    assert Flower>0 and Jreal>0 and ratioE*200<arb(1)/2
    a=min(amin_u.lower(),amin_v.lower())
    log_pair_lower=(arb(a)/2).log()+2*Flower.log()+abs(carrier).log()+smin*Jreal
    rows.append(dict(Y=yint,real_shift=str(w.real),Fourier_cutoff=N,
                     F_absolute_lower_enclosure=str(Flower),F_absolute_upper_enclosure=str(Fupper),
                     J_real_lower_enclosure=str(Jreal),J_absolute_upper_enclosure=str(Jupper),
                     all_omitted_Fourier_modes_bound=str(tailF),
                     cleared_second_to_first_coefficient_ratio_upper=str(ratioE),
                     both_directions_non_cancellation_verified=True,
                     logarithm_of_paired_growth_lower_enclosure=str(log_pair_lower)))

result=dict(date='2026-10-26',precision_bits=ctx.prec,
            symbolic_completion_and_phase_checks=True,transverse_interval=['0.9','1.1'],
            u_b_over_a_bound=str(Bu),v_b_over_a_bound=str(Bv),rows=rows,
            all_checks_passed=True,
            scope='Finite outward checks support analytic all-Y proof; not a physical reference or fixed-epsilon nonexistence certificate')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
