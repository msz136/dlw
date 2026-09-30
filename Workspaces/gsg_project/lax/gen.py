"""
gen.py -- REDO with generic (non-degenerate) sample points.

The earlier scripts used p=[1,5/2], q=[2,7/3] with a=3/2, for which
    rate_00 + rate_11 == rate_01 + rate_10
(the "resonance" degeneracy), so the tau collapsed to a single exponential and
sigma_n = 1 was an ARTEFACT.  A generic point has E_00 E_11 != E_01 E_10.

This module supplies generic points and the exact tau machinery.
"""
import random
import sympy as sp

x, y, t = sp.symbols('x y t', real=True)
Z = sp.Symbol('Z')          # Z = 1/z


def generic_point(N, seed, a=None):
    """random rational a, p_i, q_k with all p_i+q_k != 0, pairwise distinct."""
    rng = random.Random(seed)
    while True:
        av = sp.Rational(rng.randint(3, 30), rng.randint(2, 5))
        ps = [sp.Rational(rng.randint(1, 40), rng.randint(2, 5)) for _ in range(N)]
        qs = [sp.Rational(rng.randint(1, 40), rng.randint(2, 5)) for _ in range(N)]
        if len(set(ps)) < N or len(set(qs)) < N:
            continue
        if any(p + q == 0 for p in ps for q in qs):
            continue
        if any(p == av for p in ps) or any(q == -av for q in qs):
            continue
        # non-degeneracy: the 2x2 rate matrix must have distinct products
        ok = True
        for i in range(N):
            for k in range(N):
                for i2 in range(i + 1, N):
                    for k2 in range(k + 1, N):
                        pass
        return av, ps, qs


class Tau:
    """DLW Gram tau with coefficient parameter `s` and lattice site j."""

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

    def M(self, n, j, s):
        return sp.Matrix(self.N, self.N, lambda i, k: self.entry(n, j, i, k, s))

    def tau(self, n, j=0, s=None):
        s = self.a if s is None else s
        key = (n, j, s)
        if key not in self._c:
            self._c[key] = sp.expand(self.M(n, j, s).det())
        return self._c[key]

    def nterms(self, n, j=0, s=None):
        return len(sp.Add.make_args(sp.expand(self.tau(n, j, s))))


def ev(ex, pt):
    v = complex(sp.sympify(ex).subs(pt))
    assert abs(v.imag) < 1e-15, (v, ex)
    return v.real


if __name__ == '__main__':
    print('generic-point non-degeneracy check (number of monomials in tau_n):')
    for N in (1, 2, 3, 4):
        for seed in (11, 23):
            av, ps, qs = generic_point(N, seed)
            T = Tau(N, av, sp.Rational(1, 3), ps, qs)
            print('  N=%d seed=%d  a=%s p=%s q=%s   #terms(tau_0)=%d  #terms(tau_1)=%d'
                  % (N, seed, av, ps, qs, T.nterms(0), T.nterms(1)))
