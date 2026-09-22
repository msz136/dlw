"""
Universal two-site identity at N=2:
stack monomial equations from many (p,q) points with FIXED (a,h).
The common nullspace = relations whose coefficients depend only on (a,h).
"""
import sympy as sp
from engine import DLW, random_point, point_is_regular

H = sp.Symbol('h', positive=True)
A0, H0 = sp.Rational(7, 3), sp.Rational(2, 5)


def basis_pairings(m):
    f0, g0 = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    return {
        'B f1.g': m.B(f1, g0), 'B f.g1': m.B(f0, g1),
        'Dx2 f1.g': m.bilin(f1, g0, ax=2), 'Dx2 f.g1': m.bilin(f0, g1, ax=2),
        'Dt f1.g': m.bilin(f1, g0, at=1), 'Dt f.g1': m.bilin(f0, g1, at=1),
        'Dx f1.g': m.bilin(f1, g0, ax=1), 'Dx f.g1': m.bilin(f0, g1, ax=1),
        'f1.g': m.bilin(f1, g0), 'f.g1': m.bilin(f0, g1),
        'B f.g': m.B(f0, g0), 'B f1.g1': m.B(f1, g1),
    }


names = None
all_rows = []
for trial in range(12):
    m = DLW(2, kind='exp', h=H)
    pt = random_point(m, seed=11 + 97 * trial)
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
