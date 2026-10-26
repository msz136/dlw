"""Validate an actual mixed-time DLW existence contraction, not the original IVP."""
from pathlib import Path
import sys,json
import numpy as np
from flint import arb,acb,ctx
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'canonical_reference'))
from solve import Solver
ctx.prec=256

def exact_complex(c):
    return acb(arb(float(c.real)),arb(float(c.imag)))

def derivative(coefficients):
    n=len(coefficients)-1
    out=[acb(0) for _ in range(n)]
    out[-1]=2*n*coefficients[n]
    if n>1: out[-2]=2*(n-1)*coefficients[n-1]
    for j in range(n-3,-1,-1): out[j]=out[j+2]+2*(j+1)*coefficients[j+1]
    out[0]/=2
    return out+[acb(0)]

T=arb(1)/100;rho=arb(1)/10;R=arb(7)/10;datum_cap=arb(15)/100
H=(T/2).sqrt();inverse_bound=(16*H).exp()
image_bound=inverse_bound*(datum_cap+2*H*R**2)
contraction=4*H*inverse_bound*R
assert image_bound<R and contraction<1
assert image_bound<arb('.681') and contraction<arb('.615')
results=[]
for case,M in [('Sinusoidal',32),('Gaussian',128)]:
    solver=Solver(case,M,24)
    path=HERE/'canonical_reference'/f'{case}_M{M}_Y24_dt5.0e-05.npz'
    with np.load(path) as data:
        last=data['coefficients'][-1].reshape(2,25,2*M+1)
    coefficients=solver.C@last
    # These rounded endpoint Chebyshev numbers define exact terminal data.
    terminal_norm=arb(0)
    polynomial_zero_mode_bound=arb(0)
    for index,n in enumerate(solver.modes):
        u=[exact_complex(c) for c in coefficients[0,:,index]]
        w=[exact_complex(c) for c in coefficients[1,:,index]]
        aa=[du+wi for du,wi in zip(derivative(u),w)]
        frequency=abs(2*arb.pi()*int(n)/int(solver.P))
        contribution=sum(abs(c) for c in aa)*(rho*frequency).exp()
        terminal_norm+=contribution
        if int(n)==0: polynomial_zero_mode_bound=contribution
    if case=='Sinusoidal':
        # |b_{+1}|=sqrt(c^2 cos^2(kappa z)+B^2 sin^2(kappa z))/2.
        initial_norm=(arb(3)/100*arb.pi()/4)*(rho*arb.pi()/12).exp()
        assert arb(3)/100*arb.pi()/4>arb(2)/100
        exact_zero_mode_bound=arb(0)
    else:
        c=arb(5)/100*arb.pi()/4;v=arb(3)/100
        amplitude=(c*c+v*v).sqrt();cg=arb.pi().sqrt()/32;d=arb.pi()/96
        # rho*r <= r^2+rho^2/4; Gaussian lattice sum by integral comparison.
        initial_norm=amplitude*cg*(rho*rho/4).exp()*(1+arb.pi().sqrt()/(arb(8).sqrt()*d))
        exact_zero_mode_bound=amplitude*cg
    total=terminal_norm+initial_norm
    assert total<datum_cap
    corrected_terminal=terminal_norm-polynomial_zero_mode_bound+exact_zero_mode_bound
    corrected_total=corrected_terminal+initial_norm
    assert corrected_total<datum_cap
    results.append({'case':case,'terminal_a_source':path.name,
                    'terminal_a_analytic_wiener_bound':str(terminal_norm),
                    'exact_initial_b_analytic_wiener_bound':str(initial_norm),
                    'total_datum_bound':str(total),'less_than_0_15':True,
                    'mean_compatible_terminal_definition':'Replace the candidate terminal a zero Fourier mode by the exact original a0 zero mode; retain all nonzero modes',
                    'mean_compatible_terminal_norm_bound':str(corrected_terminal),
                    'mean_compatible_total_datum_bound':str(corrected_total),
                    'mean_compatible_total_less_than_0_15':True})

result={'problem':'a(T) from candidate and b(0) from exact actual initialization; a(0) is NOT imposed',
        'rho':'0.1','T':'0.01','radius':'0.7','datum_cap':'0.15',
        'H_bound':str(H),'linear_volterra_inverse_bound':str(inverse_bound),
        'fixed_point_image_norm_bound':str(image_bound),
        'contraction_constant_bound':str(contraction),
        'cases':results,'mixed_problem_certified_by_proof_and_constants':True,
        'original_initial_value_problem_certified':False,'eta_u':None,'eta_v':None,
        'review_status':'self-reviewed proof plus 256-bit constants, not independent or formal verification'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
