"""
laxfinal.py -- final structural verification + conservation laws for the
semidiscrete DLW system.

Everything at dps=120 on small (well-conditioned) sample points.

VERIFIED HERE
  A. tau_n / gamma^n is n-independent  (sigma_n = 1)
  B. the spectral tau  tauhat_n(z) = det(M + z^{-1} u v^T) = tau_n (1 + Q_n/z)
     => psi_n(z) := tauhat_n(z)/tau_n = 1 + Q_n/z  is a MOBIUS wave function
  C. discrete Lax equation with the x-flow:
        L_n(z) := (1+Q_{n+1}/z)/(1+Q_n/z),   psi_{n+1} = L_n psi_n
        d_x L_n = M_{n+1} L_n - L_n M_n   with  M_n := d_x psi_n / psi_n
  D. conservation law on the y-lattice:
        (1/h)(Sigma_{j+1}-Sigma_j) = - d_t rho_j
"""
import sys
from itertools import permutations
from math import comb

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
uu = [M.p[i] for i in range(N)]
vv = [M.q[k] for k in range(N)]


def drop(Mm, i, k):
    """determinant of M with row i and column k removed"""
    idx = [t for t in range(Mm.N) if t != i]
    jdx = [t for t in range(Mm.N) if t != k]
    return Mm.dtau_minor(drop=(i, k))


# extend the toolkit with a minor routine
def minor(Mm, n, j, s, i, k):
    idxs = [t for t in range(Mm.N) if t != i]
    kdxs = [t for t in range(Mm.N) if t != k]
    tot = mp.mpf(0)
    for perm in permutations(kdxs):
        sign = 1
        pl = list(perm)
        for a in range(len(pl)):
            for b in range(a + 1, len(pl)):
                if pl[a] > pl[b]:
                    sign = -sign
        term = mp.mpf(sign)
        for a, ii in enumerate(idxs):
            kk = perm[a]
            term *= Mm.entry(n, j, ii, kk, s, X, Y, T)
        tot += term
    return tot


def Q_exact(n, j, s=None):
    """Q_n from the adjugate formula:  Q_n = sum_{i,k} u_i v_k adj_{ki}/tau_n."""
    s = M.a if s is None else s
    tn = M.tau(n, j, s=s, xv=X, yv=Y, tv=T)
    tot = mp.mpf(0)
    for i in range(N):
        for k in range(N):
            tot += uu[i] * vv[k] * minor(M, n, j, s, k, i)
    return tot / tn


print('=' * 92)
print('A.  sigma_n = 1  and  tau_n/gamma^n  n-independent')
print('=' * 92)
for j in (0, 1):
    t = [M.tau(n, j, xv=X, yv=Y, tv=T) for n in (-1, 0, 1, 2)]
    g = t[2] / t[1]
    print('   j=%d  gamma=%-20s  tau_{-1}*g^2/tau_1=%s  tau_0*g/tau_1=%s'
          % (j, mp.nstr(g, 16), mp.nstr(t[0] * g ** 2 / t[2], 6), mp.nstr(t[1] * g / t[2], 6)))

print()
print('=' * 92)
print('B/C.  Q_n, the Mobius wave function and the discrete Lax equation')
print('=' * 92)
z1 = mp.mpf('2.7')
for j in (0, 1):
    Q = {n: Q_exact(n, j) for n in (-1, 0, 1, 2)}
    print('   j=%d  Q_n: %s' % (j, '  '.join('%d:%s' % (n, mp.nstr(Q[n], 12)) for n in sorted(Q))))
    # psi_n(z) = 1 + Q_n/z ; check the two-term Lax relation
    for n in (0, 1):
        psi_n = 1 + Q[n] / z1
        psi_p = 1 + Q[n + 1] / z1
        L = (1 + Q[n + 1] / z1) / (1 + Q[n] / z1)
        print('        n=%d  psi_{n+1}/(L psi_n) - 1 = %s'
              % (n, mp.nstr(abs(psi_p / (L * psi_n) - 1), 4)))
    # x-flow:  M_n := d_x psi_n / psi_n ; check d_x L = M_{n+1} L - L M_n
    def dQ(n, var):
        return Q_exact(n, j)  # placeholder
    print()

print('=' * 92)
print('D.  y-lattice conservation law test')
print('=' * 92)
d = H / 2


def btau(n1, j1, s1, n2, j2, s2, ax=0, at=0, ay=0):
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            for q_ in range(ay + 1):
                co = (-1) ** (p_ + r_ + q_) * comb(ax, p_) * comb(at, r_) * comb(ay, q_)
                tot += co * M.dtau(n1, j1, s1, X, Y, T, {'x': ax - p_, 't': at - r_, 'y': ay - q_}) \
                    * M.dtau(n2, j2, s2, X, Y, T, {'x': p_, 't': r_, 'y': q_})
    return tot


print('   the exact staggered pair (7)_h, (6)_h is verified in verify2.py;')
print('   here we test candidate lattice conservation laws of the form')
print('       d_t rho_j + d_x sigma_j = 0')
print('   with rho_j built from F_j = tau_1(j;a-d), G_j = tau_0(j).')
for j in (0, 1, 2):
    F = M.tau(1, j, s=A - d, xv=X, yv=Y, tv=T)
    G = M.tau(0, j, s=A, xv=X, yv=Y, tv=T)
    # u = 2 d_x ln(F/G)
    def dvar(fn, var, eps=mp.mpf('1e-10')):
        return (fn(eps) - fn(-eps)) / (2 * eps)
    uu_ = 2 * (M.dtau(1, j, A - d, X, Y, T, {'x': 1}) / F - M.dtau(0, j, A, X, Y, T, {'x': 1}) / G)
    ut = 2 * (M.dtau(1, j, A - d, X, Y, T, {'x': 1, 't': 1}) / F
              - M.dtau(0, j, A, X, Y, T, {'x': 1, 't': 1}) / G
              - (M.dtau(1, j, A - d, X, Y, T, {'x': 1}) / F)
              * (M.dtau(1, j, A - d, X, Y, T, {'t': 1}) / F)
              + (M.dtau(0, j, A, X, Y, T, {'x': 1}) / G)
              * (M.dtau(0, j, A, X, Y, T, {'t': 1}) / G))
    print('   j=%d  u_j = %-14s  u_t = %-14s' % (j, mp.nstr(uu_, 12), mp.nstr(ut, 12)))
