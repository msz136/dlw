# -*- coding: utf-8 -*-
"""
taujet2.py -- DLW Gram tau 的双变量 jet 引擎（正确版）。

    u = x - x0,  v = t - t0
    exp( (p_i+q_k) u + (q_k^2 - p_i^2) v )  <->  e^{C_ik} * exp( (p+q) u + (q^2-p^2) v )

数值稳定化：对数域的行/列规范化（只乘整行/整列的常数因子，
对 (ln tau) 的一切导数无影响）。
"""

from itertools import permutations
import mpmath as mp

from jet2 import J2, MX, MT


class Tau2:
    def __init__(self, N, a, p, q, h=None):
        self.N = N
        self.a = mp.mpf(a)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.h = None if h is None else mp.mpf(h)
        self.ux = J2.var_x()
        self.ut = J2.var_t()

    # ------------------------------------------------------------------
    def _spec(self, n, j, s, i, k, x0, t0, dy):
        p, q = self.p[i], self.q[k]
        C = (p * x0 - p ** 2 * t0) + (q * x0 + q ** 2 * t0)
        if self.h is None:
            C = C + dy * (1 / (p - self.a) + 1 / (q + self.a))
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        if j and self.h is not None:
            d = self.h / 2
            lp = (p - self.a + d) / (p - self.a - d)
            lq = (q + self.a + d) / (q + self.a - d)
            coef = coef * (lp * lq) ** j
        return coef, C, (p + q), (q * q - p * p)

    def _rowcol(self, L):
        N = self.N
        r = [mp.mpf(0)] * N
        c = [mp.mpf(0)] * N
        for _ in range(80):
            nr = [(max(L[i][k] - c[k] for k in range(N))
                   + min(L[i][k] - c[k] for k in range(N))) / 2 for i in range(N)]
            nc = [(max(L[i][k] - nr[i] for i in range(N))
                   + min(L[i][k] - nr[i] for i in range(N))) / 2 for k in range(N)]
            dr = max(abs(nr[i] - r[i]) for i in range(N))
            dc = max(abs(nc[k] - c[k]) for k in range(N))
            r, c = nr, nc
            if max(dr, dc) < mp.mpf('1e-40'):
                break
        return r, c

    # ------------------------------------------------------------------
    def tau(self, n, j, s, mu, x0, t0, dy=mp.mpf(0)):
        N = self.N
        L, sgn, wx, wt = [], [], {}, {}
        for i in range(N):
            row, srow = [], []
            for k in range(N):
                coef, C, w1, w2 = self._spec(n, j, s, i, k, x0, t0, dy)
                wx[(i, k)] = w1
                wt[(i, k)] = w2
                if coef == 0:
                    row.append(mp.mpf('-1e30'))
                    srow.append(1)
                else:
                    row.append(mp.log(abs(coef)) + C)
                    srow.append(1 if coef > 0 else -1)
            L.append(row)
            sgn.append(srow)
        for i in range(N):
            L[i][i] = max(L[i][i], mp.mpf(0))
        r, c = self._rowcol(L)
        # 重要：行/列因子必须整体化为**常数**因子，不能改变线性部分。
        #   m_ik -> m_ik * e^{-(r_i+c_k)}
        # 行列式因此乘上常数 e^{-sum r - sum c}，(ln tau) 的一切 x/t 导数不变。
        # （若额外扣掉与 (i,k) 有关的线性型，等价于给 tau 乘 e^{线性型}，
        #   而 e^{L} 不是双线性方程 B_s 的对称性，除非 L_t + 2s L_x = 0；
        #   一般不成立，会破坏 (7)_h=(6)_h=0 —— 这是本项目早前的一个陷阱。）
        # 剩下的常数平移 C：只影响 det 的整体常数，不影响任何导出量。
        C = max((L[i][k] - r[i] - c[k]) for i in range(N) for k in range(N))
        C = max(C, mp.mpf(0))
        ent = {}
        for i in range(N):
            for k in range(N):
                sh = L[i][k] - r[i] - c[k] - C
                lin = J2.const(wx[(i, k)]) * self.ux + J2.const(wt[(i, k)]) * self.ut
                jt = lin.exp() * mp.e ** sh
                if sgn[i][k] < 0:
                    jt = -jt
                if i == k:
                    jt = jt + mp.e ** (-(r[i] + c[k] + C))
                ent[(i, k)] = jt
        tot = J2.const(0)
        for perm in permutations(range(N)):
            sign = 1
            pl = list(perm)
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = J2.const(sign)
            for i in range(N):
                term = term * ent[(i, perm[i])]
            tot = tot + term
        return tot

    # ------------------------------------------------------------------
    def F(self, j, x0, t0, dy=mp.mpf(0)):
        d = (self.h / 2) if self.h is not None else mp.mpf(0)
        return self.tau(1, j, self.a - d, self.a, x0, t0, dy)

    def G(self, j, x0, t0, dy=mp.mpf(0)):
        return self.tau(0, j, self.a, self.a, x0, t0, dy)


def jmax(j):
    return j.maxabs()
