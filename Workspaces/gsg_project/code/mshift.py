"""Exact parameter-renormalisation identity for the lattice one-soliton.

Claim:  u_lattice(E; p,q,a,h)  ==  u_continuum(E; p,q, a - h/2)   (identically in E)
and     ln(lambda)/h = 1/P + 1/Q + h^2/12 (1/P^3 + 1/Q^3) + h^4/80 (1/P^5 + 1/Q^5) + ...
"""
import sympy as sp

p, q, a, h = sp.symbols('p q a h', positive=True)
E = sp.Symbol('E', positive=True)
d = h / 2

u_lat = sp.simplify(-2 * E * (p + q) ** 2 / ((1 + E) * ((q + a - d) - (p - a + d) * E)))
a2 = a - h / 2
u_cont_shift = sp.simplify(-2 * E * (p + q) ** 2 / ((1 + E) * ((q + a2) - (p - a2) * E)))
print("u_lat - u_cont(a -> a-h/2) =", sp.simplify(u_lat - u_cont_shift))
print()

z = sp.Symbol('z', positive=True)
# (1/h) ln[(z+h/2)/(z-h/2)] = (2/h) arctanh(h/(2z))
S = 2 * sp.atanh(h / (2 * z)) / h
print("Lam_h(z) = (1/h) ln[(z+h/2)/(z-h/2)] = (2/h) arctanh(h/(2z))")
for k in range(1, 8, 2):
    c = sp.simplify(sp.series(S, h, 0, k + 1).coeff(h, k - 1))
    print(f"   coefficient of h^{k-1}:", c)
print()
print("=> the lattice one-soliton PROFILE equals the continuum profile at a-h/2 EXACTLY;")
print("   the y-phase equals the continuum phase at a up to O(h^2).")
