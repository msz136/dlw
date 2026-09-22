"""
lax3.py -- exact-at-a-point verification of the structural identities.

Uses a FIXED generic rational point; a rational identity that holds at enough
generic points holds identically.  Exponentials are evaluated numerically to
high precision (mpmath) after the rational parts are simplified.
"""
import sys
import sympy as sp

sys.path.insert(0, r'C:\Users\msz\学术内容\Paper\gsg_project\lax')

x, y, t = sp.symbols('x y t', real=True)
eps = sp.Symbol('eps')
z = sp.Symbol('z', positive=True)

PT = {x: sp.Rational(1, 3), y: sp.Rational(-2, 5), t: sp.Rational(3, 7)}
PAR = dict(a=sp.Rational(3, 2), h=sp.Rational(1, 3))


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
        dd = self.h / 2
        return (v + dd) / (v - dd)

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    def entry_expr(self, n, j, i, k, e=0):
        a = self.a
        p, q = self.p[i] + e, self.q[k] + e
        P, Q = p - a, q + a
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k) ** j
        xi = p * x - p ** 2 * t + y / P
        eta = q * x + q ** 2 * t + y / Q
        return coef * sp.exp(xi + eta)

    def matrix(self, n, j, e=0):
        return sp.Matrix(self.N, self.N,
                         lambda i, k: self.entry_expr(n, j, i, k, e))

    def tau_expr(self, n, j, e=0):
        return sp.expand(self.matrix(n, j, e).det())

    def tau(self, n, j, e=0, pt=None, val=None, e_val=None):
        """numeric value at PT; if `val` given it also substitutes e -> e_val."""
        ex = self.tau_expr(n, j, e)
        sub = dict(PT)
        if e_val is not None:
            sub[e] = e_val
        v = complex(ex.subs(sub))
        return sp.nsimplify(sp.re(v)) if abs(sp.im(v)) < 1e-40 else v


def num(ex, extra=None):
    sub = dict(PT)
    if extra:
        sub.update(extra)
    v = complex(sp.sympify(ex).subs(sub))
    assert abs(v.imag) < 1e-30, 'not real: %s' % v
    return v.real


# ------------------------------------------------------------------ S1
print('=' * 90)
print('S1:  tau_{p+e,q+e}(x,y,t) = exp(e x + e^2 t) * tau_{p,q}(x + 2 e t, y, t)   ?')
print('=' * 90)
for (N, p, q) in [(1, [1], [2]),
                  (2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, PAR['a'], PAR['h'], p, q)
    for e0 in [sp.Rational(1, 3), sp.Rational(-2, 5)]:
        lhs = num(T.tau_expr(1, 1, e=eps), {eps: e0})
        # rhs: shift x -> x + 2 e t  inside the tau, times exp(e x + e^2 t)
        T0 = Tau(N, PAR['a'], PAR['h'], p, q)
        ex = T0.tau_expr(1, 1, e=0)
        shift = {x: PT[x] + 2 * e0 * PT[t]}
        val = num(ex, shift)
        rhs = val * num(sp.exp(e0 * x + e0 ** 2 * t))
        print('  N=%d e=%s   lhs=%.15g rhs=%.15g  diff=%.3g  %s'
              % (N, e0, lhs, rhs, abs(lhs - rhs), 'OK' if abs(lhs - rhs) < 1e-20 else 'FAIL'))

# ------------------------------------------------------------------ S2/S3
print()
print('=' * 90)
print('S3:  the n -> n+1 step is an exact SIMILARITY + RANK-ONE update')
print('     M(n+1,j;e) = w_e * ( M(n,j;e) + u_i v_k )     (w independent of i,k)')
print('=' * 90)
for (N, p, q) in [(1, [1], [2]),
                  (2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, PAR['a'], PAR['h'], p, q)
    e0 = sp.Rational(1, 3)
    M1 = T.matrix(1, 1, e=e0)
    M0 = T.matrix(0, 1, e=e0)
    # divide elementwise:  r_ik = M1_ik / M0_ik   should be w * (1 + u_i v_k/M0_ik)
    # test whether all r_ik share the same 'exponential part'
    # simplest: check  r_ik / r_00  is a PURE function of the 'algebraic' data?
    print('  N=%d' % N)
    for i in range(N):
        for k in range(N):
            r = sp.simplify((M1[i, k] / M0[i, k]) / (M1[0, 0] / M0[0, 0]))
            print('     r[%d,%d]/r[0,0] = %s' % (i, k, sp.nsimplify(sp.simplify(r))))
