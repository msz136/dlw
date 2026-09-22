"""
verify_final.py -- robust, well-conditioned verification at 200 digits.

Tests, for N = 2..5 and several random parameter sets / sample points:
  T1  2DTL bilinear:  (1/2 Dx Dy - 1) tau_n.tau_n + tau_{n+1} tau_{n-1} = 0
  T2  sigma_n = tau_{n+1} tau_{n-1}/tau_n^2 = 1     (log tau_n affine in n)
  T3  sigma_j = tau(j+1) tau(j-1)/tau_j^2 = 1
  T4  the semidiscrete staggered bilinear pair (7)_h , (6)_h
"""
import sys
import random
from math import comb
from itertools import permutations

import mpmath as mp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')
from mpt import MP

mp.mp.dps = 200


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
        if any(abs(p - a) < mp.mpf('0.2') for p in ps):
            continue
        if any(abs(q + a) < mp.mpf('0.2') for q in qs):
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


X = mp.mpf(1) / 3
Y = mp.mpf(-2) / 5
T = mp.mpf(3) / 7
H = mp.mpf(1) / 3
d = H / 2

print('=' * 96)
print('T1/T2/T3   (200 digits; threshold 1e-100)')
print('=' * 96)
worst = {}
for N in (2, 3, 4, 5):
    for seed in (7, 19, 31):
        rng = random.Random(seed)
        A, PS, QS = rand_data(N, rng)
        M = MP(N, A, H, PS, QS)
        for j in (0, 1):
            # T1
            t0 = M.tau(0, j, xv=X, yv=Y, tv=T)
            t1 = M.tau(1, j, xv=X, yv=Y, tv=T)
            tm = M.tau(-1, j, xv=X, yv=Y, tv=T)
            txy = btau(M, 0, j, A, 0, j, A, ax=1, ay=1)
            tx = btau(M, 0, j, A, 0, j, A, ax=1)
            ty = btau(M, 0, j, A, 0, j, A, ay=1)
            res = mp.mpf(1) / 2 * (txy - tx * ty) - t0 * t0 + t1 * tm
            sc = abs(t0 * t0) + abs(t1 * tm) + abs(txy) + abs(tx * ty)
            rel1 = abs(res) / sc
            rel2 = abs(t1 * tm / t0 ** 2 - 1)
            sj = M.tau(0, 1, xv=X, yv=Y, tv=T) * M.tau(0, -1, xv=X, yv=Y, tv=T) / t0 ** 2
            rel3 = abs(sj - 1)
            for key, v in (('T1', rel1), ('T2', rel2), ('T3', rel3)):
                worst[key] = max(worst.get(key, mp.mpf(0)), v)
            print('  N=%d seed=%2d j=%d  |2DTL|=%s  |sigma_n-1|=%s  |sigma_j-1|=%s'
                  % (N, seed, j, mp.nstr(rel1, 4), mp.nstr(rel2, 4), mp.nstr(rel3, 4)))
print()
print('worst residuals:', {k: mp.nstr(v, 5) for k, v in worst.items()})

print()
print('=' * 96)
print('T4  the staggered semidiscrete pair  (7)_h , (6)_h')
print('=' * 96)
for N in (2, 3, 4):
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
            print('  N=%d seed=%2d j=%d   (7)_h=%s  (6)_h=%s'
                  % (N, seed, j, mp.nstr(abs(r7) / sc, 4), mp.nstr(abs(r6) / sc, 4)))
