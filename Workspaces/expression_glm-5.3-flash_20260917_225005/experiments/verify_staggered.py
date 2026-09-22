# -*- coding: utf-8 -*-
"""Staggered tau system checks (fast strategy).

A. General one-soliton dispersion: SYMBOLIC (small expressions, cancel).
B. Two-soliton residuals: EXACT RANDOM-RATIONAL CERTIFICATION (Schwartz-Zippel
   style experiment; general-parameter symbolic proof is delegated to Lean by
   direction G). Exact arithmetic via sympy Rational, several random points.
C. Centered (same-site) candidate one-soliton dispersion record.
"""
import sympy as sp
from sympy import Rational, S

a, h, p1, p2, q1, q2 = sp.symbols('a h p1 p2 q1 q2')
d = h/2
P1, P2, Q1, Q2 = p1 - a, p2 - a, q1 + a, q2 + a
rho1 = (P1 + d)*(Q1 + d)/((P1 - d)*(Q1 - d))
r1 = -(P1 + d)/(Q1 - d)
Gc = (p1 - p2)*(q1 - q2)/((p1 + q1)*(p1 + q2)*(p2 + q1)*(p2 + q2))

def bil(F, G, ops):
    out = {}
    for (a1, b1), f in F.items():
        for (a2, b2), g in G.items():
            key = (a1 + a2, b1 + b2)
            w = sp.Integer(1)
            for c in ops:
                w = w*(a1 - a2) if c == 'x' else w*(b1 - b2)
            out[key] = out.get(key, 0) + sp.expand(f*g*w)
    return out

def add(F, G, c):
    out = dict(F)
    for kk, vv in G.items():
        out[kk] = out.get(kk, 0) + c*vv
    return out

def Bpair(F, G, sv):
    return add(add(bil(F, G, 'xx'), bil(F, G, 't'), 1), bil(F, G, 'x'), 2*sv)

# ---------- A. one-soliton dispersion, symbolic
al1, be1 = p1 + q1, q1**2 - p1**2
G1 = {(0, 0): 1, (al1, be1): S(1)}
F1 = {(0, 0): 1, (al1, be1): r1}          # ratio C/A = r1 candidate
G1n = {(0, 0): 1, (al1, be1): rho1}

R1 = Bpair(F1, G1, a - d).get((al1, be1), 0)
print("N=1 eq1 residual (C/A = r1):", sp.cancel(R1) == 0)
R2 = Bpair(F1, G1n, a + d).get((al1, be1), 0)
print("N=1 eq2 residual (rho1):", sp.cancel(R2) == 0)

# ---------- B. two-soliton exact random-point certification
def build(pa, hh, pv1, pv2, qv1, qv2):
    dd = hh/2
    PP1, PP2, QQ1, QQ2 = pv1 - pa, pv2 - pa, qv1 + pa, qv2 + pa
    if min(abs(PP1 - dd), abs(PP1 + dd), abs(PP2 - dd), abs(PP2 + dd),
           abs(QQ1 - dd), abs(QQ1 + dd), abs(QQ2 - dd), abs(QQ2 + dd)) == 0:
        return None
    rr1 = -(PP1 + dd)/(QQ1 - dd)
    rr2 = -(PP2 + dd)/(QQ2 - dd)
    rho1v = (PP1 + dd)*(QQ1 + dd)/((PP1 - dd)*(QQ1 - dd))
    rho2v = (PP2 + dd)*(QQ2 + dd)/((PP2 - dd)*(QQ2 - dd))
    G12 = (pv1 - pv2)*(qv1 - qv2)/((pv1 + qv1)*(pv1 + qv2)*(pv2 + qv1)*(pv2 + qv2))
    if any(z == 0 for z in [pv1 + qv1, pv1 + qv2, pv2 + qv1, pv2 + qv2]):
        return None
    al1, al2 = pv1 + qv1, pv2 + qv2
    be1, be2 = qv1**2 - pv1**2, qv2**2 - pv2**2
    K12 = (al1 + al2, be1 + be2)
    E1, E2 = (al1, be1), (al2, be2)
    Gj = {(0, 0): 1, E1: 1/(pv1 + qv1), E2: 1/(pv2 + qv2), K12: G12}
    Fj = {(0, 0): 1, E1: rr1/(pv1 + qv1), E2: rr2/(pv2 + qv2), K12: G12*rr1*rr2}
    Gj1 = {(0, 0): 1, E1: rho1v/(pv1 + qv1), E2: rho2v/(pv2 + qv2), K12: G12*rho1v*rho2v}
    return (Gj, Fj, Gj1), (pa - dd, pa + dd)

import random
random.seed(20260917)
pts = []
for _ in range(6):
    while True:
        pa = Rational(random.randint(-40, 40), random.randint(1, 7))
        hh = Rational(random.randint(1, 9), random.randint(1, 5))
        pv1 = pa + Rational(random.randint(-60, 60), random.randint(1, 7))
        pv2 = pa + Rational(random.randint(-60, 60), random.randint(1, 7))
        qv1 = -pa + Rational(random.randint(-60, 60), random.randint(1, 7))
        qv2 = -pa + Rational(random.randint(-60, 60), random.randint(1, 7))
        r = build(pa, hh, pv1, pv2, qv1, qv2)
        if r:
            pts.append(r)
            break

ok1 = ok2 = True
for i, ((Gj, Fj, Gj1), (sm, spp)) in enumerate(pts):
    R1 = Bpair(Fj, Gj, sm)
    R2 = Bpair(Fj, Gj1, spp)
    z1 = all(sp.cancel(v) == 0 for v in R1.values())
    z2 = all(sp.cancel(v) == 0 for v in R2.values())
    ok1 &= z1
    ok2 &= z2
    print("point %d: eq1 %s  eq2 %s" % (i + 1, z1, z2))
print("TWO-SOLITON exact-rational certification:", ok1 and ok2)

# ---------- C. centered same-site candidate one-soliton dispersion (record)
# eq system: B f_j.g_j = 0 ; (B f_{j+1}.g_j - B f_j.g_{j+1})/h + lam (Dx f_{j+1}.g_j + Dx f_j.g_{j+1}) = 0
# f_j = 1 + A R^j E, g_j = 1 + C R^j E  =>  eq1 forces C = -A (generic):
# coefficient of E in B f_j.g_j: al^2(A+C) + be(C-A) + 2a al(C-A)
A1, C1 = sp.symbols('A C')
fj = {(0, 0): 1, (al1, be1): A1}
gj = {(0, 0): 1, (al1, be1): C1}
cE = Bpair(fj, gj, a).get((al1, be1), 0)
solC = sp.solve(sp.Eq(sp.cancel(cE), 0), C1)[0]
print("centered candidate eq1 dispersion: C =", sp.simplify(solC/A1), "* A")
