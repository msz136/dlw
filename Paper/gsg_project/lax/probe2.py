"""
probe2.py -- is the (a+/-h/2) staggered system genuinely a *discrete integrable*
system, or just the continuum DLW with a shifted parameter?

Key test: the semidiscrete system should reduce to the continuum DLW as h -> 0,
and the SAME tau function should solve the continuum bilinear DLW for a RANGE of
a.  If tau(j; a-d) and tau(j; a+d) both solve the continuum bilinear system with
their respective a, then the scheme is "parameter staggering", not dynamics.

Test A: for fixed j, do the bilinear equations (6),(7) with parameter s hold for
        s = a-d and s = a+d, using F_j = tau_1(j;a-d), G_j = tau_0(j;a)?
Test B: does the h -> 0 limit give back the continuum solution?
Test C: conserved densities -- do the elementary symmetric coefficients of the
        tau expansion give densities whose x-derivative is a total y/t derivative?
"""
import sys
from math import comb
import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from tau4 import Tau, det_exact

mp.mp.dps = 80
H = mp.mpf(1) / 3
A = mp.mpf(17) / 5
PS = [mp.mpf(29) / 3, mp.mpf(12) / 5, mp.mpf(7)]
QS = [mp.mpf(40) / 3, mp.mpf(7) / 5, mp.mpf(9) / 2]
X0, Y0, T0 = mp.mpf(1) / 100, mp.mpf(-1) / 100, mp.mpf(1) / 100
N = 3
d = H / 2


def rates(s):
    """per-(i,k) exact rates (x,t,y) of the exponential factor"""
    T = Tau(N, A, H, PS, QS)
    return [[(T.p[i] + T.q[k], T.q[k] ** 2 - T.p[i] ** 2,
              1 / (T.p[i] - s) + 1 / (T.q[k] + s)) for k in range(N)] for i in range(N)]


def dtau(n, s, ax=0, at=0, ay=0):
    """exact derivative of tau_n(s) at (X0,Y0,T0) computed via the minor
    expansion with the exact per-entry rates"""
    T = Tau(N, A, H, PS, QS)
    B = T.Bmat(n, s, X0, Y0, T0)
    R = rates(s)
    tot = mp.mpf(0)
    import itertools
    for r in range(N + 1):
        for S in itertools.combinations(range(N), r):
            sub = mp.matrix(r, r)
            for a2, i in enumerate(S):
                for b2, k in enumerate(S):
                    w = R[i][k][0] ** ax * R[i][k][1] ** at * R[i][k][2] ** ay
                    sub[a2, b2] = B[i, k] * w
            tot += det_exact(sub)
    return tot


def bilin(n1, s1, n2, s2, ax=0, at=0, ay=0):
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            for q_ in range(ay + 1):
                co = (-1) ** (p_ + r_ + q_) * comb(ax, p_) * comb(at, r_) * comb(ay, q_)
                tot += co * dtau(n1, s1, ax - p_, at - r_, ay - q_) * dtau(n2, s2, p_, r_, q_)
    return tot


print('=' * 92)
print('A.  does (7) hold in the staggered form?')
print('    (7)_s : [D_x^2 + D_t + 2s D_x] tau_1(s1) . tau_0(s2) = 0')
print('=' * 92)
for (s1, s2, tag) in [(A, A, 'both a'), (A - d, A, 'F:a-d / G:a'),
                      (A, A + d, 'F:a / G:a+d'), (A - d, A + d, 'F:a-d / G:a+d')]:
    r7 = bilin(1, s1, 0, s2, ax=2) + bilin(1, s1, 0, s2, at=1) \
        + 2 * (A - d) * bilin(1, s1, 0, s2, ax=1)
    r7b = bilin(1, s1, 0, s2, ax=2) + bilin(1, s1, 0, s2, at=1) \
        + 2 * (A + d) * bilin(1, s1, 0, s2, ax=1)
    sc = abs(dtau(1, s1) * dtau(0, s2))
    print('   %-18s  |B_{a-d}|=%s   |B_{a+d}|=%s'
          % (tag, mp.nstr(abs(r7) / sc, 4), mp.nstr(abs(r7b) / sc, 4)))

print()
print('=' * 92)
print('B.  h-dependence of the field u = 2 d_x ln(F/G) at a generic point')
print('=' * 92)
for hh in (mp.mpf(1) / 3, mp.mpf(1) / 10, mp.mpf(1) / 100, mp.mpf(1) / 1000):
    dd = hh / 2
    T = Tau(N, A, hh, PS, QS)
    F = T.tau(1, s=A - dd, xv=X0, yv=Y0, tv=T0)
    G = T.tau(0, s=A, xv=X0, yv=Y0, tv=T0)
    print('   h=%-10s  tau_1(a-d)=%-22s tau_0(a)=%-22s'
          % (mp.nstr(hh, 6), mp.nstr(F, 16), mp.nstr(G, 16)))
