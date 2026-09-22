# -*- coding: utf-8 -*-
"""
nlstep3.py --  半离散非线性 DLW 系统的闭合性：精确诊断（修正版）。

关键的认识（本脚本要验证的）：

  1. 所有方程都自然生活在**半整数交错格**上：
       F_j  在  j+1/2
       G_j  在  j
       物理方程 (N1) 其实是半整数格点上的方程（(N2) 是整数格点上的）。

  2. 位移算子
       mu_j f := (f_{j+1} + f_j)/2          (半整数格点上的平均)
       sum_j f := (f_{j+1} + 2 f_j + f_{j-1})/4   ( = (mu_j + mu_{j-1})/2 )
     满足  mu_j - mu_{j-1} = (h/2) * delta_j,  delta_j := (f_{j+1}-f_{j-1})/h .
     于是 v_j := (2/h)(mu_j - mu_{j-1}) Psi_j = 2 delta_j Psi_j.

  3. 严格恒等式：  u_{j,t} = v_j - w_j + h sum_j[u] R'_w ,   w_j := 2 Psi_{j,x}
     （由 (N1) 与 (N2) 线性组合，逐项可验，对有限 h 精确）

  4. 消去 w 的连续极限：  w_j = v_j - u_{j,y} ,  u_{j,y} := (mu_j - mu_{j-1})u / (h/2)
"""

import sympy as sp
from dlwcommon import Lattice, Cont, DEFAULT
from dlwcommon2 import hard_simplify, is_zero_exact, ev

X0 = sp.Rational(1, 5)
T0 = sp.Rational(2, 7)
A = sp.Rational(3, 2)
VALS1 = {'p1': DEFAULT['p1'], 'q1': DEFAULT['q1']}
VALS2 = {'p1': DEFAULT['p1'], 'q1': DEFAULT['q1'], 'p2': DEFAULT['p2'], 'q2': DEFAULT['q2']}


# ---------------------------------------------------------------- 基本对象
def w_exact(M, j):
    """w_j = 2 Psi_{j,x}"""
    return 2 * sp.diff(M.Psi(j), M.x)


def delta(M, j, f):
    """delta_j f = (f_{j+1}-f_{j-1})/h"""
    return (f(M, j + 1) - f(M, j - 1)) / M.h


def mu(M, j, f):
    return (f(M, j + 1) + f(M, j)) / 2


def mu_lag(M, j, f):
    return (f(M, j) + f(M, j - 1)) / 2


def sum_op(M, j, f):
    """sum_j f = (f_{j+1}+2f_j+f_{j-1})/4"""
    return (f(M, j + 1) + 2 * f(M, j) + f(M, j - 1)) / 4


def v_of(M, j):
    """v_j = 2 delta_j Psi  (= (2/h)(mu_j - mu_{j-1}) Psi)"""
    return 2 * delta(M, j, lambda M, k: M.Psi(k))


def uy_disc(M, j):
    """u_{j,y} 的离散写法 = (2/h)(mu_j - mu_{j-1}) u = delta_j u"""
    return delta(M, j, lambda M, k: M.u(k))


def Rp_u(M, j):
    """R'_u = (N1)_x"""
    return sp.diff(M.res_N1(j), M.x)


def Rp_w(M, j):
    """R'_w = (N2)_x + (N1)_x"""
    return sp.diff(M.res_N2(j), M.x) + sp.diff(M.res_N1(j), M.x)


# ---------------------------------------------------------------- 诊断主体
def scan(name, build, hs, M_fn, x0=X0, t0=T0):
    vals = []
    for h in hs:
        M = M_fn(h)
        vals.append(ev(build(M), M, x0, t0))
    line = "  %-42s :" % name
    for v in vals:
        line += " %12.5e" % float(sp.N(abs(v), 20))
    print(line)
    for k in range(1, len(vals)):
        if vals[k] != 0 and vals[k - 1] != 0:
            r = sp.N(vals[k - 1] / vals[k], 10)
            print("  %-42s   ratio -> %s" % ('', r))
    return vals


def main():
    hs = [sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 16)]

    for N, VALS in [(1, VALS1), (2, VALS2)]:
        print("=" * 90)
        print("N = %d" % N)
        print("=" * 90)

        print("\n[1] 严格恒等式  u_t = v - w + h*sum_j[u] R'_w   (有限 h 精确)")
        for j in [1]:
            scan("N=%d j=%d" % (N, j),
                 lambda M, j=j: sp.diff(M.u(j), M.t)
                 - (v_of(M, j) - w_exact(M, j) + M.h * sum_op(M, j, lambda M, k: M.u(k)) * Rp_w(M, j)),
                 hs, lambda h: Lattice(N, VALS, h, A))

        print("\n[2] w 的连续化：w_j - (v_j - u_{j,y})  应为 O(h^2)")
        for j in [1]:
            scan("N=%d j=%d" % (N, j),
                 lambda M, j=j: w_exact(M, j) - (v_of(M, j) - uy_disc(M, j)),
                 hs, lambda h: Lattice(N, VALS, h, A))

        print("\n[3] 闭合系统残差：把 w 用 w_disc := v - u_{j,y} 代替后的 (A) 残差 应为 O(h^2)")
        for j in [1]:
            def b(M, j=j):
                wd = v_of(M, j) - uy_disc(M, j)
                lhs = sp.diff(M.u(j), M.t)
                rhs = v_of(M, j) - wd + M.d * (M.u(j) - wd) + 2 * M.d * sp.diff(M.u(j), M.x)
                return lhs - rhs
            scan("N=%d j=%d" % (N, j), b, hs, lambda h: Lattice(N, VALS, h, A))

        print("\n[4] 闭合系统残差：把 w 用 v - u_{j,y} 代替后的 (B) 残差 应为 O(h^2)")
        for j in [1]:
            def b(M, j=j):
                wd = v_of(M, j) - uy_disc(M, j)
                # (B) : w_t + sum[u]R'_w = 0 ，其中 w 换成 wd
                return sp.diff(wd, M.t) + sum_op(M, j, lambda M, k: M.u(k)) * Rp_w(M, j)
            scan("N=%d j=%d" % (N, j), b, hs, lambda h: Lattice(N, VALS, h, A))

        print("\n[5] v 的连续极限： v_j vs 2(ln fg)_{xy}|_{Y=(j+1/2)h}  应为 O(h^2)")
        for j in [1]:
            def b(M, j=j):
                MC = Cont(N, VALS, M.h, A)
                y0 = (j + sp.Rational(1, 2)) * M.h
                return v_of(M, j) - 2 * sp.diff(MC.Psi(y0), MC.x, sp.Symbol('yy'))
            # 直接构造连续 v
            def b2(M, j=j):
                MC = Cont(N, VALS, M.h, A)
                yy = sp.Symbol('yy', real=True)
                Psi_c = sp.log(MC.F(yy) * MC.G(yy))
                y0 = (j + sp.Rational(1, 2)) * M.h
                vc = sp.diff(Psi_c, MC.x, yy).subs(yy, y0)
                return v_of(M, j) - 2 * vc
            scan("N=%d j=%d" % (N, j), b2, hs, lambda h: Lattice(N, VALS, h, A))

        print("\n[6] u 的连续极限： u_j vs 2(ln f/g)_x|_{Y=(j+1/2)h}  应为 O(h^2)")
        for j in [1]:
            def b(M, j=j):
                MC = Cont(N, VALS, M.h, A)
                yy = sp.Symbol('yy', real=True)
                th_c = sp.log(MC.F(yy) / MC.G(yy))
                y0 = (j + sp.Rational(1, 2)) * M.h
                uc = sp.diff(th_c, MC.x).subs(yy, y0)
                return M.u(j) - 2 * uc
            scan("N=%d j=%d" % (N, j), b, hs, lambda h: Lattice(N, VALS, h, A))

        print()


if __name__ == '__main__':
    main()
