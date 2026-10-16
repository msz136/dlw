"""Exact certificates for the periodic zero-lattice-mean DLW branch.

The all-M proof uses skewness of R; these finite checks catch projection,
normalization, and flux signs. They are not a Liouville completeness test.
"""
from pathlib import Path
import hashlib
import json
import sympy as sp

h = sp.symbols('h', nonzero=True)
beta = h**2 / 32
records = []
for M in range(2, 7):
    Pi = sp.ones(M) / M
    P0 = sp.eye(M) - Pi
    Eminus = sp.zeros(M)
    for j in range(M):
        Eminus[j, (j - 1) % M] = 1
    delta = (sp.eye(M) - Eminus) / h
    average = (sp.eye(M) + Eminus) / 2
    R = (delta + Pi).inv() * average * P0
    assert R + R.T == sp.zeros(M)
    assert R * sp.ones(M, 1) == sp.zeros(M, 1)
    jets = {}
    def field(prefix):
        rows = []
        for order in range(3):
            vals = [sp.Symbol(f'{prefix}{j}_{order}') for j in range(M - 1)]
            rows.append(sp.Matrix(vals + [-sum(vals)]))
        for order in range(2):
            jets.update({rows[order][j]: rows[order+1][j] for j in range(M-1)})
        return rows
    p, px, pxx = field('p')
    s, sx, sxx = field('s')
    b, bx = sp.symbols('b bx')
    jets[b] = bx
    def D(expr):
        return sp.expand(sum(sp.diff(expr, v) * dv for v, dv in jets.items()))
    def mean(exprs):
        return sum(exprs) / M
    q = mean([p[j]*s[j] for j in range(M)])
    qx = D(q)
    f = sp.Matrix([p[j]**2/2 + beta*s[j]**2 for j in range(M)])
    pt = -sp.Matrix([D(b*p[j]) for j in range(M)]) - P0*sp.Matrix([D(z) for z in f]) - pxx - R*sxx
    st = -sp.Matrix([D(b*s[j]) for j in range(M)]) - P0*sp.Matrix([D(p[j]*s[j]) for j in range(M)]) + sxx
    chi = mean([-p[j]**2*s[j] - 2*beta*s[j]**3/3 + p[j]*sx[j] - s[j]*px[j] - s[j]*(R*sx)[j] for j in range(M)])
    qdot = mean([s[j]*pt[j] + p[j]*st[j] for j in range(M)])
    assert sp.expand(qdot + 2*q*bx + b*qx - D(chi)) == 0
    e = mean([p[j]**2*s[j]/2 + beta*s[j]**3/3 + s[j]*px[j] + s[j]*(R*sx)[j]/2 for j in range(M)])
    assert sp.expand(chi + 2*e - qx) == 0
    multiplier_qdot = mean([s[j]*(-D(b*p[j])) + p[j]*(-D(b*s[j])) for j in range(M)])
    assert sp.expand(multiplier_qdot + 2*q*bx + b*qx) == 0
    records.append({'M': M, 'skew_R': True, 'q_flux_identity': True, 'chi_energy_identity': True, 'constraint_bracket': True})

out = {
    'status': 'all exact checks passed',
    'sympy': sp.__version__,
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'checks': records,
    'scope': 'Finite exact algebra checks; all-M proof is skew-matrix flux calculus. No spectral completeness or nonlinear time-flow claim.'
}
Path(__file__).with_name('zero_mean_branch_checks.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(out['status'], len(records), 'lattice periods')
