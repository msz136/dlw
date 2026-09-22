# -*- coding: utf-8 -*-
"""E2/E3: finite-h open-chain solver errors against exact Gram fields.

The continuum pi/dx calculation is a fixed-lattice-phase model comparison.
gmax_discrete uses the full zero-background open-chain linearisation from
linearized.py. Its Float64 spectral abscissa is a numerical modal estimate,
not a nonlinear stability bound; nonnormal transient growth is possible.
The chosen nx=256, T=.05 experiment does not establish a maximal usable T.
Time errors versus exact Gram fields can be masked by spatial error.
"""

import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np
from gramtau import GramRef
from solver import XGrid, Chain, DLWChainRHS, integrate

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")
os.makedirs(OUT, exist_ok=True)

A = 4.0
J_L, J_R = -12, 12
L = 60.0
T_END = 0.05
NX_MAIN = 256
CASES = {"A": ([1.0], [2.0], [3.0]), "B": ([2.0], [3.0], [5.0])}


def gmax(nx, h=1 / 4, Lg=L):
    """Report-7 CONTINUOUS estimate: Re sigma at k = pi/dx (planning bound).

    This is a MODEL number (continuous x).  It is NOT the solver's maximum
    growth rate -- use gmax_discrete for that (REVIEW.md section 4).
    """
    k = np.pi / (Lg / nx)
    K = 2.0 / h * np.sin(0.25)
    C = np.cos(0.25)
    rhs = k ** 4 + 4.0 * k ** 3 * C / K - h ** 2 * k ** 2
    return (-2j * A * k + np.sqrt(complex(rhs))).real


from functools import lru_cache
from linearized import spectral_max

@lru_cache(None)
def gmax_discrete(nx, h=1/4, Lg=L):
    """Zero-background fixed-boundary open-chain spectral abscissa."""
    return spectral_max(nx,Lg,h,J_L,J_R)["g_max_discrete"]


def budget(nx, h=1 / 4, eps=1e-12, eta=1e-6):
    return np.log(eta / eps) / gmax(nx, h)


def budget_discrete(nx, h=1 / 4, eps=1e-12, eta=1e-6):
    return np.log(eta / eps) / gmax_discrete(nx, h)


res = {"experiment": "E2_E3", "a": A, "chain": [J_L, J_R], "L": L,
       "t_end": T_END,
       "note": "g_max/T_budget = report-7 CONTINUOUS pi/dx planning estimate; "
               "g_max_discrete/T_budget_discrete = zero-background open-chain modal spectrum estimate "
               "(see e6_growth.json).  Both are linearised-model statements: "
               "neither proves a run must overflow nor that it cannot "
               "(REVIEW.md section 4)."}


def make_case(cname, h, nx):
    pp, qq, rr = CASES[cname]
    G = GramRef(pp, qq, rr, A, h)
    X = XGrid(nx, L, 4)
    C = Chain(J_L, J_R, h, A)
    rhs = DLWChainRHS(C, X, b_fun=lambda t: G.u_row(J_L, X.x, t),
                      ghost_left=lambda t: G.u_row(J_L - 1, X.x, t),
                      ghost_right=lambda t: G.u_row(J_R + 1, X.x, t))
    rhs.use_ext = True
    rhs._ple = lambda t: (G.u_row(J_L, X.x, t) - G.u_row(J_L - 1, X.x, t)) / h
    rhs._pre = lambda t: (G.u_row(J_R + 1, X.x, t) - G.u_row(J_R, X.x, t)) / h
    Ublk = G.u_block(range(J_L - 1, J_R + 2), X.x, 0.0)
    Vblk = G.v_block(range(J_L, J_R + 1), X.x, 0.0)
    P0 = np.array([(Ublk[j - (J_L - 1)] - Ublk[j - 1 - (J_L - 1)]) / h
                   for j in range(J_L + 1, J_R + 1)])
    W0 = np.array([Vblk[j - J_L] - (Ublk[j + 1 - (J_L - 1)] - Ublk[j - 1 - (J_L - 1)]) / (2 * h)
                   for j in range(J_L, J_R + 1)])
    return G, X, C, rhs, P0, W0


def metrics(P, W, G, X, C, t, h):
    u = C.u_from_P(P, G.u_row(J_L, X.x, t))
    ue = np.empty((C.nj + 2, X.n))
    ue[0] = G.u_row(J_L - 1, X.x, t)
    ue[1:-1] = u
    ue[-1] = G.u_row(J_R + 1, X.x, t)
    v = W + (ue[2:] - ue[:-2]) / (2 * h)
    eu = u - G.u_block(range(J_L, J_R + 1), X.x, t)
    ev = v - G.v_block(range(J_L, J_R + 1), X.x, t)
    if not (np.all(np.isfinite(eu)) and np.all(np.isfinite(ev))):
        return {k: float('nan') for k in ("Einf_u", "Einf_v", "E2_u", "E2_v")}
    # L2 = sqrt( dx * h * sum_j sum_x |e|^2 ).  Both quadrature weights must
    # be present: dx along x and h along j.  No endpoint half-weights: the
    # x-grid is periodic (endpoints are not repeated) and the j-sum is over
    # interior chain sites.  Matches the E1 convention.
    return dict(Einf_u=float(np.max(np.abs(eu))), Einf_v=float(np.max(np.abs(ev))),
                E2_u=float(np.sqrt(X.dx * h * np.sum(eu ** 2))),
                E2_v=float(np.sqrt(X.dx * h * np.sum(ev ** 2))))


def main():
    t0 = time.time()
    print("=" * 78)
    print("E2/E3  time integration of the closed nonlinear system (N1)(N2)")
    print("=" * 78)
    print(f"chain j={J_L}..{J_R};  L={L};  T={T_END}")
    print("heuristic modal time scales (not nonlinear stability bounds) from BOTH budgets (left: continuous pi/dx estimate,")
    print("right: zero-background open-chain modal spectrum -- REVIEW.md section 4):\n")
    print(f"  {'nx':>5} {'dx':>9} {'g cont.':>10} {'T cont.':>9} "
          f"{'g disc.':>10} {'T disc.':>9}")
    for nx in (64, 128, 256, 512):
        print(f"  {nx:>5} {L/nx:>9.4f} {gmax(nx):>10.4e} {budget(nx):>9.4f} "
              f"{gmax_discrete(nx):>10.4e} {budget_discrete(nx):>9.4f}")
    print(f"\n  chosen nx={NX_MAIN} for both studies")
    print(f"  -- the pure spatial RHS error (experiments/space_error.py) is 4th order")
    print(f"     and reaches 2.8e-1 at nx=256; at nx<=128 the soliton is UNRESOLVED")
    print(f"     and the error stalls, which is why an nx=128 run has a dt-independent")
    print(f"     error floor.  nx=256 clears BOTH budgets "
          f"(cont {budget(256):.4f}, disc {budget_discrete(256):.4f}) compared with T={T_END};")
    print(f"     nx=512 open-chain modal time ({budget_discrete(512):.4f}) and was NOT run.")
    res["budget_table"] = [{"nx": nx, "dx": L / nx, "g_max": gmax(nx),
                            "T_budget": budget(nx),
                            "g_max_discrete": gmax_discrete(nx),
                            "T_budget_discrete": budget_discrete(nx)}
                           for nx in (64, 128, 256, 512)]

    G, X, C, rhs, P0, W0 = make_case("A", 1 / 4, NX_MAIN)
    m0 = metrics(P0, W0, G, X, C, 0.0, 1 / 4)
    print(f"\n[sanity] t=0 state -> field reconstruction: Einf(u)={m0['Einf_u']:.3e} "
          f"Einf(v)={m0['Einf_v']:.3e}  (must be ~1e-14)")

    # ------------------------------------------------- E3(a): time order
    print(f"\n--- E3(a) time refinement, h=1/4, nx={NX_MAIN}, T={T_END} (case A) ---")
    time_rows = []
    for h in (1 / 4, 1 / 8):
        G, X, C, rhs, P0, W0 = make_case("A", h, NX_MAIN)
        print(f"\n  h = {h:.4f}   (g cont={gmax(NX_MAIN,h):.3e} budget={budget(NX_MAIN,h):.4f};"
              f"  g disc={gmax_discrete(NX_MAIN,h):.3e} budget={budget_discrete(NX_MAIN,h):.4f})")
        print(f"  {'method':>10} {'dt':>9} {'Einf(u)':>11} {'Einf(v)':>11} "
              f"{'E2(u)':>11} {'E2(v)':>11} {'slope':>7} {'steps':>5}")
        for method in ("euler", "rk4", "trapezoid"):
            dts = {"euler": [4e-3, 2e-3, 1e-3],
                   "rk4": [8e-3, 4e-3, 2e-3],
                   "trapezoid": [8e-3, 4e-3, 2e-3]}[method]
            prev = None
            for dt in dts:
                P, W, info = integrate(rhs, 0.0, T_END, P0, W0, dt, method=method, tol=1e-13)
                m = metrics(P, W, G, X, C, T_END, h)
                sl = None
                if prev and np.isfinite(prev["Einf_u"]) and np.isfinite(m["Einf_u"]) \
                   and prev["Einf_u"] > 0 and m["Einf_u"] > 0:
                    sl = float(np.log2(prev["Einf_u"] / m["Einf_u"]))
                print(f"  {method:>10} {dt:>9.5f} {m['Einf_u']:>11.3e} {m['Einf_v']:>11.3e} "
                      f"{m['E2_u']:>11.3e} {m['E2_v']:>11.3e} "
                      f"{(f'{sl:.3f}' if sl else '-'):>7} {info['steps']:>5}")
                rec = {"h": h, "method": method, "dt": dt, **m, "steps": info["steps"],
                       "slope_Einf_u": sl, "g_max": gmax(NX_MAIN, h),
                       "g_max_discrete": gmax_discrete(NX_MAIN, h)}
                if "trap_mean_iters" in info:
                    rec.update(trap_mean_iters=info["trap_mean_iters"],
                               trap_max_resid=info["trap_max_resid"])
                time_rows.append(rec)
                prev = m
    res["time_refinement"] = time_rows

    # ------------------------------------------------- E3(b): space error
    print(f"\n--- E3(b) x-refinement, h=1/4, dt=2e-3 RK4, T={T_END} ---")
    print("    (each nx reported with its own report-7 budget for honesty)")
    space_rows = []
    prev = None
    for nx in (128, 256):
        G, X, C, rhs, P0, W0 = make_case("A", 1 / 4, nx)
        P, W, info = integrate(rhs, 0.0, T_END, P0, W0, 2e-3, method="rk4")
        m = metrics(P, W, G, X, C, T_END, 1 / 4)
        sl = None
        if prev and np.isfinite(prev["Einf_u"]) and np.isfinite(m["Einf_u"]) \
           and prev["Einf_u"] > 0 and m["Einf_u"] > 0:
            sl = float(np.log2(prev["Einf_u"] / m["Einf_u"]))
        print(f"  nx={nx:>4} dx={X.dx:.5f}  Einf(u)={m['Einf_u']:.4e}  Einf(v)={m['Einf_v']:.4e}"
              f"  E2(u)={m['E2_u']:.4e}  slope={(f'{sl:.3f}' if sl else '-')}"
              f"   [budget cont {budget(nx):.4f} / disc {budget_discrete(nx):.4f}]")
        space_rows.append({"h": 1 / 4, "nx": nx, "dx": X.dx, **m,
                           "slope_Einf_u": sl, "T_budget": budget(nx),
                           "T_budget_discrete": budget_discrete(nx)})
        prev = m
    res["space_refinement"] = space_rows

    with open(os.path.join(OUT, "e2_e3_solver.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(f"\n[E2/E3] wrote out/e2_e3_solver.json   ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
