import sympy as sp
import test_v2 as T

print('V keys:', list(T.V.keys()))
for seed in (1037, 1042, 1000 + 37 * 2):
    r = T.residual(T.V['v1  (7) at site j'], 1, seed)
    print('v1 N=1 seed=%d -> %s' % (seed, r))

# direct comparison
from engine2 import Model, rand_point
m = Model(1, a=sp.Rational(5, 2), h=sp.Rational(1, 3))
pt = rand_point(m, seed=1037)
print('pt:', {str(k): str(v) for k, v in pt.items()})
pt[m.a] = sp.Rational(5, 2)
pt[m.h] = sp.Rational(1, 3)
m.subs_point(pt)
print('a,h =', m.a, m.h, ' p,q =', m.p, m.q)
