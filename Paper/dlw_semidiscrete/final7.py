# -*- coding: utf-8 -*-
"""
final7.py -- 用**有限差分**独立计算 B_a(f,g) = (D_x^2+D_t+2aD_x) f.g，
            与 tau 引擎的 (7)_h 结果对照。f,g 用显式单孤子。

这一步不依赖任何内部引擎，直接检验 (7) 是否成立。
"""
import mpmath as mp

mp.mp.dps = 50
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3


def run(a, p, q, label):
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (q + a) + 1 / (p - a)
    cF = (-(p - a) / (q + a)) / (p + q)
    cG = 1 / (p + q)

    def f(x, t, y):
        return 1 + cF * mp.e ** (S * x + R * t + T * y)

    def g(x, t, y):
        return 1 + cG * mp.e ** (S * x + R * t + T * y)

    h = mp.mpf('1e-5')

    def Dx2(fn, gn):
        """(f_xx g - 2 f_x g_x + f g_xx) 数值"""
        fxx = (fn(X0 + h, T0, Y0) - 2 * fn(X0, T0, Y0) + fn(X0 - h, T0, Y0)) / h ** 2
        gxx = (gn(X0 + h, T0, Y0) - 2 * gn(X0, T0, Y0) + gn(X0 - h, T0, Y0)) / h ** 2
        fx = (fn(X0 + h, T0, Y0) - fn(X0 - h, T0, Y0)) / (2 * h)
        gx = (gn(X0 + h, T0, Y0) - gn(X0 - h, T0, Y0)) / (2 * h)
        return fxx * gn(X0, T0, Y0) - 2 * fx * gx + fn(X0, T0, Y0) * gxx

    def Dt(fn, gn):
        ft = (fn(X0, T0 + h, Y0) - fn(X0, T0 - h, Y0)) / (2 * h)
        gt = (gn(X0, T0 + h, Y0) - gn(X0, T0 - h, Y0)) / (2 * h)
        return ft * gn(X0, T0, Y0) - fn(X0, T0, Y0) * gt

    def Dx(fn, gn):
        fx = (fn(X0 + h, T0, Y0) - fn(X0 - h, T0, Y0)) / (2 * h)
        gx = (gn(X0 + h, T0, Y0) - gn(X0 - h, T0, Y0)) / (2 * h)
        return fx * gn(X0, T0, Y0) - fn(X0, T0, Y0) * gx

    B = Dx2(f, g) + Dt(f, g) + 2 * a * Dx(f, g)
    print("  %-26s  cF=%-12s cG=%-12s" % (label, mp.nstr(cF, 8), mp.nstr(cG, 8)))
    print("      B_a(f,g) [有限差分] = %s" % mp.nstr(B, 10))
    print("      f/g 比值          = %s" % mp.nstr(f(X0, T0, Y0) / g(X0, T0, Y0), 10))
    print()


run(mp.mpf(4), mp.mpf(2) / 3, mp.mpf(-18) / 5, "a=4 p=2/3 q=-18/5")
run(mp.mpf(-2), mp.mpf(1), mp.mpf(-2), "a=-2 p=1 q=-2")
run(mp.mpf(4), mp.mpf(2) / 3, mp.mpf(2) / 3 + 8, "a=4 p=2/3 q=26/3")
