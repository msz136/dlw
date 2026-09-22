"""
gen_cons.py -- generating function for the conserved quantities.

M_n(z) = Q_{n,x}/(z+Q_n)  expands as  sum_{l>=1} (-1)^{l-1} Q_{n,x} Q_n^{l-1} / z^l,
so the conserved densities are the coefficients
      I_l = Q_{n,x} Q_n^{l-1} ,   l = 1, 2, 3, ...
of 1/z^l in the diagonal part of the x-flow.

A density I_l is conserved if  d_y I_l = d_x (something), i.e. if I_l is a total
x-derivative or has vanishing x-average.  We test the cleanest statement:
      d_y (Q_{n,xx}/Q_{n,x}) = d_x ( ... )     /   d_y (ln Q_{n,x}) is a total x-derivative
and more directly, whether the residues of M_n dz are x-integrated invariants.
"""
import sys
from itertools import permutations

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from mpt import MP

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
N = 3
M = MP(N, A, H, PS[:N], QS[:N])
uu = [M.p[i] for i in range(N)]
vv = [M.q[k] for k in range(N)]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
EPS = mp.mpf('1e-10')


def minor_at(n, j, s, i, k, Xv, Yv, Tv):
    idxs = [t for t in range(N) if t != i]
    kdxs = [t for t in range(N) if t != k]
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
            term *= M.entry(n, j, ii, perm[a], s, Xv, Yv, Tv)
        tot += term
    return tot


def Q(n, j, Xv, Yv, Tv, s=None):
    s = M.a if s is None else s
    tn = M.tau(n, j, s=s, xv=Xv, yv=Yv, tv=Tv)
    tot = mp.mpf(0)
    for i in range(N):
        for k in range(N):
            tot += uu[i] * vv[k] * minor_at(n, j, s, k, i, Xv, Yv, Tv)
    return tot / tn


def d(var, fn):
    h = EPS
    if var == 'x':
        return (fn(X0 + h, Y0, T0) - fn(X0 - h, Y0, T0)) / (2 * h)
    if var == 'y':
        return (fn(X0, Y0 + h, T0) - fn(X0, Y0 - h, T0)) / (2 * h)
    return (fn(X0, Y0, T0 + h) - fn(X0, Y0, T0 - h)) / (2 * h)


print('=' * 92)
print('Conserved densities from the x-flow generating function')
print('  M_n(z) = sum_l (-1)^{l-1} Q_{n,x} Q_n^{l-1} / z^l')
print('  test:  d_y rho_l = d_x sigma_l   (rho_l = Q_{n,x} Q_n^{l-1})')
print('=' * 92)
for j in (0, 1):
    for n in (0, 1, 2):
        Qf = lambda Xv, Yv, Tv: Q(n, j, Xv, Yv, Tv)
        Qx = d('x', Qf)
        print('  j=%d n=%d  Q_x = %s' % (j, n, mp.nstr(Qx, 12)))
    print()

print('=' * 92)
print('Ricci/Riccati invariant:  Q_{n,x}^2 / Q_{n,xx}   and friends')
print('=' * 92)
for j in (0, 1):
    for n in (0, 1):
        Qf = lambda Xv, Yv, Tv: Q(n, j, Xv, Yv, Tv)
        Qx = d('x', Qf)
        def Qxf(Xv, Yv, Tv):
            return (Qf(Xv + EPS, Yv, Tv) - Qf(Xv - EPS, Yv, Tv)) / (2 * EPS)
        Qxx = d('x', Qxf)
        print('  j=%d n=%d   Q_x^2/Q_xx = %s' % (j, n, mp.nstr(Qx ** 2 / Qxx, 12)))
