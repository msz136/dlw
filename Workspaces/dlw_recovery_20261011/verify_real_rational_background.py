"""Exact witnesses for nonempty full-M real zero-flux rational charts.

Finite witnesses check the universal polynomial/implicit-function proof;
they do not certify nonlinear flows or infinite Liouville completeness.
"""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone
import sympy as sp

z = sp.Symbol('z')
records = []
checks = 0

for m in range(3, 11):
    alpha = [sp.Rational(2*j-m+1, 2) for j in range(m)]
    gamma = [alpha[j] + sp.Rational(1, 3) for j in range(m-3)]
    q = sp.Poly(sp.prod(z-a for a in alpha), z)
    k = sp.Poly(sp.prod(z-g for g in gamma), z)
    a3 = sp.Rational(1, 10**m)
    r = sp.Poly(q.as_expr()+a3*k.as_expr(), z)
    radius = sp.Rational(1, 10)
    for a in alpha:
        assert r.eval(a-radius)*r.eval(a+radius) < 0
        checks += 1
    # Disjoint sign-change intervals force every root to be simple and real.
    assert q.nth(m-1) == r.nth(m-1) == 0
    assert q.nth(m-2) == r.nth(m-2)
    assert (r-q).nth(m-3) == a3
    assert sp.resultant(q, k, z) != 0
    assert sp.resultant(q, r, z) != 0
    assert sp.resultant(k, r, z) != 0
    assert k == sp.Poly(1, z) if m == 3 else sp.discriminant(k, z) != 0
    checks += 7
    # Newton sums: first two root moments agree; third differs by -3*a3.
    def power3(poly):
        c1, c2, c3 = poly.nth(m-1), poly.nth(m-2), poly.nth(m-3)
        return -c1**3 + 3*c1*c2 - 3*c3
    assert power3(r)-power3(q) == -3*a3
    checks += 1
    records.append({'M':m,'a3':str(a3),'real_root_intervals':m,
                    'K_degree':m-3,'all_exact_checks_passed':True})

result = {'purpose':'Nonempty real rational factor charts at c=Gamma=0, kappa!=0',
          'executed_at_utc':datetime.now(timezone.utc).isoformat(),
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'exact_assertions':checks,'records':records,
          'scope':'Finite certificates; universal existence follows from the saved perturbation proof.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'PASS: {checks} exact assertions for M=3,...,10.')
