"""Validated Cole-Hopf reference for NEW compatible DLW data, not original data.

All transcendental operations and polynomial coefficients use Arb/Acb balls.
Analytic truncation bounds apply on the full continuous space-time cylinder.
Usage: python reference.py [--case sine|gaussian --x 0 --z 1 --t .01]
"""
from pathlib import Path
import argparse
import json
import math
from fractions import Fraction
from flint import arb, acb, acb_poly, ctx

ctx.prec = 256
M = 32


def parameters(case):
    kappa = arb.pi()/4
    if case == 'sine':
        return arb(3)/100, arb.pi()/12, arb(0), 1, kappa
    return arb(1)/20, arb.pi()/96, arb.pi().sqrt()/32, 96, kappa


def bounds(case):
    A, w, C, K, kappa = parameters(case)
    if case == 'sine':
        Jnorm = (1+w)**2/w
        Jtail = arb(0)
    else:
        alpha = 9*w*w
        Jnorm = sum((2*C*(-alpha*n*n).exp()*(1+w*n)**2/(w*n)
                     for n in range(1, K+1)), arb(0))
        n = K+1
        # Ratios of successive positive tail summands <= 4 exp(-alpha(2K+3)).
        ratio = 4*(-alpha*(2*K+3)).exp()
        assert ratio < 1
        Jtail = 2*C*(-alpha*n*n).exp()*(1+w*n)**2/(w*n)/(1-ratio)
    R = A*(1+kappa)*(Jnorm+Jtail)/2
    e = A*(1+kappa)*Jtail/2
    delta = R.exp()*(e + R**(M+1)/math.factorial(M+1))
    assert R < arb('0.5')
    assert delta < arb('1e-35')
    # Conservative bound for BOTH physical fields, derived in PROOF.md.
    eta = 1000*delta
    assert eta < arb('1e-32')
    return {'R': str(R), 'fourier_primitive_tail': str(Jtail),
            'heat_derivative_error_delta': str(delta),
            'physical_truncation_error_each': str(eta)}, eta


def shifted(p, k):
    return acb_poly([0]*k + list(p))


def evaluate(case, x='0', z='1', t='.01'):
    """Return full-error real balls at a rational/decimal (x,z,t).

    z=y+2; 0<=z<=4, 0<=t<=.01. x is in physical, not moving coordinates.
    The reported ball includes finite-evaluation rounding AND analytic tails.
    """
    A, w, C, K, kappa = parameters(case)
    assert 0 <= Fraction(z) <= 4 and 0 <= Fraction(t) <= Fraction(1, 100)
    x, z, t = arb(x), arb(z), arb(t)
    _, eta = bounds(case)
    s = -A*(kappa*z).sin()/2
    sz = -A*kappa*(kappa*z).cos()/2
    mu = A*C*(kappa*z).sin()
    muz = A*C*kappa*(kappa*z).cos()
    coeffs = [acb(0) for _ in range(2*K+1)]
    for n in range(1, K+1):
        f = arb(1)/2 if case == 'sine' else C*(-9*(w*n)**2).exp()
        coeffs[K+n] = acb(0, -f/(w*n))
        coeffs[K-n] = acb(0, f/(w*n))
    J = acb_poly(coeffs)
    term, termz = acb_poly([1]), acb_poly([0])
    Q, Qz = acb_poly([1]), acb_poly([0])
    for m in range(1, M+1):
        termz = J*(s*termz+sz*term)*(arb(1)/m)
        term = J*term*(s/m)
        Q = shifted(Q, K)+term
        Qz = shifted(Qz, K)+termz
    Y = x-4*t-mu*t
    H = Hx = Hxx = Hz = Hxz = acb(0)
    center = K*M
    for j in range(2*center+1):
        freq = w*(j-center)
        e = acb(-freq*freq*t, freq*Y).exp()
        d = acb(0, freq)
        h, hz = Q[j]*e, Qz[j]*e
        H += h
        Hx += d*h
        Hxx += d*d*h
        Hz += hz
        Hxz += d*hz
    u = mu-2*Hx/H
    uz = muz-2*((Hxz-muz*t*Hxx)/H-Hx*(Hz-muz*t*Hx)/(H*H))
    v = 4-uz
    assert u.imag.contains(0) and v.imag.contains(0)
    assert u.real.rad() < arb('1e-40') and v.real.rad() < arb('1e-40')
    # 1e-32 is a strictly outward, decimal envelope of the analytic tail.
    enlargement = arb('0 +/- 1e-32')
    ufull, vfull = u.real+enlargement, v.real+enlargement
    assert ufull.rad() < arb('1.01e-32') and vfull.rad() < arb('1.01e-32')
    return {'case': case, 'x': str(x), 'z': str(z), 't': str(t),
            'u': str(ufull), 'v': str(vfull),
            'u_radius': str(ufull.rad()), 'v_radius': str(vfull.rad()),
            'finite_eval_roundoff_u': str(u.real.rad()),
            'finite_eval_roundoff_v': str(v.real.rad())}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['sine', 'gaussian'])
    parser.add_argument('--x', default='0')
    parser.add_argument('--z', default='1')
    parser.add_argument('--t', default='.01')
    args = parser.parse_args()
    if args.case:
        print(json.dumps(evaluate(args.case, args.x, args.z, args.t), indent=2))
    else:
        result = {
            'scope': 'New compatible data v0=4-u0_z; original data remain unresolved.',
            'proof_status': 'Self-reviewed analytic proof with Arb evaluation; not formal verification.',
            'domain': 'x periodic 192, 0<=z<=4, 0<=t<=0.01',
            'M': M, 'precision_bits': ctx.prec,
            'uniform_bounds': {case: bounds(case)[0] for case in ['sine', 'gaussian']},
            'samples': [evaluate(case) for case in ['sine', 'gaussian']],
        }
        Path(__file__).with_name('certificate.json').write_text(
            json.dumps(result, indent=2), encoding='utf-8')
        print(json.dumps(result, indent=2))
