"""
wave.py -- the discrete Lax operator of the semidiscrete DLW system.

Natural basis:  M(n)_{ik} = c_k delta_ik + c_k A_ik(n) R_i C_k  with the
eigenvectors of the diagonal parts, so the natural (normalised) wave function is

      phi_n := tauhat_n / s_n ,      s_n := prod_{i,k} M(n)_{ik}^{1/N} (geometric mean)
or simply  s_n = A_ik(n) R_i C_k  -- which by construction is index independent
only for the leading exponential.

We therefore determine the Lax operator DIRECTLY from the data:
      L_n(z) := tauhat_{n+1}(z) tau_n / ( tauhat_n(z) tau_{n+1} )
as a function of z, and fit the rational form (z + beta_n)/(z + alpha_n).
"""
import sys
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
T = Tau(3, A, H, PS, QS)
N = T.N
uu, vv = list(T.p), list(T.q)


def tauhat(n, zinv, xv=X0, yv=Y0, tv=T0):
    M = T.gram(n, T.a, xv, yv, tv).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * uu[i] * vv[k]
    return det_exact(M)


def L(n, z):
    return tauhat(n + 1, 1 / z) * T.tau(n, xv=X0, yv=Y0, tv=T0) / \
        (tauhat(n, 1 / z) * T.tau(n + 1, xv=X0, yv=Y0, tv=T0))


print('=' * 94)
print('L_n(z) = tauhat_{n+1}(z) tau_n / (tauhat_n(z) tau_{n+1})')
print('=' * 94)
for n in (0, 1, 2):
    print('  n=%d' % n)
    for z in (mp.mpf('1.5'), mp.mpf(3), mp.mpf(10), mp.mpf(100), mp.mpf(10000)):
        print('     z=%-10s L_n(z) = %s' % (mp.nstr(z, 6), mp.nstr(L(n, z), 20)))

print()
print('=' * 94)
print('Fit L_n(z) = C_n (z + beta_n)/(z + alpha_n)  using three z values')
print('=' * 94)
for n in (0, 1, 2):
    z1, z2, z3 = mp.mpf(2), mp.mpf(5), mp.mpf(20)
    l1, l2, l3 = L(n, z1), L(n, z2), L(n, z3)
    # unknowns C, alpha, beta:  L(z)(z+alpha) = C(z+beta)
    # => L z + L alpha = C z + C beta  ->  (L1-L2) alpha + (L2 z2 - L1 z1) = C(z2-z1) ...
    # solve the 3x3 linear system  L_i z_i + L_i alpha - C z_i - C beta = 0
    Mx = mp.matrix(3, 3)
    rhs = mp.matrix(3, 1)
    for r, (zz, ll) in enumerate([(z1, l1), (z2, l2), (z3, l3)]):
        Mx[r, 0] = ll            # alpha
        Mx[r, 1] = -zz           # C
        Mx[r, 2] = -1            # C*beta
        rhs[r] = -ll * zz
    sol = mp.lu_solve(Mx, rhs)
    alpha, C, Cbeta = sol[0], sol[1], sol[2]
    print('  n=%d  alpha=%s   C=%s   beta=%s'
          % (n, mp.nstr(alpha, 16), mp.nstr(C, 16), mp.nstr(Cbeta / C, 16)))
    for z in (mp.mpf('1.5'), mp.mpf(7), mp.mpf(50)):
        print('        z=%-8s L=%-20s fit=%-20s' % (mp.nstr(z, 4), mp.nstr(L(n, z), 16),
                                                    mp.nstr(C * (z + Cbeta / C) / (z + alpha), 16)))
