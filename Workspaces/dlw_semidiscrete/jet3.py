# -*- coding: utf-8 -*-
"""
jet3.py -- tau 的精确三变量 (x,t,y) 表示。

tau 是有限个指数单项式之和：  tau = sum_k C_k * exp(a_k x + b_k t + c_k y)
本模块用 (a,b,c) -> C 的字典精确表示，因此任意阶偏导都是精确的。

行列式展开：Gram 矩阵元
    m_ik = c_k delta_ik + E_ik
    E_ik = coef_ik * chi_ik^j * exp(S_ik x + R_ik t + T_ik y)
        coef_ik = (-(p_i-s)/(q_k+s))^n / (p_i+q_k)
        S = p_i+q_k ,  R = q_k^2-p_i^2 ,  T = 1/(p_i-s) + 1/(q_k+s)
        chi_ik = lam(p_i-mu) lam(q_k+mu)
所有单项式按 (S,R,T) 归类：同一 (S,R,T) 的系数相加。
"""
import mpmath as mp
from itertools import permutations

mp.mp.dps = 60

ZERO = (mp.mpf(0), mp.mpf(0), mp.mpf(0))


def add(d1, d2):
    out = dict(d1)
    for k, v in d2.items():
        nv = out.get(k, mp.mpf(0)) + v
        if nv == 0:
            out.pop(k, None)
        else:
            out[k] = nv
    return out


def scale(d, s):
    return dict((k, v * s) for k, v in d.items() if v * s != 0)


def mul(d1, d2):
    out = {}
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            out[k] = out.get(k, mp.mpf(0)) + v1 * v2
    return dict((k, v) for k, v in out.items() if v != 0)


def deriv(d, mx=0, mt=0, my=0):
    return dict((k, v * (k[0] ** mx) * (k[1] ** mt) * (k[2] ** my)) for k, v in d.items())


def ev(d, x0=mp.mpf(0), t0=mp.mpf(0), y0=mp.mpf(0)):
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


def tau3(N, a, p, q, h, n, s, mu, j):
    """返回 dict {(S,R,T): C}（系数 C 不含基点平移，求值时用 ev 传入基点）。"""
    dd = (h / 2) if h is not None else mp.mpf(0)

    def entry(i, k):
        P = p[i] - s
        Q = q[k] + s
        coef = (-P / Q) ** n / (p[i] + q[k])
        S = p[i] + q[k]
        R = q[k] ** 2 - p[i] ** 2
        T = 1 / P + 1 / Q
        if h is not None and j:
            pm = p[i] - mu
            qm = q[k] + mu
            coef = coef * ((((pm + dd) / (pm - dd)) * ((qm + dd) / (qm - dd))) ** j)
        out = {(S, R, T): coef}
        if i == k:
            out = add(out, {ZERO: mp.mpf(1)})
        return out

    total = {}
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for ii in range(N):
            for jj in range(ii + 1, N):
                if pl[ii] > pl[jj]:
                    sign = -sign
        term = {ZERO: mp.mpf(sign)}
        for i in range(N):
            term = mul(term, entry(i, perm[i]))
        total = add(total, term)
    return total


def Bs3(F, G, s, mx=2, mt=1, sx=1):
    """(D_x^2 + D_t + 2s D_x) F.G ，F,G 为 (S,R,T)->C 字典"""
    from math import comb

    def bil(dx, dt):
        tot = {}
        for pp in range(dx + 1):
            for rr in range(dt + 1):
                co = (-1) ** (pp + rr) * comb(dx, pp) * comb(dt, rr)
                tot = add(tot, scale(mul(deriv(F, dx - pp, dt - rr), deriv(G, pp, rr)), co))
        return tot

    return add(add(bil(2, 0), bil(0, 1)), scale(bil(1, 0), 2 * s))
