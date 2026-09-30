"""
cons2.py -- conservation laws, done right.

The lattice system is {(7)_h, (6)_h}:  the discrete direction is y (site j),
x and t are continuous.  A lattice conservation law is
      d_t rho_j = d_x sigma_j            (no j-difference needed: j is not a
                                          time-like direction)
or, in the y-flow form,
      d_y rho_j + (1/h)(sigma_{j+1} - sigma_j) = 0 .

We look for exact rho, sigma built from the tau data and verify them at generic
rational points.
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Workspaces\gsg_project\lax')

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

    def entry(self, n, j, i, k, s):
        p, q = self.p[i], self.q[k]
        P, Q = p - s, q + s
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= (self.lam(P) * self.lam(Q)) ** j
        return coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))

    def tau(self, n, j=0, s=None):
        s = self.a if s is None else s
        key = (n, j, s)
        if key not in self._c:
            M = sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k, s))
            self._c[key] = sp.expand(M.det())
        return self._c[key]


def ev(ex):
    v = complex(sp.sympify(ex).subs(P0))
    assert abs(v.imag) < 1e-16, v
    return v.real


N = 2
p = [1, sp.Rational(5, 2)]
q = [2, sp.Rational(7, 3)]
T = Tau(N, A_VAL, H_VAL, p, q)
d = T.h / 2


def F(j=0):
    return T.tau(1, j, s=T.a - d)


def G(j=0):
    return T.tau(0, j, s=T.a)


print('=' * 92)
print('continuum tau (h=0 replacement): use the same tau with y = continuous')
print('=' * 92)
tau = T.tau(1, 0, s=T.a) * T.tau(0, 0, s=T.a)   # the product tau_1 tau_0
tau0 = T.tau(0, 0, s=T.a)
tau1 = T.tau(1, 0, s=T.a)

# conserved densities of the (2+1) DLW from the tau:  D_k = d_x^k ln tau0
print('  D_k := d_x^k ln G     (G = tau_0)')
for k in range(0, 5):
    Dk = sp.diff(sp.log(tau0), x, k)
    dDk_t = sp.simplify(sp.diff(Dk, t))
    dDk_y = sp.simplify(sp.diff(Dk, y))
    print('   k=%d   d_t D_k = %.6g     d_y D_k = %.6g     d_x D_k = %s'
          % (k, ev(dDk_t), ev(dDk_y), sp.simplify(sp.diff(Dk, x))))

print()
print('  --- is  d_t(D_k)  a total x-derivative?   (test: solve for flux)')
for k in range(1, 5):
    Dk = sp.diff(sp.log(tau0), x, k)
    dDk_t = sp.simplify(sp.diff(Dk, t))
    if ev(dDk_t) == 0:
        print('   k=%d  d_t D_k = 0  (trivially conserved)' % k)
        continue
    # try to represent dDk_t as d_x of a combination of D_1..D_{k+1} and x,t,y
    print('   k=%d  d_t D_k = %s' % (k, sp.simplify(dDk_t)))
