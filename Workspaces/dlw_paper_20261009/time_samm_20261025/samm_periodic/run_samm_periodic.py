"""Centered-SD with a shared moving x mesh, mapped centred differences.

Both members of the comparison use the same three-point computational
differences and the same Jacobian mapping, so the only difference is the node
distribution. The mesh velocity follows the periodic form of the cumulative
density condition rho*V - q = const with the spatial mean of q as the constant,
which removes the common drift and keeps the mapping periodic.

State (u,w), omega=h*w/4, v = Delta_h u + (w_k+w_{k-1})/2, rho = 1-w/4,
q = (u+2a)rho - D_x rho - 2a.
"""
from pathlib import Path
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')
import sys, json, hashlib, time, argparse
import numpy as np
from scipy.integrate import cumulative_trapezoid

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ROOT = PROJECT.parents[1]
AUDIT = PROJECT / 'spatial_audit_20261023'
sys.path.insert(0, str(AUDIT))
from run import Model, HALF_WIDTHS

DT, TEND = 1e-4, 0.01


def physical_v(u, w, h):
    return np.diff(u, axis=0) / h + (w[1:] + w[:-1]) / 2


def initial_state(m, x):
    u = m.profile(m.y, 0, x)[0]
    yv = (m.y[1:] + m.y[:-1]) / 2
    v = m.profile(yv, 0, x)[1]
    _, g = m.G.tau(m.y[:1] / m.h - .5, x, 0, False)
    w = np.empty_like(u)
    w[0] = 4 * m.G.cov(g, 0, 2)[0]
    r = 2 * (v - np.diff(u, axis=0) / m.h)
    for k in range(1, len(u)):
        w[k] = r[k - 1] - w[k - 1]
    return np.array([u, w])


class MappedGrid:
    def __init__(self, xi, L):
        self.xi = xi
        self.L = L
        self.dx = L / len(xi)

    def dxi(self, z):
        return (np.roll(z, -1, axis=-1) - np.roll(z, 1, axis=-1)) / (2 * self.dx)

    def dxxi(self, z):
        return (np.roll(z, -1, axis=-1) - 2 * z + np.roll(z, 1, axis=-1)) / self.dx ** 2

    def set(self, s):
        self.s = s
        self.x = self.xi + s
        self.J = 1 + self.dxi(s)
        self.Jxi = self.dxi(self.J)
        self.spacing = np.diff(np.r_[self.x, self.x[0] + self.L])
        assert self.J.min() > 0 and self.spacing.min() > 0, (self.J.min(), self.spacing.min())

    def d1(self, z):
        return self.dxi(z) / self.J

    def d2(self, z):
        return self.dxxi(z) / self.J ** 2 - self.Jxi * self.dxi(z) / self.J ** 3


def initial_mesh(m, nfine=40001):
    fine = np.linspace(-m.half, m.half, nfine)
    density = []
    for x in np.array_split(fine, 80):
        w = initial_state(m, x)[1]
        density.append((1 - w / 4).mean(axis=0))
    rho = np.concatenate(density)
    assert rho.min() > 0
    mass = np.r_[0, cumulative_trapezoid(rho, fine)]
    nodes = np.interp(np.arange(m.nx) / m.nx * mass[-1], mass, fine)
    return nodes, dict(dense_points=nfine, rho_min=float(rho.min()), rho_max=float(rho.max()),
                       total_mass=float(mass[-1]), mean_density=float(mass[-1] / (2 * m.half)))


def lower_rates(m, x, t):
    _, f = m.G.tau(m.y[:1] / m.h - .5, x, t, True)
    _, g = m.G.tau(m.y[:1] / m.h - .5, x, t, False)
    ut = 2 * (m.G.cov(f, 0, 1) - m.G.cov(g, 0, 1))[0]
    ux = 2 * (m.G.cov(f, 0, 0) - m.G.cov(g, 0, 0))[0]
    return ut, ux


def velocity(grid, u, w, a):
    rho = 1 - w / 4
    rhobar = rho.mean(axis=0)
    qbar = ((u + 2 * a) * rho - grid.d1(rho) - 2 * a).mean(axis=0)
    assert rhobar.min() > 0
    return (qbar - qbar.mean()) / rhobar, rhobar, qbar


def rhs(m, grid, t, state, mode):
    z, s = state
    u, w = z
    h = m.h
    grid.set(s)
    v = physical_v(u, w, h)
    F = u * u / 2 + 2 * m.a * u + h * h * (w * w / 32 - w / 4)
    r = -np.diff(grid.d1(F), axis=0) / h - grid.d2(v)
    boundary, ux0 = lower_rates(m, grid.x, t)
    ut = np.concatenate((boundary[None], boundary[None] + h * np.cumsum(r, axis=0)))
    wt = grid.d2(w) - grid.d1((u + 2 * m.a) * w - 4 * u)
    vel = np.zeros(m.nx)
    if mode == 'moving':
        vel = velocity(grid, u, w, m.a)[0]
        ut = ut + vel * grid.d1(u)
        wt = wt + vel * grid.d1(w)
        ut[0] = boundary + vel * ux0
    return np.array([ut, wt]), vel


def plus(state, rate, factor):
    return tuple(a + factor * b for a, b in zip(state, rate))


def rk4(m, grid, t, state, dt, mode):
    k1 = rhs(m, grid, t, state, mode)
    k2 = rhs(m, grid, t + dt / 2, plus(state, k1, dt / 2), mode)
    k3 = rhs(m, grid, t + dt / 2, plus(state, k2, dt / 2), mode)
    k4 = rhs(m, grid, t + dt, plus(state, k3, dt), mode)
    return tuple(z + dt * (a + 2 * b + 2 * c + d) / 6 for z, a, b, c, d in zip(state, k1, k2, k3, k4))


def native_fields(m, x, u, v, t):
    r = HALF_WIDTHS[m.case]
    yv = (m.y[1:] + m.y[:-1]) / 2
    eu = m.profile(m.y, t, x)[0]
    ev = m.profile(yv, t, x)[1]
    return eu, ev


def native_errors(m, x, u, v, t):
    eu, ev = native_fields(m, x, u, v, t)
    yv = (m.y[1:] + m.y[:-1]) / 2
    r = HALF_WIDTHS[m.case]
    mx = abs(x) <= r
    return [float(abs((u - eu)[abs(m.y) < r][:, mx]).max()),
            float(abs((v - ev)[abs(yv) < r][:, mx]).max())]


def mesh_diagnostics(m, grid, state):
    z, s = state
    grid.set(s)
    rho = (1 - z[1] / 4).mean(axis=0)
    cell = (rho + np.roll(rho, -1)) * grid.spacing / 2
    return dict(min_J=float(grid.J.min()), max_J=float(grid.J.max()), min_spacing=float(grid.spacing.min()),
                max_spacing=float(grid.spacing.max()), rho_min=float(rho.min()), rho_max=float(rho.max()),
                mass=float(cell.sum()), max_cell_mass_deviation=float(abs(cell / cell.mean() - 1).max()))


def run(case, mode, dt=DT):
    stem = f'{case}_{mode}_{dt:g}'
    dest = HERE / (stem + '.json')
    if dest.exists():
        print('Retained', dest.name, flush=True)
        return
    start = time.perf_counter()
    m = Model(case, 'Centered-SD', .1, .1)
    grid = MappedGrid(m.x.copy(), 2 * m.half)
    meshfile = HERE / f'{case}_initial_mesh.npz'
    if not meshfile.exists():
        xadapt, meshmeta = initial_mesh(m)
        np.savez_compressed(meshfile, x=xadapt)
        (HERE / f'{case}_initial_mesh.json').write_text(json.dumps(meshmeta, indent=2))
    else:
        xadapt = np.load(meshfile)['x']
    x0 = m.x.copy() if mode == 'uniform' else xadapt
    z0 = initial_state(m, x0)
    state = (z0.copy(), x0 - grid.xi)
    initial_error = native_errors(m, x0, z0[0], physical_v(*z0, m.h), 0)
    assert max(initial_error) < 1e-11, initial_error
    times, xs, diagnostics, error_history = [0.], [x0.copy()], [mesh_diagnostics(m, grid, state)], [initial_error]
    for i in range(round(TEND / dt)):
        state = rk4(m, grid, i * dt, state, dt, mode)
        assert np.isfinite(state[0]).all() and np.max(abs(state[0])) < 1e6
        if (i + 1) % max(1, round(.001 / dt)) == 0:
            t = (i + 1) * dt
            times.append(t)
            xs.append(grid.xi + state[1])
            diagnostics.append(mesh_diagnostics(m, grid, state))
            error_history.append(native_errors(m, xs[-1], state[0][0], physical_v(*state[0], m.h), t))
    z, s = state
    x = grid.xi + s
    v = physical_v(*z, m.h)
    errors = native_errors(m, x, z[0], v, TEND)
    grid.set(s)
    rho = (1 - z[1] / 4).mean(axis=0)
    vel, rhobar, qbar = velocity(grid, z[0], z[1], m.a)
    artifact = HERE / (stem + '.npz')
    np.savez_compressed(artifact, z=z, z0=z0, u=z[0], v=v, x=x, x0=x0, xi=grid.xi, y=m.y,
                        yv=(m.y[1:] + m.y[:-1]) / 2, rho=rho, rho0=(1 - z0[1] / 4).mean(axis=0),
                        times=times, xs=xs, error_history=error_history, J=grid.J, spacing=grid.spacing,
                        velocity=vel)
    saved = np.load(artifact)
    independent_v = np.diff(saved['u'], axis=0) / m.h + (saved['z'][1, 1:] + saved['z'][1, :-1]) / 2
    periodicity_defect = float(abs(x[-1] + grid.spacing[-1] - (x[0] + 2 * m.half)))
    record = dict(case=case, mesh=mode, method='natural Centered-SD, mapped centred x differences',
                  integrator='RK4', h=.1, computational_dx=.1, dt=dt, T=TEND, status='complete',
                  nx=m.nx, ny=len(m.y), compute_x=[-m.half, m.half], evaluation_half_width=HALF_WIDTHS[case],
                  error=errors, initial_error=initial_error, initial_mesh_diagnostics=diagnostics[0],
                  final_mesh_diagnostics=diagnostics[-1],
                  min_J_all=min(d['min_J'] for d in diagnostics), max_J_all=max(d['max_J'] for d in diagnostics),
                  min_spacing_all=min(d['min_spacing'] for d in diagnostics),
                  max_spacing_all=max(d['max_spacing'] for d in diagnostics),
                  max_initial_displacement=float(abs(x0 - grid.xi).max()),
                  max_evolution_displacement=float(abs(x - x0).max()),
                  relative_mass_drift=float(abs(diagnostics[-1]['mass'] / diagnostics[0]['mass'] - 1)),
                  max_cell_mass_deviation=float(diagnostics[-1]['max_cell_mass_deviation']),
                  periodicity_defect=periodicity_defect,
                  velocity_min=float(vel.min()), velocity_max=float(vel.max()),
                  velocity_mass_weighted_mean=float((rhobar * vel).sum() / rhobar.sum()),
                  native_reconstruction_error=float(abs(independent_v - saved['v']).max()),
                  lower_u_boundary_error=float(abs(z[0, 0] - m.profile(m.y[:1], TEND, x)[0, 0]).max()),
                  error_history=error_history,
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  artifact_sha256=hashlib.sha256(artifact.read_bytes()).hexdigest(),
                  seconds=time.perf_counter() - start)
    dest.write_text(json.dumps(record, indent=2), encoding='utf8')
    print(json.dumps({k: record[k] for k in ('case', 'mesh', 'error', 'min_J_all', 'relative_mass_drift',
                                             'max_evolution_displacement', 'periodicity_defect', 'seconds')}), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('case', choices=['A', 'D'])
    p.add_argument('--mode', choices=['uniform', 'frozen', 'moving', 'all'], default='all')
    p.add_argument('--dt', type=float, default=DT)
    a = p.parse_args()
    for mode in (['uniform', 'frozen', 'moving'] if a.mode == 'all' else [a.mode]):
        run(a.case, mode, a.dt)
