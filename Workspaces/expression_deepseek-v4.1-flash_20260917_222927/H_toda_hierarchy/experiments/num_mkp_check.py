#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High-precision NUMERICAL evaluation of the modified-KP -> DLW reduction
(Sheng-Yu eqs. (9)-(15)) for N up to 3, avoiding symbolic blow-up.

All quantities are evaluated with mpmath at >50 significant digits; mixed
partial derivatives are computed by central finite differences with a
Richardson-extrapolated step, so the reported residuals carry ~10+ correct
digits.  The purpose is to decide, for the multi-soliton data, whether

  (a)  (D_x^2 + D_t + 2a D_x) f.g            = 0      (paper eq. (7)/(10))
  (b)  (D_y B - 4 D_x) f.g                   = 0      (paper eq. (6), lam=-2)
  (c)  d_y ln(f/g)  = 0   (DLW field y-trivial?)  -- scale invariant
  (d)  the induced (u,v) solves (1)-(2)

with f = tau_1, g = tau_0.

Run:  python -u num_mkp_check.py
"""

import mpmath as mp

mp.mp.dps = 60

# parameter vectors; a, lam fixed at the round-1 values
A = mp.mpf(2)
LAM = mp.mpf(-2)


def make_tau(nv, ps, qs, cs, xis, etas):
    """Return tau_n as a function of (x, y, t)."""
    N = len(ps)

    def tau(X):
        x, y, t = X
        # matrix entries
        M = [[mp.mpf(0) * 0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                xi = ps[i] * x - ps[i] ** 2 * t + y / (ps[i] - A) + xis[i]
                eta = qs[j] * x + qs[j] ** 2 * t + y / (qs[j] + A) + etas[j]
                M[i][j] = (cs[j] if i == j else 0) \
                    + (-(ps[i] - A) / (qs[j] + A)) ** nv * mp.e ** (xi + eta) / (ps[i] + qs[j])
        return mp.det(mp.matrix(M))
    return tau


def d(f, X, idx, order=1, h=mp.mpf('1e-8')):
    """Central difference of order `order` in coordinate idx, Richardson-extrapolated."""
    def shift(s):
        Y = list(X)
        Y[idx] = Y[idx] + s
        return Y

    if order == 1:
        d1 = (f(shift(h)) - f(shift(-h))) / (2 * h)
        d2 = (f(shift(h / 2)) - f(shift(-h / 2))) / h
        return (4 * d2 - d1) / 3
    if order == 2:
        d1 = (f(shift(h)) - 2 * f(X) + f(shift(-h))) / h ** 2
        d2 = (f(shift(h / 2)) - 2 * f(X) + f(shift(-h / 2))) / (h / 2) ** 2
        return (4 * d2 - d1) / 3
    raise ValueError


def mixed2(f, X, i, j, h=mp.mpf('1e-6')):
    def sh(a, b):
        Y = list(X)
        Y[i] = Y[i] + a
        Y[j] = Y[j] + b
        return Y
    v1 = (f(sh(h, h)) - f(sh(h, -h)) - f(sh(-h, h)) + f(sh(-h, -h))) / (4 * h * h)
    v2 = (f(sh(h / 2, h / 2)) - f(sh(h / 2, -h / 2))
          - f(sh(-h / 2, h / 2)) + f(sh(-h / 2, -h / 2))) / (4 * (h / 2) ** 2)
    return (4 * v2 - v1) / 3


def bilinear(f, g, X, powers):
    """Hirota D_x^p D_y^q D_t^r (f.g) at point X (0 = x, 1 = y, 2 = t)."""
    p, q, r = powers
    total = mp.mpf(0)
    for i in range(p + 1):
        for j in range(q + 1):
            for k in range(r + 1):
                coef = (-1) ** (i + j + k) * mp.binomial(p, i) * mp.binomial(q, j) * mp.binomial(r, k)
                # derivative of f of order (p-i, q-j, r-k), of g of order (i,j,k)
                total += coef * dmixed(f, X, (p - i, q - j, r - k)) * dmixed(g, X, (i, j, k))
    return total


def derive(f, idx):
    """Return the function  Y |-> d f / d X_idx (Y)."""
    return lambda Y: d(f, Y, idx, 1, mp.mpf('1e-6'))


def dmixed(f, X, orders):
    """Mixed partial derivative of f at X with the given (x,y,t) orders."""
    ox, oy, ot = orders
    if ox == 0 and oy == 0 and ot == 0:
        return f(X)
    g = f
    for idx, order in ((0, ox), (1, oy), (2, ot)):
        for _ in range(order):
            g = derive(g, idx)
    return g(X)


def report(N, ps, qs, cs, label, pts):
    xis = [mp.mpf(i + 1) for i in range(N)]
    etas = [mp.mpf(-i - 2) for i in range(N)]
    tau1 = make_tau(1, ps, qs, cs, xis, etas)
    tau0 = make_tau(0, ps, qs, cs, xis, etas)
    print(f"\n=== {label}: N={N} p={ps} q={qs} c={cs} a={A}")
    print("    (p_i+q_j+2a) =",
          [[ps[i] + qs[j] + 2 * A for j in range(N)] for i in range(N)])
    for pt in pts:
        X = list(pt)
        f0, g0 = tau1(X), tau0(X)
        r7 = (bilinear(tau1, tau0, X, (2, 0, 0)) + bilinear(tau1, tau0, X, (0, 0, 1))
              + 2 * A * bilinear(tau1, tau0, X, (1, 0, 0)))
        r6 = (bilinear(tau1, tau0, X, (2, 1, 0)) + bilinear(tau1, tau0, X, (0, 1, 1))
              + 2 * A * bilinear(tau1, tau0, X, (1, 1, 0))
              - 4 * bilinear(tau1, tau0, X, (1, 0, 0)))
        # scale-invariant y-dynamics measure of the DLW field
        dyln = (d(tau1, X, 1, 1) / f0) - (d(tau0, X, 1, 1) / g0)
        u = 2 * ((d(tau1, X, 0, 1) / f0) - (d(tau0, X, 0, 1) / g0))
        print(f"    pt={tuple(float(v) for v in pt)}: f={mp.nstr(f0, 12)} g={mp.nstr(g0, 12)}")
        print(f"        eq(7) residual = {mp.nstr(r7, 10)}")
        print(f"        eq(6) residual = {mp.nstr(r6, 10)}")
        print(f"        d_y ln(f/g)    = {mp.nstr(dyln, 10)}")
        print(f"        u              = {mp.nstr(u, 10)}")


if __name__ == '__main__':
    pts = [(mp.mpf(1) / 3, mp.mpf(2) / 5, mp.mpf(1) / 7),
           (mp.mpf(2) / 5, mp.mpf(3) / 7, mp.mpf(4) / 9)]
    report(1, [mp.mpf(1)], [mp.mpf(3)], [mp.mpf(1)], "N=1 generic", pts)
    report(1, [mp.mpf(1)], [mp.mpf(-5)], [mp.mpf(1)], "N=1 constrained", pts)
    report(2, [mp.mpf(1), mp.mpf(3)], [mp.mpf(-5), mp.mpf(-7)],
           [mp.mpf(1), mp.mpf(1)], "N=2 diagonal-constrained", pts)
    report(2, [mp.mpf(1), mp.mpf(3)], [mp.mpf(-5), mp.mpf(4)],
           [mp.mpf(1), mp.mpf(1)], "N=2 mixed", pts)
