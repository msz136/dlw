# -*- coding: utf-8 -*-
"""
solo.py -- 完全独立的单孤子核对：不用 tau 引擎，直接写显式 f, g。

按论文 (5)(6)(7) 与 m11^(n) = c1 + (-(p1-a)/(q1+a))^n * 1/(p1+q1) * e^{xi1+eta1}
    xi1  + eta1 = (p1+q1)x + (q1^2-p1^2)t + (1/(q1+a) + 1/(p1-a)) y
    u = 2(ln f/g)_x ,  v = 2(ln fg)_{xy}
测 u,v 是否满足 DLW (1)(2)。
"""
import mpmath as mp

mp.mp.dps = 60
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3

CASES = [
    (mp.mpf(4), mp.mpf(2) / 3, mp.mpf(-18) / 5, mp.mpf(-2)),
    (mp.mpf(-2), mp.mpf(1), mp.mpf(-2), mp.mpf(-2)),
    (mp.mpf(5) / 3, mp.mpf(1) / 5, mp.mpf(-1), mp.mpf(-2)),
    (mp.mpf(0), mp.mpf(1), mp.mpf(2), mp.mpf(1)),
]


def make(a, p, q):
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (p - a) + 1 / (q + a)
    cf = (-(p - a) / (q + a)) / S
    cg = 1 / S
    return cf, cg, (S, R, T)


def run(a, p, q, lam, label):
    cf, cg, (S, R, T) = make(a, p, q)
    # f = 1 + cf E,  g = 1 + cg E ;  E = e^{Sx+Rt+Ty}
    E = lambda x, t, y: mp.e ** (S * x + R * t + T * y)
    # ln f, ln g 的导数
    def dl(c, m):
        """d^m/dz^m ln(1 + c e^{z})，z = Sx+Rt+Ty；返回关于 z 的导数"""
        e = c * mp.e ** 0  # 占位
        raise SystemExit

    # ln(1+c e^z) 的 z 阶导数，写成 W = c e^z/(1+c e^z) 的多项式：
    #   u_1 = W ;  u_{n+1} = (d/dW u_n) * W(1-W) + W * u_n
    def poly_table(nmax=6):
        polys = [[mp.mpf(0), mp.mpf(1)]]
        for _ in range(1, nmax):
            prev = polys[-1]
            m = len(prev) + 1
            d = [mp.mpf(0)] * m
            for k, ck in enumerate(prev):
                if ck == 0:
                    continue
                d[k] += ck * k
                d[k + 1] -= ck * k
            for k, ck in enumerate(prev):
                d[k + 1] += ck           # 加 W * u_n
            polys.append(d)
        return polys

    POLY = poly_table(7)

    def valU(c, z, n):
        W = c * mp.e ** z / (1 + c * mp.e ** z)
        p = POLY[n]
        return sum(ck * W ** k for k, ck in enumerate(p))

    def lz(c, mx, mt, my, x=X0, t=T0, y=Y0):
        z = S * x + R * t + T * y
        mult = S ** mx * R ** mt * T ** my
        order = mx + mt + my
        if order == 0:
            return mp.log(1 + c * mp.e ** z)
        return mult * valU(c, z, order)

    # 对数导数 needed: up to 3rd order in (x,t,y) combos
    def ld(c, mx, mt, my):
        return lz(c, mx, mt, my)

    th = lambda mx, mt, my: ld(cf, mx, mt, my) - ld(cg, mx, mt, my)
    Ps = lambda mx, mt, my: ld(cf, mx, mt, my) + ld(cg, mx, mt, my)

    u = 2 * th(1, 0, 0)
    ux = 2 * th(2, 0, 0)
    uy = 2 * th(1, 0, 1)
    uxy = 2 * th(2, 0, 1)
    uyt = 2 * th(1, 1, 1)
    uxxy = 2 * th(3, 0, 1)
    v = 2 * Ps(1, 0, 1)
    vx = 2 * Ps(2, 0, 1)
    vxx = 2 * Ps(3, 0, 1)
    vt = 2 * Ps(1, 1, 1)

    D1 = uyt + vxx + u * uxy + ux * uy + 2 * a * uxy
    D2 = vt + u * vx + ux * v + uxxy + 2 * a * vx + 2 * lam * ux
    print("  %-26s u=%-14s v=%-14s" % (label, mp.nstr(u, 8), mp.nstr(v, 8)))
    print("      DLW-1 = %-16s DLW-2 = %-16s" % (mp.nstr(D1, 8), mp.nstr(D2, 8)))


print("点 (x,t,y) = (1/5, 2/7, 1/3)")
for (a, p, q, lam) in CASES:
    run(a, p, q, lam, "a=%s p=%s q=%s lam=%s"
        % (mp.nstr(a, 5), mp.nstr(p, 5), mp.nstr(q, 5), mp.nstr(lam, 5)))
