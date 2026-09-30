"""
N=1 fully symbolic: find the exact two-site identity replacing (6).

tau:  g = c + A0 E,  f = c + A1 E,
  A_n = (-P/Q)^n /(p+q),  P = p-a, Q = q+a
  E = exp(theta),  theta_x = p+q, theta_t = q^2 - p^2
  lattice: E -> chi^j * exp(...),  chi = (P/(P-h))*(Q/(Q-h))
"""
import sympy as sp

p, q, a, h, c = sp.symbols('p q a h c', positive=True)
P, Q = p - a, q + a
E = sp.Symbol('E', positive=True)          # phase exponential at site j (generic value)
chi = (P / (P - h)) * (Q / (Q - h))        # one-step multiplier of E


def A(n):
    return (-P / Q) ** n / (p + q)


# theta rates
thx, tht = p + q, q ** 2 - p ** 2


def dx(F, G):
    return thx * (F[1] * G[0] - F[0] * G[1])   # placeholder, unused


def bil(F0, F1, G0, G1, ax=0, at=0):
    """D_x^ax D_t^at (F0 + F1 E).(G0 + G1 E), symbolically in E."""
    from math import comb
    # derivatives: d_x^r (F0+F1 E) = F1 (thx)^r E for r>0 ; = F0+F1 E for r=0
    def der(F0, F1, var, r):
        rate = thx if var == 'x' else tht
        if r == 0:
            return (F0, F1)
        return (0, F1 * rate ** r)
    tot = 0
    for i in range(ax + 1):
        for k in range(at + 1):
            co = (-1) ** (i + k) * comb(ax, i) * comb(at, k)
            fpart = der(der(F0, F1, 'x', ax - i), 0, 't', at - k) if False else None
    # do it more directly
    res_E = {0: 0, 1: 0, 2: 0}
    for i in range(ax + 1):
        for k in range(at + 1):
            co = (-1) ** (i + k) * comb(ax, i) * comb(at, k)
            df = (0, F1 * thx ** (ax - i) * tht ** (at - k)) if (ax - i + at - k) > 0 else (F0, F1)
            dg = (0, G1 * thx ** i * tht ** k) if (i + k) > 0 else (G0, G1)
            # product (df0 + df1 E)(dg0 + dg1 E)
            res_E[0] += co * df[0] * dg[0]
            res_E[1] += co * (df[0] * dg[1] + df[1] * dg[0])
            res_E[2] += co * df[1] * dg[1]
    return sum(res_E[r] * E ** r for r in res_E if res_E[r] != 0)


def Bop(F0, F1, G0, G1, aa):
    return sp.expand(bil(F0, F1, G0, G1, 2, 0) + bil(F0, F1, G0, G1, 0, 1)
                     + 2 * aa * bil(F0, F1, G0, G1, 1, 0))


g0, g1 = c, A(0)
f0, f1 = c, A(1)

# (D7) site-wise
r7 = Bop(f0, f1, g0, g1, a)
print("(D7) B f.g =", sp.factor(r7))

# two-site pieces:  f_{j+1} = f0 + f1*chi*E etc.
two_site = sp.expand(Bop(f0, f1 * chi, g0, g1, a) - Bop(f0, f1, g0, g1 * chi, a))
dxf = sp.expand(bil(f0, f1, g0, g1, 1, 0))
print("\n(1/h)[B f1.g - B f.g1] =")
TS = sp.factor(two_site / h)
print("  ", TS)
print("\nD_x f.g =")
print("  ", sp.factor(dxf))
print("\nratio (1/h)[...]/ D_x f.g =")
print("  ", sp.factor(TS / dxf))
