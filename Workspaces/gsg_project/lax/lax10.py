"""
lax10.py -- the nonlinear structure of the LATTICE direction j.

Established (lax8/lax9):
  * sigma_n := tau_{n+1} tau_{n-1}/tau_n^2 = 1  for the DLW Gram tau at EVERY
    lattice site j  =>  log tau_n is affine in n  (the n-direction is linear,
    it carries no Toda potential).  Consequence:
        2 tau_n tau_{n,xx} - 2 tau_{n,x}^2 = tau_{n+1} tau_{n-1} - tau_n^2 .
  * the staggered objects are  F_j = tau_1(j; a-d),  G_j = tau_0(j),  d = h/2.

Now: the j-direction.  Is  sigma_j := G_{j+1} G_{j-1}/G_j^2  nontrivial?
And does the staggered pair (F_j, G_j) satisfy a Toda-type bilinear equation
in j, i.e. a genuine discrete integrable system with a spectral parameter?
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

    def chi(self, i, k, s=None):
        s = self.a if s is None else s
        P = self.p[i] - s
        Q = self.q[k] + s
        return self.lam(P) * self.lam(Q)

    def entry(self, n, j, i, k, s=None):
        """Gram entry with coefficient parameter s (defaults to a) and site j."""
        s = self.a if s is None else s
        p, q = self.p[i], self.q[k]
        P, Q = p - s, q + s
        coef = (-P / Q) ** n / (p + q)
        if j:
            coef *= self.chi(i, k, s) ** j
        return coef * sp.exp((p * x - p ** 2 * t + y / P) + (q * x + q ** 2 * t + y / Q))

    def M(self, n, j=0, s=None):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k, s))

    def tau(self, n, j=0, s=None):
        return sp.expand(self.M(n, j, s).det())


def ev(ex):
    v = complex(sp.sympify(ex).subs(P0))
    assert abs(v.imag) < 1e-16, v
    return v.real


for (N, p, q) in [(1, [1], [2]),
                  (2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)]),
                  (3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])]:
    T = Tau(N, A_VAL, H_VAL, p, q)
    print('=' * 92)
    print('N=%d' % N)
    d = T.h / 2
    print('  --- G_j = tau_0(j):  sigma_j = G_{j+1}G_{j-1}/G_j^2')
    for j in (1, 2):
        sg = sp.simplify(T.tau(0, j + 1) * T.tau(0, j - 1) / T.tau(0, j) ** 2)
        print('      j=%d  sigma_j = %.12g' % (j, ev(sg)))
    print('  --- staggered F_j = tau_1(j; a-d): cross-ratio F G test')
    for j in (0, 1, 2):
        F = T.tau(1, j, s=T.a - d)
        G = T.tau(0, j)
        Fp = T.tau(1, j + 1, s=T.a - d)
        Gp = T.tau(0, j + 1)
        # candidate discrete equations in j
        e1 = sp.simplify(Fp * G - F * Gp)
        e2 = sp.simplify(F * G - Fp * Gp)
        e3 = sp.simplify(Fp * Gp - F * G)
        print('      j=%d  F_{j+1}G_j - F_jG_{j+1} = %.6g   FG - F_{j+1}G_{j+1} = %.6g'
              % (j, ev(e1), ev(e2)))
        # is F_j/G_j = const in j?  (equivalently a 2-site linear relation)
        print('           F_j/G_j = %.10g   F_{j+1}/G_{j+1} = %.10g'
              % (ev(F) / ev(G), ev(Fp) / ev(Gp)))
    # 2DTL-type bilinear in j for the staggered pair?
    print('  --- probe:  (1/2 Dx Dy - 1) F_j.G_j + F_{j+1}G_{j-1} = 0 ?')
    for j in (1, 2):
        F = T.tau(1, j, s=T.a - d)
        G = T.tau(0, j)
        Fp = T.tau(1, j + 1, s=T.a - d)
        Gm = T.tau(0, j - 1)
        val = sp.Rational(1, 2) * (sp.diff(F, x, y) * G - sp.diff(F, x) * sp.diff(G, y)) - F * G + Fp * Gm
        print('      j=%d residual = %.6g' % (j, ev(val)))
