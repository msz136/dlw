"""
test_v2.py -- are the two "extra" uniform-class vectors genuine for all N?

The intersection search at N <= 5 gives dim = 4 for the UNIFORM class
(f = tau_1 with coefficient parameter a):

   v1 = (7) at site j          (Dx2+Dt+2aDx)_{(0,0)}
   v3 = (7) at site j+1        (Dx2+Dt+2aDx)_{(1,1)}
   v2, v4 = two cross-site vectors with an undifferentiated (id) term

If v2, v4 are genuine for every N the "obstruction" to a discrete (6) is much
weaker than claimed; if they die at some larger N they were N<=5 artifacts.

A hand check shows they MUST die somewhere: their id coefficients are O(1) in h,
so their h->0 limit would be a *continuum* identity d_x f.g = 0, which is false.
This script locates the failure.

Run:  python -u test_v2.py
"""
import sympy as sp

from engine2 import Model, eadd, escale, emul, rand_point

a, h = sp.symbols('a h', real=True)
OFFSETS = [(0, 0), (1, 0), (0, 1), (1, 1), (-1, 0), (0, -1)]
OPS = ['Dx2', 'Dt', 'Dx', 'id']
LAB = ['%s_(%d,%d)' % (op, p, q) for (p, q) in OFFSETS for op in OPS]

# coefficients taken from the N<=5 intersection at a = 5/2, h = 1/3
V = {
    'v1  (7) at site j': {'Dx2_(0,0)': sp.Rational(1, 5), 'Dt_(0,0)': sp.Rational(1, 5),
                          'Dx_(0,0)': sp.Integer(1)},
    'v2  cross-site A': {'Dx2_(1,0)': sp.Integer(-9), 'Dt_(1,0)': sp.Integer(-9),
                        'Dx_(1,0)': sp.Integer(-39), 'id_(1,0)': sp.Integer(-1),
                        'Dx2_(0,1)': sp.Integer(9), 'Dt_(0,1)': sp.Integer(9),
                        'Dx_(0,1)': sp.Integer(51), 'id_(0,1)': sp.Integer(1)},
    'v4  cross-site B': {'Dx2_(-1,0)': sp.Integer(-9), 'Dt_(-1,0)': sp.Integer(-9),
                        'Dx_(-1,0)': sp.Integer(-51), 'id_(-1,0)': sp.Integer(-1),
                        'Dx2_(0,-1)': sp.Integer(9), 'Dt_(0,-1)': sp.Integer(9),
                        'Dx_(0,-1)': sp.Integer(39), 'id_(0,-1)': sp.Integer(1)},
}


def residual(vec, N, seed):
    m = Model(N, a=sp.Rational(5, 2), h=sp.Rational(1, 3))
    pt = rand_point(m, seed=seed)
    pt[m.a] = sp.Rational(5, 2)          # keep a, h fixed at the values the
    pt[m.h] = sp.Rational(1, 3)          # canonical basis was computed for
    m._subs = {}
    m.subs_point(pt)
    cache = {}

    def F(j):
        if ('F', j) not in cache:
            cache[('F', j)] = m.tau(1, j=j, s=m.a, mu=m.a)
        return cache[('F', j)]

    def G(j):
        if ('G', j) not in cache:
            cache[('G', j)] = m.tau(0, j=j)
        return cache[('G', j)]

    res = {}
    for lab, coef in vec.items():
        op, off = lab.split('_')
        p, q = [int(z) for z in off.strip('()').split(',')]
        f, g = F(p), G(q)
        d = {'Dx2': m.bilin(f, g, ax=2), 'Dt': m.bilin(f, g, at=1),
             'Dx': m.bilin(f, g, ax=1), 'id': emul(f, g)}[op]
        res = eadd(res, escale(d, coef))
    return res


print('=' * 90)
print('testing the uniform-class vectors at a = 5/2, h = 1/3, random spectral data')
print('=' * 90)
for name, vec in V.items():
    line = '%-20s :' % name
    firstfail = None
    for N in range(1, 9):
        ok = all(len(residual(vec, N, 1000 + 37 * N + 5 * s)) == 0 for s in range(2))
        line += '  N=%d:%s' % (N, 'ok' if ok else 'FAIL')
        if not ok and firstfail is None:
            firstfail = N
            bad = residual(vec, N, 1000 + 37 * N)
            print(line, flush=True)
            print('        first failure at N=%d ; residual has %d nonzero monomials, e.g. %s'
                  % (N, len(bad), list(bad.items())[:2]))
            break
    if firstfail is None:
        print(line, flush=True)
print()
print('If v2/v4 are "ok" for every tested N then they are genuine all-N identities and')
print('the no-go statement must be weakened; if they FAIL at some N they are artifacts')
print('of truncating the intersection at N <= 5.')
