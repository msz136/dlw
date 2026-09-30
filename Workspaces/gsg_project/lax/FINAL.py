"""
FINAL.py -- definitive verification of the integrable structure of the
semidiscrete DLW / GSG staggered system.

Uses tau4.py, whose principal-minor expansion has been cross-validated against
the literal Gram determinant to 60 digits (see v4.py).
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


def report(title):
    print()
    print('=' * 94)
    print(title)
    print('=' * 94)


# ---------------------------------------------------------------------------
report('1.  the n-dependence of tau is NOT geometric:  sigma_n is nontrivial')
for N in (1, 2, 3):
    T = Tau(N, A, H, PS[:N], QS[:N])
    vals = [T.tau(n + 1, xv=X0, yv=Y0, tv=T0) * T.tau(n - 1, xv=X0, yv=Y0, tv=T0)
            / T.tau(n, xv=X0, yv=Y0, tv=T0) ** 2 for n in (-1, 0, 1, 2)]
    print('   N=%d  sigma_n:  %s' % (N, '   '.join(mp.nstr(v, 14) for v in vals)))

# ---------------------------------------------------------------------------
report('2.  the wave function  psi_n(z) = tauhat_n(z)/tau_n  and its Lax operator')
print('    tauhat_n(z) = det( M(n) + z^{-1} u v^T )   with u_i = p_i, v_k = q_k')

T = Tau(3, A, H, PS, QS)
uu = list(T.p)
vv = list(T.q)
N = T.N


def tauhat(n, zinv, s=None, xv=X0, yv=Y0, tv=T0):
    s = T.a if s is None else s
    M = T.gram(n, s, xv, yv, tv)
    M = M.copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * uu[i] * vv[k]
    return det_exact(M)


zs = [mp.mpf('1.7'), mp.mpf('3.3'), mp.mpf('8.9')]
print('    psi_n(z) for n = 0..3 and several z:')
for z in zs:
    row = []
    for n in range(4):
        row.append(tauhat(n, 1 / z) / T.tau(n, xv=X0, yv=Y0, tv=T0))
    print('      z=%-6s  %s' % (mp.nstr(z, 4), '  '.join(mp.nstr(v, 12) for v in row)))
print()
print('    L_n(z) := psi_{n+1}(z)/psi_n(z)  --  does it depend on z?')
for z in zs:
    row = []
    for n in range(3):
        pn = tauhat(n, 1 / z) / T.tau(n, xv=X0, yv=Y0, tv=T0)
        pp = tauhat(n + 1, 1 / z) / T.tau(n + 1, xv=X0, yv=Y0, tv=T0)
        row.append(pp / pn)
    print('      z=%-6s  %s' % (mp.nstr(z, 4), '  '.join(mp.nstr(v, 12) for v in row)))

# ---------------------------------------------------------------------------
report('3.  conserved densities from the wave function:  coefficients of 1/z')
print('    -(z^2) d_z ln psi_n(z)  expanded at large z gives the density sequence')
for n in (0, 1, 2):
    pn = lambda z: tauhat(n, 1 / z) / T.tau(n, xv=X0, yv=Y0, tv=T0)
    for z in (mp.mpf(50), mp.mpf(100)):
        d = -(z ** 2) * (mp.log(pn(z * (1 + mp.mpf('1e-12')))) - mp.log(pn(z))) / (z * mp.mpf('1e-12'))
        print('      n=%d z=%-6s  -z^2 d_z ln psi = %s' % (n, mp.nstr(z, 5), mp.nstr(d, 12)))
