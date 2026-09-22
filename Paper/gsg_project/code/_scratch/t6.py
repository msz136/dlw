import sympy as sp
import engine as E
from engine import DLW, random_point, e_is_zero, e_add, e_scale

m = DLW(1, kind="none")
pt = random_point(m, seed=1)
print("pt:", pt)
m.point = pt
f, g = m.tau(1), m.tau(0)
print("g:", g)
print("f:", f)
r = m.B(f,g)
print("B f.g (numeric):", r)
print("Dx f.g:", m.Dx(f,g))
print("DyB:", m.DyB(f,g))
# compare with hand formula at this point
p,q,a = m.p, m.q, m.a
P,Q = p[0]-a, q[0]+a
E11 = sp.exp(0)  # dummy
import mpmath
