"""
lax8.py -- is the DLW Gram tau really n-dependent?  And what is
sigma_n = tau_{n+1} tau_{n-1} / tau_n^2 ?
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

    def entry(self, n, j, i, k, cvals=None):
        c = self.c if cvals is None else cvals
        p, q = self.p[i], self.q[k]
        P, Q = p - self.a, q + self.a
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k) ** j
        return coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))

    def M(self, n, j=0, cvals=None):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k, cvals))

    def tau(self, n, j=0, cvals=None):
        return sp.expand(self.M(n, j, cvals).det())


def ev(ex):
    v = complex(sp.sympify(ex).subs(P0))
    assert abs(v.imag) < 1e-16, v
    return v.real


print('=' * 92)
print('A.  is tau_n n-dependent?   (c_k = 1)')
print('=' * 92)
for (N, p, q) in [(1, [1], [2]),
                  (2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    for j in (0, 1):
        vals = [ev(T.tau(n, j)) for n in range(-1, 3)]
        print('  N=%d j=%d   tau_n (n=-1..2) = %s' % (N, j, ' '.join('%.8g' % v for v in vals)))

print()
print('=' * 92)
print('B.  sigma_n = tau_{n+1} tau_{n-1} / tau_n^2   (c_k = 1)')
print('=' * 92)
for (N, p, q) in [(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    for j in (0, 1):
        row = []
        for n in range(-1, 3):
            s = sp.simplify(T.tau(n + 1, j) * T.tau(n - 1, j) / T.tau(n, j) ** 2)
            row.append('%.10g' % ev(s))
        print('  N=%d j=%d  sigma = %s' % (N, j, ' '.join(row)))

print()
print('=' * 92)
print('C.  same with c_k NOT all equal (breaks the n-triviality)')
print('=' * 92)
for (N, p, q, cc) in [(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)],
                       [sp.Rational(1, 2), sp.Rational(3, 4)]),
                      (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)],
                       [sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(7, 4)])]:
    T = Tau(N, A_VAL, H_VAL, p, q, c=cc)
    for j in (0, 1):
        vals = [ev(T.tau(n, j)) for n in range(-1, 3)]
        sigs = ['%.10g' % ev(sp.simplify(T.tau(n + 1, j) * T.tau(n - 1, j) / T.tau(n, j) ** 2))
                for n in range(-1, 3)]
        print('  N=%d j=%d c=%s' % (N, j, cc))
        print('        tau_n  = %s' % ' '.join('%.8g' % v for v in vals))
        print('        sigma_n= %s' % ' '.join(sigs))
