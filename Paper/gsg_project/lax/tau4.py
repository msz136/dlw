"""
tau4.py -- CORRECT and validated implementation.

Paper (Sheng-Yu, Physica D 432 (2022) 133140), Lemma 2.1, eqs. (12)-(15):

    tau_n = det( m_ij^{(n)} ),  1 <= i,j <= N
    m_ij^{(n)} = c_j delta_ij + (1/(p_i+q_j)) (-(p_i-a)/(q_j+a))^n e^{xi_i + eta_j}

Substituting  e^{xi_i} = r_i ,  e^{eta_j} = c_j^{col}  (call them R_i , C_j):

    M = I + R A C ,  R = diag(R_i), C = diag(C_j),  A_ij = c_j^{gram} (coeff)_ij

Matrix determinant lemma:   det(I + R A C) = det(I + A C R) = det(I + B)
with   B_ij = A_ij C_i R_j  =  (1/(p_i+q_j)) (-P_i/Q_j)^n c_j e^{xi_i + eta_j} |_{i as column}

Hence EXACTLY

    tau_n = sum_{S subset of {1..N}} det( B[S] ),      B_ij = m_ij - delta_ij c_j ,

i.e. the principal-minor expansion of the coefficient matrix B = M - diag(c).

This is what the code below implements, cross-validated against the literal
Gram determinant.
"""
import itertools
import mpmath as mp

mp.mp.dps = 60


def det_exact(Mm):
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
        tot += (-1) ** j * Mm[0, j] * det_exact(sub)
    return tot


class Tau:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a = mp.mpf(a)
        self.h = mp.mpf(h)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.c = [mp.mpf(1)] * self.N if c is None else [mp.mpf(v) for v in c]

    # -------------------------------------------------------- raw Gram matrix
    def gram(self, n, s, xv, yv, tv):
        N = self.N
        Mm = mp.matrix(N, N)
        for i in range(N):
            Pi = self.p[i] - s
            ri = mp.e ** (self.p[i] * xv - self.p[i] ** 2 * tv + yv / Pi)
            for k in range(N):
                Qk = self.q[k] + s
                ck = mp.e ** (self.q[k] * xv + self.q[k] ** 2 * tv + yv / Qk)
                Mm[i, k] = self.c[k] * (1 / (self.p[i] + self.q[k])) * (-Pi / Qk) ** n * ri * ck
                if i == k:
                    Mm[i, k] += self.c[k]
        return Mm

    # ----------------------------------------------------- the two tau values
    def tau_raw(self, n, s=None, xv=0, yv=0, tv=0):
        s = self.a if s is None else s
        return det_exact(self.gram(n, s, mp.mpf(xv), mp.mpf(yv), mp.mpf(tv)))

    def Bmat(self, n, s, xv, yv, tv):
        """B_ik = A_ik * C_i * R_k = m_ik^{(n)} - delta_ik c_k  (the matrix whose
        principal minors give tau)."""
        N = self.N
        B = mp.matrix(N, N)
        for i in range(N):
            Pi = self.p[i] - s
            Ri = mp.e ** (self.p[i] * xv - self.p[i] ** 2 * tv + yv / Pi)
            for k in range(N):
                Qk = self.q[k] + s
                Ck = mp.e ** (self.q[k] * xv + self.q[k] ** 2 * tv + yv / Qk)
                B[i, k] = self.c[k] * (1 / (self.p[i] + self.q[k])) * (-Pi / Qk) ** n * Ri * Ck
        return B

    def tau(self, n, s=None, xv=0, yv=0, tv=0):
        """principal-minor expansion:  tau = sum_S det(B[S])"""
        s = self.a if s is None else s
        N = self.N
        B = self.Bmat(n, s, mp.mpf(xv), mp.mpf(yv), mp.mpf(tv))
        tot = mp.mpf(0)
        for r in range(N + 1):
            for S in itertools.combinations(range(N), r):
                sub = mp.matrix(r, r)
                for a2, i in enumerate(S):
                    for b2, k in enumerate(S):
                        sub[a2, b2] = B[i, k]
                tot += det_exact(sub)
        return tot

    # --------------------------------------------------------------- rates
    def rates(self, s=None):
        """d_x tau = Rx tau, etc. -- the exponent sum is index-independent only
        for the GLOBAL factor.  Here we return the individual per-entry rates so
        that derivatives can be computed from the minor expansion."""
        s = self.a if s is None else s
        return [(self.p[i] + self.q[k],
                 self.q[k] ** 2 - self.p[i] ** 2,
                 1 / (self.p[i] - s) + 1 / (self.q[k] + s))
                for i in range(self.N) for k in range(self.N)]
