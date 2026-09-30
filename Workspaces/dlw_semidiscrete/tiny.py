# -*- coding: utf-8 -*-
"""
tiny.py -- 最小复现：手算 D_x^2(f,g)，与有限差分对照。
"""
import mpmath as mp

mp.mp.dps = 60
a = mp.mpf(4)
p = mp.mpf(2) / 3
q = mp.mpf(-18) / 5
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3

S = p + q
R = q ** 2 - p ** 2
T = 1 / (q + a) + 1 / (p - a)
cF = (-(p - a) / (q + a)) / (p + q)
cG = 1 / (p + q)
E = mp.e ** (S * X0 + R * T0 + T * Y0)

f = lambda x, t, y: 1 + cF * mp.e ** (S * x + R * t + T * y)
g = lambda x, t, y: 1 + cG * mp.e ** (S * x + R * t + T * y)

print("S=%s  cF=%s  cG=%s  E=%s" % (mp.nstr(S, 10), mp.nstr(cF, 10),
                                    mp.nstr(cG, 10), mp.nstr(E, 10)))
print("cF*E = %s   cG*E = %s   1+cF*E = %s" % (mp.nstr(cF * E, 10),
                                               mp.nstr(cG * E, 10),
                                               mp.nstr(1 + cF * E, 10)))
print()
for h in [mp.mpf('1e-3'), mp.mpf('1e-4'), mp.mpf('1e-5'), mp.mpf('1e-6')]:
    F0, G0 = f(X0, T0, Y0), g(X0, T0, Y0)
    Fx = (f(X0 + h, T0, Y0) - f(X0 - h, T0, Y0)) / (2 * h)
    Gx = (g(X0 + h, T0, Y0) - g(X0 - h, T0, Y0)) / (2 * h)
    Fxx = (f(X0 + h, T0, Y0) - 2 * F0 + f(X0 - h, T0, Y0)) / h ** 2
    Gxx = (g(X0 + h, T0, Y0) - 2 * G0 + g(X0 - h, T0, Y0)) / h ** 2
    dx2 = Fxx * G0 - 2 * Fx * Gx + F0 * Gxx
    print("h=%-8s  Fxx=%s  G0=%s  Fxx*G0=%s" %
          (mp.nstr(h, 4), mp.nstr(Fxx, 12), mp.nstr(G0, 12), mp.nstr(Fxx * G0, 12)))
    print("           -2Fx Gx=%s   F0 Gxx=%s   D_x^2=%s"
          % (mp.nstr(-2 * Fx * Gx, 12), mp.nstr(F0 * Gxx, 12), mp.nstr(dx2, 12)))
print()
F0, G0 = f(X0, T0, Y0), g(X0, T0, Y0)
an = 2 * cF * cG * S ** 2 * E ** 2 + (cF + cG) * S ** 2 * E
print("解析 D_x^2 = 2 cF cG S^2 E^2 + (cF+cG)S^2 E")
print("   2cFcG S^2 E^2 = %s" % mp.nstr(2 * cF * cG * S ** 2 * E ** 2, 12))
print("   (cF+cG)S^2 E   = %s" % mp.nstr((cF + cG) * S ** 2 * E, 12))
print("   合计           = %s" % mp.nstr(an, 12))
print()
print("手算 Fxx = cF S^2 E :", mp.nstr(cF * S ** 2 * E, 12))
print("手算 Gxx = cG S^2 E :", mp.nstr(cG * S ** 2 * E, 12))
print("手算 Fxx*G0 = cF S^2 E + cF cG S^2 E^2 :",
      mp.nstr(cF * S ** 2 * E + cF * cG * S ** 2 * E ** 2, 12))
print("手算 F0*Gxx = cG S^2 E + cF cG S^2 E^2 :",
      mp.nstr(cG * S ** 2 * E + cF * cG * S ** 2 * E ** 2, 12))
print("手算 -2 Fx Gx = -2 cF cG S^2 E^2 :", mp.nstr(-2 * cF * cG * S ** 2 * E ** 2, 12))
