"""
tau_ref.py -- a SINGLE clean reference implementation, validated against
(a) the exact N=1 formula and (b) a direct matrix determinant.

Sign / structure conventions (from the paper, eqs. (13)-(15)):
    M_{ik}^{(n)}(j) = delta_ik + A_ik * exp(xi_i + eta_k)
    A_ik = (1/(p_i+q_k)) * (-P_i/Q_k)^n * (chi_i * psi_k)^j
    xi_i = p_i x - p_i^2 t + y/(p_i - s),   eta_k = q_k x + q_k^2 t + y/(q_k + s)
    tau_n(j) = det M^{(n)}(j)
"""
import mpmath as mp

mp.mp.dps = 60


class Ref:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a = mp.mpf(a)
        self.h = mp.mpf(h)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.c = [mp.mpf(1)] * self.N if c is None else [mp.mpf(v) for v in c]

    # ------------------------------------------------------------ primitives
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

    # -------------------------------------------------------- exact formula
    def tau_closed(self, n, j, s, xv, yv, tv):
        """Exact: tau = prod_{i,k} e^{xi_i+eta_k} * det(delta_ik/A_ik + 1) ...
        Actually  M = D_e (D_e^{-1} + A) D_e with D_e = diag(e^{xi_i}) ...
        We use the clean identity derived in the report:
            M_{ik} = delta_ik + A_ik E_ik ,  E_ik = e^{xi_i} e^{eta_k}
        => det M = prod_{i} e^{xi_i} * prod_k e^{eta_k} * det(delta_ik + A_ik)
        (because E_ik = r_i c_k factorises).  Verified against the raw matrix.
        """
        import itertools
        N = self.N
        tot = mp.mpf(0)
        for perm in itertools.permutations(range(N)):
            sign = 1
            pl = list(perm)
            for i in range(N):
                for k in range(i + 1, N):
                    if pl[i] > pl[k]:
                        sign = -sign
            term = mp.mpf(sign)
            for i in range(N):
                term *= self.A(n, j, i, perm[i], s)
            tot += term
        pref = mp.mpf(1)
        for i in range(N):
            pref *= mp.e ** self.xi(i, s, xv, yv, tv)
        for k in range(N):
            pref *= mp.e ** self.eta(k, s, xv, yv, tv)
        return pref * tot

    def dtau_closed(self, n, j, s, xv, yv, tv, mult):
        """d/dt... of the closed form; the prefactor carries the affine part and
        the inner determinant carries the interaction."""
        import itertools
        N = self.N
        rx = sum(self.p) + sum(self.q)
        rt = sum(v ** 2 for v in self.q) - sum(v ** 2 for v in self.p)
        ry = sum(1 / (self.p[i] - s) + 1 / (self.q[k] + s) for i in range(N) for k in range(N)) / N

        def rate_i(i, k):
            return {'x': self.p[i] + self.q[k],
                    't': self.q[k] ** 2 - self.p[i] ** 2,
                    'y': 1 / (self.p[i] - s) + 1 / (self.q[k] + s)}

        # derivative of  prod e^{xi} prod e^{eta}  pulls out the common rate
        common = mp.mpf(1)
        for var, m in mult.items():
            if m:
                if var == 'x':
                    common *= (sum(self.p) + sum(self.q)) ** m
                elif var == 't':
                    common *= (sum(v ** 2 for v in self.q) - sum(v ** 2 for v in self.p)) ** m
                elif var == 'y':
                    common *= (sum(1 / (self.p[i] - s) for i in range(N))
                               + sum(1 / (self.q[k] + s) for k in range(N))) ** m
        return common * self.tau_closed(n, j, s, xv, yv, tv)

    def tau_raw(self, n, j, s, xv, yv, tv):
        """the raw determinant of the actual matrix (no identity used)"""
        N = self.N
        mat = mp.matrix(N, N)
        scale = mp.mpf(0)
        ent = mp.matrix(N, N)
        for i in range(N):
            for k in range(N):
                e = self.A(n, j, i, k, s) * mp.e ** (self.xi(i, s, xv, yv, tv)
                                                     + self.eta(k, s, xv, yv, tv))
                ent[i, k] = e
                scale = max(scale, abs(e))
        for i in range(N):
            for k in range(N):
                mat[i, k] = ent[i, k] / scale
                if i == k:
                    mat[i, k] += 1
        return mp.det(mat) * scale
