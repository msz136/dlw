# -*- coding: utf-8 -*-
"""
solo2.py -- 用有限差分算 DLW 残差，u 取论文 (27) 的显式解析式。

u = -2(p1+q1)^2 / [ sqrt((a-p1)(a+q1)) cosh(xi1+eta1-theta) + (2a-p1+q1) ]
v = 2(ln fg)_{xy}，由 f,g 的显式形式给出。
"""
import mpmath as mp

mp.mp.dps = 50
X0, T0, Y0 = mp.mpf('0.3'), mp.mpf('0.4'), mp.mpf('0.5')


def analyze(a, p1, q1, lam, label):
    S = p1 + q1
    R = q1 ** 2 - p1 ** 2
    T = 1 / (q1 + a) + 1 / (p1 - a)
    # (27)
    sq = mp.sqrt((a - p1) * (a + q1))
    eth = S * sq          # exp(theta) = (p1+q1) sqrt((a+q1)/(a-p1)) ; 检验用下面等价式
    # 直接按论文： exp(theta) = (p1+q1) sqrt((a+q1)/(a-p1))
    eth = S * mp.sqrt((a + q1) / (a - p1))

    def u(x, t, y):
        z = S * x + R * t + T * y
        return -2 * S ** 2 / (sq * mp.cosh(z - mp.log(eth)) + (2 * a - p1 + q1))

    def v(x, t, y):
        cf = (-(p1 - a) / (q1 + a)) / S
        cg = 1 / S
        z = S * x + R * t + T * y
        f = 1 + cf * mp.e ** z
        g = 1 + cg * mp.e ** z
        # v = 2 (ln f g)_{xy}
        return 2 * mp.diff(lambda xx, yy: mp.log(f.subs({}) if False else
                                                 (1 + cf * mp.e ** (S * xx + R * t + T * yy)))
                           + mp.log(1 + cg * mp.e ** (S * xx + R * t + T * yy)),
                           x, y) if False else None
    # v 用解析对数导数
    def lz(c, mx, my):
        z = S * X0 + R * T0 + T * Y0
        W = c * mp.e ** z / (1 + c * mp.e ** z)
        return (S ** mx) * (T ** my) * (W if (mx + my) == 1 else W * (1 - W))

    cf = (-(p1 - a) / (q1 + a)) / S
    cg = 1 / S
    vval = 2 * (lz(cf, 1, 1) + lz(cg, 1, 1))

    # 数值导数
    hx = mp.mpf('1e-6')
    def d(fn, *args, idx=0):
        a2 = list(args)
        a2[idx] += hx
        b2 = list(args)
        b2[idx] -= hx
        return (fn(*a2) - fn(*b2)) / (2 * hx)

    uu = lambda x, t, y: u(x, t, y)
    vv = lambda x, t, y: 2 * (lz2(cf, x, t, y) + lz2(cg, x, t, y))

    def lz2(c, x, t, y):
        z = S * x + R * t + T * y
        W = c * mp.e ** z / (1 + c * mp.e ** z)
        return S * T * W * (1 - W)

    def d2(fn, i, j, x, t, y):
        return d(lambda *a: d(fn, *a, idx=j), x, t, y, idx=i)

    uval = uu(X0, T0, Y0)
    uy = d(uu, X0, T0, Y0, idx=2)
    ux = d(uu, X0, T0, Y0, idx=0)
    uxy = d2(uu, 0, 2, X0, T0, Y0)
    uyt = d2(uu, 1, 2, X0, T0, Y0)
    vxx = d2(vv, 0, 0, X0, T0, Y0)
    vx = d(vv, X0, T0, Y0, idx=0)
    vt = d(vv, X0, T0, Y0, idx=1)
    uxxy = d2(lambda *a: d(uu, *a, idx=0), 0, 2, X0, T0, Y0)

    D1 = uyt + vxx + uval * uxy + ux * uy + 2 * a * uxy
    D2 = vt + uval * vx + ux * vval + uxxy + 2 * a * vx + 2 * lam * ux
    print("  %-30s u=%-14s v=%-14s" % (label, mp.nstr(uval, 8), mp.nstr(vval, 8)))
    print("      DLW-1 = %-16s DLW-2 = %-16s" % (mp.nstr(D1, 8), mp.nstr(D2, 8)))


for (a, p1, q1, lam, lbl) in [
        (mp.mpf(4), mp.mpf(2) / 3, mp.mpf(-18) / 5, mp.mpf(-2), "a=4 p=2/3 q=-18/5"),
        (mp.mpf(1), mp.mpf(3) / 2, mp.mpf(-2), mp.mpf(-2), "a=1 p=3/2 q=-2")]:
    analyze(a, p1, q1, lam, lbl)
