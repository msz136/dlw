# -*- coding: utf-8 -*-
"""
cmp.py -- 把 B_a(f,g) 的解析式与有限差分**逐项**对照，找出差异来源。
"""
import mpmath as mp

mp.mp.dps = 60


def go(a, p, q, X0, T0, Y0):
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (q + a) + 1 / (p - a)
    cF = (-(p - a) / (q + a)) / (p + q)
    cG = 1 / (p + q)
    z = S * X0 + R * T0 + T * Y0
    E = mp.e ** z

    f = lambda x, t, y: 1 + cF * mp.e ** (S * x + R * t + T * y)
    g = lambda x, t, y: 1 + cG * mp.e ** (S * x + R * t + T * y)
    F0, G0 = f(X0, T0, Y0), g(X0, T0, Y0)

    h = mp.mpf('1e-8')
    Fx = (f(X0 + h, T0, Y0) - f(X0 - h, T0, Y0)) / (2 * h)
    Gx = (g(X0 + h, T0, Y0) - g(X0 - h, T0, Y0)) / (2 * h)
    Fxx = (f(X0 + h, T0, Y0) - 2 * F0 + f(X0 - h, T0, Y0)) / h ** 2
    Gxx = (g(X0 + h, T0, Y0) - 2 * G0 + g(X0 - h, T0, Y0)) / h ** 2
    Ft = (f(X0, T0 + h, Y0) - f(X0, T0 - h, Y0)) / (2 * h)
    Gt = (g(X0, T0 + h, Y0) - g(X0, T0 - h, Y0)) / (2 * h)

    fd_x2 = Fxx * G0 - 2 * Fx * Gx + F0 * Gxx
    fd_t = Ft * G0 - F0 * Gt
    fd_x = Fx * G0 - F0 * Gx
    B_fd = fd_x2 + fd_t + 2 * a * fd_x

    # 解析表达式（逐步）
    # D_x^2 f.g 的解析值 = 2 cF cG (S^2) E^2 + (cF+cG) S^2 E
    an_x2 = 2 * cF * cG * S ** 2 * E ** 2 + (cF + cG) * S ** 2 * E
    an_t = (cF - cG) * R * E
    an_x = (cF - cG) * S * E
    B_an = an_x2 + an_t + 2 * a * an_x

    # 我先前的手推公式
    hand = 2 * cF * cG * S * E ** 2 * (S - 2 * a) + (cF + cG) * E * (S ** 2 + R - 4 * a * S)
    hand2 = (cF + cG) * E * (S ** 2 + R + 2 * a * S)

    print("  点=(%s,%s,%s) E=%s" % (mp.nstr(X0, 4), mp.nstr(T0, 4), mp.nstr(Y0, 4),
                                    mp.nstr(E, 8)))
    print("    D_x^2 差分=%s  解析=%s  差=%s"
          % (mp.nstr(fd_x2, 10), mp.nstr(an_x2, 10), mp.nstr(fd_x2 - an_x2, 4)))
    print("    D_t   差分=%s  解析=%s  差=%s"
          % (mp.nstr(fd_t, 10), mp.nstr(an_t, 10), mp.nstr(fd_t - an_t, 4)))
    print("    2aD_x 差分=%s  解析=%s  差=%s"
          % (mp.nstr(2 * a * fd_x, 10), mp.nstr(2 * a * an_x, 10),
             mp.nstr(2 * a * (fd_x - an_x), 4)))
    print("    B_a   差分=%s  解析=%s" % (mp.nstr(B_fd, 10), mp.nstr(B_an, 10)))
    print("    手推式1=%s   手推式2=%s" % (mp.nstr(hand, 10), mp.nstr(hand2, 10)))
    print("    2cFcG S E^2 (S-2a) = %s ;  (cF+cG)E(S^2+R-4aS) = %s"
          % (mp.nstr(2 * cF * cG * S * E ** 2 * (S - 2 * a), 10),
             mp.nstr((cF + cG) * E * (S ** 2 + R - 4 * a * S), 10)))
    print("    cF+cG=%s  S^2+R-4aS=%s  S^2+R+2aS=%s"
          % (mp.nstr(cF + cG, 8), mp.nstr(S ** 2 + R - 4 * a * S, 8),
             mp.nstr(S ** 2 + R + 2 * a * S, 8)))
    print()


go(mp.mpf(4), mp.mpf(2) / 3, mp.mpf(-18) / 5, mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3)
go(mp.mpf(-2), mp.mpf(1), mp.mpf(-2), mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3)
