# -*- coding: utf-8 -*-
"""
audit_cont.py -- 独立审计：连续 DLW 的双线性方程组 (7)(6) 是否对 Gram tau 恒成立。

论文 (Sheng-Yu, Physica D 432 (2022) 133140):
    (7)  B_a f . g := (D_x^2 + D_t + 2a D_x) f.g = 0
    (6)  [D_y B_a + 2λ D_x] f.g = 0 ,   λ = -2 时等价于 B_a f.g_y + 2 D_x f.g = 0
    tau:  m_ik = c_k δ_ik + (1/(p_i+q_k)) (-(p_i-a)/(q_k+a))^n e^{ξ_i+η_k}
          ξ_i = p_i x - p_i^2 t + y/(p_i-a)
          η_k = q_k x + q_k^2 t + y/(q_k+a)
    u = 2 (ln f/g)_x ,  v = 2 (ln fg)_{xy}

本脚本用 sympy 对 N=1 与 N=2 逐项验证 (7) 与 (6)，把结果化到指数基上读系数。
"""
import sympy as sp

x, t, y = sp.symbols('x t y', real=True)
lam = sp.Integer(-2)


def build_tau(N, a, p, q, n):
    """返回 tau 的指数基表示：dict {phase_symbol: coefficient}，并给出符号表。"""
    # 用 (S,R,T) 作键，键 -> 系数
    from itertools import permutations
    keys = {}
    total = {}
    for perm in permutations(range(N)):
        sign = 1
        pl = list(perm)
        for i in range(N):
            for j in range(i + 1, N):
                if pl[i] > pl[j]:
                    sign = -sign
        term = {(sp.Integer(0), sp.Integer(0), sp.Integer(0)): sp.Integer(sign)}
        for i in range(N):
            k = perm[i]
            P = p[i] - a
            Q = q[k] + a
            coef = (-P / Q) ** n / (p[i] + q[k])
            S = p[i] + q[k]
            R = q[k] ** 2 - p[i] ** 2
            T = 1 / P + 1 / Q
            out = {(S, R, T): coef}
            if i == k:
                out[(sp.Integer(0),) * 3] = out.get((0, 0, 0), 0) + 1
                if out[(0, 0, 0)] == 0:
                    del out[(0, 0, 0)]
                    out[(0, 0, 0)] = sp.Integer(1)
            term = _mul(term, out)
        total = _add(total, term)
    return total


def _add(d1, d2):
    out = dict(d1)
    for k, v in d2.items():
        nv = out.get(k, sp.Integer(0)) + v
        if sp.simplify(nv) == 0:
            out.pop(k, None)
        else:
            out[k] = sp.simplify(nv)
    return out


def _mul(d1, d2):
    out = {}
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            k = tuple(a + b for a, b in zip(k1, k2))
            out[k] = sp.simplify(out.get(k, sp.Integer(0)) + v1 * v2)
    return {k: v for k, v in out.items() if sp.simplify(v) != 0}


def _deriv(d, mx=0, mt=0, my=0):
    return {k: v * k[0] ** mx * k[1] ** mt * k[2] ** my for k, v in d.items()}


def _bilin(F, G, mx=0, mt=0, my=0):
    tot = {}
    for i in range(mx + 1):
        for j in range(mt + 1):
            for l in range(my + 1):
                co = (-1) ** (i + j + l) * sp.binomial(mx, i) * sp.binomial(mt, j) \
                    * sp.binomial(my, l)
                tot = _add(tot, {k: co * v for k, v in _mul(
                    _deriv(F, mx - i, mt - j, my - l), _deriv(G, i, j, l)).items()})
    return tot


def Bs(F, G, s):
    return _add(_add(_bilin(F, G, 2, 0), _bilin(F, G, 0, 1)),
                {k: 2 * s * v for k, v in _bilin(F, G, 1, 0).items()})


def test(N, a, p, q, label):
    print("=" * 70)
    print(label)
    print("=" * 70)
    f = build_tau(N, a, p, q, 1)
    g = build_tau(N, a, p, q, 0)
    print("  f 项数 =", len(f), "  g 项数 =", len(g))
    r7 = Bs(f, g, a)
    print("  (7)  B_a f.g  残差项数 =", len(r7))
    if r7:
        for k, v in list(r7.items())[:4]:
            print("     键", tuple(str(z) for z in k), " 系数", sp.simplify(v))
    r6 = Bs(_deriv(f, 0, 0, 1), g, a)
    r6 = _add(r6, {k: 2 * v for k, v in _bilin(f, g, 1, 0).items()})
    print("  (6)  B_a f_y.g + 2 D_x f.g  残差项数 =", len(r6))
    if r6:
        for k, v in list(r6.items())[:4]:
            print("     键", tuple(str(z) for z in k), " 系数", sp.simplify(v))


if __name__ == '__main__':
    test(1, sp.Integer(4), [sp.Rational(2, 3)], [sp.Rational(-18, 5)],
         "N=1, a=4, p=2/3, q=-18/5")
    print()
    test(2, sp.Integer(1), [sp.Rational(3, 2), sp.Rational(5, 2)],
         [sp.Rational(-2), sp.Rational(-3)], "N=2, a=1")
