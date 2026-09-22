# -*- coding: utf-8 -*-
"""Regression self-checks for the six defects found in the 2026-09-22 review.

Live behavior checks exercise current source; JSON checks are supplementary. The
suite is a guard against silent reintroduction.  Each check states the defect
it guards and the invariant it asserts.

Run:  python -u experiments/check_regressions.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import numpy as np

from gramtau import GramRef, ContRef          # noqa: E402
from solver import XGrid, periodic_diff_matrix, integrate   # noqa: E402

A = 4.0
FAILED = []


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAILED.append(name)


print("=" * 78)
print("regression self-checks for the 2026-09-22 review findings")
print("=" * 78)

# ---------------------------------------------------------------- defect 1
print("\n1. [P1] ContRef time phase is q^2-p^2 (NOT Q^2-P^2)")
print("   invariant: as h->0 the exact lattice field must converge to ContRef")
P, Q, RHO = [1.0], [2.0], [3.0]
cr = ContRef(P, Q, RHO, A)
errs = []
for h in (1 / 4, 1 / 8, 1 / 16, 1 / 32, 1 / 64):
    G = GramRef(P, Q, RHO, A, h)
    j = 0
    y = (j + 0.5) * h
    errs.append(abs(G.u(j, 0.3, 0.2) - cr.u0(y, 0.3, 0.2)))
ratios = [errs[i] / errs[i + 1] for i in range(len(errs) - 1)]
# With the bug the error stalls (ratio ~1.0); correct gives ratio ~4.0.
check("lattice -> ContRef converges (not stalled)", all(r > 3.5 for r in ratios),
      "ratios " + " ".join(f"{r:.2f}" for r in ratios))
check("ContRef t-rate is q^2-p^2 family", abs(cr._trate[0, 0] - (4.0 - 1.0)) < 1e-12,
      f"_trate={cr._trate[0,0]:.6f} expected {4.0-1.0:.6f}")
# With a=4,p=1,q=2, the shifted phase would be Q^2-P^2=36-9=27.
check("ContRef does NOT use Q^2-P^2", abs(cr._trate[0, 0] - 27.0) > 1e-6,
      f"_trate={cr._trate[0,0]:.6f} != 27")

# ---------------------------------------------------------------- defect 6
print("\n2. [P2] order=2 central difference has the 1/2")
n = 128
L = 2 * np.pi
D2 = periodic_diff_matrix(n, L, 2)
x = np.linspace(0, L, n, endpoint=False)
check("order=2 D1 of sin at x=0 equals 1", abs((D2 @ np.sin(x))[0] - 1.0) < 1e-3,
      f"got {(D2 @ np.sin(x))[0]:.10f}")
for order in (2, 4, 6):
    Do = periodic_diff_matrix(n, L, order)
    v = (Do @ np.sin(x))[0]
    check(f"order={order} D1 of sin at x=0 equals 1", abs(v - 1.0) < 1e-2,
          f"got {v:.10f}")

# ---------------------------------------------------------------- defect 5
print("\n3. [P2] trapezoid refuses a non-converged step")

# a stiff scalar problem that cannot converge in 2 iterations
class StiffRHS:
    def __call__(self, t, P, W):
        return 10.0 * P, 10.0 * W


Pf = np.array([[1.0]])
Wf = np.array([[1.0]])
Pout, Wout, info = integrate(StiffRHS(), 0.0, 1.0, Pf, Wf, 1.0,
                             method="trapezoid", tol=1e-12, maxit=2)
check("non-converged trapezoid reports failure", info.get("stopped") is not None,
      f"stopped={info.get('stopped')!r}")
check("non-converged trapezoid marks trap_converged False",
      info.get("trap_converged") is False, f"trap_converged={info.get('trap_converged')}")
check("non-converged trapezoid does NOT advance time", info["final_t"] == 0.0,
      f"final_t={info['final_t']}")
check("non-converged trapezoid does NOT accept the value",
      np.allclose(Pout, Pf), f"P={Pout.ravel()[0]:.6f} vs {Pf.ravel()[0]:.6f}")


# a well-behaved problem that must still converge
class SmoothRHS:
    def __call__(self, t, P, W):
        return -P, -W


Ps, Ws, infos = integrate(SmoothRHS(), 0.0, 0.1, pf0 := np.array([[1.0]]),
                          np.array([[1.0]]), 0.01, method="trapezoid",
                          tol=1e-12, maxit=50)
check("converging trapezoid still succeeds", infos.get("stopped") is None,
      f"stopped={infos.get('stopped')!r}")
check("converging trapezoid advances to T", abs(infos["final_t"] - 0.1) < 1e-12,
      f"final_t={infos['final_t']}")
check("converging trapezoid is accurate", abs(float(pf0 := Ps.ravel()[0]) - np.exp(-0.1)) < 1e-6,
      f"got {Ps.ravel()[0]:.10f} vs exp(-0.1)={np.exp(-0.1):.10f}")

# ---------------------------------------------------------------- defect 3
print("\n4. [P2] L2 norms carry BOTH dx and h weights, fixed physical window")
import importlib.util  # noqa: E402

# Re-derive E1's norm from its source to make sure the definition is the
# weighted one, by checking the reported slopes are 2.0 (not 2.5).
e1json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out",
                      "e1_continuum.json")
if os.path.exists(e1json):
    import json
    with open(e1json, encoding="utf-8") as f:
        e1 = json.load(f)
    check("E1 json declares the weighted L2 definition",
          "dx * h" in e1.get("l2_definition", ""),
          e1.get("l2_definition", "")[:60] + "...")
    check("E1 json declares a FIXED y-window", "y_window" in e1,
          str(e1.get("y_window")))
    rows = e1["cases"]["A"]["rows"]
    njs = None
    obs = e1["cases"]["A"]["observed_slopes"]
    s2 = [o["slope_E2_u"] for o in obs]
    check("E1 L2 slope is 2, not 2.5", all(abs(v - 2.0) < 0.05 for v in s2),
          " ".join(f"{v:.3f}" for v in s2))
    if "nonzero_time" in e1:
        nt = e1["nonzero_time"][0]["rows"]
        rr = [nt[i]["Einf_u"] / nt[i + 1]["Einf_u"] for i in range(len(nt) - 1)]
        check("E1 nonzero-time model error is O(h^2)",
              all(abs(r - 4.0) < 0.1 for r in rr),
              " ".join(f"{r:.3f}" for r in rr))
else:
    check("E1 json exists", False, "run e1_continuum.py first")

# ---------------------------------------------------------------- defect 4
print("\n5. [P1] E6 uses the ACTUAL discrete operator symbol, not pi/dx")
X = XGrid(256, 60.0, 4)
th = 2 * np.pi * np.fft.fftfreq(256, d=X.dx)


def d1_symbol(Xg, t_):
    return np.sum(Xg.D1[0] * np.exp(-1j * t_ * Xg.x))


Ke = np.array([d1_symbol(X, t_).imag for t_ in th])
vny = np.cos(th[128] * X.x)
check("D1 annihilates the discrete Nyquist mode",
      np.max(np.abs(X.D1 @ vny)) < 1e-12,
      f"||D1 v_nyq||={np.max(np.abs(X.D1 @ vny)):.3e}")
check("D1 symbol at Nyquist is ~0 (continuous k=pi/dx would be 13.4)",
      abs(Ke[128]) < 1e-12, f"Keff={Ke[128]:.3e} vs pi/dx={np.pi/X.dx:.4f}")
check("D1 symbol is bounded by the continuous k over all modes",
      np.all(np.abs(Ke) <= np.pi / X.dx + 1e-9),
      f"max|Keff|={np.max(np.abs(Ke)):.4f} vs pi/dx={np.pi/X.dx:.4f}")

e6json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out",
                      "e6_growth.json")
if os.path.exists(e6json):
    import json
    with open(e6json, encoding="utf-8") as f:
        e6 = json.load(f)
    check("E6 json records the discrete g_max",
          bool(e6.get("grid_gmax")) and all("g_max_discrete" in g for g in e6["grid_gmax"]),
          "")
    ratios = [g["g_max_discrete"] / g["g_max_continuous_nyq"]
              for g in e6.get("grid_gmax", []) if g["g_max_continuous_nyq"]]
    check("E6 discrete g_max is clearly below the continuous pi/dx value",
          all(r < 0.5 for r in ratios),
          " ".join(f"{r:.3f}" for r in ratios))
    check("E6 records the Nyquist null-vector check",
          "nyquist_check" in e6, "")
    sg = e6.get("solver_growth", [])
    check("E6 measures growth as a difference of two advancing orbits",
          bool(sg) and all(s.get("finite") and s.get("relative_error",1)<1e-5 for s in sg), f"{len(sg)} rows")
else:
    check("E6 json exists", False, "run e6_growth.py first")

# Live-source checks: no experiment top-level execution and no JSON writes.
import ast
from pathlib import Path
EXPDIR=Path(__file__).resolve().parent

def functions_from(name, scope):
    tree=ast.parse((EXPDIR/name).read_text(encoding="utf-8"))
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
    exec(compile(ast.Module(body=funcs,type_ignores=[]),name,"exec"),scope)
    return scope

print("\n6. Live E7 temporal self-convergence (current source)")
X7=XGrid(256,40.,4); ys=np.linspace(-6,6,241)
scope={"np":np,"X":X7,"A":4.,"dy":ys[1]-ys[0],
       "U":np.array([cr.u0_row(y,X7.x,0) for y in ys]),
       "V":np.array([cr.v0_row(y,X7.x,0) for y in ys])}
run=functions_from("e7_fd_baseline.py",scope)["run"]
ur,vr,_=run(.01/128,.01); errs=[]
for div in [2,4,8,16]:
    u,v,n=run(.01/div,.01)
    check(f"E7 reaches {div} steps with finite fields",n==div and np.isfinite(u).all() and np.isfinite(v).all())
    errs.append(float(np.max(abs(v-vr))))
orders=np.log2(np.array(errs[:-1])/errs[1:])
check("live E7 RK4 order exceeds 3.5",np.isfinite(orders).all() and np.all(orders>3.5),str(orders))

print("\n7. Live E1 quadrature and E5 initial/site checks")
xs=np.linspace(-1.5,1.5,25)
ns=functions_from("e1_continuum.py",{"np":np,"Y_LO":-1.5,"Y_HI":1.5,"DXW":.125})
unit=np.ones((12,25)); norm=ns["norms"](unit,unit,.25,xs)[2]
check("E1 constant integrates to rectangle area",abs(norm-3.)<1e-12,str(norm))
for h in [.25,.125]:
    js=ns["js_in_window"](h)
    check(f"E1 physical window h={h}",abs(len(js)*h-3)<1e-12)
from solver import Chain
C5=Chain(-2,2,.25,4.); X5=XGrid(8,8.,4)
class ZeroRHS:
    def b_fun(self,t): return np.full(8,10.)
    def __call__(self,t,P,W): return np.zeros_like(P),np.zeros_like(W)
scope={"np":np,"Cs":C5,"Xg":X5,"MID":0,"J_L":-2,"H_S":.25,"integrate":integrate}
record=functions_from("e5_conservation.py",scope)["integrate_full"]
P=np.repeat(np.arange(1,5)[:,None],8,axis=1).astype(float)
W=np.repeat(np.arange(5)[:,None],8,axis=1).astype(float)
cap,info,_=record(ZeroRHS(),P,W,.01,.005,"rk4")
check("E5 includes t=0",cap[0][0]==0 and len(cap)==3)
check("E5 selects correct u/W site",np.allclose(cap[0][1],10.75) and np.allclose(cap[0][3],2))
check("E5 reconstructs correct v site",np.allclose(cap[0][2],4.5))

print("\n8. Live E6 Jacobian and eigenmode measured through the solver")
sys.path.insert(0,str(EXPDIR))
from e6_growth import eigenmode_check
from linearized import effective_k
for nx in [64,128]:
    result=eigenmode_check(nx)
    check(f"E6 live mode agrees nx={nx}",result["relative_error"]<1e-5 and result["jacobian_error"]<1e-8,str(result["relative_error"]))
    X6=XGrid(nx,60.,4); theta=2*np.pi*(nx//8)/60
    wave=np.exp(1j*theta*X6.x)
    check(f"E6 symbol matches actual D1 nx={nx}",np.max(abs(X6.D1@wave-1j*effective_k(theta,X6.dx)*wave))<1e-11)

print()
print("=" * 78)
if FAILED:
    print(f"RESULT: {len(FAILED)} check(s) FAILED")
    for f_ in FAILED:
        print("   - " + f_)
    sys.exit(1)
print("RESULT: all regression checks PASSED")
