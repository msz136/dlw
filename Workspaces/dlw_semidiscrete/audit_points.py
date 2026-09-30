# -*- coding: utf-8 -*-
"""
audit_points.py -- 多点 / 多参数体检：把每个"已证"恒等式在**多个独立随机点**上算，
看它是恒零还是只在某一点碰巧为零。用 mpmath 高精度 + 自适应精度倍增。

用法：对每个 (等式, 参数组) 输出 |残差| 在多点上的最大值与相对尺度。
恒等式应当在**所有**点都达到精度地板；若只在个别点为 0，则打印反例点。
"""
import mpmath as mp

import jet3

mp.mp.dps = 120

POINTS = [
    (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(0)),
    (mp.mpf(1) / 5, mp.mpf(2) / 7, mp.mpf(1) / 3),
    (mp.mpf(1) / 3, mp.mpf(1) / 5, mp.mpf(1) / 7),
    (mp.mpf(2) / 9, mp.mpf(3) / 11, mp.mpf(-5) / 13),
    (mp.mpf('1.234'), mp.mpf('0.567'), mp.mpf('0.891')),
    (mp.mpf('-0.721'), mp.mpf('2.113'), mp.mpf('-1.417')),
]

CASES = [
    (mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4),
    (mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)], mp.mpf(1) / 4),
    (mp.mpf(5) / 3, [mp.mpf(1) / 5], [mp.mpf(-1)], mp.mpf(1) / 8),
]


def ev(d, x0, t0, y0):
    return sum(v * mp.e ** (k[0] * x0 + k[1] * t0 + k[2] * y0) for k, v in d.items())


def deriv(d, mx=0, mt=0, my=0):
    return jet3.deriv(d, mx, mt, my)


def scale_of(d, x0, t0, y0):
    return max(abs(ev(deriv(d, mx, mt, my), x0, t0, y0))
               for mx in range(3) for mt in range(2) for my in range(2))


def run():
    for (a, p, q, h) in CASES:
        d = h / 2
        print("=" * 76)
        print("a=%s h=%s" % (mp.nstr(a, 6), mp.nstr(h, 5)))
        for j in (0, 1, 2):
            F = jet3.tau3(1, a, p, q, h, 1, a - d, a, j)
            G = jet3.tau3(1, a, p, q, h, 0, a, a, j)
            G1 = jet3.tau3(1, a, p, q, h, 0, a, a, j + 1)
            tests = {
                '(7)_h = B_{a-d}F_j.G_j': lambda x0, t0, y0:
                    ev(jet3.Bs3(F, G, a - d), x0, t0, y0),
                '(6)_h = B_{a+d}F_j.G_{j+1}': lambda x0, t0, y0:
                    ev(jet3.Bs3(F, G1, a + d), x0, t0, y0),
            }
            for name, fn in tests.items():
                vals = []
                for (x0, t0, y0) in POINTS:
                    sc = max(scale_of(F, x0, t0, y0), scale_of(G, x0, t0, y0), mp.mpf(1))
                    vals.append(abs(fn(x0, t0, y0)) / sc)
                mx = max(vals)
                tag = 'ALL ZERO (相对 ~1e-%d)' % int(-mp.log10(mx)) if mx < mp.mpf('1e-40') \
                    else 'NOT IDENTICALLY ZERO  max_rel=%.6g' % mx
                print("  j=%d  %-28s %s" % (j, name, tag))
                if mx >= mp.mpf('1e-40'):
                    for (x0, t0, y0), v in zip(POINTS, vals):
                        if v > mp.mpf('1e-40'):
                            print("        反例点 (x,t,y)=(%s,%s,%s) 相对残差=%s"
                                  % (mp.nstr(x0, 4), mp.nstr(t0, 4), mp.nstr(y0, 4),
                                     mp.nstr(v, 6)))
                            break
        print()


if __name__ == '__main__':
    run()
