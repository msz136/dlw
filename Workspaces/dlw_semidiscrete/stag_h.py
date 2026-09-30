"""stag_h.py -- is the STAGGERED dim-4 result stable across h?

uni_identity.py shows that the extra UNIFORM-class cross-site vector vanishes at
h = 1/3 and h = 1/4 but NOT at h = 1/2 (for N = 3,4).  So a null-space search
performed at a single fixed h can pick up vectors that are zero only at that h --
they are not identities.

Here we redo the STAGGERED search at several h to check that its null space is
always the same 4-dimensional span, namely

   (7)_h at site j ,  (7)_h at site j+1 ,  (6)_h at (j,j+1) ,  (6)_h at (j-1,j) .
"""
import sympy as sp

import nosearch as NS

a = sp.Rational(5, 2)

for h in (sp.Rational(1, 2), sp.Rational(3, 7), sp.Rational(1, 3),
          sp.Rational(1, 5), sp.Rational(1, 10)):
    d = h / 2
    M, basis = NS.search(True, a, h, Ns=(1, 2, 3, 4, 5))
    print('=' * 88)
    print('STAGGERED  a=%s  h=%s  (d=%s) : dim=%d' % (a, h, d, len(basis)))
    for v in basis:
        nz = [(NS.LAB[j], sp.nsimplify(v[j])) for j in range(len(v)) if v[j] != 0]
        print('   ', nz)
    print('   (a-d = %-6s   a+d = %s)' % (a - d, a + d))
