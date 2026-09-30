"""
dkp.py -- the PROPER dKP wave function test.

The standard dKP/KP wave function carries the spectral parameter through the
time shift [z^{-1}]:
      t_i  ->  t_i - (1/i) z^{-i} ,     i.e.  x -> x - 1/z,  t2 -> t2 - (1/2)z^{-2}
and the Baklund/Akhmel wave function is
      psi_n(z) = tau_n(t - [z^-1])/tau_n(t) * exp(sum t_i z^i)

Here, with our variables  xi_i = p_i x - p_i^2 t + y/(p_i-a), a time shift
x -> x - 1/z and t -> t - (1/2) z^{-2} shifts xi_i by -(p_i + p_i^2/(2z))/z...
We test the tau-ratio directly, at LARGE z (small shift) so that the shift is a
genuine perturbative deformation, and ask whether the resulting psi_n(z) gives a
2nd-order recurrence with nonconstant A_n(z), B_n(z).
"""
import sys
import itertools
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 60
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
N = 3
T = Tau(N, A, H, PS, QS)
TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-3, 5)}


def psi_shift(n, z, which):
    z = mp.mpf(z)
    dx = -1 / z
    dt = -mp.mpf(1) / 2 / z ** 2
    if which == 'x':
        return T.tau(n, xv=X0 + dx, yv=Y0, tv=T0) / TAU[n]
    if which == 't':
        return T.tau(n, xv=X0, yv=Y0, tv=T0 + dt) / TAU[n]
    if which == 'both':
        return T.tau(n, xv=X0 + dx, yv=Y0, tv=T0 + dt) / TAU[n]
    if which == 'y':
        return T.tau(n, xv=X0, yv=Y0 + dx, tv=T0) / TAU[n]


def AB(psi, n, z):
    p1 = psi(n + 1, z)
    p0 = psi(n, z)
    pm = psi(n - 1, z)
    p2 = psi(n + 2, z)
    dd = p1 * pm - p0 * p0
    if abs(dd) < mp.mpf('1e-55'):
        return None
    return ((-p2 * pm + p1 * p0) / dd, (p1 * (-p1) - p0 * (-p2)) / dd)


for which in ('x', 't', 'both', 'y'):
    print('=' * 92)
    print('dKP time-shift wave function, shift in: %s' % which)
    print('=' * 92)
    for n in (0, 1):
        row = []
        for z in (mp.mpf('3'), mp.mpf(10), mp.mpf(50), mp.mpf(500)):
            sol = AB(lambda m, zz: psi_shift(m, zz, which), n, z)
            row.append((z, sol))
        print('   n=%d' % n)
        for z, sol in row:
            if sol is None:
                print('      z=%-8s degenerate' % mp.nstr(z, 6))
            else:
                print('      z=%-8s  A_n(z)=%-22s B_n(z)=%s'
                      % (mp.nstr(z, 6), mp.nstr(sol[0], 16), mp.nstr(sol[1], 16)))
    print()
