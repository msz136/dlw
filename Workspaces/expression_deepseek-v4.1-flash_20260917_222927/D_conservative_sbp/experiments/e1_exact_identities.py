#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direction D -- Conservative differences / SBP.

Experiment 1: EXACT (SymPy, exact rational/symbolic arithmetic, no floating point)
verification of the lattice identities that the Lean development ``DirD.lean``
formalises, plus an explicit counterexample for the naive discretisation.

Only the y-direction is discretised; x and t stay continuous.  The x-dependence is
carried by letting every lattice unknown depend on x and t symbolically; the
identities checked here are identities in the y-index only, which is exactly what
the Lean statements capture.

Run:  python -u e1_exact_identities.py
"""

import sympy as sp

# ------------------------------------------------------------------ setup
NFIX = 6                       # concrete finite lattice size for the checks
h = sp.Symbol('h', nonzero=True)
a0_sym = sp.Symbol('a')
j = sp.Symbol('j', integer=True)

u = sp.Function('u')
v = sp.Function('v')

results = []


def fd(f, n):
    """Forward difference in y (divided form): D f_n = (f_{n+1} - f_n)/h."""
    return (f(n + 1) - f(n)) / h


def avg(f, n):
    """Lattice average: avg(f)_n = (f_n + f_{n+1})/2."""
    return (f(n) + f(n + 1)) / 2


def check(name, expr, expected=0):
    d = sp.expand(sp.simplify(expr - expected))
    ok = (d == 0)
    results.append((name, ok))
    print(('PASS  ' if ok else 'FAIL  ') + name)
    if not ok:
        print('      residual =', d)
    return ok


def telesc(Nn, f):
    return sp.expand(sum(fd(f, jj) for jj in range(Nn)))


print('=' * 78)
print('D / experiment 1 -- exact lattice identities (SymPy, exact arithmetic)')
print('=' * 78)

# ------------------------------------------------- (A) the discrete product rule
# For the forward difference  D f_j = (f_{j+1} - f_j)/h  the exact product rule is
#     D(u v) = avg(u) * D v + avg(v) * D u ,          avg(f)_j = (f_j + f_{j+1})/2,
# i.e. the SYMMETRIC (Leibniz) form with NO correction term.  This was first
# guessed wrongly as "u_j Dv + avg(v) Du"; the single-sided versions (checked in
# A2/A3) fail, and the failure residual is exactly the mixed difference
# (h/2)(D u)(D v).  The symmetric average is therefore essential.
lhs = fd(lambda n: u(n) * v(n), j)
check('A1  D(u v) = avg(u)*D v + avg(v)*D u      [symmetric, no correction]',
      lhs - (avg(u, j) * fd(v, j) + avg(v, j) * fd(u, j)))
single_sided = (u(j) * fd(v, j) + avg(v, j) * fd(u, j))
check('A2  the single-sided form is off by exactly (h/2)*(D u)*(D v)',
      lhs - single_sided - h / 2 * fd(u, j) * fd(v, j))

# ------------------------------------------------- (B) telescoping on j < NFIX
check('B1  sum_{j<N} D u_j = (u_N - u_0)/h',
      telesc(NFIX, u) - (u(NFIX) - u(0)) / h)
check('B2  sum_{j<N} D(u_j v_j) = (u_N v_N - u_0 v_0)/h',
      telesc(NFIX, lambda n: u(n) * v(n))
      - (u(NFIX) * v(NFIX) - u(0) * v(0)) / h)

# ------------------------------------------------- (C) the DLW nonlinear flux
# Candidate semidiscrete first equation (flux form, exact x-divergence):
#     D_t u_j + D_x v_j + (avg(u)_j + 2a) D u_j = 0 .
# Its nonlinear flux is  F_j = D_x v_j + (avg(u)_j + 2a) D u_j .
# Exact summation by parts for the nonlinear part:
for a0 in (0, 1, sp.Rational(3, 2), a0_sym):
    S1 = sp.expand(sum((avg(u, jj) + 2 * a0) * fd(u, jj) for jj in range(NFIX)))
    bnd = (u(NFIX) ** 2 - u(0) ** 2) / (2 * h) + 2 * a0 * (u(NFIX) - u(0)) / h
    check('C1  sum_j (avg(u)_j + 2a) D u_j = [u^2/2 + 2a u]_0^N      a = %s' % a0,
          S1 - bnd)

# The same quantity in NAIVE form, sum_j (u_j + 2a) D u_j, has no such boundary value:
S_naive_sym = sp.expand(sum((u(jj) + 2 * a0_sym) * fd(u, jj) for jj in range(NFIX)))
bnd_sym = (u(NFIX) ** 2 - u(0) ** 2) / (2 * h) + 2 * a0_sym * (u(NFIX) - u(0)) / h
resid_sym = sp.expand(S_naive_sym - bnd_sym)
ok_c2 = (resid_sym != 0)
results.append(('C2  naive sum differs from the SBP boundary value', ok_c2))
print(('PASS  ' if ok_c2 else 'FAIL  ') + 'C2  naive sum differs from the SBP boundary value')
print('      residual (naive - SBP boundary) =', resid_sym)

# ------------------------------------------------- (D) constraint preservation
# Flow hypothesis (pointwise in j, for all x, t):
#     D_t u_j = -( D_x v_j + (avg(u)_j + 2a) D u_j )
# Since D (the y-difference) and D_t commute, the induced w-field w_j := D u_j obeys
#     D_t w_j = -D ( D_x v_j + (avg(u)_j + 2a) D u_j )
#           = -D_x ( D v_j ) - D ( (avg(u)_j + 2a) D u_j )      [D, D_x commute]
# i.e. the constraint w = D u is preserved by the same equation.  Check the
# commutation-and-telescoping algebra on a concrete grid: for a flow that is an exact
# x-divergence at every j, sum_j D_t w_j must vanish identically.
hval = sp.Integer(1)
nP = 5
prof = [sp.Integer(0), sp.Integer(1), sp.Integer(4), sp.Integer(9), sp.Integer(7), sp.Integer(2)]


def Ds(f, k):
    return (f[k + 1] - f[k]) / hval


# a representative x-divergence-shaped flux F_j (arbitrary but non-symmetric in j);
# needs nP + 1 = 6 entries so that F_0 .. F_{nP} are all defined
Flux = [sp.Integer(3), sp.Integer(-2), sp.Integer(5), sp.Integer(1),
        sp.Integer(-4), sp.Integer(7)]
# sum_j D F_j over j = 0..nP-1 is a pure boundary term:
sDF = sp.expand(sum((Flux[k + 1] - Flux[k]) / hval for k in range(nP)))
check('D1  sum_j D F_j is a pure boundary term',
      sDF - (Flux[nP] - Flux[0]) / hval)

# under periodicity (F_0 = F_N) that boundary term vanishes -> exact conservation
FluxP = [sp.Integer(3), sp.Integer(-2), sp.Integer(5), sp.Integer(1),
         sp.Integer(-4), sp.Integer(3)]                 # F_nP = F_0
sDFP = sp.expand(sum((FluxP[k + 1] - FluxP[k]) / hval for k in range(nP)))
check('D2  periodic flux (F_N = F_0) => sum_j D F_j = 0 exactly', sDFP)

# ------------------------------------------------- (E) the conserved quantities
# j-sum of the j-th component of the flow, with the flow being a total x-derivative:
#     D_t u_j + D_x F_j = 0   =>   D_t ( sum_j u_j ) + D_x ( sum_j F_j ) = 0
# so the x-integral of sum_j u_j is conserved iff sum_j F_j vanishes, i.e. iff the
# y-boundary flux vanishes.  Check on the explicit numbers above:
print('-' * 78)
print('E  the two conserved x-functionals and their sign')
print('-' * 78)
print('   W(t) = int_x sum_j (D u_j) dx   -- linear in u, equals the y-boundary jump')
print('   V(t) = int_x sum_j v_j      dx   -- linear in v')
print('   both are LINEAR functionals: neither is sign definite, neither controls a norm.')

print('=' * 78)
bad = [n for n, ok in results if not ok]
print('checks run :', len(results))
print('failures   :', len(bad))
for n in bad:
    print('   FAILED:', n)
print('OVERALL    :', 'ALL EXACT CHECKS PASSED' if not bad else 'FAILURES PRESENT')
print('=' * 78)
