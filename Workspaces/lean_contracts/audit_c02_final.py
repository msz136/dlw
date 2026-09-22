"""
Step 0f: DECISIVE.  c1 and c2 each lie in the ideal <R, E2> alone (Clairaut imposed).

So there are smooth multipliers P1, Q1, P2, Q2 with

    c1 = P1 * R + Q1 * E2
    c2 = P2 * R + Q2 * E2

in the jet ring mod Clairaut.  Find them.

Because the ideal has only two generators, the quotient by <R, E2> is a
polynomial ring in the remaining free coordinates, and the cofactors can be read
off directly by linear algebra:  expand c_i in powers of the "leading" jets that
R and E2 involve.

We solve the linear system for multipliers of increasing degree in the free jets.

Run:  python -u audit_c02_final.py
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
    free = {}
    for j, k in itertools.product(range(M + 1), repeat=2):
        if j + k <= M:
            free[('A', j, k)] = sp.Symbol('PA_%d_%d' % (j, k))
            free[('B', j, k)] = sp.Symbol('PB_%d_%d' % (j, k))

    def subst(expr):
        sub = {}
        for s in expr.free_symbols:
            nm = str(s)
            if len(nm) == 4 and nm[0] in 'AB' and nm[1:].isdigit():
                i, j, k = int(nm[1]), int(nm[2]), int(nm[3])
                sub[s] = free[(nm[0], j + i, k)]
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


def main():
    free, Rf, Ef, c1f, c2f = build(5, 7, 32003)
    # Leading jets: R involves PA_20; E2 involves PA_21, PB_21, PA_20 ...
    # So quotient coordinates = all free jets except PA_20, PA_21, PB_21.
    lead = {('A', 2, 0), ('A', 2, 1), ('B', 2, 1)}
    others = sorted([v for k, v in free.items() if k not in lead], key=str)
    freesyms = sorted(free.values(), key=str)
    print('free jets %d, quotient coords %d' % (len(freesyms), len(others)))

    for deg in (0, 1, 2, 3):
        basis = [sp.Integer(1)] + others
        if deg >= 2:
            basis = basis + [s1 * s2 for i, s1 in enumerate(others) for s2 in others[i:]]
        if deg >= 3:
            basis = basis + [s1 * s2 * s3 for i, s1 in enumerate(others)
                             for j, s2 in enumerate(others[i:]) for s3 in others[j:]]
        print('--- multiplier basis of degree <= %d : %d elements ---' % (deg, len(basis)))
        KR = sp.symbols('kr0:%d' % len(basis))
        KE = sp.symbols('ke0:%d' % len(basis))
        unknowns = list(KR) + list(KE)
        for nm, f in (('c1', c1f), ('c2', c2f)):
            MR = sum(c * b for c, b in zip(KR, basis))
            ME = sum(c * b for c, b in zip(KE, basis))
            expr = sp.expand(f - MR * Rf - ME * Ef)
            poly = sp.Poly(expr, *freesyms)
            eqs = poly.coeffs()
            if len(eqs) > 40000:
                print('  %s: too large (%d eqs), skipping' % (nm, len(eqs)))
                continue
            sol = sp.solve(eqs, unknowns, dict=True)
            print('  %s: %d eqs / %d unknowns -> %d solutions' % (nm, len(eqs), len(unknowns), len(sol)))
            if sol:
                s = dict(sol[0])
                MRs = sp.expand(MR.subs(s))
                MEs = sp.expand(ME.subs(s))
                print('    residual:', sp.expand(f - MRs * Rf - MEs * Ef))
                print('    P_%s = %s' % (nm, MRs))
                print('    Q_%s = %s' % (nm, MEs))


if __name__ == '__main__':
    main()
