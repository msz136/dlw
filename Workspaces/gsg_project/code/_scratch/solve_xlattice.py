"""
x-lattice (GSG device in x): discover the exact two-site bilinear identities.

tau: rows get (1-h p)^{-j}, cols get (1-h q)^{-j};  y, t continuous.
Ansatz (KP-BT form): operators {Id, Dy, Dt} x pairings {(f1.g),(f.g1)} + site Id.
"""
import sympy as sp
from engine import DLW, random_point, point_is_regular

H = sp.Symbol('h', positive=True)
A0, H0 = sp.Rational(7, 3), sp.Rational(2, 5)


def basis_pairings(m):
    f0, g0 = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    out = {}
    for nm, F, G in [('f1.g', f1, g0), ('f.g1', f0, g1)]:
        out['Id ' + nm] = m.bilin(F, G)
        out['Dy ' + nm] = m.bilin(F, G, ay=1)
        out['Dt ' + nm] = m.bilin(F, G, at=1)
    out['Id f.g'] = m.bilin(f0, g0)
    out['Id f1.g1'] = m.bilin(f1, g1)
    return out


names = None
all_rows = []
for trial in range(20):
    m = DLW(2, kind='expx', h=H)
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
