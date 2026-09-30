# -*- coding: utf-8 -*-
"""Measure the PURE spatial operator error of the solver RHS.

No time stepping: we compare  P_rhs(P_exact, W_exact)  against the exact
dP/dt evaluated at t=0, for increasing nx.  This isolates the x-discretisation
error from the time-integration error, which E3(a) showed to be negligible.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef
from solver import XGrid, Chain, DLWChainRHS

A = 4.0
J_L, J_R = -12, 12
L = 60.0
h = 1 / 4
t = 0.0
dt = 1e-6
G = GramRef([1.0], [2.0], [3.0], A, h)

print("Pure spatial RHS error (no time stepping), case A, h=1/4, t=0")
print(f"{'nx':>6} {'dx':>8} {'rms|dP|':>11} {'max|dP err|':>13} {'rel':>10} "
      f"{'max|dW err|':>13} {'rel':>10}")
rows = []
for NX in (64, 128, 256, 512, 1024):
    X = XGrid(NX, L, 4)
    C = Chain(J_L, J_R, h, A)
    Ublk = G.u_block(range(J_L - 1, J_R + 2), X.x, t)
    Vblk = G.v_block(range(J_L, J_R + 1), X.x, t)
    P = np.array([(Ublk[j - (J_L - 1)] - Ublk[j - 1 - (J_L - 1)]) / h
                  for j in range(J_L + 1, J_R + 1)])
    W0 = np.array([Vblk[j - J_L] - (Ublk[j + 1 - (J_L - 1)] - Ublk[j - 1 - (J_L - 1)]) / (2 * h)
                   for j in range(J_L, J_R + 1)])
    rhs = DLWChainRHS(C, X, b_fun=lambda tt: G.u_row(J_L, X.x, tt),
                      ghost_left=lambda tt: G.u_row(J_L - 1, X.x, tt),
                      ghost_right=lambda tt: G.u_row(J_R + 1, X.x, tt))
    rhs.use_ext = True
    rhs._ple = lambda tt: (G.u_row(J_L, X.x, tt) - G.u_row(J_L - 1, X.x, tt)) / h
    rhs._pre = lambda tt: (G.u_row(J_R + 1, X.x, tt) - G.u_row(J_R, X.x, tt)) / h
    dP, dW = rhs(t, P, W0)
    Pex = np.array([((G.u_row(j, X.x, dt) - G.u_row(j, X.x, -dt)) / (2 * dt)
                     - (G.u_row(j - 1, X.x, dt) - G.u_row(j - 1, X.x, -dt)) / (2 * dt)) / h
                    for j in range(J_L + 1, J_R + 1)])
    Wex = np.array([((G.v_row(j, X.x, dt) - G.v_row(j, X.x, -dt)) / (2 * dt)
                     - ((G.u_row(j + 1, X.x, dt) - G.u_row(j + 1, X.x, -dt)) / (2 * dt)
                        - (G.u_row(j - 1, X.x, dt) - G.u_row(j - 1, X.x, -dt)) / (2 * dt)) / (2 * h))
                    for j in range(J_L, J_R + 1)])
    eP, eW = np.max(np.abs(dP - Pex)), np.max(np.abs(dW - Wex))
    nP, nW = np.max(np.abs(Pex)), np.max(np.abs(Wex))
    print(f"{NX:>6} {X.dx:>8.4f} {np.sqrt(np.mean(Pex**2)):>11.3e} {eP:>13.4e} "
          f"{eP/nP:>10.3e} {eW:>13.4e} {eW/nW:>10.3e}")
    rows.append((NX, X.dx, eP, eW))

print("\nobserved order between successive nx:")
for i in range(len(rows) - 1):
    n1, d1, p1, w1 = rows[i]
    n2, d2, p2, w2 = rows[i + 1]
    print(f"  {n1}->{n2}:  dP order {np.log2(p1/p2):.3f}    dW order {np.log2(w1/w2):.3f}")
