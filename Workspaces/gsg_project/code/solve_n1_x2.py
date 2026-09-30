"""
N=1 fully symbolic, x2-lattice (rows (1-hp)^{-j}, cols (1+hq)^j).
1) verify rank-one:  m(j+1)-m(j) should factor as (i-part)x(j-part)
2) symbolic nullspace over two-site pairings x {Id, Dy, Dt}
"""
import sympy as sp
from engine import DLW

p, q, a, h, c = sp.symbols('p q a h c', positive=True)

m = DLW(1, kind='expx2', h=h)
m.set_point({m.p[0]: p, m.q[0]: q, m.a: a})
m.c = [c]

# --- rank-one check on the single entry
P, Q = p - a, q + a
R, C = 1 / (1 - h * p), (1 + h * q)
base = (-P / Q) ** sp.Symbol('n') / (p + q)   # symbolic n not needed; use n=0,1
for n in (0, 1):
    moff = (-P / Q) ** n / (p + q)
    diff = sp.factor(moff * (R * C - 1))
    print(f"n={n}:  m(j+1)-m(j) = {diff}")

f0, g0 = m.tau(1), m.tau(0)
f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)

basis = {}
for nm, F, G in [('f1.g', f1, g0), ('f.g1', f0, g1),
                 ('f1.f', f1, f0), ('g1.g', g1, g0),
                 ('f.g', f0, g0), ('f1.g1', f1, g1)]:
    basis['Id ' + nm] = m.bilin(F, G)
    basis['Dy ' + nm] = m.bilin(F, G, ay=1)
    basis['Dt ' + nm] = m.bilin(F, G, at=1)

names = list(basis.keys())
keys = sorted({k for d in basis.values() for k in d}, key=str)
print("\nkeys:", keys)
rows = [[sp.expand(basis[nm].get(k, 0)) for nm in names] for k in keys]
M = sp.Matrix(rows)
ns = M.nullspace()
print("nullity:", len(ns))
for v in ns:
    v = sp.Matrix(v)
    den = sp.lcm([sp.fraction(x)[1] for x in v])
    v = sp.expand(den * v)
    g_ = sp.gcd_list([sp.fraction(x)[0] for x in v if x != 0] + [sp.Integer(1)])
    v = v / g_
    terms = [(nm, sp.factor(cf)) for nm, cf in zip(names, v) if cf != 0]
    print("\nidentity:")
    for nm, cf in terms:
        print(f"   ({cf}) * {nm}")
