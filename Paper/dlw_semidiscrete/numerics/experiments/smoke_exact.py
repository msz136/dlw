# -*- coding: utf-8 -*-
"""Smoke test: validate the exact Gram reference against closed-form N=1."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef, ContRef, lam
from exact import SingleSoliton

a, h = 4.0, 0.25
p1, q1, rho1 = 1.0, 2.0, 3.0

G = GramRef([p1], [q1], [rho1], a, h)
S = SingleSoliton(p1, q1, rho1, a, h)

print("chi closed form :", S.chi)
print("gram F(j=0):", G.F(0, 0.0, 0.0), " closed 1+gamma:", 1 + S.gamma)
print("gram G(j=0):", G.G(0, 0.0, 0.0), " closed 1+E     :", 1 + S.E(0, 0.0, 0.0))

print("\n  x     t     j |   u_gram        u_closed      |   v_gram        v_closed")
maxerr = 0.0
for x in (-1.0, -0.3, 0.0, 0.4, 1.5):
    for t in (0.0, 0.7, 2.0):
        for j in (-1, 0, 1, 2):
            ug, uc = G.u(j, x, t), S.u(j, x, t)
            vg, vc = G.v(j, x, t), S.v(j, x, t)
            maxerr = max(maxerr, abs(ug - uc), abs(vg - vc))
            if abs(ug - uc) > 1e-9 or abs(vg - vc) > 1e-9:
                print("MISMATCH", x, t, j, ug, uc, vg, vc)
print("max |gram - closed| over 60 samples =", maxerr)
