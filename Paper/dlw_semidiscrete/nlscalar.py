# -*- coding: utf-8 -*-
"""
nlscalar.py -- 用**标量 tau** + 高精度 Richardson 数值微分核对非线性层的全部关系。

tau 由 jet3.tau3 的字典在给定点求值得到（精确到机器精度），
所有关于 (x,t,y) 的导数用 mpmath 的高阶差分（步长按 ~1e-6 量级，中心差分 + Richardson）。

核对：
  (7)_h = (6)_h = 0
  (I)  = Psi_xx + 2 theta_x Psi_x + theta_t + 2(a-d) theta_x = 0
  (II) = Phi_xx + 2 Theta_x Phi_x + Theta_t + 2(a+d) Theta_x = 0
  v - 2*(Psi_{j+1}-Psi_{j-1})_x/(2h)  等等
"""
import mpmath as mp

import jet3

mp.mp.dps = 80

X0 = mp.mpf(1) / 5
T0 = mp.mpf(2) / 7
Y0 = mp.mpf(0)
EPS = mp.mpf('1e-8')


def Fd(N, a, p, q, h, j):
    d = h / 2
    return jet3.tau3(N, a, p, q, h, 1, a - d, a, j)


def Gd(N, a, p, q, h, j):
    d = h / 2
    return jet3.tau3(N, a, p, q, h, 0, a, a, j)


def T(d, x=None, t=None, y=None):
    return jet3.ev(d, X0 if x is None else x, T0 if t is None else t, Y0 if y is None else y)


def D1(f, var, e=EPS):
    if var == 'x':
        return (f(X0 + e, T0, Y0) - f(X0 - e, T0, Y0)) / (2 * e)
    if var == 't':
        return (f(X0, T0 + e, Y0) - f(X0, T0 - e, Y0)) / (2 * e)
    return (f(X0, T0, Y0 + e) - f(X0, T0, Y0 - e)) / (2 * e)


def D2(f, var, e=EPS):
    if var == 'x':
        return (f(X0 + e, T0, Y0) - 2 * f(X0, T0, Y0) + f(X0 - e, T0, Y0)) / e ** 2
    if var == 't':
        return (f(X0, T0 + e, Y0) - 2 * f(X0, T0, Y0) + f(X0, T0 - e, Y0)) / e ** 2
    return (f(X0, T0, Y0 + e) - 2 * f(X0, T0, Y0) + f(X0, T0, Y0 - e)) / e ** 2


def Lfun(d):
    """返回 f(x,t,y) = ln tau 的函数。"""
    def f(x, t, y):
        v = jet3.ev(d, x, t, y)
        return mp.log(abs(v))
    return f


def run(N, a, p, q, h, j0):
    print("=" * 96)
    print("N=%d a=%s p=%s q=%s h=%s j=%d" % (N, mp.nstr(a, 6), [mp.nstr(z, 5) for z in p],
                                             [mp.nstr(z, 5) for z in q], mp.nstr(h, 5), j0))
    print("=" * 96)
    F, G, G1 = Fd(N, a, p, q, h, j0), Gd(N, a, p, q, h, j0), Gd(N, a, p, q, h, j0 + 1)
    aF, aG, aG1 = Lfun(F), Lfun(G), Lfun(G1)

    # 势函数
    th = lambda mx=0, mt=0: (D1(aF, 'x') - D1(aG, 'x')) if (mx, mt) == (1, 0) else None
    def TH(mx=0, mt=0):
        if (mx, mt) == (0, 0):
            return aF(X0, T0, Y0) - aG1(X0, T0, Y0)
        if (mx, mt) == (1, 0):
            return D1(aF, 'x') - D1(aG1, 'x')
        if (mx, mt) == (0, 1):
            return D1(aF, 't') - D1(aG1, 't')
        if (mx, mt) == (2, 0):
            return D2(aF, 'x') - D2(aG1, 'x')

    def PS(mx=0, mt=0):
        if (mx, mt) == (1, 0):
            return D1(aF, 'x') + D1(aG, 'x')
        if (mx, mt) == (2, 0):
            return D2(aF, 'x') + D2(aG, 'x')

    def THI(mx=0, mt=0):
        if (mx, mt) == (0, 0):
            return aF(X0, T0, Y0) - aG(X0, T0, Y0)
        if (mx, mt) == (1, 0):
            return D1(aF, 'x') - D1(aG, 'x')
        if (mx, mt) == (0, 1):
            return D1(aF, 't') - D1(aG, 't')

    def PHI():
        return aF(X0, T0, Y0) + aG1(X0, T0, Y0)

    def PHI2():
        return D2(aF, 'x') + D2(aG1, 'x')

    def PHIx():
        return D1(aF, 'x') + D1(aG1, 'x')

    t0 = lambda: aF(X0, T0, Y0) - aG(X0, T0, Y0)
    tx = lambda: D1(aF, 'x') - D1(aG, 'x')
    tt = lambda: D1(aF, 't') - D1(aG, 't')
    Psx = lambda: D1(aF, 'x') + D1(aG, 'x')
    Psxx = lambda: D2(aF, 'x') + D2(aG, 'x')
    Thx = lambda: D1(aF, 'x') - D1(aG1, 'x')
    Tht = lambda: D1(aF, 't') - D1(aG1, 't')
    Phx = lambda: D1(aF, 'x') + D1(aG1, 'x')
    Phxx = lambda: D2(aF, 'x') + D2(aG1, 'x')

    d = h / 2
    rI = Psxx() + 2 * tx() * Psx() + tt() + 2 * (a - d) * tx()
    rII = Phxx() + 2 * Thx() * Phx() + Tht() + 2 * (a + d) * Thx()
    print("  (I)  = %.4e" % float(abs(rI)))
    print("  (II) = %.4e" % float(abs(rII)))

    # 物理变量（在格点上）
    def u_at(j):
        return 2 * (D1(Lfun(Fd(N, a, p, q, h, j)), 'x') - D1(Lfun(Gd(N, a, p, q, h, j)), 'x'))

    def w_at(j):
        return 2 * (D1(Lfun(Fd(N, a, p, q, h, j)), 'x') + D1(Lfun(Gd(N, a, p, q, h, j)), 'x'))

    def v_at(j):
        Psp = Lfun(Fd(N, a, p, q, h, j + 1))
        Psm = Lfun(Fd(N, a, p, q, h, j - 1))

        def Pp(x, t, y):
            return Psp(x, t, y) + Lfun(Gd(N, a, p, q, h, j + 1))(x, t, y)

        def Pm(x, t, y):
            return Psm(x, t, y) + Lfun(Gd(N, a, p, q, h, j - 1))(x, t, y)
        return (D1(Pp, 'x') - D1(Pm, 'x')) / h

    print("  u_j = %s   w_j = %s   v_j = %s" % (mp.nstr(u_at(j0), 8), mp.nstr(w_at(j0), 8),
                                                 mp.nstr(v_at(j0), 8)))
    print("  [lat] w_{j+1}-w_j-h u_x = %.4e" % float(abs(w_at(j0 + 1) - w_at(j0) - h * 2 * tx())))
    print("  [lat] v_j - w_{j+1} - h u_x = %.4e" % float(abs(v_at(j0) - w_at(j0 + 1) - h * 2 * tx())))
    print("  [lat] v_j - 2*(w_{j+1}-w_{j-1})/(2h) = %.4e"
          % float(abs(v_at(j0) - (w_at(j0 + 1) - w_at(j0 - 1)) / h)))


if __name__ == '__main__':
    for (N, a, p, q, h) in [
        (1, mp.mpf(4), [mp.mpf(2) / 3], [mp.mpf(-18) / 5], mp.mpf(1) / 4),
        (1, mp.mpf(-2), [mp.mpf(1)], [mp.mpf(-2)], mp.mpf(1) / 4),
    ]:
        for j0 in (0, 1):
            run(N, a, p, q, h, j0)
