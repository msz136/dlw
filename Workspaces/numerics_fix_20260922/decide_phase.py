"""Decide the ContRef time phase by comparing to the EXACT lattice solution.

Ground truth: GramRef (finite h) is known-good -- it is the object that E0
verifies against the bilinear identity and that E1/N1N2 verify against (N1)(N2).

Continuous limit as h->0 of u_j, v_j must reproduce ContRef.
We therefore compare GramRef at shrinking h against BOTH phase choices and
see which one the lattice solution actually converges to.

This does NOT depend on my ability to write the continuous DLW residual.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NUM = os.path.abspath(os.path.join(HERE, "..", "..", "Paper", "dlw_semidiscrete", "numerics"))
sys.path.insert(0, os.path.join(NUM, "lib"))

from gramtau import GramRef, ContRef  # noqa: E402

A = 4.0
P = [2.0]
Q = [3.0]
RHO = [5.0]

print("=" * 78)
print("Lattice (exact) vs continuous reference, at fixed t != 0")
print("The lattice solution is ground truth (E0 verifies it exactly).")
print("=" * 78)

X, T = 0.1, 0.2

for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64):
    ref = GramRef(P, Q, RHO, A, h)
    j = 0
    y = (j + 0.5) * h
    try:
        u_lat = ref.u(j, X, T)
    except Exception as e:
        print(f"h={h}: lattice u failed: {e}")
        continue
    print(f"h={1/h:7.0f}  y={(j+0.5)*h: .6f}  u_lattice = {u_lat: .10f}")

print()
print("Continuous reference candidates at y = 0 (h->0 limit):")
for phase in ("q2-p2", "Q2-P2"):
    cr = ContRef(P, Q, RHO, A)
    # monkeypatch the phase by temporarily rewriting the rate
    Pv = np.array(cr.P)[:, None]
    Qv = np.array(cr.Q)[None, :]
    print(f"  phase={phase:>7}: need to patch; see below")

print()


# Direct construction of both continuous candidates, vectorised, exact same
# formula as ContRef except for the t-rate.
def cont_u_v(phase, y, x, t):
    p = np.array(P)[:, None]
    q = np.array(Q)[None, :]
    Pp = p - A
    Qq = q + A
    rho = np.array(RHO)[:, None]

    def entry(n):
        gam = (-(Pp) / (Qq)) ** n
        c = rho / (Pp + Qq) * gam
        if phase == "q2-p2":
            tr = (q ** 2 - p ** 2) * t
        else:
            tr = (Qq ** 2 - Pp ** 2) * t
        return c * np.exp((p + q) * x + tr + y * (1 / Pp + 1 / Qq))

    def dlog_x(n):
        E = entry(n)
        M = E + np.eye(len(P))
        iM = np.linalg.inv(M)
        pq = (p + q)
        return float(np.trace(iM @ (E * pq)))

    def dlog_xy(n):
        E = entry(n)
        M = E + np.eye(len(P))
        iM = np.linalg.inv(M)
        pq = p + q
        ry = 1 / Pp + 1 / Qq
        Amat = E * pq
        Bmat = E * ry
        AB = E * pq * ry
        return float(np.trace(iM @ AB) - np.trace((iM @ Amat) @ (iM @ Bmat)))

    u = 2.0 * (dlog_x(1) - dlog_x(0))
    v = 2.0 * (dlog_xy(1) + dlog_xy(0))
    return u, v


print(f"{'h':>7} {'u_lattice':>16} {'u_cont(q2-p2)':>16} {'u_cont(Q2-P2)':>16} "
      f"{'err_q2p2':>12} {'err_Q2P2':>12}")
prev = None
for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64):
    ref = GramRef(P, Q, RHO, A, h)
    j = 0
    y = (j + 0.5) * h
    u_lat = ref.u(j, X, T)
    uc1, _ = cont_u_v("q2-p2", 0.0, X, T)
    uc2, _ = cont_u_v("Q2-P2", 0.0, X, T)
    print(f"{1/h:7.0f} {u_lat:16.10f} {uc1:16.10f} {uc2:16.10f} "
          f"{abs(u_lat-uc1):12.3e} {abs(u_lat-uc2):12.3e}")

print()
print("Ratios (should be ~4 per halving if converging at O(h^2)):")
errs1, errs2 = [], []
for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64):
    ref = GramRef(P, Q, RHO, A, h)
    j = 0
    y = (j + 0.5) * h
    u_lat = ref.u(j, X, T)
    uc1, _ = cont_u_v("q2-p2", 0.0, X, T)
    uc2, _ = cont_u_v("Q2-P2", 0.0, X, T)
    errs1.append(abs(u_lat - uc1))
    errs2.append(abs(u_lat - uc2))
for name, e in (("q2-p2", errs1), ("Q2-P2", errs2)):
    r = [f"{e[i]/e[i+1]:.3f}" for i in range(len(e) - 1)]
    print(f"  {name}: " + "  ".join(r))

print()
print("=" * 78)
print("Also test at t = 0 (where the review says the error is hidden):")
print("=" * 78)
T0 = 0.0
for h in (1 / 4, 1 / 16):
    ref = GramRef(P, Q, RHO, A, h)
    j = 0
    y = (j + 0.5) * h
    u_lat = ref.u(j, X, T0)
    uc1, _ = cont_u_v("q2-p2", 0.0, X, T0)
    uc2, _ = cont_u_v("Q2-P2", 0.0, X, T0)
    print(f"h={1/h:4.0f}  lat={u_lat: .10f}  q2-p2={uc1: .10f} (err {abs(u_lat-uc1):.3e})"
          f"  Q2-P2={uc2: .10f} (err {abs(u_lat-uc2):.3e})")
