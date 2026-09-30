# -*- coding: utf-8 -*-
"""
exact7b.py -- 用 exact7.py 得到的闭式，在数值上确认 B_a(F,G) 不为零。

闭式（sympy 导出）：
    B_a(F,G) = E * [ (cF+cG)(S^2+R+2aS) - 8a cF cG S E ]
其中 E = exp(Sx+Rt+Ty)。
（注：E^2 项来自 cF cG，因为 F,G 共用同一个 E。）
"""
import mpmath as mp

mp.mp.dps = 50
X0, T0, Y0 = mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3

CASES = [(mp.mpf(4), mp.mpf(2) / 3, mp.mpf(-18) / 5),
         (mp.mpf(-2), mp.mpf(1), mp.mpf(-2)),
         (mp.mpf(5) / 3, mp.mpf(1) / 5, mp.mpf(-1))]

for (a, p, q) in CASES:
    S = p + q
    R = q ** 2 - p ** 2
    T = 1 / (q + a) + 1 / (p - a)
    cF = (-(p - a) / (q + a)) / (p + q)
    cG = 1 / (p + q)
    E = mp.e ** (S * X0 + R * T0 + T * Y0)
    cl = (cF + cG) * (S ** 2 + R + 2 * a * S)
    ce = 2 * cF * cG * S * (S - 4 * a)
    print("a=%-7s  [E]=%-16s [E^2]=%-16s E=%s"
          % (mp.nstr(a, 6), mp.nstr(cl, 10), mp.nstr(ce, 10), mp.nstr(E, 8)))
    print("        B_a(F,G) = E*[E] + E^2*[E^2] = %s"
          % mp.nstr(E * cl + E ** 2 * ce, 10))
    print("        若 1-孤子满足 (7)，此值应为 0。")
    print()
