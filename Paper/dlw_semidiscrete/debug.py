"""debug.py -- pin down (i) the E identity and (ii) the fate of the symmetric
two-site identity beyond N=1."""
import sympy as sp
from engine2 import Model, eadd, escale, rand_point

H = sp.Rational(1, 3)

print('--- E identity, element-wise, with h properly substituted ---')
for N in (1, 2, 3, 4):
    mm = Model(N, h=H)
    mm.subs_point(rand_point(mm, seed=21 + N))
    d = mm.h / 2
    lhs = mm.tau(1, j=1, s=mm.a + d, mu=mm.a)
    rhs = mm.tau(1, j=0, s=mm.a - d, mu=mm.a)
    keys_ok = lhs.keys() == rhs.keys()
    diffs = [sp.simplify(lhs[k] - rhs[k]) for k in lhs] if keys_ok else []
    print('   N=%d keys_equal=%s  all_zero=%s' % (N, keys_ok, all(v == 0 for v in diffs)))

print()
print('--- symmetric two-site identity  B_a f_{j+1}.g_j + B_a f_j.g_{j+1} = 0 ---')
for N in (1, 2, 3, 4):
    for seed in (3, 17):
        mm = Model(N, h=H)
        mm.subs_point(rand_point(mm, seed=seed))
        r = eadd(mm.B(mm.tau(1, j=1), mm.tau(0)),
                 mm.B(mm.tau(1), mm.tau(0, j=1)))
        print('   N=%d seed=%2d  #monomials=%d  %s'
              % (N, seed, len(r), 'ZERO' if len(r) == 0 else 'nonzero'))
        if len(r) and N <= 2:
            for k, v in list(r.items())[:3]:
                print('        key=%s  coef=%s' % (k, sp.nsimplify(v)))

print()
print('--- continuum version  B_a f_{j+1}.g_j + B_a f_j.g_{j+1} - 2 B_a f.g = 0 ? ---')
for N in (1, 2, 3, 4):
    mm = Model(N)
    mm.subs_point(rand_point(mm, seed=5 + N))
    r = eadd(mm.B(mm.tau(1, j=1), mm.tau(0)),
             mm.B(mm.tau(1), mm.tau(0, j=1)),
             escale(mm.B(mm.tau(1), mm.tau(0)), -2))
    print('   N=%d  %s' % (N, 'ZERO' if len(r) == 0 else 'nonzero'))

print()
print('--- how big is the lattice defect of the symmetric combination? ---')
for N in (2, 3):
    mm = Model(N, h=sp.Symbol('h'))
    mm.subs_point(rand_point(mm, seed=9 + N))
    r = eadd(mm.B(mm.tau(1, j=1), mm.tau(0)),
             mm.B(mm.tau(1), mm.tau(0, j=1)))
    print('   N=%d  leading h-order of each monomial coefficient:' % N)
    for k, v in list(r.items())[:4]:
        s = sp.series(v, mm.h, 0, 3).removeO()
        print('        %s -> %s' % (k, sp.expand(s)))
