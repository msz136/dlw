"""
veto2.py -- final test: does ANY of the natural wave-function constructions give
a monodromy with a NONCONSTANT trace tr T(z)?

If tr T(z) is a nonconstant function of z for some construction, that is a genuine
spectral curve => strong integrability.  If it is constant for all of them, the
discrete direction carries no spectral data.

We use the second-order recurrence  psi_{n+1} + A_n(z) psi_n + B_n(z) psi_{n-1}=0
(valid for the c-perturbation), convert to a 2x2 transfer matrix
      [psi_{n+1}]   [ -A_n(z)  -B_n(z) ] [psi_n  ]
      [psi_n    ] = [   1         0    ] [psi_{n-1}]
and compute tr and det of the product over a period.
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
TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-3, 5)}


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


def AB(psi, n, z):
    """solve A,B from the two neighbouring relations at a single z using a
    second, independent equation: use n and n+1 to close the system."""
    # psi_{n+1} + A psi_n + B psi_{n-1} = 0
    # psi_{n+2} + A psi_{n+1} + B psi_n = 0
    p2 = psi(n + 2, z)
    p1 = psi(n + 1, z)
    p0 = psi(n, z)
    pm = psi(n - 1, z)
    det = p1 * p0 - p2 * pm
    if abs(det) < mp.mpf('1e-50'):
        return None
    A_ = (-p2 * p0 + p1 * p1) / det * (-1) if False else (p1 * p1 - p2 * p0) / det
    # solve properly:  [p1 p0; p2 p1][A;B] = [-p2_? ...]
    # equations:  p2 + A p1 + B p0 = 0 ; p1 + A p0 + B pm = 0
    # => A p1 + B p0 = -p2 ;  A p0 + B pm = -p1
    dd = p1 * pm - p0 * p0
    if abs(dd) < mp.mpf('1e-50'):
        return None
    A2 = (-p2 * pm + p1 * p0) / dd
    B2 = (p1 * (-p1) - p0 * (-p2)) / dd
    return A2, B2


print('=' * 92)
print('c-perturbation wave function: transfer matrix over a period, tr T(z)')
print('=' * 92)
for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30), mp.mpf(200)):
    prod = mp.eye(2)
    ok = True
    for n in (0, 1, 2):
        sol = AB(psi_cpert, n, z)
        if sol is None:
            ok = False
            break
        An, Bn = sol
        prod = mp.matrix([[-An, -Bn], [1, 0]]) * prod
    if ok:
        print('   z=%-8s  tr T = %-24s  det T = %s'
              % (mp.nstr(z, 6), mp.nstr(prod[0, 0] + prod[1, 1], 18),
                 mp.nstr(prod[0, 0] * prod[1, 1] - prod[0, 1] * prod[1, 0], 18)))
    else:
        print('   z=%-8s  system degenerate' % mp.nstr(z, 6))

print()
print('=' * 92)
print('A,B from the c-perturbation as functions of z (are they nonconstant?)')
print('=' * 92)
for n in (0, 1):
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30), mp.mpf(200)):
        sol = AB(psi_cpert, n, z)
        print('   n=%d z=%-8s  A=%-20s B=%s'
              % (n, mp.nstr(z, 6), mp.nstr(sol[0], 14), mp.nstr(sol[1], 14)))
