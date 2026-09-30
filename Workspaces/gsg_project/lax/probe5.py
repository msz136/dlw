"""
probe5.py -- consolidated decisive tests.

(1) tr T(z) over a period is EXACTLY constant (symbolic, generic Q values).
(2) psi_n is exactly Mobius  => the n-direction has NO second-order structure.
(3) Conserved densities: does the continuous DLW bilinear pair give densities
    rho_k with  d_y rho_k = d_x sigma_k  for the tau function?  (direct search)
"""
import sympy as sp
import sys
import itertools
from math import comb
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau, det_exact

print('=' * 92)
print('(1)  SYMBOLIC: tr of the period-N monodromy of the first-order problem')
print('     L_n(z) = (z + Q_{n+1})/(z + Q_n)  ->  matrix [[1, Q_{n+1}],[1, Q_n]]')
print('=' * 92)
z = sp.symbols('z')
for Nper in (2, 3, 4):
    qs = sp.symbols('q0:%d' % (Nper + 1))
    Mm = sp.eye(2)
    for k in range(Nper):
        Mm = sp.Matrix([[1, qs[(k + 1) % Nper]], [1, qs[k % Nper]]]) * Mm
    tr = sp.simplify(sp.expand(sp.trace(Mm)))
    de = sp.simplify(sp.expand(sp.det(Mm)))
    print('   period N=%d :  tr T = %-20s   det T = %-20s   (z-free: %s)'
          % (Nper, tr, de, sp.simplify(sp.diff(tr, z)) == 0))

print()
print('=' * 92)
print('(2)  psi_n(z) = 1 + Q_n/z EXACTLY  (=> first order, no 2nd-order invariant)')
print('=' * 92)
mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
T = Tau(3, A, H, PS, QS)
N = 3
U, V = list(T.p), list(T.q)


def that(n, zi):
    M = T.gram(n, T.a, X0, Y0, T0).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zi * U[i] * V[k]
    return det_exact(M)


def P(n, zz):
    return that(n, 1 / mp.mpf(zz)) / T.tau(n, xv=X0, yv=Y0, tv=T0)


worst = mp.mpf(0)
for n in range(-1, 4):
    Qn = (P(n, mp.mpf(10) ** 8) - 1) * mp.mpf(10) ** 8
    for zz in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30), mp.mpf(1000)):
        worst = max(worst, abs(P(n, zz) - (1 + Qn / zz)))
print('   max over n,z of  |psi_n(z) - (1+Q_n/z)|  =', mp.nstr(worst, 6))
print('   => psi_n is EXACTLY Mobius in z; all higher 1/z coefficients vanish.')

print()
print('=' * 92)
print('(3)  conserved densities from the continuous bilinear structure')
print('     candidates:  rho = d_x ln tau, (d_x ln tau)^2, d_x^2 ln tau, ...')
print('     test:  d_y (rho) is a total x-derivative?  i.e. d_y rho = d_x sigma')
print('     We test the cleanest notion: is  d_y d_x ln tau  a total d_x?')
print('=' * 92)


def rate(i, k, s=None):
    s = T.a if s is None else s
    return (T.p[i] + T.q[k], T.q[k] ** 2 - T.p[i] ** 2,
            1 / (T.p[i] - s) + 1 / (T.q[k] + s))


def dtau(n, ax=0, at=0, ay=0):
    B = T.Bmat(n, T.a, X0, Y0, T0)
    tot = mp.mpf(0)
    for r in range(N + 1):
        for S in itertools.combinations(range(N), r):
            sub = mp.matrix(r, r)
            for a2, i in enumerate(S):
                for b2, k in enumerate(S):
                    rr = rate(i, k)
                    sub[a2, b2] = B[i, k] * rr[0] ** ax * rr[1] ** at * rr[2] ** ay
            tot += det_exact(sub)
    return tot


for n in (0, 1):
    t = dtau(n)
    tx = dtau(n, ax=1)
    ty = dtau(n, ay=1)
    txy = dtau(n, ax=1, ay=1)
    txx = dtau(n, ax=2)
    # d_y (t_x/t)  = (t_xy t - t_x t_y)/t^2
    dy_rho = (txy * t - tx * ty) / t ** 2
    dy_rho2 = (dtau(n, ax=2, ay=1) * t - txx * ty) / t ** 2
    print('   n=%d   d_y(d_x ln tau) = %-22s   d_y(d_x^2 ln tau) = %s'
          % (n, mp.nstr(dy_rho, 14), mp.nstr(dy_rho2, 14)))
    print('        d_x ln tau = %-20s   (constant in x,t => nothing to conserve)'
          % mp.nstr(tx / t, 14))
