import sympy as sp
from engine2 import Model, eadd, escale, emul, rand_point, is_regular

a5, h3 = sp.Rational(5, 2), sp.Rational(1, 3)
m = Model(1, a=a5, h=h3)
pt = rand_point(m, seed=1001 + 37)
print('random point keys:', {str(k): str(v) for k, v in pt.items()})
pt[a5] = a5
pt[h3] = h3
m.subs_point(pt)
print('after subs: a =', m.a, ' h =', m.h, ' p =', m.p, ' q =', m.q)

F = m.tau(1, j=0, s=m.a, mu=m.a)
G = m.tau(0, j=0)
print('F =', F)
print('G =', G)
B = m.B(F, G)
print('B_a F.G =', B, ' -> empty?', len(B) == 0)

manual = eadd(escale(m.bilin(F, G, ax=2), sp.Rational(1, 5)),
              escale(m.bilin(F, G, at=1), sp.Rational(1, 5)),
              m.bilin(F, G, ax=1))
print('v1 combination =', manual, ' -> empty?', len(manual) == 0)

alt = Model(1, a=a5, h=h3)
alt.p = [sp.Rational(13, 7)]
alt.q = [sp.Rational(9, 4)]
F2, G2 = alt.tau(1, j=0, s=alt.a, mu=alt.a), alt.tau(0, j=0)
print('no-subs path: B =', alt.B(F2, G2), ' -> empty?', len(alt.B(F2, G2)) == 0)
