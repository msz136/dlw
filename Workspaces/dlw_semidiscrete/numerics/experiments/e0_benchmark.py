# -*- coding: utf-8 -*-
"""E0 -- benchmark implementation: exact Gram reference and bilinear residuals.

Report sections 4.1, 4.2, 6.1 (E0).

Checks:
  (a) N=1 exact Gram evaluation against the closed form of report 4.1
  (b) N=1,2: the two finite-h bilinear equations hold on the exact solution,
      measured by the NORMALIZED residuals
          R_B^- = B_{a-h/2} F_j . G_j      / (F_j G_j)
          R_B^+ = B_{a+h/2} F_j . G_{j+1}  / (F_j G_{j+1})
      evaluated with ANALYTIC x,t derivatives  -> tests the benchmark
  (c) the same residuals with FINITE-DIFFERENCE x,t operators -> tests the
      discrete operators; report 4.2 asks these two to be reported separately.
  (d) high-precision (mpmath) spot check at 60 digits.
"""

import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef
from exact import SingleSoliton

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

A = 4.0
CASES = {
    "A": ([1.0], [2.0], [3.0]),                   # regular single soliton, S=3
    "B": ([2.0], [3.0], [5.0]),                   # narrower, S=5
    "C": ([1.0, 2.0], [1.0, 3.0], [3.0, 4.0]),    # two solitons
}
HS = [1 / 4, 1 / 8, 1 / 16, 1 / 32]

results = {"experiment": "E0", "a": A, "hs": HS, "checks": []}


def fd_dx(f, x, t, dx):
    return (f(x + dx, t) - f(x - dx, t)) / (2 * dx)


def fd_dx2(f, x, t, dx):
    return (f(x + dx, t) - 2 * f(x, t) + f(x - dx, t)) / dx ** 2


def fd_dt(f, x, t, dt):
    return (f(x, t + dt) - f(x, t - dt)) / (2 * dt)


def bilinear_norm_fd(G, j, sign, x, t, dx, dt):
    """B_s F.G / (F G) with central finite differences in x and t."""
    s = A - G.d if sign < 0 else A + G.d
    Ff = lambda xx, tt: G.F(j, xx, tt)
    Gf = (lambda xx, tt: G.G(j, xx, tt)) if sign < 0 else (lambda xx, tt: G.G(j + 1, xx, tt))
    F0, G0 = Ff(x, t), Gf(x, t)
    Fx, Gx = fd_dx(Ff, x, t, dx), fd_dx(Gf, x, t, dx)
    Fxx, Gxx = fd_dx2(Ff, x, t, dx), fd_dx2(Gf, x, t, dx)
    Ft, Gt = fd_dt(Ff, x, t, dt), fd_dt(Gf, x, t, dt)
    val = (Fxx * G0 - 2 * Fx * Gx + F0 * Gxx
           + Ft * G0 - F0 * Gt
           + 2 * s * (Fx * G0 - F0 * Gx))
    return val / (F0 * G0)


t_start = time.time()
print("=" * 78)
print("E0  benchmark implementation and bilinear residuals")
print("=" * 78)

# ---------------------------------------------------------------- (a) N=1
print("\n(a) N=1 exact Gram vs closed form of report 4.1")
p, q, rho = CASES["A"]
for h in HS:
    G = GramRef(p, q, rho, A, h)
    S = SingleSoliton(p[0], q[0], rho[0], A, h)
    err = 0.0
    for x in (-1.5, -0.4, 0.0, 0.5, 1.8):
        for t in (0.0, 0.6, 2.0):
            for j in (-2, -1, 0, 1, 2):
                err = max(err, abs(G.u(j, x, t) - S.u(j, x, t)),
                          abs(G.v(j, x, t) - S.v(j, x, t)))
    print(f"   h={h:<8.5f}  max|Gram - closed form| = {err:.3e}")
    results["checks"].append({"kind": "N1_closed_form", "h": h, "max_abs_err": err})

# ---------------------------------------------------------------- (b),(c)
print("\n(b) EXACT normalized bilinear residuals (analytic derivatives)")
print("(c) same residuals with FINITE-DIFFERENCE x,t operators")
print(f"\n{'case':>5} {'h':>8} | {'max|R_B^-| exact':>17} {'max|R_B^+| exact':>17} "
      f"| {'max|R_B^-| fd':>15} {'max|R_B^+| fd':>15}")
for cname, (pp, qq, rr) in CASES.items():
    N = len(pp)
    for h in HS:
        G = GramRef(pp, qq, rr, A, h)
        dx = dt = h / 4.0
        we_m = we_p = wf_m = wf_p = 0.0
        for j in (-2, -1, 0, 1, 2):
            for x in (-0.7, 0.0, 0.9):
                for t in (0.0, 0.5):
                    we_m = max(we_m, abs(G.B_norm(j, -1, x, t)))
                    we_p = max(we_p, abs(G.B_norm(j, +1, x, t)))
                    wf_m = max(wf_m, abs(bilinear_norm_fd(G, j, -1, x, t, dx, dt)))
                    wf_p = max(wf_p, abs(bilinear_norm_fd(G, j, +1, x, t, dx, dt)))
        print(f"{cname:>5} {h:>8.5f} | {we_m:>17.3e} {we_p:>17.3e} "
              f"| {wf_m:>15.3e} {wf_p:>15.3e}")
        results["checks"].append({
            "kind": "bilinear_residual", "case": cname, "N": N, "h": h,
            "max_abs_exact_Rminus": we_m, "max_abs_exact_Rplus": we_p,
            "max_abs_fd_Rminus": wf_m, "max_abs_fd_Rplus": wf_p,
        })

# ------------------------------------------------------- (c2) FD scaling
print("\n(c2) finite-difference bilinear residual vs FD step (h fixed = 1/8)")
h = 1 / 8
G = GramRef(*CASES["A"], A, h)
print(f"{'dx=dt':>10} {'max|R_B^-| fd':>15} {'max|R_B^+| fd':>15} {'ratio':>9}")
prev = None
fd_scan = []
for k in range(1, 7):
    dx = dt = 0.2 / 2 ** k
    m = 0.0
    for j in (-1, 0, 1):
        for x in (-0.5, 0.0):
            m = max(m,
                    abs(bilinear_norm_fd(G, j, -1, x, 0.3, dx, dt)),
                    abs(bilinear_norm_fd(G, j, +1, x, 0.3, dx, dt)))
    ratio = (prev / m) if (prev and m > 0) else float('nan')
    print(f"{dx:>10.6f} {m:>15.3e} {m:>15.3e} {ratio:>9.3f}")
    fd_scan.append({"dx": dx, "max_abs_fd": m, "ratio": ratio})
    prev = m
results["checks"].append({"kind": "fd_scaling", "h": h, "scan": fd_scan})

# ---------------------------------------------------------------- (d)
print("\n(d) high-precision spot check of the exact normalized residual (mpmath)")
import mpmath as mp
mp.mp.dps = 60
h = mp.mpf(1) / 8


def det_mp(n, j, s, x, t):
    """N=1 Gram entry, 60-digit precision."""
    p0, q0, r0 = CASES["A"]
    a_ = mp.mpf(A)
    P = mp.mpf(p0[0]) - a_
    Q = mp.mpf(q0[0]) + a_
    d_ = h / 2
    chi = ((P + d_) / (P - d_)) * ((Q + d_) / (Q - d_))
    gam = (-(mp.mpf(p0[0]) - s) / (mp.mpf(q0[0]) + s)) ** n
    ent = (mp.mpf(r0[0]) / (mp.mpf(p0[0]) + mp.mpf(q0[0]))) * gam * chi ** j \
        * mp.e ** ((mp.mpf(p0[0]) + mp.mpf(q0[0])) * x
                   + (mp.mpf(q0[0]) ** 2 - mp.mpf(p0[0]) ** 2) * t)
    return 1 + ent


mp_rows = []
for (x, t, j) in [(mp.mpf(3) / 10, mp.mpf(1) / 5, 1), (mp.mpf(-2) / 5, mp.mpf(7) / 10, -1)]:
    print(f"   x={float(x): .3f} t={float(t): .3f} j={j}")
    for sign, lbl in ((-1, "R_B^-"), (+1, "R_B^+")):
        s_ = (mp.mpf(A) - h / 2) if sign < 0 else (mp.mpf(A) + h / 2)
        Ff = lambda xx, tt: det_mp(1, j, mp.mpf(A) - h / 2, xx, tt)
        if sign < 0:
            Gf = lambda xx, tt: det_mp(0, j, mp.mpf(A), xx, tt)
        else:
            Gf = lambda xx, tt: det_mp(0, j + 1, mp.mpf(A), xx, tt)
        F0, G0 = Ff(x, t), Gf(x, t)
        Fx = mp.diff(lambda xx: Ff(xx, t), x)
        Gx = mp.diff(lambda xx: Gf(xx, t), x)
        Fxx = mp.diff(lambda xx: Ff(xx, t), x, 2)
        Gxx = mp.diff(lambda xx: Gf(xx, t), x, 2)
        Ft = mp.diff(lambda tt: Ff(x, tt), t)
        Gt = mp.diff(lambda tt: Gf(x, tt), t)
        val = (Fxx * G0 - 2 * Fx * Gx + F0 * Gxx + Ft * G0 - F0 * Gt
               + 2 * s_ * (Fx * G0 - F0 * Gx)) / (F0 * G0)
        fl = G.B_norm(j, sign, float(x), float(t))
        print(f"      {lbl}: 60-digit residual = {mp.nstr(val, 6):>14}    float64 = {fl: .4e}")
        mp_rows.append({"x": float(x), "t": float(t), "j": j, "label": lbl,
                        "mp60": mp.nstr(val, 6), "float64": fl})
results["checks"].append({"kind": "mpmath_spotcheck", "rows": mp_rows})

with open(os.path.join(OUT, "e0_benchmark.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n[E0] wrote out/e0_benchmark.json   ({time.time()-t_start:.1f}s)")
