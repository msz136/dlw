"""Two bounded direct original rank-one monodromy checks, M=2.

Unlike the scalar/split equations, the integrated coefficients use only b,d.
This independently checks the stronger fixed-original-frame constant tail.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
import scipy
from scipy.integrate import solve_ivp

L, delta, epsilon = 2*np.pi, 0.1, 0.025
S = 2*delta
slow_limit = np.exp(-epsilon**2*L/S)
coefficient = -epsilon*(slow_limit-1)/S
Tbg = np.array([[0.5, 1], [0.5, -1]], dtype=complex)
records = []
for k in [40, 160]:
    tau = np.sqrt(k*k/4-delta*delta)
    lam = 2j*tau
    zs, zf = -1j*k/2+1j*tau, 1j*k/2+1j*tau
    Gbg = np.array([[1, 0], [lam, -S]], dtype=complex)
    E0 = np.array([[1, 1], [zs, zf]], dtype=complex)
    Eoriginal = Tbg@np.linalg.inv(Gbg)@E0
    def rhs(x, y):
        u = v = epsilon*np.cos(x)
        d0, d1 = delta+v, delta-v
        q = -S+u
        b1 = -d0-d0*q/S
        b0 = b1+q+S
        projector = np.array([[d0, d0], [d1, d1]], dtype=complex)/S
        C = np.array([[b0, d0], [-d1, b1]], dtype=complex)
        return ((lam*projector+C)@y.reshape(2, 2)).reshape(4)
    sol = solve_ivp(rhs, (0, L), np.eye(2, dtype=complex).reshape(4),
                    method='DOP853', rtol=2e-12, atol=2e-13)
    assert sol.success
    Tphysical = sol.y[:, -1].reshape(2, 2)
    block = np.linalg.inv(Eoriginal)@Tphysical@Eoriginal
    cplus = block[1, 0]/np.exp(zs*L)
    relative_error = abs(cplus-coefficient)/abs(coefficient)
    K = L*k*tau/(8*S)
    Qraw = k**(-0.5)*cplus/np.sqrt(K)
    records.append({'k': k, 'solver_rhs_calls': sol.nfev,
                    'cplus_original_real': float(cplus.real),
                    'cplus_original_imag': float(cplus.imag),
                    'relative_error_to_proven_constant_tail': float(relative_error),
                    'k_power_1_5_Q_real': float((k**1.5*Qraw).real),
                    'k_power_1_5_Q_imag': float((k**1.5*Qraw).imag)})
assert records[-1]['relative_error_to_proven_constant_tail'] < 0.05
assert records[-1]['relative_error_to_proven_constant_tail'] < records[0]['relative_error_to_proven_constant_tail']
source = Path(__file__)
out = {'purpose': 'Direct original fixed rank-one frame has constant monodromy tail; no nonlinear inverse claim',
       'script_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
       'executed_at_utc': datetime.now(timezone.utc).isoformat(),
       'scipy_version': scipy.__version__, 'delta': delta, 'epsilon': epsilon,
       'L': L, 'slow_holonomy_limit': float(slow_limit),
       'proven_constant_tail_coefficient': float(coefficient),
       'original_frame_monodromy_checks': records}
source.with_suffix('.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print('2 direct original b,d-only rank-one monodromy checks passed.')
print(json.dumps({'constant_tail_coefficient': coefficient,
                  'last_relative_error': records[-1]['relative_error_to_proven_constant_tail']}))
print('script_sha256=' + out['script_sha256'])
