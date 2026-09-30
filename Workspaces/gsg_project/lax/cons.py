"""
cons.py -- conservation laws of the semidiscrete DLW system.

Two independent tasks:
  (1) verify the exact rank-one / geometric structure of the n-step  (the
      "structural theorem" that kills the nonlinearity in n and j);
  (2) find and verify a genuine family of conservation laws for the LATTICE
      system {(7)_h, (6)_h}, i.e. densities rho_j with
          d_t rho_j = d_x sigma_j     (x,t conservation)
      or, for the y-direction,
          (1/h)[ sigma_{j+1} - sigma_j ] + ... = 0 .
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

print('=' * 92)
print('(1) exact structure of the n-step and of the j-step  [N=%d]' % N)
print('=' * 92)
for j in (0, 1):
    for n in (0, 1):
        a = sp.simplify(T.tau(n + 1, j) * T.tau(n - 1, j) / T.tau(n, j) ** 2)
        b = sp.simplify(T.tau(n, j + 1) * T.tau(n, j - 1) / T.tau(n, j) ** 2)
        print('   n=%d j=%d   sigma_n = %.12g      sigma_j = %.12g' % (n, j, ev(a), ev(b)))
    # the exact geometric ratios
    rn = sp.simplify(T.tau(1, j) / T.tau(0, j))
    rj = sp.simplify(T.tau(0, j + 1) / T.tau(0, j))
    print('        tau_1/tau_0 = %.12g   tau(j+1)/tau(j) = %.12g' % (ev(rn), ev(rj)))

print()
print('=' * 92)
print('(2) conservation laws of the LATTICE system')
print('    fields:  u_j = 2 d_x ln(F_j/G_j)  with  F_j = tau_1(j;a-d), G_j = tau_0(j)')
print('=' * 92)


def F(j):
    return T.tau(1, j, s=T.a - d)


def G(j):
    return T.tau(0, j, s=T.a)


# candidates for a t-conservation law  d_t rho = d_x sigma
cands = {
    'u_j': 2 * sp.diff(sp.log(F(0) / G(0)), x),
    'ln(F/G)': sp.log(F(0) / G(0)),
    'ln(FG)_x': sp.diff(sp.log(F(0) * G(0)), x),
    'ln(F/G)_t': sp.diff(sp.log(F(0) / G(0)), t),
    'ln(FG)_xx': sp.diff(sp.log(F(0) * G(0)), x, 2),
}
for name, rho in cands.items():
    # is d_t rho a total x-derivative?  test by looking at d_t rho / (something)
    drho = sp.simplify(sp.diff(rho, t))
    # integrate in x symbolically is hard; instead check the "potential" form:
    # for u:  u_t = d_x( -(u^2)/2 - 2(a-d)u - Psi_xx )  with Psi = ln FG
    print('   rho=%-12s   d_t rho = %s' % (name, sp.simplify(drho)))

print()
print('   --- explicit check of the DLW conservation law on the LATTICE:')
print('       u_t + u u_x + 2(a-d) u_x + 2 Psi_xxx = 0 ,  Psi = ln(F_j G_j)')
u = 2 * sp.diff(sp.log(F(0) / G(0)), x)
Psi = sp.log(F(0) * G(0))
res = sp.simplify(sp.diff(u, t) + u * sp.diff(u, x) + 2 * (T.a - d) * sp.diff(u, x)
                  + 2 * sp.diff(Psi, x, 3))
print('       residual = %.8g' % ev(res))
print('       (this is exactly the x-derivative of (N1) in REPORT.md section 7)')
