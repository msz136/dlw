"""
Universal two-site identity at N=1, x2-lattice, symbolic (a,h).
Stack the 3-monomial system over many (p,q) points; nullspace over Q(a,h)
= identities whose coefficients depend only on (a,h).
"""
import sympy as sp
from engine import DLW

p, q, a, h, c = sp.symbols('p q a h c', positive=True)

PAIRINGS = [('f1.g', 1, 0, 'f', 'g'), ('f.g1', 0, 1, 'f', 'g'),
            ('f1.f', 1, 0, 'f', 'f'), ('g1.g', 1, 0, 'g', 'g'),
            ('f.g', 0, 0, 'f', 'g'), ('f1.g1', 1, 1, 'f', 'g')]
OPS = [('Id', {}), ('Dy', dict(ay=1)), ('Dt', dict(at=1))]


def build(m):
    f = {s: m.tau(1, jshift=s) for s in (0, 1)}
    g = {s: m.tau(0, jshift=s) for s in (0, 1)}
    T = {'f': f, 'g': g}
    out = {}
    for nm, s1, s2, A, B in PAIRINGS:
        for opn, kw in OPS:
            out[f'{opn} {nm}'] = m.bilin(T[A][s1], T[B][s2], **kw)
    return out


names = None
rows = []
points = [(sp.Rational(r), sp.Rational(s)) for r, s in
          [(3, 2), (5, 4), (7, 3), (11, 5), (13, 6), (4, 7), (9, 2), (6, 11)]]
for pv, qv in points:
    m = DLW(1, kind='expx2', h=h)
    m.set_point({m.p[0]: pv, m.q[0]: qv, m.a: a})
    m.c = [c]
    basis = build(m)
    names = list(basis.keys())
    keymap = {}
    for nm, d in basis.items():
        for k, v in d.items():
            keymap.setdefault(k, {})[nm] = v
    for k, entries in keymap.items():
        rows.append([sp.expand(entries.get(nm, 0)) for nm in names])

M = sp.Matrix(rows)
print("eqns:", M.rows, "unknowns:", M.cols, " (over Q(a,h,c))")
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
