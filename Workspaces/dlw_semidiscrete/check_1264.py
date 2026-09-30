"""check_1264.py -- is the N=7 failure of v4 at seed 1264 a genuine failure or a pole?

A genuine failure of a rational identity cannot happen at one generic point and
not at others.  The intersection search (nosearch_uniform.py) gives dim = 4 at
N = 7 using 3 regular samples, i.e. v2 and v4 DO satisfy the N = 7 constraints at
those samples.  So if seed 1264 fails, that point must be non-generic.
"""
import sympy as sp

from engine2 import Model, rand_point
import test_v2 as T

A = sp.Rational(5, 2)
H = sp.Rational(1, 3)
D = H / 2

N = 7
for seed, tag in ((1000 + 37 * N, 's=0'), (1000 + 37 * N + 5, 's=1')):
    m = Model(N, a=A, h=H)
    pt = rand_point(m, seed=seed)
    p = [pt[sp.Symbol('p%d' % (i + 1))] for i in range(N)]
    q = [pt[sp.Symbol('q%d' % (i + 1))] for i in range(N)]
    resid = T.residual(T.V['v4  cross-site B'], N, seed)
    bad = []
    for i in range(N):
        if p[i] - A == D or p[i] - A == -D:
            bad.append('P%d = p%d - a = +-h/2  (pole of lambda)' % (i + 1, i + 1))
        if q[i] + A == D or q[i] + A == -D:
            bad.append('Q%d = q%d + a = +-h/2  (pole of lambda)' % (i + 1, i + 1))
        for k in range(N):
            if p[i] + q[k] == 0:
                bad.append('p%d + q%d = 0  (pole of the Gram coefficient)' % (i + 1, k + 1))
    print('seed %d (%s): %d nonzero monomials' % (seed, tag, len(resid)))
    print('   p = %s' % (p,))
    print('   q = %s' % (q,))
    print('   degeneracies: %s' % (bad if bad else 'none'))
    print()
