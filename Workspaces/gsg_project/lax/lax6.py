"""
lax6.py -- decisive search for a linear (spectral) problem in the discrete
index n.

We know exactly (verified at rational points):
  * tau_n(j) satisfies the 2DTL bilinear equation
        (1/2 Dx Dy - 1) tau_n . tau_n + tau_{n+1} tau_{n-1} = 0
  * the "spectral tau"
        TH_n(z) = det( M(n,j) + z^{-1} u v^T ) = tau_n * (1 + Q_n / z)
    is exactly LINEAR in 1/z.

Here we ask: does psi_n(z) := TH_n(z)/tau_n satisfy a LINEAR SPECTRAL PROBLEM
        psi_{n+1}(z) = a_n(z) psi_n(z) + b_n(z) psi_{n-1}(z)
with z-rational coefficients a_n, b_n whose z-dependence is *universal*
(i.e. the monodromy is nontrivial)?  We fit a_n, b_n exactly and inspect.
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')

x, y, t = sp.symbols('x y t', real=True)
Z = sp.Symbol('Z')          # Z := 1/z

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
        self._cache = {}

    def lam(self, v):
        return (v + self.h / 2) / (v - self.h / 2)

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    def entry(self, n, j, i, k):
        p, q = self.p[i], self.q[k]
        P, Q = p - self.a, q + self.a
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k) ** j
        return coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))

    def M(self, n, j=0):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k))

    def tau(self, n, j=0):
        key = (n, j)
        if key not in self._cache:
            self._cache[key] = sp.expand(self.M(n, j).det())
        return self._cache[key]

    def tauhat(self, n, Zv, j=0):
        """det(M + Zv * u v^T),  u_i = p_i, v_k = q_k."""
        M = self.M(n, j).copy()
        for i in range(self.N):
            for k in range(self.N):
                M[i, k] = M[i, k] + Zv * self.p[i] * self.q[k]
        return sp.expand(M.det())


def ev(ex, extra=None):
    s = dict(P0)
    if extra:
        s.update(extra)
    v = complex(sp.sympify(ex).subs(s))
    assert abs(v.imag) < 1e-18, (v)
    return v.real


def run(N, p, q, j=0, nmax=3):
    T = Tau(N, A_VAL, H_VAL, p, q)
    print('=' * 92)
    print('N=%d  p=%s q=%s  j=%d' % (N, p, q, j))
    # Q_n : coefficient of 1/z in  TH_n(z) = tau_n (1 + Q_n / z)
    Q = {}
    for n in range(-2, nmax + 2):
        tn = T.tau(n, j)
        th = T.tauhat(n, Z, j)
        # TH = tau + Z * (something) ; expand
        expr = sp.expand(th)
        c0 = sp.simplify(expr.subs(Z, 0))
        assert sp.simplify(c0 - tn) == 0, 'linearity fails: TH(0) != tau'
        c1 = sp.simplify((expr - c0).subs(Z, 1))
        Q[n] = sp.simplify(c1 / tn)
        print('   n=%2d   Q_n = %.12g' % (n, ev(Q[n])))
    # check the closed form  Q_n = tau_{n+1} tau_{n-1}/tau_n^2 - 1 ?
    print('   --- test  Q_n = tau_{n+1} tau_{n-1}/tau_n^2 - 1')
    for n in range(-1, nmax + 1):
        rhs = sp.simplify(T.tau(n + 1, j) * T.tau(n - 1, j) / T.tau(n, j) ** 2 - 1)
        print('       n=%2d  Q_n=%.12g  rhs=%.12g  %s'
              % (n, ev(Q[n]), ev(rhs), 'OK' if abs(ev(Q[n]) - ev(rhs)) < 1e-14 else 'FAIL'))


run(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)])
run(3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])
