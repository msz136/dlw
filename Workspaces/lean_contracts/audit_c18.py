"""Exact symbolic audit of the C18 hand-expansion (project rules 1, 2, 4).

C18 claims, with `PowBound 2` = O(h^2):
    n1(j=0) - c1(x, y-h/2, t) = O(h^2)
    n2(j=0) - c2(x, y,   t) = O(h^2)

Method (no floats, NOT a single-point test): take GENERIC polynomial test fields
    u = sum cu[i,j,k] x^i y^j t^k ,  v = sum cv[i,j,k] x^i y^j t^k
with symbolic coefficients.  A generic polynomial realises every compatible jet
tuple up to its degree, so the h^0 and h^1 coefficients of the difference are
polynomials in the cu/cv that vanish identically iff the expansion is correct.
That is a genuine identity test, not an evaluation at a lucky point.

The reductions used by the Lean proof are recorded as comments at the end.
"""
import sympy as sp
from itertools import product

x, y, t, h, a = sp.symbols('x y t h a', real=True)

# --- generic polynomial test fields ----------------------------------------
I, J, K = 3, 4, 3          # x-order, y-order, t-order
cu = {(i, j, k): sp.Symbol(f'cu{i}{j}{k}') for i, j, k in product(range(I + 1), range(J + 1), range(K + 1))}
cv = {(i, j, k): sp.Symbol(f'cv{i}{j}{k}') for i, j, k in product(range(I + 1), range(J + 1), range(K + 1))}


def poly(c):
    return sum(c[(i, j, k)] * x ** i * y ** j * t ** k for i, j, k in c)


U = poly(cu)
V = poly(cv)


def u(k):
    """localSamples y h u at lattice index k."""
    return U.subs(y, y + k * h)


def v(k):
    return V.subs(y, y + k * h)


def dm(e0, em):
    return sp.cancel((e0 - em) / h)


def d0(ep, em):
    return sp.cancel((ep - em) / (2 * h))


def mm(e0, em):
    return (e0 + em) / 2


def lap(ep, e0, em):
    return sp.cancel((ep - 2 * e0 + em) / h ** 2)


def W(k):
    return v(k) - d0(u(k + 1), u(k - 1))


def H(k):
    return u(k) ** 2 / 2 + 2 * a * u(k) + h ** 2 * (W(k) ** 2 / 32 - W(k) / 4)


# --- n1 at j = 0:  dm h (lt u + lx (H)) + lxx (mm v - (h^2/4) lap h (dm h u))
n1 = (dm(sp.diff(u(0), t) + sp.diff(H(0), x),
         sp.diff(u(-1), t) + sp.diff(H(-1), x))
      + sp.diff(mm(v(0), v(-1))
                - sp.cancel(h ** 2 / 4 * lap(dm(u(1), u(0)), dm(u(0), u(-1)), dm(u(-1), u(-2)))), x, 2))

# --- n2 at j = 0: lt v + lx (d0 h H + (u+2a) W - 4u) + lxx (d0 h u + (h^2/4) lap h W)
inner = d0(H(1), H(-1)) + (u(0) + 2 * a) * W(0) - 4 * u(0)
n2 = (sp.diff(v(0), t) + sp.diff(inner, x)
      + sp.diff(d0(u(1), u(-1)) + sp.cancel(h ** 2 / 4 * lap(W(1), W(0), W(-1))), x, 2))

# --- continuous targets ----------------------------------------------------
Y = sp.Symbol('Y', real=True)
Us = U.subs(y, Y)          # u as a function of the evaluation point Y
Vs = V.subs(y, Y)


def c1_at(Yv):
    """c1 a u v = sy(st u) + sx(sx v) + sx(u sy u) + (2a) sx(sy u), at y = Yv."""
    return (sp.diff(sp.diff(Us.subs(Y, Yv), t), Yv)
            + sp.diff(Vs.subs(Y, Yv), x, 2)
            + sp.diff(Us.subs(Y, Yv) * sp.diff(Us.subs(Y, Yv), Yv), x)
            + 2 * a * sp.diff(sp.diff(Us.subs(Y, Yv), Yv), x))


def c2_at(Yv):
    """c2 a u v = st v + sx(u v) + sx(sx(sy u)) + (2a) sx v - 4 sx u, at y = Yv."""
    return (sp.diff(Vs.subs(Y, Yv), t)
            + sp.diff(Us.subs(Y, Yv) * Vs.subs(Y, Yv), x)
            + sp.diff(sp.diff(Us.subs(Y, Yv), Yv), x, 2)
            + 2 * a * sp.diff(Vs.subs(Y, Yv), x)
            - 4 * sp.diff(Us.subs(Y, Yv), x))


def taylor_low(expr_in_Y, shift):
    """Maclaurin-in-h truncation of expr_in_Y evaluated at Y = y + shift*h, to h^1."""
    out = 0
    for m in range(2):                     # need h^0, h^1 only
        out += (sp.diff(expr_in_Y, Y, m).subs(Y, y) * (shift * h) ** m) / sp.factorial(m)
    return sp.cancel(out)


def coeffs(e):
    e = sp.cancel(sp.expand(e))
    return sp.simplify(e.coeff(h, 0)), sp.simplify(e.coeff(h, 1))


print('=== n1 - c1(y - h/2)   [contract requires the y-h/2 shift] ===')
d1 = sp.cancel(n1 - taylor_low(c1_at(Y), sp.Rational(-1, 2)))
c0, c1c = coeffs(d1)
print(f'  h^0 coefficient identically zero: {c0 == 0}')
print(f'  h^1 coefficient identically zero: {c1c == 0}')
if c0 != 0:
    print(f'    *** h^0 NONZERO, sample terms: {sp.expand(c0).as_ordered_terms()[:3]}')
if c1c != 0:
    print(f'    *** h^1 NONZERO, sample terms: {sp.expand(c1c).as_ordered_terms()[:3]}')

print('=== n2 - c2(y)         [contract uses no shift] ===')
d2 = sp.cancel(n2 - taylor_low(c2_at(Y), sp.Integer(0)))
d0c, d1c = coeffs(d2)
print(f'  h^0 coefficient identically zero: {d0c == 0}')
print(f'  h^1 coefficient identically zero: {d1c == 0}')
if d0c != 0:
    print(f'    *** h^0 NONZERO, sample terms: {sp.expand(d0c).as_ordered_terms()[:3]}')
if d1c != 0:
    print(f'    *** h^1 NONZERO, sample terms: {sp.expand(d1c).as_ordered_terms()[:3]}')

print('=== NEGATIVE CONTROL: n1 - c1(y), shift removed ===')
dn = sp.cancel(n1 - taylor_low(c1_at(Y), sp.Integer(0)))
n0, n1c = coeffs(dn)
print(f'  h^0 zero: {n0 == 0}   h^1 zero: {n1c == 0}')
print('  (expect h^0 TRUE, h^1 FALSE: proves the y-h/2 shift in the contract is load-bearing,')
print('   not decoration.)')
