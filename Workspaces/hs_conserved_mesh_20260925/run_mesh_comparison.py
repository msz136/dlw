"""Matched ALE comparison for a smooth 2HS one-soliton (c=1).

The physical-field stencil, Poisson inversion, RK4, and boundary data are
identical across meshes. Only initial equidistribution and node velocity vary.
This is an ordinary second-order field discretization, not the integrable
semi-discretization from the Sheng--Yu paper.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import solve_banded
from scipy.special import expit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "hs_numerics_plan"))
from hs_exact import Soliton


def reference(sol: Soliton, x: np.ndarray, t: float):
    # One-soliton hodograph inversion with a guaranteed bracket. For p>2,
    # omega<0 and dx/dX=1-omega*beta*w*(1-w)>0.
    x = np.asarray(x, dtype=float)
    omega, beta = float(sol.omega[0]), float(sol.beta[0])
    lower = x - sol.shift + min(0., omega)
    upper = x - sol.shift + max(0., omega)
    X = (lower + upper) / 2
    phase = sol.phase[0] if sol.phase else 0.
    for _ in range(60):
        w = expit(beta * X + omega * t + phase)
        mapped = X - omega * w + sol.shift
        if np.max(np.abs(mapped - x)) <= 1e-13:
            break
        lower = np.where(mapped < x, X, lower)
        upper = np.where(mapped > x, X, upper)
        derivative = 1 - omega * beta * w * (1 - w)
        trial = X - (mapped - x) / derivative
        X = np.where((trial > lower) & (trial < upper), trial, (lower + upper) / 2)
    w = expit(beta * X + omega * t + phase)
    mapped = X - omega * w + sol.shift
    if np.max(np.abs(mapped - x)) > 2e-12:
        raise RuntimeError("Bracketed hodograph inversion did not converge")
    u = omega * omega * w * (1 - w)
    rho = 1 / (1 - omega * beta * w * (1 - w))
    p = sol.p[0]
    s = 1 - 2 / p
    theta = sol.beta[0] * X + sol.omega[0] * t
    z = np.tanh(theta / 2)
    R = 1 + s * s * (1 - z * z) * (1 + s * s * z * z) / (1 - s * s * z * z) ** 2
    return u, rho, 2 * rho * R, R


def first_derivative(y: np.ndarray, x: np.ndarray):
    h0, h1 = x[1:-1] - x[:-2], x[2:] - x[1:-1]
    return (-h1 / (h0 * (h0 + h1)) * y[:-2]
            + (h1 - h0) / (h0 * h1) * y[1:-1]
            + h0 / (h1 * (h0 + h1)) * y[2:])


def second_derivative(y: np.ndarray, x: np.ndarray):
    h0, h1 = x[1:-1] - x[:-2], x[2:] - x[1:-1]
    return 2 * ((y[2:] - y[1:-1]) / h1
                - (y[1:-1] - y[:-2]) / h0) / (h0 + h1)


def poisson(x: np.ndarray, m: np.ndarray, left: float, right: float):
    h0, h1 = x[1:-1] - x[:-2], x[2:] - x[1:-1]
    lower = 2 / (h0 * (h0 + h1))
    diag = -2 / (h0 * h1)
    upper = 2 / (h1 * (h0 + h1))
    b = m[1:-1] - 2
    b[0] -= lower[0] * left
    b[-1] -= upper[-1] * right
    ab = np.zeros((3, len(b)))
    ab[0, 1:] = upper[:-1]
    ab[1] = diag
    ab[2, :-1] = lower[1:]
    u = np.empty_like(x)
    u[0], u[-1] = left, right
    u[1:-1] = solve_banded((1, 1), ab, b, check_finite=False)
    return u


def initial_grid(sol: Soliton, mode: str, n: int, halfwidth: float):
    if mode == "fixed":
        return np.linspace(-halfwidth, halfwidth, n + 1)
    dense = np.linspace(-halfwidth, halfwidth, max(20001, 50 * n + 1))
    _, rho, _, Rm = reference(sol, dense, 0)
    density = rho if mode == "rho" else Rm
    mass = np.r_[0., np.cumsum((density[:-1] + density[1:]) * np.diff(dense) / 2)]
    return np.interp(np.linspace(0, mass[-1], n + 1), mass, dense)


def unpack(state, sol, t, left, right):
    x, mi, ri = state
    if not all(np.all(np.isfinite(part)) for part in state):
        raise FloatingPointError("nonfinite state")
    if np.any(np.diff(x) <= 0):
        raise FloatingPointError("mesh tangling")
    ub, rb, mb, _ = reference(sol, np.array([left, right]), t)
    m = np.r_[mb[0], mi, mb[1]]
    rho = np.r_[rb[0], ri, rb[1]]
    if np.min(rho) <= 0:
        raise FloatingPointError("rho lost positivity")
    u = poisson(x, m, ub[0], ub[1])
    Rm = m / (2 * rho)
    return m, rho, u, Rm


def rhs(state, sol, t, mode, left, right):
    x, _, _ = state
    m, rho, u, Rm = unpack(state, sol, t, left, right)
    if mode == "rm" and np.min(Rm) <= 0:
        raise FloatingPointError("Rm lost positivity")
    if mode == "fixed":
        velocity = np.zeros(len(x) - 2)
    elif mode == "rho":
        velocity = -u[1:-1]
    else:
        velocity = -u[1:-1] - (rho[1:-1] - 1) / (2 * Rm[1:-1])
    ux = first_derivative(u, x)
    mx = first_derivative(m, x)
    rx = first_derivative(rho, x)
    dm = (u[1:-1] + velocity) * mx + 2 * ux * m[1:-1] + rho[1:-1] * rx
    dr = (u[1:-1] + velocity) * rx + rho[1:-1] * ux
    vx = np.r_[0., velocity, 0.]
    return vx, dm, dr


def add(state, k, factor):
    return tuple(a + factor * b for a, b in zip(state, k))


def rk4(state, sol, t, dt, mode, left, right):
    k1 = rhs(state, sol, t, mode, left, right)
    k2 = rhs(add(state, k1, dt / 2), sol, t + dt / 2, mode, left, right)
    k3 = rhs(add(state, k2, dt / 2), sol, t + dt / 2, mode, left, right)
    k4 = rhs(add(state, k3, dt), sol, t + dt, mode, left, right)
    return tuple(a + dt * (b + 2 * c + 2 * d + e) / 6
                 for a, b, c, d, e in zip(state, k1, k2, k3, k4))


def cell_mass(state, sol, t, mode, left, right):
    m, rho, _, Rm = unpack(state, sol, t, left, right)
    R = rho if mode == "rho" else Rm
    return np.diff(state[0]) * (R[1:] + R[:-1]) / 2


def evaluate(state, sol, t, mode, left, right, initial_mass, n_eval=4001,
             eval_halfwidth=None):
    x = state[0]
    m, rho, u, Rm = unpack(state, sol, t, left, right)
    eval_left, eval_right = (left, right) if eval_halfwidth is None else (-eval_halfwidth, eval_halfwidth)
    xu = np.linspace(eval_left, eval_right, n_eval)
    eu, erho, _, _ = reference(sol, xu, t)
    nu = np.interp(xu, x, u)
    nr = np.interp(xu, x, rho)
    ue_nodes, re_nodes, _, _ = reference(sol, x, t)
    interp_u = np.interp(xu, x, ue_nodes)
    interp_r = np.interp(xu, x, re_nodes)
    peak = np.abs(xu) <= 1.
    slope = (np.abs(xu) > .25) & (np.abs(xu) <= 1.5)
    mass = cell_mass(state, sol, t, mode, left, right)
    def errors(mask):
        return dict(u_linf=float(np.max(np.abs(nu[mask] - eu[mask]))),
                    rho_linf=float(np.max(np.abs(nr[mask] - erho[mask]))))
    return dict(time=t, full=errors(np.ones(len(xu), dtype=bool)),
                peak=errors(peak), slope=errors(slope),
                node=dict(u_linf=float(np.max(np.abs(u - ue_nodes))),
                          rho_linf=float(np.max(np.abs(rho - re_nodes)))),
                reconstruction=dict(u_linf=float(np.max(np.abs(interp_u - eu))),
                                    rho_linf=float(np.max(np.abs(interp_r - erho)))),
                min_rho=float(np.min(rho)), min_Rm=float(np.min(Rm)),
                min_h=float(np.min(np.diff(x))), max_h=float(np.max(np.diff(x))),
                cell_mass_max_rel_drift=float(np.max(np.abs(mass - initial_mass)) / np.mean(initial_mass)),
                total_mass_rel_drift=float(abs(np.sum(mass) - np.sum(initial_mass)) / np.sum(initial_mass)))


def run(p, mode, n, dt, final_time, halfwidth, grid_mode=None,
        sample_times=None, n_eval=4001, eval_halfwidth=None, initial_x=None):
    if p <= 2 or mode not in ("fixed", "rho", "rm"):
        raise ValueError("This experiment uses c=1, p>2 and a supported mesh mode")
    sol = Soliton((float(p),), shift=-(1 - 2 / p) / 2)
    left, right = -halfwidth, halfwidth
    grid_mode = mode if grid_mode is None else grid_mode
    x = initial_grid(sol, grid_mode, n, halfwidth) if initial_x is None else np.asarray(initial_x, dtype=float)
    if len(x) != n+1 or abs(x[0]-left) > 1e-12 or abs(x[-1]-right) > 1e-12:
        raise ValueError("initial_x must contain n+1 nodes with the configured endpoints")
    u0, rho0, _, _ = reference(sol, x, 0)
    m0 = np.r_[0., second_derivative(u0, x) + 2, 0.]
    state = (x, m0[1:-1], rho0[1:-1])
    mass0 = cell_mass(state, sol, 0, mode, left, right)
    initial = evaluate(state, sol, 0, mode, left, right, mass0, n_eval, eval_halfwidth)
    steps = int(round(final_time / dt))
    if abs(steps * dt - final_time) > 1e-12:
        raise ValueError("final_time must be an integer number of steps")
    if sample_times is None:
        sample_steps = (steps // 2, steps)
    else:
        sample_steps = tuple(int(round(value / dt)) for value in sample_times)
        if any(abs(step * dt - value) > 1e-12 or step < 1 or step > steps
               for step, value in zip(sample_steps, sample_times)):
            raise ValueError("sample times must lie on the time grid")
    snapshots = []
    path_min_h = float(np.min(np.diff(state[0])))
    path_min_rho = float(np.min(state[2]))
    path_min_Rm = float(np.min(state[1] / (2 * state[2])))
    for step in range(1, steps + 1):
        try:
            state = rk4(state, sol, (step - 1) * dt, dt, mode, left, right)
        except Exception as exc:
            raise RuntimeError(f"p={p} mode={mode} failed at t={(step-1)*dt:.8g}: {exc}") from exc
        path_min_h = min(path_min_h, float(np.min(np.diff(state[0]))))
        path_min_rho = min(path_min_rho, float(np.min(state[2])))
        path_min_Rm = min(path_min_Rm, float(np.min(state[1] / (2 * state[2]))))
        if step in sample_steps:
            snapshots.append(evaluate(state, sol, step * dt, mode, left, right, mass0,
                                      n_eval, eval_halfwidth))
    return dict(p=p, mode=mode, grid_mode=grid_mode, n=n, dt=dt, T=final_time,
                halfwidth=halfwidth, eval_halfwidth=eval_halfwidth, n_eval=n_eval,
                initial=initial, snapshots=snapshots,
                path_min_h=path_min_h, path_min_rho=path_min_rho,
                path_min_Rm=path_min_Rm,
                final_mesh=state[0], final_u=unpack(state, sol, final_time, left, right)[2],
                final_rho=unpack(state, sol, final_time, left, right)[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--long", action="store_true")
    args = parser.parse_args()
    if args.long:
        configurations = [(5, 200, .001, 1., 4.), (12, 200, .0005, .5, 4.)]
    else:
        configurations = [(5, n, dt, .25, 4.)
                          for n, dt in ([(200, .001)] if args.quick else
                                        [(200, .001), (200, .0005), (400, .0005)])]
    if not args.quick and not args.long:
        configurations += [(12, n, .0005, .1, 4.) for n in (200, 400)]
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    rows = []
    for p, n, dt, T, halfwidth in configurations:
        for mode in ("fixed", "rho", "rm"):
            result = run(p, mode, n, dt, T, halfwidth)
            suffix = f"_T{T}" if args.long else ""
            file = out / f"profile_p{p}_{mode}_n{n}_dt{dt}{suffix}.npz"
            np.savez_compressed(file, x=result.pop("final_mesh"),
                                u=result.pop("final_u"), rho=result.pop("final_rho"))
            rows.append(result)
            final = result["snapshots"][-1]
            print(f"p={p:2} n={n:3} dt={dt:.4g} {mode:5} "
                  f"u={final['full']['u_linf']:.3e} rho={final['full']['rho_linf']:.3e} "
                  f"minR={final['min_Rm']:.4f} mass={final['cell_mass_max_rel_drift']:.3e}", flush=True)
    if not args.quick and not args.long:
        # Diagnostic crossovers separate initial placement from subsequent motion.
        for p, n, dt, T in ((5, 400, .0005, .25), (12, 400, .0005, .1)):
            for velocity_mode, grid_mode in (("rm", "rho"), ("rho", "rm"),
                                             ("fixed", "rm")):
                result = run(p, velocity_mode, n, dt, T, 4., grid_mode=grid_mode)
                file = out / f"profile_p{p}_{velocity_mode}_on_{grid_mode}_n{n}_dt{dt}.npz"
                np.savez_compressed(file, x=result.pop("final_mesh"),
                                    u=result.pop("final_u"), rho=result.pop("final_rho"))
                rows.append(result)
                final = result["snapshots"][-1]
                print(f"p={p:2} n={n:3} {velocity_mode:5} on {grid_mode:5} "
                      f"u={final['full']['u_linf']:.3e} rho={final['full']['rho_linf']:.3e}",
                      flush=True)
    if args.long:
        long_crossovers = []
        for p, dt, T in ((5, .001, 1.), (12, .0005, .5)):
            result = run(p, "fixed", 200, dt, T, 4., grid_mode="rm")
            for field in ("final_mesh", "final_u", "final_rho"):
                result.pop(field)
            long_crossovers.append(result)
            final = result["snapshots"][-1]["full"]
            print(f"p={p:2} n=200 fixed on rm, T={T}: "
                  f"u={final['u_linf']:.3e} rho={final['rho_linf']:.3e}", flush=True)
        (out / "long_crossovers.json").write_text(json.dumps(long_crossovers, indent=2) + "\n",
                                                  encoding="utf-8")
    output_name = "long_results.json" if args.long else ("quick_results.json" if args.quick else "results.json")
    (out / output_name).write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
