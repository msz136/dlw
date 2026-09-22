# -*- coding: utf-8 -*-
"""
exactexp.py -- 指数和 `sum_j C_j exp(k_j . x)`（C_j ∈ Q, k_j ∈ Q^n）的严格恒零判定。

判定原理
--------
记 E(k) := exp(k.x) = ∏_i X_i^{k_i}（X_i = e^{x_i}）。
设所有键 k_j 共同满足的有理线性关系构成零化空间
    L = { ℓ ∈ Q^n : ℓ·k_j = 0  ∀j } .
取投影 π : Q^n → Q^m（m = n − dim L），使 π 限制在 span{k_j} 上单射。
则两个键给出**同一个单项式**当且仅当 π(k_j) = π(k_l)。

（因为 E(k) = E(k') ⟺ k − k' ∈ L^⊥∩Q^n；而 π 正是商掉 L 的坐标。）

于是   Σ_j C_j E(k_j) ≡ 0  ⟺  对每个 π-类，系数和 = 0。
"""
from fractions import Fraction as Fr


def rref(mat):
    """Q 上的 RREF。返回 (M, pivots)。M 已去掉全零行。"""
    M = [[Fr(x) for x in row] for row in mat]
    if not M:
        return [], []
    nrow, ncol = len(M), len(M[0])
    piv, r = [], 0
    for c in range(ncol):
        p = None
        for i in range(r, nrow):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(nrow):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == nrow:
            break
    return M[:r], piv


def nullspace(mat, ncol):
    """mat·v = 0 的基础解系（v ∈ Q^ncol）。"""
    if not mat:
        return [tuple(Fr(1) if i == j else Fr(0) for i in range(ncol))
                for j in range(ncol)]
    R, piv = rref(mat)
    free = [c for c in range(ncol) if c not in piv]
    out = []
    for f in free:
        v = [Fr(0)] * ncol
        v[f] = Fr(1)
        for i, pc in enumerate(piv):
            v[pc] = -R[i][f]
        out.append(tuple(v))
    return out


def canonical_projection(keys):
    """
    返回 (proj, m)。proj(k) ∈ Q^m 满足：E(k)=E(k') ⟺ proj(k)=proj(k')。
    构造：L = 零化空间；再从标准基 e_i 中挑出 (n − dim L) 个与 L 线性无关者作坐标。
    """
    K = [[Fr(c) for c in k] for k in keys]
    n = len(K[0])
    # L = { ℓ ∈ Q^n : k_j · ℓ = 0  ∀j } = nullspace of K （K 的行是键）
    L = nullspace(K, n)
    need = n - len(L)
    idx = []
    for i in range(n):
        e = [Fr(0)] * n
        e[i] = Fr(1)
        # e 与 L ∪ (已挑的 e) 张成的空间中的向量比较
        test = [list(v) for v in L] + [[Fr(1) if j == t else Fr(0) for j in range(n)]
                                       for t in idx]
        R, piv = rref(test) if test else ([], [])
        # 判断 e 是否在 test 的张成里
        rr = [Fr(x) for x in e]
        for ii, pc in enumerate(piv):
            if rr[pc] != 0:
                f = rr[pc]
                rr = [a - f * b for a, b in zip(rr, R[ii])]
        if any(x != 0 for x in rr):
            idx.append(i)
        if len(idx) == need:
            break
    assert len(idx) == need, (len(idx), need)

    def proj(k):
        return tuple(Fr(k[i]) for i in idx)

    return proj, need, idx


def is_identically_zero(items):
    items = [([Fr(c) for c in k], Fr(v)) for k, v in items if Fr(v) != 0]
    if not items:
        return True, 'empty (字典本就为空)'
    keys = [k for k, _ in items]
    proj, m, idx = canonical_projection(keys)
    acc = {}
    for k, v in items:
        c = proj(k)
        acc[c] = acc.get(c, Fr(0)) + v
    nz = {c: v for c, v in acc.items() if v != 0}
    if nz:
        return False, nz
    return True, 'm=%d (坐标 %s), 所有类系数和精确为 0' % (m, idx)
