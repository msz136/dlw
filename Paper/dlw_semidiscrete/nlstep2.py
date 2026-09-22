# -*- coding: utf-8 -*-
"""
nlstep2.py --  DLW 半离散非线性层：闭合性诊断。

核心构造（全部记号见 dlwcommon.py）：

    alpha_j = ln F_j,   beta_j = ln G_j,   d = h/2
    u_j = 2 (alpha_j - beta_j)_x
    w_j = 2 (alpha_j + beta_j)_x          ( = 2 Psi_{j,x} )
    v_j = (1/(2h)) D_x [ (Psi_{j+1}-Psi_j) + (Psi_j-Psi_{j-1}) ]

(N1) 的精确等价形式：
    (A_exact)  u_{j,t} = v_j - w_j + 2d theta_{j,x} + 2d u_{j,x}
                其中 theta_{j,x} = (u_j - w_j)/2
    => (A)     u_{j,t} = v_j - w_j + d (u_j - w_j) + 2 d u_{j,x}

本脚本诊断：
  [C1] (A) 精确成立（代数恒等式，来自 (N1)）
  [C2] (N2)_x 与 (N1)_x 组合给出的 v 演化方程
  [C3] 把 w_j 用  w_j = v_j - u_{j,y} + O(h^2)  消去后的闭合系统残差阶数
  [C4] 各候选 v_j 定义的连续极限阶数
"""

import sympy as sp
from dlwcommon import Lattice, Cont, DEFAULT, at

x0 = sp.Rational(1, 5)
t0 = sp.Rational(2, 7)


# --------------------------------------------------------------------------
#  w 的离散替代：w_j  <=>  v_j - u_{j,y}
#  在格点上 u_{j,y} 的自然二阶写法：
#     (u_{j+1}-u_{j-1})/(2h)      (中心)
#     (u_{j+1}-u_j)/h             (前向)
#     (u_j-u_{j-1})/h             (后向)
#  或者用 v 的差分算子直接给出 w：
#     w_j = (v_j + v_{j-1})/2 + ... 见诊断
# --------------------------------------------------------------------------
def w_from_v_center(M, j):
    """w_j := v_j - (u_{j+1}-u_{j-1})/(2h)"""
    return M.v_mid(j) - (M.u(j + 1) - M.u(j - 1)) / (2 * M.h)


def w_from_v_fwd(M, j):
    return M.v_fwd(j) - (M.u(j + 1) - M.u(j)) / M.h


def w_from_v_bwd(M, j):
    return M.v_bwd(j) - (M.u(j) - M.u(j - 1)) / M.h


def main():
    N = 1
    a = sp.Rational(3, 2)
    vals = {'p1': DEFAULT['p1'], 'q1': DEFAULT['q1']}

    print("=" * 78)
    print("[C1]  (A)  u_t = v - w + d(u-w) + 2d u_x    是否精确成立")
    print("=" * 78)
    for h in [sp.Rational(1, 4), sp.Rational(1, 8)]:
        M = Lattice(N, vals, h, a)
        for j in [0, 1]:
            # w_j = 2 (alpha+beta)_x  (exact)
            wj = 2 * sp.diff(M.Psi(j), M.x)
            lhs = sp.diff(M.u(j), M.t)
            rhs = M.v_mid(j) - wj + M.d * (M.u(j) - wj) + 2 * M.d * sp.diff(M.u(j), M.x)
            print("  h=%-5s j=%d :  resid = %s" % (h, j, at(lhs - rhs, M, x0, t0)))

    print()
    print("=" * 78)
    print("[C2]  w 的三种离散替代 vs 精确 w = 2 Psi_x : 误差随 h 的阶数")
    print("=" * 78)
    for name, fn in [('center', w_from_v_center),
                     ('fwd', w_from_v_fwd),
                     ('bwd', w_from_v_bwd)]:
        print("  --- w 替代: %s ---" % name)
        for j in [1]:
            errs = []
            hs = [sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 16)]
            for h in hs:
                M = Lattice(N, vals, h, a)
                wj = 2 * sp.diff(M.Psi(j), M.x)
                errs.append(at(fn(M, j) - wj, M, x0, t0))
            print("     j=%d  err(h) =" % j, ["%.4e" % sp.N(e, 6) for e in errs])
            for k in range(1, len(errs)):
                if errs[k] != 0:
                    print("          ratio = %.5f" % sp.N(errs[k - 1] / errs[k], 8))

    print()
    print("=" * 78)
    print("[C3]  闭合系统：把 w 消去后 (N1) 的残差阶数")
    print("      (即  u_t - [v - w + d(u-w) + 2d u_x]  在 w -> w_disc 下的残差)")
    print("=" * 78)
    for name, fn in [('center', w_from_v_center),
                     ('fwd', w_from_v_fwd),
                     ('bwd', w_from_v_bwd)]:
        for j in [1]:
            errs = []
            hs = [sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 16)]
            for h in hs:
                M = Lattice(N, vals, h, a)
                wj_ex = 2 * sp.diff(M.Psi(j), M.x)
                wj_di = fn(M, j)
                lhs = sp.diff(M.u(j), M.t)
                rhs_ex = M.v_mid(j) - wj_ex + M.d * (M.u(j) - wj_ex) + 2 * M.d * sp.diff(M.u(j), M.x)
                rhs_di = M.v_mid(j) - wj_di + M.d * (M.u(j) - wj_di) + 2 * M.d * sp.diff(M.u(j), M.x)
                errs.append(at(rhs_di - rhs_ex, M, x0, t0))
            print("  w=%-7s j=%d  err =" % (name, j), ["%.4e" % sp.N(e, 6) for e in errs])
            for k in range(1, len(errs)):
                if errs[k] != 0:
                    print("          ratio = %.5f" % sp.N(errs[k - 1] / errs[k], 8))

    print()
    print("=" * 78)
    print("[C4]  v 候选定义的连续极限阶数 :  v_j - 2(ln fg)_{xy}|_{Y=(j+1/2)h}")
    print("=" * 78)
    for name in ['v_fwd', 'v_bwd', 'v_mid', 'v_cross']:
        for j in [1]:
            errs = []
            hs = [sp.Rational(1, 8), sp.Rational(1, 16), sp.Rational(1, 32)]
            for h in hs:
                ML = Lattice(N, vals, h, a)
                MC = Cont(N, vals, h, a)
                y0 = (j + sp.Rational(1, 2)) * h
                vj = at(getattr(ML, name)(j), ML, x0, t0)
                vc = at(MC.v_cont(y0), MC, x0, t0)
                errs.append(sp.simplify(vj - vc))
            print("  %-8s j=%d err =" % (name, j), ["%.4e" % sp.N(e, 6) for e in errs])
            for k in range(1, len(errs)):
                if errs[k] != 0:
                    print("          ratio = %.5f" % sp.N(errs[k - 1] / errs[k], 8))


if __name__ == '__main__':
    main()
