# -*- coding: utf-8 -*-
"""
jet2.py -- 双变量（x,t）截断泰勒 jet。

    J = sum_{m<=MX, n<=MT} a[m][n] u^m v^n ,   u = x - x0,  v = t - t0

为什么需要双变量：DLW 的 tau 不满足热方程（相位是 (p+q)x + (q^2-p^2)t，
一般 (p+q)^2 != q^2-p^2），所以 d/dt 不能写成 d_x^2。必须对 x 与 t 各自展开。
"""

import mpmath as mp

MX = 6      # x 方向阶数
MT = 3      # t 方向阶数


class J2:
    """截断到 (MX, MT) 的双变量 jet。表示是**唯一规范化**的：
    永远是 (MX+1) x (MT+1) 的复数矩阵。"""
    __slots__ = ('a',)

    def __init__(self, a):
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        for i, row in enumerate(a):
            if i > MX:
                break
            for j, v in enumerate(row):
                if j > MT:
                    break
                out[i][j] = mp.mpc(v)
        self.a = out

    # ---------------------------------------------------------------- 构造
    @staticmethod
    def const(c):
        return J2([[c]])

    @staticmethod
    def var_x():
        return J2([[0, 0], [1, 0]])

    @staticmethod
    def var_t():
        return J2([[0, 1]])

    def coef(self, m, n):
        if 0 <= m <= MX and 0 <= n <= MT:
            return self.a[m][n]
        return mp.mpc(0)

    def maxabs(self):
        return max(abs(v) for row in self.a for v in row)

    # ---------------------------------------------------------------- 算术
    def __add__(self, o):
        o = o if isinstance(o, J2) else J2.const(o)
        return J2([[self.a[i][j] + o.a[i][j] for j in range(MT + 1)]
                   for i in range(MX + 1)])

    __radd__ = __add__

    def __neg__(self):
        return J2([[-v for v in row] for row in self.a])

    def __sub__(self, o):
        return self + (-(o if isinstance(o, J2) else J2.const(o)))

    def __rsub__(self, o):
        return J2.const(o) + (-self)

    def __mul__(self, o):
        o = o if isinstance(o, J2) else J2.const(o)
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        A, B = self.a, o.a
        for i in range(MX + 1):
            for j in range(MT + 1):
                va = A[i][j]
                if va == 0:
                    continue
                for k in range(MX + 1 - i):
                    for l in range(MT + 1 - j):
                        vb = B[k][l]
                        if vb != 0:
                            out[i + k][j + l] += va * vb
        return J2(out)

    __rmul__ = __mul__

    def inv(self):
        """1/J（常数项非零）"""
        a0 = self.a[0][0]
        if a0 == 0:
            raise ZeroDivisionError('J2 with zero constant term')
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        out[0][0] = 1 / a0
        for m in range(MX + 1):
            for n in range(MT + 1):
                if m == 0 and n == 0:
                    continue
                s = mp.mpc(0)
                for i in range(m + 1):
                    for j in range(n + 1):
                        if i == 0 and j == 0:
                            continue
                        if i == m and j == n:
                            continue
                        s += self.a[i][j] * out[m - i][n - j]
                out[m][n] = -(s + self.a[m][n] * out[0][0]) / a0
        return J2(out)

    def __truediv__(self, o):
        return self * (o if isinstance(o, J2) else J2.const(o)).inv()

    def __pow__(self, n):
        r = J2.const(1)
        for _ in range(abs(int(n))):
            r = r * self
        return r if n >= 0 else J2.const(1) / r

    def exp(self):
        """exp(J)"""
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        pw = J2.const(1)
        for n in range(0, MX + MT + 3):
            for i in range(MX + 1):
                for j in range(MT + 1):
                    out[i][j] += pw.a[i][j] / mp.factorial(n)
            pw = pw * self
        return J2(out)

    def log(self):
        """ln J ：用 dL = dJ/J 逐项积分。"""
        a0 = self.a[0][0]
        if a0 == 0:
            raise ValueError('ln of J2 with zero constant term')
        inv = self.inv()
        Lx = self.dx() * inv
        Lt = self.dt() * inv
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        out[0][0] = mp.log(a0)
        for m in range(MX + 1):
            for n in range(MT + 1):
                if m == 0 and n == 0:
                    continue
                if m >= 1:
                    out[m][n] = Lx.coef(m - 1, n) / m
                else:
                    out[m][n] = Lt.coef(m, n - 1) / n
        return J2(out)

    # -------------------------------------------------------------- 导数
    def dx(self):
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        for m in range(MX):
            for n in range(MT + 1):
                out[m][n] = (m + 1) * self.a[m + 1][n]
        return J2(out)

    def dt(self):
        out = [[mp.mpc(0)] * (MT + 1) for _ in range(MX + 1)]
        for m in range(MX + 1):
            for n in range(MT):
                out[m][n] = (n + 1) * self.a[m][n + 1]
        return J2(out)

    def dxn(self, n):
        r = self
        for _ in range(n):
            r = r.dx()
        return r

    def dtn(self, n):
        r = self
        for _ in range(n):
            r = r.dt()
        return r

    # ------------------------------------------------------------ 数值检验
    def ev(self, u=0, v=0):
        s = mp.mpc(0)
        for m in range(MX + 1):
            for n in range(MT + 1):
                s += self.a[m][n] * mp.mpf(u) ** m * mp.mpf(v) ** n
        return s


def jmax(j):
    return j.maxabs()
