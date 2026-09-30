import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from cons2 import Tau, x, y, t, A_VAL, H_VAL

T = Tau(2, A_VAL, H_VAL, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)])
d = T.h / 2
G = T.tau(0, 0, s=T.a)
F = T.tau(1, 0, s=T.a - d)
print('a =', T.a, ' h =', T.h, ' d =', d)
print('P =', T.P, ' Q =', T.Q)
print()
print('G =', sp.simplify(G))
print()
print('F =', sp.simplify(F))
print()
print('G_x/G      =', sp.simplify(sp.diff(G, x) / G))
print('F_x/F      =', sp.simplify(sp.diff(F, x) / F))
print('F/G        =', sp.simplify(sp.expand(F / G)))
print('u=2dln(F/G)=', sp.simplify(2 * sp.diff(sp.log(F / G), x)))
print()
print('p+q =', sum(T.p) + sum(T.q))
print('p1+q1 =', T.p[0] + T.q[0])
