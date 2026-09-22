"""Exact rational checks; no symbolic or numerical third-party packages.

Tests the centered edge candidate, NOT a proven integrable lattice.
The two-exponential ansatz uses the continuous DLW interaction coefficient.
"""
from fractions import Fraction as F
from itertools import product
from math import prod


def residuals(p, q, a, h):
    n = len(p)
    modes = list(product((0, 1), repeat=n))
    ell = [1 / (p[i] - a) + 1 / (q[i] + a) for i in range(n)]
    R = [(2 + h * e) / (2 - h * e) for e in ell]
    g = {}
    f = {}
    for m in modes:
        active = [i for i in range(n) if m[i]]
        c = prod((1 / (p[i] + q[i]) for i in active), start=F(1))
        for i in active:
            for j in active:
                if i < j:
                    c *= (p[i] - p[j]) * (q[i] - q[j]) / ((p[i] + q[j]) * (p[j] + q[i]))
        g[m] = c
        f[m] = c * prod((-(p[i] - a) / (q[i] + a) for i in active), start=F(1))
    base, edge = {}, {}
    for m, nmode in product(modes, repeat=2):
        k = sum((m[i] - nmode[i]) * (p[i] + q[i]) for i in range(n))
        w = sum((m[i] - nmode[i]) * (q[i]**2 - p[i]**2) for i in range(n))
        rm = prod((R[i]**m[i] for i in range(n)), start=F(1))
        rn = prod((R[i]**nmode[i] for i in range(n)), start=F(1))
        key = tuple(m[i] + nmode[i] for i in range(n))
        b = k*k + w + 2*a*k
        weight = f[m] * g[nmode]
        base[key] = base.get(key, F(0)) + weight*b
        edge[key] = edge.get(key, F(0)) + weight*(b*(rm-rn)/h - 2*k*(rm+rn))
    return R, base, edge


if __name__ == '__main__':
    for count in (1, 2):
        R, base, edge = residuals([F(1), F(0)][:count], [F(2), F(3)][:count], F(2), F(1, 10))
        assert all(v == 0 for v in base.values())
        bad = {k: str(v) for k, v in edge.items() if v}
        print(f'{count} exponential(s): R={[str(r) for r in R]}, edge nonzero coefficients={bad}')
        if count == 1:
            assert not bad
        else:
            assert bad, 'Expected failure of the unchanged continuous two-soliton interaction.'
    print('Two-exponential residual coefficient under refinement (ansatz residual, not solution error):')
    for h in (F(1, 10), F(1, 20), F(1, 40)):
        _, _, edge = residuals([F(1), F(0)], [F(2), F(3)], F(2), h)
        value = edge[(1, 1)]
        print(f'h={h}, coefficient={value}, coefficient/h^2={float(value/h**2):.9g}')
