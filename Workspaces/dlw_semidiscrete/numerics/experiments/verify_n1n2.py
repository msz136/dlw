# -*- coding: utf-8 -*-
"""Verify the exact Gram fields satisfy the closed nonlinear system (N1)(N2).

Prerequisite for solver work: if the exact solution does not satisfy N1/N2,
the solver has nothing correct to converge to.

The residuals below are evaluated with central differences in x and t, so the
measured size is the O(dx^2) truncation floor, not zero.  We therefore also
halve dx to expose that scaling and separate truncation from a genuine defect.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef

A = 4.0
CASES = {"A": ([1.0], [2.0], [3.0]),
         "C": ([1.0, 2.0], [1.0, 3.0], [3.0, 4.0])}


def fields(G, x, t, h):
    """Return closures u(m), v(m), W(m), H(m) at fixed (x,t)."""
    u = lambda m: G.u(m, x, t)
    v = lambda m: G.v(m, x, t)
    W = lambda m: G.v(m, x, t) - (G.u(m + 1, x, t) - G.u(m - 1, x, t)) / (2 * h)
    H = lambda m: 0.5 * u(m) ** 2 + 2 * A * u(m) + h ** 2 * (W(m) ** 2 / 32 - W(m) / 4)
    return u, v, W, H


def res_N1(G, j, x, t, h, dx):
    """delta_-(u_t + d_x H) + d_x^2 ( M_- v - (h^2/4) Delta_h delta_- u )."""
    u, v, W, H = fields(G, x, t, h)

    def ut(m):
        return (G.u(m, x, t + dx) - G.u(m, x, t - dx)) / (2 * dx)

    def Hx(m):
        _, _, _, Hminus = fields(G, x - dx, t, h)
        _, _, _, Hplus = fields(G, x + dx, t, h)
        return (Hplus(m) - Hminus(m)) / (2 * dx)

    d_ut = (ut(j) - ut(j - 1)) / h
    d_Hx = (Hx(j) - Hx(j - 1)) / h

    def inner(m, xx):
        uu, vv, WW, _ = fields(G, xx, t, h)
        Mmv = 0.5 * (vv(m) + vv(m - 1))
        dm = lambda k: (uu(k) - uu(k - 1)) / h
        Dl = (dm(m + 1) - 2 * dm(m) + dm(m - 1)) / h ** 2
        return Mmv - h ** 2 / 4 * Dl

    d2_inner = (inner(j, x + dx) - 2 * inner(j, x) + inner(j, x - dx)) / dx ** 2
    return d_ut + d_Hx + d2_inner


def res_N2(G, j, x, t, h, dx):
    """v_t + d_x[delta_0 H + (u+2a)W - 4u] + d_x^2[delta_0 u + (h^2/4) Delta_h W]."""
    u, v, W, H = fields(G, x, t, h)

    def vt(m):
        return (G.v(m, x, t + dx) - G.v(m, x, t - dx)) / (2 * dx)

    def flux(m, xx):
        uu, vv, WW, HH = fields(G, xx, t, h)
        d0H = (HH(m + 1) - HH(m - 1)) / (2 * h)
        return d0H + (uu(m) + 2 * A) * WW(m) - 4 * uu(m)

    def inner(m, xx):
        uu, vv, WW, _ = fields(G, xx, t, h)
        d0u = (uu(m + 1) - uu(m - 1)) / (2 * h)
        DlW = (WW(m + 1) - 2 * WW(m) + WW(m - 1)) / h ** 2
        return d0u + h ** 2 / 4 * DlW

    d_flux = (flux(j, x + dx) - flux(j, x - dx)) / (2 * dx)
    d2_inner = (inner(j, x + dx) - 2 * inner(j, x) + inner(j, x - dx)) / dx ** 2
    return vt(j) + d_flux + d2_inner


print("=" * 78)
print("Exact Gram fields vs the closed nonlinear system (N1)(N2)")
print("=" * 78)
print("Residuals use central differences in x,t; expect O(dx^2) truncation floor.\n")

for cname, (pp, qq, rr) in CASES.items():
    for h in (1 / 4, 1 / 8):
        G = GramRef(pp, qq, rr, A, h)
        print(f"--- case {cname}, h={h:.4f} ---")
        for (x, t, j) in [(0.0, 0.0, 0), (0.3, 0.2, 1)]:
            r1 = res_N1(G, j, x, t, h, 1e-4)
            r1b = res_N1(G, j, x, t, h, 5e-5)
            r2 = res_N2(G, j, x, t, h, 1e-4)
            r2b = res_N2(G, j, x, t, h, 5e-5)
            print(f"   x={x:4.1f} t={t:4.1f} j={j}:  "
                  f"N1={r1: .4e} (half-dx ratio {r1/r1b: .2f})   "
                  f"N2={r2: .4e} (half-dx ratio {r2/r2b: .2f})")
