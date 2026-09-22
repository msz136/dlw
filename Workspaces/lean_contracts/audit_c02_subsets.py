"""
Step 0j: which HYPOTHESIS DERIVATIVES are needed, decided by the reliable
exact-linear-algebra membership test (audit_c02_linalg.py), not by sympy Groebner.

Generators available:  R, sx R, sy R, st R, sxx R, syy R, stt R, sxy R
                       E2, sx E2, sy E2, st E2
where R and E2 are the two smooth hypotheses and sx/sy/st are total derivatives.

We test, for each subset, whether c1 (resp c2) admits multipliers of degree <= D.
For small subsets the D needed is small, so this is tractable.

Run:  python -u audit_c02_subsets.py <M> <a> <deg> <size>
"""

import itertools
import sys
import sympy as sp
from sympy.polys.domains import GF


def build(M, amod, p):
    A, B = {}, {}
    for i, j, k in itertools.product(range(M + 1), repeat=3):
        if i + j + k <= M:
            A[(i, j, k)] = sp.Symbol('A%d_%d_%d' % (i, j, k))
            B[(i, j, k)] = sp.Symbol('B%d_%d_%d' % (i, j, k))
    a = sp.Integer(amod)
    free = {}
    for j, k in itertools.product(range(M + 1), repeat=2):
        if j + k <= M:
            free[('A', j, k)] = sp.Symbol('PA_%d_%d' % (j, k))
            free[('B', j, k)] = sp.Symbol('PB_%d_%d' % (j, k))

    def subst(expr):
        sub = {}
        for s in expr.free_symbols:
            nm = s.name
            if len(nm) >= 6 and nm[0] in 'AB':
                parts = nm[1:].split('_')
                if len(parts) == 3 and all(t.isdigit() for t in parts):
                    i, j, k = (int(t) for t in parts)
                    tgt = free.get((nm[0], j + i, k))
                    if tgt is not None:
                        sub[s] = tgt
        return sp.expand(expr.subs(sub))

    def der(e, var, upto):
        """raw jet derivative, returning None when out of range"""
        out = e
        for _ in range(upto):
            sub = {}
            for idx, s in list(A.items()) + list(B.items()):
                t = list(idx); t[var] += 1; t = tuple(t)
                if t in A:
                    sub[s] = A[t]
            out = sp.expand(out.subs(sub))
        return out

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

    gens = {}
    for idx in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0)]:
        e = R0
        for _ in range(idx[0]):
            e = der(e, 0, 1)
        for _ in range(idx[1]):
            e = der(e, 1, 1)
        for _ in range(idx[2]):
            e = der(e, 2, 1)
        gens[('R',) + idx] = subst(e)
    for idx in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        e = E20
        for _ in range(idx[0]):
            e = der(e, 0, 1)
        for _ in range(idx[1]):
            e = der(e, 1, 1)
        for _ in range(idx[2]):
            e = der(e, 2, 1)
        gens[('E',) + idx] = subst(e)
    return free, subst(c1), subst(c2), gens


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    amod = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    deg = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    size = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    p = 32003
    free, c1f, c2f, gens = build(M, amod, p)
    vs = sorted(free.values(), key=lambda s: s.name)
    print('M=%d a=%d deg=%d size=%d vars=%d' % (M, amod, deg, size, len(vs)))

    mult_mons = [sp.Integer(1)]
    cur = [sp.Integer(1)]
    for _ in range(deg):
        nxt = []
        for m in cur:
            for v in vs:
                nxt.append(m * v)
        mult_mons.extend(nxt)
        cur = nxt

    def member(f, gs):
        pd_f = sp.Poly(f, *vs, modulus=p)
        fdict = dict(zip(pd_f.monoms(), pd_f.coeffs()))
        gdicts = []
        for g in gs:
            pg = sp.Poly(g, *vs, modulus=p)
            gdicts.append(dict(zip(pg.monoms(), pg.coeffs())))
        cols = []
        for gd in gdicts:
            for m in mult_mons:
                mm = sp.Poly(m, *vs, modulus=p).monoms()[0]
                col = {}
                for gm, gc in gd.items():
                    key = tuple(x + y for x, y in zip(gm, mm))
                    col[key] = (col.get(key, 0) + int(gc)) % p
                cols.append(col)
        keys = set(fdict)
        for c in cols:
            keys |= set(c)
        keys = sorted(keys)
        dom = GF(p)
        rows = [[dom.convert(c.get(k, 0)) for c in cols] for k in keys]
        rhs = [[dom.convert(fdict.get(k, 0))] for k in keys]
        from sympy.polys.matrices import DomainMatrix
        Amat = DomainMatrix(rows, (len(keys), len(cols)), dom)
        bvec = DomainMatrix(rhs, (len(keys), 1), dom)
        rref, _ = Amat.hstack(bvec).rref()
        rref = rref.to_Matrix()
        for r in range(rref.rows):
            row = rref.row(r)
            if all(row[c] == 0 for c in range(len(cols))) and row[len(cols)] != 0:
                return False
        return True

    keys = list(gens)
    for nm, f in (('c1', c1f), ('c2', c2f)):
        print('==== %s ====' % nm, flush=True)
        hits = []
        n = 0
        for combo in itertools.combinations(keys, size):
            n += 1
            r = member(f, [gens[k] for k in combo])
            print('   [%d] %s -> %s' % (n, combo, r), flush=True)
            if r:
                hits.append(combo)
        print('  tested %d subsets of size %d -> %d hits' % (n, size, len(hits)), flush=True)
        for h in hits[:20]:
            print('     ', h)
        if len(hits) > 20:
            print('      ...')


if __name__ == '__main__':
    main()
