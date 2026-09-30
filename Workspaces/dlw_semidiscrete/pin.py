# -*- coding: utf-8 -*-
"""
pin.py -- 定位矛盾：同时算 B_a(f,g) 的 (a) 有限差分、(b) 解析式 (cF+cG)(S^2+R+2aS)E，
         以及 E7 = psi_xx + th_x^2 + psi_t + 2a th_x。三者必须一致。
"""
import mpmath as mp

mp.mp.dps = 50
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3


def expnd(a, p, q):
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (q + a) + 1 / (p - a)
    cF = (-(p - a) / (q + a)) / (p + q)
    cG = 1 / (p + q)
    z = S * X0 + R * T0 + T * Y0
    E = mp.e ** z

    f = lambda x, t, y: 1 + cF * mp.e ** (S * x + R * t + T * y)
    g = lambda x, t, y: 1 + cG * mp.e ** (S * x + R * t + T * y)

    h = mp.mpf('1e-6')
    fxx = (f(X0 + h, T0, Y0) - 2 * f(X0, T0, Y0) + f(X0 - h, T0, Y0)) / h ** 2
    gxx = (g(X0 + h, T0, Y0) - 2 * g(X0, T0, Y0) + g(X0 - h, T0, Y0)) / h ** 2
    fx = (f(X0 + h, T0, Y0) - f(X0 - h, T0, Y0)) / (2 * h)
    gx = (g(X0 + h, T0, Y0) - g(X0 - h, T0, Y0)) / (2 * h)
    ft = (f(X0, T0 + h, Y0) - f(X0, T0 - h, Y0)) / (2 * h)
    gt = (g(X0, T0 + h, Y0) - g(X0, T0 - h, Y0)) / (2 * h)
    B_fd = (fxx * g(X0, T0, Y0) - 2 * fx * gx + f(X0, T0, Y0) * gxx) \
        + (ft * g(X0, T0, Y0) - f(X0, T0, Y0) * gt) \
        + 2 * a * (fx * g(X0, T0, Y0) - f(X0, T0, Y0) * gx)
    B_an = (cF + cG) * (S ** 2 + R + 2 * a * S) * E

    # E7 —— 用解析对数导数
    def W(c):
        return c * E / (1 + c * E)

    def uz(c, n):
        w = W(c)
        polys = [[mp.mpf(0), mp.mpf(1)]]
        for _ in range(1, 8):
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
        return sum(ck * w ** k for k, ck in enumerate(polys[n]))

    ps_xx = S ** 2 * (uz(cF, 2) + uz(cG, 2))
    ps_t = R * (uz(cF, 1) + uz(cG, 1))
    th_x = S * (uz(cF, 1) - uz(cG, 1))
    E7 = ps_xx + th_x ** 2 + ps_t + 2 * a * th_x

    print("  S=%s R=%s T=%s" % (mp.nstr(S, 8), mp.nstr(R, 8), mp.nstr(T, 8)))
    print("  cF=%s  cG=%s" % (mp.nstr(cF, 10), mp.nstr(cG, 10)))
    print("  E  = %s" % mp.nstr(E, 10))
    print("  S^2+R+2aS = %s" % mp.nstr(S ** 2 + R + 2 * a * S, 10))
    print("  B_a 解析 = %s" % mp.nstr(B_an, 10))
    print("  B_a 差分 = %s" % mp.nstr(B_fd, 10))
    print("  E7      = %s" % mp.nstr(E7, 10))
    print("  ps_xx=%s  th_x^2=%s  ps_t=%s  2a th_x=%s"
          % (mp.nstr(ps_xx, 8), mp.nstr(th_x ** 2, 8), mp.nstr(ps_t, 8),
             mp.nstr(2 * a * th_x, 8)))
    print()


print("a=4 p=2/3 q=-18/5")
expnd(mp.mpf(4), mp.mpf(2) / 3, mp.mpf(-18) / 5)
print("a=-2 p=1 q=-2")
expnd(mp.mpf(-2), mp.mpf(1), mp.mpf(-2))
