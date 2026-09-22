# -*- coding: utf-8 -*-
"""
dlwcommon2.py -- 改进的化简工具：把 ln(exp(...)) 显式展开后再化简。

问题：sp.simplify 对形如 ln(1 + C exp(S))-组合的表达式经常不能判定零。
对策：先用 expand_log(force=True) 把对数拆开（我们的 tau 是"1 + 指数和"，
      在一般位置恒正，故 force=True 合法），用 powsimp(force=True) 合并指数，
      再 cancel/simplify。
"""

import sympy as sp


def hard_simplify(e):
    e = sp.expand(sp.powsimp(sp.expand(e), force=True))
    e = sp.expand_log(e, force=True)
    e = sp.expand(sp.powsimp(e, force=True))
    e = sp.cancel(sp.together(e))
    e = sp.simplify(e)
    e = sp.nsimplify(sp.radsimp(e))
    return sp.simplify(e)


def is_zero_exact(e):
    """经验上足够强的精确零判定。"""
    if e == 0:
        return True
    s = hard_simplify(e)
    if s == 0:
        return True
    # 数值兜底（高精度）：若 |e| < 1e-40 认为零（仅作辅助，不替代上一步）
    try:
        v = complex(sp.N(s, 60))
        return abs(v) < sp.Float('1e-40')
    except Exception:
        return False


def ev(expr, M, x0, t0):
    """在 (x0,t0) 求值并 hard_simplify。"""
    return hard_simplify(expr.subs({M.x: x0, M.t: t0}))


def order_scan(build, hs, x0, t0, label=''):
    """build(h) -> 残差表达式；返回各 h 下的值以及比值。"""
    vals = []
    for h in hs:
        vals.append(ev(build(h), build(h), x0, t0))
    return vals
