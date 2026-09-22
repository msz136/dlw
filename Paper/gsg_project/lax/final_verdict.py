"""
final_verdict.py -- THE decisive test.

Wave function (standard dKP / Akhmediev-Backlund type):
      psi_n(z) = tau_n(t - [z^{-1}]) / tau_n(t)
with  x -> x - 1/z,  t -> t - (1/2) z^{-2}.

This is NOT Mobius (verified: A_n(z), B_n(z) both z-dependent and B_n != 0),
so the n-recurrence is genuinely second order.  The spectral curve is then
governed by  tr T(z)  of the transfer matrix product over a period:

      [psi_{n+1}]   [ -A_n(z)  -B_n(z) ] [psi_n  ]
      [psi_n    ] = [   1         0    ] [psi_{n-1}]

  tr T(z) NONCONSTANT  =>  nontrivial spectral curve  =>  strong integrability.
  tr T(z) CONSTANT     =>  degenerate                  =>  no discrete hierarchy.
"""
import sys
import itertools
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
N = 3
T = Tau(N, A, H, PS, QS)
TAU = {}


def tau_at(n, xv, tv):
    return T.tau(n, xv=xv, yv=Y0, tv=tv)


for n in range(-4, 7):
    TAU[n] = tau_at(n, X0, T0)


def psi(n, z):
    z = mp.mpf(z)
    return tau_at(n, X0 - 1 / z, T0 - mp.mpf(1) / 2 / z ** 2) / TAU[n]


def AB(n, z):
    p1, p0, pm, p2 = psi(n + 1, z), psi(n, z), psi(n - 1, z), psi(n + 2, z)
    dd = p1 * pm - p0 * p0
    return ((-p2 * pm + p1 * p0) / dd, (p1 * (-p1) - p0 * (-p2)) / dd)


print('=' * 94)
print('tr T(z) for the dKP time-shift wave function, period 3')
print('=' * 94)
for z in (mp.mpf('1.5'), mp.mpf(3), mp.mpf(10), mp.mpf(50), mp.mpf(200), mp.mpf(1000)):
    prod = mp.eye(2)
    for n in (-1, 0, 1):
        An, Bn = AB(n, z)
        prod = mp.matrix([[-An, -Bn], [1, 0]]) * prod
    print('   z=%-8s  tr T = %-26s  det T = %s'
          % (mp.nstr(z, 6), mp.nstr(prod[0, 0] + prod[1, 1], 20),
             mp.nstr(prod[0, 0] * prod[1, 1] - prod[0, 1] * prod[1, 0], 20)))

print()
print('=' * 94)
print('A_n(z), B_n(z) for reference (nonconstant => genuine 2nd order)')
print('=' * 94)
for n in (0, 1):
    for z in (mp.mpf('1.5'), mp.mpf(10), mp.mpf(200)):
        An, Bn = AB(n, z)
        print('   n=%d z=%-8s A=%-22s B=%s' % (n, mp.nstr(z, 6), mp.nstr(An, 18), mp.nstr(Bn, 18)))

print()
print('=' * 94)
print('CONTROL: is T(z) conjugate to a constant matrix?')
print('  eigenvalue ratio  lambda_+/lambda_-  (should vary with z for a')
print('  nontrivial curve; the discriminant  tr^2 - 4 det  is the curve)')
print('=' * 94)
for z in (mp.mpf('1.5'), mp.mpf(3), mp.mpf(10), mp.mpf(50), mp.mpf(200), mp.mpf(1000)):
    prod = mp.eye(2)
    for n in (-1, 0, 1):
        An, Bn = AB(n, z)
        prod = mp.matrix([[-An, -Bn], [1, 0]]) * prod
    tr = prod[0, 0] + prod[1, 1]
    de = prod[0, 0] * prod[1, 1] - prod[0, 1] * prod[1, 0]
    disc = tr ** 2 - 4 * de
    print('   z=%-8s  discriminant tr^2-4det = %s' % (mp.nstr(z, 6), mp.nstr(disc, 20)))
