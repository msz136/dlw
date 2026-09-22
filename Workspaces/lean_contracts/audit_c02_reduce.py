"""
Step 0b: an explicit membership certificate for c1 and c2 in the ideal generated
by the two smooth hypotheses alone.

Ambient ring: polynomials in the jets A_ijk, B_ijk (total order <= M), i.e.
C^infinity jets at a point WITH all Clairaut (mixed-partial symmetry) relations
imposed by the substitution A_ijk -> a_(i-k)jk  (only the free coordinates
A_0jk / B_0jk are used).

Smooth hypotheses (as FUNCTIONS, so all their partials vanish too):
    (I)  R  := A_200 + B_100^2 + B_001 + 2a B_100
    (II) E2 := beta_y*(S_xx + (D_x)^2 + D_t + 2a D_x) + 2 B_100
             with beta_y = (A_010-B_010)/2, S = alpha+beta_y, D = alpha-beta_y,
             alpha = (A+B)/2.

We look for identity elements

    c_i  =  sum_{q=0..Q} ( coefficient_q ) * d^q(dx^p dy^r dt^s) R
          + sum_{r=0..P} ( coefficient_r ) * d^r(...) E2

where each coefficient is an arbitrary smooth function expression of the same
form:  Sum_k (aux_k) * (a jet monomial), with aux_k fresh indeterminates whose
own derivatives we control (zeta: x only; chi: y only).

Membership in the *ambient* ring is checked by Groebner reduction of the residual.

Run:  python -u audit_c02_reduce.py
"""

import sys
import itertools
import sympy as sp


def main():
    p = 32003
    amod = 7
    M = 5          # maximal total jet order
    NX = 3         # aux zeta with 0..NX x-derivatives (zeta_t = zeta_y = 0)
    NY = 2         # aux chi with 0..NY y-derivatives (chi_x = chi_t = 0)
    # derivative orders we allow for the hypotheses
    RORD = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0),
            (0, 0, 2), (1, 1, 0)]
    EORD = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]

    A, B = {}, {}
    for i, j, k in itertools.product(range(M + 1), repeat=3):
        if i + j + k <= M:
            A[(i, j, k)] = sp.Symbol('A%d%d%d' % (i, j, k))
            B[(i, j, k)] = sp.Symbol('B%d%d%d' % (i, j, k))
    a = sp.Integer(amod)

    # ---- Clairaut substitution: keep only the free coordinates -------------
    # A_ijk  with i>=1  ->  A_(i-1)(j+1)k  -> ... -> A_0(j+i)k
    free = {}          # (0,j,k) -> canonical symbol
    for j, k in itertools.product(range(M + 1), repeat=2):
        if j + k <= M:
            free[('A', j, k)] = sp.Symbol('PA_%d_%d' % (j, k))
            free[('B', j, k)] = sp.Symbol('PB_%d_%d' % (j, k))

    def canon(sym):
        # recover the index from the name
        nm = str(sym)
        if nm[0] == 'A':
            i, j, k = int(nm[1]), int(nm[2]), int(nm[3])
            return free[('A', j + i, k)]
        i, j, k = int(nm[1]), int(nm[2]), int(nm[3])
        return free[('B', j + i, k)]

    def subst(expr):
        sub = {s: canon(s) for s in expr.free_symbols
               if str(s)[0] in 'AB' and len(str(s)) == 4 and str(s)[1:].isdigit()}
        e = sp.expand(expr.subs(sub))
        return e

    # ---- auxiliary function symbols ---------------------------------------
    # zeta_k : a smooth function of x;  we write A - zeta_k, etc.
    Z = {(q, i): sp.Symbol('Zw%d_%d' % (q, i)) for q in range(NX + 1) for i in range(2)}
    Y = {(q, j): sp.Symbol('Yw%d_%d' % (q, j)) for q in range(NX + 1) for j in range(2)}
    # Chi_q : smooth in y
    C = {(q, i): sp.Symbol('Cw%d_%d' % (q, i)) for q in range(NY + 1) for i in range(2)}

    # (A - zeta)_0jk = PA_jk - Z[q,j] for k=0 ; for k>=1 the t-derivative of zeta
    # is zero but the *mixed* jet (A-zeta)_0jk = PA_jk - (d^k/dt^k) zeta = PA_jk
    # for k>=1 only if zeta has no t-dependence: yes, zeta = zeta(x) only.
    # So (A-zeta)_0jk = PA_jk  for k>=1 ; = PA_j0 - Z[q,0] for k=0
    # but we also need x-derivatives of (A - zeta), which live in PA_?  hmm.
    #
    # Simpler and sufficient: use NON-differentiated coefficients only, i.e.
    #   c_i = c_R * R + c_E * E2,  c_R and c_E arbitrary smooth functions.
    # Decide whether that is possible first.
    print('M=%d  NX=%d  NY=%d' % (M, NX, NY))
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

    # differentiate R and E2
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

    Rgens = []
    for (i, j, k) in RORD:
        e = R0
        for _ in range(i):
            e = der(e, 0)
        for _ in range(j):
            e = der(e, 1)
        for _ in range(k):
            e = der(e, 2)
        Rgens.append(e)
    Egens = []
    for (i, j, k) in EORD:
        e = E20
        for _ in range(i):
            e = der(e, 0)
        for _ in range(j):
            e = der(e, 1)
        for _ in range(k):
            e = der(e, 2)
        Egens.append(e)

    # free (Clairaut-reduced) variables
    freesyms = sorted(free.values(), key=str)
    Rf = [subst(g) for g in Rgens]
    Ef = [subst(g) for g in Egens]
    c1f = subst(c1)
    c2f = subst(c2)

    # membership test: is c_if in the ideal <Rf, Ef>?  (no coefficients needed)
    G = sp.groebner(Rf + Ef, *freesyms, modulus=p, order='grevlex')
    print('GB size %d' % len(G.exprs))
    for name, f in (('c1', c1f), ('c2', c2f)):
        out = G.reduce(f)
        r = out[0] if isinstance(out, tuple) else out
        r = sp.expand(r[0] if isinstance(r, list) else r)
        print('%s reduced (no coefficients): %s' % (name, r))


if __name__ == '__main__':
    main()
