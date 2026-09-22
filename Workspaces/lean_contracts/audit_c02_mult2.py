"""
Step 0c: extract the explicit identity in the QUOTIENT ring (all Clairaut relations
imposed).  Then the identity

      c_i  =  M_i * R + N_i * E2      (mod Clairaut)

holds in the polynomial ring modulo the Clairaut ideal, which, when specialised to
actual smooth functions (where every Clairaut expression is literally 0), gives

      c_i  =  M_i * R + N_i * E2      as functions.

Here M_i, N_i are polynomials in the free jets PA_jk, PB_jk with j+k <= M.

Run:  python -u audit_c02_mult2.py
"""

import itertools
import sympy as sp


def setup(M=5, amod=7, p=32003):
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
    return subst(R0), subst(E20), subst(c1), subst(c2), free


def main():
    Rf, Ef, c1f, c2f, free = setup()
    freesyms = sorted(free.values(), key=str)
    # candidate multipliers: degree <= 2 polynomials in the free jets
    basis = [sp.Integer(1)] + freesyms
    for i, s1 in enumerate(freesyms):
        for s2 in freesyms[i:]:
            basis.append(s1 * s2)
    print('multiplier basis size: %d' % len(basis))
    KR = sp.symbols('kr0:%d' % len(basis))
    KE = sp.symbols('ke0:%d' % len(basis))
    unknowns = list(KR) + list(KE)
    for name, f in (('c1', c1f), ('c2', c2f)):
        MR = sum(c * b for c, b in zip(KR, basis))
        ME = sum(c * b for c, b in zip(KE, basis))
        expr = sp.expand(f - MR * Rf - ME * Ef)
        poly = sp.Poly(expr, *freesyms)
        eqs = poly.coeffs()
        print('%s: %d equations, %d unknowns' % (name, len(eqs), len(unknowns)))
        sol = sp.solve(eqs, unknowns, dict=True)
        print('  solutions: %d' % len(sol))
        if sol:
            s = sol[0]
            MRs = sp.expand(MR.subs(s))
            MEs = sp.expand(ME.subs(s))
            chk = sp.expand(f - MRs * Rf - MEs * Ef)
            print('  MR =', MRs)
            print('  ME =', MEs)
            print('  residual:', chk)


if __name__ == '__main__':
    main()
