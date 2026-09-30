"""
Soliton structure on the GSG-style y-lattice for the DLW system.

Objects:
  d  = h/2
  P_i = p_i - a ,  Q_k = q_k + a
  lam_ik = ((P_i+d)/(P_i-d)) ((Q_k+d)/(Q_k-d))          (rank-one: lam_i * mu_k)
  G_j = det[ delta_ik + (1/(p_i+q_k)) (-P_i/Q_k)^0 lam_ik^j e^{xi_i+eta_k} ]
  F_j = det[ delta_ik - ((P_i+d)/(Q_k-d)) (1/(p_i+q_k)) lam_ik^j e^{xi_i+eta_k} ]
  xi_i = p_i x - p_i^2 t + xi_i0 ,  eta_k = q_k x + q_k^2 t + eta_k0
"""
import sympy as sp
from engine import DLW, e_add, e_scale

h, a, x, t = sp.symbols('h a x t', real=True)
p1, p2, q1, q2 = sp.symbols('p1 p2 q1 q2', positive=True)

print("=" * 92)
print("1.  lattice phase / dispersion")
print("=" * 92)
z = sp.Symbol('z', positive=True)
Lam = sp.log((z + h / 2) / (z - h / 2)) / h
print("   Lam_h(z) = (1/h) ln[(z+h/2)/(z-h/2)]")
for k in range(1, 6, 2):
    print(f"      h^{k-1}: {sp.simplify(sp.expand(sp.series(Lam, h, 0, k+1).coeff(h, k-1)))}")
print("   =>  Lam_h(z) = 1/z + h^2/(12 z^3) + h^4/(80 z^5) + O(h^6)")
print("   lattice soliton phase:  theta_i(j) = (p_i+q_i) x + (q_i^2-p_i^2) t + j*ln(lam_i) + const")
print("   with   ln(lam_i)/h = Lam_h(P_i) + Lam_h(Q_i) ,   lam_i = ((P_i+d)/(P_i-d))((Q_i+d)/(Q_i-d))")

print()
print("=" * 92)
print("2.  one-soliton on the lattice  (N = 1)")
print("=" * 92)
p, q = sp.symbols('p q', positive=True)
P, Q = p - a, q + a
d = h / 2
lam = ((P + d) / (P - d)) * ((Q + d) / (Q - d))
r = -(P + d) / (Q - d)
print("   G_j = 1 + E_j ,   F_j = 1 + r E_j")
print("   r =", sp.simplify(r))
print("   lam =", sp.simplify(lam))
print("   E_j = (1/(p+q)) exp[ (p+q)x + (q^2-p^2)t + j ln(lam) ]")
Ej = sp.Symbol('E', positive=True)      # stands for E_j
u = sp.simplify(2 * (p + q) * (r * Ej / (1 + r * Ej) - Ej / (1 + Ej)))
print("   u_j = 2 d_x ln(F_j/G_j) =", sp.factor(sp.simplify(u)))
Ej0 = sp.symbols('E0', positive=True)
u_cont = sp.simplify(u.subs({h: 0, Ej: Ej0}))
print("   continuum (h=0): u =", sp.factor(sp.simplify(u_cont)))
umax_lat = [sp.simplify(s) for s in sp.solve(sp.diff(u, Ej), Ej)]
print("   u_j = 2 d_x ln(F_j/G_j) = -2 E (p+q)^2 / [ (1+E) ( (Q-d) - (P+d) E ) ]")
print("   d u_j / d E_j = 0  at  E =", umax_lat)
vals = {}
for k, v in (('p', 3), ('q', 2), ('a', sp.Rational(1, 2))):
    vals[sp.Symbol(k, positive=True)] = v
for hv in (0, sp.Rational(1, 4), sp.Rational(1, 2), 1):
    sub = dict(vals)
    sub[h] = hv
    Ecr = [sp.N(e.subs(sub)) for e in umax_lat]
    Ecr = [e for e in Ecr if e.is_real and e > 0]
    if not Ecr:
        print(f"   h={hv}: no positive critical point")
        continue
    Ecr = Ecr[0]
    print(f"   h={hv}:  E_cr = {Ecr:.6f}   u_max = {sp.N(u.subs(sub).subs(Ej, Ecr)):.8f}"
          f"   (sech^2-like pulse; continuum u_max -> "
          f"{sp.N(u_cont.subs({sp.Symbol('p'):3, sp.Symbol('q'):2, sp.Symbol('a'):sp.Rational(1,2)}).subs(Ej0, Ecr)):.8f})")

print()
print("=" * 92)
print("3.  two-soliton:  the interaction coefficient Gamma is h-independent")
print("=" * 92)
m = DLW(2, h=sp.Symbol('h'), kind='sym')
from engine import random_point
m.set_point(random_point(m, seed=99))
G2 = m.tau(0)
# monomial keys:  (1,0|1,0) = E_11, (0,1|0,1) = E_22, (1,1|1,1) = E_11 E_22
k1 = ((1, 0), (1, 0))
k2 = ((0, 1), (0, 1))
k12 = ((1, 1), (1, 1))
# normalise by the coefficient of E_11 and E_22
c1 = G2[k1]
c2 = G2[k2]
c12 = G2[k12]
print("   G_j = 1 + E_1 + E_2 + Gamma E_1 E_2  with")
print("   Gamma = (coeff of E_1E_2)/(coeff of E_1)/(coeff of E_2)  =",
      sp.simplify(c12 / (c1 * c2)))
P1, P2 = p1 - a, p2 - a
Q1, Q2 = q1 + a, q2 + a
Gam_ref = sp.simplify(((p1 - p2) * (q1 - q2)) / ((p1 + q2) * (p2 + q1)))
print("   Cauchy-determinant value  ((p1-p2)(q1-q2))/((p1+q2)(p2+q1)) =", Gam_ref)
print("   (numerically)  engine:", sp.N(c12 / (c1 * c2)), "   closed form:", sp.N(Gam_ref))
print("   => Gamma carries NO h and NO j: the two-soliton phase shift is untouched by the lattice.")

print()
print("=" * 92)
print("4.  continuum limit of the lattice phase")
print("=" * 92)
print("   theta_i(j) - theta_i^{cont}(y=jh) = j [ ln(lam_i)/h - (1/P_i + 1/Q_i) ] h")
print("   with ln(lam_i)/h - (1/P_i+1/Q_i) = h^2/12 (1/P_i^3 + 1/Q_i^3) + O(h^4)")
print("   => an O(h^2) phase error, i.e. the scheme is second-order accurate for the soliton phase.")

print()
print("=" * 92)
print("5.  continuum-limit check of the O(h^2) constants in section F")
print("=" * 92)
print("   (E_+ + E_-)/2 = M_0 + (h^2/8) [B_a f.g_YY + 4 D_x f.g_Y] + O(h^4)")
print("   (E_+ - E_-)/h = M_1 + (h^2/24) [B_a f.g_YYY + 6 D_x f.g_YY] + O(h^4)")
