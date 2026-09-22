# -*- coding: utf-8 -*-
"""
nlstep1.py --  DLW 半离散系统：从双线性层 (star) 反变换到非线性势变量层的第一步。

目标（本文件只做诊断，不做结论）：
  1. 用交错 Gram tau 造出精确的 F_j, G_j（任意 N，任意格点 j）。
  2. 精确检验势变量形式 (N1)(N2)：
        (N1):  Psi_{j,xx} + theta_{j,x}^2 + theta_{j,t} + 2(a-d) theta_{j,x} = 0
        (N2):  Phi_{j,xx} + Theta_{j,x}^2 + Theta_{j,t} + 2(a+d) Theta_{j,x} = 0
     其中 theta=ln(F/G), Psi=ln(FG), Theta=ln(F/G_{j+1}), Phi=ln(F G_{j+1})。
  3. 诊断候选物理变量
        u_j := 2 (ln F_j/G_j)_x
     与各种 v_j 候选（格点差分）的连续极限阶数。

一切用精确有理运算（sympy 在有理点上求值），零判定是精确的。
"""

import itertools
import sympy as sp

# --------------------------------------------------------------------------
# tau 函数：交错 Gram 行列式
# --------------------------------------------------------------------------
# 连续/格点通用。我们固定一组"一般位置"的有理参数，用 sympy 求值。
#
#   m^(n)_{ik} = c_k delta_{ik} + (1/(p_i+q_k)) (-(p_i-s)/(q_k+s))^n
#                * [lam(p_i-a) lam(q_k+a)]^j * exp(xi_i + eta_k)
#   xi_i  = p_i x - p_i^2 t ,  eta_k = q_k x + q_k^2 t      (已去掉 y 部分)
#   G_j   = tau_0(j)                  (= det m^(0))
#   F_j   = tau_1(j; s=a-d)           (交错)
#   lam(z) = (z+d)/(z-d),  d = h/2
# --------------------------------------------------------------------------


class DLW:
    def __init__(self, N, vals, h, a):
        """
        vals : dict with keys 'p1..pN','q1..qN' -> sympy numbers
        h, a : sympy numbers
        """
        self.N = N
        self.h = sp.nsimplify(h)
        self.d = self.h / 2
        self.a = sp.nsimplify(a)
        self.p = [sp.nsimplify(vals['p%d' % (i + 1)]) for i in range(N)]
        self.q = [sp.nsimplify(vals['q%d' % (k + 1)]) for k in range(N)]
        self.c = [sp.Integer(1)] * N
        self.x, self.t = sp.symbols('x t', real=True)
        self._cache = {}

    def lam(self, z):
        return (z + self.d) / (z - self.d)

    def entry(self, n, i, k, j, s):
        p, q, a = self.p[i], self.q[k], self.a
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        if j:
            coef = coef * (self.lam(p - a) * self.lam(q + a)) ** j
        expo = (p * self.x - p ** 2 * self.t) + (q * self.x + q ** 2 * self.t)
        m = coef * sp.exp(expo)
        if i == k:
            m = m + self.c[k]
        return sp.expand(m)

    def tau(self, n, j, s):
        N = self.N
        tot = 0
        for perm in itertools.permutations(range(N)):
            sign = sp.Integer(1)
            pl = list(perm)
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = sign
            for i in range(N):
                term = term * self.entry(n, i, perm[i], j, s)
            tot = tot + term
        return sp.expand(tot)

    def F(self, j):
        return self.tau(1, j, self.a - self.d)

    def G(self, j):
        return self.tau(0, j, self.a)

    # ------------------------------------------------------------------ 诊断
    def check_N1N2(self, j):
        """精确检验 (N1) 与 (N2) 在格点 j 上。"""
        F, G = self.F(j), self.G(j)
        G1 = self.G(j + 1)
        th = sp.log(F / G)
        Ps = sp.log(F * G)
        Th = sp.log(F / G1)
        Ph = sp.log(F * G1)
        R1 = sp.diff(Ps, self.x, 2) + sp.diff(th, self.x) ** 2 \
             + sp.diff(th, self.t) + 2 * (self.a - self.d) * sp.diff(th, self.x)
        R2 = sp.diff(Ph, self.x, 2) + sp.diff(Th, self.x) ** 2 \
             + sp.diff(Th, self.t) + 2 * (self.a + self.d) * sp.diff(Th, self.x)
        return sp.simplify(R1), sp.simplify(R2)

    # 物理变量
    def u(self, j):
        return 2 * sp.diff(sp.log(self.F(j) / self.G(j)), self.x)

    def v_diff(self, j):
        """v_j = (1/h) d_x [ ln(F_j G_j) - ln(F_{j-1} G_{j-1}) ]"""
        Pj = sp.log(self.F(j) * self.G(j))
        Pjm = sp.log(self.F(j - 1) * self.G(j - 1))
        return sp.diff(Pj - Pjm, self.x) / self.h

    def v_mid(self, j):
        """v_j = (1/(2h)) d_x [ ln(F_{j+1}G_{j+1}) - ln(F_{j-1}G_{j-1}) ]"""
        Pp = sp.log(self.F(j + 1) * self.G(j + 1))
        Pm = sp.log(self.F(j - 1) * self.G(j - 1))
        return sp.diff(Pp - Pm, self.x) / (2 * self.h)

    def v_fwd(self, j):
        """v_j = (1/h) d_x [ ln(F_{j+1}G_{j+1}) - ln(F_j G_j) ]"""
        Pp = sp.log(self.F(j + 1) * self.G(j + 1))
        Pj = sp.log(self.F(j) * self.G(j))
        return sp.diff(Pp - Pj, self.x) / self.h

    # 连续参照
    def cont_u(self, y):
        """连续 u = 2(ln f/g)_x ，f=tau_1(s=a), g=tau_0, y 连续。"""
        # 连续 tau：把格点相位换成 y*(1/(p-a)+1/(q+a))
        raise NotImplementedError


# --------------------------------------------------------------------------
# 连续 tau（用于连续极限对照）
# --------------------------------------------------------------------------
class DLWcont(DLW):
    def entry(self, n, i, k, y, s, base_a):
        p, q = self.p[i], self.q[k]
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        expo = (p * self.x - p ** 2 * self.t) + (q * self.x + q ** 2 * self.t) \
               + y * (1 / (p - base_a) + 1 / (q + base_a))
        m = coef * sp.exp(expo)
        if i == k:
            m = m + self.c[k]
        return m

    def tau_c(self, n, y, s, base_a):
        N = self.N
        tot = 0
        for perm in itertools.permutations(range(N)):
            sign = sp.Integer(1)
            pl = list(perm)
            for ii in range(N):
                for jj in range(ii + 1, N):
                    if pl[ii] > pl[jj]:
                        sign = -sign
            term = sign
            for i in range(N):
                term = term * self.entry(n, i, perm[i], y, s, base_a)
            tot = tot + term
        return sp.expand(tot)

    def f_cont(self, y):
        return self.tau_c(1, y, self.a, self.a)

    def g_cont(self, y):
        return self.tau_c(0, y, self.a, self.a)

    def u_cont(self, y):
        return 2 * sp.diff(sp.log(self.f_cont(y) / self.g_cont(y)), self.x)

    def v_cont(self, y):
        """v = 2 (ln f g)_{xy}"""
        return 2 * sp.diff(sp.log(self.f_cont(y) * self.g_cont(y)), self.x, y)


def main():
    print("=" * 78)
    print("DLW 半离散：势变量层 (N1)(N2) 的精确检验")
    print("=" * 78)

    N = 1
    vals = {'p1': sp.Rational(5, 3), 'q1': sp.Rational(7, 4)}
    a = sp.Rational(3, 2)

    for h in [sp.Rational(1, 4), sp.Rational(1, 8)]:
        M = DLW(N, vals, h, a)
        print("\nh = %s,  a = %s,  p1 = %s, q1 = %s"
              % (h, a, vals['p1'], vals['q1']))
        for j in [0, 1, 2]:
            x0 = sp.Rational(1, 5)
            t0 = sp.Rational(2, 7)
            R1, R2 = M.check_N1N2(j)
            e1 = sp.simplify(R1.subs({M.x: x0, M.t: t0}))
            e2 = sp.simplify(R2.subs({M.x: x0, M.t: t0}))
            print("  j=%d :  (N1) resid = %s   (N2) resid = %s"
                  % (j, e1, e2))

    # --- 连续极限阶数扫描：v 的各候选定义 vs 2(ln fg)_{xy}
    print("\n" + "=" * 78)
    print("连续极限阶数扫描：  v_j 候选  vs  2(ln fg)_{xy}")
    print("=" * 78)
    for j in [0, 1]:
        print("\n 格点 j = %d" % j)
        for name, fn in [('v_fwd', 'v_fwd'), ('v_diff', 'v_diff'), ('v_mid', 'v_mid')]:
            errs = []
            for hh in [sp.Rational(1, 4), sp.Rational(1, 8),
                       sp.Rational(1, 16), sp.Rational(1, 32)]:
                M = DLWcont(N, vals, hh, a)
                x0, t0 = sp.Rational(1, 5), sp.Rational(2, 7)
                y0 = (j + sp.Rational(1, 2)) * hh
                vj = getattr(M, fn)(j).subs({M.x: x0, M.t: t0})
                vc = M.v_cont(y0).subs({M.x: x0, M.t: t0})
                errs.append(sp.nsimplify(sp.simplify(vj - vc)))
            print("   %-8s :" % name, ["%.6e" % sp.N(e, 8) for e in errs])
            for k in range(1, len(errs)):
                if errs[k - 1] != 0:
                    r = sp.nsimplify(sp.simplify(errs[k - 1] / errs[k]))
                    print("              比值 = %.6f" % sp.N(r, 8))


if __name__ == '__main__':
    main()
