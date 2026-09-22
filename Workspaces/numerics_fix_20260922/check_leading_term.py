"""Clean test of the "(u0,v0) = leading term only" claim.

Claim under test (NONLINEAR_CLOSURE section 4):
    u_j = 2(a-b)_x - (h^2/4) b_xyy + O(h^4)
    v_j = 2(a+b)_xy + h^2(...) + O(h^4)
so u^0, v^0 are the h->0 LEADING terms, and the gap to the lattice field
should be O(h^2).

This test does NOT need a PDE residual, and does NOT need a y-derivative
along the lattice.  It just compares the exact lattice field at shrinking h
to the continuous reference, both evaluated at the SAME physical point
(y = (j+1/2)h -> 0).

If the gap is O(h^2) -> the "leading term only" story holds, and any
remaining PDE residual on (u0,v0) is genuine model offset.
If the gap is O(1) or O(h) -> the story does not hold as stated.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.abspath(os.path.join(HERE, "..", "..", "Paper", "dlw_semidiscrete", "numerics"))
sys.path.insert(0, os.path.join(NUM, "lib"))

from gramtau import GramRef, ContRef  # noqa: E402

A = 4.0
P = [1.0]
Q = [2.0]
RHO = [3.0]

X = 0.3
print("=" * 78)
print("gap between exact lattice field and continuous reference, vs h")
print("both sampled at the SAME physical point y=(j+1/2)h with j=0")
print("=" * 78)

cr = ContRef(P, Q, RHO, A)

for T in (0.0, 0.2):
    print(f"\n-- t = {T} --")
    print(f"{'h':>7} {'u_lattice':>16} {'u_ContRef':>16} {'|du|':>11} {'ratio':>8}"
          f" | {'|dv|':>11} {'ratio':>8}")
    pu = pv = None
    for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64, 1 / 128, 1 / 256):
        ref = GramRef(P, Q, RHO, A, h)
        j = 0
        y = (j + 0.5) * h
        try:
            ulat = ref.u(j, X, T)
            vlat = ref.v(j, X, T)
        except Exception:
            continue
        ucont = cr.u0(y, X, T)
        vcont = cr.v0(y, X, T)
        du = abs(ulat - ucont)
        dv = abs(vlat - vcont)
        ru = f"{pu/du:.3f}" if pu else "     -"
        rv = f"{pv/dv:.3f}" if pv else "     -"
        print(f"{1/h:7.0f} {ulat:16.10f} {ucont:16.10f} {du:11.3e} {ru:>8}"
              f" | {dv:11.3e} {rv:>8}")
        pu, pv = du, dv

print()
print("=" * 78)
print("Same, but comparing to a PURELY CONTINUOUS (h-free) construction")
print("to rule out ContRef's own residual h-dependence")
print("=" * 78)
