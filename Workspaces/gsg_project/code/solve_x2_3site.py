"""
x2-lattice: 3-site stencil ansatz.
From e^{eps Dx} f.g = f(x+eps)g(x-eps), the lattice version uses
F(h)=f1.g-1, F(0)=f.g, F(-h)=f-1.g1.
Operators {Id, Dy, Dt, DyDt} x stencil {(1,-1),(0,0),(-1,1),(1,0),(0,1)}.
"""
import sympy as sp
from engine import DLW, random_point, point_is_regular

H = sp.Symbol('h', positive=True)
A0, H0 = sp.Rational(7, 3), sp.Rational(2, 5)

OPS = [('Id', {}), ('Dy', dict(ay=1)), ('Dt', dict(at=1)), ('DyDt', dict(ay=1, at=1))]


def basis_pairings(m):
    f = {s: m.tau(1, jshift=s) for s in (-1, 0, 1)}
    g = {s: m.tau(0, jshift=s) for s in (-1, 0, 1)}
    out = {}
    for nm, F, G in [('f1.g-1', f[1], g[-1]), ('f.g', f[0], g[0]), ('f-1.g1', f[-1], g[1]),
                     ('f1.g', f[1], g[0]), ('f.g1', f[0], g[1])]:
        for opn, kw in OPS:
            out[f'{opn} {nm}'] = m.bilin(F, G, **kw)
    return out


names = None
all_rows = []
for trial in range(12):
    m = DLW(2, kind='expx2', h=H)
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
