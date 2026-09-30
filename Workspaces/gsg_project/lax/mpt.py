"""
mpt.py -- mpmath-based exact-as-possible toolkit for the DLW tau function.

Rational data are entered exactly and evaluated in mpmath at high precision.
Derivatives are computed ANALYTICALLY (each entry differentiates by its exact
rate), so there is no finite-difference error.
"""
import mpmath as mp

mp.mp.dps = 60


class MP:
    def __init__(self, N, a, h, p, q, c=None):
        self.N = int(N)
        self.a = mp.mpf(a)
        self.h = mp.mpf(h)
        self.p = [mp.mpf(v) for v in p]
        self.q = [mp.mpf(v) for v in q]
        self.c = [mp.mpf(1)] * self.N if c is None else [mp.mpf(v) for v in c]

    # ------------------------------------------------------------------ data
    def P(self, i, s=None):
        return self.p[i] - (self.a if s is None else s)

    def Q(self, k, s=None):
        return self.q[k] + (self.a if s is None else s)

    def lam(self, v):
        return (v + self.h / 2) / (v - self.h / 2)

    # --------------------------------------------------------------- entries
    def coef(self, n, j, i, k, s):
        P, Q = self.P(i, s), self.Q(k, s)
        c = (-P / Q) ** n / (self.p[i] + self.q[k])
        if j:
            c *= (self.lam(self.p[i] - self.a) * self.lam(self.q[k] + self.a)) ** j
        return c

    def expo(self, i, k, s, xv, yv, tv):
        P, Q = self.P(i, s), self.Q(k, s)
        return (self.p[i] * xv - self.p[i] ** 2 * tv + yv / P) + \
               (self.q[k] * xv + self.q[k] ** 2 * tv + yv / Q)

    def drate(self, var, i, k, s):
        P, Q = self.P(i, s), self.Q(k, s)
        if var == 'x':
            return self.p[i] + self.q[k]
        if var == 't':
            return self.q[k] ** 2 - self.p[i] ** 2
        if var == 'y':
            return 1 / P + 1 / Q
        raise ValueError(var)

    def entry(self, n, j, i, k, s, xv, yv, tv):
        return self.coef(n, j, i, k, s) * mp.e ** self.expo(i, k, s, xv, yv, tv)

    # ------------------------------------------------- derivative machinery
    def dtau(self, n, j, s, xv, yv, tv, mult):
        """sum over permutations of  sign * prod over rows of (rate_i,perm(i))^mult
        times the entry coef.  mult = dict {'x':kx,'y':ky,'t':kt}."""
        from itertools import permutations
        N = self.N
        tot = mp.mpf(0)
        for perm in permutations(range(N)):
            sign = 1
            pl = list(perm)
            for i in range(N):
                for k in range(i + 1, N):
                    if pl[i] > pl[k]:
                        sign = -sign
            term = mp.mpf(sign)
            for i in range(N):
                k = perm[i]
                r = mp.mpf(1)
                for var, m in mult.items():
                    if m:
                        r *= self.drate(var, i, k, s) ** m
                term *= self.coef(n, j, i, k, s) * r
                term *= mp.e ** self.expo(i, k, s, xv, yv, tv)
            tot += term
        return tot

    def tau(self, n, j=0, s=None, xv=0, yv=0, tv=0):
        s = self.a if s is None else s
        return self.dtau(n, j, s, mp.mpf(xv), mp.mpf(yv), mp.mpf(tv), {})
