"""
probe3.py -- find the GENUINE spectral problem.

The rank-one deformation gives psi_n(z) = 1 + Q_n/z, i.e. FIRST order in n with
a trivial (constant) z-independent monodromy.  So the genuine spectral problem,
if it exists, cannot be that.

Here we test for a genuine SECOND-ORDER (2DTL-type) spectral problem

      psi_{n+1} + A_n(z) psi_n + B_n(z) psi_{n-1} = 0

by direct elimination on the exact wave function psi_n(z) = tauhat_n(z)/tau_n,
using several independent constructions of tauhat:

  (a) rank-one deformation  M(n) + z^{-1} u v^T        (u_i=p_i, v_k=q_k)
  (b) general rank-one      M(n) + z^{-1} u v^T        (random u, v)
  (c) c-perturbation        M(n) with c_j -> c_j + z^{-1}
  (d) time-shift (dKP) wave function  tau(n; t - [z^-1]) / tau(n)

For each, we compute psi_n(z) at n-1, n, n+1 for many z and solve for
A_n(z), B_n(z); then we ask whether B_n(z) is identically zero (=> first order
in disguise) and whether A_n, B_n are nonconstant in z.
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
TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-3, 4)}


def tauhat_rank1(n, zinv, u, v):
    M = T.gram(n, T.a, X0, Y0, T0).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * u[i] * v[k]
    return det_exact(M)


def psi_rank1(n, z, u, v):
    return tauhat_rank1(n, 1 / mp.mpf(z), u, v) / TAU[n]


def psi_cpert(n, z, delta):
    """deform the diagonal parameters c_j -> c_j + delta"""
    B = T.Bmat(n, T.a, X0, Y0, T0)
    tot = mp.mpf(0)
    for r in range(N + 1):
        for S in itertools.combinations(range(N), r):
            sub = mp.matrix(r, r)
            for a2, i in enumerate(S):
                for b2, k in enumerate(S):
                    sub[a2, b2] = B[i, k] + (delta if i == k else 0)
            tot += det_exact(sub)
    return tot / TAU[n]


def psi_timeshift(n, z):
    """dKP wave function: shift x by 1/z and t by -(1/2)/z^2"""
    dx = 1 / mp.mpf(z)
    dt = -mp.mpf(1) / 2 / mp.mpf(z) ** 2
    return T.tau(n, xv=X0 + dx, yv=Y0, tv=T0 + dt) / TAU[n]


def solve_AB(p, pm, p0):
    """solve p = -(A p0 + B pm) for A,B is 1 equation, 2 unknowns -> need 2 z.
    We instead probe with two different z values and report the resulting
    linear system's consistency, returning (A,B) from a least-squares solve
    over many z values."""
    return None


print('=' * 92)
print('probe A: rank-one deformation with u_i=p_i, v_k=q_k  (the previous choice)')
print('=' * 92)
U, V = list(T.p), list(T.q)
for n in (1, 2):
    print('  n=%d' % n)
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30)):
        p = psi_rank1(n + 1, z, U, V)
        p0 = psi_rank1(n, z, U, V)
        pm = psi_rank1(n - 1, z, U, V)
        # if first order: p = L p0 with L = (z+Q_{n+1})/(z+Q_n); check
        ratio_p = p / p0
        ratio_0 = p0 / pm
        same = abs(ratio_p / ratio_0 - 1)
        print('     z=%-6s  psi_{n+1}/psi_n=%-18s psi_n/psi_{n-1}=%-18s  equal? %s'
              % (mp.nstr(z, 4), mp.nstr(ratio_p, 14), mp.nstr(ratio_0, 14), mp.nstr(same, 3)))

print()
print('=' * 92)
print('probe B: c-perturbation wave function, psi_n(z) = tau_n(c+z^-1)/tau_n(c)')
print('=' * 92)
for n in (1, 2):
    print('  n=%d' % n)
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30)):
        p = psi_cpert(n + 1, z, 1 / z)
        p0 = psi_cpert(n, z, 1 / z)
        pm = psi_cpert(n - 1, z, 1 / z)
        print('     z=%-6s  psi=%s %s %s' % (mp.nstr(z, 4), mp.nstr(p, 12),
                                              mp.nstr(p0, 12), mp.nstr(pm, 12)))

print()
print('=' * 92)
print('probe C: dKP time-shift wave function')
print('=' * 92)
for n in (1, 2):
    print('  n=%d' % n)
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30)):
        p = psi_timeshift(n + 1, z)
        p0 = psi_timeshift(n, z)
        pm = psi_timeshift(n - 1, z)
        print('     z=%-6s  psi=%s %s %s' % (mp.nstr(z, 4), mp.nstr(p, 12),
                                              mp.nstr(p0, 12), mp.nstr(pm, 12)))
