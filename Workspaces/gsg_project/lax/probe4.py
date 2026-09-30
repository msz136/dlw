"""
probe4.py -- decisive tests.

(A) Correct index orientation of the discrete wave function.
(B) Monodromy over a full period: is tr T(z) constant?  (=> no spectral curve)
(C) The CONTINUOUS bilinear equations: does tau_n solve the 2DTL-type system
    that would carry a spectral parameter in the x-direction?
"""
import sys
import itertools
from math import comb
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 70
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
N = 3
T = Tau(N, A, H, PS, QS)
U, V = list(T.p), list(T.q)
TAU = {n: T.tau(n, xv=X0, yv=Y0, tv=T0) for n in range(-4, 5)}


def tauhat(n, zinv):
    M = T.gram(n, T.a, X0, Y0, T0).copy()
    for i in range(N):
        for k in range(N):
            M[i, k] += zinv * U[i] * V[k]
    return det_exact(M)


print('=' * 92)
print('(A)  psi_{n+1}/psi_n  vs  (z+Q_n)/(z+Q_{n+1})')
print('=' * 92)
for n in (0, 1, 2):
    Qn = (tauhat(n, mp.mpf(10) ** -8) / TAU[n] - 1) * mp.mpf(10) ** 8
    Qn1 = (tauhat(n + 1, mp.mpf(10) ** -8) / TAU[n + 1] - 1) * mp.mpf(10) ** 8
    for z in (mp.mpf('1.5'), mp.mpf(4), mp.mpf(30)):
        r_emp = (tauhat(n + 1, 1 / z) / TAU[n + 1]) / (tauhat(n, 1 / z) / TAU[n])
        pred = (z + Qn) / (z + Qn1)
        print('   n=%d z=%-6s  psi_{n+1}/psi_n=%-20s  (z+Q_n)/(z+Q_{n+1})=%-20s rel=%s'
              % (n, mp.nstr(z, 4), mp.nstr(r_emp, 14), mp.nstr(pred, 14),
                 mp.nstr(abs(r_emp / pred - 1), 3)))

print()
print('=' * 92)
print('(B)  monodromy over a full period  T(z) = prod L_n(z),  L_n=(z+Q_n)/(z+Q_{n+1})')
print('=' * 92)
Q = {}
for n in range(-2, 4):
    Q[n] = (tauhat(n, mp.mpf(10) ** -8) / TAU[n] - 1) * mp.mpf(10) ** 8
print('   Q_n:', {k: mp.nstr(v, 10) for k, v in Q.items()})
print()
print('   Note L_n(z) = (z+Q_n)/(z+Q_{n+1}); if Q_{n+3}=Q_n (period 3) then')
print('   the product telescopes to 1 identically.  Check:')
for n in range(-1, 3):
    print('     Q_%d - Q_%d = %s' % (n, n + 3, mp.nstr(Q[n] - Q[n + 3], 6)))

print()
print('=' * 92)
print('(C)  CONTINUOUS bilinear relations for tau_n (parameter a)')
print('     test (i)  D_x D_y tau.tau = 2(tau^2 - tau_{n+1}tau_{n-1})')
print('     test (ii) D_x^2 tau.tau = -(D_t + 2a D_x) tau.tau   ... etc.')
print('=' * 92)


def rate(i, k, s=None):
    s = T.a if s is None else s
    return (T.p[i] + T.q[k], T.q[k] ** 2 - T.p[i] ** 2,
            1 / (T.p[i] - s) + 1 / (T.q[k] + s))


def dtau(n, ax=0, at=0, ay=0, s=None):
    B = T.Bmat(n, T.a if s is None else s, X0, Y0, T0)
    tot = mp.mpf(0)
    for r in range(N + 1):
        for S in itertools.combinations(range(N), r):
            sub = mp.matrix(r, r)
            for a2, i in enumerate(S):
                for b2, k in enumerate(S):
                    rr = rate(i, k, s)
                    sub[a2, b2] = B[i, k] * rr[0] ** ax * rr[1] ** at * rr[2] ** ay
            tot += det_exact(sub)
    return tot


def D(n1, n2, ax=0, at=0, ay=0):
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            for q_ in range(ay + 1):
                co = (-1) ** (p_ + r_ + q_) * comb(ax, p_) * comb(at, r_) * comb(ay, q_)
                tot += co * dtau(n1, ax - p_, at - r_, ay - q_) * dtau(n2, p_, r_, q_)
    return tot


for n in (-1, 0, 1):
    t0 = dtau(n); t1 = dtau(n + 1); tm = dtau(n - 1)
    lhs = D(n, n, ax=1, ay=1)
    rhs = 2 * (t0 * t0 - t1 * tm)
    sc = abs(lhs) + abs(rhs) + mp.mpf('1e-300')
    print('   n=%d   DxDy t.t - 2(t^2 - t_{n+1}t_{n-1})  rel = %s'
          % (n, mp.nstr(abs(lhs - rhs) / sc, 4)))
