"""
lax9.py -- decisive tests.

Established so far, exactly:
  * tau_n(j) satisfies the 2DTL bilinear equation
        (1/2 Dx Dy - 1) tau_n.tau_n + tau_{n+1} tau_{n-1} = 0
  * sigma_n := tau_{n+1} tau_{n-1} / tau_n^2  =  1   (identically!)
    => the "Toda potential" of the n-direction is trivial: the Lax operator
    Lambda + (sigma_n - 1) reduces to Lambda, i.e. the n-direction carries no
    nonlinearity, only the rank-one spectral data.

Here we look for the genuine linear problem in the MODIFIED-KP index n in a
form that does carry a spectral parameter, and for the conservation laws.
"""
import sys
import sympy as sp

x, y, t = sp.symbols('x y t', real=True)
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
        return sp.expand(self.M(n, j).det())


def ev(ex):
    v = complex(sp.sympify(ex).subs(P0))
    assert abs(v.imag) < 1e-16, v
    return v.real


def probe(N, p, q, j=0, n=1):
    T = Tau(N, A_VAL, H_VAL, p, q)
    tn = T.tau(n, j)
    tnp = T.tau(n + 1, j)
    tnm = T.tau(n - 1, j)
    print('=' * 92)
    print('N=%d  n=%d  j=%d' % (N, n, j))
    print('   sigma_n                       = %.12g' % ev(sp.simplify(tnp * tnm / tn ** 2)))
    print('   (tau_n tau_n,xx - tau_n,x^2)/tau_n^2 = %.12g'
          % ev(sp.simplify((tn * sp.diff(tn, x, 2) - sp.diff(tn, x) ** 2) / tn ** 2)))
    print('   (tau_{n+1}tau_{n-1} - tau_n^2)/tau_n^2  = %.12g'
          % ev(sp.simplify((tnp * tnm - tn ** 2) / tn ** 2)))
    # residual of  2 tau tau_xx - 2 tau_x^2 - tau_{n+1}tau_{n-1} + tau_n^2
    res = sp.simplify(2 * tn * sp.diff(tn, x, 2) - 2 * sp.diff(tn, x) ** 2
                      - tnp * tnm + tn ** 2)
    print('   residual 2tt_xx-2t_x^2-t_{n+1}t_{n-1}+t_n^2 = %.6g' % ev(res))
    # y-derivative version
    resy = sp.simplify(tn * sp.diff(tn, x, 1, y, 1) - sp.diff(tn, x) * sp.diff(tn, y)
                       - (tnp * tnm - tn ** 2))
    print('   residual t t_xy - t_x t_y - (t_{n+1}t_{n-1}-t_n^2) = %.6g' % ev(resy))


for (N, p, q) in [(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)]),
                  (4, [1, sp.Rational(3, 2), 3, sp.Rational(7, 2)],
                   [sp.Rational(4, 3), 2, sp.Rational(5, 2), 5])]:
    for j in (0, 1):
        for n in (1, 2):
            probe(N, p, q, j, n)
