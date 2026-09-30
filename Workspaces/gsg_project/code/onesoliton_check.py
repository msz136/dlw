"""Numerical cross-check of the lattice one-soliton against the paper's (27)."""
import sympy as sp

p, q, a, h = sp.symbols('p q a h', positive=True)
d = h / 2
P, Q = p - a, q + a
lam = ((P + d) / (P - d)) * ((Q + d) / (Q - d))
r = -(P + d) / (Q - d)

# lattice one-soliton:  F_j = 1 + r E , G_j = 1 + E ,  u = 2 d_x ln(F/G)
E = sp.Symbol('E', positive=True)
u_lat = sp.simplify(2 * (p + q) * (r * E / (1 + r * E) - E / (1 + E)))
print("u_lattice(E) =", sp.factor(u_lat))
print("u_cont   (E) =", sp.factor(sp.simplify(u_lat.subs(h, 0))))

# paper (27) with exp(theta) = (p+q) sqrt((a+q)/(a-p))
theta = sp.log((p + q) * sp.sqrt((a + q) / (a - p)))
# E = exp(xi+eta)/(p+q); the paper's cosh argument is xi+eta-theta  =>
# exp(xi+eta) = (p+q) E,  so cosh(xi+eta-theta) = [(p+q)E e^{-theta} + e^{theta}/((p+q)E)]/2
cosh_arg = ((p + q) * E * sp.exp(-theta) + sp.exp(theta) / ((p + q) * E)) / 2
u_paper = -2 * (p + q) ** 2 / (sp.sqrt(2) * (a - p) * (a + q) * cosh_arg + (2 * a - p + q))
print("difference (paper 27) - (our h=0) =",
      sp.simplify(sp.expand(sp.simplify(sp.together(u_paper - u_lat.subs(h, 0))))))

vals = {p: sp.Integer(1), q: sp.Integer(2), a: sp.Integer(3)}
print()
print("numeric spot check  p=1,q=2,a=3  (so a-p=2>0, a+q=5>0, PQ<0 : regular):")
print("   E        u_paper           u_cont(h=0)       u_lat(h=1/4)      u_lat(h=1/2)")
for Ev in (sp.Rational(1, 10), sp.Rational(1, 4), 1, 2, 4, 10):
    e = {E: Ev}
    up = u_paper.subs(vals).subs(e)
    uc = u_lat.subs(h, 0).subs(vals).subs(e)
    u1 = u_lat.subs(h, sp.Rational(1, 4)).subs(vals).subs(e)
    u2 = u_lat.subs(h, sp.Rational(1, 2)).subs(vals).subs(e)
    print(f"   {float(Ev):<6.3g} {float(up):<17.8f} {float(uc):<17.8f} {float(u1):<17.8f} {float(u2):<17.8f}")

print()
print("lattice phase: lam =", sp.simplify(lam))
print("   ln(lam)/h =", sp.simplify(sp.log(lam) / h), " (-> 1/P + 1/Q as h->0)")
print("   regular when (P+d)(Q-d) < 0, i.e. the lattice generalises (a-p)(a+q) > 0")
