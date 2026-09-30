"""One locked paper two-soliton point: structure-preserving vs ordinary moving FD.

Both methods use the same continuous initial u/x, left boundary, RK4 step and mesh.
The time window covers the interaction, not asymptotic scattering.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "hs_numerics_plan"))
from hs_exact import Soliton
from hs_solver import MovingSystem, advance

P = (1.1, 1.25)
C = 1.0
A = 0.005
N = 1600
DT = 0.003125
T0, T1 = -3.0, 3.0
TIMES = (-3.0, -2.5, -2.0, -1.5, 0.0, 1.5, 3.0)
PHASE = (np.log(6.5), np.log(6.5))
SHIFT = -(1 / 11 + 1 / 5)
X = np.linspace(-4.0, 4.0, N + 1)
GRID = np.linspace(-2.5, 1.5, 16001)
SOL = Soliton(P, c=C, phase=PHASE, shift=SHIFT)


def fields(system, z, t):
    f = system.fields(t, z)
    return f["x"], f["u"], (f["x"][1:] + f["x"][:-1]) / 2, f["rho"]


def measure(data, t):
    x, u, rx, rho = data
    if x[0] > GRID[0] or x[-1] < GRID[-1]:
        raise ValueError("Common evaluation interval left the numerical domain")
    ue, re, _ = SOL.continuous_x(GRID, t)
    return {"u": float(np.max(np.abs(np.interp(GRID, x, u) - ue))),
            "rho": float(np.max(np.abs(np.interp(GRID, rx, rho) - re)))}


def run(kind, dt):
    k = np.arange(-N // 2, N // 2 + 1)
    initial = SOL.lattice_state(k, A, T0)
    u0, x0 = initial["u"], initial["x"]
    left = lambda t: float(SOL.lattice_state(k[:2], A, t)["u"][0])
    system = MovingSystem(A, C, N, left, kind=kind)
    state = system.pack(np.diff(u0), np.diff(x0), x0[0])
    snapshots = {}
    metrics = {}
    min_edge = float("inf")
    t = T0
    try:
        for target in TIMES:
            steps = int(round((target - t) / dt))
            assert abs(t + steps * dt - target) < 1e-10
            for _ in range(steps):
                state, _, _ = advance(system, t, state, dt, "rk4")
                t += dt
                min_edge = min(min_edge, float(np.min(state[N:2*N])))
            t = target
            data = fields(system, state, t)
            metrics[str(t)] = measure(data, t)
            exact = SOL.lattice_state(k, A, t)
            metrics[str(t)]["lattice_tracking"] = {
                "u": float(np.max(np.abs(data[1] - exact["u"]))),
                "rho": float(np.max(np.abs(data[3] - exact["rho"]))),
                "x": float(np.max(np.abs(data[0] - exact["x"])))
            }
            for name, arr in zip(("x", "u", "rho_x", "rho"), data):
                snapshots[f"t{t}_{name}"] = arr.copy()
    except (ValueError, RuntimeError, FloatingPointError, OverflowError) as exc:
        status, error = "failed", f"{type(exc).__name__}: {exc}"
    else:
        status, error = "completed", ""
    path = HERE / f"{kind}_dt{dt:g}_profiles.npz"
    np.savez_compressed(path, **snapshots)
    return {"status": status, "error": error, "last_time": t,
            "min_edge": min_edge, "metrics": metrics,
            "profile": path.name,
            "profile_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def plot(results):
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6), layout="constrained")
    for col, t in enumerate((0.0, 3.0)):
        ue, re, _ = SOL.continuous_x(GRID, t)
        for row, (field, exact) in enumerate((("u", ue), ("rho", re))):
            ax = axes[row, col]
            ax.plot(GRID, exact, color="black", lw=1.8, label="continuous exact")
            for kind, label in (("sd", "integrable SD"), ("fd", "ordinary moving FD")):
                if str(t) not in results["main"][kind]["metrics"]:
                    continue
                with np.load(HERE / results["main"][kind]["profile"]) as z:
                    x = z[f"t{t}_{'x' if field == 'u' else 'rho_x'}"]
                    y = z[f"t{t}_{field}"]
                    ax.plot(GRID, np.interp(GRID, x, y), lw=1, label=label)
            ax.set(xlabel="physical x", ylabel=field, title=f"t={t:g}")
            ax.grid(alpha=.2)
            ax.legend(fontsize=8)
    path = HERE / "interaction_line.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)


def main():
    assert np.allclose(SOL.q, (11, 5))
    assert np.isclose(SOL.interaction, 0.9 / 38.025)
    results = {label: {kind: run(kind, dt) for kind in ("sd", "fd")}
               for label, dt in (("main", DT), ("half_dt", DT/2))}
    config = {"p": P, "q": SOL.q.tolist(), "c": C, "a": A, "n": N,
              "initial_condition": "same finite-a exact lattice state for both methods",
              "normalized_phase": PHASE, "shift": SHIFT, "X_bounds": (-4, 4),
              "evaluation_bounds": (float(GRID[0]), float(GRID[-1])),
              "dt": DT, "times": TIMES, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "reference_sha256": hashlib.sha256(Path(sys.modules["hs_exact"].__file__).read_bytes()).hexdigest(),
              "solver_sha256": hashlib.sha256(Path(sys.modules["hs_solver"].__file__).read_bytes()).hexdigest()}
    (HERE / "results.json").write_text(json.dumps({"configuration": config, "results": results}, indent=2) + "\n", encoding="utf-8")
    plot(results)
    print(json.dumps({label: {kind: {"status": v["status"], "last_time": v["last_time"], "metrics": v["metrics"]}
                              for kind, v in group.items()} for label, group in results.items()}, indent=2))


if __name__ == "__main__":
    main()
