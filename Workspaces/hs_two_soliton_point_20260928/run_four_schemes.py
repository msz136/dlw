"""Locked paper point under the current S1-S4 definitions, one RK4 time line."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "hs_numerics_plan"))
sys.path.insert(0, str(HERE.parent / "hs_conserved_mesh_20260925"))
sys.path.insert(0, str(HERE.parent / "hs_four_schemes_20260927"))
from hs_exact import Soliton
from run_parameter_calibration import AuditedMovingSystem
_spec = importlib.util.spec_from_file_location(
    "hs_four_scheme_study", HERE.parent / "hs_four_schemes_20260927" / "run_study.py")
base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(base)

eng, ale = base.eng, base.ale
SOL = Soliton((1.1, 1.25), c=1., phase=(np.log(6.5),)*2,
              shift=-(1/11+1/5))


def two_soliton_reference(sol, x, t):
    """Exact u, rho, m=u_xx+2 and R=m/(2rho) from four tau weights."""
    u, rho, Xaux = sol.continuous_x(np.asarray(x, dtype=float), t)
    w, om, beta = sol._weights(Xaux, t)
    mean = np.sum(w*om, axis=0)
    mean2 = np.sum(w*om**2, axis=0)
    b = np.sum(w*beta, axis=0)
    b2 = np.sum(w*beta**2, axis=0)
    ob = np.sum(w*om*beta, axis=0)
    ob2 = np.sum(w*om*beta**2, axis=0)
    o2b = np.sum(w*om**2*beta, axis=0)
    o2b2 = np.sum(w*om**2*beta**2, axis=0)
    mean_x = ob - mean*b
    mean_xx = ob2 - 2*ob*b - mean*b2 + 2*mean*b*b
    mean2_x = o2b - mean2*b
    mean2_xx = o2b2 - 2*o2b*b - mean2*b2 + 2*mean2*b*b
    ux_aux = mean2_x - 2*mean*mean_x
    uxx_aux = mean2_xx - 2*mean_x**2 - 2*mean*mean_xx
    jac = 1 - mean_x
    m = 2 + uxx_aux/jac**2 + ux_aux*mean_xx/jac**3
    return u, rho, m, m/(2*rho)


# The older ALE helper's own reference is explicitly one-soliton-only.
# Its unpack/rhs globals must use the exact two-soliton boundary data here.
ale.reference = two_soliton_reference
A, N, DT = .005, 1600, .003125
T0, T1 = -3., 3.
TIMES = (-3., -2.5, -2., -1.5, -1., 0., 1., 3.)
X = np.linspace(-4, 4, N+1)
U0, X0, _ = SOL.continuous_X(X, T0)
GRID = np.linspace(-2.5, 1.5, 16001)


def initialize(scheme):
    if scheme in ("S1", "S2"):
        c = 1. if scheme == "S1" else A + np.hypot(1., A)
        left = lambda t: float(SOL.continuous_X(X[:1], t)[0][0])
        system = AuditedMovingSystem(A, c, N, left, "sd")
        return system, system.pack(np.diff(U0), np.diff(X0), X0[0])
    x = X0.copy() if scheme == "S3" else np.linspace(X0[0], X0[-1], N+1)
    u, rho, _, _ = two_soliton_reference(SOL, x, T0)
    return None, (x, ale.second_derivative(u, x)+2, rho[1:-1])


def fields(system, state, t):
    if system is not None:
        f = system.fields(t, state)
        x = f["x"]
        return x, f["u"], (x[1:]+x[:-1])/2, f["rho"]
    x = state[0]
    _, rho, u, _ = ale.unpack(state, SOL, t, x[0], x[-1])
    return x, u, x, rho


def metrics(data, t):
    x, u, rx, rho = data
    if max(x[0], rx[0]) > GRID[0] or min(x[-1], rx[-1]) < GRID[-1]:
        raise ValueError("Common physical evaluation interval not covered")
    ue, re, _, _ = two_soliton_reference(SOL, GRID, t)
    return {"u": float(np.max(np.abs(np.interp(GRID, x, u)-ue))),
            "rho": float(np.max(np.abs(np.interp(GRID, rx, rho)-re)))}


def step(scheme, system, state, t):
    if system is not None:
        state, _, _ = eng.original_advance(system, t, state, DT, "rk4")
    elif scheme == "S4":
        state = eng.ale_step(state, SOL, t, DT, "fixed", X0[0], X0[-1], "rk4")
    else:
        aa, cc, bb = base.butcher("rk4")
        ks = []
        for i in range(len(bb)):
            trial = tuple(v + DT*sum(aa[i,k]*ks[k][part] for k in range(i) if aa[i,k] != 0)
                          for part, v in enumerate(state))
            ks.append(base.paper_ale_rhs(trial, SOL, t+cc[i]*DT))
        state = tuple(v + DT*sum(bb[k]*ks[k][part] for k in range(len(bb)) if bb[k] != 0)
                      for part, v in enumerate(state))
    return state


def run(scheme):
    system, state = initialize(scheme)
    t = T0
    snapshots, errors = {}, {}
    min_edge, min_rho = np.inf, np.inf
    try:
        for target in TIMES:
            nsteps = round((target-t)/DT)
            assert abs(t+nsteps*DT-target) < 1e-10
            for _ in range(nsteps):
                state = step(scheme, system, state, t)
                t += DT
                data = fields(system, state, t)
                min_edge = min(min_edge, float(np.min(np.diff(data[0]))))
                min_rho = min(min_rho, float(np.min(data[3])))
                if not np.isfinite(min_edge) or not np.isfinite(min_rho) or min_edge <= 0 or min_rho <= 0:
                    raise ValueError("Nonfinite/nonpositive edge or rho")
            t = target
            data = fields(system, state, t)
            errors[str(t)] = metrics(data, t)
            for name, arr in zip(("x", "u", "rho_x", "rho"), data):
                snapshots[f"t{t}_{name}"] = arr.copy()
    except (ValueError, RuntimeError, FloatingPointError, OverflowError, AssertionError) as exc:
        status, reason = "failed", f"{type(exc).__name__}: {exc}"
    else:
        status, reason = "completed", ""
    path = HERE / f"four_{scheme}_profiles.npz"
    np.savez_compressed(path, **snapshots)
    return {"status": status, "reason": reason, "last_time": t,
            "min_edge": min_edge, "min_rho": min_rho, "metrics": errors,
            "profile": path.name, "profile_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    results = {}
    for scheme in base.SCHEMES:
        results[scheme] = run(scheme)
        print(scheme, results[scheme]["status"], results[scheme]["last_time"], flush=True)
    config = {"p": [1.1,1.25], "q": [11,5], "c_phys":1., "a":A,
              "n":N, "phase_normalized":[float(np.log(6.5))]*2,
              "shift":SOL.shift, "initial":"common continuous two-soliton",
              "X_bounds":[-4,4], "evaluation_bounds":[-2.5,1.5],
              "dt":DT, "times":TIMES, "method":"rk4",
              "driver_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "four_scheme_sha256":base.sha(base.__file__),
              "engine_hashes":eng.source_hashes()}
    (HERE / "four_schemes_results.json").write_text(
        json.dumps({"configuration":config,"results":results},indent=2)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
