"""Validate background constants for exact-initial fields built from candidates.

Rounded Bernstein/Chebyshev coefficients define an exact polynomial. This does
not assert their interpolation is exact, nor that they approximate a PDE solution.
"""
from pathlib import Path
import sys,json
import numpy as np
from flint import arb,acb,ctx

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'canonical_reference'))
from solve import Solver
ctx.prec=192

def exact_complex(c):
    return acb(arb(float(c.real)),arb(float(c.imag)))

def maxima(current,values):
    # Max of upper endpoints is safe even if input interval balls overlap.
    return [max(x.upper(),y.upper()) for x,y in zip(current,values)]

# Coarse rigorous bounds for the exact initial profiles, for both cases.
d=arb.pi()/96
cg=arb.pi().sqrt()/32
g_bound=cg*(1+arb.pi().sqrt()/(3*d))
gx_bound=cg/(3*arb(1).exp().sqrt())*(1+(2*arb.pi()/9).sqrt()/d)
assert g_bound<2 and gx_bound<1
kappa=arb.pi()/4; omega=arb.pi()/12
assert arb('.05')*kappa*2<arb('.1')
assert arb('.05')*kappa*gx_bound<arb('.1')
assert (arb('.05')*kappa+arb('.03'))*2<arb('.2')
assert (arb('.05')*kappa+arb('.03'))*gx_bound<arb('.2')
assert arb('.03')*kappa<arb('.1')
assert arb('.03')*kappa*omega<arb('.1')
assert arb('.03')*kappa+arb('.02')<arb('.2')
assert (arb('.03')*kappa+arb('.02'))*omega<arb('.2')

results=[]
for case,M in [('Sinusoidal',32),('Gaussian',128)]:
    solver=Solver(case,M,24)
    path=HERE/'canonical_reference'/f'{case}_M{M}_Y24_dt5.0e-05.npz'
    with np.load(path) as data:
        times=data['times'];states=data['coefficients']
    states=states.reshape(len(times),2,25,2*M+1)
    rhs=[solver.rhs(float(t),z.ravel()).reshape(2,25,2*M+1) for t,z in zip(times,states)]
    endpoint_coefficients=[solver.C@state for state in states]
    endpoint_derivatives=[solver.C@state for state in rhs]
    maxima4=[arb(0)]*4
    freqs=[abs(2*arb.pi()*int(n)/int(solver.P)) for n in solver.modes]
    for j in range(10):
        # Rounded endpoint coefficients/derivatives are defined as exact numbers.
        # Rational Bernstein operations enforce exact C1 joins at j/1000.
        for control_index in range(4):
            endpoint=j if control_index<2 else j+1
            pp=arb(0);ppx=arb(0);ww=arb(0);wwx=arb(0)
            for degree in range(25):
                derivative_weight=arb(degree*degree)/2
                for mode,frequency in enumerate(freqs):
                    coeffs=[exact_complex(endpoint_coefficients[endpoint][field,degree,mode]) for field in (0,1)]
                    if control_index in (1,2):
                        sign=1 if control_index==1 else -1
                        coeffs=[value+sign*exact_complex(endpoint_derivatives[endpoint][field,degree,mode])/3000 for field,value in enumerate(coeffs)]
                    uabs,wabs=map(abs,coeffs)
                    pp+=derivative_weight*uabs
                    ppx+=derivative_weight*uabs*frequency
                    ww+=wabs
                    wwx+=wabs*frequency
            maxima4=maxima(maxima4,[pp,ppx,ww,wwx])
    pp,ppx,ww,wwx=maxima4
    # U=P_u(t)-P_u(0)+u0, V=P_v(t)-P_v(0)+v0;
    # P_v=(P_u)_z+P_w. Exact subtraction of P_u(z=0) enforces lower U=0.
    bounds={'P':2*pp+arb('.1'),'Q':2*ppx+arb('.1'),
            'M_a':2*(2*pp+ww)+arb('.2'),'M_b':2*ww+arb('.2'),
            'N_a':2*(2*ppx+wwx)+arb('.2'),'N_b':2*wwx+arb('.2')}
    assert all(value<1 for value in bounds.values()),bounds
    results.append({'case':case,'source':path.name,
                    'background_bounds':{key:str(value) for key,value in bounds.items()},
                    'all_six_strictly_below_one':True})
result={'definition':'Exact rounded Chebyshev endpoint values and derivatives; exact rational cubic Bernstein controls enforce C1 time joins; lower-u corrected exactly; then add exact initial profile minus polynomial initial profile to each physical field',
        'coordinate':'Bounds invariant under X=x-4t; apply in moving coordinates',
        'initial_and_boundary':'Exact original initialization and u=0 lower boundary',
        'arb_precision_bits':ctx.prec,'results':results,
        'meaning':'Proves applicability of residual-change example to these constructed baselines; does not bound baseline PDE residual or error to a true solution',
        'continuum_reference_certified':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
