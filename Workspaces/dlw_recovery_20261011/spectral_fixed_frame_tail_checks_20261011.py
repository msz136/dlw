"""Bounded M=2 check of the fixed-background nonlinear framed-sample tail.

The proof is an explicit high-parameter block-diagonalization in section 11 of
spectral_independent_review_20261011.md.  This checks its asymptotic coefficient
against actual monodromy integration, and is not an inverse spectral theorem.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as sp

S, d, q = sp.symbols('S d q', nonzero=True)
b1 = -d-d*q/S
b0 = b1+q+S
V = b0-d-d*q/S
assert sp.simplify(V-(S-2*d)*(1+q/S)) == 0
x, eps, delt = sp.symbols('x eps delta', real=True)
example_V = sp.simplify(V.subs({d: delt+eps*sp.sin(x), q: -S+eps*sp.sin(x)}, simultaneous=True).subs(S, 2*delt))
assert sp.simplify(example_V+eps**2*sp.sin(x)**2/delt) == 0

L, delta, epsilon = 2*np.pi, 0.1, 0.025
S = 2*delta
assert 0 < delta < 0.5 and 0 < epsilon < S
qbase = -S
mu_slow_infinity = np.exp(-epsilon**2*L/S)
W_basepoint = -epsilon/S
coefficient = W_basepoint*(mu_slow_infinity-1)
records = []
for k in [20, 40, 80, 160]:
    tau = np.sqrt(k*k/4-delta*delta)
    lam = 2j*tau
    zs, zf = -1j*k/2+1j*tau, 1j*k/2+1j*tau
    def rhs(xx, yy):
        sn, cs = np.sin(xx), np.cos(xx)
        d0 = delta+epsilon*sn
        qq = -S+epsilon*sn
        d0x = epsilon*cs
        rr = (d0*(S-d0)*(2+qq/S)-d0x)/S
        vv = (S-2*d0)*(1+qq/S)
        A = np.array([[lam, qq], [rr, vv]], dtype=complex)
        return (A@yy.reshape(2, 2)).reshape(4)
    sol = solve_ivp(rhs, (0, L), np.eye(2, dtype=complex).reshape(4),
                    method='DOP853', rtol=2e-12, atol=2e-13)
    assert sol.success
    Tphysical = sol.y[:, -1].reshape(2, 2)
    G = np.array([[1, 0], [lam, qbase]], dtype=complex)
    Tcompanion = G@Tphysical@np.linalg.inv(G)
    Ebackground = np.array([[1, 1], [zs, zf]], dtype=complex)
    cplus = (np.linalg.inv(Ebackground)@Tcompanion@Ebackground)[1, 0]/np.exp(zs*L)
    scaled = lam*cplus
    relative_error = abs(scaled-coefficient)/abs(coefficient)
    records.append({'k': k, 'solver_rhs_calls': sol.nfev,
                    'lambda_times_cplus_real': float(scaled.real),
                    'lambda_times_cplus_imag': float(scaled.imag),
                    'relative_error_to_proven_leading_coefficient': float(relative_error)})
assert records[-1]['relative_error_to_proven_leading_coefficient'] < 0.05
assert records[-1]['relative_error_to_proven_leading_coefficient'] < records[0]['relative_error_to_proven_leading_coefficient']
source = Path(__file__)
out = {'purpose': 'Fixed-background nonlinear monodromy sample has an algebraic tail; no nonlinear inverse claim',
       'script_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
       'executed_at_utc': datetime.now(timezone.utc).isoformat(),
       'python_version': sys.version, 'scipy_version': scipy.__version__,
       'symbolic_V_identity_exact': True,
       'delta': delta, 'epsilon': epsilon, 'L': L,
       'slow_holonomy_limit': float(mu_slow_infinity),
       'W_basepoint': float(W_basepoint),
       'proven_nonzero_tail_coefficient': float(coefficient),
       'monodromy_checks': records}
source.with_suffix('.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print('Exact V identity and 4 bounded actual monodromy integrations passed.')
print(json.dumps({'tail_coefficient': coefficient,
                  'last_relative_error': records[-1]['relative_error_to_proven_leading_coefficient']}))
print('script_sha256=' + out['script_sha256'])
