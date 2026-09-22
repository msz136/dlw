"""
N=1 symbolic hunt for the exact lattice identity replacing (6).

Facts so far (N=1, exact):
  (1/h)[B f1.g - B f.g1] / (D_x f.g) = 4 chi (1 - h/(p+q)),  chi = chi_p chi_q
  site-wise (D7) B f.g = 0 exact.

Try: centered differences, cross D_x pairings, shifted D_x.
"""
import sympy as sp

p, q, a, h, c = sp.symbols('p q a h c', positive=True)
P, Q = p - a, q + a
E = sp.Symbol('E', positive=True)
chi = (P / (P - h)) * (Q / (Q - h))

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


# tau at shifted sites: multiply E-coefficient by chi^s
def f(s):
    return (c, A(1) * chi ** s)


def g(s):
    return (c, A(0) * chi ** s)


def Bfg(sf, sg):
    F, G = f(sf), g(sg)
    return Bop(F[0], F[1], G[0], G[1], a)


def Dxfg(sf, sg):
    F, G = f(sf), g(sg)
    return sp.expand(bil(F[0], F[1], G[0], G[1], 1, 0))


dxj = Dxfg(0, 0)

cands = {
    '(1/h)[B f1.g - B f.g1]': (Bfg(1, 0) - Bfg(0, 1)) / h,
    '(1/2h)[B f1.g-1 - B f-1.g1]': (Bfg(1, -1) - Bfg(-1, 1)) / (2 * h),
    '(1/h)[B f.g-1 - B f-1.g]': (Bfg(0, -1) - Bfg(-1, 0)) / h,
}
for name, expr in cands.items():
    print(f"{name:34s} / Dx f.g = {sp.factor(expr / dxj)}")

print()
dx_cands = {
    'Dx f.g @j': dxj,
    'Dx f.g @j+1': Dxfg(1, 1),
    '(1/h^2?) none': 0,
    'Dx f1.g-1': Dxfg(1, -1),
    'Dx f-1.g1': Dxfg(-1, 1),
    'Dx f1.g': Dxfg(1, 0),
    'Dx f.g1': Dxfg(0, 1),
}
base = cands['(1/h)[B f1.g - B f.g1]']
for name, expr in dx_cands.items():
    if expr == 0:
        continue
    print(f"(1/h)[B f1.g - B f.g1] / {name:12s} = {sp.factor(base / expr)}")
