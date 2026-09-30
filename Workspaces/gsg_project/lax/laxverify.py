"""
laxverify.py -- verify the discrete Lax pair WITH spectral parameter.

Wave function:   psi_n(z) = tauhat_n(z)/tau_n = 1 + Q_n/z
Spectral problem: psi_{n+1}(z) = L_n(z) psi_n(z),  L_n(z) = (z+Q_{n+1})/(z+Q_n)
x-flow:           d_x psi_n(z) = M_n(z) psi_n(z),  M_n(z) = (A_n z + B_n)/(z + Q_n)

Discrete Lax compatibility:   d_x L_n + L_n M_n = M_{n+1} L_n
"""
import sys
from itertools import permutations

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from mpt import MP

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
N = 3
M = MP(N, A, H, PS, QS)
uu = [M.p[i] for i in range(N)]
vv = [M.q[k] for k in range(N)]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100


def minor_at(Mm, n, j, s, i, k, Xv, Yv, Tv):
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
            term *= Mm.entry(n, j, ii, perm[a], s, Xv, Yv, Tv)
        tot += term
    return tot


def Q_at(n, j, Xv, Yv, Tv, s=None):
    s = M.a if s is None else s
    tn = M.tau(n, j, s=s, xv=Xv, yv=Yv, tv=Tv)
    tot = mp.mpf(0)
    for i in range(N):
        for k in range(N):
            tot += uu[i] * vv[k] * minor_at(M, n, j, s, k, i, Xv, Yv, Tv)
    return tot / tn


print('=' * 92)
print('Q_n(x) along the x direction (needed for the x-flow coefficients)')
print('=' * 92)
EPS = mp.mpf('1e-12')
z1 = mp.mpf('3.1')
z2 = mp.mpf('7.7')

for j in (0, 1):
    Q = {}
    Qx = {}
    Qxx = {}
    for n in (0, 1, 2):
        qm = Q_at(n, j, X0 - EPS, Y0, T0)
        q0 = Q_at(n, j, X0, Y0, T0)
        qp = Q_at(n, j, X0 + EPS, Y0, T0)
        Q[n] = q0
        Qx[n] = (qp - qm) / (2 * EPS)
        Qxx[n] = (qp - 2 * q0 + qm) / EPS ** 2
    print('  j=%d' % j)
    for n in (0, 1, 2):
        print('     n=%d Q=%-16s Q_x=%-16s Q_xx=%s'
              % (n, mp.nstr(Q[n], 12), mp.nstr(Qx[n], 12), mp.nstr(Qxx[n], 12)))

    # M_n(z) = d_x ln(1 + Q_n/z) = (Q_x/z)/(1+Q_n/z) = Q_x/(z+Q_n)
    # L_n(z) = (z+Q_{n+1})/(z+Q_n)
    # check  d_x L_n + L_n M_n - M_{n+1} L_n = 0
    print('     discrete Lax residual  d_x L_n + L_n M_n - M_{n+1} L_n :')
    for n in (0, 1):
        # d_x L_n
        dL = (Qx[n + 1] * (z1 + Q[n]) - (z1 + Q[n + 1]) * Qx[n]) / (z1 + Q[n]) ** 2
        Ln = (z1 + Q[n + 1]) / (z1 + Q[n])
        Mn = Qx[n] / (z1 + Q[n])
        Mnp = Qx[n + 1] / (z1 + Q[n + 1])
        res = dL + Ln * Mn - Mnp * Ln
        # second spectral value
        dL2 = (Qx[n + 1] * (z2 + Q[n]) - (z2 + Q[n + 1]) * Qx[n]) / (z2 + Q[n]) ** 2
        Ln2 = (z2 + Q[n + 1]) / (z2 + Q[n])
        Mn2 = Qx[n] / (z2 + Q[n])
        Mnp2 = Qx[n + 1] / (z2 + Q[n + 1])
        res2 = dL2 + Ln2 * Mn2 - Mnp2 * Ln2
        print('        n=%d  z=%s : %-12s     z=%s : %s'
              % (n, z1, mp.nstr(res, 4), z2, mp.nstr(res2, 4)))
