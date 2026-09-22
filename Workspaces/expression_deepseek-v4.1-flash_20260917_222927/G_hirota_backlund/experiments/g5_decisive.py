"""Decisive verification of the two-soliton staggered candidate.

Two independent computations of the SAME quantity:
  (A) direct partial differentiation of explicit F_j, G_j built from
      det(I+M) with the staggered amplitudes rho^j, gamma;
  (B) the mode-sum expansion used in the audit scripts.

If they disagree, the mode-sum/eigen bookkeeping is wrong.
"""
import sympy as sp

x, t = sp.symbols('x t')
a = sp.Rational(2)
h = sp.Rational(1, 10)
d = h / 2
p1, p2 = sp.Rational(7, 3), sp.Rational(13, 6)
q1, q2 = sp.Rational(3), sp.Rational(10, 3)
j = sp.Integer(0)
s = a - d

P1, P2, Q1, Q2 = p1 - a, p2 - a, q1 + a, q2 + a
rho1 = (P1 + d) * (Q1 + d) / ((P1 - d) * (Q1 - d))
rho2 = (P2 + d) * (Q2 + d) / ((P2 - d) * (Q2 - d))
r1 = -(P1 + d) / (Q1 - d)
r2 = -(P2 + d) / (Q2 - d)
Gam = (p1 - p2) * (q1 - q2) / ((p1 + q1) * (p1 + q2) * (p2 + q1) * (p2 + q2))
E1 = rho1 ** j * sp.exp((p1 + q1) * x + (q1 ** 2 - p1 ** 2) * t)
E2 = rho2 ** j * sp.exp((p2 + q2) * x + (q2 ** 2 - p2 ** 2) * t)
G = 1 + E1 / (p1 + q1) + E2 / (p2 + q2) + Gam * E1 * E2
F = 1 + r1 * E1 / (p1 + q1) + r2 * E2 / (p2 + q2) + Gam * r1 * r2 * E1 * E2
print('rho =', sp.nsimplify(rho1), sp.nsimplify(rho2))
print('r   =', sp.nsimplify(r1), sp.nsimplify(r2))
print('Gam =', sp.nsimplify(Gam))

def B(sv, f, g):
    return (sp.diff(f, x, 2) * g - 2 * sp.diff(f, x) * sp.diff(g, x) + f * sp.diff(g, x, 2)
            + sp.diff(f, t) * g - f * sp.diff(g, t)
            + 2 * sv * (sp.diff(f, x) * g - f * sp.diff(g, x)))

res = sp.expand(B(s, F, G))
# coefficient of E1^2 : extract by treating E1,E2 as symbols
Xs, Ys = sp.symbols('E1 E2')
# substitute exp(...) -> symbols
Xv = sp.exp((p1 + q1) * x + (q1 ** 2 - p1 ** 2) * t)
Xv2 = sp.exp((p2 + q2) * x + (q2 ** 2 - p2 ** 2) * t)
res2 = sp.expand(sp.simplify(res.subs({Xv: Xs, Xv2: Ys})))
poly = sp.Poly(sp.expand(res2), Xs, Ys)
print()
print('direct residual, as polynomial in E1, E2:')
for mon, co in zip(poly.monoms(), poly.coeffs()):
    print('   E1^%d E2^%d ->' % mon, sp.nsimplify(sp.simplify(co)))

# now the mode sum
print()
print('mode sum (coefficient of E1^2, i.e. mode (2,0)):')
FT = {(0, 0): sp.Integer(1), (1, 0): r1 / (p1 + q1), (0, 1): r2 / (p2 + q2),
      (1, 1): Gam * r1 * r2}
GT = {(0, 0): sp.Integer(1), (1, 0): 1 / (p1 + q1), (0, 1): 1 / (p2 + q2),
      (1, 1): Gam}
kk = {(0, 0): 0, (1, 0): p1 + q1, (0, 1): p2 + q2, (1, 1): p1 + q1 + p2 + q2}
ww = {(0, 0): 0, (1, 0): q1 ** 2 - p1 ** 2, (0, 1): q2 ** 2 - p2 ** 2,
      (1, 1): q1 ** 2 - p1 ** 2 + q2 ** 2 - p2 ** 2}
acc = {}
for m, cf in FT.items():
    for M, cg in GT.items():
        key = (m[0] + M[0], m[1] + M[1])
        dk, dw = kk[m] - kk[M], ww[m] - ww[M]
        acc[key] = acc.get(key, sp.Integer(0)) + cf * cg * (dk ** 2 + dw + 2 * s * dk)
for key in sorted(acc):
    print('   mode', key, '->', sp.nsimplify(sp.simplify(acc[key])))
