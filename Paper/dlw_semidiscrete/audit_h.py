# -*- coding: utf-8 -*-
"""
audit_h.py -- (7)_h, (6)_h 残差的真实量级与 h 标度（多点取值，不用单点）。

结论若残差 ~ C*h 则它不是恒等式，而是一个 O(h) 的离散化误差。
"""
import mpmath as mp

import jet3

mp.mp.dps = 120
a = mp.mpf(4)
p = [mp.mpf(2) / 3]
q = [mp.mpf(-18) / 5]
PT = (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3)


def ev(d, x0, t0, y0):
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


print("a=4, p=2/3, q=-18/5,  j=1,  点 (x,t,y)=(1/5, 2/7, 1/3)")
print("%-8s %-26s %-14s %-26s %-14s" % ("h", "(7)_h 残差", "比值", "(6)_h 残差", "比值"))
prev7 = prev6 = None
for k in range(1, 7):
    h = mp.mpf(1) / 2 ** k
    d = h / 2
    F = jet3.tau3(1, a, p, q, h, 1, a - d, a, 1)
    G = jet3.tau3(1, a, p, q, h, 0, a, a, 1)
    G1 = jet3.tau3(1, a, p, q, h, 0, a, a, 2)
    r7 = ev(jet3.Bs3(F, G, a - d), *PT)
    r6 = ev(jet3.Bs3(F, G1, a + d), *PT)
    # 相对尺度
    sc = max(abs(ev(jet3.deriv(F, mx, mt), *PT))
             for mx in range(3) for mt in range(2))
    print("%-8s %-26s %-14s %-26s %-14s"
          % (mp.nstr(h, 6), mp.nstr(abs(r7), 8),
             ("-" if prev7 is None else mp.nstr(abs(r7) / abs(prev7), 5)),
             mp.nstr(abs(r6), 8),
             ("-" if prev6 is None else mp.nstr(abs(r6) / abs(prev6), 5))))
    prev7, prev6 = r7, r6

print()
print("对照：连续 (7) B_a f.g 在同一点的残差")
d = mp.mpf(0)
F = jet3.tau3(1, a, p, q, None, 1, a, a, 0)
G = jet3.tau3(1, a, p, q, None, 0, a, a, 0)
print("   h=0 (连续):", mp.nstr(abs(ev(jet3.Bs3(F, G, a), *PT)), 8))
