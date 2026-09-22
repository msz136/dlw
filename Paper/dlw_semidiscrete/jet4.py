# -*- coding: utf-8 -*-
"""
jet4.py -- tau 的**精确有理**三变量表示（系数用 fractions.Fraction，零误差）。

与 jet3.py 的差别只有一个：所有系数是 Fraction 而不是 mpmath.mpf。
因此在基点处求值不再需要 exp 参与判零（见 ev_exact）。

tau = sum_k C_k * exp(a_k x + b_k t + c_k y),   C_k in Q
字典 (a_k,b_k,c_k) -> Fraction(C_k)，任意阶偏导精确。

Gram 矩阵元（同 jet3.py）：
    m_ik = c_k delta_ik + coef_ik * chi_ik^j * exp(S_ik x + R_ik t + T_ik y)
        coef_ik = (-(p_i-s)/(q_k+s))^n / (p_i+q_k)
        S = p_i+q_k ,  R = q_k^2-p_i^2 ,  T = 1/(p_i-s) + 1/(q_k+s)
        chi_ik = lam(p_i-mu) lam(q_k+mu) ,  lam(z) = (z+d)/(z-d) ,  d = h/2
"""
from fractions import Fraction as Fr
from itertools import permutations
from math import comb

ZERO = (Fr(0), Fr(0), Fr(0))


def F(x):
    """把 int / str / Fraction 统一成 Fraction。"""
    return x if isinstance(x, Fr) else Fr(x)


def add(d1, d2):
    out = dict(d1)
    for k, v in d2.items():
        nv = out.get(k, Fr(0)) + v
        if nv == 0:
            out.pop(k, None)
        else:
            out[k] = nv
    return out


def scale(d, s):
    s = F(s)
    if s == 0:
        return {}
    return dict((k, v * s) for k, v in d.items())


def mul(d1, d2):
    out = {}
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            out[k] = out.get(k, Fr(0)) + v1 * v2
    return dict((k, v) for k, v in out.items() if v != 0)


def deriv(d, mx=0, mt=0, my=0):
    if mx == mt == my == 0:
        return dict(d)
    return dict((k, v * (k[0] ** mx) * (k[1] ** mt) * (k[2] ** my))
                for k, v in d.items() if v != 0 and
                not ((mx and k[0] == 0) or (mt and k[1] == 0) or (my and k[2] == 0)))


def tau3(N, a, p, q, h, n, s, mu, j):
    """h 必须是 Fraction（精确）或 int。返回 {(S,R,T): Fraction}。"""
    a, s, mu = F(a), F(s), F(mu)
    p = [F(x) for x in p]
    q = [F(x) for x in q]
    h = F(h)
    dd = h / 2

    def entry(i, k):
        P = p[i] - s
        Q = q[k] + s
        coef = (-P / Q) ** n / (p[i] + q[k])
        S = p[i] + q[k]
        R = q[k] ** 2 - p[i] ** 2
        T = 1 / P + 1 / Q
        if j:
            pm = p[i] - mu
            qm = q[k] + mu
            coef *= (((pm + dd) / (pm - dd)) * ((qm + dd) / (qm - dd))) ** j
        out = {(S, R, T): coef}
        if i == k:
            out = add(out, {ZERO: Fr(1)})
        return out

    total = {}
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for ii in range(N):
            for jj in range(ii + 1, N):
                if pl[ii] > pl[jj]:
                    sign = -sign
        term = {ZERO: Fr(sign)}
        for i in range(N):
            term = mul(term, entry(i, perm[i]))
        total = add(total, term)
    return total


def bilin(Fd, Gd, mx=0, mt=0):
    """D_x^{mx} D_t^{mt} F . G （Hirota 双线性算子，精确）。"""
    tot = {}
    for pp in range(mx + 1):
        for rr in range(mt + 1):
            co = Fr((-1) ** (pp + rr) * comb(mx, pp) * comb(mt, rr))
            tot = add(tot, scale(mul(deriv(Fd, mx - pp, mt - rr), deriv(Gd, pp, rr)), co))
    return tot


def Bs3(Fd, Gd, s, ):
    """(D_x^2 + D_t + 2s D_x) F.G"""
    return add(add(bilin(Fd, Gd, 2, 0), bilin(Fd, Gd, 0, 1)),
               scale(bilin(Fd, Gd, 1, 0), 2 * F(s)))


def is_zero(d):
    """精确判零：字典为空 <=> 恒等于 0。"""
    return len(d) == 0


def show(d, limit=6):
    if not d:
        return '{0}  (空字典)'
    items = sorted(d.items(), key=lambda kv: -abs(kv[1]))[:limit]
    return '  '.join('%s*E%s' % (c, k) for k, c in items)
