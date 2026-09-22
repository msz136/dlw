"""
lax1.py -- stage 1.

Goal: find, by exact computation, the DISCRETE LINEAR PROBLEM in the modified-KP
index n that the DLW tau function satisfies, and check whether the epsilon-shift
(the shift of all spectral parameters p_i -> p_i+eps, q_k -> q_k+eps) supplies a
spectral parameter.

Structural claim to be tested (all symbols exact):

    M_ik(n+1, j; eps) = z(eps) * [ M(n,j;eps) + sum_{a,b} u_a v_b E_ab ]_{ik}

with
    z(eps) = ((a+eps-p_i)(a+q_k+eps)) / ((p_i+eps+q_k+eps)(a-p_i)(a+q_k)) * c_ik(eps)
where c_ik(eps) = exp( (p_i+eps-p_i)x - (p_i^2-(p_i+eps)^2)t + y(1/(p_i+eps-a)-1/(p_i-a))
                    + ((q_k+eps)-q_k)x + (q_k^2-(q_k+eps)^2)t + y(1/(q_k+eps+a)-1/(q_k+a)) )

If z(eps) is independent of (i,k) then the perturbation is rank one and
    tau(n+1,j;eps) = z(eps)^N * det( M(n,j;eps) + u v^T )   (u,v independent of eps)
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')

x, y, t = sp.symbols('x y t', real=True)
eps = sp.Symbol('eps')


class Tau:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a = sp.nsimplify(a)
        self.h = sp.nsimplify(h)
        self.p = [sp.nsimplify(v) for v in p]
        self.q = [sp.nsimplify(v) for v in q]
        self.c = [sp.Integer(1)] * self.N if c is None else [sp.nsimplify(v) for v in c]
        self.P = [self.p[i] - self.a for i in range(self.N)]
        self.Q = [self.q[k] + self.a for k in range(self.N)]

    def lam(self, v):
        dd = self.h / 2
        return (v + dd) / (v - dd)

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    # ---- exponent of xi_i + eta_k at spectral parameter shift e
    def E(self, i, k, e):
        """exp(xi_i + eta_k) evaluated at p_i -> p_i+e, q_k -> q_k+e."""
        a = self.a
        p, q = self.p[i] + e, self.q[k] + e
        P, Q = p - a, q + a
        xi = p * x - p ** 2 * t + y / P
        eta = q * x + q ** 2 * t + y / Q
        return sp.exp(xi + eta)

    # ---- geometric (j-lattice) factor: uses the UNshifted P_i, Q_k
    def g(self, i, k, j):
        if j == 0:
            return sp.Integer(1)
        return (self.lam(self.P[i]) * self.lam(self.Q[k])) ** j

    # ---- entry of the Gram matrix
    def entry(self, n, j, i, k, e=0):
        a = self.a
        p, q = self.p[i] + e, self.q[k] + e
        P, Q = p - a, q + a
        coef = (-P / Q) ** n / (p + q) * self.g(i, k, j)
        return coef * self.E(i, k, e)

    def matrix(self, n, j, e=0):
        M = sp.zeros(self.N, self.N)
        for i in range(self.N):
            for k in range(self.N):
                M[i, k] = self.entry(n, j, i, k, e)
        return M

    def tau(self, n, j, e=0):
        return sp.expand(self.matrix(n, j, e).det())


def z_of(T, i, k, e):
    """ratio  M_ik(n+1,j;e) / M_ik(n,j;e)  with the off-diagonal part only."""
    a = T.a
    p, q = T.p[i] + e, T.q[k] + e
    P, Q = p - a, q + a
    # coefficient ratio:  (-P/Q)^{n+1}/(p+q) / [ (-P_i/Q_k)^n/(p_i+q_k) ]
    P0, Q0 = T.P[i], T.Q[k]
    r = (-P / Q) / (-P0 / Q0) * (T.p[i] + T.q[k]) / (p + q)
    return sp.simplify(r * (T.E(i, k, e) / T.E(i, k, 0)))


if __name__ == '__main__':
    pts = [
        (2, sp.Rational(3, 2), sp.Rational(1, 3), [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
        (3, sp.Rational(1, 2), sp.Rational(1, 4), [2, 3, sp.Rational(9, 2)],
         [sp.Rational(3, 2), 4, sp.Rational(11, 3)]),
    ]
    for (N, a, h, p, q) in pts:
        T = Tau(N, a, h, p, q)
        print('=' * 88)
        print('N =', N, ' a =', a, ' h =', h, ' p =', p, ' q =', q)
        # test: is z_of(i,k) independent of (i,k)?
        vals = {}
        for i in range(N):
            for k in range(N):
                vals[(i, k)] = sp.simplify(z_of(T, i, k, eps))
        base = vals[(0, 0)]
        for key, v in vals.items():
            diff = sp.simplify(v - base)
            print('   z[%s] - z[0,0] = %s' % (key, diff))
        print('   z[0,0] =', sp.simplify(base))
        zz = sp.simplify(base)
        print('   z(eps=0) =', sp.simplify(zz.subs(eps, 0)))
        print('   eps-derivative of z at 0 =', sp.simplify(sp.diff(zz, eps).subs(eps, 0)))
