# -*- coding: utf-8 -*-
"""
v3.py -- DLW 半离散非线性层：高精度综合验证（第三版，修正了 tau 规范化与 y 扰动）。

验证清单
  A  热方程审计  (ln F)_t = (ln F)_xx
  B  双线性基线  (7)_h = (6)_h = 0 与势变量基线 (N1)=(N2)=0   —— 应达机器精度
  C  精确恒等式  u_t = v - w + h*sum_j[u]*R'_w              —— 有限 h 精确
  D  连续化      w_j = v_j - u_{j,y} + O(h^2)
  E  闭合系统 (A)：把 w 换成 w_d = v - u_y 后的 u 方程残差    —— O(h^2)
  F  闭合系统 (B)：把 w 换成 w_d 后的 v 方程残差              —— O(h^2)
  G  连续极限    u_j, v_j vs 连续 u,v（同一参数 a）           —— O(h^2)
  H  连续 DLW (1)(2) 在 (u_cont, v_cont) 上的残差             —— 机器精度
"""

import random
from itertools import permutations

import mpmath as mp

from jet import Jet
from taujet import Tau, jetmax

DPS = 90
mp.mp.dps = DPS

X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7
J0 = 1
HS = [mp.mpf(1) / 4, mp.mpf(1) / 8, mp.mpf(1) / 16, mp.mpf(1) / 32]
HS3 = HS[:3]

MACH = mp.mpf(10) ** (-(DPS - 20))


# ==========================================================================
#  派生量
# ==========================================================================
def alpha(T, j, dy=mp.mpf(0)):
    return T.F(j, X0, T0, dy).log()


def beta(T, j, dy=mp.mpf(0)):
    return T.G(j, X0, T0, dy).log()


def u_of(T, j):
    return 2 * (alpha(T, j) - beta(T, j)).dx()


def w_of(T, j):
    return 2 * (alpha(T, j) + beta(T, j)).dx()


def v_of(T, j):
    Ps = lambda k: alpha(T, k) + beta(T, k)
    return (Ps(j + 1) - Ps(j - 1)).dx() / T.h


def uy_of(T, j):
    return (u_of(T, j + 1) - u_of(T, j - 1)) / T.h


def sumop(T, j, f):
    return (f(T, j + 1) + 2 * f(T, j) + f(T, j - 1)) / 4


def N1(T, j):
    th = alpha(T, j) - beta(T, j)
    Ps = alpha(T, j) + beta(T, j)
    return Ps.dxn(2) + th.dx() ** 2 + th.dt() + 2 * (T.a - T.h / 2) * th.dx()


def N2(T, j):
    Th = alpha(T, j) - beta(T, j + 1)
    Ph = alpha(T, j) + beta(T, j + 1)
    return Ph.dxn(2) + Th.dx() ** 2 + Th.dt() + 2 * (T.a + T.h / 2) * Th.dx()


def Rp_w(T, j):
    return N1(T, j).dx() + N2(T, j).dx()


def bEplus(T, j):
    F, G = T.F(j, X0, T0), T.G(j, X0, T0)
    s = T.a - T.h / 2
    return F.dxn(2) * G - 2 * F.dx() * G.dx() + F * G.dxn(2) \
        + (F.dt() * G - F * G.dt()) + 2 * s * (F.dx() * G - F * G.dx())


def bEminus(T, j):
    F, G = T.F(j, X0, T0), T.G(j + 1, X0, T0)
    s = T.a + T.h / 2
    return F.dxn(2) * G - 2 * F.dx() * G.dx() + F * G.dxn(2) \
        + (F.dt() * G - F * G.dt()) + 2 * s * (F.dx() * G - F * G.dx())


# --------------------------------------------------------------------------
def show(name, vals, ratios=True):
    print("  %-30s" % name + "".join(" %11.3e" % float(v) for v in vals))
    if ratios and len(vals) > 1:
        rr = [float(vals[k - 1] / vals[k]) if vals[k] != 0 else float('inf')
              for k in range(1, len(vals))]
        print("  %-30s" % "" + "".join(" %11.3f" % r for r in rr) + "   <- ratios")


# ==========================================================================
#  正则参数搜索（用标量 mpmath 求值）
# ==========================================================================
def tau_scalar(N, a, p, q, h, n, j, s, mu, x0, t0):
    ent = {}
    for i in range(N):
        for k in range(N):
            coef = (-(p[i] - s) / (q[k] + s)) ** n / (p[i] + q[k])
            if j:
                d = h / 2
                lp = (p[i] - a + d) / (p[i] - a - d)
                lq = (q[k] + a + d) / (q[k] + a - d)
                coef = coef * (lp * lq) ** j
            c0 = (p[i] * x0 - p[i] ** 2 * t0) + (q[k] * x0 + q[k] ** 2 * t0)
            e = coef * mp.e ** c0
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


def is_regular(N, a, p, q, h, j0, margin=mp.mpf('0.05')):
    for j in range(j0 - 2, j0 + 4):
        F = tau_scalar(N, a, p, q, h, 1, j, a - h / 2, a, X0, T0)
        G = tau_scalar(N, a, p, q, h, 0, j, a, a, X0, T0)
        if not (abs(F) > margin and abs(G) > margin):
            return None
        if abs(F - G) <= margin:
            return None
        if abs(F / G - 1) < mp.mpf('0.02'):
            return None
    return True


def find_params(N, tries=40000, seed=1):
    rng = random.Random(seed)
    best = None
    for _ in range(tries):
        a = mp.mpf(rng.randint(-10, 10)) / rng.randint(1, 4)
        p = [mp.mpf(rng.randint(1, 20)) / rng.randint(1, 7) for _ in range(N)]
        q = [mp.mpf(rng.randint(-20, -1)) / rng.randint(1, 7) for _ in range(N)]
        bad = False
        for i in range(N):
            if abs(p[i] - a) < mp.mpf('0.3') or abs(q[i] + a) < mp.mpf('0.3'):
                bad = True
        for i in range(N):
            for k in range(N):
                if abs(p[i] + q[k]) < mp.mpf('0.3'):
                    bad = True
        for i in range(N):
            for k in range(i + 1, N):
                if abs(p[i] - p[k]) < mp.mpf('0.3') or abs(q[i] - q[k]) < mp.mpf('0.3'):
                    bad = True
        if bad:
            continue
        ok = all(is_regular(N, a, p, q, h, J0) for h in HS3)
        if not ok:
            continue
        # 评分：F/G 偏离 1 的最小值大者优先
        sc = []
        for h in HS3:
            for j in range(J0 - 2, J0 + 4):
                F = tau_scalar(N, a, p, q, h, 1, j, a - h / 2, a, X0, T0)
                G = tau_scalar(N, a, p, q, h, 0, j, a, a, X0, T0)
                sc.append(abs(F / G - 1))
        score = min(sc)
        if best is None or score > best[0]:
            best = (score, a, list(p), list(q))
    return best


# ==========================================================================
#  单个 N 的完整验证
# ==========================================================================
def run_N(N):
    b = find_params(N, tries=3000, seed=4242 + 17 * N)
    if b is None:
        print("N=%d : 未找到正则参数点" % N)
        return
    score, a, p, q = b
    print("\n" + "=" * 92)
    print("N = %d   a = %s   p = %s   q = %s      (min|F/G-1| = %.4f)"
          % (N, mp.nstr(a, 10), [mp.nstr(v, 10) for v in p],
             [mp.nstr(v, 10) for v in q], float(score)))
    print("=" * 92)
    j = J0

    TL = {h: Tau(N, a, p, q, h) for h in HS}
    TC = {h: Tau(N, a, p, q, None) for h in HS}

    def hmax(e):
        return jetmax(e)

    print("\n  [A] 热方程审计 (ln F)_t - (ln F)_xx  (j = %d,%d,%d)" % (j - 1, j, j + 1))
    for jj in [j - 1, j, j + 1]:
        e = alpha(TL[HS[0]], jj).dt() - alpha(TL[HS[0]], jj).dxn(2)
        print("      j=%d : %.3e" % (jj, float(hmax(e))))

    print("\n  [B] 基线残差（应达机器精度 ~1e-%d）" % (DPS - 20))
    for h in HS3:
        T = TL[h]
        print("      h=%-7s : (7)_h=%.2e  (6)_h=%.2e  (N1)=%.2e  (N2)=%.2e"
              % (mp.nstr(h, 5), float(hmax(bEplus(T, j))), float(hmax(bEminus(T, j))),
                 float(hmax(N1(T, j))), float(hmax(N2(T, j)))))

    print("\n  [C] 精确恒等式  u_t - [v - w + h*sum_j[u]*R'_w]  (有限 h 精确)")
    show("residual", [hmax(u_of(TL[h], j).dt()
                            - (v_of(TL[h], j) - w_of(TL[h], j)
                               + h * sumop(TL[h], j, lambda T, k: u_of(T, k)) * Rp_w(TL[h], j)))
                      for h in HS], ratios=False)

    print("\n  [D] w_j - (v_j - u_{j,y})   期望 O(h^2) -> ratio 4")
    show("w-(v-u_y)", [hmax(w_of(TL[h], j) - (v_of(TL[h], j) - uy_of(TL[h], j)))
                       for h in HS])

    print("\n  [E] 闭合 (A): u_t - [v - w_d + (h/2)(u - w_d) + h u_x],  w_d = v - u_y")
    vals = []
    for h in HS:
        T = TL[h]
        wd = v_of(T, j) - uy_of(T, j)
        vals.append(hmax(u_of(T, j).dt() - (v_of(T, j) - wd + h / 2 * (u_of(T, j) - wd)
                                            + h * u_of(T, j).dx())))
    show("(A) residual", vals)

    print("\n  [F] 闭合 (B): w_d,t + sum_j[u] R'_w ,  w_d = v - u_y")
    vals = []
    for h in HS:
        T = TL[h]
        wd = v_of(T, j) - uy_of(T, j)
        vals.append(hmax(wd.dt() + sumop(T, j, lambda T, k: u_of(T, k)) * Rp_w(T, j)))
    show("(B) residual", vals)

    print("\n  [G] 连续极限  Y=(j+1/2)h ： |u_j - u_cont(Y)| , |v_j - v_cont(Y)|")
    uv, vv = [], []
    for h in HS:
        Y = (mp.mpf(j) + mp.mpf(1) / 2) * h
        TC_ = TC[h]
        uc = 2 * (alpha(TC_, 0, Y) - beta(TC_, 0, Y)).dx()
        eps = mp.mpf(10) ** (-(DPS // 2))
        lf = lambda dy: alpha(TC_, 0, dy) + beta(TC_, 0, dy)
        vc = 2 * ((lf(Y + eps) - lf(Y - eps)) / (2 * eps)).dx()
        uv.append(hmax(u_of(TL[h], j) - uc))
        vv.append(hmax(v_of(TL[h], j) - vc))
    show("|u_j - u_cont|", uv)
    show("|v_j - v_cont|", vv)

    print("\n  [H] 连续 DLW (1)(2) 在 (u_cont, v_cont) 上的残差（机器精度）")
    e1s, e2s = [], []
    for h in HS3:
        Y = (mp.mpf(j) + mp.mpf(1) / 2) * h
        T = TC[h]
        eps = mp.mpf(10) ** (-(DPS // 2))
        ucf = lambda dy: 2 * (alpha(T, 0, dy) - beta(T, 0, dy)).dx()
        lf = lambda dy: alpha(T, 0, dy) + beta(T, 0, dy)
        vcf = lambda dy: 2 * ((lf(dy + eps) - lf(dy - eps)) / (2 * eps)).dx()
        dY = lambda f: (f(Y + eps) - f(Y - eps)) / (2 * eps)
        uc, vc = ucf(Y), vcf(Y)
        t1 = uc.dt() + dY(vcf) + uc * dY(ucf) + 2 * T.a * dY(ucf)
        t2 = vc.dt() + (uc * vc).dx() + dY(lambda dy: ucf(dy).dxn(2)) \
            + 2 * T.a * vc.dx() - 4 * uc.dx()
        e1s.append(hmax(t1))
        e2s.append(hmax(t2))
    show("(1) residual", e1s, ratios=False)
    show("(2) residual", e2s, ratios=False)


if __name__ == '__main__':
    import sys
    Ns = [int(v) for v in sys.argv[1:]] or [1, 2]
    for N in Ns:
        run_N(N)
