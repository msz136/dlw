"""Honest verification of the C02 certificate (proper Leibniz derivation).

Jet polynomial ring: monomials are tuples of jet symbols ('A',i,j,k)/('B',i,j,k);
total derivative D_v uses the Leibniz rule with Clairaut built into the
multi-index.  Exact sympy / Fraction coefficients, no floats.
"""
import itertools
from fractions import Fraction
import sympy as sp

M = 7  # keep jets up to total order M


def sym(field, i, j, k):
    return (field, i, j, k)


# ---------------------------------------------------------------- polynomials
def pmul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(sorted(m1 + m2))
            r[m] = r.get(m, 0) + c1 * c2
    return {m: c for m, c in r.items() if c != 0}


def padd(p, q):
    r = dict(p)
    for m, c in q.items():
        r[m] = r.get(m, 0) + c
    return {m: c for m, c in r.items() if c != 0}


def psub(p, q):
    return padd(p, {m: -c for m, c in q.items()})


def pscale(p, c):
    return {m: c * cc for m, cc in p.items()} if c != 0 else {}


def pconst(c):
    return {} if c == 0 else {(): c}


def psym(field, i, j, k):
    return {(sym(field, i, j, k),): 1}


def D(p, v):
    """total derivative w.r.t. variable v (0=x,1=y,2=t), Leibniz rule."""
    out = {}
    for m, c in p.items():
        for idx in range(len(m)):
            f, i, j, k = m[idx]
            t = [i, j, k]
            t[v] += 1
            if sum(t) > M:
                raise ValueError('jet order exceeded: %s%s' % (f, tuple(t)))
            nm = list(m)
            nm[idx] = (f, t[0], t[1], t[2])
            nm = tuple(sorted(nm))
            out[nm] = out.get(nm, 0) + c
    return {m: c for m, c in out.items() if c != 0}


def Dx(p):
    return D(p, 0)


def Dy(p):
    return D(p, 1)


def Dt(p):
    return D(p, 2)


def show(p):
    if not p:
        return '0'
    terms = []
    for m, c in sorted(p.items(), key=lambda t: (len(t[0]), t[0])):
        name = '*'.join('%s%d%d%d' % (f, i, j, k) for (f, i, j, k) in m) or '1'
        terms.append('%s*%s' % (c, name))
    return ' + '.join(terms)


a, amod = sp.Symbol('a'), None
# We keep `a` symbolic by treating it as a coefficient expression.
A = lambda i, j, k: psym('A', i, j, k)
B = lambda i, j, k: psym('B', i, j, k)

# ------------------------------------------------------------------- objects
# R = A_xx + B_x^2 + B_t + 2a B_x
R = padd(padd(padd(A(2, 0, 0), pmul(B(1, 0, 0), B(1, 0, 0))), B(0, 0, 1)),
         pscale(B(1, 0, 0), 2 * a))
# c1, c2 reduced jet forms
c1 = padd(padd(padd(padd(pscale(B(1, 1, 1), 2), pscale(A(3, 1, 0), 2)),
                    pscale(pmul(B(2, 0, 0), B(1, 1, 0)), 4)),
               pscale(pmul(B(1, 0, 0), B(2, 1, 0)), 4)),
          pscale(B(2, 1, 0), 4 * a))
c2 = padd(psub(padd(padd(padd(padd(pscale(A(1, 1, 1), 2),
                                    pscale(pmul(B(2, 0, 0), A(1, 1, 0)), 4)),
                               pscale(pmul(B(1, 0, 0), A(2, 1, 0)), 4)),
                          pscale(B(3, 1, 0), 2)),
                     pscale(A(2, 1, 0), 4 * a)),
                pscale(B(2, 0, 0), 8)), {})
# S = 2E + 4 sx B  in A,B form
S = padd(padd(padd(padd(psub(A(2, 1, 0), B(2, 1, 0)),
                         pscale(psub(A(0, 1, 1), B(0, 1, 1)), -1)),
                    pscale(pmul(B(1, 0, 0), psub(A(1, 1, 0), B(1, 1, 0))), -2)),
               pscale(psub(A(1, 1, 0), B(1, 1, 0)), -2 * a)),
          pscale(B(1, 0, 0), 4))

DxDyR = Dx(Dy(R))
print('(1) c1 - 2 DxDy R  =', show(psub(c1, pscale(DxDyR, 2))))
print('(2) c2 - (2 DxDy R - 2 Dx S) =', show(psub(c2, psub(pscale(DxDyR, 2), pscale(Dx(S), 2)))))

# --------------------------------------------------------- bridge computation
# C13 quotient for (f, sy g):  log f = p,  log(sy g) = q + L,  L = log(q_y)
# p = (A+B)/2, q = (A-B)/2
def Ab(i, j, k):
    return sp.Symbol('A_%d_%d_%d' % (i, j, k))


def Bb(i, j, k):
    return sp.Symbol('B_%d_%d_%d' % (i, j, k))


def DD(expr, v):
    """ordinary jet derivative on the *flat* sympy representation (linear-safe
    only) -- only used on expressions that are already polynomial in the jets
    and where each jet appears linearly.  For our use it is applied to the
    rational expression q_y * bracket; we instead do it by hand below."""
    raise NotImplementedError


Ax = lambda i, j, k: Ab(i, j, k)
Bx_ = lambda i, j, k: Bb(i, j, k)

qy = (Ax(0, 1, 0) - Bx_(0, 1, 0)) / 2
qxy = (Ax(1, 1, 0) - Bx_(1, 1, 0)) / 2
qxxy = (Ax(2, 1, 0) - Bx_(2, 1, 0)) / 2
qyt = (Ax(0, 1, 1) - Bx_(0, 1, 1)) / 2
Lx = qxy / qy
Lxx = qxxy / qy - (qxy / qy) ** 2
Lt = qyt / qy

Rf = Ax(2, 0, 0) + Bx_(1, 0, 0) ** 2 + Bx_(0, 0, 1) + 2 * a * Bx_(1, 0, 0)
brack = ((Ax(2, 0, 0) + Lxx) + (Bx_(1, 0, 0) - Lx) ** 2 + (Bx_(0, 0, 1) - Lt)
         + 2 * a * (Bx_(1, 0, 0) - Lx))
Ef = qxxy - 2 * Bx_(1, 0, 0) * qxy - qyt - 2 * a * qxy
print('(3b) cbil a f (sy g)/(fg) - (q_y R + E) =', sp.cancel(sp.together(qy * brack - (qy * Rf + Ef))))

# numeric specialisation (rational) as a cross-check of the identity
subs_num = {}
import random
random.seed(11)
for i, j, k in itertools.product(range(4), repeat=3):
    if i + j + k <= 3:
        subs_num[Ab(i, j, k)] = sp.Rational(random.randint(-5, 5), random.randint(1, 4))
        subs_num[Bb(i, j, k)] = sp.Rational(random.randint(-5, 5), random.randint(1, 4))
for i, j, k in itertools.product(range(4), repeat=3):
    if i + j + k <= 4:
        subs_num.setdefault(Ab(i, j, k), sp.Rational(random.randint(-5, 5), random.randint(1, 4)))
        subs_num.setdefault(Bb(i, j, k), sp.Rational(random.randint(-5, 5), random.randint(1, 4)))
subs_num[a] = sp.Rational(3, 2)
val = sp.nsimplify(sp.simplify((qy * brack - (qy * Rf + Ef)).subs(subs_num)))
print('(3c) random rational point check of (3b):', val)
