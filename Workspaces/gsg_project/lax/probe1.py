"""
probe1.py -- is the n-direction really first order / trivial?

Three tests, all with the validated tau4 implementation:

  T1. psi_n(z) = 1 + alpha_n/z exactly?  (measures alpha_n accurately)
  T2. the two-step map  L_{n+1} o L_n  -- constant or not?
  T3. large-z expansion psi_n(z) = 1 + a1/z + a2/z^2 + a3/z^3 + ...
      (a2, a3 would be the genuine second-order invariants)
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 120
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
T = Tau(3, A, H, PS, QS)
N = T.N
uu, vv = list(T.p), list(T.q)


def tauhat(n, zinv):
    M = T.gram(n, T.a, X0, Y0, T0).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * uu[i] * vv[k]
    return det_exact(M)


TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-2, 6)}
THAT = {}


def psi(n, z):
    zn = 1 / mp.mpf(z)
    if n not in THAT:
        THAT[n] = tauhat(n, zn)
    return THAT[n] / TAU[n] if n in TAU else None


def psin(n, z):
    return tauhat(n, 1 / mp.mpf(z)) / TAU[n]


print('=' * 92)
print('T1.  is  psi_n(z) = 1 + alpha_n/z  exact?   (dps=120)')
print('=' * 92)
for n in range(4):
    z0 = mp.mpf(10) ** 7
    al = (psin(n, z0) - 1) * z0
    ok = []
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30), mp.mpf(1000)):
        ok.append(abs(psin(n, z) - (1 + al / z)))
    print('   n=%d  alpha_n = %-24s  max|psi-(1+a/z)| over z = %s'
          % (n, mp.nstr(al, 20), mp.nstr(max(ok), 4)))

print()
AL = {}
for n in range(-2, 6):
    z0 = mp.mpf(10) ** 8
    AL[n] = (psin(n, z0) - 1) * z0

print('=' * 92)
print('T2.  two-step map  L_{n+1} o L_n  = (z+a_{n+1}+a_{n+2})/(z+a_n+a_{n+2})')
print('     (derived exactly).  Test numerically.')
print('=' * 92)
for n in range(4):
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30), mp.mpf(1000), mp.mpf(10) ** 5):
        Ln = (z + AL[n + 1]) / (z + AL[n])
        comp = (Ln + AL[n + 2]) / (Ln + AL[n + 1])
        pred = (z + AL[n + 1] + AL[n + 2]) / (z + AL[n] + AL[n + 2])
        print('   n=%d z=%-10s comp=%-22s pred=%-22s rel=%s'
              % (n, mp.nstr(z, 6), mp.nstr(comp, 16), mp.nstr(pred, 16), mp.nstr(abs(comp / pred - 1), 3)))

print()
print('=' * 92)
print('T3.  large-z expansion of psi_n(z):  1 + a1/z + a2/z^2 + a3/z^3 + ...')
print('=' * 92)
for n in range(4):
    z0 = mp.mpf(10) ** 5
    vals = {}
    for z in (10 ** 5, 10 ** 6, 10 ** 7, 10 ** 8):
        vals[z] = psin(n, mp.mpf(z))
    # fit a1,a2,a3 from three large z
    zs = [mp.mpf(10 ** 6), mp.mpf(10 ** 7), mp.mpf(10 ** 8)]
    Mx = mp.matrix(3, 3)
    rhs = mp.matrix(3, 1)
    for r, zz in enumerate(zs):
        Mx[r, 0] = 1 / zz
        Mx[r, 1] = 1 / zz ** 2
        Mx[r, 2] = 1 / zz ** 3
        rhs[r] = vals[int(zz)] - 1
    sol = mp.lu_solve(Mx, rhs)
    print('   n=%d   a1=%-22s a2=%-22s a3=%s'
          % (n, mp.nstr(sol[0], 16), mp.nstr(sol[1], 16), mp.nstr(sol[2], 16)))
