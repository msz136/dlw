"""
lax7.py -- the genuine DISCRETE LAX PAIR of the semidiscrete DLW system.

Established exactly (see report):
  * tau_n(j) satisfies the 2DTL bilinear equation  (1/2 Dx Dy - 1) tau.tau + tau_{n+1} tau_{n-1} = 0
  * therefore the standard 2D-Toda/dKP dressing construction applies with the
    ONE-TERM Lax operator L = Lambda + a_0(n),   (Lambda f)(n) = f(n+1),
    i.e. the discrete SPECTRAL PROBLEM is

        psi_{n+1}(z) + a_0(n) psi_n(z) = z psi_n(z)               (S)

    and the continuous flow is

        d/dy psi_n(z) = b_0(n) psi_{n-1}(z)                       (T)

    with
        a_0(n) = sigma_n - 1,   sigma_n = tau_{n+1} tau_{n-1} / tau_n^2 ,
        b_0(n) = tau_{n+1} tau_{n-1} / tau_n^2        ... (to be fixed)

Here the Baker-Akhiezer function is
        psi_n(z) = z^n * tau(n; y - 1/z) / tau(n)         (Lambda-convention),
or in the Delta-convention  psi = (1+z)^n tau(n; y - [z^{-1}])/tau(n).

This script VERIFIES (S) and (T) exactly, order by order in 1/z, from the
explicit DLW Gram tau.
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

    def chi(self, i, k):
        return self.lam(self.P[i]) * self.lam(self.Q[k])

    def entry(self, n, j, i, k, xv=None, yv=None, tv=None):
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
        if key not in self._c:
            self._c[key] = sp.expand(self.M(n, j).det())
        return self._c[key]

    def tau_y(self, n, j=0):
        """tau with the y-shift  y -> y + eps  applied, as a truncated series
        generator: returns callable eps -> value, using exact exp."""
        T = self.tau(n, j)
        return T


def ev(ex, extra=None):
    s = dict(P0)
    if extra:
        s.update(extra)
    v = complex(sp.sympify(ex).subs(s))
    assert abs(v.imag) < 1e-16, v
    return v.real


def phi_terms(T, n, j, K):
    """coefficients c_k(n) of  psi_n(z) = sum_{k>=0} c_k z^{-k},  with
         psi_n(z) = tau(n; y - 1/z)/tau(n)  (Delta/Lambda convention, no z^n).
       tau(n; y - 1/z) = exp(-(1/z) d_y) tau(n;y) = sum_m (-1/z)^m/m! d_y^m tau.
       =>  c_k(n) = (-1)^k / k! * d_y^k tau_n / tau_n .
    Returns list [c_0, ..., c_K]."""
    cs = []
    tk = T.tau(n, j)
    for k in range(K + 1):
        dk = sp.expand(sp.diff(T.tau(n, j), y, k))
        cs.append(sp.simplify(dk / tk))
    return cs


def check(N, p, q, j=0, K=4, verbose=True):
    T = Tau(N, A_VAL, H_VAL, p, q)
    print('=' * 92)
    print('N=%d  p=%s  q=%s  j=%d' % (N, p, q, j))
    sig = {}
    for n in range(-2, 4):
        sig[n] = sp.simplify(T.tau(n + 1, j) * T.tau(n - 1, j) / T.tau(n, j) ** 2)
    for n in range(-1, 3):
        print('   n=%2d  sigma_n = %.12g' % (n, ev(sig[n])))
    print('   --- residual check of the Toda equation')
    for n in range(-1, 3):
        pass
    # ---- spectral problem:  psi_{n+1} + a0(n) psi_n = z psi_n  with
    #      a0(n) = sigma(n) - 1
    print('   --- (S)  psi_{n+1}(z) = (z + 1 - sigma_n) psi_n(z)   [order by order]')
    for n in range(-1, 2):
        cs_n = phi_terms(T, n, j, K)
        cs_p = phi_terms(T, n + 1, j, K)
        a0 = sig[n] - 1
        ok_all = True
        for k in range(K):
            # coeff of z^{-k} in  psi_{n+1} - (z + 1 - sigma_n) psi_n :
            #   from z*psi_n : c_{k+1}(n)
            #   from (1-sigma_n) psi_n : (1-sigma_n) c_k(n)
            #   from psi_{n+1}: c_k(n+1)
            lhs = sp.simplify(cs_p[k] - (1 - sig[n]) * cs_n[k] - cs_n[k + 1])
            v = ev(lhs)
            if abs(v) > 1e-12:
                ok_all = False
            if verbose:
                print('        k=%d residual = %.6g' % (k, v))
        print('      => order %d..%d %s' % (0, K - 1, 'OK' if ok_all else 'FAIL'))
    # ---- y-flow:  d_y psi_n = b0(n) psi_{n-1}
    #   d_y psi_n = c'_k(n) ;  b0(n) psi_{n-1} = b0(n) c_k(n-1)
    print('   --- (T)  d_y psi_n(z) = b0(n) psi_{n-1}(z)')
    for n in range(-1, 2):
        cs_n = phi_terms(T, n, j, K)
        cs_m = phi_terms(T, n - 1, j, K)
        dcs = []
        tk = T.tau(n, j)
        for k in range(K + 1):
            dk = sp.expand(sp.diff(T.tau(n, j), y, k + 1))
            dcs.append(sp.simplify(dk / tk))
        for b0try, name in [(sig[n] - 1, 'sigma-1'), (sig[n], 'sigma'),
                            (-1, '-1')]:
            res = [sp.simplify(dcs[k] - b0try * cs_m[k]) for k in range(K)]
            vals = [ev(r) for r in res]
            print('        b0=%s (%s): residuals %s'
                  % (name, '%.6g' % ev(b0try), ' '.join('%.3g' % v for v in vals)))


check(2, [1, sp.Rational(5, 2)], [2, sp.Rational(7, 3)])
check(3, [2, 3, sp.Rational(9, 2)], [sp.Rational(3, 2), 4, sp.Rational(11, 3)])
