# -*- coding: utf-8 -*-
"""
taujet.py -- DLW Gram tau 的 jet 引擎（对数域行/列规范化版）。

约定
    d = h/2,  lam(z) = (z+d)/(z-d)
    G_j = tau_0(j) ,   F_j = tau_1(j; s = a-d)
    矩阵元  m_ik = c_k delta_ik + (1/(p_i+q_k)) (-(p_i-s)/(q_k+s))^n
                   * [lam(p_i-a) lam(q_k+a)]^j * exp( (p_i+q_k) u + C_ik )
    u = x - x0,  C_ik = (p_i x0 - p_i^2 t0) + (q_k x0 + q_k^2 t0)
    （连续情形 C_ik 再加 dy (1/(p_i-a) + 1/(q_k+a))）

数值稳定化：**对数域的行/列规范化**
    令 L_ik := log|coef_ik| + C_ik ，并按
        m_ik  ->  m_ik * exp( -(r_i + c_k) ),   r_i := median-ish, c_k := ...
    需要 L_ik - (r_i+c_k) ∈ [-A, A]。行/列尺度存在 iff 差分矩阵
    L_ik - L_i0 - L_0k + L_00 有界；这里用不动点迭代求 (r,c)：
        r_i <- (1/2)( max_k(L_ik - c_k) + min_k(L_ik - c_k) )
        c_k <- (1/2)( max_i(L_ik - r_i) + min_i(L_ik - r_i) )
    收敛后矩阵元量级为 O(1)（典型 1e-6 ~ 1e6），再做 Leibniz 展开就不会
    损失有效位。行列式整体乘上常数 exp(-sum r - sum c)，对 (ln tau) 的导数无关。
"""

from itertools import permutations
import mpmath as mp

from jet import Jet


class Tau:
    def __init__(self, N, a, p, q, h=None):
        self.N = N
        self.a = mp.mpf(a)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.h = None if h is None else mp.mpf(h)
        self.uv = Jet.var()

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
        return coef, C, (p + q)

    # ------------------------------------------------------------------
    def _rowcol(self, L):
        """不动点求 (r_i, c_k) 使 L_ik - r_i - c_k 居中。"""
        N = self.N
        r = [mp.mpf(0)] * N
        c = [mp.mpf(0)] * N
        for _ in range(60):
            nr = [(max(L[i][k] - c[k] for k in range(N))
                   + min(L[i][k] - c[k] for k in range(N))) / 2 for i in range(N)]
            nc = [(max(L[i][k] - nr[i] for i in range(N))
                   + min(L[i][k] - nr[i] for i in range(N))) / 2 for k in range(N)]
            dr = max(abs(nr[i] - r[i]) for i in range(N))
            dc = max(abs(nc[k] - c[k]) for k in range(N))
            r, c = nr, nc
            if max(dr, dc) < mp.mpf('1e-30'):
                break
        return r, c

    # ------------------------------------------------------------------
    def tau(self, n, j, s, mu, x0, t0, dy=mp.mpf(0)):
        N = self.N
        coefs, wxs, L, sgn = {}, {}, [], []
        for i in range(N):
            row, srow = [], []
            for k in range(N):
                coef, C, wx = self._spec(n, j, s, i, k, x0, t0, dy)
                coefs[(i, k)] = coef
                wxs[(i, k)] = wx
                if coef == 0:
                    row.append(mp.mpf('-1e30'))
                    srow.append(1)
                else:
                    row.append(mp.log(abs(coef)) + C)
                    srow.append(1 if coef > 0 else -1)
            L.append(row)
            sgn.append(srow)
        # 对角项的常数 1 也纳入视野
        for i in range(N):
            L[i][i] = max(L[i][i], mp.mpf(0))
        r, c = self._rowcol(L)
        ent = {}
        for i in range(N):
            for k in range(N):
                sh = L[i][k] - r[i] - c[k]
                wx = wxs[(i, k)]
                jt = (Jet.const(wx) * self.uv).exp() * mp.e ** sh
                if sgn[i][k] < 0:
                    jt = -jt
                if i == k:
                    # 原始的 1 被缩放了 exp(-(r_i + c_k))
                    jt = jt + mp.e ** (-(r[i] + c[k]))
                ent[(i, k)] = jt
        tot = Jet.const(0)
        for perm in permutations(range(N)):
            sign = 1
            pl = list(perm)
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = Jet.const(sign)
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


def jetmax(jt):
    return max(abs(v) for v in jt.a)
