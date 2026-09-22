# -*- coding: utf-8 -*-
"""Debug one point of the continuous two-soliton check."""
import sympy as sp
from sympy import Rational
import random

def bil3(F, G, ops):
    out = {}
    for (a1, b1, g1v), f in F.items():
        for (a2, b2, g2v), g in G.items():
            key = (a1 + a2, b1 + b2, g1v + g2v)
            w = sp.Integer(1)
            for c in ops:
                w = w*(a1 - a2) if c == 'x' else (w*(b1 - b2) if c == 't' else w*(g1v - g2v))
            out[key] = out.get(key, 0) + sp.expand(f*g*w)
    return out

def add(F, G, c):
    out = dict(F)
    for kk, vv in G.items():
        out[kk] = out.get(kk, 0) + c*vv
    return out

def build(pa, pv1, pv2, qv1, qv2):
    PP1, PP2, QQ1, QQ2 = pv1 - pa, pv2 - pa, qv1 + pa, qv2 + pa
    al1, al2 = pv1 + qv1, pv2 + qv2
    be1, be2 = qv1**2 - pv1**2, qv2**2 - pv2**2
    gam1, gam2 = 1/PP1 + 1/QQ1, 1/PP2 + 1/QQ2
    G12 = (pv1 - pv2)*(qv1 - qv2)/((pv1 + qv1)*(pv1 + qv2)*(pv2 + qv1)*(pv2 + qv2))
    E1, E2 = (al1, be1, gam1), (al2, be2, gam2)
    K12 = (al1 + al2, be1 + be2, gam1 + gam2)
    f = {(0, 0, 0): 1, E1: -(PP1/QQ1)/(pv1 + qv1), E2: -(PP2/QQ2)/(pv2 + qv2),
         K12: G12*(PP1*PP2)/(QQ1*QQ2)}
    g = {(0, 0, 0): 1, E1: 1/(pv1 + qv1), E2: 1/(pv2 + qv2), K12: G12}
    return f, g

random.seed(917)
pa = Rational(random.randint(-30, 30), random.randint(1, 6))
pv1 = pa + Rational(random.randint(-50, 50), random.randint(1, 6))
pv2 = pa + Rational(random.randint(-50, 50), random.randint(1, 6))
qv1 = -pa + Rational(random.randint(-50, 50), random.randint(1, 6))
qv2 = -pa + Rational(random.randint(-50, 50), random.randint(1, 6))
print("params:", pa, pv1, pv2, qv1, qv2)
f, g = build(pa, pv1, pv2, qv1, qv2)
R7 = add(add(bil3(f, g, 'xx'), bil3(f, g, 't'), 1), bil3(f, g, 'x'), 2*pa)
for k, v in sorted(R7.items()):
    c = sp.cancel(v)
    print("R7", k, "->", c)
