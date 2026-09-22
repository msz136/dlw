# -*- coding: utf-8 -*-
"""
verify_nl2.py --  DLW 半离散非线性层：高精度（70 位）综合验证。

设计要点
  * 用 jet（截断泰勒）在 (x,t) 展开；对 DLW 的 tau 有 tau_xx = tau_t，
    故 d/dt = d_x^2（脚本用 (ln F)_t = (ln F)_xx 审计）。
  * 自动搜索"正则参数点"，使被测格点邻域上 F_j,G_j > 0 且 F_j != G_j
    （对数必须为实）。同一组参数在 h = 1/4,1/8,1/16 上都要正则。
  * tau 求值时整体除以一个参考量级，避免指数溢出。
  * 每族导出的量都给 jet 系数最大绝对值；h 减半的比值给出阶数
    （16 = h^4，4 = h^2，1 = 非收敛）。

验证清单
  A  热方程审计
  B  双线性基线  (7)_h = (6)_h = 0 与势变量基线  (N1) = (N2) = 0
  C  精确恒等式  u_t = v - w + h * sum_j[u] * R'_w        （有限 h 精确）
  D  连续化      w_j = v_j - u_{j,y} + O(h^2)
  E  闭合系统 (A) ：把 w 换成 w_disc 后的 u 方程残差      O(h^2)
  F  闭合系统 (B) ：把 w 换成 w_disc 后的 v 方程残差      O(h^2)
  G  u_j, v_j 的连续极限与二阶精度
  H  连续极限下本系统恢复 DLW (1)(2)
"""

import random
from itertools import permutations

import mpmath as mp
from jet import Jet

mp.mp.dps = 70

X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7
J0 = 1
HS = [mp.mpf(1) / 4, mp.mpf(1) / 8, mp.mpf(1) / 16]


# ==========================================================================
#  模型
# ==========================================================================
def lam(z, h):
    return (z + h / 2) / (z - h / 2)


class Model:
    def __init__(self, N, h, a, p, q, scale=None):
        self.N = N
        self.h = mp.mpf(h)
        self.a = mp.mpf(a)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.uv = Jet.var()
        self._c = {}
        self.scale = mp.mpf(scale) if scale is not None else self._find_scale()

    # ------- 尺度（只用 0 阶近似估）-------------------------------------
    def _find_scale(self):
        m = mp.mpf(0)
        for i in range(self.N):
            for k in range(self.N):
                rate = (self.p[i] * X0 - self.p[i] ** 2 * T0) + (self.q[k] * X0 + self.q[k] ** 2 * T0)
                m = max(m, abs(mp.e ** rate / (self.p[i] + self.q[k])))
        return mp.mpf(1) if m == 0 else m

    # ------- tau --------------------------------------------------------
    def entry(self, n, i, k, j, s, mu):
        p, q = self.p[i], self.q[k]
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        if j:
            coef = coef * (lam(p - mu, self.h) * lam(q + mu, self.h)) ** j
        rate = (p * X0 - p ** 2 * T0) + (q * X0 + q ** 2 * T0)
        jt = coef * (mp.e ** rate) * (Jet.const(p + q) * self.uv).exp()
        if i == k:
            jt = jt + 1
        return jt * (1 if i == k else 1)

    def tau_raw(self, n, j, s, mu):
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

    # 用"列尺度"缩放矩阵元，使行列式量级 ~ 1（相似变换不改变行列式的符号结构）
    def tau(self, n, j, s, mu):
        t = self.tau_raw(n, j, s, mu)
        sc = self.scale ** (self.N * (j + 1))
        return t * (1 / sc)

    def F(self, j):
        return self.tau(1, j, self.a - self.h / 2, self.a)

    def G(self, j):
        return self.tau(0, j, self.a, self.a)

    # ------- 势变量 ------------------------------------------------------
    def alpha(self, j):
        return self.F(j).log()

    def beta(self, j):
        return self.G(j).log()

    def theta(self, j):
        return self.alpha(j) - self.beta(j)

    def Psi(self, j):
        return self.alpha(j) + self.beta(j)

    def u(self, j):
        return 2 * self.theta(j).dx()

    def w(self, j):
        return 2 * self.Psi(j).dx()

    # ------- 残差 --------------------------------------------------------
    def N1(self, j):
        th, Ps = self.theta(j), self.Psi(j)
        return Ps.dxn(2) + th.dx() ** 2 + th.dt() + 2 * (self.a - self.h / 2) * th.dx()

    def N2(self, j):
        Th = self.alpha(j) - self.beta(j + 1)
        Ph = self.alpha(j) + self.beta(j + 1)
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
    """连续参照（真实 y 坐标）。"""

    def __init__(self, N, h, a, p, q, scale=None):
        super().__init__(N, h, a, p, q, scale)
        self._cc = {}

    def entry_c(self, n, i, k, y, s):
        p, q = self.p[i], self.q[k]
        coef = (-(p - s) / (q + s)) ** n / (p + q)
        rate = (p * X0 - p ** 2 * T0) + (q * X0 + q ** 2 * T0) \
            + y * (1 / (p - self.a) + 1 / (q + self.a))
        jt = coef * (mp.e ** rate) * (Jet.const(p + q) * self.uv).exp()
        if i == k:
            jt = jt + 1
        return jt

    def tau_c(self, n, y, s):
        key = (n, y, s)
        if key in self._cc:
            return self._cc[key]
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
                term = term * self.entry_c(n, i, perm[i], y, s)
            tot = tot + term
        self._cc[key] = tot
        return tot

    def Fc(self, y):
        return self.tau_c(1, y, self.a) / (self.scale ** self.N)

    def Gc(self, y):
        return self.tau_c(0, y, self.a) / (self.scale ** self.N)

    def uc(self, y):
        return 2 * (self.Fc(y).log() - self.Gc(y).log()).dx()

    def vc(self, y, eps=None):
        if eps is None:
            eps = mp.mpf('1e-16')
        lf = lambda yy: self.Fc(yy).log() + self.Gc(yy).log()
        return 2 * ((lf(y + eps) - lf(y - eps)) * (1 / (2 * eps))).dx()


# ==========================================================================
#  工具
# ==========================================================================
def jetmax(jt):
    m = max(abs(v) for v in jt.a)
    return m


def show(name, vals, ratios=True, unit=''):
    s = "  %-34s" % name + "".join(" %11.4e" % float(v) for v in vals)
    if unit:
        s += "   " + unit
    print(s)
    if ratios and len(vals) > 1:
        rr = []
        for k in range(1, len(vals)):
            rr.append(float(vals[k - 1] / vals[k]) if vals[k] != 0 else float('inf'))
        print("  %-34s" % "" + "".join(" %11.3f" % r for r in rr) + "    <- ratios")


def v_of(M, j):
    """v_j = (1/h) d_x (Psi_{j+1} - Psi_{j-1}) = 2 delta_j Psi_j"""
    return (M.Psi(j + 1) - M.Psi(j - 1)).dx() / M.h


def uy_of(M, j):
    """u_{j,y} = delta_j u_j = (u_{j+1}-u_{j-1})/h"""
    return (M.u(j + 1) - M.u(j - 1)) / M.h


def sumop(M, j, f):
    """sum_j[u] f = (f_{j+1} + 2 f_j + f_{j-1})/4"""
    return (f(M, j + 1) + 2 * f(M, j) + f(M, j - 1)) / 4


def Rp_w(M, j):
    """R'_w = (N1)_x + (N2)_x"""
    return M.N1(j).dx() + M.N2(j).dx()


# ==========================================================================
#  正则参数搜索
# ==========================================================================
def find_params(N, hs, tries=30000, seed=4242):
    rng = random.Random(seed)
    x0, t0 = X0, T0
    best = None
    for _ in range(tries):
        a = mp.mpf(rng.randint(-8, 8)) / rng.randint(1, 3)
        p = [mp.mpf(rng.randint(1, 15)) / rng.randint(1, 6) for _ in range(N)]
        q = [mp.mpf(rng.randint(-15, -1)) / rng.randint(1, 6) for _ in range(N)]
        if any(abs(p[i] - a) < mp.mpf('0.3') for i in range(N)):
            continue
        if any(abs(q[k] + a) < mp.mpf('0.3') for k in range(N)):
            continue
        if any(abs(p[i] + q[k]) < mp.mpf('0.3') for i in range(N) for k in range(N)):
            continue
        if any(abs(p[i] - p[j]) < mp.mpf('0.3') for i in range(N) for j in range(i + 1, N)):
            continue
        if any(abs(q[i] - q[j]) < mp.mpf('0.3') for i in range(N) for j in range(i + 1, N)):
            continue
        ok = True
        spreads = []
        scales = []
        for h in hs:
            for j in range(J0 - 2, J0 + 4):
                try:
                    F = float(Fnum(N, p, q, a, h, j, x0, t0))
                    G = float(Gnum(N, p, q, a, h, j, x0, t0))
                except (OverflowError, ValueError):
                    ok = False
                    break
                if not (F > 0.05 and G > 0.05):
                    ok = False
                    break
                if abs(F - G) < 0.05:
                    ok = False
                    break
                spreads.append(abs(F - G) / max(F, G))
                scales.append(max(F, G))
            if not ok:
                break
        if not ok:
            continue
        if max(scales) / min(scales) > 1e8:
            continue
        score = min(spreads)
        if best is None or score > best[0]:
            best = (score, a, list(p), list(q))
    return best


def Fnum(N, p, q, a, h, j, x0, t0):
    return _taunum(N, p, q, a, h, 1, j, a - h / 2, a, x0, t0)


def Gnum(N, p, q, a, h, j, x0, t0):
    return _taunum(N, p, q, a, h, 0, j, a, a, x0, t0)


def _taunum(N, p, q, a, h, n, j, s, mu, x0, t0):
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


# ==========================================================================
#  主流程
# ==========================================================================
def run_N(N, a, p, q):
    print("\n" + "=" * 96)
    print("N = %d    a = %s    p = %s    q = %s    (x0,t0)=(%s,%s)"
          % (N, mp.nstr(a, 8), [mp.nstr(v, 8) for v in p],
             [mp.nstr(v, 8) for v in q], mp.nstr(X0, 6), mp.nstr(T0, 6)))
    print("=" * 96)
    j = J0

    # A 热方程审计
    M = Model(N, HS[0], a, p, q)
    for jj in [J0 - 1, J0, J0 + 1]:
        e = M.alpha(jj).dt() - M.alpha(jj).dxn(2)
        print("  [A] heat audit j=%d : jetmax = %.3e" % (jj, float(jetmax(e))))

    # B 基线
    print("\n  [B] 基线残差（应精确为零）")
    for h in HS:
        M = Model(N, h, a, p, q)
        print("      h=%-7s : (7)_h=%.2e  (6)_h=%.2e  (N1)=%.2e  (N2)=%.2e"
              % (mp.nstr(h, 5), float(jetmax(M.bEplus(j))), float(jetmax(M.bEminus(j))),
                 float(jetmax(M.N1(j))), float(jetmax(M.N2(j)))))

    # C 精确恒等式
    print("\n  [C] 精确恒等式  u_t - [v - w + h*sum_j[u]*R'_w] = 0  (有限 h)")
    vals = []
    for h in HS:
        M = Model(N, h, a, p, q)
        e = M.u(j).dt() - (v_of(M, j) - M.w(j)
                           + M.h * sumop(M, j, lambda M, k: M.u(k)) * Rp_w(M, j))
        vals.append(jetmax(e))
    show("residual", vals, ratios=False)

    # D w 连续化
    print("\n  [D] w_j - (v_j - u_{j,y})   期望 O(h^2)")
    vals = []
    for h in HS:
        M = Model(N, h, a, p, q)
        vals.append(jetmax(M.w(j) - (v_of(M, j) - uy_of(M, j))))
    show("w-(v-u_y)", vals)

    # E 闭合 (A)
    print("\n  [E] 闭合系统 (A)：u_t - [v - w_d + d(u - w_d) + 2d u_x] ,  w_d = v - u_y")
    vals = []
    for h in HS:
        M = Model(N, h, a, p, q)
        wd = v_of(M, j) - uy_of(M, j)
        e = M.u(j).dt() - (v_of(M, j) - wd + M.h / 2 * (M.u(j) - wd) + M.h * M.u(j).dx())
        vals.append(jetmax(e))
    show("(A) residual", vals)

    # F 闭合 (B)
    print("\n  [F] 闭合系统 (B)：w_d,t + sum_j[u]*R'_w ,  w_d = v - u_y")
    vals = []
    for h in HS:
        M = Model(N, h, a, p, q)
        wd = v_of(M, j) - uy_of(M, j)
        e = wd.dt() + sumop(M, j, lambda M, k: M.u(k)) * Rp_w(M, j)
        vals.append(jetmax(e))
    show("(B) residual", vals)

    # G 连续极限
    print("\n  [G] 连续极限  Y = (j+1/2)h ;  |u_j - u_cont| , |v_j - v_cont|")
    uv, vv = [], []
    for h in HS:
        M = Model(N, h, a, p, q)
        MC = ContModel(N, h, a, p, q)
        Y = (mp.mpf(j) + mp.mpf(1) / 2) * h
        uv.append(jetmax(M.u(j) - MC.uc(Y)))
        vv.append(jetmax(v_of(M, j) - MC.vc(Y)))
    show("|u_j-u_cont|", uv)
    show("|v_j-v_cont|", vv)

    # H 连续 DLW 残差
    print("\n  [H] 连续 DLW 方程 (1)(2) 在 (u_cont, v_cont) 上的残差（应精确为零）")
    e1s, e2s = [], []
    eps = mp.mpf('1e-16')
    for h in HS:
        MC = ContModel(N, h, a, p, q)
        Y = (mp.mpf(j) + mp.mpf(1) / 2) * h
        ucf = lambda yy: MC.uc(yy)
        vcf = lambda yy: MC.vc(yy)
        dY = lambda f: (f(Y + eps) - f(Y - eps)) * (1 / (2 * eps))
        uc, vc = ucf(Y), vcf(Y)
        t1 = uc.dt() + dY(vcf) + uc * dY(ucf) + 2 * MC.a * dY(ucf)
        # (2) 用 v_t + (u v)_x + u_xxy + 2a v_x + 2 lambda u_x , lambda = -2
        u_x = uc.dx()
        uv_x = (uc * vc).dx()
        u_xxy = dY(lambda yy: ucf(yy).dxn(2))
        v_x = vc.dx()
        t2 = vc.dt() + uv_x + u_xxy + 2 * MC.a * v_x + 2 * mp.mpf(-2) * u_x
        e1s.append(jetmax(t1))
        e2s.append(jetmax(t2))
    show("(1) residual", e1s, ratios=False)
    show("(2) residual", e2s, ratios=False)


def main():
    for N in [1, 2, 3]:
        b = find_params(N, HS, tries=20000, seed=99 + 7 * N)
        if b is None:
            print("N=%d : no regular parameter point found" % N)
            continue
        score, a, p, q = b
        print("\n[params] N=%d  min spread = %.4f" % (N, score))
        run_N(N, a, p, q)


if __name__ == '__main__':
    main()
