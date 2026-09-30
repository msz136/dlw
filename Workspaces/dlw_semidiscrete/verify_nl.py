# -*- coding: utf-8 -*-
"""
verify_nl.py --  DLW 半离散非线性层的高精度验证。

用 jet（截断泰勒）算术在 (x,t) 展开。对 DLW 的 tau 有热方程 tau_{xx} = tau_t
（逐元素成立：xi_i 的 x 速率 p_i、t 速率 -p_i^2；eta_k 的 x 速率 q_k、t 速率 +q_k^2），
故 d/dt = d_x^2。脚本用 (ln F)_t 与 (ln F)_{xx} 的一致性审计这一点。

"零"判定用 jet 系数的最大绝对值（相对量级另附）；"阶数"用 h -> h/2 的比值
（16 = h^4，4 = h^2）。
"""

from itertools import permutations
import mpmath as mp

from jet import Jet

mp.mp.dps = 60

A = mp.mpf(3) / 2
P = [mp.mpf(5) / 3, mp.mpf(3) / 2]
Q = [mp.mpf(7) / 4, mp.mpf(9) / 5]
X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7


def lam(z, h):
    d = h / 2
    return (z + d) / (z - d)


def jetmax(jt):
    m = max(abs(v) for v in jt.a)
    return m


def jet0(jt):
    return abs(jt.a[0])


class Model:
    def __init__(self, N, h):
        self.N = N
        self.h = mp.mpf(h)
        self.a = A
        self.p = P[:N]
        self.q = Q[:N]
        self.uv = Jet.var()
        self._c = {}

    def entry(self, n, i, k, j, s, mu):
        p, q = self.p[i], self.q[k]
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        if j:
            coef = coef * (lam(p - mu, self.h) * lam(q + mu, self.h)) ** j
        rate = (p * X0 - p ** 2 * T0) + (q * X0 + q ** 2 * T0)
        jt = coef * mp.e ** rate * (Jet.const(p + q) * self.uv).exp()
        if i == k:
            jt = jt + 1
        return jt

    def tau(self, n, j, s, mu):
        key = (n, j, s, mu)
        if key in self._c:
            return self._c[key]
        N = self.N
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
                term = term * self.entry(n, i, perm[i], j, s, mu)
            tot = tot + term
        self._c[key] = tot
        return tot

    def F(self, j):
        return self.tau(1, j, self.a - self.h / 2, self.a)

    def G(self, j):
        return self.tau(0, j, self.a, self.a)

    def alpha(self, j):
        return self.F(j).log()

    def beta(self, j):
        return self.G(j).log()

    def theta(self, j):
        return self.alpha(j) - self.beta(j)

    def Psi(self, j):
        return self.alpha(j) + self.beta(j)

    def ThetaX(self, j):
        return self.alpha(j) - self.beta(j + 1)

    def PhiX(self, j):
        return self.alpha(j) + self.beta(j + 1)

    def u(self, j):
        return 2 * self.theta(j).dx()

    def w(self, j):
        return 2 * self.Psi(j).dx()

    def v(self, j):
        return (self.Psi(j + 1) - self.Psi(j - 1)).dx() / self.h

    def N1(self, j):
        th, Ps = self.theta(j), self.Psi(j)
        return Ps.dxn(2) + th.dx() ** 2 + th.dt() + 2 * (self.a - self.h / 2) * th.dx()

    def N2(self, j):
        Th, Ph = self.ThetaX(j), self.PhiX(j)
        return Ph.dxn(2) + Th.dx() ** 2 + Th.dt() + 2 * (self.a + self.h / 2) * Th.dx()

    def bEplus(self, j):
        F, G = self.F(j), self.G(j)
        s = self.a - self.h / 2
        return F.dxn(2) * G - 2 * F.dx() * G.dx() + F * G.dxn(2) \
            + (F.dt() * G - F * G.dt()) + 2 * s * (F.dx() * G - F * G.dx())

    def bEminus(self, j):
        F, G = self.F(j), self.G(j + 1)
        s = self.a + self.h / 2
        return F.dxn(2) * G - 2 * F.dx() * G.dx() + F * G.dxn(2) \
            + (F.dt() * G - F * G.dt()) + 2 * s * (F.dx() * G - F * G.dx())


class ContModel(Model):
    def entry(self, n, i, k, y, s):
        p, q = self.p[i], self.q[k]
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        rate = (p * X0 - p ** 2 * T0) + (q * X0 + q ** 2 * T0) \
            + y * (1 / (p - self.a) + 1 / (q + self.a))
        jt = coef * mp.e ** rate * (Jet.const(p + q) * self.uv).exp()
        if i == k:
            jt = jt + 1
        return jt

    def tau_c(self, n, y, s):
        N = self.N
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
                term = term * self.entry(n, i, perm[i], y, s)
            tot = tot + term
        return tot

    def Fc(self, y):
        return self.tau_c(1, y, self.a)

    def Gc(self, y):
        return self.tau_c(0, y, self.a)

    def uc(self, y):
        return 2 * (self.Fc(y).log() - self.Gc(y).log()).dx()

    def vc(self, y, eps=None):
        """v = 2 (ln f g)_{xy} : 对 y 用高精度中心差分（对 jet 逐系数作用）。
        因为 (ln fg)_{xy} 是对 y 的解析函数，中心差分误差 O(eps^2)，
        取 eps = 1e-15 时误差 ~1e-30，足够区分 O(h^2)。"""
        if eps is None:
            eps = mp.mpf('1e-14')
        f = lambda yy: (self.Fc(yy).log() + self.Gc(yy).log())
        jp, jm = f(y + eps), f(y - eps)
        dv = (jp - jm) * (1 / (2 * eps))
        return 2 * dv.dx()


# --------------------------------------------------------------------------
def show(name, vals, ratios=True):
    print("  %-40s" % name + "".join(" %11.4e" % float(v) for v in vals))
    if ratios and len(vals) > 1:
        rr = []
        for k in range(1, len(vals)):
            rr.append(float(vals[k - 1] / vals[k]) if vals[k] != 0 else float('inf'))
        print("  %-40s" % "" + "".join(" %11.3f" % r for r in rr) + "   <- ratios")


def v_of(M, j):
    return (M.Psi(j + 1) - M.Psi(j - 1)).dx() / M.h


def uy_of(M, j):
    return (M.u(j + 1) - M.u(j - 1)) / M.h


def sumop(M, j, f):
    return (f(M, j + 1) + 2 * f(M, j) + f(M, j - 1)) / 4


def Rp_w(M, j):
    return M.N2(j).dx() + M.N1(j).dx()


def main():
    hs = [mp.mpf(1) / 4, mp.mpf(1) / 8, mp.mpf(1) / 16]
    print("x0=%s t0=%s a=%s" % (mp.nstr(X0, 6), mp.nstr(T0, 6), mp.nstr(A, 6)))
    for N in [1, 2]:
        print("\n" + "=" * 92)
        print("N = %d   p = %s   q = %s"
              % (N, [mp.nstr(v, 6) for v in P[:N]], [mp.nstr(v, 6) for v in Q[:N]]))
        print("=" * 92)

        print("\n[A] 热方程审计  (ln F_j)_t - (ln F_j)_xx  （应为 0）")
        for h in hs[:1]:
            M = Model(N, h)
            for j in [0, 1]:
                e = M.alpha(j).dt() - M.alpha(j).dxn(2)
                print("   h=%s j=%d : jetmax = %.3e" % (mp.nstr(h, 4), j, float(jetmax(e))))

        print("\n[B] 基线残差（应精确为 0）")
        for j in [1]:
            for h in hs[:1]:
                M = Model(N, h)
                print("   h=%-6s j=%d : (7)_h=%.2e  (6)_h=%.2e  (N1)=%.2e  (N2)=%.2e"
                      % (mp.nstr(h, 4), j, float(jetmax(M.bEplus(j))),
                         float(jetmax(M.bEminus(j))), float(jetmax(M.N1(j))),
                         float(jetmax(M.N2(j)))))

        print("\n[C] 精确恒等式  u_t - [v - w + h*sum_j[u]*R'_w]  (应精确为 0)")
        for j in [1]:
            vals = []
            for h in hs:
                M = Model(N, h)
                wj = M.w(j)
                e = M.u(j).dt() - (v_of(M, j) - wj
                                   + M.h * sumop(M, j, lambda M, k: M.u(k)) * Rp_w(M, j))
                vals.append(jetmax(e))
            show("residual j=%d" % j, vals, ratios=False)

        print("\n[D] 连续化  w_j - (v_j - u_{j,y})   期望 O(h^2)")
        for j in [1]:
            vals = []
            for h in hs:
                M = Model(N, h)
                e = M.w(j) - (v_of(M, j) - uy_of(M, j))
                vals.append(jetmax(e))
            show("w-(v-u_y) j=%d" % j, vals)

        print("\n[E] 闭合系统残差 (A)  u_t - [v - w_disc + d(u-w_disc) + 2d u_x]")
        for j in [1]:
            vals = []
            for h in hs:
                M = Model(N, h)
                wd = v_of(M, j) - uy_of(M, j)
                e = M.u(j).dt() - (v_of(M, j) - wd + M.h / 2 * (M.u(j) - wd)
                                   + M.h * M.u(j).dx())
                vals.append(jetmax(e))
            show("(A) j=%d" % j, vals)

        print("\n[F] 闭合系统残差 (B)  w_disc,t + sum_j[u] R'_w")
        for j in [1]:
            vals = []
            for h in hs:
                M = Model(N, h)
                wd = v_of(M, j) - uy_of(M, j)
                e = wd.dt() + sumop(M, j, lambda M, k: M.u(k)) * Rp_w(M, j)
                vals.append(jetmax(e))
            show("(B) j=%d" % j, vals)

        print("\n[G] 连续极限  |u_j - u_cont(Y)| ,  |v_j - v_cont(Y)| ,  Y=(j+1/2)h")
        for j in [1]:
            uv, vv = [], []
            for h in hs:
                M = Model(N, h)
                MC = ContModel(N, h)
                Y = (mp.mpf(j) + mp.mpf(1) / 2) * h
                uv.append(jetmax(M.u(j) - MC.uc(Y)))
                vv.append(jetmax(v_of(M, j) - MC.vc(Y)))
            show("|u_j-u_cont| j=%d" % j, uv)
            show("|v_j-v_cont| j=%d" % j, vv)

        print("\n[H] 连续 DLW 方程在 u_cont, v_cont 上的残差（应精确为 0）")
        for j in [1]:
            vals1, vals2 = [], []
            for h in hs:
                MC = ContModel(N, h)
                Y = (mp.mpf(j) + mp.mpf(1) / 2) * h
                yy = mp.mpf(Y)
                uc, vc = MC.uc(yy), MC.vc(yy)
                # u_t + v_x + u u_y + 2a u_y : 用解析 d/dY（对 jet 的 y 差分）
                eps = mp.mpf('1e-14')
                def uc_at(zz):
                    return MC.uc(zz)
                def vc_at(zz):
                    return MC.vc(zz)
                dY = lambda f: (f(Y + eps) - f(Y - eps)) * (1 / (2 * eps))
                e1 = uc.dt() + dY(vc_at) + uc * dY(uc_at) + 2 * MC.a * dY(uc_at)
                vals1.append(jetmax(e1))
            show("(1) resid j=%d" % j, vals1)
        print()


if __name__ == '__main__':
    main()
