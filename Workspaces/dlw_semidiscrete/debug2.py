import sympy as sp
from engine2 import Model, eadd, escale, emul, rand_point
import nosearch as NS

a, h = sp.symbols('a h', real=True)
LAB = NS.labels()
print('labels:', LAB)

# candidate: (7) itself
v = [sp.Integer(0)] * len(LAB)
v[LAB.index('Dx2_(0,0)')] = sp.Integer(1)
v[LAB.index('Dt_(0,0)')] = sp.Integer(1)
v[LAB.index('Dx_(0,0)')] = 2 * a
print('candidate (7), nonzero entries:',
      [(LAB[i], v[i]) for i in range(len(v)) if v[i] != 0])

for N in (1, 2, 3):
    ok, att = NS.is_zero_at(v, N, False)
    print('  is_zero_at N=%d -> %s (att=%d)' % (N, ok, att))

print()
print('is (7) inside the N=1 nullspace?')
M, ns = NS.nullspace_N1(([sp.Rational(3, 2)], [sp.Rational(7, 4)]), False)
print('   nullspace dim', len(ns), ' rank', M.rank(), ' cols', M.cols)
print('   M * v =', [sp.simplify(x) for x in (M * sp.Matrix(v)).tolist()][:8], '...')
print('   M*v all zero:', all(sp.simplify(x) == 0 for x in (M * sp.Matrix(v)).tolist()))

print()
print('a generic nullspace member:')
for i, w in enumerate(ns[:3]):
    print('   v%d nonzero: %s' % (i + 1, [(LAB[j], sp.nsimplify(w[j])) for j in range(len(w)) if w[j] != 0]))
    for N in (1, 2, 3):
        ok, att = NS.is_zero_at(w, N, False)
        print('        N=%d -> %s (att=%d)' % (N, ok, att))
