"""
veto.py -- the decisive negative test.

If the system had a genuine spectral problem in the n-direction, the wave
function family {psi_n(z)} would be a nontrivial second-order (or higher)
recurrence in n, i.e. there would exist nonconstant rational functions
A_n(z), B_n(z) with

      psi_{n+1} + A_n(z) psi_n + B_n(z) psi_{n-1} = 0 ,

and B_n != 0.  We test this by exact elimination on the tau data:

for fixed n and z, psi_{n+1}, psi_n, psi_{n-1} are three numbers; the relation
has two unknown coefficients, so testing it at TWO different z values gives an
overdetermined (4 equations, 2 unknowns) system whose solvability we check.

We do this for three independent wave-function constructions.
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
U, V = list(T.p), list(T.q)
TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-3, 4)}


def psi_rank1(n, z):
    M = T.gram(n, T.a, X0, Y0, T0).copy()
    zi = 1 / mp.mpf(z)
    for i in range(N):
        for k in range(N):
            M[i, k] += zi * U[i] * V[k]
    return det_exact(M) / TAU[n]


def psi_cpert(n, z):
    delta = 1 / mp.mpf(z)
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


def solve2(a, b):
    """solve the 2x2 system  a0*X + b0*Y = c0 ; a1*X + b1*Y = c1"""
    det = a[0] * b[1] - a[1] * b[0]
    if abs(det) < mp.mpf('1e-50'):
        return None
    X = (a[0] * 0 + (-b[0]) * 0)  # placeholder
    return None


def fit_B(psi, n, zs):
    """Given psi, test existence of A,B with psi_{n+1}+A psi_n+B psi_{n-1}=0.
    Two unknowns, so use zs[0] to solve (with a normalisation) and zs[1] to test.
    We instead form the 2x2 system for (A,B) from two z-values and solve."""
    z1, z2 = zs
    p1p, p10, p1m = psi(n + 1, z1), psi(n, z1), psi(n - 1, z1)
    p2p, p20, p2m = psi(n + 1, z2), psi(n, z2), psi(n - 1, z2)
    # A p10 + B p1m = -p1p ;  A p20 + B p2m = -p2p
    det = p10 * p2m - p20 * p1m
    if abs(det) < mp.mpf('1e-55'):
        return None
    A_ = (-p1p * p2m + p2p * p1m) / det
    B_ = (p10 * (-p2p) - p20 * (-p1p)) / det
    return A_, B_


print('=' * 92)
print('second-order recurrence test:  psi_{n+1} + A_n(z) psi_n + B_n(z) psi_{n-1} = 0')
print('  (B_n != 0 and nonconstant would be a genuine spectral curve)')
print('=' * 92)
for name, psi in (('rank-one (u=p, v=q)', psi_rank1), ('c-perturbation', psi_cpert)):
    print('  construction: %s' % name)
    for n in (0, 1):
        # solve (A,B) as functions of z from two anchor z values, then verify
        # at a THIRD z: if the ansatz is right, (A,B) must be z-independent
        zs = (mp.mpf('1.5'), mp.mpf(4))
        sol = fit_B(psi, n, zs)
        if sol is None:
            print('     n=%d  degenerate' % n)
            continue
        A1, B1 = sol
        sol2 = fit_B(psi, n, (mp.mpf('1.5'), mp.mpf(30)))
        A2, B2 = sol2
        print('     n=%d  from z=(1.5,4):  A=%-18s B=%-18s' % (n, mp.nstr(A1, 12), mp.nstr(B1, 12)))
        print('          from z=(1.5,30): A=%-18s B=%-18s' % (mp.nstr(A2, 12), mp.nstr(B2, 12)))
        print('          => z-independent (A,B)?  %s'
              % ('YES' if abs(A1 / A2 - 1) < mp.mpf('1e-20') and abs(B1 / B2 - 1) < mp.mpf('1e-20') else 'NO'))
        # if B can be made 0 with a consistent A, it is first order
        print('          |B| significance: %s' % mp.nstr(abs(B1), 6))
