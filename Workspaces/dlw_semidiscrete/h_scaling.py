"""h_scaling.py -- how do the uniform-class null-vector coefficients depend on h?

Theory: any uniform-class lattice identity, in the limit h->0, must become a
single-point operator proportional to B_a; in particular the coefficient of the
UNDIFFERENTIATED term (id) must tend to 0.  The canonical (rref) basis at h = 1/3
and h = 2/5 showed id = +-1, which would contradict that -- unless the canonical
normalisation hides an overall h factor.

If the id coefficients scale like h (or h^2 ...) there is no contradiction and the
extra vectors may well be genuine identities.  If they stay O(1), they must die at
some larger N.
"""
import sympy as sp

import nosearch as NS

a = sp.Rational(5, 2)
for h in (sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 5),
          sp.Rational(1, 10), sp.Rational(1, 20)):
    M, basis = NS.search(False, a, h, Ns=(1, 2, 3, 4, 5))
    print('=' * 88)
    print('UNIFORM  a=%s  h=%s : dim=%d' % (a, h, len(basis)), flush=True)
    for v in basis:
        nz = [(NS.LAB[j], sp.nsimplify(v[j])) for j in range(len(v)) if v[j] != 0]
        print('   ', nz, flush=True)
