"""
crosscheck.py -- the two independent tau implementations must agree.

   tau_A : det of the matrix built from  entry(n,j,i,k,s) = coef * exp(expo)
   tau_B : dtau via the permutation expansion (should be identical)

They are different code paths; any disagreement means a bug.  We normalise by
the largest |entry| to stay well conditioned.
"""
import sys
from itertools import permutations

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from mpt import MP

mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
# a deliberately SMALL, benign point
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100


def tau_matrix(M, n, j, s, Xv, Yv, Tv):
    Nn = M.N
    mat = mp.matrix(Nn, Nn)
    scale = mp.mpf(0)
    raw = mp.matrix(Nn, Nn)
    for i in range(Nn):
        for k in range(Nn):
            raw[i, k] = M.entry(n, j, i, k, s, Xv, Yv, Tv)
            scale = max(scale, abs(raw[i, k]))
    for i in range(Nn):
        for k in range(Nn):
            mat[i, k] = raw[i, k] / scale
            if i == k:
                mat[i, k] += 1
    return mp.det(mat) * scale, scale


print('=' * 92)
print('tau_A (matrix determinant) vs tau_B (permutation expansion)')
print('=' * 92)
for N in (1, 2, 3, 4):
    M = MP(N, A, H, PS[:N], QS[:N])
    for (n, j) in [(0, 0), (1, 0), (0, 1), (2, 1)]:
        ta, sc = tau_matrix(M, n, j, M.a, X0, Y0, T0)
        tb = M.tau(n, j, s=M.a, xv=X0, yv=Y0, tv=T0)
        print('  N=%d n=%d j=%d  tau_A=%-22s tau_B=%-22s  rel.diff=%s'
              % (N, n, j, mp.nstr(ta, 16), mp.nstr(tb, 16),
                 mp.nstr(abs(ta - tb) / max(abs(ta), abs(tb)), 4)))

print()
print('=' * 92)
print('cross-check at the LARGE point used before (conditioning check)')
print('=' * 92)
X1, Y1, T1 = mp.mpf(1) / 3, mp.mpf(-2) / 5, mp.mpf(3) / 7
for N in (1, 2, 3):
    M = MP(N, A, H, PS[:N], QS[:N])
    for (n, j) in [(0, 0), (1, 0)]:
        ta, sc = tau_matrix(M, n, j, M.a, X1, Y1, T1)
        tb = M.tau(n, j, s=M.a, xv=X1, yv=Y1, tv=T1)
        print('  N=%d n=%d  tau_A=%-22s tau_B=%-22s  rel.diff=%s'
              % (N, n, mp.nstr(ta, 16), mp.nstr(tb, 16),
                 mp.nstr(abs(ta - tb) / max(abs(ta), abs(tb)), 4)))
