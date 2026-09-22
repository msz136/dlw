"""
Step 0i: RIGOROUS membership by exact linear algebra (no sympy Groebner).

Everything happens in the truncated polynomial ring
    Q = F_p[PA_jk, PB_jk : j+k <= M]        (F_p = GF(32003))
which is the Clairaut quotient of the jet ring: PA_jk stands for the class of
d^(j+k) A / dx^j dt^k, so all mixed-partial symmetries are built in.

Given polynomials f and generators g_1..g_s, "f in <g_1..g_s>" means there exist
polynomials h_1..h_s with f = sum h_i g_i.  We decide this by linear algebra:
truncate the h_i at a degree D and solve the (huge but exact) linear system

    sum_i h_i g_i  ==  f        coefficient-wise.

This is a *sufficient* test: a solution certifies membership (and hands us the
explicit multipliers).  There is no Groebner basis involved, so there is nothing
to go wrong in the variable ordering.

Run:  python -u audit_c02_linalg.py <M> <a> <deg>
"""

import itertools
import sys
import sympy as sp


def setup(M, amod):
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
                if len(parts) == 3 and all(t.lstrip('-').isdigit() for t in parts):
                    i, j, k = (int(t) for t in parts)
                    tgt = free.get((nm[0], j + i, k))
                    if tgt is not None:
                        sub[s] = tgt
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
    return free, subst(R0), subst(E20), subst(c1), subst(c2)


def monomials(vs, deg):
    """all monomials of total degree <= deg in vs"""
    out = [sp.Integer(1)]
    cur = [sp.Integer(1)]
    for _ in range(deg):
        nxt = []
        for m in cur:
            for v in vs:
                mm = m * v
                nxt.append(mm)
        out.extend(nxt)
        cur = nxt
    return sorted(set(out), key=lambda m: sp.Poly(m, *vs).monoms()[0] if vs else ())


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    amod = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    deg = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    p = 32003
    free, Rf, Ef, c1f, c2f = setup(M, amod)
    vs = sorted(free.values(), key=lambda s: s.name)
    print('M=%d a=%d deg=%d vars=%d' % (M, amod, deg, len(vs)))
    print('R  =', Rf)
    print('c1 =', c1f)
    print('c2 =', c2f)

    # monomial basis for the multipliers
    mult_mons = []
    cur = [sp.Integer(1)]
    mult_mons.extend(cur)
    for _ in range(deg):
        nxt = []
        for m in cur:
            for v in vs:
                nxt.append(m * v)
        mult_mons.extend(nxt)
        cur = nxt
    mult_mons = mult_mons          # may contain duplicates; fine (over-determined)
    print('multiplier monomials (with dups): %d' % len(mult_mons))

    def solve_membership(f, gens, label):
        # unknowns: coefficient of each (multiplier monomial) * (generator)
        cols = []
        def poly_to_dict(e):
            pd = sp.Poly(e, *vs, modulus=p)
            return {m: c for m, c in zip(pd.monoms(), pd.coeffs())}
        fdict = poly_to_dict(f)
        # build all monomial keys
        colkeys = []
        for gi, g in enumerate(gens):
            gd = poly_to_dict(g)
            for mi, m in enumerate(mult_mons):
                md = sp.Poly(m, *vs, modulus=p).monoms()
                col = {}
                for gm, gc in gd.items():
                    key = tuple(a + b for a, b in zip(gm, md[0]))
                    col[key] = (col.get(key, 0) + gc) % p
                cols.append(col)
                colkeys.append((gi, mi))
        allkeys = sorted(set(fdict) | set().union(*[set(c) for c in cols]) if cols else set(fdict))
        idx = {k: i for i, k in enumerate(allkeys)}
        nrows, ncols = len(allkeys), len(cols)
        print('  [%s] %d rows x %d cols' % (label, nrows, ncols))
        # dense GF(p) matrix
        from sympy.polys.matrices import DomainMatrix
        from sympy.polys.domains import GF
        dom = GF(p)
        rows = []
        for k in allkeys:
            rows.append([dom.convert(c.get(k, 0)) for c in cols])
        A = DomainMatrix(rows, (nrows, ncols), dom)
        b = DomainMatrix([[dom.convert(fdict.get(k, 0))] for k in allkeys], (nrows, 1), dom)
        try:
            Ab = A.hstack(b)
            rref, piv = Ab.rref()
        except Exception as e:
            print('  rref failed:', e)
            return None
        rref = rref.to_Matrix()
        ncols_tot = ncols
        for r in range(rref.rows):
            row = rref.row(r)
            if all(row[c] == 0 for c in range(ncols_tot)) and row[ncols_tot] != 0:
                print('  [%s] INCONSISTENT -> not a member at this degree' % label)
                return None
        print('  [%s] CONSISTENT -> member (explicit multipliers exist)' % label)
        sol = [dom.convert(0)] * ncols
        for r in range(rref.rows):
            row = rref.row(r)
            pc = None
            for c in range(ncols_tot):
                if row[c] != 0:
                    pc = c
                    break
            if pc is None:
                continue
            sol[pc] = row[ncols_tot]
        out = {}
        for (gi, mi), val in zip(colkeys, sol):
            if val != 0:
                out.setdefault(gi, []).append((mult_mons[mi], int(val)))
        return out

    for label, f in (('c1', c1f), ('c2', c2f)):
        res = solve_membership(f, [Rf, Ef], label)
        if res:
            for gi, terms in res.items():
                name = 'P' if gi == 0 else 'Q'
                print('    %s_%s = %s' % (name, label,
                      ' + '.join('%d*%s' % (v, m) for m, v in terms)))
        # sanity: the routine must FAIL on a random non-member
        rr = sp.expand(f + sp.Symbol('zzz_dummy') * Rf) if False else None
    # negative control
    neg = sp.expand(c1f * Ef + 1)
    print('\n-- negative control: c1*E2 + 1 --')
    solve_membership(neg, [Rf, Ef], 'neg')


if __name__ == '__main__':
    main()
