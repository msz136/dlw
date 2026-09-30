"""Compare time integrators across four mathematically defined 2HS routes."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate._ivp import dop853_coefficients as dc

HERE = Path(__file__).resolve().parent
HS = HERE.parent / "hs_numerics_plan"
sys.path.insert(0, str(HS))
from hs_exact import Soliton
from hs_solver import MovingSystem, advance as original_advance
from run_mesh_comparison import initial_grid, reference, second_derivative, rhs, unpack

METHODS = ("euler", "heun", "rk4", "rk8")
ROUTES = ("integrable_rho", "difference_rho", "difference_rm", "difference_fixed")
DEFAULT_PS = (5., 12.)
DEFAULT_DTS = (.0125, .00625, .003125)


def ale_add(state, derivative, factor):
    return tuple(a + factor * b for a, b in zip(state, derivative))


def ale_step(state, sol, t, h, mode, left, right, method):
    f = lambda time, value: rhs(value, sol, time, mode, left, right)
    if method == "euler":
        ks = [f(t, state)]
        weights = (1.,)
    elif method == "heun":
        k1 = f(t, state)
        ks = [k1, f(t+h, ale_add(state, k1, h))]
        weights = (.5, .5)
    elif method == "rk4":
        k1 = f(t, state)
        k2 = f(t+h/2, ale_add(state, k1, h/2))
        k3 = f(t+h/2, ale_add(state, k2, h/2))
        ks = [k1, k2, k3, f(t+h, ale_add(state, k3, h))]
        weights = (1/6, 1/3, 1/3, 1/6)
    elif method == "rk8":
        ks = []
        for i in range(dc.N_STAGES):
            trial = tuple(a + h * sum(dc.A[i,j] * ks[j][part] for j in range(i)
                                      if dc.A[i,j] != 0)
                          for part, a in enumerate(state))
            ks.append(f(t + h*dc.C[i], trial))
        weights = dc.B[:dc.N_STAGES]
    else:
        raise ValueError(method)
    return tuple(a + h * sum(weight * k[part] for weight, k in zip(weights, ks))
                 for part, a in enumerate(state))


def initial_ale(sol, mode, n, halfwidth):
    x = initial_grid(sol, mode, n, halfwidth)
    u, rho, _, _ = reference(sol, x, 0.)
    m = second_derivative(u, x) + 2
    return (x, m, rho[1:-1])


def initial_integrable(sol, n, halfwidth):
    a = 2*halfwidth/n
    X = a * np.arange(-n//2, -n//2+n+1)
    u, x, _ = sol.continuous_X(X, 0.)
    boundary = lambda t: float(sol.continuous_X(np.array([X[0]]), t)[0][0])
    system = MovingSystem(a, sol.c, n, boundary, "sd")
    return system, system.pack(np.diff(u), np.diff(x), float(x[0]))


def errors(route, sol, t, state, system, core):
    if route == "integrable_rho":
        fields = system.fields(t, state)
        x, u = fields["x"], fields["u"]
        rho_x = (x[1:]+x[:-1])/2
        rho = fields["rho"]
    else:
        x = state[0]
        _, rho, u, _ = unpack(state, sol, t, x[0], x[-1])
        rho_x = x
    if x[0] > core[0] or x[-1] < core[-1] or rho_x[0] > core[0] or rho_x[-1] < core[-1]:
        raise ValueError("core not covered")
    exact_u, exact_rho, _, _ = reference(sol, core, t)
    return {"u_linf": float(np.max(np.abs(np.interp(core, x, u)-exact_u))),
            "rho_linf": float(np.max(np.abs(np.interp(core, rho_x, rho)-exact_rho))),
            "min_h": float(np.min(np.diff(x))), "min_rho": float(np.min(rho))}


def profile(route, sol, t, state, system, core):
    if route == "integrable_rho":
        f = system.fields(t, state)
        x, u = f["x"], f["u"]
        rho_x, rho = (x[1:]+x[:-1])/2, f["rho"]
    else:
        x = state[0]
        _, rho, u, _ = unpack(state, sol, t, x[0], x[-1])
        rho_x = x
    return (np.interp(core,x,u), np.interp(core,rho_x,rho))


def run_one(p, route, method, dt, n, final_time, halfwidth, samples, core,
            include_profile=False):
    sol = Soliton((p,), shift=-(1-2/p)/2)
    if route == "integrable_rho":
        system, state = initial_integrable(sol, n, halfwidth)
    else:
        system = None
        mode = route.split("_")[-1]
        state = initial_ale(sol, mode, n, halfwidth)
    num_steps = int(round(final_time/dt))
    if abs(num_steps*dt-final_time) > 1e-12:
        raise ValueError("T must divide by dt")
    step_samples = {int(round(t/dt)): t for t in samples}
    if any(abs(j*dt-t)>1e-12 for j,t in step_samples.items()):
        raise ValueError("sample not on time grid")
    start = perf_counter()
    snapshots = {}
    min_h = float("inf")
    min_rho = float("inf")
    for j in range(1, num_steps+1):
        t = (j-1)*dt
        if system is None:
            state = ale_step(state, sol, t, dt, mode, -halfwidth, halfwidth, method)
        else:
            state, _, _ = original_advance(system, t, state, dt, method)
        if not all(np.all(np.isfinite(part)) for part in (state if system is None else (state,))):
            raise FloatingPointError("nonfinite state")
        if j in step_samples:
            e = errors(route, sol, step_samples[j], state, system, core)
            snapshots[str(step_samples[j])] = e
            min_h = min(min_h, e["min_h"])
            min_rho = min(min_rho, e["min_rho"])
    output = {"status": "completed", "seconds": perf_counter()-start,
            "snapshots": snapshots, "min_h_at_samples": min_h,
            "min_rho_at_samples": min_rho}
    if include_profile:
        output["profile"] = [v.tolist() for v in profile(route,sol,final_time,state,system,
                                                          np.linspace(core[0],core[-1],401))]
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--long", action="store_true")
    args = parser.parse_args()
    ps = (5.,) if args.quick else DEFAULT_PS
    dts = (.0125, .00625) if args.quick else DEFAULT_DTS
    n, T, halfwidth = 200, (.5 if args.long else .25), 4.
    samples = (.25,.5) if args.long else (.125,.25)
    core = np.linspace(-2., 2., 2001)
    rows = []
    for p in ps:
        for route in ROUTES:
            for method in METHODS:
                for dt in dts:
                    try:
                        result = run_one(p,route,method,dt,n,T,halfwidth,samples,core,
                                         include_profile=True)
                    except Exception as exc:
                        result = {"status": "failed", "error": f"{type(exc).__name__}: {exc}"}
                    row = {"p":p,"route":route,"method":method,"dt":dt,**result}
                    rows.append(row)
                    print(p,route,method,dt,result["status"],flush=True)
    out = HERE/"out"/"time_methods"
    out.mkdir(parents=True,exist_ok=True)
    # Fixed-step RK8 at a much smaller step supplies a same-space temporal reference.
    temporal_references = {}
    if not args.quick:
        for p in ps:
            for route in ROUTES:
                ref = run_one(p,route,"rk8",.00078125,n,T,halfwidth,samples,core,
                              include_profile=True)
                temporal_references[f"p{p:g}_{route}"] = {"dt":.00078125,
                                                         "status":ref["status"]}
                target = [np.asarray(v) for v in ref["profile"]]
                for row in rows:
                    if row["p"] == p and row["route"] == route and row["status"] == "completed":
                        candidate = [np.asarray(v) for v in row["profile"]]
                        row["temporal_profile_linf"] = {
                            "u":float(np.max(np.abs(candidate[0]-target[0]))),
                            "rho":float(np.max(np.abs(candidate[1]-target[1])))}
                print("temporal reference",p,route,flush=True)
    for row in rows:
        row.pop("profile",None)
    path = out/("long_results.json" if args.long else
                ("quick.json" if args.quick else "results.json"))
    path.write_text(json.dumps({"configuration":{"n":n,"T":T,"halfwidth":halfwidth,
                                "samples":samples,"core":[-2,2],"ps":ps,"dts":dts,
                                "methods":METHODS,"routes":ROUTES,
                                "temporal_references":temporal_references},"rows":rows},
                               indent=2)+"\n",encoding="utf-8")
    print(path,flush=True)


if __name__ == "__main__":
    main()
