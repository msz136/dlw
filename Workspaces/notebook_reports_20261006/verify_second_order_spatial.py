"""Independent three-point spatial audit; no complete PDE run is performed.

Fourier symbols include Nyquist to distinguish direct Dxi2 from Dxi composition.
Analytic fields on a smooth moving map establish spatial convergence. Explicit
NumPy ghost values check SD matrices, tau ratios, and SD2 additive jumps. Each
lift is checked against its constrained system and the common physical initial
fields; a time/mesh finite difference checks its material boundary derivative.

The direct Dxi2 agrees with the GSG comparison. Dxi and the chain-rule stencil
are choices for the DLW transfer, rather than formulas explicitly stated there.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
from verify_dlw_tau import definitions, dxi, dxi2

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / 'gsg_second_order'


def explicit_derivatives(f, spacing, jacobian, jump=0.):
    """NumPy ghost values, independent of Grid and all sparse matrices."""
    left, right = np.roll(f, 1, axis=-1).copy(), np.roll(f, -1, axis=-1).copy()
    left[..., :1] -= jump
    right[..., -1:] += jump
    fxi = (right-left)/(2*spacing)
    fxxi = (right-2*f+left)/spacing**2
    return fxi/jacobian, fxxi/jacobian**2-dxi(jacobian, spacing)*fxi/jacobian**3


def maximum(f):
    return float(np.max(np.abs(f)))


def relative_difference(a, b):
    return maximum(a-b)/max(1., maximum(b))


def observed_orders(errors):
    return [float(np.log2(a/b)) for a, b in zip(errors[:-1], errors[1:])]


def check_uniform(ns):
    rows, symbol_rows = [], []
    for n in (64, 128, 256):
        grid = ns['Grid'](n, 2*np.pi)
        for mode in (1, 3, n//2):
            theta = 2*np.pi*mode/n
            f = ((-1.)**np.arange(n) if mode == n//2 else
                 np.exp(1j*theta*np.arange(n)))
            first = 1j*np.sin(theta)/grid.dx
            second = -4*np.sin(theta/2)**2/grid.dx**2
            errors = [relative_difference(grid.d1(f), first*f),
                      relative_difference(grid.d2(f), second*f)]
            assert max(errors) < 3e-12, (n, mode, errors)
            symbol_rows.append(dict(nx=n, mode=mode, D1_symbol_scaled_error=errors[0],
                                    D2_symbol_scaled_error=errors[1]))
        k = 3
        f = np.sin(k*grid.xi)
        rows.append(dict(nx=n, D1_error=maximum(grid.d1(f)-k*np.cos(k*grid.xi)),
                         D2_error=maximum(grid.d2(f)+k*k*f)))
    orders = {key: observed_orders([r[key] for r in rows])
              for key in ('D1_error', 'D2_error')}
    assert all(1.9 < p < 2.1 for ps in orders.values() for p in ps), orders
    return dict(rows=rows, observed_orders=orders, symbols=symbol_rows,
                D1_symbol='i sin(theta)/d', D2_symbol='-4 sin(theta/2)^2/d^2',
                Nyquist_D2_checked=True)


def manufactured_shift(xi):
    return .16*np.sin(xi)+.05*np.sin(2*xi)


def check_moving_convergence(ns):
    rows = []
    for n in (64, 128, 256):
        grid = ns['Grid'](n, 2*np.pi)
        grid.set_s(manufactured_shift(grid.xi))
        exact_j = 1+.16*np.cos(grid.xi)+.1*np.cos(2*grid.xi)
        f = np.sin(2*grid.x)+.2*np.cos(3*grid.x)
        exact_first = 2*np.cos(2*grid.x)-.6*np.sin(3*grid.x)
        exact_second = -4*np.sin(2*grid.x)-1.8*np.cos(3*grid.x)
        independent = explicit_derivatives(f, grid.dx, grid.J)
        assert relative_difference(grid.d1(f), independent[0]) < 3e-12
        assert relative_difference(grid.d2(f), independent[1]) < 3e-12
        rows.append(dict(nx=n, min_J=float(grid.J.min()),
                         J_error=maximum(grid.J-exact_j),
                         D1_error=maximum(grid.d1(f)-exact_first),
                         D2_error=maximum(grid.d2(f)-exact_second)))
    orders = {key: observed_orders([r[key] for r in rows])
              for key in ('J_error', 'D1_error', 'D2_error')}
    assert all(1.85 < p < 2.15 for ps in orders.values() for p in ps), orders
    return dict(rows=rows, observed_orders=orders,
                mapping='x=xi+0.16 sin(xi)+0.05 sin(2xi)',
                field='sin(2x)+0.2 cos(3x)')


def check_sd_matrices(ns):
    cfg = dict(ns['CONFIG'], nx=128, L=2*np.pi)
    model = ns['SDModel']('A', cfg)
    grid = model.X
    grid.set_s(manufactured_shift(grid.xi))
    D1, D2 = model.operators()
    rng = np.random.default_rng(20261007)
    f = sum(rng.normal(size=(3, 1))*np.sin(k*grid.xi)[None, :]
            for k in range(1, 9))
    expected = explicit_derivatives(f, grid.dx, grid.J)
    checks = dict(D1_matrix_visible_scaled_error=relative_difference((D1@f.T).T, grid.d1(f)),
                  D2_matrix_visible_scaled_error=relative_difference((D2@f.T).T, grid.d2(f)),
                  D1_matrix_independent_scaled_error=relative_difference((D1@f.T).T, expected[0]),
                  D2_matrix_independent_scaled_error=relative_difference((D2@f.T).T, expected[1]))
    unknown_logs = .2*np.sin(grid.xi)+.1*np.cos(2*grid.xi)
    known_logs = .3*np.cos(grid.xi)-.15*np.sin(3*grid.xi)
    unknown, known = np.exp(unknown_logs), np.exp(known_logs)
    ratios = model.derivative_ratios(unknown_logs)
    expected_ratios = explicit_derivatives(unknown, grid.dx, grid.J)
    checks['D1_tau_ratio_scaled_error'] = relative_difference(ratios[0], expected_ratios[0]/unknown)
    checks['D2_tau_ratio_scaled_error'] = relative_difference(ratios[1], expected_ratios[1]/unknown)
    ratio = 1+.07*np.sin(3*grid.xi)
    u = unknown*ratio
    ux, uxx = explicit_derivatives(u, grid.dx, grid.J)
    kx, kxx = explicit_derivatives(known, grid.dx, grid.J)
    drift = .1+.03*np.cos(grid.xi)
    for solve_f, sign in ((True, 1), (False, -1)):
        matrix = model.matrix_for(unknown_logs, known_logs, drift, solve_f)
        raw = (uxx*known-2*ux*kx+u*kxx
               +sign*2*drift*(ux*known-u*kx))/(unknown*known)
        checks[('F' if solve_f else 'G')+'_linearized_bilinear_scaled_error'] = relative_difference(matrix@ratio, raw)
    assert max(checks.values()) < 5e-12, checks
    return dict(nx=grid.n, min_J=float(grid.J.min()), checks=checks)


def check_sd2_lifts(ns):
    rows = []
    for case in ns['CASES']:
        for mesh in ('fixed', 'moving'):
            problem = ns['Problem'](case, 'SD2', mesh, ns['CONFIG'])
            state = problem.initial()
            model, grid = problem.m, problem.X
            q, r = model.unpack(state[:-grid.n], 0.)
            u, v = model.G.uv(model.js, grid.x, 0.)
            fields = problem.fields(state, 0.)
            b = np.zeros(grid.n)
            b[0] = b[-1] = 1/(2*grid.dx)
            qxi = dxi(q, grid.dx)+b*model.jump
            lift_residual = qxi-.5*grid.J*u*q
            qx, qxx = explicit_derivatives(q, grid.dx, grid.J, model.jump)
            rx, rxx = explicit_derivatives(r, grid.dx, grid.J, model.rjump)
            differences = dict(lift_scaled_residual=maximum(lift_residual)/max(1., maximum(.5*grid.J*u*q)),
                D_matrix_scaled_error=relative_difference((model.D@q.T).T, dxi(q, grid.dx)),
                jump_vector_error=maximum(model.b-b),
                Q_jump_D1_scaled_error=relative_difference(model.dx(q, model.jump), qx),
                R_jump_D1_scaled_error=relative_difference(model.dx(r, model.rjump), rx),
                Q_jump_D2_scaled_error=relative_difference(grid.d2(q, model.jump), qxx),
                R_jump_D2_scaled_error=relative_difference(grid.d2(r, model.rjump), rxx),
                normalization_error=maximum(q[:, 0]-1),
                reciprocal_endpoint_jump_error=maximum((1+model.jump)*(1+model.rjump)-1),
                analytic_initial_uv_error=max(maximum(a-bb) for a, bb in zip(fields, (u, v))))
            for other_name in ('SD', 'FD'):
                other = ns['Problem'](case, other_name, mesh, ns['CONFIG'])
                other_state = other.initial()
                assert maximum(other.X.x-grid.x) < 1e-13
                other_fields = other.fields(other_state, 0.)
                differences['common_initial_'+other_name+'_uv_error'] = max(
                    maximum(a-bb) for a, bb in zip(fields, other_fields))
            # A time/mesh finite difference independently checks the lift's material derivative.
            s0 = grid.s.copy()
            velocity = .02*np.sin(2*np.pi*grid.xi/grid.L)
            boundary_q = model.boundary(0.)[0].copy()
            physical_qt = model.boundary_derivative(0., velocity)
            material_qt = physical_qt+velocity*explicit_derivatives(
                boundary_q, grid.dx, grid.J, model.jump[0])[0]
            eps = 2e-7
            grid.set_s(s0+eps*velocity)
            plus = model.boundary(eps)[0].copy()
            grid.set_s(s0-eps*velocity)
            minus = model.boundary(-eps)[0].copy()
            grid.set_s(s0)
            model.boundary(0.)
            boundary_fd_error = relative_difference((plus-minus)/(2*eps), material_qt)
            assert boundary_fd_error < 2e-6, (case, mesh, boundary_fd_error)
            assert max(differences.values()) < 1e-10, (case, mesh, differences)
            assert q.min() > 0 and (1+model.jump).min() > 0
            rows.append(dict(case=case, mesh=mesh, min_Q=float(q.min()),
                             min_endpoint_Q_ratio=float((1+model.jump).min()),
                             boundary_material_derivative_scaled_error=boundary_fd_error,
                             checks=differences))
    return rows


def main():
    started = time.perf_counter()
    ns, cells = definitions()
    record = dict(success=True,
                  scope='Analytic spatial modes and moving coordinates; matrix and six initial-lift checks; no complete PDE run',
                  independent_derivatives=True,
                  operator='D1=J^-1 Dxi; D2=J^-2 Dxi2-(Dxi J)J^-3 Dxi',
                  uniform=check_uniform(ns), moving=check_moving_convergence(ns),
                  SD_matrices=check_sd_matrices(ns), SD2_lifts=check_sd2_lifts(ns),
                  notebook_definition_sources_sha256={k: hashlib.sha256(v.encode()).hexdigest()
                      for k, v in cells.items() if k in ('dlw-spatial', 'dlw-sd', 'dlw-sd2_lift', 'dlw-sd2_evolution')})
    record['seconds'] = time.perf_counter()-started
    EVIDENCE.mkdir(exist_ok=True)
    target = EVIDENCE/'verify_second_order_spatial.json'
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(dict(success=True, seconds=record['seconds'], file=str(target),
                         uniform_orders=record['uniform']['observed_orders'],
                         moving_orders=record['moving']['observed_orders']), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
