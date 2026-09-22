"""
A-route bilinearisation audit  (reviewing agent's analysis).

Can the "simple finite difference" road of route A be pushed to
(i) a DISCRETE BILINEAR form and (ii) (N-)soliton structure?

Answer: NO.  Four exact obstructions, plus the contrast that shows what the
staggered construction does differently.

Notation (Sheng-Yu, Physica D 432 (2022) 133140):
    B = D_x^2 + D_t + 2a D_x ,   (7) B f.g = 0 ,   (6) [D_y B + 2 lam D_x] f.g = 0
    N=1 Gram data (c_1 = 0):  tau_n = 1 + A E,  A = R^n/(p+q),
    R = -(p-a)/(q+a),  E = exp(xi+eta),  f = tau_{n+1} = 1 + R A E,  g = tau_n
"""
import sympy as sp

p, q, a, lam, h = sp.symbols('p q a lam h')
A, E = sp.symbols('A E', positive=True)
j = sp.symbols('j', integer=True)
kappa = sp.symbols('kappa', positive=True)
d = h / 2
P, Q = p - a, q + a
R = -P / Q

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        failures.append(name)
    if detail:
        for line in str(detail).splitlines():
            print(f"        {line}")


def simp(e):
    return sp.factor(sp.simplify(sp.expand(e)))


f = 1 + R * A * E
g = 1 + A * E

# chain rule:  d_x E = (p+q) E ,  d_t E = (q^2-p^2) E ,  d_y E = (1/P + 1/Q) E
Cx, Ct, Cy = p + q, q**2 - p**2, 1 / P + 1 / Q
dx = lambda e: sp.diff(e, E) * Cx * E
dt = lambda e: sp.diff(e, E) * Ct * E
dy = lambda e: sp.diff(e, E) * Cy * E

Dx = lambda F, G: dx(F) * G - F * dx(G)
Dt = lambda F, G: dt(F) * G - F * dt(G)
Dx2 = lambda F, G: dx(dx(F)) * G - 2 * dx(F) * dx(G) + F * dx(dx(G))
B = lambda F, G: sp.expand(Dx2(F, G) + Dt(F, G) + 2 * a * Dx(F, G))

print("=" * 78)
print("A-route bilinearisation audit: simple finite difference -> discrete")
print("bilinear form -> solitons?")
print("=" * 78)

check("CHECK 1  B f.g = 0   (paper's equation (7), exact for all parameters)",
      simp(B(f, g)) == 0, f"B f.g = {simp(B(f, g))}")

Dxfg = simp(Dx(f, g))
check("CHECK 2  D_x f.g = -A E (p+q)^2/(q+a)  != 0 generically",
      sp.simplify(Dxfg + A * E * (p + q) ** 2 / (q + a)) == 0, f"D_x f.g = {Dxfg}")

# ---------------------------------------------------------------- (F1)
print()
print("(F1) COLLAPSE at fixed operator parameter a:")
print("     B f_j.g_j = 0 at EVERY site => any difference of it vanishes,")
print("     so the difference-discretised (6) degenerates to 2*lam*D_x f.g = 0.")
forced = simp(sp.together(Dxfg / (A * E) * (q + a)))
check("CHECK 3  degenerate equation holds only on the branch p+q = 0",
      sp.simplify(forced + (p + q) ** 2) == 0,
      f"D_x f.g/(A E) = {sp.together(Dxfg/(A*E))}   (zero iff p+q = 0)")

# ---------------------------------------------------------------- (F2)
print()
print("(F2) on the locus, (6) is EQUIVALENT to  B f.g_y + 2 D_x f.g = 0 ;")
print("     all y-information sits in the single bilinear form B(f.g_y).")
lhs = simp(B(f, dy(g)))
check("CHECK 4  B f.g_y = -2 D_x f.g   hence  B f.g_y + 2 D_x f.g = 0",
      sp.simplify(lhs + 2 * Dxfg) == 0, f"B f.g_y = {lhs}")

# ---------------------------------------------------------------- (F3)
print()
print("(F3) replacing g_y by a CENTRED difference in j:")
print("     since B is linear in its second slot,")
print("         B(f_j, (g_{j+1}-g_{j-1})/(2h)) = [ratio] * B(f_j, g_y)")
rho = sp.symbols('rho', positive=True)
gj = 1 + A * rho**j * E
centred = (gj.subs(j, j + 1) - gj.subs(j, j - 1)) / (2 * h)
exact = sp.diff(gj, j) / h                       # d_y of the geometric tau
ratio = sp.simplify(sp.expand(centred / exact))
check("CHECK 5  ratio = sinh(kappa)/kappa   (kappa = log rho), deficit kappa^2/6",
      sp.simplify(ratio - (rho - 1 / rho) / (2 * sp.log(rho))) == 0
      and abs(float(ratio.subs(rho, 2)) - float(sp.sinh(sp.log(2)) / sp.log(2))) < 1e-12,
      f"ratio = {ratio}  = (rho - 1/rho)/(2 log rho) = sinh(kappa)/kappa\n"
      f"numeric rho=2: {float(ratio.subs(rho, 2)):.12f}\n"
      f"sinh(k)/k - 1 = {sp.series(sp.sinh(kappa)/kappa - 1, kappa, 0, 5).removeO()}")
check("CHECK 6  no lattice factor can fix it: sinh(kappa)=kappa only at kappa=0",
      sp.simplify(sp.series(sp.sinh(kappa) - kappa, kappa, 0, 5).removeO()) != 0,
      "so the discrete bilinear equation has residual "
      "2*D_x f.g*(1 - sinh(kappa)/kappa) != 0 for every h > 0")

# ---------------------------------------------------------------- (F4)
print()
print("(F4) the CONSTRAINT is transcendental, not bilinear:")
print("     w_j = (u_{j+1}-u_{j-1})/(2h), u_j = 2 d_x ln(f_j/g_j)  forces")
print("         exp(h phi_j) = f_{j+1} g_{j-1} / (g_{j+1} f_{j-1}) ,  d_x phi_j = w_j")
alpha, beta, phi, psi = sp.symbols('alpha beta phi psi', positive=True)
fsep, gsep = phi * alpha**j, psi * beta**j
sepv = sp.simplify(sp.expand_log(
    sp.log((fsep.subs(j, j + 1) * gsep.subs(j, j - 1))
           / (gsep.subs(j, j + 1) * fsep.subs(j, j - 1))) / h, force=True))
check("CHECK 7  separable tau => phi_j independent of j => w_j = d_x phi_j = 0",
      sp.simplify(sp.diff(sepv, sp.Symbol('x'))) == 0, f"phi_j = {sepv}")

# ---------------------------------------------------------------- (F5)
print()
print("(F5) CONTRAST: the staggered scheme is exact at N=1 because it shifts the")
print("     OPERATOR PARAMETER (s = a -+ h/2) at neighbouring sites, instead of")
print("     differencing the tau in y.  (Set j = 0; the equations carry no d_y.)")
rhos = ((P + d) * (Q + d)) / ((P - d) * (Q - d))
r = -(P + d) / (Q - d)
M0 = E / (p + q)
F0, G0, G1 = 1 + r * M0, 1 + M0, 1 + rhos * M0
e1 = sp.simplify(sp.expand(Dx2(F0, G0) + Dt(F0, G0) + (2 * a - h) * Dx(F0, G0)))
e2 = sp.simplify(sp.expand(Dx2(F0, G1) + Dt(F0, G1) + (2 * a + h) * Dx(F0, G1)))
check("CHECK 8  (B - hD_x)F_j.G_j = 0  and  (B + hD_x)F_j.G_{j+1} = 0  exactly",
      e1 == 0 and e2 == 0, f"(B-hD_x)F.G = {e1}\n(B+hD_x)F.G+ = {e2}")

ser = sp.series(sp.log(rhos) / h, h, 0, 4).removeO()
check("CHECK 9  staggered log(rho)/h = 1/P + 1/Q + h^2/12 (1/P^3 + 1/Q^3) + O(h^4)",
      sp.simplify(ser - (1 / P + 1 / Q + h**2 / 12 * (1 / P**3 + 1 / Q**3))) == 0,
      "series verified against  1/P + 1/Q + h^2/12 (1/P^3 + 1/Q^3)")

print()
print("=" * 78)
print("FAILURES: " + str(failures) if failures else "ALL CHECKS PASSED")
print("=" * 78)
