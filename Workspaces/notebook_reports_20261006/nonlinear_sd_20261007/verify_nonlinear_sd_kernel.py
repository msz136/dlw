"""Independent finite-difference checks of nonlinear SD Report (7)."""

import hashlib
import json
import runpy
import sys
from pathlib import Path

import numpy as np

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
cells = runpy.run_path(str(BASE / "dlw_numeric_cells.py"))["CELLS"]
sd_source = runpy.run_path(str(BASE / "sd_nonlinear_cell.py"))["CELLS_SD"]
ns = {}
for key in ("imports", "config", "reference", "spatial", "sd_fd"):
    exec(cells[key], ns)
exec(sd_source, ns)
exec(cells["mesh"], ns)


def independent_operators(grid):
    dx = grid.dx

    def dxi(f):
        return (np.roll(f, -1, axis=-1)-np.roll(f, 1, axis=-1))/(2*dx)

    def dxxi(f):
        return (np.roll(f, -1, axis=-1)-2*f+np.roll(f, 1, axis=-1))/dx**2

    J = 1+dxi(grid.s)
    Jxi = dxi(J)
    return (lambda f: dxi(f)/J,
            lambda f: dxxi(f)/J**2-Jxi*dxi(f)/J**3)


def relative_error(actual, expected):
    return float(np.max(abs(actual-expected))/max(1., float(np.max(abs(expected)))))


def generic_step(fun, t, z, dt, method):
    if method == "Euler":
        return z+dt*fun(t, z)
    k1 = fun(t, z)
    k2 = fun(t+dt/2, z+dt*k1/2)
    k3 = fun(t+dt/2, z+dt*k2/2)
    k4 = fun(t+dt, z+dt*k3)
    return z+dt*(k1+2*k2+2*k3+k4)/6


rows = []
for case in ("A", "B", "C"):
    for mesh in ("fixed", "moving"):
        config = dict(ns["CONFIG"], nx=64, yhalf=.5)
        problem = ns["Problem"](case, "SD", mesh, config)
        state = problem.initial()
        model, grid = problem.m, problem.X
        initial = problem.fields(state, 0.)
        exact = model.G.uv(model.js, grid.x, 0.)
        initial_error = max(float(np.max(abs(a-b))) for a, b in zip(initial, exact))
        assert initial_error < 1e-10

        # Arbitrary small perturbations exercise the boundary closure as well.
        rng = np.random.default_rng(1024)
        z = state[:-grid.n].copy()+rng.normal(0, 1e-3, len(state)-grid.n)
        t = .001
        p, w = model.unpack(z)
        u, v = model.fields(z, t)
        h, a = model.h, model.a
        d1, d2 = independent_operators(grid)
        omega = h*w/4
        H = (u*u+omega*omega)/2+2*a*u-h*omega
        pt = -np.diff(d1(H), axis=0)/h-d2(p+4/h*(omega[1:]+omega[:-1])/2)
        omega_t = -d1((u+2*a)*omega-h*u)+d2(omega)
        expected = model.pack(pt, 4/h*omega_t)
        computed = model.rhs(t, z)
        omega_error = relative_error(computed, expected)
        assert omega_error < 1e-10

        # P + M_- W = M_- v - (h^2/4) delta_- delta_yy u.
        ghosts = ns["ghost_u"](model.G, model.js, grid.x, t, u)
        ext = np.vstack((ghosts[0], u, ghosts[1]))
        lap_y = (ext[2:]-2*ext[1:-1]+ext[:-2])/h**2
        expanded = (v[1:]+v[:-1])/2-h*h/4*np.diff(lap_y, axis=0)/h
        compact = p+(w[1:]+w[:-1])/2
        flux_identity_error = relative_error(expanded, compact)
        assert flux_identity_error < 1e-10
        pt_expanded = -np.diff(d1(H), axis=0)/h-d2(expanded)
        expanded_rhs_error = relative_error(pt_expanded, model.unpack(computed)[0])
        assert expanded_rhs_error < 1e-9

        # The existing ALE stage transports both packed physical variables.
        tested_state = np.r_[z, grid.s]
        stage = problem.stage(t, tested_state)
        assert np.all(np.isfinite(stage))
        velocity = stage[-grid.n:]
        packed_transport = model.pack(d1(p)*velocity, d1(w)*velocity)
        ale_error = relative_error(stage[:-grid.n], computed+packed_transport)
        assert ale_error < 1e-10
        step_maximum = {}
        for method in ("Euler", "RK4"):
            candidate = generic_step(problem.stage, 0., state, config["dt"], method)
            assert np.all(np.isfinite(candidate))
            problem.fields(candidate, config["dt"])
            step_maximum[method] = float(np.max(abs(candidate)))
        rows.append(dict(case=case, mesh=mesh, initial_error=initial_error,
                         omega_form_relative_error=omega_error,
                         expanded_y_flux_relative_error=flux_identity_error,
                         expanded_rhs_relative_error=expanded_rhs_error,
                         ALE_relative_error=ale_error,
                         one_step_maximum=step_maximum))

result = dict(
    scheme="Report (7), nonlinear (u, omega), packed P=delta_-u and W=4omega/h",
    source_sha256=hashlib.sha256((BASE / "sd_nonlinear_cell.py").read_bytes()).hexdigest(),
    config=dict(nx=64, L=40., h=.125, dt=.000125, yhalf=.5),
    comparisons=rows,
    all_passed=True,
)
out = Path(__file__).with_name("kernel_validation.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
