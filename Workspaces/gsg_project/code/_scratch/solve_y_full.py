"""
y-lattice: comprehensive identity search.
pairings: {f1.g, f.g1, f.g, f1.g1, f1.f, g1.g}
operators: {Id, Dx, Dx2, Dx3, Dt, DxDt, Dt2}
"""
import sympy as sp
from engine import DLW, random_point, point_is_regular

H = sp.Symbol('h', positive=True)
A0, H0 = sp.Rational(7, 3), sp.Rational(2, 5)

OPS = [('Id', {}), ('Dx', dict(ax=1)), ('Dx2', dict(ax=2)), ('Dx3', dict(ax=3)),
       ('Dt', dict(at=1)), ('DxDt', dict(ax=1, at=1)), ('Dt2', dict(at=2))]


def basis_pairings(m):
    f0, g0 = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    out = {}
    for nm, F, G in [('f1.g', f1, g0), ('f.g1', f0, g1), ('f.g', f0, g0),
                     ('f1.g1', f1, g1), ('f1.f', f1, f0), ('g1.g', g1, g0)]:
        for opn, kw in OPS:
            out[f'{opn} {nm}'] = m.bilin(F, G, **kw)
    return out


names = None
all_rows = []
for trial in range(10):
    m = DLW(2, kind='exp', h=H)
    pt = random_point(m, seed=31 + 131 * trial)
    pt[sp.Symbol('a', real=True)] = A0
    pt[H] = H0
    m.set_point(pt)
    if not point_is_regular(m):
        continue
    basis = basis_pairings(m)
    names = list(basis.keys())
    keymap = {}
    for nm, d in basis.items():
        for k, v in d.items():
            keymap.setdefault(k, {})[nm] = v
    for k, entries in keymap.items():
        all_rows.append([entries.get(nm, sp.Integer(0)) for nm in names])

M = sp.Matrix(all_rows)
print("eqns:", M.rows, "unknowns:", M.cols)
ns = M.nullspace()
print("nullity:", len(ns))
for v in ns:
    v = sp.Matrix(v)
    den = sp.lcm([sp.fraction(x)[1] for x in v])
    v = sp.expand(den * v)
    g_ = sp.gcd_list([sp.fraction(x)[0] for x in v if x != 0] + [sp.Integer(1)])
    v = v / g_
    terms = [(nm, cf) for nm, cf in zip(names, v) if cf != 0]
    print("\nidentity:")
    for nm, cf in terms:
        print(f"   ({sp.factor(cf)}) * {nm}")
