"""
rank.py -- how many independent monomials does the DLW Gram tau have?

Key question: is  det(c_k d_ik + A_ik E_ik)  with E_ik = e^{xi_i + eta_k} and
A_ik = (1/(p_i+q_k)) (-P_i/Q_k)^n  a genuine sum of many exponentials, or does
it collapse?  The answer controls whether the semidiscrete system carries a
nonlinear Toda potential sigma_n = tau_{n+1}tau_{n-1}/tau_n^2 != 1.
"""
import sys
from itertools import permutations

import mpmath as mp

mp.mp.dps = 60

A_PAR = mp.mpf(17) / 5


def build(N, PS, QS, n, a, s=None):
    """exact monomial expansion of the determinant.

    Returns dict  {exponent-key: coefficient}  where the exponent key is the
    tuple (n-vector, m-vector) of row/column multiplicities, as in
    gsg_project/code/engine.py.
    """
    s = a if s is None else s
    out = {}
    P = [PS[i] - s for i in range(N)]
    Q = [QS[k] + s for k in range(N)]
    # entry (i,k) = delta_ik + A_ik * (row_i * col_k)
    A = [[((-P[i] / Q[k]) ** n) / (PS[i] + QS[k]) for k in range(N)] for i in range(N)]
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for i in range(N):
            for k in range(i + 1, N):
                if pl[i] > pl[k]:
                    sign = -sign
        nvec = [0] * N
        mvec = [0] * N
        coef = mp.mpf(sign)
        ok = True
        for i in range(N):
            k = perm[i]
            if i == k:
                coef *= 1                       # the delta part
            else:
                coef *= A[i][k]
                nvec[i] += 1
                mvec[k] += 1
        if coef != 0:
            key = (tuple(nvec), tuple(mvec))
            out[key] = out.get(key, mp.mpf(0)) + coef
    return {k: v for k, v in out.items() if v != 0}


def rank_num(N, PS, QS, n, a):
    d = build(N, PS, QS, n, a)
    return len(d), d


print('=' * 92)
print('number of nonzero monomials in det(M(n)), and the value of the')
print('coefficient matrix determinant det(A_ik):')
print('=' * 92)
tests = [
    (2, [mp.mpf(29) / 3, mp.mpf(12) / 5], [mp.mpf(40) / 3, mp.mpf(7) / 5], 0),
    (2, [mp.mpf(29) / 3, mp.mpf(12) / 5], [mp.mpf(40) / 3, mp.mpf(7) / 5], 1),
    (3, [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)],
        [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2], 0),
    (3, [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)],
        [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2], 1),
    (4, [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4],
        [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3], 0),
]
for (N, PS, QS, n) in tests:
    d = build(N, PS, QS, n, A_PAR)
    # determinant of the coefficient matrix A_ik
    Amat = mp.matrix(N, N)
    for i in range(N):
        for k in range(N):
            P = PS[i] - A_PAR
            Q = QS[k] + A_PAR
            Amat[i, k] = 1 / (PS[i] + QS[k]) * (-P / Q) ** n
    print('  N=%d n=%d  #monomials=%2d   det(A)=%s'
          % (N, n, len(d), mp.nstr(mp.det(Amat), 12)))
    if N <= 3:
        for k, v in sorted(d.items()):
            print('        key=%s  coef=%s' % (k, mp.nstr(v, 12)))
