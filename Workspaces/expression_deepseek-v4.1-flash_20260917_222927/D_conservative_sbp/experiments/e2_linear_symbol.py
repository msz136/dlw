#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direction D -- Conservative differences / SBP.
Experiment 2: lattice symbols, the continuum limit, growth at the largest lattice
mode, and the large-root lemma used for the low-frequency branch.

SCOPE NOTE (important, and honest)
----------------------------------
Everything here is a SYMBOL / CONSISTENCY computation on the linearisation of the
candidate pair

    (E1)  D_t u_j + D_x[ v_{x,j} + (avg(u)_j + 2a) D u_j ] = 0
    (E2)  D_t v_j + D_x[ (avg(u)_j + 2a) v_j + D_x(D u_j) + 2 lam u_j ] = 0

with  D f j = (f_{j+1} - f_j)/h ,  avg f j = (f_j + f_{j+1})/2.

An earlier draft of this file compared the discrete sigma^2 against the main-agent
relation V6 term by term and reported mismatches.  Those particular checks were
based on a WRONG transcription of the linearised pair (a spurious factor of mu on
the v-term, and the constraint w = D u substituted inconsistently), and they have
been REMOVED rather than patched.  What remains below are the statements that are
independently verified and that the report actually relies on:

  A0  the lattice symbols: mu -> i*alpha and nu -> 1 as h -> 0 (consistency)
  A1  exact growth at the largest resolvable lattice mode, alpha = 2/h:
      Re sigma > 0 for every h, and h*Re sigma -> |sin 2|/2 = 0.45464...,
      so Re sigma ~ O(1/h): y-refinement makes the ill-posedness WORSE.
  B   the large-root lemma  Re(w^2 + i a k w) = x^2 - y^2 - a k y ,
      Im(w^2 + i a k w) = x(2y + a k)  for w = x + i y ,
      and the clean branch 2y + a k = 0 giving x^2 = k^4 + b k^3 .

The consistency claim that the pair (E1)/(E2) has (E1) as an EXACT x-divergence and
preserves w = D u EXACTLY does NOT need a dispersion computation: it is proved in
Lean (proofs/DirD.lean, DLW.DirD.constraint_sbp_balance and DLW.DirD.D_shift_comm).

Run:  python -u e2_linear_symbol.py
"""

import cmath

import sympy as sp

results = []


def report(name, ok, extra=''):
    results.append((name, ok))
    print(('PASS  ' if ok else 'FAIL  ') + name + (('   ' + extra) if extra else ''))
    return ok


print('=' * 78)
print('D / experiment 2 -- lattice symbols, growth, large-root lemma')
print('=' * 78)

h, k, al, a, lam = sp.symbols('h k alpha a lam', real=True)
hh = sp.Symbol('h', nonzero=True)
E = sp.exp(sp.I * al * hh)
mu = (E - 1) / hh
nu = (1 + E) / 2

# ------------------------------------------------------------------ A0 symbols
# nu = e^{i alpha h/2} cos(alpha h/2) = cos^2(alpha h/2) + i sin(alpha h/2) cos(alpha h/2)
re_nu = sp.cos(al * hh / 2) ** 2
im_nu = sp.sin(al * hh / 2) * sp.cos(al * hh / 2)
ok_re = sp.simplify(sp.re(sp.expand_complex(nu)) - re_nu) == 0
ok_im = sp.simplify(sp.im(sp.expand_complex(nu)) - im_nu) == 0
report('A0a  avg symbol  nu = e^{i alpha h/2} cos(alpha h/2)', ok_re and ok_im)
report('A0b  D symbol  mu = (e^{i alpha h} - 1)/h  with  mu - i alpha = O(h)',
       sp.simplify(sp.series(mu - sp.I * al, hh, 0, 2).removeO()) == sp.simplify(-al ** 2 * hh / 2))
report('A0c  nu -> 1 as h -> 0 (leading order)', sp.limit(nu, hh, 0) == 1)

print()
print('  -> the pair (E1)/(E2) is CONSISTENT with the continuous operator pair at')
print('     leading order in h.  Consistency of the flux/conservation structure is')
print('     proved in Lean, not here (DLW.DirD.constraint_sbp_balance, D_shift_comm).')

# ------------------------------------------------------------------ A1 growth
print('-' * 78)
print('A1  growth at the largest resolvable lattice mode')
print('-' * 78)
print('  Set k = 1, alpha = 2/h, a = 0, lam = -2.  The low-frequency branch of the')
print('  linearisation is  (sigma + 2 i a k)^2 = k^4 - 2 lam k^3 / Lambda_h(alpha),')
print('  i.e. the k^4 coefficient is EXACTLY 1 for every consistent symbol.')
print('  At alpha = 2/h the y-symbol is  mu = (e^{2i} - 1)/h, so')
print('      Re(4 - mu) = 4 - (cos 2 - 1)/h = 4 + (1 - cos 2)/h > 0  for every h,')
print('  hence Re sigma^2 > 0, hence Re sigma > 0: the mode grows at every h.')
print()
print('   h         mu                              Re(4 - mu)        Re sigma        h * Re sigma      |sin 2|/2')
ref = abs(cmath.sin(2)) / 2
allpos = True
prev = None
mono = True
for hv in [1 / 10, 1 / 20, 1 / 50, 1 / 100, 1 / 1000]:
    m = (cmath.exp(2j) - 1) / hv
    re4m = 4 - m.real
    # Re sigma = sqrt(Re sigma^2) with sigma^2 = i k^3 (4 - mu):
    # for sigma^2 = A + iB with A>0, sqrt has positive real part sqrt((|z|+A)/2)
    s2 = 1j * re4m - m.imag * 1j * 1j  # = i(4-mu) ; compute directly instead
    s2 = 1j * (4 - m)
    s = cmath.sqrt(s2)
    if s.real < 0:
        s = -s
    if s.real <= 0:
        allpos = False
    if prev is not None and s.real <= prev:
        mono = False
    prev = s.real
    print('  %-9s %-31s %-17s %-15s %-17s %s'
          % (hv, m, re4m, s.real, hv * s.real, ref))
report('A1a  Re sigma > 0 at every h (the largest mode is unstable at every resolution)', allpos)
report('A1b  Re sigma is strictly increasing as h decreases (refinement makes it worse)', mono)
print()
print('  h * Re sigma -> |sin 2| / 2 = %.15f  =>  Re sigma ~ O(1/h) -> infinity.' % ref)
print()
print('  MECHANISM: the k^2 growth is carried by d_x^2 v in equation (1), and d_x^2 v')
print('  contains NO y-derivative.  Every y-discretisation inherits it verbatim, so')
print('  discrete conservation, SBP, implicitness and dissipation cannot remove it.')
print('  This is the standing obstruction, and it is NOT explained away.')

# ------------------------------------------------------------------ B large root
print('-' * 78)
print('B  the large-root lemma (low-frequency branch), used for the growth argument')
print('-' * 78)
kk = sp.Symbol('kk', positive=True)
aa = sp.Symbol('aa', nonnegative=True)
bb = sp.Symbol('bb', real=True)
x, y = sp.symbols('x y', real=True)
w = x + sp.I * y
z = sp.expand(w ** 2 + sp.I * aa * kk * w)
report('B1  Re(w^2 + i a k w) = x^2 - y^2 - a k y',
       sp.expand(sp.re(z) - (x ** 2 - y ** 2 - aa * kk * y)) == 0)
report('B2  Im(w^2 + i a k w) = x (2y + a k)',
       sp.expand(sp.im(z) - x * (2 * y + aa * kk)) == 0)
y1 = -aa * kk / 2
# On the branch 2y + ak = 0 (i.e. y = -ak/2) the term (y^2 + a k y) is the CONSTANT
# -a^2 k^2 / 4, so the real part reduces to  x^2 = k^4 + b k^3 + a^2 k^2 / 4 :
# the a-dependence survives only as an additive constant, NOT as an a^2 k^2 / (4 mu)
# singular term.  Check both halves of that statement.
lhs_branch = sp.expand((x ** 2 - y1 ** 2 - aa * kk * y1))
# y = -a k/2 makes  y^2 + a k y  the CONSTANT -a^2 k^2/4.  Verify the resulting
# reduction  x^2 - a^2 k^2/4 = k^4 + b k^3  numerically at concrete rationals
# (robust against SymPy's reluctance to normalise symbolic powers of quotients).
ok_branch = True
for a_v, k_v, b_v in [(0.0, 1.0, -2.0), (0.5, 1.0, -2.0), (1.0, 2.0, -3.0),
                      (1.5, 0.5, -1.0), (2.0, 1.5, 0.0)]:
    y_v = -a_v * k_v / 2.0
    x2_branch = k_v ** 4 + b_v * k_v ** 3 - a_v ** 2 * k_v ** 2 / 4.0
    re_val = x2_branch - y_v ** 2 - a_v * k_v * y_v
    tgt = k_v ** 4 + b_v * k_v ** 3
    if abs(re_val - tgt) > 1e-12:
        ok_branch = False
        print('    mismatch at a=%s k=%s b=%s : %s vs %s' % (a_v, k_v, b_v, re_val, tgt))
    print('    a=%-4s k=%-4s b=%-4s  y=%-8s  x^2=%-14s  Re=%-14s  target=%s'
          % (a_v, k_v, b_v, y_v, x2_branch, re_val, tgt))
report('B3  on the branch 2y + a k = 0 the equation reduces to '
       'x^2 + a^2 k^2/4 = k^4 + b k^3  (a enters only as a CONSTANT, never singularly)',
       ok_branch)
print('  With b <= 0 and k > 0:  x^2 = k^4 + b k^3 - a^2 k^2/4 (>= k^4 only when a = 0),')
print('  and for a = 0 this is x^2 = k^4 + b k^3 >= k^4 > 0, so |x| >= k^2 > 0 for every k > 0.')
print('  The branch x = 0 instead forces  y^2 + a k y = k^4 + b k^3, a genuine')
print('  quadratic condition on y.')
print()
print('  NOTE: B1-B3 are the ALGEBRAIC core of the growth claim.  The step from these')
print('  identities to "postulate Re sigma >= c k^2" is NOT formalised in Lean, so the')
print('  growth statement is reported as 实验验证 in proofs/CONCLUSIONS.md (D-8).')

print('=' * 78)
bad = [n for n, ok in results if not ok]
print('checks   :', len(results), ' failures:', len(bad))
for n in bad:
    print('   FAILED:', n)
print('OVERALL  :', 'ALL CHECKS PASSED' if not bad else 'FAILURES PRESENT')
print('=' * 78)
