#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Focused test of the modified-KP -> DLW reduction (Sheng-Yu eqs. (9)-(15)).

For each configuration this script computes, by exact symbolic differentiation
and exact rational evaluation at non-singular points:

  res7 = (D_x^2 + D_t + 2a D_x) f.g                 (paper eq. (7)/(10))
  res6 = (D_y B - 4 D_x) f.g                        (paper eq. (6), lam = -2)
  dyln = d_y ln(f/g)                                (y-dynamics of the DLW field)
  u    = 2 d_x ln(f/g),  v = 2 d_xy ln(f g)

Bilinear residuals are polynomial in the tau data, so they are evaluated
directly (no division).  u, v at a point require f, g != 0 at that point.

Run:  python -u diagnose_mkp_tau.py
"""

import sympy as sp

x, y, t = sp.symbols('x y t')


def bilinear(f, g, powers):
    a, b, c = powers
    total = 0
    for p in range(a + 1):
        for q in range(b + 1):
            for r in range(c + 1):
                coef = ((-1) ** (p + q + r) * sp.binomial(a, p)
                        * sp.binomial(b, q) * sp.binomial(c, r))
                total += coef * sp.diff(f, x, a - p, y, b - q, t, c - r) \
                    * sp.diff(g, x, p, y, q, t, r)
    return sp.expand(total)


def Bop(f, g, ac):
    return sp.expand(bilinear(f, g, (2, 0, 0)) + bilinear(f, g, (0, 0, 1))
                     + 2 * ac * bilinear(f, g, (1, 0, 0)))


def DyB(f, g, ac):
    return sp.expand(bilinear(f, g, (2, 1, 0)) + bilinear(f, g, (0, 1, 1))
                     + 2 * ac * bilinear(f, g, (1, 1, 0)))


def tau(n, ps, qs, cs, a, xis, etas):
    N = len(ps)
    M = sp.zeros(N, N)
    for i in range(N):
        for j in range(N):
            xi = ps[i] * x - ps[i] ** 2 * t + y / (ps[i] - a) + xis[i]
            eta = qs[j] * x + qs[j] ** 2 * t + y / (qs[j] + a) + etas[j]
            M[i, j] = cs[j] * (1 if i == j else 0) \
                + (-(ps[i] - a) / (qs[j] + a)) ** n * sp.exp(xi + eta) / (ps[i] + qs[j])
    return sp.expand(M.det())


def analyse(N, ps, qs, cs, a, lam, pts, label):
    xis = [sp.Integer(i + 1) for i in range(N)]
    etas = [sp.Integer(-i - 2) for i in range(N)]
    f = tau(1, ps, qs, cs, a, xis, etas)
    g = tau(0, ps, qs, cs, a, xis, etas)
    res7 = Bop(f, g, a)
    res6 = sp.expand(DyB(f, g, a) - 4 * bilinear(f, g, (1, 0, 0)))
    dyln = sp.simplify(sp.diff(sp.log(f / g), y))
    print(f"\n=== {label}: N={N} p={ps} q={qs} c={cs} a={a}")
    print(f"    (p_i+q_j+2a) matrix = "
          f"{[[ps[i] + qs[j] + 2 * a for j in range(N)] for i in range(N)]}")
    print(f"    d_y ln(f/g) = {dyln}")
    for pt in pts:
        p1 = sp.nsimplify(res7.subs({x: pt[0], y: pt[1], t: pt[2]}))
        p2 = sp.nsimplify(res6.subs({x: pt[0], y: pt[1], t: pt[2]}))
        fv = sp.nsimplify(f.subs({x: pt[0], y: pt[1], t: pt[2]}))
        gv = sp.nsimplify(g.subs({x: pt[0], y: pt[1], t: pt[2]}))
        print(f"    pt={pt}: eq7={sp.simplify(p1)}  eq6={sp.simplify(p2)}"
              f"   f={sp.N(fv, 12)}  g={sp.N(gv, 12)}")
    # scale-invariant check of the y-dynamics: does d_y ln(f/g) have to vanish?
    return res7, res6, dyln


if __name__ == '__main__':
    a, lam = sp.Integer(2), sp.Integer(-2)
    pts = [(sp.Rational(1, 3), sp.Rational(2, 5), sp.Rational(1, 7)),
           (sp.Rational(2, 5), sp.Rational(3, 7), sp.Rational(4, 9))]
    analyse(1, [sp.Integer(1)], [sp.Integer(3)], [sp.Integer(1)], a, lam, pts,
            "N=1 generic (p+q+2a = 8 != 0)")
    analyse(1, [sp.Integer(1)], [sp.Integer(-5)], [sp.Integer(1)], a, lam, pts,
            "N=1 constrained (p+q+2a = 0)")
    analyse(2, [sp.Integer(1), sp.Integer(2)], [sp.Integer(-5), sp.Integer(-6)],
            [sp.Integer(1), sp.Integer(1)], a, lam, pts,
            "N=2 both diagonal constraints (p_i+q_i+2a = 0)")
    analyse(2, [sp.Integer(1), sp.Integer(2)], [sp.Integer(-5), sp.Integer(3)],
            [sp.Integer(1), sp.Integer(1)], a, lam, pts,
            "N=2 mixed (only i=1 constraint)")
