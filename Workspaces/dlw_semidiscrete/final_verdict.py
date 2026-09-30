# -*- coding: utf-8 -*-
"""
final_verdict.py -- 最终判定：B_a(F,G) 到底是 0 还是非 0？

用 jet4 的精确字典算 B_a(F,G)，打印所有项，再在测试点上高精度求值。
如果字典非空，则 (7) 不成立，其值为多少一目了然。
"""
from fractions import Fraction as Fr

import mpmath as mp

import jet4 as J

mp.mp.dps = 60
a, p, q = Fr(4), [Fr(2, 3)], [Fr(-18, 5)]
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3

# 连续情形 h=0, s = mu = a
F = J.tau3(1, a, p, q, Fr(0), 1, a, a, 0)
G = J.tau3(1, a, p, q, Fr(0), 0, a, a, 0)
print("F =", [(tuple(str(x) for x in k), str(v)) for k, v in F.items()])
print("G =", [(tuple(str(x) for x in k), str(v)) for k, v in G.items()])
print()

d2 = J.bilin(F, G, 2, 0)
dt = J.bilin(F, G, 0, 1)
dx = J.bilin(F, G, 1, 0)
B = J.add(J.add(d2, dt), J.scale(dx, 2 * a))

for nm, dd in (("D_x^2 F.G", d2), ("D_t F.G", dt), ("2a D_x F.G", J.scale(dx, 2 * a)),
               ("B_a(F,G)", B)):
    print("%-14s 项数=%d" % (nm, len(dd)))
    for k, v in dd.items():
        print("      key=%s   coef=%s" % (tuple(str(x) for x in k), v))


def ev(dd, x0, t0, y0):
    tot = mp.mpf(0)
    for k, v in dd.items():
        tot += mp.mpf(v.numerator) / v.denominator \
            * mp.e ** (mp.mpf(k[0].numerator) / k[0].denominator * x0
                       + mp.mpf(k[1].numerator) / k[1].denominator * t0
                       + mp.mpf(k[2].numerator) / k[2].denominator * y0)
    return tot


print()
print("在测试点求值：")
print("  D_x^2 F.G   =", mp.nstr(ev(d2, X0, T0, Y0), 12))
print("  D_t   F.G   =", mp.nstr(ev(dt, X0, T0, Y0), 12))
print("  2a D_x F.G  =", mp.nstr(ev(J.scale(dx, 2 * a), X0, T0, Y0), 12))
print("  B_a(F,G)    =", mp.nstr(ev(B, X0, T0, Y0), 12))
print()
print("对照：解析公式 B_a = (cF+cG)S^2 E + (cF-cG)(R+2aS)E + 2cFcG S(S-4a)E^2")
S = p[0] + q[0]
R = q[0] ** 2 - p[0] ** 2
cF = (-(p[0] - a) / (q[0] + a)) / (p[0] + q[0])
cG = 1 / (p[0] + q[0])
E = ev({(S, R, 1 / (p[0] - a) + 1 / (q[0] + a)): Fr(1)}, X0, T0, Y0)
print("  S=%s R=%s cF=%s cG=%s" % (S, R, cF, cG))
print("  E =", mp.nstr(E, 10))
print("  [E]   =", (cF + cG) * S ** 2 + (cF - cG) * (R + 2 * a * S))
print("  [E^2] =", 2 * cF * cG * S * (S - 4 * a))
print("  解析值 =",
      mp.nstr(mp.mpf(((cF + cG) * S ** 2 + (cF - cG) * (R + 2 * a * S)).numerator)
              / ((cF + cG) * S ** 2 + (cF - cG) * (R + 2 * a * S)).denominator * E
              + mp.mpf((2 * cF * cG * S * (S - 4 * a)).numerator)
              / (2 * cF * cG * S * (S - 4 * a)).denominator * E ** 2, 12))
