"""test_v4_N7.py -- is the N=7 failure of v4 genuine, or a pole artifact?

test_v2.py overrides (a,h) AFTER rand_point has drawn the point, so rand_point's
regularity checks (which used its own random a) no longer protect against
p_i - a = +-h/2 (a pole of lambda) or p_i + q_k = 0.  Here we re-draw until the
point is regular for a = 5/2, h = 1/3.
"""
import sympy as sp

from engine2 import Model, eadd, escale, emul, rand_point
import test_v2 as T

A = sp.Rational(5, 2)
H = sp.Rational(1, 3)
D = H / 2


def regular(p, q):
    if any(pi - A == 0 for pi in p) or any(qk + A == 0 for qk in q):
        return False
    if any(pi + qk == 0 for pi in p for qk in q):
        return False
    if any(pi - A == D or pi - A == -D for pi in p):
        return False
    if any(qk + A == D or qk + A == -D for qk in q):
        return False
    return True


def point(N, seed):
    """draw p,q only; keep a,h fixed and regular."""
    m = Model(N, a=A, h=H)
    pt = rand_point(m, seed=seed)
    pt[A] = A
    pt[H] = H
    p = [pt[sp.Symbol('p%d' % (i + 1))] for i in range(N)]
    q = [pt[sp.Symbol('q%d' % (i + 1))] for i in range(N)]
    return p, q


print('v4 = ' + str(T.V['v4  cross-site B']))
print()
for N in (6, 7, 8):
    tot = fail = bad = 0
    for seed in range(3000, 3040):
        p, q = point(N, seed)
        if not regular(p, q):
            bad += 1
            continue
        r = T.residual(T.V['v4  cross-site B'], N, seed)
        tot += 1
        if len(r) != 0:
            fail += 1
            if fail == 1:
                print('   N=%d  FIRST genuine failure at seed %d' % (N, seed))
                print('        p = %s' % (p,))
                print('        q = %s' % (q,))
                print('        residual: %d monomials, e.g. %s'
                      % (len(r), list(r.items())[:1]))
    print('   N=%d : %d regular points tested, %d failures, %d skipped as non-regular'
          % (N, tot, fail, bad))
print()
print('If failures persist at regular points, v4 is NOT an all-N identity.')
