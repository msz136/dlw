"""
Definitive checks for the GSG-style semi-discretisation of the DLW bilinear pair (6),(7).

  A. continuum baseline: (7) and (6) from the DLW Gram tau          [exact, N<=6]
  B. (7) survives the y-lattice at every site (all multipliers)     [exact]
  C. the naive lattice replacement of (6) fails                     [exact, N=1 closed form]
  D. site shift == spectral shift                                   [exact identity]
  E. the staggered lattice bilinear pair                            [exact, N<=5]
  F. continuum limit of the pair, exact jets in h
"""
import sympy as sp
from math import comb
from engine import DLW, e_add, e_scale, zero_at_points, random_point

x, y, t, h, a = sp.symbols('x y t h a', real=True)
H = sp.Rational(1, 3)

print("=" * 94)
print("A. continuum baseline  (kind='none')")
print("=" * 94)
for N in (1, 2, 3, 4, 5, 6):
    ok7, _ = zero_at_points(lambda m: m.B(m.tau(1), m.tau(0)), N, trials=2, kind='none')
    ok6, _ = zero_at_points(
        lambda m: e_add(m.DyB(m.tau(1), m.tau(0)), e_scale(m.Dx(m.tau(1), m.tau(0)), -4)),
        N, trials=2, kind='none')
    print(f"   N={N}:  (7) Bf.g = 0 -> {'OK' if ok7 else 'FAIL'}"
          f"     (6)@lam=-2  D_yBf.g - 4D_xf.g = 0 -> {'OK' if ok6 else 'FAIL'}", flush=True)

print()
print("=" * 94)
print("B. (7) is exact on the y-lattice at EVERY site, for every multiplier")
print("=" * 94)
for kind in ('exp', 'expneg', 'sym'):
    row = []
    for N in (1, 2, 3):
        ok, _ = zero_at_points(lambda m: m.B(m.tau(1), m.tau(0)), N,
                               trials=2, h=H, kind=kind)
        row.append(f"N={N}:{'OK' if ok else 'FAIL'}")
    print(f"   kind={kind:7s} " + "   ".join(row), flush=True)

print()
print("=" * 94)
print("C. exact N=1 defect of the naive lattice replacement of (6)")
print("    (1/h)[B f_{j+1}.g_j - B f_j.g_{j+1}] + 4 D_x f_j.g_j = 4 c chi^j e^{theta} * Delta")
print("=" * 94)
p, q = sp.symbols('p q', positive=True)
P, Q = p - a, q + a
for name, chi in (("literal GSG   chi = (1-h/P)^-1 (1-h/Q)^-1", P * Q / ((P - h) * (Q - h))),
                  ("central       chi = ((P+h/2)/(P-h/2))((Q+h/2)/(Q-h/2))",
                   ((P + h / 2) / (P - h / 2)) * ((Q + h / 2) / (Q - h / 2)))):
    D = sp.factor(sp.simplify(P * (1 - chi) / h + (p + q) / Q))
    print(f"   {name}\n      Delta = {D}")
print("   => Delta is exactly h x (nonzero rational function): the naive scheme is")
print("      first order only, and (6) is NOT an exact lattice identity.")

print()
print("=" * 94)
print("D. exact identity  tau_1(j+1 ; a) = tau_1(j ; a-h)")
print("=" * 94)
for N in (1, 2, 3, 4):
    m = DLW(N, h=sp.Symbol('h'), kind='sym')
    m.set_point(random_point(m, seed=5 + N))
    lhs = m.tau(1, jshift=1, a_shift=+m.h / 2)
    rhs = m.tau(1, jshift=0, a_shift=-m.h / 2)
    same = (lhs.keys() == rhs.keys()) and all(sp.simplify(lhs[k] - rhs[k]) == 0 for k in lhs)
    print(f"   N={N}: {'OK' if same else 'FAIL'}")

print()
print("=" * 94)
print("E. staggered lattice bilinear pair   (d = h/2)")
print("     (7)_h :  B_(a-d) F_j . G_j      = 0        F_j = tau_1(j; a-d), G_j = tau_0(j)")
print("     (6)_h :  B_(a+d) F_j . G_(j+1)  = 0        G_(j+1) = tau_0(j+1)")
print("=" * 94)
for N in (1, 2, 3, 4, 5):
    okm, _ = zero_at_points(
        lambda m: m.B(m.tau(1, a_shift=-m.h / 2), m.tau(0), s=m.a - m.h / 2),
        N, trials=2, h=H, kind='sym')
    okp, _ = zero_at_points(
        lambda m: m.B(m.tau(1, a_shift=-m.h / 2), m.tau(0, jshift=1), s=m.a + m.h / 2),
        N, trials=2, h=H, kind='sym')
    print(f"   N={N}:  (7)_h -> {'OK' if okm else 'FAIL'}    (6)_h -> {'OK' if okp else 'FAIL'}", flush=True)

print()
print("=" * 94)
print("F. continuum limit of the lattice pair (exact jet Taylor expansion in h)")
print("=" * 94)
jet = {}


def jf(name, nx, ny, nt):
    k = (name, nx, ny, nt)
    if k not in jet:
        jet[k] = sp.Symbol(f'{name}_{nx}_{ny}_{nt}')
    return jet[k]


def bilk(ax, at, k):
    """(D_x^ax D_t^at F) . (d_Y^k G),  both read at the reference point Y."""
    tot = 0
    for pp in range(ax + 1):
        for rr in range(at + 1):
            co = (-1) ** (pp + rr) * comb(ax, pp) * comb(at, rr)
            tot += co * jf('F', ax - pp, 0, at - rr) * jf('G', pp, k, rr)
    return sp.expand(tot)


def Bk(s, k):
    return sp.expand(bilk(2, 0, k) + bilk(0, 1, k) + 2 * s * bilk(1, 0, k))


ORD = 8
E_plus = sp.expand(sum((h / 2) ** k / sp.factorial(k) * Bk(a + h / 2, k) for k in range(ORD + 1)))
E_minus = sp.expand(sum((-h / 2) ** k / sp.factorial(k) * Bk(a - h / 2, k) for k in range(ORD + 1)))


def taylor(expr, order):
    e = sp.expand(expr)
    return sp.expand(sum(sp.expand(e.diff(h, k).subs(h, 0)) / sp.factorial(k) * h ** k
                        for k in range(order + 1)))


ref_sym = Bk(a, 0)                                       # = B_a f.g              -> (7)
ref_diff = Bk(a, 1) + 2 * bilk(1, 0, 0)                  # = B_a f.g_Y + 2 D_x f.g -> (6), lam=-2

sym_lim = taylor((E_plus + E_minus) / 2, ORD)
diff_lim = taylor((E_plus - E_minus) / h, ORD)

print("   [1]  (E_+ + E_-)/2  -  B_a f.g                   =",
      sp.factor(sp.simplify(sp.expand(sym_lim - ref_sym))))
print("   [2]  (E_+ - E_-)/h  -  [B_a f.g_Y + 2 D_x f.g]    =",
      sp.factor(sp.simplify(sp.expand(diff_lim - ref_diff))))
print()
print("   with M_0 := B_a f.g,  M_1 := B_a f.g_Y + 2 D_x f.g :")
print("     (E_+ + E_-)/2 = M_0 + (h^2/8) M_2 + (h^4/384) M_4 + ...")
print("     (E_+ - E_-)/h = M_1 + (h^2/24) M_3 + (h^4/1920) M_5 + ...")
print("   M_2 =", sp.factor(Bk(a, 2) + 4 * bilk(1, 0, 1)))
print("   M_3 =", sp.factor(Bk(a, 3) + 6 * bilk(1, 0, 2)))
print()
print("   check (E_++E_-)/2 - M_0 - h^2/8*M_2 :",
      sp.simplify(sp.expand(sym_lim - ref_sym - h ** 2 / 8 * (Bk(a, 2) + 4 * bilk(1, 0, 1)))))
print("   check (E_+-E_-)/h - M_1 - h^2/24*M_3 :",
      sp.simplify(sp.expand(diff_lim - ref_diff - h ** 2 / 24 * (Bk(a, 3) + 6 * bilk(1, 0, 2)))))
