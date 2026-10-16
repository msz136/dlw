"""Independent exact/numerical checks for the full-M Floquet tangent bridge.

The all-M proof is in spectral_independent_review_20261011.md.  These checks
do not claim nonlinear inverse spectral or Liouville completeness.
"""
from pathlib import Path
import json
import sympy as sp
import mpmath as mp

y, kap, delta = sp.symbols('y kappa delta', nonzero=True)
records = []
for M in range(2, 9):
    m = M - 1
    S = M * delta
    Q = (y + delta) ** M
    R = (y - delta) ** M
    Qs = (y + kap + delta) ** M
    Rs = (y + kap - delta) ** M
    p, ps = R / Q, Rs / Qs
    C, Cs = (Q - R) / (2 * S), (Qs - Rs) / (2 * S)
    W = y * y + kap * y - delta * delta
    u, v = W - kap * delta, W + kap * delta
    assert sp.expand(Rs * Q - R * Qs - (v ** M - u ** M)) == 0
    # Arbitrary numerator: exact Frechet/Mobius/pencil identity is linear in it.
    test_N = sum(sp.Rational(j + 1, j + 2) * y ** j for j in range(2*m))
    dp = -2 * test_N / (Qs * Q)
    dL = 2 * S * dp / ((ps - 1) * (p - 1))
    assert sp.cancel(Cs * dL + test_N / (S * C)) == 0
    records.append({'M': M, 'resonance_polynomial_identity': True,
                    'pencil_coupling_identity': True})

k, cot = sp.symbols('k cot', real=True)
omega_sq = kap ** 4 + 4 * delta ** 2 * kap ** 2 + 4 * delta * (-sp.I*cot) * kap**3
disc = k ** 4 - 4 * delta * cot * k ** 3 - 4 * delta ** 2 * k ** 2
assert sp.expand(omega_sq.subs(kap, sp.I*k) - disc) == 0

mp.mp.dps = 70
numerical = []
for M in range(2, 9):
    m = M-1
    d = mp.mpf('0.371')
    for n in range(1, 5):
        kk = mp.j*n  # L=2*pi
        roots = []
        for r in range(1, M):
            cc = -mp.j * mp.cot(mp.pi*r/M)
            root = mp.sqrt(kk*kk/4 + d*d + kk*d*cc)
            roots.extend([-kk/2 + root, -kk/2 - root])
        # Source columns alpha_0,...,alpha_{m-1}, beta_0,...,beta_{m-1};
        # last lattice component is negative sum.  N(y) from ordered product.
        V = mp.matrix(2*m, 2*m)
        for row, yy in enumerate(roots):
            WW = yy*yy + kk*yy - d*d
            Fs = [(WW + kk*d)**(m-j)*(WW-kk*d)**j for j in range(M)]
            for j in range(m):
                V[row, j] = d*(Fs[j]-Fs[m])
                V[row, m+j] = yy*(Fs[j]-Fs[m])
        actual = mp.det(V)
        det_coeff = (-1)**(m*(m-1)//2)*d**m*(2*kk*d)**(m*(m+1))
        vand = mp.mpf(1)
        for a in range(2*m):
            for b in range(a+1, 2*m):
                vand *= roots[b]-roots[a]
        ratio_error = abs(actual/(det_coeff*vand)-1)
        min_C = min(abs(((zz+d)**M-(zz-d)**M)/(2*M*d)) for zz in roots)
        min_gap = min(abs(roots[b]-roots[a]) for a in range(2*m) for b in range(a+1, 2*m))
        assert ratio_error < mp.mpf('1e-48')
        assert min_C > mp.mpf('1e-20') and min_gap > mp.mpf('1e-20')
        numerical.append({'M': M, 'n': n,
                          'evaluation_determinant_ratio_error': mp.nstr(ratio_error, 8),
                          'min_C_at_resonances': mp.nstr(min_C, 8),
                          'min_resonance_root_gap': mp.nstr(min_gap, 8)})

out = {'purpose': 'Floquet tangent bridge; no completeness claim',
       'exact_checks': records, 'physical_dispersion_identity': True,
       'numerical_checks': numerical}
z = sp.symbols('z')
companion_checks = []
for M in range(2, 8):
    # Test the general companion left-eigenvector normalization underlying
    # the Floquet variation formula, with an exactly resonant spatial pair.
    roots_exact = [sp.Rational(1, 3), sp.Rational(1, 3)+sp.I]
    roots_exact += [sp.Rational(j+2, 1) for j in range(M-2)]
    char = sp.prod(z-root for root in roots_exact).expand()
    forcing = sum(sp.Rational(j+2, j+3)*z**j for j in range(M))
    E = sp.Matrix([[root**j for root in roots_exact] for j in range(M)])
    perturb = sp.zeros(M)
    for j in range(M):
        perturb[M-1, j] = -forcing.coeff(z, j)
    eig_perturb = E.inv()*perturb*E
    for a in range(M):
        for b in range(M):
            predicted = -forcing.subs(z, roots_exact[a])/sp.diff(char, z).subs(z, roots_exact[b])
            assert sp.cancel(eig_perturb[b, a]-predicted) == 0
    companion_checks.append({'M': M, 'all_companion_coupling_entries_exact': True})
out['companion_checks'] = companion_checks
small_background_checks = []
for M in range(2, 9):
    d = mp.mpf('0.01')
    bound = mp.tan(mp.pi/(2*M))/2  # k0=1
    assert d < bound
    endpoints = []
    for n in range(1, 5):
        kk = mp.j*n
        for r in range(1, M):
            cc = -mp.j*mp.cot(mp.pi*r/M)
            radical = kk*kk/4+d*d+kk*d*cc
            assert abs(mp.im(radical)) < mp.mpf('1e-60') and mp.re(radical) < 0
            ss = mp.sqrt(radical)
            for yy in [-kk/2+ss, -kk/2-ss]:
                assert abs(mp.re(yy)) < mp.mpf('1e-60')
                endpoints.extend([yy, yy+kk])
    endpoint_gap = min(abs(endpoints[b]-endpoints[a])
                       for a in range(len(endpoints))
                       for b in range(a+1, len(endpoints)))
    assert endpoint_gap > mp.mpf('1e-40')
    small_background_checks.append({'M': M, 'delta': '0.01',
                                    'small_background_bound': mp.nstr(bound, 8),
                                    'sampled_endpoints_distinct': True,
                                    'min_endpoint_gap': mp.nstr(endpoint_gap, 8)})
out['small_background_checks'] = small_background_checks
target = Path(__file__).with_suffix('.json')
target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(records)} exact all-period instances; dispersion identity; '
      f'{len(numerical)} resonance interpolation checks; '
      f'{len(companion_checks)} exact companion checks; '
      f'{len(small_background_checks)} small-background checks passed.')
