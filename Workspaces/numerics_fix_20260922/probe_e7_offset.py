# -*- coding: utf-8 -*-
"""What is e7's model_offset now that ContRef has the correct time phase?

If (u0,v0) solves continuous DLW exactly (REVIEW probe: ~6e-61 at 60 digits),
then the O(1e-2) left-hand-side value reported by e7_fd_baseline.py must come
from the FINITE-DIFFERENCE probe itself (dy, dx, dt truncation), not from a
model mismatch.  This probe refines ny / nx / dt and prints the scaling of
each term of DLW1 / DLW2 evaluated on ContRef.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "Paper", "dlw_semidiscrete",
                                "numerics", "lib"))
import numpy as np
from gramtau import ContRef
from solver import XGrid

A = 4.0
C = ContRef([1.0], [2.0], [3.0], A)
T0 = 0.0
Y_L, Y_R = -6.0, 6.0


def dy_c(f, dy):
    g = np.empty_like(f)
    g[1:-1] = (f[2:] - f[:-2]) / (2 * dy)
    g[0] = (-3 * f[0] + 4 * f[1] - f[2]) / (2 * dy)
    g[-1] = (3 * f[-1] - 4 * f[-2] + f[-3]) / (2 * dy)
    return g


def probe(nx, ny, dt, L=40.0):
    X = XGrid(nx, L, 4)
    ys = np.linspace(Y_L, Y_R, ny)
    dy = ys[1] - ys[0]
    U = np.array([C.u0_row(y, X.x, T0) for y in ys])
    V = np.array([C.v0_row(y, X.x, T0) for y in ys])
    Up = np.array([C.u0_row(y, X.x, T0 + dt) for y in ys])
    Um = np.array([C.u0_row(y, X.x, T0 - dt) for y in ys])
    Vp = np.array([C.v0_row(y, X.x, T0 + dt) for y in ys])
    Vm = np.array([C.v0_row(y, X.x, T0 - dt) for y in ys])
    uyt = dy_c((Up - Um) / (2 * dt), dy)
    vt = (Vp - Vm) / (2 * dt)
    vx = V @ X.D1.T
    vxx = V @ X.D2.T
    ux = U @ X.D1.T
    uy = dy_c(U, dy)
    wxx = U @ X.D2.T
    L1 = uyt + vxx + ((U * uy) @ X.D1.T) + 2 * A * dy_c(ux, dy)
    L2 = vt + ((U * V) @ X.D1.T) + dy_c(wxx, dy) + 2 * A * vx - 4 * ux
    terms1 = {"uyt": uyt, "vxx": vxx, "uuy_x": (U * uy) @ X.D1.T,
              "2au_xy": 2 * A * dy_c(ux, dy)}
    terms2 = {"vt": vt, "uv_x": (U * V) @ X.D1.T, "u_xxy": dy_c(wxx, dy),
              "2av_x": 2 * A * vx, "m4ux": -4 * ux}
    return dict(nx=nx, ny=ny, dy=dy, dx=X.dx, dt=dt,
                L1=float(np.max(np.abs(L1))), L2=float(np.max(np.abs(L2))),
                t1={k: float(np.max(np.abs(v))) for k, v in terms1.items()},
                t2={k: float(np.max(np.abs(v))) for k, v in terms2.items()})


print("refine ny (nx=256 fixed, dt=1e-5):")
prev = None
for ny in (121, 241, 481, 961):
    r = probe(256, ny, 1e-5)
    ratio = f"{prev / r['L1']:6.2f}" if prev else "     -"
    prev = r["L1"]
    print(f"  ny={ny:4d} dy={r['dy']:.5f}  |L1|={r['L1']:.4e}  |L2|={r['L2']:.4e}"
          f"  ratio_L1={ratio}")

print("\nrefine nx (ny=961 fixed, dt=1e-5):")
prev = None
for nx in (128, 256, 512, 1024):
    r = probe(nx, 961, 1e-5)
    ratio = f"{prev / r['L1']:6.2f}" if prev else "     -"
    prev = r["L1"]
    print(f"  nx={nx:4d} dx={r['dx']:.5f}  |L1|={r['L1']:.4e}  |L2|={r['L2']:.4e}"
          f"  ratio_L1={ratio}")

print("\nrefine dt (nx=512, ny=961):")
prev = None
for dt in (1e-4, 1e-5, 1e-6):
    r = probe(512, 961, dt)
    ratio = f"{prev / r['L1']:6.2f}" if prev else "     -"
    prev = r["L1"]
    print(f"  dt={dt:.0e}  |L1|={r['L1']:.4e}  |L2|={r['L2']:.4e}  ratio_L1={ratio}")

print("\nterm breakdown at the production setting (nx=256, ny=241, dt=1e-5):")
r = probe(256, 241, 1e-5)
print(f"  |L1|={r['L1']:.4e}  |L2|={r['L2']:.4e}")
for k, v in r["t1"].items():
    print(f"    DLW1 {k:8s} {v:.4e}")
for k, v in r["t2"].items():
    print(f"    DLW2 {k:8s} {v:.4e}")

print("\nfinest available (nx=512, ny=961, dt=1e-6):")
r = probe(512, 961, 1e-6)
print(f"  |L1|={r['L1']:.4e}  |L2|={r['L2']:.4e}")
