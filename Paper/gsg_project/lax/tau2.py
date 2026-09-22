"""
tau2.py -- CORRECT reference implementation for the DLW Gram tau function.

Key algebra (exact).  Write the Gram matrix as

    M_{ik} = delta_{ik} + A_{ik} E_{ik},        E_{ik} = e^{xi_i} e^{eta_k},

with A_{ik} = (1/(p_i+q_k)) (-P_i/Q_k)^n (chi_i psi_k)^j.  Since E_{ik} factorises,

    det M = ( prod_i e^{xi_i} ) ( prod_k e^{eta_k} ) * det( delta_{ik} + A_{ik} )

and the last determinant expands as a sum over SUBSETS:

    det( delta + A ) = sum_{S subset of {1..N}} det( A[S] ),      det(A[{}]) = 1,

where A[S] is the principal submatrix on S.

This is the implementation used for all final checks.
"""
import mpmath as mp

mp.mp.dps = 60


def _det_sub(A, S):
    n = len(S)
    if n == 0:
        return mp.mpf(1)
    if n == 1:
        return A[S[0]][S[0]]
    import itertools
    tot = mp.mpf(0)
    for perm in itertools.permutations(S):
        sign = 1
        pl = list(perm)
        for a in range(n):
            for b in range(a + 1, n):
                if pl[a] > pl[b]:
                    sign = -sign
        term = mp.mpf(sign)
        for a in range(n):
            term *= A[S[a]][perm[a]]
        tot += term
    return tot


class T:
    def __init__(self, N, a, h, p, q):
        self.N = int(N)
        self.a = mp.mpf(a)
        self.h = mp.mpf(h)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]

    # ---------------------------------------------------------------- pieces
    def A(self, n, j, i, k, s):
        P = self.p[i] - s
        Q = self.q[k] + s
        v = (1 / (self.p[i] + self.q[k])) * (-P / Q) ** n
        if j:
            li = (self.p[i] - self.a + self.h / 2) / (self.p[i] - self.a - self.h / 2)
            lk = (self.q[k] + self.a + self.h / 2) / (self.q[k] + self.a - self.h / 2)
            v *= (li * lk) ** j
        return v

    def xi(self, i, s, xv, yv, tv):
        return self.p[i] * xv - self.p[i] ** 2 * tv + yv / (self.p[i] - s)

    def eta(self, k, s, xv, yv, tv):
        return self.q[k] * xv + self.q[k] ** 2 * tv + yv / (self.q[k] + s)

    def E(self, i, k, s, xv, yv, tv):
        return mp.e ** (self.xi(i, s, xv, yv, tv) + self.eta(k, s, xv, yv, tv))

    # ------------------------------------------------------------- tau, exact
    def tau(self, n, j, s, xv, yv, tv):
        import itertools
        N = self.N
        Amat = [[self.A(n, j, i, k, s) for k in range(N)] for i in range(N)]
        tot = mp.mpf(0)
        for r in range(N + 1):
            for S in itertools.combinations(range(N), r):
                dS = _det_sub(Amat, list(S))
                if dS == 0:
                    continue
                pr = mp.mpf(1)
                for i in S:
                    pr *= self.E(i, i, s, xv, yv, tv)
                tot += dS * pr
        return tot

    # ------------------------------------- raw determinant (independent check)
    def tau_raw(self, n, j, s, xv, yv, tv):
        N = self.N
        ent = mp.matrix(N, N)
        scale = mp.mpf(0)
        for i in range(N):
            for k in range(N):
                e = self.A(n, j, i, k, s) * self.E(i, k, s, xv, yv, tv)
                ent[i, k] = e
                scale = max(scale, abs(e))
        if scale == 0:
            return mp.mpf(0)
        mat = mp.matrix(N, N)
        for i in range(N):
            for k in range(N):
                mat[i, k] = ent[i, k] / scale
                if i == k:
                    mat[i, k] += 1
        return mp.det(mat) * scale

    # -------------------------------------------------- derivatives of tau
    def dtau(self, n, j, s, xv, yv, tv, ax=0, at=0, ay=0):
        """d_x^ax d_t^at d_y^ay of tau; the prefactor prod e^{xi_i} prod e^{eta_k}
        contributes the sum of the individual rates (independent of the subset
        and of the index), so it factors out cleanly."""
        import itertools
        N = self.N
        Amat = [[self.A(n, j, i, k, s) for k in range(N)] for i in range(N)]
        rx = sum(self.p) + sum(self.q)
        rt = sum(v ** 2 for v in self.q) - sum(v ** 2 for v in self.p)
        ry = sum(1 / (self.p[i] - s) for i in range(N)) + sum(1 / (self.q[k] + s) for k in range(N))
        pref = rx ** ax * rt ** at * ry ** ay
        return pref * self.tau(n, j, s, xv, yv, tv)
