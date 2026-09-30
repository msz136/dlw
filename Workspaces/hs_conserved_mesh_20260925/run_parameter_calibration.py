"""Calibrated 2HS lattice versus original and ordinary routes; old solvers unchanged.

All PDE error references and boundary data retain c_phys=1.  Only the constant
parameter of MovingSystem(kind='sd') changes to a+sqrt(c_phys**2+a**2).
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np

from run_time_methods import (METHODS, Soliton, MovingSystem, original_advance,
                              ale_step, initial_ale, unpack, reference)

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "parameter_calibration"
ROUTES = ("integrable_original", "integrable_calibrated", "difference_rho",
          "difference_rm", "difference_fixed", "difference_matched")
MOVING = ("integrable_original", "integrable_calibrated", "difference_matched")
PS = (5., 12.)
TIMES = (.25, .5)
DT = .003125


def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+"\n",
                    encoding="utf-8")


def source_hashes():
    sources = [Path(__file__), HERE/"run_time_methods.py", HERE/"run_mesh_comparison.py",
               HERE.parent/"hs_numerics_plan"/"hs_solver.py",
               HERE.parent/"hs_numerics_plan"/"hs_exact.py"]
    return {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sources}


class AuditedMovingSystem(MovingSystem):
    """Check every RHS stage and accepted state without changing the formula."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_h = float("inf")
        self.min_rho = float("inf")
        self.evaluations = 0

    def fields(self, t, z):
        f = super().fields(t, z)
        self.min_h = min(self.min_h, float(np.min(f["d"])))
        self.min_rho = min(self.min_rho, float(np.min(f["rho"])))
        return f

    def rhs(self, t, z):
        self.evaluations += 1
        return super().rhs(t, z)


def initialize(p, route, n, halfwidth=4.):
    sol = Soliton((p,), c=1., shift=-(1-2/p)/2)
    a = 2*halfwidth/n
    if route in MOVING:
        X = np.linspace(-halfwidth, halfwidth, n+1)
        u, x, _ = sol.continuous_X(X, 0.)
        left = lambda t: float(sol.continuous_X(np.array([X[0]]), t)[0][0])
        C = a + np.hypot(sol.c, a) if route == "integrable_calibrated" else sol.c
        kind = "fd" if route == "difference_matched" else "sd"
        system = AuditedMovingSystem(a, C, n, left, kind)
        state = system.pack(np.diff(u), np.diff(x), x[0])
    else:
        C, system = sol.c, None
        state = initial_ale(sol, route.split("_")[-1], n, halfwidth)
    return sol, system, state, a, C


def fields(sol, system, state, t):
    if system is not None:
        f = system.fields(t, state)
        return f["x"], f["u"], (f["x"][1:]+f["x"][:-1])/2, f["rho"]
    x = state[0]
    _, rho, u, _ = unpack(state, sol, t, x[0], x[-1])
    return x, u, x, rho


def measure(sol, data, t, size=8001):
    x, u, rx, rho = data
    grid = np.linspace(-2., 2., size)
    if min(x[-1],rx[-1]) < 2 or max(x[0],rx[0]) > -2:
        raise ValueError("Common core not covered")
    ue, re, _, _ = reference(sol, grid, t)
    return {"u": float(np.max(abs(np.interp(grid,x,u)-ue))),
            "rho": float(np.max(abs(np.interp(grid,rx,rho)-re)))}


def case_key(spec):
    return (f"p{spec['p']:g}_{spec['route']}_{spec['method']}_n{spec['n']}"
            f"_dt{spec['dt']:g}_L{spec['halfwidth']:g}")


def run_one(spec):
    p, route, n, method, dt, half = (spec[k] for k in
                                     ("p","route","n","method","dt","halfwidth"))
    sol, system, state, a, C = initialize(p, route, n, half)
    mode = route.split("_")[-1]
    initial = fields(sol,system,state,0.)
    result = {"a": a, "C": C, "c_phys": sol.c, "initial_errors": measure(sol,initial,0.),
              "initial_x_bounds": [float(initial[0][0]),float(initial[0][-1])],
              "initial_state_sha256": hashlib.sha256(
                  b"".join(np.asarray(v).tobytes() for v in
                           (state if system is None else (state,)))).hexdigest()}
    steps = int(round(.5/dt))
    assert abs(steps*dt-.5)<1e-12
    sample_steps = {int(round(t/dt)):t for t in TIMES}
    snapshots, arrays = {}, {}
    min_h, min_rho, min_Rm = float("inf"), float("inf"), float("inf")
    start = perf_counter()
    for j in range(1, steps+1):
        t = (j-1)*dt
        if system is not None:
            state, _, _ = original_advance(system,t,state,dt,method)
        else:
            state = ale_step(state,sol,t,dt,mode,-half,half,method)
            _, rr, _, Rm = unpack(state,sol,j*dt,-half,half)
            min_h = min(min_h,float(np.min(np.diff(state[0]))))
            min_rho = min(min_rho,float(np.min(rr)))
            min_Rm = min(min_Rm,float(np.min(Rm)))
        if j in sample_steps:
            time = sample_steps[j]
            data = fields(sol,system,state,time)
            snapshots[str(time)] = {"errors":measure(sol,data,time),
                                   "eval_16001":measure(sol,data,time,16001)}
            for label, value in zip(("x","u","rho_x","rho"),data):
                arrays[f"t{time}_{label}"] = value
    if system is not None:
        min_h, min_rho = system.min_h, system.min_rho
    if min_h <= 0 or min_rho <= 0:
        raise FloatingPointError("Lost grid/density positivity")
    path = OUT / "profiles" / (case_key(spec)+".npz")
    path.parent.mkdir(parents=True,exist_ok=True)
    np.savez_compressed(path, **arrays)
    result.update(status="completed", seconds=perf_counter()-start, snapshots=snapshots,
                  min_h=min_h, min_rho=min_rho,
                  min_Rm=min_Rm if system is None else None,
                  rhs_calls=system.evaluations if system is not None else
                  steps*dict(euler=1,heun=2,rk4=4,rk8=12)[method],
                  profile=str(path.relative_to(OUT)))
    return result


def specs(pilot=False):
    result = {}
    def add(p,route,method,n,dt,half=4.,purpose="matrix"):
        spec=dict(p=p,route=route,method=method,n=n,dt=dt,halfwidth=half)
        key=case_key(spec)
        if key not in result:
            result[key]={**spec,"purposes":[]}
        if purpose not in result[key]["purposes"]:
            result[key]["purposes"].append(purpose)
    if not pilot:
        for p in PS:
            for route in ROUTES:
                for method in METHODS:
                    for dt in (.0125,.00625,DT):
                        add(p,route,method,200,dt)
    for p in PS:
        for route in (MOVING if pilot else ROUTES):
            for n in (200,400,800):
                add(p,route,"rk4",n,DT,purpose="space")
            if not pilot:
                add(p,route,"rk4",800,DT/2,purpose="time_control")
                # Equal a=.02 for moving models; equal nominal dx for ALE.
                add(p,route,"rk4",500,DT,5.,purpose="domain_control")
    if not pilot:
        for p in PS:
            for route in ROUTES:
                add(p,route,"rk8",200,.00078125,purpose="time_reference")
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--pilot",action="store_true")
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/("pilot.json" if args.pilot else "results.json")
    plan=specs(args.pilot)
    hashes=source_hashes()
    saved=json.loads(path.read_text(encoding="utf-8")) if path.exists() else {
        "source_hashes":hashes,"configuration":{"physical_c":1.,"p":PS,"times":TIMES,
            "core":[-2.,2.],"evaluation_points":8001,"routes":ROUTES,"methods":METHODS,
            "scope":"deterministic representative cases, no statistical claim"},
        "plan":plan,"rows":{}}
    if saved["source_hashes"]!=hashes or saved["plan"]!=plan:
        raise RuntimeError("Saved run configuration/source changed; preserve it and use a new output")
    # JSON round-tripping normalizes tuples and scalar representations.
    for key,spec in plan.items():
        if key in saved["rows"]:
            continue
        try:
            outcome=run_one(spec)
        except Exception as exc:
            outcome={"status":"failed","error":f"{type(exc).__name__}: {exc}"}
        saved["rows"][key]={"spec":spec,**outcome}
        dump(path,saved)
        print(f"{len(saved['rows'])}/{len(plan)} {key}: {outcome['status']}",flush=True)
    print(path,flush=True)


if __name__=="__main__":
    main()
