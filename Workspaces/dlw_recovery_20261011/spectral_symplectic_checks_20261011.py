"""Bounded independent checks of the original-physical linear symplectic bridge.

The all-M/all-frequency proofs are in spectral_independent_review_20261011.md,
sections 7-10.  These finite checks do not prove nonlinear inverse spectral or
nonlinear Liouville completeness.  Only this script and its own JSON are used.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 65
tol = mp.mpf('1e-45')
y, kap, delta = sp.symbols('y kappa delta', nonzero=True)
exact = []
for M in range(2, 9):
    m, S = M-1, M*delta
    Q, R = (y+delta)**M, (y-delta)**M
    C = (Q-R)/(2*S)
    lam = S*(Q+R)/(Q-R)
    z = sp.symbols('z')
    A = ((S-lam)*(z+delta)**M + (S+lam)*(z-delta)**M)/(2*S)
    assert sp.cancel(C*sp.diff(A, z).subs(z, y)-(y*y-delta*delta)**m) == 0
    t = sp.symbols('t')
    a = sp.expand(sp.series(lam.subs(y, 1/t), t, 0, 3).removeO()).coeff(t, 1)
    assert sp.simplify(a-(M*M-1)*delta**2/3) == 0
    assert sp.simplify(3*a-S*S+delta*delta) == 0
    exact.append({'M': M, 'companion_derivative_weight_exact': True,
                  'C2_polynomial_exact': True})

cot, cc = sp.symbols('cot c')
zeta = sp.symbols('zeta', nonzero=True)
# Use sum y_++y_-=-kappa and product -delta^2-kappa*delta*c.
prod = -delta**2-kap*delta*cc
Rprod = (prod-kap*(kap+delta)+(kap+delta)**2)/(prod-kap*delta+delta**2)
assert sp.cancel(Rprod.subs(cc, (zeta+1)/(zeta-1))-1/zeta) == 0
diff = (y+kap)**3-delta**2*(y+kap)-y**3+delta**2*y
assert sp.expand(diff-kap*(3*(y*y+kap*y-delta**2)+kap**2+2*delta**2)) == 0
Lsym, Ssym, ksym, tausym, Msym = sp.symbols('L S k tau M', nonzero=True)
Ksym = Lsym*ksym*tausym/(8*Ssym)
det_expr = (Lsym/Ssym)**2 * delta * (-2*sp.I*tausym)/(zeta*Ksym)
assert sp.cancel(det_expr.subs(Ssym, Msym*delta)+16*sp.I*Lsym/(Msym*ksym*zeta)) == 0

def max_entry(A):
    return max(abs(A[i, j]) for i in range(A.rows) for j in range(A.cols))

def frobenius(A):
    return mp.sqrt(sum(abs(A[i, j])**2 for i in range(A.rows) for j in range(A.cols)))

L = 2*mp.pi  # k0=1; same explicit small-background normalization as old checks.
pairing_checks = []
asymptotic_checks = []
normalization_count = 0
for M in range(2, 9):
    m = M-1
    for sign in [-1, 1]:
        d, S = sign*mp.mpf('0.01'), M*sign*mp.mpf('0.01')
        assert 0 < abs(d) < mp.tan(mp.pi/(2*M))/2
        norm_values, inverse_values = [], []
        for n in [1, 3, 10, 100, 10000]:
            k, kk = mp.mpf(n), mp.j*n
            for r in range(1, M):
                theta = mp.pi*r/M
                zt = mp.exp(2*mp.j*theta)
                tau = mp.sqrt(k*k/4-d*d-k*d*mp.cot(theta))
                yp, ym = -kk/2+mp.j*tau, -kk/2-mp.j*tau
                Rp, Rm = (yp+kk+d)/(yp+d), (ym+kk+d)/(ym+d)
                assert abs(Rp*Rm-1/zt) < tol
                Dp, Dm = (L/S)*Rp, (L/S)*Rm
                K = L*k*tau/(8*S)
                H = mp.matrix([[k**(-mp.mpf('0.5'))*Dp*d,
                                k**(-mp.mpf('0.5'))*Dp*yp],
                               [sign*k**mp.mpf('0.5')*Dm*d,
                                sign*k**mp.mpf('0.5')*Dm*ym]])/mp.sqrt(abs(K))
                Jsource = mp.matrix([[0, -M*kk/(16*L)], [-M*kk/(16*L), 0]])
                Jcanonical = H*Jsource*H.transpose_conj()
                assert max_entry(Jcanonical-mp.matrix([[0, 1], [-1, 0]])) < tol
                predicted_det = -16*mp.j*L/(M*k*zt)
                assert abs(mp.det(H)/predicted_det-1) < tol
                Hscaled = mp.sqrt(k)*H
                norm_values.append(frobenius(Hscaled))
                inverse_values.append(frobenius(Hscaled**-1))
                xi_a, xi_b = mp.im(yp), mp.im(yp+kk)
                assert abs(xi_a) < mp.mpf('0.5') and xi_b > mp.mpf('0.5')
                G = 2*S
                freq = ((yp+kk)**3-d*d*(yp+kk)-yp**3+d*d*yp)/(8*G)
                predicted_freq = mp.j*k*(-k*k+2*d*d+3*k*d*mp.cot(theta))/(8*G)
                assert abs(freq-predicted_freq) < tol*(1+abs(predicted_freq))
                normalization_count += 1
        asymptotic_checks.append({'M': M, 'delta': str(d),
            'n_samples': [1, 3, 10, 100, 10000],
            'max_norm_sqrt_k_H': mp.nstr(max(norm_values), 12),
            'max_norm_inverse_sqrt_k_H': mp.nstr(max(inverse_values), 12),
            'all_canonical_brackets_and_exact_determinants': True})

        # Full physical P0 pairing, including all off-diagonal channels.
        for n in [1, 3, 11]:
            k, kk = mp.mpf(n), mp.j*n
            Sp, Sm = mp.matrix(2*m, 2*M), mp.matrix(2*m, 2*M)
            Hp, Hm = mp.matrix(2*m, 2*M), mp.matrix(2*m, 2*M)
            expected_c, expected_h = mp.matrix(2*m), mp.matrix(2*m)
            for r in range(1, M):
                theta, zt = mp.pi*r/M, mp.exp(2*mp.j*mp.pi*r/M)
                tau = mp.sqrt(k*k/4-d*d-k*d*mp.cot(theta))
                for branch, yy in enumerate([-kk/2+mp.j*tau, -kk/2-mp.j*tau]):
                    row = 2*(r-1)+branch
                    W = yy*yy+kk*yy-d*d
                    u, v = W-kk*d, W+kk*d
                    Dp = (L/S)*(yy+kk+d)/(yy+d)
                    Dm = (L/S)*(yy+d)/(yy+kk+d)
                    for j in range(M):
                        fp, fm = zt**(-j), zt**j
                        Sp[row, j], Sp[row, M+j] = Dp*d*fp, Dp*yy*fp
                        Sm[row, j], Sm[row, M+j] = Dm*d*fm, Dm*(yy+kk)*fm
                        Hp[row, j], Hp[row, M+j] = v**m*d*fp, v**m*yy*fp
                        Hm[row, j], Hm[row, M+j] = u**m*d*fm, u**m*(yy+kk)*fm
                    expected_c[row, row] = -L*kk*(2*yy+kk)/(16*S)
                    expected_h[row, row] = -M*kk*d*(2*yy+kk)*(u*v)**m/(16*L)
            J = mp.matrix(2*M)
            for a in range(M):
                for b in range(M):
                    val = -kk/(16*L)*((1 if a == b else 0)-mp.mpf(1)/M)
                    J[a, M+b] = J[M+a, b] = val
            err_c = max_entry(Sp*J*Sm.T-expected_c)/max_entry(expected_c)
            err_h = max_entry(Hp*J*Hm.T-expected_h)/max_entry(expected_h)
            assert err_c < tol and err_h < tol
            pairing_checks.append({'M': M, 'delta': str(d), 'n': n,
                'full_framed_pairing_relative_error': mp.nstr(err_c, 6),
                'full_numerator_pairing_relative_error': mp.nstr(err_h, 6)})

source = Path(__file__)
out = {'purpose': 'Original-physical linear symplectic bridge only; no nonlinear completeness claim',
       'script_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
       'executed_at_utc': datetime.now(timezone.utc).isoformat(),
       'python_version': sys.version, 'sympy_version': sp.__version__,
       'mpmath_version': mp.__version__, 'mpmath_precision': mp.mp.dps,
       'exact_companion_and_C2_checks': exact,
       'symbolic_R_product_determinant_C2_frequency': True,
       'full_pairing_checks': pairing_checks,
       'canonical_high_frequency_channel_checks': normalization_count,
       'high_frequency_samples': asymptotic_checks}
source.with_suffix('.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(exact)} exact M checks; 3 symbolic identities; '
      f'{len(pairing_checks)} full physical pairing blocks; '
      f'{normalization_count} canonical channel/high-frequency checks passed.')
print('script_sha256=' + out['script_sha256'])
