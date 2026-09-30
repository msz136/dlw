# -*- coding: utf-8 -*-
"""
nlverify.py -- DLW 半离散系统的**非线性层**验证（用精确解析导数的 tau）。

tau 是 N x N Gram 行列式
    tau = det(c_k delta_ik + E_ik),   E_ik = coef_ik * chi_ik^j * exp(S u + R v + T w)
    行/列因子的秩一结构使每个单项式由 (行重数 n, 列重数 m) 唯一决定。
这里直接对每个单项式做精确解析求导（不需要截断阶数）。

物理变量（d = h/2, mu = a）：
    F_j = tau_1(j; s=a-d, mu=a) ,  G_j = tau_0(j; s=a, mu=a)
    alpha_j = ln F_j , beta_j = ln G_j
    u_j = 2(alpha_j - beta_j)_x ,  w_j = 2(alpha_j + beta_j)_x
    v_j = (Psi_{j+1} - Psi_{j-1})_x / h ,  Psi_j = alpha_j + beta_j
"""
import mpmath as mp
from itertools import permutations
from math import comb, factorial

mp.mp.dps = 60


# --------------------------------------------------------------------------
class Mono:
    """tau 的单项式：c * exp(ux*S + ut*R + uy*T)，带有 (行,列) 重数键。"""

    __slots__ = ('c', 'S', 'R', 'T', 'key')

    def __init__(self, c, S, R, T, key):
        self.c, self.S, self.R, self.T, self.key = c, S, R, T, key


class Tau:
    """精确 tau 及其任意阶解析导数。"""

    def __init__(self, N, a, p, q, h, n, s, mu, j, x0, t0, y0,
                 ux=mp.mpf(0), ut=mp.mpf(0), uy=mp.mpf(0)):
        self.N, self.a, self.h = N, a, h
        self.p, self.q = list(p), list(q)
        self.n, self.s, self.mu, self.j = n, s, mu, j
        self.ux, self.ut, self.uy = ux, ut, uy
        self.x0, self.t0, self.y0 = x0, t0, y0
        d = (h / 2) if h is not None else mp.mpf(0)
        self.ent = {}
        for i in range(N):
            for k in range(N):
                P = self.p[i] - s
                Q = self.q[k] + s
                coef = (-P / Q) ** n / (self.p[i] + self.q[k])
                S = self.p[i] + self.q[k]
                R = self.q[k] ** 2 - self.p[i] ** 2
                T = 1 / P + 1 / Q
                if h is not None and j:
                    pm = self.p[i] - mu
                    qm = self.q[k] + mu
                    coef = coef * (((pm + d) / (pm - d)) * ((qm + d) / (qm - d))) ** j
                A = coef * mp.e ** (S * x0 + R * t0 + T * y0)
                self.ent[(i, k)] = (A, S, R, T)
        self._cache = {}

    # --- 单项式集合：{(行重数, 列重数): 系数} ---
    def _terms(self):
        """返回 {(nvec, mvec): coefficient}，系数已含 exp(Sx0+Rt0+Ty0) 的常量部分。"""
        if 'terms' in self._cache:
            return self._cache['terms']
        N = self.N
        # 每个 (i,k) 的单项式
        def entry(i, k):
            A, S, R, T = self.ent[(i, k)]
            nv = [0] * N
            mv = [0] * N
            nv[i] = 1
            mv[k] = 1
            out = {(tuple(nv), tuple(mv)): (A, S, R, T)}
            if i == k:
                z = (tuple([0] * N), tuple([0] * N))
                if z in out:
                    a, S0, R0, T0 = out[z]
                    out[z] = (a + 1, S0, R0, T0)
                else:
                    out[z] = (mp.mpf(1), mp.mpf(0), mp.mpf(0), mp.mpf(0))
            return out

        def mul(d1, d2):
            out = {}
            for k1, v1 in d1.items():
                for k2, v2 in d2.items():
                    kk = (tuple(x + y for x, y in zip(k1[0], k2[0])),
                          tuple(x + y for x, y in zip(k1[1], k2[1])))
                    c1, S1, R1, T1 = v1
                    c2, S2, R2, T2 = v2
                    c = c1 * c2
                    S, R, T = S1 + S2, R1 + R2, T1 + T2
                    if kk in out:
                        a, b, cc, dd = out[kk]
                        out[kk] = (a + c, S, R, T)
                    else:
                        out[kk] = (c, S, R, T)
            return dict((k, v) for k, v in out.items() if v[0] != 0)

        total = {}
        for perm in permutations(range(N)):
            sign = 1
            pl = list(perm)
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = {(tuple([0] * N), tuple([0] * N)): (mp.mpf(sign), mp.mpf(0), mp.mpf(0), mp.mpf(0))}
            for i in range(N):
                term = mul(term, entry(i, perm[i]))
            for k, v in term.items():
                if k in total:
                    a, S, R, T = total[k]
                    total[k] = (a + v[0], v[1], v[2], v[3])
                else:
                    total[k] = v
        total = dict((k, v) for k, v in total.items() if v[0] != 0)
        self._cache['terms'] = total
        return total

    # --- 导数 ---
    def d(self, mx=0, mt=0, my=0):
        """d_x^mx d_t^mt d_y^my tau（在位移增量处）"""
        tot = mp.mpf(0)
        for (nv, mv), (c, S, R, T) in self._terms().items():
            tot += c * (S ** mx) * (R ** mt) * (T ** my) \
                * mp.e ** (S * self.ux + R * self.ut + T * self.uy)
        return tot

    def ln(self, mx=0, mt=0, my=0):
        return mp.log(self.d(mx, mt, my))


# --------------------------------------------------------------------------
def bilin(F, G, mx=0, mt=0, my=0):
    """D_x^mx D_t^mt D_y^my F.G（精确，含 F,G 各自的位移增量）"""
    tot = mp.mpf(0)
    for pp in range(mx + 1):
        for rr in range(mt + 1):
            for qq in range(my + 1):
                co = (-1) ** (pp + rr + qq) * comb(mx, pp) * comb(mt, rr) * comb(my, qq)
                tot += co * F.d(mx - pp, mt - rr, my - qq) * G.d(pp, rr, qq)
    return tot


def Bs(F, G, s):
    return bilin(F, G, 2, 0, 0) + bilin(F, G, 0, 1, 0) + 2 * s * bilin(F, G, 1, 0, 0)


# ==========================================================================
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3


def make(N, a, p, q, h, n, s, mu, j, **kw):
    return Tau(N, a, p, q, h, n, s, mu, j, X0, T0, Y0, **kw)


def check(N, a, p, q, h, j0, label=''):
    d = h / 2

    def F(j, **kw):
        return make(N, a, p, q, h, 1, a - d, a, j, **kw)

    def G(j, **kw):
        return make(N, a, p, q, h, 0, a, a, j, **kw)

    print("=" * 92)
    print("N=%d a=%s p=%s q=%s h=%s j=%d  %s"
          % (N, mp.nstr(a, 8), [mp.nstr(v, 8) for v in p], [mp.nstr(v, 8) for v in q],
             mp.nstr(h, 6), j0, label))
    print("=" * 92)

    # --- 1. 双线性基线 ---
    e7 = Bs(F(j0), G(j0), a - d)
    e6 = Bs(F(j0), G(j0 + 1), a + d)
    f0 = abs(F(j0).d())
    print("  [1] bilinear   |(7)_h|=%.3e  |(6)_h|=%.3e   (|F|=%s)" %
          (float(abs(e7)), float(abs(e6)), mp.nstr(f0, 6)))

    # --- 2. 势函数形式 ---
    def th(j, mx=0, mt=0):
        return F(j).ln(mx, mt) - G(j).ln(mx, mt)

    def Ps(j, mx=0, mt=0):
        return F(j).ln(mx, mt) + G(j).ln(mx, mt)

    def Th(j, mx=0, mt=0):
        return F(j).ln(mx, mt) - G(j + 1).ln(mx, mt)

    def Ph(j, mx=0, mt=0):
        return F(j).ln(mx, mt) + G(j + 1).ln(mx, mt)

    rI = Ps(j0, 2, 0) + th(j0, 1, 0) ** 2 + th(j0, 0, 1) + 2 * (a - d) * th(j0, 1, 0)
    rII = Ph(j0, 2, 0) + Th(j0, 1, 0) ** 2 + Th(j0, 0, 1) + 2 * (a + d) * Th(j0, 1, 0)
    print("  [2] potential  |(I)|=%.3e  |(II)|=%.3e" % (float(abs(rI)), float(abs(rII))))

    # --- 3. 物理变量 ---
    def u(j, mx=0):
        return 2 * th(j, mx)

    def w(j, mx=0):
        return 2 * Ps(j, mx)

    def v(j):
        return (Ps(j + 1, 1) - Ps(j - 1, 1)) / h

    def uy(j):
        return (u(j + 1) - u(j - 1)) / h

    print("  [3] rel  v_j - w_{j+1} + h u_{j,x} = %.3e" % float(abs(v(j0) - w(j0 + 1) + h * u(j0, 1))))
    print("      rel  v_j - u_{j,y} - w_{j+1} + h u_{j,x} = %.3e"
          % float(abs(v(j0) - uy(j0) - w(j0 + 1) + h * u(j0, 1))))

    # --- 4. 闭合的 on-site 系统 ---
    A = 2 * th(j0, 0, 1) - (w(j0 + 1) - h * u(j0, 1) - 2 * a * u(j0))
    print("  [4] (A) u_{j,t} - [w_{j+1} - h u_{j,x} - 2a u_j] = %.3e" % float(abs(A)))


if __name__ == '__main__':
    for (N, a, p, q, h, j0) in [
        (1, mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4, 1),
        (1, mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)], mp.mpf(1) / 4, 1),
        (1, mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)], mp.mpf(1) / 4, 1),
    ]:
        check(N, a, p, q, h, j0)
