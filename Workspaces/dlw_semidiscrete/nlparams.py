# -*- coding: utf-8 -*-
"""
nlparams.py -- 自动搜索"正则参数点"：使交错 Gram tau 在被测格点邻域上严格为正。

需要： F_j > 0, G_j > 0 （j 在 {j0-2,...,j0+2} 与 {j0+1}）并且 F_j != G_j。
做法：随机（有理）采样参数，直接以高精度数值求值判断。
"""

import random
import mpmath as mp

mp.mp.dps = 40


def lam(z, h):
    return (z + h / 2) / (z - h / 2)


def eval_tau_num(N, p, q, a, h, n, j, s, mu, x0, t0):
    """数值 tau（与 verify_nl.Model 同构，但 mpmath 标量版）"""
    from itertools import permutations
    ent = {}
    for i in range(N):
        for k in range(N):
            coef = (-(p[i] - s) / (q[k] + s)) ** n / (p[i] + q[k])
            if j:
                coef = coef * (lam(p[i] - mu, h) * lam(q[k] + mu, h)) ** j
            rate = (p[i] * x0 - p[i] ** 2 * t0) + (q[k] * x0 + q[k] ** 2 * t0)
            e = coef * mp.e ** rate
            if i == k:
                e = e + 1
            ent[(i, k)] = e
    tot = mp.mpf(0)
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for ii in range(N):
            for jj in range(ii + 1, N):
                if pl[ii] > pl[jj]:
                    sign = -sign
        t = mp.mpf(sign)
        for i in range(N):
            t *= ent[(i, perm[i])]
        tot += t
    return tot


def Fnum(N, p, q, a, h, j, x0, t0):
    return eval_tau_num(N, p, q, a, h, 1, j, a - h / 2, a, x0, t0)


def Gnum(N, p, q, a, h, j, x0, t0):
    return eval_tau_num(N, p, q, a, h, 0, j, a, a, x0, t0)


def regular(N, p, q, a, h, j0, x0, t0, margin=mp.mpf('0.05')):
    """检查 j0-2..j0+2 上 F_j, G_j > margin 且 |F-G| > margin"""
    js = list(range(j0 - 2, j0 + 4))
    Fs, Gs = [], []
    for j in js:
        F = Fnum(N, p, q, a, h, j, x0, t0)
        G = Gnum(N, p, q, a, h, j, x0, t0)
        if F is None:
            return None
        Fs.append(F)
        Gs.append(G)
    if any(F <= margin for F in Fs) or any(G <= margin for G in Gs):
        return None
    if any(abs(F - G) <= margin for F, G in zip(Fs, Gs)):
        return None
    ratio = max(max(Fs) / min(Fs), max(Gs) / min(Gs))
    if ratio > mp.mpf('1e6'):
        return None
    return Fs, Gs


def search(N, h, j0, x0, t0, tries=40000, seed=12345):
    rng = random.Random(seed)
    best = None
    for _ in range(tries):
        a = mp.mpf(rng.randint(-9, 9)) / rng.randint(1, 4)
        p = [mp.mpf(rng.randint(1, 12)) / rng.randint(1, 5) for _ in range(N)]
        q = [mp.mpf(rng.randint(-12, -1)) / rng.randint(1, 5) for _ in range(N)]
        # 基本非退化条件
        if any(abs(p[i] - a) < mp.mpf('0.2') for i in range(N)):
            continue
        if any(abs(q[k] + a) < mp.mpf('0.2') for k in range(N)):
            continue
        if any(abs(p[i] + q[k]) < mp.mpf('0.2') for i in range(N) for k in range(N)):
            continue
        if any(abs(p[i] - p[j]) < mp.mpf('0.2') for i in range(N) for j in range(i + 1, N)):
            continue
        if any(abs(q[i] - q[j]) < mp.mpf('0.2') for i in range(N) for j in range(i + 1, N)):
            continue
        r = regular(N, p, q, a, h, j0, x0, t0)
        if r is None:
            continue
        Fs, Gs = r
        # 偏好 F/G 远离 1（u 不退化）且量级适中
        spread = min(abs(F - G) / max(abs(F), abs(G)) for F, G in zip(Fs, Gs))
        if best is None or spread > best[0]:
            best = (spread, a, list(p), list(q))
    return best


if __name__ == '__main__':
    x0 = mp.mpf(1) / 5
    t0 = mp.mpf(2) / 7
    for N in [1, 2, 3]:
        for h in [mp.mpf(1) / 4, mp.mpf(1) / 8]:
            for j0 in [0]:
                b = search(N, h, j0, x0, t0, tries=20000, seed=777 + 13 * N + int(100 * float(h)))
                if b is None:
                    print("N=%d h=%s : NOT FOUND" % (N, mp.nstr(h, 4)))
                else:
                    spread, a, p, q = b
                    print("N=%d h=%-5s j0=%d : a=%s  p=%s  q=%s   spread=%.4f"
                          % (N, mp.nstr(h, 4), j0, mp.nstr(a, 8),
                             [mp.nstr(v, 8) for v in p], [mp.nstr(v, 8) for v in q],
                             float(spread)))
                    Fs, Gs = regular(N, p, q, a, h, j0, x0, t0)
                    print("        F =", [mp.nstr(v, 8) for v in Fs])
                    print("        G =", [mp.nstr(v, 8) for v in Gs])
