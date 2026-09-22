"""
verify2.py -- well-conditioned verification.

Use SMALL values of (x,y,t) so that all entries are O(1).  The tau function is
a sum of exponentials with vastly different rates; large sample points make the
sum catastrophically ill-conditioned.  Small points keep everything O(1) and
the identities then hold to full working precision.
"""
import sys
import random
from math import comb
from itertools import permutations

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from mpt import MP

mp.mp.dps = 120


def rand_data(N, rng):
    while True:
        a = mp.mpf(rng.randint(5, 40)) / rng.randint(2, 5)
        ps = [mp.mpf(rng.randint(1, 60)) / rng.randint(2, 5) for _ in range(N)]
        qs = [mp.mpf(rng.randint(1, 60)) / rng.randint(2, 5) for _ in range(N)]
        if len(set(ps)) < N or len(set(qs)) < N:
            continue
        if any(p + q == 0 for p in ps for q in qs):
            continue
        if any(p == a for p in ps) or any(q == -a for q in qs):
            continue
        if any(abs(p - a) < mp.mpf('0.3') for p in ps):
            continue
        if any(abs(q + a) < mp.mpf('0.3') for q in qs):
            continue
        return a, ps, qs


def btau(M, n1, j1, s1, n2, j2, s2, ax=0, at=0, ay=0):
    tot = mp.mpf(0)
    for p_ in range(ax + 1):
        for r_ in range(at + 1):
            for q_ in range(ay + 1):
                co = (-1) ** (p_ + r_ + q_) * comb(ax, p_) * comb(at, r_) * comb(ay, q_)
                A_ = M.dtau(n1, j1, s1, X, Y, T, {'x': ax - p_, 't': at - r_, 'y': ay - q_})
                B_ = M.dtau(n2, j2, s2, X, Y, T, {'x': p_, 't': r_, 'y': q_})
                tot += co * A_ * B_
    return tot


# small, well-conditioned sample point
X = mp.mpf(1) / 100
Y = mp.mpf(-1) / 100
T = mp.mpf(1) / 100
H = mp.mpf(1) / 3
d = H / 2

w1 = w2 = w3 = mp.mpf(0)
print('=' * 96)
print('T1 2DTL bilinear | T2 sigma_n-1 | T3 sigma_j-1   (dps=120, small point)')
print('=' * 96)
for N in (2, 3, 4, 5):
    for seed in (7, 19, 31):
        rng = random.Random(seed)
        A, PS, QS = rand_data(N, rng)
        M = MP(N, A, H, PS, QS)
        for j in (0, 1, 2):
            t0 = M.tau(0, j, xv=X, yv=Y, tv=T)
            t1 = M.tau(1, j, xv=X, yv=Y, tv=T)
            tm = M.tau(-1, j, xv=X, yv=Y, tv=T)
            txy = btau(M, 0, j, A, 0, j, A, ax=1, ay=1)
            tx = btau(M, 0, j, A, 0, j, A, ax=1)
            ty = btau(M, 0, j, A, 0, j, A, ay=1)
            res = mp.mpf(1) / 2 * (txy - tx * ty) - t0 * t0 + t1 * tm
            sc = abs(t0 * t0) + abs(t1 * tm) + abs(txy) + abs(tx * ty)
            r1 = abs(res) / sc
            r2 = abs(t1 * tm / t0 ** 2 - 1)
            sj = M.tau(0, j + 1, xv=X, yv=Y, tv=T) * M.tau(0, j - 1, xv=X, yv=Y, tv=T) / t0 ** 2
            r3 = abs(sj - 1)
            w1 = max(w1, r1); w2 = max(w2, r2); w3 = max(w3, r3)
            print('  N=%d seed=%2d j=%d  |2DTL|=%-10s |sig_n-1|=%-10s |sig_j-1|=%-10s'
                  % (N, seed, j, mp.nstr(r1, 3), mp.nstr(r2, 3), mp.nstr(r3, 3)))
print()
print('worst: 2DTL=%s  sigma_n=%s  sigma_j=%s' % (mp.nstr(w1, 4), mp.nstr(w2, 4), mp.nstr(w3, 4)))

print()
print('=' * 96)
print('T4  staggered pair (7)_h , (6)_h    (dps=120, small point)')
print('=' * 96)
for N in (2, 3, 4, 5):
    for seed in (7, 19):
        rng = random.Random(seed)
        A, PS, QS = rand_data(N, rng)
        M = MP(N, A, H, PS, QS)
        for j in (0, 1, 2):
            r7 = btau(M, 1, j, A - d, 0, j, A, ax=2) + btau(M, 1, j, A - d, 0, j, A, at=1) \
                + 2 * (A - d) * btau(M, 1, j, A - d, 0, j, A, ax=1)
            r6 = btau(M, 1, j, A - d, 0, j + 1, A, ax=2) + btau(M, 1, j, A - d, 0, j + 1, A, at=1) \
                + 2 * (A + d) * btau(M, 1, j, A - d, 0, j + 1, A, ax=1)
            Fv = M.tau(1, j, s=A - d, xv=X, yv=Y, tv=T)
            Gv = M.tau(0, j + 1, s=A, xv=X, yv=Y, tv=T)
            sc = abs(Fv * Gv)
            print('  N=%d seed=%2d j=%d   (7)_h=%-10s (6)_h=%-10s'
                  % (N, seed, j, mp.nstr(abs(r7) / sc, 3), mp.nstr(abs(r6) / sc, 3)))
