# -*- coding: utf-8 -*-
"""Validate exact derivatives (u_t) against high-precision finite differences,
and validate the continuous reference against its own h->0 expansion."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef, ContRef, lam
from exact import SingleSoliton

a, h = 4.0, 0.25
G = GramRef([1.0, 2.0], [1.0, 3.0], [3.0, 4.0], a, h)

print("=== u_t analytic vs central difference (N=2) ===")
for (x, t, j) in [(0.0, 0.0, 0), (0.3, 0.4, 1), (-0.7, 1.1, -1)]:
    an = G.u_t(j, x, t)
    for ddt in (1e-3, 1e-4, 1e-5):
        fd = (G.u(j, x, t + ddt) - G.u(j, x, t - ddt)) / (2 * ddt)
        print(f"  x={x:5.2f} t={t:4.2f} j={j:2d} dt={ddt:.0e}  analytic={an: .10f}  fd={fd: .10f}  diff={an-fd: .3e}")

print("\n=== u_x analytic vs central difference ===")
for (x, t, j) in [(0.3, 0.4, 0)]:
    for ddx in (1e-4, 1e-5):
        fd = (G.u(j, x + ddx, t) - G.u(j, x - ddx, t)) / (2 * ddx)
        an = G.dlogF(j, x, t)
        # u_x = 2 dlogF' - dlogG' - dlogG_{j+1}'
        dux = (2 * G.d2logF(j, x, t) - G.d2logG(j, x, t) - G.d2logG(j + 1, x, t))
        print(f"  dd={ddx:.0e}  analytic u_x={dux: .10f}  fd={fd: .10f}  diff={dux-fd: .3e}")

print("\n=== continuous reference: dlog_xy vs d_x(dlog_y) and d_y(dlog_x) ===")
C = ContRef([1.0], [2.0], [3.0], a)
for (y, x, t) in [(0.0, 0.0, 0.0), (0.5, 0.3, 0.2), (-0.5, -1.0, 0.5)]:
    for n in (0, 1):
        an = C.dlog_xy(n, y, 0.0, x, t)
        dd = 1e-5
        fdx = (C.dlog_y(n, y, 0.0, x + dd, t) - C.dlog_y(n, y, 0.0, x - dd, t)) / (2 * dd)
        fdy = (C.dlog_x(n, y + dd, 0.0, x, t) - C.dlog_x(n, y - dd, 0.0, x, t)) / (2 * dd)
        print(f"  n={n} y={y:5.2f} x={x:5.2f} t={t:4.2f}  analytic={an: .10f}  d_x(dlog_y)={fdx: .10f}  d_y(dlog_x)={fdy: .10f}")

print("\n=== v0 vs finite-difference d_y( u0 )/... cross-check (N=1) ===")
for (y, x, t) in [(0.0, 0.0, 0.0), (0.5, 0.3, 0.2)]:
    v0 = C.v0(y, x, t)
    dd = 1e-5
    fd = 2.0 * ((C.dlog_xy(1, y, 0.0, x, t) + C.dlog_xy(0, y, 0.0, x, t)))
    print(f"  y={y:5.2f} x={x:5.2f}  v0={v0: .8f}")

print("\n=== report 4.3 expansion: (1/h) log chi = 1/P + 1/Q + h^2/12 (P^-3+Q^-3) ===")
p_, q_ = 1.0, 2.0
P, Q = p_ - a, q_ + a
for hh in (1/4, 1/8, 1/16, 1/32, 1/64):
    lhs = np.log(lam(P, hh) * lam(Q, hh)) / hh
    exp2 = 1/P + 1/Q + hh**2/12 * (P**-3 + Q**-3)
    print(f"  h={hh:.5f}  lhs={lhs:.12f}  order2={exp2:.12f}  diff={lhs-exp2: .3e}")
