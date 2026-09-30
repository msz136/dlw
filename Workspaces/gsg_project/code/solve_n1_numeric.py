"""
Universal two-site identity at N=1, x2-lattice.
Fix (a,h) numeric; stack many (p,q) points; common nullspace = universal.
Then repeat over a grid of (a,h) and interpolate coefficients.
"""
import sympy as sp
from engine import DLW

p, q, a, h, c = sp.symbols('p q a h c', positive=True)

PAIRINGS = [('f1.g', 1, 0, 'f', 'g'), ('f.g1', 0, 1, 'f', 'g'),
            ('f1.f', 1, 0, 'f', 'f'), ('g1.g', 1, 0, 'g', 'g'),
            ('f.g', 0, 0, 'f', 'g'), ('f1.g1', 1, 1, 'f', 'g')]
OPS = [('Id', {}), ('Dy', dict(ay=1)), ('Dt', dict(at=1))]

PQ_POINTS = [(sp.Rational(r), sp.Rational(s)) for r, s in
             [(3, 2), (5, 4), (7, 3), (11, 5), (13, 6), (4, 7), (9, 2), (6, 11),
              (8, 3), (12, 5), (5, 9), (14, 3)]]


def nullspace_at(ah, hh):
    rows = []
    names = None
    for pv, qv in PQ_POINTS:
        m = DLW(1, kind='expx2', h=h)
        m.set_point({m.p[0]: pv, m.q[0]: qv, m.a: ah, m.h: hh})
        m.c = [sp.Integer(1)]
        f = {s: m.tau(1, jshift=s) for s in (0, 1)}
        g = {s: m.tau(0, jshift=s) for s in (0, 1)}
        T = {'f': f, 'g': g}
        basis = {}
        for nm, s1, s2, A, B in PAIRINGS:
            for opn, kw in OPS:
                basis[f'{opn} {nm}'] = m.bilin(T[A][s1], T[B][s2], **kw)
        names = list(basis.keys())
        keymap = {}
        for nm, d in basis.items():
            for k, v in d.items():
                keymap.setdefault(k, {})[nm] = v
        for k, entries in keymap.items():
            rows.append([entries.get(nm, sp.Integer(0)) for nm in names])
    M = sp.Matrix(rows)
    ns = M.nullspace()
    out = []
    for v in ns:
        v = sp.Matrix(v)
        den = sp.lcm([sp.fraction(x)[1] for x in v])
        v = sp.expand(den * v)
        g_ = sp.gcd_list([sp.fraction(x)[0] for x in v if x != 0] + [sp.Integer(1)])
        out.append(v / g_)
    return names, out


names, ns = nullspace_at(sp.Rational(7, 3), sp.Rational(2, 5))
print("nullity at (a=7/3,h=2/5):", len(ns))
for v in ns:
    terms = [(nm, cf) for nm, cf in zip(names, v) if cf != 0]
    print("\nidentity:")
    for nm, cf in terms:
        print(f"   ({cf}) * {nm}")
