"""
Step 0d: explicit certificate in the coefficient ring C^inf(J^2).

Unknown smooth multipliers are modelled by formal power series: we let the
multiplier be an arbitrary element of the *jet ring* truncated at the order that
the computation actually needs.  Concretely, instead of guessing a shape we run
the division algorithm by hand:

    c_i  is divided by the GB {R, dx R, dy R, ...} of  K' = <d^q R, d^r E2>+Clairaut

in the ambient frame, with remainders expressed in the *free* coordinates.

Because the target lies in K', we can request the cofactors from `reduce` and
then lift them into derivative form.  The lifting step is the crux: a cofactor
that is a polynomial in the free jets PA_jk is NOT literally a function of
(A,B) unless it is a differential polynomial.  We therefore redo the division
with the *derivative* generators taken in Weyl form:

    Rgan = { d^q R }  presented as  W_q(A, B)  (a differential operator applied to R)

and solve for structure polynomials P_q, Q_r with differential-polynomial
coefficients, i.e. coefficients that are themselves jets of auxiliary functions.

We shortcut: allow the coefficient ring to be C^inf (free, unconstrained jets)
and require the identity to hold as an identity in the ambient jet ring.  This is
a *stronger* requirement than needed for Lean (there the coefficients are concrete
smooth functions and only their actual jets matter), but it gives a certificate
that is trivially checkable.  Print the search result either way.

Run:  python -u audit_c02_mult3.py
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
    return A, B, der, R0, E20, c1, c2


def main():
    M = 5
    A, B, der, R0, E20, c1, c2 = build(M, 7, 32003)
    # derivative generators
    dR = {(0, 0, 0): R0}
    dE = {(0, 0, 0): E20}
    for idx in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0)]:
        e = R0
        for _ in range(idx[0]):
            e = der(e, 0)
        for _ in range(idx[1]):
            e = der(e, 1)
        for _ in range(idx[2]):
            e = der(e, 2)
        dR[idx] = e
    for idx in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        e = E20
        for _ in range(idx[0]):
            e = der(e, 0)
        for _ in range(idx[1]):
            e = der(e, 1)
        for _ in range(idx[2]):
            e = der(e, 2)
        dE[idx] = e

    gens = list(dR.values()) + list(dE.values())
    names = ['dR%s' % (i,) for i in dR] + ['dE%s' % (i,) for i in dE]
    for nm, g in zip(names, gens):
        print('%-14s : %s' % (nm, sp.expand(g)))
    sys_vars = sorted(set().union(*[g.free_symbols for g in gens]) |
                      c1.free_symbols | c2.free_symbols, key=str)
    print('vars %d' % len(sys_vars))
    G = sp.groebner(gens, *sys_vars, modulus=32003, order='grevlex')
    print('GB %d' % len(G.exprs))
    for nm, f in (('c1', c1), ('c2', c2)):
        out = G.reduce(f)
        r = out[0] if isinstance(out, tuple) else out
        r = sp.expand(r[0] if isinstance(r, list) else r)
        print('%s -> %s' % (nm, r))


if __name__ == '__main__':
    main()
