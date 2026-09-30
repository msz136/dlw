# -*- coding: utf-8 -*-
"""
jet.py -- 高精度 jet（截断泰勒级数）算术，固定截断阶数。

对 DLW 的 tau 我们只用到两族导出量：
    (ln F_j)_x , (ln G_j)_x , (ln F_j)_{xx} , ...

关键：交错 Gram tau 在 (x,t) 方向满足 F_{xx} = F_t（热方程，逐元素成立，
因为 xi_i 与 eta_k 的 x 速率是 p_i,q_k 而 t 速率是 -p_i^2,+q_k^2）。
（注意：连续情形也有 tau_{xx}=tau_t 吗？—— 有，此时 xi 不含其它 x,t 依赖。
  但格点 tau 的 y 部分被 j 承担，同样成立。）
因此可只对 x 展开、把 d/dt 当作 d_x^2 作用 —— 只对本脚本诊断的 *连续解*
是正确的；脚本会对 (ln F)_t 做一致性审计。
（若要做"任意 u,v 构型"的验证，必须改用真实的二层 Taylor 展开。）

一个 jet 在基点 (x0,t0) 处表示  J = sum_k a_k u^k,  u = x - x0，
系数 a_k 是高精度数（t = t0 处求值）。
"""

import mpmath as mp

ORDER = 14


class Jet:
    __slots__ = ('a',)

    def __init__(self, a):
        a = [mp.mpc(x) for x in a][:ORDER + 1]
        self.a = a if a else [mp.mpc(0)]

    @staticmethod
    def const(c):
        return Jet([mp.mpc(c)])

    @staticmethod
    def var():
        return Jet([mp.mpc(0), mp.mpc(1)])

    # ---------------------------------------------------------------- 算术
    def __add__(self, o):
        o = o if isinstance(o, Jet) else Jet.const(o)
        n = max(len(self.a), len(o.a))
        return Jet([(self.a[i] if i < len(self.a) else 0) + (o.a[i] if i < len(o.a) else 0)
                    for i in range(n)])

    __radd__ = __add__

    def __neg__(self):
        return Jet([-v for v in self.a])

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Jet) else Jet.const(o)))

    def __rsub__(self, o):
        return Jet.const(o) + (-self)

    def __mul__(self, o):
        o = o if isinstance(o, Jet) else Jet.const(o)
        a = [mp.mpc(0)] * min(len(self.a) + len(o.a) - 1, ORDER + 1)
        for i, ai in enumerate(self.a):
            if ai == 0:
                continue
            for k, bk in enumerate(o.a):
                if i + k > ORDER:
                    break
                a[i + k] += ai * bk
        return Jet(a)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, Jet) else Jet.const(o)
        return self * o.inv()

    def __pow__(self, n):
        if isinstance(n, int):
            return self.pow_int(n)
        raise TypeError('Jet power must be an integer')

    def __rpow__(self, o):
        raise TypeError('reflected power unsupported')

    def inv(self):
        a0 = self.a[0]
        if a0 == 0:
            raise ZeroDivisionError('jet with zero constant term')
        b = [mp.mpc(0)] * min(len(self.a), ORDER + 1)
        b[0] = 1 / a0
        for n in range(1, len(b)):
            s = mp.mpc(0)
            for i in range(1, min(n, len(self.a) - 1) + 1):
                s += self.a[i] * b[n - i]
            b[n] = -s / a0
        return Jet(b)

    def log(self):
        """ln J —— 用 (ln J)' = J'/J 逐阶积分。允许复常数项（DLW 的 tau 可以变号）。"""
        a0 = self.a[0]
        if a0 == 0:
            raise ValueError('ln of jet with zero constant term')
        ld = self.dx() / self          # J'/J = sum c_m u^m
        out = [mp.log(a0)]
        for m in range(0, ORDER):
            out.append(ld.coef(m) / (m + 1))
        return Jet(out)

    def exp(self):
        """exp(J)"""
        acc = [mp.mpc(0)] * (ORDER + 1)
        pw = Jet.const(1)
        for n in range(0, ORDER + 1):
            for k in range(min(len(pw.a), ORDER + 1)):
                acc[k] += pw.a[k] / mp.factorial(n)
            pw = pw * self
        return Jet(acc)

    def pow_int(self, n):
        r = Jet.const(1)
        for _ in range(abs(int(n))):
            r = r * self
        return r if n >= 0 else Jet.const(1) / r

    # -------------------------------------------------------------- 微积分
    def dx(self):
        a = [(k + 1) * self.a[k + 1] for k in range(len(self.a) - 1)]
        return Jet(a if a else [mp.mpc(0)])

    def dxn(self, n):
        j = self
        for _ in range(n):
            j = j.dx()
        return j

    def dt(self):
        return self.dx().dx()

    def dtn(self, n):
        j = self
        for _ in range(n):
            j = j.dt()
        return j

    def dlog_x(self, n=1):
        return self.log().dxn(n)

    def coef(self, k):
        return self.a[k] if k < len(self.a) else mp.mpc(0)

    def is_zero(self, tol=None):
        if tol is None:
            tol = mp.mpf(10) ** (-(mp.mp.dps - 20))
        return all(abs(v) < tol for v in self.a)

