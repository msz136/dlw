# -*- coding: utf-8 -*-
"""
1(c) hodograph 变换 / loop soliton  —— 修正版
======================================================================
论文 generalized sG (nu = -1) 的变换链:
    (2.1)  r^2 = 1 + u_x^2 ,  r > 0
    (2.7)  u_y = sin(phi) ,   -pi/2 < phi < pi/2  (mod 2pi)
    (2.8)  1/r = cos(phi)          <- 由 (2.5)(2.7) 推出
    (2.39) x_y = 1/r = cos(phi)
    (2.9)  phi_tau = sin(u)

本脚本演示三件事:
  [A] 正确的构造:  x_y = cos(phi) > 0  -> x(y) 严格单调;
      同时 u_y = sin(phi) 可变号      -> u(y) 非单调
      ==> (x, u) 平面上出现自交 = LOOP
  [B] 为什么限制 |phi| < pi/2 是必需的(否则 x 非单调, hodograph 失去意义)
  [C] 均匀 y-网格 映到 x-网格后自动加密/变稀  = SAMM 的数学内核
"""

import numpy as np

PI2 = np.pi / 2.0


# ----------------------------------------------------------------------
# 构造: 选 phi(y) = A sin(y),  要求 A < pi/2  (保证 cos(phi) > 0)
#        u(y)  = -A cos(y)            (因为 u_y = sin(phi) = sin(A sin y))
#        等一下: u_y = sin(phi) = sin(A sin y), 不是 -A cos y 的导数.
#        -A cos y 的导数是 A sin y.  所以 u_y = sin(phi) 要求
#        sin(A sin y) = A sin y  ==> 只有 A -> 0 才成立.
#
#   ==> 正确的做法: 不要预设 u 的形式, 而是 *积分*:
#           u(y) = u0 + int_0^y sin(phi(s)) ds
#           x(y) = x0 + int_0^y cos(phi(s)) ds
#       这是唯一与 (2.7)(2.8)(2.39) 一致的构造.
# ----------------------------------------------------------------------
def construct(A, y0, y1, n):
    y   = np.linspace(y0, y1, n)
    phi = A * np.sin(y)

    assert A < PI2, "必须 A < pi/2, 否则 cos(phi) 变号, 违反论文 (2.7)"

    dy  = np.diff(y)
    uy  = np.sin(phi)
    xy  = np.cos(phi)

    u = np.concatenate(([0.0], np.cumsum(0.5 * (uy[1:] + uy[:-1]) * dy)))
    x = np.concatenate(([0.0], np.cumsum(0.5 * (xy[1:] + xy[:-1]) * dy)))
    return y, phi, u, x, uy, xy


def count_branches(x, u, xs, tol):
    """对给定的 x 值, 数出对应的 u 值分支数(归并相近值)."""
    out = []
    for xt in xs:
        m = np.abs(x - xt) < tol
        if m.sum() == 0:
            out.append((xt, []))
            continue
        vals = np.sort(u[m])
        merged = []
        for v in vals:
            if not merged or abs(v - merged[-1]) > 0.05:
                merged.append(v)
        out.append((xt, merged))
    return out


def main():
    lin = "=" * 74
    print(lin)
    print(" 1(c) hodograph / loop soliton  --  修正版演示")
    print(lin)

    # ==================================================================
    # [A] 正确构造
    # ==================================================================
    A = 1.45                     # < pi/2 = 1.5708
    y0, y1, n = -6 * np.pi, 6 * np.pi, 600001
    y, phi, u, x, uy, xy = construct(A, y0, y1, n)

    print("\n[A] 构造  phi(y) = A sin y ,  A = %.4f  (< pi/2 = %.4f)" % (A, PI2))
    print("    u(y) = u0 + int sin(phi) dy      [论文 (2.7)]")
    print("    x(y) = x0 + int cos(phi) dy      [论文 (2.8)+(2.39)]")

    dx = np.diff(x); du = np.diff(u)
    print("\n    检验 x(y) 严格单调 ?   %s" % ("YES  (x_y = cos(phi) > 0 恒成立)" if np.all(dx > 0) else "NO"))
    print("    检验 u(y) 单调 ?       %s" % ("YES" if (np.all(du > 0) or np.all(du < 0)) else "NO  (u 在 y 上振荡)"))
    print("    x 范围 [%.3f, %.3f]    u 范围 [%.3f, %.3f]" % (x.min(), x.max(), u.min(), u.max()))
    print("    |u_x| 最大值 = |tan(phi)| 最大 = %.3f" % np.abs(np.tan(phi)).max())

    print("\n    ==> x 单调 但 u 振荡  =>  (x,u) 平面上曲线来回折返  =>  LOOP (多值)")

    # 多值证据
    print("\n    多值证据 (在相同 x 处列出所有 u 值):")
    xs = np.linspace(np.percentile(x, 8), np.percentile(x, 92), 7)
    for xt, vals in count_branches(x, u, xs, tol=3e-3):
        print("      x = %+8.4f  ->  %d 个 u 值:  %s"
              % (xt, len(vals), ", ".join("%+.4f" % v for v in vals)))

    # ==================================================================
    # [B] 为什么 |phi| < pi/2 必需
    # ==================================================================
    print("\n" + "-" * 74)
    print("[B] 为什么论文 (2.7) 必须限制 |phi| < pi/2 ?")
    print("-" * 74)
    for A_test in (1.45, 1.60, 2.50):
        yt, phit, ut, xt, _, xyt = construct(A_test, y0, y1, 200001)
        mono = np.all(np.diff(xt) > 0)
        print("    A = %.2f :  min cos(phi) = %+.4f  ->  x(y) 单调? %s   %s"
              % (A_test, np.cos(phit).min(), "YES" if mono else "NO ",
                 "" if A_test < PI2 else "  <-- 违反 (2.7)! hodograph 破裂"))
    print("\n    结论: cos(phi) > 0 保证 x <-> y 是可逆坐标变换;")
    print("          一旦允许 cos(phi) < 0, x(y) 不再单调, (2.4) 的链式法则失效.")

    # ==================================================================
    # [C] 自适应网格
    # ==================================================================
    print("\n" + "-" * 74)
    print("[C] 均匀 y-网格 -> 非均匀 x-网格   (= self-adaptive moving mesh)")
    print("-" * 74)
    Ny = 17
    yg = np.linspace(-2 * np.pi, 2 * np.pi, Ny)
    phig = A * np.sin(yg)
    yfine = np.linspace(-2 * np.pi, 2 * np.pi, 400001)
    phif = A * np.sin(yfine)
    xf = np.concatenate(([0.0], np.cumsum(0.5 * (np.cos(phif[1:]) + np.cos(phif[:-1])) * np.diff(yfine))))
    xg = np.interp(yg, yfine, xf)
    slope = np.tan(phig)          # u_x = u_y / x_y = sin(phi)/cos(phi) = tan(phi)

    print("      y        x(y)      dx(间距)     |u_x|")
    for i in range(Ny):
        if i == 0:
            print("   %+7.3f  %+8.4f   %8s    %7.4f" % (yg[i], xg[i], "-", abs(slope[i])))
        else:
            print("   %+7.3f  %+8.4f   %8.5f    %7.4f" % (yg[i], xg[i], xg[i] - xg[i-1], abs(slope[i])))

    corr = np.corrcoef(np.abs(slope[1:]), np.abs(np.diff(xg)))[0, 1]
    print("\n     corr( |u_x| , dx ) = %+.4f" % corr)
    print("     负相关 => |u_x| 越大(解越陡), dx 越小(网格越密)")
    print("     ==> 这就是 SAMM 的数学内核:  网格自动聚到解最陡的地方")

    # ==================================================================
    # 存盘
    # ==================================================================
    idx = slice(None, None, 200)
    np.savetxt("loop_demo_fixed.csv", np.column_stack([x[idx], u[idx]]),
               delimiter=",", header="x,u", comments="")
    print("\n[saved] loop_demo_fixed.csv   (列: x, u)")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))

        ax[0].plot(x, u, lw=1.0)
        ax[0].set_xlabel("x"); ax[0].set_ylabel("u")
        ax[0].set_title("[A] (x,u): LOOP / multivalued")
        ax[0].grid(alpha=.3)

        ax[1].plot(y, x, lw=1.0, label="x(y)")
        ax[1].plot(y, u, lw=1.0, label="u(y)")
        ax[1].set_xlabel("y"); ax[1].legend()
        ax[1].set_title("[A] both single-valued in y")
        ax[1].grid(alpha=.3)

        ax[2].plot(xg, yg * 0, 'o', ms=4)
        for i in range(Ny):
            ax[2].axvline(xg[i], color='gray', lw=.4)
        ax[2].set_xlabel("x"); ax[2].set_yticks([])
        ax[2].set_title("[C] uniform y-grid -> x clustering")
        fig.tight_layout()
        fig.savefig("loop_demo_fixed.png", dpi=130)
        print("[saved] loop_demo_fixed.png")
    except Exception as e:
        print("[skip plotting] %s" % e)


if __name__ == "__main__":
    main()
