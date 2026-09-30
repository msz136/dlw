"""
laxpair.py -- verify (exactly, high precision) the discrete linear structure of
the semidiscrete DLW system, and look for its conservation laws.

Established facts to be used:
  (F1) tau_n = C * gamma^n  in n   (sigma_n = 1) : log tau_n is affine in n.
  (F2) tau_n(j) = C' * R^j  in j    (sigma_j = 1).
  (F3) M(n+1,j;e) = z(e) * [ M(n,j;e) + sum_{i,k} u_i v_k E_ik ] with
       z(e) independent of (i,k)  =>  for the rank-one spectral deformation
       tauhat_n(z) = det(M(n,j) + z^{-1} u v^T) we have
            tauhat_n(z)/tau_n = 1 + Q_n / z    (exactly linear in 1/z).

Therefore the natural discrete linear problem in n is
      psi_n(z) = tauhat_n(z)/tau_n = 1 + Q_n/z ,
      psi_{n+1}(z) = L_n(z) psi_n(z),   L_n(z) = (1 + Q_{n+1}/z)/(1 + Q_n/z),
i.e.  (1 + Q_n/z) psi_{n+1} = (1 + Q_{n+1}/z) psi_n   -- a Möbius Lax operator
in the spectral parameter z.

This script checks:
  L1  tauhat_n(z) = tau_n (1 + Q_n/z) exactly, and finds the exact Q_n;
  L2  the discrete Lax equation  d_x L_n = M_{n+1} L_n - L_n M_n  with
      psi_n also satisfying a first-order x-flow;
  L3  which combinations of Q and its x-derivatives are conserved.
"""
import sys
import random

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from mpt import MP

mp.mp.dps = 120
X = mp.mpf(1) / 100
Y = mp.mpf(-1) / 100
T = mp.mpf(1) / 100
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]

N = 3
M = MP(N, A, H, PS, QS)
zz = mp.mpf('2.7')          # a generic spectral value z
uu = [M.p[i] for i in range(N)]     # fixed perturbation u_i = p_i
vv = [M.q[k] for k in range(N)]     # v_k = q_k


def tauhat(n, j, zinv, s=None):
    """det( M(n,j) + zinv * u v^T ) evaluated at (X,Y,T)."""
    from itertools import permutations
    s = M.a if s is None else s
    tot = mp.mpf(0)
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for i in range(N):
            for k in range(i + 1, N):
                if pl[i] > pl[k]:
                    sign = -sign
        term = mp.mpf(sign)
        for i in range(N):
            k = perm[i]
            term *= M.entry(n, j, i, k, s, X, Y, T) + (zinv * uu[i] * vv[k] if i == k else 0)
        # the perturbation is a full rank-one matrix, not diagonal!
        tot += term
    return tot


def tauhat_full(n, j, zinv, s=None):
    """same but with the FULL rank-one perturbation uv^T (all i,k)."""
    from itertools import permutations
    s = M.a if s is None else s
    tot = mp.mpf(0)
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for i in range(N):
            for k in range(i + 1, N):
                if pl[i] > pl[k]:
                    sign = -sign
        term = mp.mpf(sign)
        for i in range(N):
            k = perm[i]
            term *= M.entry(n, j, i, k, s, X, Y, T) + zinv * uu[i] * vv[k]
        tot += term
    return tot


print('=' * 92)
print('L1.  tauhat_n(z) = tau_n * (1 + Q_n/z) exactly?   [full rank-one pert.]')
print('=' * 92)
for j in (0, 1):
    for n in (0, 1, 2):
        t0 = M.tau(n, j, xv=X, yv=Y, tv=T)
        zinv = 1 / zz
        th = tauhat_full(n, j, zinv)
        # solve for Q_n from the identity
        Qn = (th / t0 - 1) * zz
        # verify at a second spectral value
        zz2 = mp.mpf('5.3')
        th2 = tauhat_full(n, j, 1 / zz2)
        pred = t0 * (1 + Qn / zz2)
        print('  j=%d n=%d  Q_n=%-18s  check at z=%s: %s'
              % (j, n, mp.nstr(Qn, 14), zz2, mp.nstr(abs(th2 - pred) / abs(pred), 3)))
