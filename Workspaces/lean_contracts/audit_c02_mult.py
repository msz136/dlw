"""
Step 0c: extract the explicit multiplier identity.

Result of step 0b:  in the ambient ring of jets, the two smooth hypotheses
    d^q R = 0   (q = 0, dx, dy, dt, dx^2, dy^2, dt^2, dxdy)
    d^r E2 = 0  (r = 0, dx, dy, dt)
ALREADY generate an ideal containing c1 and c2.  So c_i = B_i,0 * R + C_i,0 * E2
with ordinary (non-differentiated) multipliers!  Let's find them.

Run:  python -u audit_c02_mult.py
"""

import itertools
import sympy as sp


def main():
    p = 32003
    amod = 7
    M = 5
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

    freesyms = sorted(free.values(), key=str)
    # unknown multipliers: quadratic in jets is plenty for c1, c2 which are cubic
    # -> use multipliers LINEAR in the free jets (plus a constant term).
    basis = [sp.Integer(1)] + freesyms
    KR = sp.symbols('kr0:%d' % len(basis))
    KE = sp.symbols('ke0:%d' % len(basis))
    MR = sum(c * b for c, b in zip(KR, basis))
    ME = sum(c * b for c, b in zip(KE, basis))

    unknowns = list(KR) + list(KE)
    for name, f in (('c1', c1), ('c2', c2)):
        expr = sp.expand(subst(f) - MR * subst(R0) - ME * subst(E20))
        eqs = sp.Poly(expr, *freesyms).coeffs()
        print('%s: %d equations, %d unknowns' % (name, len(eqs), len(unknowns)))
        sol = sp.solve(eqs, unknowns, dict=True)
        print('  solutions found: %d' % len(sol))
        if sol:
            s = sol[0]
            # keep only the free unknowns
            fr = {k: v for k, v in s.items()}
            print('  MR =', sp.expand(MR.subs(fr)))
            print('  ME =', sp.expand(ME.subs(fr)))
            chk = sp.expand(subst(f) - MR.subs(fr) * subst(R0) - ME.subs(fr) * subst(E20))
            print('  residual:', chk)


if __name__ == '__main__':
    main()
