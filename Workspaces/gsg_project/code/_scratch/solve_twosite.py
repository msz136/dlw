"""
Solve for the exact two-site lattice identity.

Ansatz:  sum over basis pairings = 0
basis:   {B, D_x^2, D_t, D_x, 1} x { f_{j+1}.g_j ,  f_j.g_{j+1} }
(B = D_x^2 + D_t + 2a D_x included for completeness; the solver will find
 the linear relation(s) - we expect a 2-dim nullspace spanned by the
 site-wise (7) at the two sites and one genuinely two-site identity.)
"""
import sympy as sp
from engine import DLW, random_point, point_is_regular, e_add, e_scale

H = sp.Symbol('h', positive=True)


def basis_pairings(m):
    f0, g0 = m.tau(1), m.tau(0)
    f1, g1 = m.tau(1, jshift=1), m.tau(0, jshift=1)
    B = lambda F, G: m.B(F, G)
    Dx2 = lambda F, G: m.bilin(F, G, ax=2)
    Dt = lambda F, G: m.bilin(F, G, at=1)
    Dx = lambda F, G: m.bilin(F, G, ax=1)
    Id = lambda F, G: m.bilin(F, G)
    return {
        'B f1.g': B(f1, g0), 'B f.g1': B(f0, g1),
        'Dx2 f1.g': Dx2(f1, g0), 'Dx2 f.g1': Dx2(f0, g1),
        'Dt f1.g': Dt(f1, g0), 'Dt f.g1': Dt(f0, g1),
        'Dx f1.g': Dx(f1, g0), 'Dx f.g1': Dx(f0, g1),
        'f1.g': Id(f1, g0), 'f.g1': Id(f0, g1),
    }


N = 2
names = None
rows = []
for trial in range(40):
    m = DLW(N, kind='exp', h=H)
    pt = random_point(m, seed=11 + 97 * trial)
    m.set_point(pt)
    if not point_is_regular(m):
        continue
    basis = basis_pairings(m)
    names = list(basis.keys())
    # collect all monomial keys
    keys = sorted({k for d in basis.values() for k in d})
    rowmap = {}
    for nm, d in basis.items():
        for k, v in d.items():
            rowmap.setdefault(k, {})[nm] = v
    for k, entries in rowmap.items():
        rows.append([entries.get(nm, sp.Integer(0)) for nm in names])
    if len(rows) >= 14:
        break

M = sp.Matrix(rows)
print("basis:", names)
print("eqns:", M.rows, "unknowns:", M.cols)
ns = M.nullspace()
print("nullity:", len(ns))
for v in ns:
    # normalize to nice leading coefficient
    v = sp.Matrix(v)
    den = sp.lcm([sp.fraction(x)[1] for x in v])
    v = sp.expand(den * v)
    g = sp.gcd_list([sp.fraction(x)[0] for x in v if x != 0] + [sp.Integer(1)])
    v = v / g
    print("\nidentity:  0 =")
    for nm, cf in zip(names, v):
        if cf != 0:
            print(f"   ({sp.factor(cf)}) * {nm}")
