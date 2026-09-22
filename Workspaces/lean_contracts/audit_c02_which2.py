"""
Step 0g: which generators are REALLY needed?

Careful re-run of the subset search, printing the generators explicitly so that a
construction bug cannot masquerade as a mathematical fact.

Run:  python -u audit_c02_which2.py
"""

import itertools
import sympy as sp


def build(M, amod, p):
    A, B = {}, {}
    for i, j, k in itertools.product(range(M + 1), repeat=3):
        if i + j + k <= M:
            A[(i, j, k)] = sp.Symbol('A%d%d%d' % (i, j, k))
            B[(i, j, k)] = sp.Symbol('B%d%d%d' % (i, j, k))
    a = sp.Integer(amod)

    def der(expr, var):
        sub = {}
        for idx, s in A.items():
            t = list(idx); t[var] += 1; t = tuple(t)
            if t in A:
                sub[s] = A[t]
        for idx, s in B.items():
            t = list(idx); t[var] += 1; t = tuple(t)
            if t in B:
                sub[s] = B[t]
        return sp.expand(expr.subs(sub))

    R0 = A[(2, 0, 0)] + B[(1, 0, 0)] ** 2 + B[(0, 0, 1)] + 2 * a * B[(1, 0, 0)]
    T1 = A[(0, 1, 0)] - B[(0, 1, 0)]
    Sxx2 = A[(2, 0, 0)] + B[(2, 0, 0)] + A[(2, 1, 0)] - B[(2, 1, 0)]
    Dx2 = A[(1, 0, 0)] + B[(1, 0, 0)] - A[(1, 1, 0)] + B[(1, 1, 0)]
    Dt2 = A[(0, 0, 1)] + B[(0, 0, 1)] - A[(0, 1, 1)] + B[(0, 1, 1)]
    W2c = 2 * Sxx2 + Dx2 ** 2 + 2 * Dt2 + 4 * a * Dx2
    E20 = T1 * W2c + 16 * B[(1, 0, 0)]
    c1 = (2 * B[(1, 1, 1)] + 2 * A[(3, 1, 0)] + 4 * B[(2, 0, 0)] * B[(1, 1, 0)]
          + 4 * B[(1, 0, 0)] * B[(2, 1, 0)] + 4 * a * B[(2, 1, 0)])
    c2 = (2 * A[(1, 1, 1)] + 4 * B[(2, 0, 0)] * A[(1, 1, 0)]
          + 4 * B[(1, 0, 0)] * A[(2, 1, 0)] + 2 * B[(3, 1, 0)]
          + 4 * a * A[(2, 1, 0)] - 8 * B[(2, 0, 0)])
    return der, R0, E20, c1, c2


def d(der, e, idx):
    for _ in range(idx[0]):
        e = der(e, 0)
    for _ in range(idx[1]):
        e = der(e, 1)
    for _ in range(idx[2]):
        e = der(e, 2)
    return e


def main():
    der, R0, E20, c1, c2 = build(5, 7, 32003)
    gens = {}
    for idx in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0)]:
        gens[('R',) + idx] = d(der, R0, idx)
    for idx in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        gens[('E',) + idx] = d(der, E20, idx)

    for nm, f in (('c1', c1), ('c2', c2)):
        print('==== %s ====' % nm)
        for k, g in gens.items():
            print('   %-14s %s' % (str(k), sp.expand(g)))
        break
    print()

    def in_ideal(gs, f):
        # NB: the variable list must be given in a *consistent, lexicographic*
        # order; `sorted(..., key=str)` is NOT lexicographic ("A200" < "A20"),
        # which corrupts the Groebner computation and yields false positives.
        vs = set(f.free_symbols)
        for g in gs:
            vs |= g.free_symbols
        vs = sorted(vs, key=lambda s: s.name)
        assert len(set(s.name for s in vs)) == len(vs)
        G = sp.groebner(gs, *vs, modulus=32003, order='grevlex')
        out = G.reduce(f)
        r = out[0] if isinstance(out, tuple) else out
        r = sp.expand(r[0] if isinstance(r, list) else r)
        return r == 0

    keys = list(gens)
    for nm, f in (('c1', c1), ('c2', c2)):
        print('==== %s ====' % nm)
        done = False
        for size in (1, 2, 3):
            hits = []
            for combo in itertools.combinations(keys, size):
                if in_ideal([gens[k] for k in combo], f):
                    hits.append(combo)
            print('  size %d: %d hits' % (size, len(hits)))
            for h in hits[:10]:
                print('     ', h)
            if hits:
                done = True
                break
        if not done:
            print('  none up to size 3')


if __name__ == '__main__':
    main()
