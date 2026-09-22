"""
Fully symbolic two-site identity hunt at N=1.

tau dicts at N=1 have keys in {(0,0),(1,1),(2,2)} -> tiny symbolic matrix.
"""
import sympy as sp
from engine import DLW, e_add, e_scale

p, q, a, h, c = sp.symbols('p q a h c', positive=True)

m = DLW(1, kind='exp', h=h)
m.set_point({m.p[0]: p, m.q[0]: q, m.a: a})
m.c = [c]

f0, g0 = m.tau(1), m.tau(0)
f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)

basis = {
    'B f1.g': m.B(f1, g0), 'B f.g1': m.B(f0, g1),
    'Dx2 f1.g': m.bilin(f1, g0, ax=2), 'Dx2 f.g1': m.bilin(f0, g1, ax=2),
    'Dt f1.g': m.bilin(f1, g0, at=1), 'Dt f.g1': m.bilin(f0, g1, at=1),
    'Dx f1.g': m.bilin(f1, g0, ax=1), 'Dx f.g1': m.bilin(f0, g1, ax=1),
    'f1.g': m.bilin(f1, g0), 'f.g1': m.bilin(f0, g1),
    # also site-wise (7) at both sites, for reference
    'B f.g': m.B(f0, g0), 'B f1.g1': m.B(f1, g1),
}
names = list(basis.keys())
keys = sorted({k for d in basis.values() for k in d}, key=str)
print("keys:", keys)
rows = []
for k in keys:
    rows.append([sp.expand(basis[nm].get(k, 0)) for nm in names])
M = sp.Matrix(rows)
ns = M.nullspace()
print("nullity:", len(ns), "\n")
for v in ns:
    v = sp.Matrix(v)
    den = sp.lcm([sp.fraction(x)[1] for x in v])
    v = sp.expand(den * v)
    g_ = sp.gcd_list([sp.fraction(x)[0] for x in v if x != 0] + [sp.Integer(1)])
    v = v / g_
    terms = [(nm, sp.factor(cf)) for nm, cf in zip(names, v) if cf != 0]
    print("identity:")
    for nm, cf in terms:
        print(f"   ({cf}) * {nm}")
    print()
