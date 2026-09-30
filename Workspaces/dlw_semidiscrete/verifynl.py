# -*- coding: utf-8 -*-
"""
verifynl.py -- 直接数值核对 DLW-1 = 2 ∂_y(E7)，以及 u,v 是否满足 DLW。

用单孤子：f = 1 + cF e^z, g = 1 + cG e^z, z = Sx+Rt+Ty。
对 ln(1+c e^z) 的 z 阶导数用多项式递推（w = c e^z/(1+c e^z)）。
"""
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 60
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3


def logderiv_polys(nmax=8):
    polys = [[mp.mpf(0), mp.mpf(1)]]           # u_1 = w
    for _ in range(1, nmax):
        prev = polys[-1]
        d = [mp.mpf(0)] * (len(prev) + 1)
        for k, ck in enumerate(prev):
            if ck == 0:
                continue
            d[k] += ck * k
            d[k + 1] -= ck * k
        for k, ck in enumerate(prev):
            d[k + 1] += ck
        polys.append(d)
    return polys


POLY = logderiv_polys(9)


def uz(c, z, n):
    w = c * mp.e ** z / (1 + c * mp.e ** z)
    return sum(ck * w ** k for k, ck in enumerate(POLY[n]))


def tomp(x):
    return mp.mpf(x.numerator) / x.denominator if isinstance(x, Fr) else mp.mpf(x)


def run(a, p, q, lam, label):
    a = tomp(a)
    p = tomp(p)
    q = tomp(q)
    lam = tomp(lam)
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (q + a) + 1 / (p - a)
    cF = (-(p - a) / (q + a)) / (p + q)
    cG = 1 / (p + q)
    z = S * X0 + R * T0 + T * Y0

    def th(mx, mt, my):
        n = mx + mt + my
        if n == 0:
            return mp.log(1 + cF * mp.e ** z) - mp.log(1 + cG * mp.e ** z)
        return (S ** mx) * (R ** mt) * (T ** my) * (uz(cF, z, n) - uz(cG, z, n))

    def ps(mx, mt, my):
        n = mx + mt + my
        if n == 0:
            return mp.log(1 + cF * mp.e ** z) + mp.log(1 + cG * mp.e ** z)
        return (S ** mx) * (R ** mt) * (T ** my) * (uz(cF, z, n) + uz(cG, z, n))

    u = 2 * th(1, 0, 0)
    ux = 2 * th(2, 0, 0)
    uy = 2 * th(1, 0, 1)
    uxy = 2 * th(2, 0, 1)
    uyt = 2 * th(1, 1, 1)
    v = 2 * ps(1, 0, 1)
    vxx = 2 * ps(3, 0, 1)
    vx = 2 * ps(2, 0, 1)
    vt = 2 * ps(1, 1, 1)
    uxxy = 2 * th(3, 0, 1)

    # E7 = psi_xx + th_x^2 + psi_t + 2a th_x
    E7 = ps(2, 0, 0) + th(1, 0, 0) ** 2 + ps(0, 1, 0) + 2 * a * th(1, 0, 0)
    # ∂_y E7
    dE7 = ps(2, 0, 1) + 2 * th(1, 0, 0) * th(1, 0, 1) + ps(0, 1, 1) \
        + 2 * a * th(1, 0, 1)

    DLW1 = uyt + vxx + u * uxy + ux * uy + 2 * a * uxy

    D2 = vt + u * vx + ux * v + uxxy + 2 * a * vx + 2 * lam * ux
    print("  %-24s" % label)
    print("     E7                = %s" % mp.nstr(E7, 8))
    print("     DLW-1             = %s" % mp.nstr(DLW1, 8))
    print("     DLW-1 - 2*dE7     = %s" % mp.nstr(DLW1 - 2 * dE7, 8))
    print("     DLW-2             = %s" % mp.nstr(D2, 8))
    print()


run(4, Fr(2, 3), Fr(-18, 5), -2, "a=4 p=2/3 q=-18/5")
run(-2, 1, -2, -2, "a=-2 p=1 q=-2")
run(1, Fr(-10, 7), Fr(-1), -2, "a=1 p=-10/7 q=-1")
