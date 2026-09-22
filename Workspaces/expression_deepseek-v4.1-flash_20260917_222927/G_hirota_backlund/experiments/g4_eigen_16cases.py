"""Check: does the eigenvalue of every pair of the four two-soliton monomials
vanish, given the DLW dispersion relations?  Independent of Lean.

The algebraic fact used: for monomials, k and w are additive, so
  eigen(mu,nu) = eigen_single(k_mu, w_mu) - eigen_single(k_nu, w_nu)
                 + 2*(delta parameter)*(k_mu - k_nu) - 2*delta*(...)
and the two single-mode dispersion residuals vanish.  Here we check the *raw*
expression for all 16 pairs after reducing the two dispersion relations.
"""
import sympy as sp

a, d, p1, p2, q1, q2 = sp.symbols('a d p1 p2 q1 q2')
k1, k2 = p1 + q1, p2 + q2
w1, w2 = q1**2 - p1**2, q2**2 - p2**2
vecs = {'00': (0, 0), '10': (1, 0), '01': (0, 1), '11': (1, 1)}

R1 = k1**2 + w1 + 2*a*k1          # = (p1+q1)(p1+q1+2a)
R2 = k2**2 + w2 + 2*a*k2


def reduce_expr(E):
    """Reduce E modulo the two dispersion relations (k_i^2 = -w_i - 2 a k_i)."""
    E = sp.expand(E)
    E = sp.expand(E.subs(k1**2, -w1 - 2*a*k1))
    E = sp.expand(E.subs(k2**2, -w2 - 2*a*k2))
    return sp.simplify(E)


bad = []
for nm, m in vecs.items():
    for nn, n in vecs.items():
        kk = (m[0] - n[0])*k1 + (m[1] - n[1])*k2
        ww = (m[0] - n[0])*w1 + (m[1] - n[1])*w2
        E = kk**2 + ww + 2*(a + d)*kk
        r = reduce_expr(E)
        if r != 0:
            bad.append((nm, nn, sp.factor(sp.expand(E)), r))
print('pairs examined: 16')
print('pairs whose eigenvalue does NOT vanish:', len(bad))
for nm, nn, E, r in bad:
    print(' ', nm, nn, '->', E, ' reduces to ', r)

# second, independent check: plugging rational numbers
subs = {a: sp.Rational(2), d: sp.Rational(1, 10), p1: sp.Rational(7, 3),
        p2: sp.Rational(13, 6), q1: sp.Rational(3), q2: sp.Rational(10, 3)}
bad2 = []
for nm, m in vecs.items():
    for nn, n in vecs.items():
        kk = (m[0] - n[0])*k1 + (m[1] - n[1])*k2
        ww = (m[0] - n[0])*w1 + (m[1] - n[1])*w2
        E = (kk**2 + ww + 2*(a + d)*kk).subs(subs)
        if sp.nsimplify(E) != 0:
            bad2.append((nm, nn, sp.nsimplify(E)))
print('numeric check failures:', len(bad2), bad2)
