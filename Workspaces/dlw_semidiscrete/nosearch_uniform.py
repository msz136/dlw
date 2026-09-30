"""nosearch_uniform.py -- where does the UNIFORM-class null space collapse to dim 2?

The two extra uniform-class vectors carry an undifferentiated f.g term with an
O(1) coefficient, so they cannot be all-N identities (their h->0 limit would be
the false continuum identity D_x f.g = 0).  Here we push the intersection to
larger N and watch the dimension.
"""
import sympy as sp

import nosearch as NS

av, hv = sp.Rational(5, 2), sp.Rational(1, 3)
for Ns in [(1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5), (1, 2, 3, 4, 5, 6),
           (1, 2, 3, 4, 5, 6, 7)]:
    M, basis = NS.search(False, av, hv, Ns=Ns)
    print('UNIFORM  N in %s : %d rows, rank=%d/%d, dim=%d'
          % (Ns, M.rows, M.rank(), M.cols, len(basis)), flush=True)
    for v in basis:
        nz = [(NS.LAB[j], v[j]) for j in range(len(v)) if v[j] != 0]
        print('     ', nz, flush=True)
