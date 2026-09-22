"""
Decisive numeric verdict: which parts of the soliton structure does a PLAIN
FINITE DIFFERENCE keep?

    (7_j)   B f_j.g_j = 0
    (6d_j)  B f_j.(D_h g)_j + 2 D_x f_j.g_j = 0
    (D_h g)_j = (alpha g_{j+1} + beta g_j + gamma g_{j-1})/h
    theta-family: alpha=(1+s)/2, beta=-s, gamma=(s-1)/2

Two-soliton tau with FREE interaction coefficient Gam:
    g_j = 1 + A1 rho1^j E1 + A2 rho2^j E2 + Gam A1 A2 (rho1 rho2)^j E1 E2
    f_j = 1 + R1 A1 rho1^j E1 + R2 A2 rho2^j E2 + Gam R1 R2 A1 A2 (rho1 rho2)^j E1 E2

Question chain:
  1. single soliton  -> exact?            (rho_i from Lam(rho_i) = h*Cy_i)
  2. two soliton     -> does ANY Gam make every monomial vanish?
     if not, is (1,1) the only obstruction, or do the degree-3 monomials
     also obstruct?
"""
import sympy as sp
from collections import defaultdict

p1, p2, q1, q2, a, h = sp.symbols('p1 p2 q1 q2 a h')
s_ = sp.symbols('s')
rho1, rho2, Gam = sp.symbols('rho1 rho2 Gam')

A1, A2 = 1 / (p1 + q1), 1 / (p2 + q2)
R1, R2 = -(p1 - a) / (q1 + a), -(p2 - a) / (q2 + a)
GAMC = (p1 - p2) * (q1 - q2) / ((p1 + q2) * (p2 + q1))
CY1 = 1 / (p1 - a) + 1 / (q1 + a)
CY2 = 1 / (p2 - a) + 1 / (q2 + a)
PAR = dict(p1=1.3, p2=2.7, q1=0.9, q2=2.1, a=0.4)
CY1n = 1 / (PAR['p1'] - PAR['a']) + 1 / (PAR['q1'] + PAR['a'])
CY2n = 1 / (PAR['p2'] - PAR['a']) + 1 / (PAR['q2'] + PAR['a'])


def freqs(m):
    m1, m2 = m
    return (m1 * (p1 + q1) + m2 * (p2 + q2),
            m1 * (q1 ** 2 - p1 ** 2) + m2 * (q2 ** 2 - p2 ** 2))


def addm(m, n):
    return (m[0] + n[0], m[1] + n[1])


def Bpair(F, G, dxonly=False):
    out = defaultdict(lambda: sp.Integer(0))
    for mu, fmu in F.items():
        for nu, gnu in G.items():
            k1, w1 = freqs(mu)
            k2, w2 = freqs(nu)
            dk, dw = k1 - k2, w1 - w2
            out[addm(mu, nu)] += fmu * gnu * (dk if dxonly else dk ** 2 + dw + 2 * a * dk)
    return {m: sp.expand(v) for m, v in out.items()}


Gj = {(0, 0): 1, (1, 0): A1 * rho1, (0, 1): A2 * rho2,
      (1, 1): Gam * A1 * A2 * rho1 * rho2}
Fj = {(0, 0): 1, (1, 0): R1 * A1 * rho1, (0, 1): R2 * A2 * rho2,
      (1, 1): Gam * R1 * R2 * A1 * A2 * rho1 * rho2}


def Lam(x, sv):
    al, be, ga = (1 + sv) / 2, -sv, (sv - 1) / 2
    return al * x + be + ga / x


def build(sv):
    DhG = {m: c * Lam(rho1 ** m[0] * rho2 ** m[1], sv) / h for m, c in Gj.items()}
    eq = dict(Bpair(Fj, DhG))
    for m, v in Bpair(Fj, Gj, dxonly=True).items():
        eq[m] = eq.get(m, 0) + 2 * v
    return {m: sp.expand(v) for m, v in eq.items()}


def solve_rho(C, sv, hh):
    al, be, ga = (1 + sv) / 2, -sv, (sv - 1) / 2
    if al == 0:                       # backward: Lam = beta + gamma/x
        return 1.0 / (1.0 - hh * C / (-ga)) if False else 1.0 / (1.0 - hh * C)
    bb = be - hh * C
    disc = bb * bb - 4 * al * ga
    return max((-bb + disc ** 0.5) / (2 * al), (-bb - disc ** 0.5) / (2 * al))


print("=" * 78)
print("Which soliton structure survives a plain finite difference?")
print(f"parameters: {PAR}")
print("=" * 78)

for sv, label in [(0, "centred"), (1, "forward"), (-1, "backward")]:
    print()
    print(f"--- {label}  (s = {sv}) ---")
    eq = build(sv)
    sub0 = {**PAR, s_: sv}

    for hh in [0.1, 0.05]:
        sb = {**sub0, h: hh, rho1: solve_rho(CY1n, sv, hh),
              rho2: solve_rho(CY2n, sv, hh)}
        row = []
        # (a) single-soliton monomials
        e1 = abs(float(eq[(1, 0)].coeff(Gam, 0).subs(sb)))
        e2 = abs(float(eq[(0, 1)].coeff(Gam, 0).subs(sb)))
        # (b) each monomial as  c0 + c1*Gam
        info = {}
        for m, v in sorted(eq.items()):
            c0 = float(v.coeff(Gam, 0).subs(sb))
            c1 = float(v.coeff(Gam, 1).subs(sb))
            info[m] = (c0, c1)
        print(f"  h = {hh}")
        print(f"    single soliton : |E1| = {e1:.2e}   |E2| = {e2:.2e}")
        # solve (1,1) for Gam
        c0, c1 = info[(1, 1)]
        if c1 != 0:
            gstar = -c0 / c1
            gc = float(GAMC.subs(sub0))
            print(f"    Gamma from (1,1) : Gamma* = {gstar:+.10f}   "
                  f"Cauchy Gamma = {gc:+.10f}   diff = {abs(gstar-gc):.3e}")
            print(f"    with Gamma = Gamma*, remaining monomials:")
            for m in [(2, 1), (1, 2), (2, 2), (2, 0), (0, 2)]:
                if m in info:
                    v = info[m][0] + info[m][1] * gstar
                    print(f"        E1^{m[0]}E2^{m[1]} : {abs(v):.6e}")
            print(f"    with the CONTINUOUS Cauchy Gamma, residuals:")
            for m in [(1, 1), (2, 1), (1, 2)]:
                if m in info:
                    v = info[m][0] + info[m][1] * gc
                    print(f"        E1^{m[0]}E2^{m[1]} : {abs(v):.6e}")

print()
print("=" * 78)
