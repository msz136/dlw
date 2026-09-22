"""
link.py -- is the DLW tau function a 2DTL tau function?

If   (1/2 D_x D_y - 1) tau_n.tau_n + tau_{n+1} tau_{n-1} = 0     (2DTL bilinear)
holds, then the standard 2DTL theory applies verbatim:
    spectral problem   psi_{n+1} + u_n psi_n = z psi_n ,  u_n = sigma_n - 1
    flow               psi_y = v_n psi_{n-1}
    compatibility      u_{n,y} = v_{n+1} - v_n ,  v_{n,x} = v_n (u_n - u_{n-1})
and the monodromy over a period gives a genuine spectral curve.

We test the bilinear relation exactly (minor expansion + exact rates).
"""
import sys
import itertools
from math import comb
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 70
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7), mp.mpf(31) / 4]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2, mp.mpf(13) / 3]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100


def build(N, s=None):
    T = Tau(N, A, H, PS[:N], QS[:N])
    ss = T.a if s is None else s

    def rate(i, k):
        return (T.p[i] + T.q[k], T.q[k] ** 2 - T.p[i] ** 2,
                1 / (T.p[i] - ss) + 1 / (T.q[k] + ss))

    def dtau(n, ax=0, at=0, ay=0):
        B = T.Bmat(n, ss, X0, Y0, T0)
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
    return T, dtau


def D(dtau, n1, n2, ax=0, at=0, ay=0):
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            for q_ in range(ay + 1):
                co = (-1) ** (p_ + r_ + q_) * comb(ax, p_) * comb(at, r_) * comb(ay, q_)
                tot += co * dtau(n1, ax - p_, at - r_, ay - q_) * dtau(n2, p_, r_, q_)
    return tot


print('=' * 94)
print('2DTL bilinear:  (1/2 Dx Dy - 1) tau_n.tau_n + tau_{n+1} tau_{n-1} = 0')
print('=' * 94)
for N in (1, 2, 3, 4):
    try:
        T, dtau = build(N)
    except Exception as e:
        print('  N=%d skipped (%s)' % (N, e))
        continue
    for n in (-1, 0, 1):
        t0 = dtau(n)
        t1 = dtau(n + 1)
        tm = dtau(n - 1)
        lhs = mp.mpf(1) / 2 * D(dtau, n, n, ax=1, ay=1) - t0 * t0 + t1 * tm
        sc = abs(t0 * t0) + abs(t1 * tm) + abs(D(dtau, n, n, ax=1, ay=1))
        print('   N=%d n=%2d   rel.resid = %s' % (N, n, mp.nstr(abs(lhs) / sc, 4)))

print()
print('=' * 94)
print('also test the other natural bilinear form of the DLW tau:')
print('  Dx^2 tau.tau = -(Dt + 2a Dx) tau.tau   (i.e. (7) with f=g=tau)')
print('=' * 94)
for N in (1, 2, 3):
    T, dtau = build(N)
    for n in (0, 1):
        lhs = D(dtau, n, n, ax=2) + D(dtau, n, n, at=1) + 2 * T.a * D(dtau, n, n, ax=1)
        sc = abs(D(dtau, n, n, ax=2)) + abs(D(dtau, n, n, at=1)) + abs(D(dtau, n, n, ax=1))
        print('   N=%d n=%d   (7) with f=g=tau : rel.resid = %s'
              % (N, n, mp.nstr(abs(lhs) / sc, 4)))
