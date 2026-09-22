"""
lax12.py -- verify the 2DTL Lax-pair machinery against the explicit DLW tau,
and identify precisely what is (and is not) nontrivial.

2DTL Lax pair (Ueno-Takasaki / Liu-Zeng-Lin, arXiv:0710.5411 eq.(5)):
      psi_{n+1} + u_n psi_n = z psi_n          (S)   [spectral problem]
      d/dy psi_n = v_n psi_{n-1}               (T)   [flow]
compatibility:
      u_{n,y} = v_{n+1} - v_n ,      v_{n,x} = v_n (u_n - u_{n-1}) ,   (F)
with  u_n = sigma_n - 1,   sigma_n = tau_{n+1} tau_{n-1}/tau_n^2 .
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')

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
        self._c = {}

    def lam(self, v):
        return (v + self.h / 2) / (v - self.h / 2)

    def entry(self, n, j, i, k):
        p, q = self.p[i], self.q[k]
        P, Q = p - self.a, q + self.a
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= (self.lam(P) * self.lam(Q)) ** j
        return coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))

    def tau(self, n, j=0):
        key = (n, j)
        if key not in self._c:
            M = sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k))
            self._c[key] = sp.expand(M.det())
        return self._c[key]


def ev(ex):
    v = complex(sp.sympify(ex).subs(P0))
    assert abs(v.imag) < 1e-16, v
    return v.real


for (N, p, q) in [(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    for j in (0, 1):
        print('=' * 88)
        print('N=%d j=%d' % (N, j))
        # Toda potentials
        u = {}
        v = {}
        for n in range(-1, 3):
            sig = sp.simplify(T.tau(n + 1, j) * T.tau(n - 1, j) / T.tau(n, j) ** 2)
            u[n] = sp.simplify(sig - 1)
            v[n] = sp.simplify(T.tau(n, j) * T.tau(n + 1, j) / T.tau(n, j) ** 2) * 0 + sig
        print('   sigma_n:', ' '.join('%d:%.8g' % (n, ev(u[n] + 1)) for n in sorted(u)))
        # (F) flow equations with v_n := sigma_n
        for n in range(0, 2):
            r1 = sp.simplify(sp.diff(u[n], y) - (v[n + 1] - v[n]))
            r2 = sp.simplify(sp.diff(v[n], x) - v[n] * (u[n] - u[n - 1]))
            print('   n=%d  u_y-(v_{n+1}-v_n) = %.6g    v_x - v(u_n-u_{n-1}) = %.6g'
                  % (n, ev(r1), ev(r2)))
