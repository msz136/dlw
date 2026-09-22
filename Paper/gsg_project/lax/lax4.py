"""
lax4.py -- exact rank-one structure of the n-step, and the exact form of the
spectral tau.

Everything is done with FIXED generic rational sample values, so every test is
an exact rational-arithmetic test.
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')

x, y, t = sp.symbols('x y t', real=True)
eps = sp.Symbol('eps')
z = sp.Symbol('z')

A_VAL = sp.Rational(3, 2)
H_VAL = sp.Rational(1, 3)
P0 = {x: sp.Rational(1, 3), y: sp.Rational(-2, 5), t: sp.Rational(3, 7)}


class Tau:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a, self.h = sp.nsimplify(a), sp.nsimplify(h)
        self.p = [sp.nsimplify(v) for v in p]
        self.q = [sp.nsimplify(v) for v in q]
        self.c = [sp.Integer(1)] * self.N if c is None else [sp.nsimplify(v) for v in c]
        self.P = [self.p[i] - self.a for i in range(self.N)]
        self.Q = [self.q[k] + self.a for k in range(self.N)]

    def lam(self, v):
        return (v + self.h / 2) / (v - self.h / 2)

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    def entry(self, n, j, i, k, e=0):
        p, q = self.p[i] + e, self.q[k] + e
        P, Q = p - self.a, q + self.a
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k) ** j
        xi = p * x - p ** 2 * t + y / P
        eta = q * x + q ** 2 * t + y / Q
        return coef * sp.exp(xi + eta)

    def M(self, n, j, e=0):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k, e))

    def tau(self, n, j, e=0):
        return sp.expand(self.M(n, j, e).det())


def subs(ex, extra=None):
    s = dict(P0)
    if extra:
        s.update(extra)
    return ex.subs(s)


def cn(ex, extra=None):
    v = complex(subs(sp.sympify(ex), extra))
    assert abs(v.imag) < 1e-25, v
    return v.real


print('=' * 92)
print('I.  RANK-ONE structure of the n-step:')
print('     M_ik(n+1,j) = w * ( M_ik(n,j) + u_i v_k ) ,  w independent of (i,k)')
print('=' * 92)
for (N, p, q) in [(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    for j in (0, 1):
        M1 = T.M(1, j)
        M0 = T.M(0, j)
        # compute the *algebraic* ratio (without the exp) by dividing entries
        # define r_ik = M1_ik / M0_ik ; a rank-one-with-common-scalar means
        #    r_ik = w * (1 + t_ik) where t_ik rank one
        # equivalently  (r_ik/r_00 - 1) is rank one.
        R = sp.Matrix(N, N, lambda i, k: sp.simplify(M1[i, k] / M0[i, k]))
        base = R[0, 0]
        Zn = sp.Matrix(N, N, lambda i, k: sp.simplify(R[i, k] / base - 1))
        # test rank one: all 2x2 minors of Zn vanish
        ok = True
        for i in range(N):
            for k in range(N):
                for i2 in range(i + 1, N):
                    for k2 in range(k + 1, N):
                        m = sp.simplify(Zn[i, k] * Zn[i2, k2] - Zn[i, k2] * Zn[i2, k])
                        if m != 0:
                            ok = False
        print('  N=%d j=%d  rank-one? %s   w = %.10f   (Zn[0,0]=%.3g)'
              % (N, j, 'YES' if ok else 'NO', cn(base), cn(Zn[0, 0])))

print()
print('=' * 92)
print('II. the SPECTRAL TAU: tauhat_n(z) = det(M(n,j) + z^{-1} u v^T) with')
print('    u_i v_k = M_ik(n+1,j)/w - M_ik(n,j).  Linearity in 1/z?')
print('=' * 92)
for (N, p, q) in [(1, [1], [2]),
                  (2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    print('  N=%d' % N)
    for (n, j) in [(0, 0), (1, 0), (0, 1)]:
        M0 = T.M(n, j)
        M1 = T.M(n + 1, j)
        R = sp.Matrix(N, N, lambda i, k: sp.simplify(M1[i, k] / M0[i, k]))
        w = R[0, 0]
        # u_i v_k = M1_ik/w - M0_ik ; pick u_i = M1_i0/w - M0_i0 and v_k=delta? no:
        # simplest exact choice: u_i = col 0 of (M1/w - M0), v = e_0^T is not rank one.
        # Instead use the *square root* decomposition when the matrix is exactly rank one.
        D = sp.Matrix(N, N, lambda i, k: sp.simplify(M1[i, k] / w - M0[i, k]))
        # D should be exactly rank one: check minors
        rk = D.rank()
        Mk = M0.copy()
        # use D = u v^T with u = D e_0 / D[0,0], v = e_0^T D  (if D[0,0]!=0)
        d00 = sp.simplify(D[0, 0])
        u = [sp.simplify(D[i, 0] / d00) for i in range(N)]
        v = [sp.simplify(D[0, k]) for k in range(N)]
        Dtest = sp.Matrix(N, N, lambda i, k: sp.simplify(u[i] * v[k] - D[i, k]))
        recon_ok = all(sp.simplify(Dtest[i, k]) == 0 for i in range(N) for k in range(N))
        Mp = sp.Matrix(N, N, lambda i, k: M0[i, k] + u[i] * v[k] / z)
        tauhat = sp.expand(sp.cancel(Mp.det()))
        tau = sp.expand(M0.det())
        # ratio as a function of z
        ratio = sp.cancel(tauhat / tau)
        num, den = sp.fraction(sp.together(ratio))
        print('     n=%d j=%d  rank(D)=%d recon=%s   tauhat/tau = %s'
              % (n, j, rk, recon_ok, sp.simplify(ratio)))
