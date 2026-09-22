"""
N=1, y-lattice with GENERAL one-step multiplier chi (E -> chi E).
Compute (1/h)[B f1.g - B f.g1] / (D_x f.g) symbolically in chi.
Also with B evaluated at shifted a.
"""
import sympy as sp

p, q, a, h, c, chi = sp.symbols('p q a h c chi', positive=True)
P, Q = p - a, q + a
E = sp.Symbol('E', positive=True)
thx, tht = p + q, q ** 2 - p ** 2


def A(n):
    return (-P / Q) ** n / (p + q)


def bil(F0, F1, G0, G1, ax=0, at=0):
    from math import comb
    res = {0: 0, 1: 0, 2: 0}
    for i in range(ax + 1):
        for k in range(at + 1):
            co = (-1) ** (i + k) * comb(ax, i) * comb(at, k)
            df = (0, F1 * thx ** (ax - i) * tht ** (at - k)) if (ax - i + at - k) > 0 else (F0, F1)
            dg = (0, G1 * thx ** i * tht ** k) if (i + k) > 0 else (G0, G1)
            res[0] += co * df[0] * dg[0]
            res[1] += co * (df[0] * dg[1] + df[1] * dg[0])
            res[2] += co * df[1] * dg[1]
    return sum(res[r] * E ** r for r in res if res[r] != 0)


def Bop(F0, F1, G0, G1, aa):
    return sp.expand(bil(F0, F1, G0, G1, 2, 0) + bil(F0, F1, G0, G1, 0, 1)
                     + 2 * aa * bil(F0, F1, G0, G1, 1, 0))


g0, g1 = c, A(0)
f0, f1 = c, A(1)

# general chi: f_{j+1} = f0 + f1*chi*E
two_site = sp.expand(Bop(f0, f1 * chi, g0, g1, a) - Bop(f0, f1, g0, g1 * chi, a))
dxf = sp.expand(bil(f0, f1, g0, g1, 1, 0))
print("(B f1.g - B f.g1) =")
print("  ", sp.factor(two_site))
print("\nD_x f.g =")
print("  ", sp.factor(dxf))
print("\nratio =")
print("  ", sp.factor(two_site / dxf))

# what if B uses a shifted parameter a+s ?
s = sp.Symbol('s')
two_site_s = sp.expand(Bop(f0, f1 * chi, g0, g1, a + s) - Bop(f0, f1, g0, g1 * chi, a + s))
print("\nwith a -> a+s:  ratio =")
print("  ", sp.factor(two_site_s / dxf))
