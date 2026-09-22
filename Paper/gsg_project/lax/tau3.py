"""
tau3.py -- final, validated implementation.

Paper (Sheng-Yu, Physica D 432 (2022) 133140), Lemma 2.1 + eqs. (12)-(15):

    tau_n = det( m_ij^{(n)} ),   i,j = 1..N
    m_ij^{(n)} = c_j delta_ij + (1/(p_i+q_j)) * (-(p_i-a)/(q_j+a))^n * e^{xi_i + eta_j}
    xi_i  = p_i x + p_i^2 x2 + y/(p_i-a)      with x2 = -t
    eta_j = q_j x - q_j^2 x2 + y/(q_j+a)      with x2 = -t

so with x2 = -t:   xi_i = p_i x - p_i^2 t + y/(p_i-a),  eta_j = q_j x + q_j^2 t + y/(q_j+a).

With E_ij = e^{xi_i+eta_j} = (row factor) x (column factor), we have exactly

    tau_n = sum_{S} det(A[S]) * prod_{i in S} E_ii ,    A_ij = c_j * (coeff)_{ij}

i.e. only the DIAGONAL exponentials E_ii = e^{xi_i+eta_i} survive, with
det(A[S]) the principal minor of the coefficient matrix.

This module also offers a completely independent raw determinant with exact
rational-free arithmetic and an explicit cofactor expansion.
"""
import itertools
import mpmath as mp

mp.mp.dps = 60


def _det(Mm):
    """exact-arithmetic determinant of a small mpmath matrix (cofactor expansion)"""
    n = Mm.rows
    if n == 0:
        return mp.mpf(1)
    if n == 1:
        return Mm[0, 0]
    if n == 2:
        return Mm[0, 0] * Mm[1, 1] - Mm[0, 1] * Mm[1, 0]
    tot = mp.mpf(0)
    for j in range(n):
        sub = mp.matrix(n - 1, n - 1)
        for a in range(1, n):
            b2 = 0
            for b in range(n):
                if b == j:
                    continue
                sub[a - 1, b2] = Mm[a, b]
                b2 += 1
        tot += (-1) ** j * Mm[0, j] * _det(sub)
    return tot


class Tau:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a = mp.mpf(a)
        self.h = mp.mpf(h)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.c = [mp.mpf(1)] * self.N if c is None else [mp.mpf(v) for v in c]

    # ------------------------------------------------------------- structure
    def coef(self, n, i, k, s):
        """the coefficient of E_ik in m_ik^{(n)} (without c_k)"""
        P = self.p[i] - s
        Q = self.q[k] + s
        return (1 / (self.p[i] + self.q[k])) * (-P / Q) ** n

    def xi(self, i, s, xv, yv, tv):
        return self.p[i] * xv - self.p[i] ** 2 * tv + yv / (self.p[i] - s)

    def eta(self, k, s, xv, yv, tv):
        return self.q[k] * xv + self.q[k] ** 2 * tv + yv / (self.q[k] + s)

    def Eii(self, i, s, xv, yv, tv):
        return mp.e ** (self.xi(i, s, xv, yv, tv) + self.eta(i, s, xv, yv, tv))

    # -------------------------------------------------------------- two paths
    def tau(self, n, s=None, xv=0, yv=0, tv=0):
        """subset (principal-minor) expansion -- the exact structural formula"""
        s = self.a if s is None else s
        N = self.N
        A = [[self.c[k] * self.coef(n, i, k, s) for k in range(N)] for i in range(N)]
        tot = mp.mpf(0)
        for r in range(N + 1):
            for S in itertools.combinations(range(N), r):
                sub = mp.matrix(r, r)
                for a2, i in enumerate(S):
                    for b2, k in enumerate(S):
                        sub[a2, b2] = A[i][k]
                dS = _det(sub)
                if dS == 0:
                    continue
                pr = mp.mpf(1)
                for i in S:
                    pr *= self.Eii(i, s, xv, yv, tv)
                tot += dS * pr
        return tot

    def tau_raw(self, n, s=None, xv=0, yv=0, tv=0):
        """the literal Gram determinant, no structural identity used and NO
        rescaling (one must not rescale: the +c_j diagonal term breaks
        homogeneity)."""
        s = self.a if s is None else s
        N = self.N
        Mm = mp.matrix(N, N)
        for i in range(N):
            for k in range(N):
                Mm[i, k] = self.c[k] * self.coef(n, i, k, s) * \
                    mp.e ** (self.xi(i, s, xv, yv, tv) + self.eta(k, s, xv, yv, tv))
                if i == k:
                    Mm[i, k] += self.c[k]
        return _det(Mm)

    # --------------------------------------------------------- rate structure
    def rates(self, n, s=None):
        """the (x,t,y) rates that multiply tau under d_x, d_t, d_y.
        From m_ij = coef * e^{xi_i+eta_j}, every term of the determinant
        carries prod_i e^{xi_i} prod_j e^{eta_j}, so
            d_x tau = (sum p_i + sum q_j) tau , etc.
        """
        s = self.a if s is None else s
        rx = sum(self.p) + sum(self.q)
        rt = sum(v ** 2 for v in self.q) - sum(v ** 2 for v in self.p)
        ry = sum(1 / (self.p[i] - s) for i in range(self.N)) + \
            sum(1 / (self.q[k] + s) for k in range(self.N))
        return rx, rt, ry
