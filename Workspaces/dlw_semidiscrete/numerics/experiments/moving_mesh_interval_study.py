"""Refresh-interval study, with frozen initial Gram grid as interval infinity.

The long-distance experiment evolves a *transport* equation, not DLW.  All
intervals start from identical Gram nodes and fields.  Remaps at the final
observation time are excluded so the comparison measures evolved fields.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'lib'), str(ROOT / 'experiments')]
import numpy as np

from moving_mesh import MovingGrid, gram_mesh
from moving_mesh_study import ALL
from moving_mesh_route1_coupled import norm, periodic_interpolate, run as dlw_run
from moving_mesh_route1_transport import density, redistribute
from parametric import Exact

PARAMETER_INDICES = (0, 1, 6, 9)
INTERVALS_D = (None, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625)
METRICS = ('u_common_error', 'v_common_error', 'u_node_error', 'v_node_error')


def transport_run(pars, width, nx, dt, interval_d, diagnose_defects=False):
    h, length = .125, 20.
    js = np.arange(-12, 12)
    speed = pars.p - pars.q
    exact = Exact(pars, h)
    grid = MovingGrid(nx, length)
    x0 = gram_mesh(pars, h, js, grid.xi)
    grid.set_s(x0 - grid.xi)
    u, v = exact.uv(js, grid.x, 0.)
    shadow_u, shadow_v = (u.copy(), v.copy()) if diagnose_defects else (None, None)
    target = np.linspace(-8, 8, 801)
    final_time = 2 * width / abs(speed)
    steps = round(final_time / dt)
    step = final_time / steps
    if interval_d is None:
        event_indices = set()
    else:
        # Schedule against absolute target distances, avoiding accumulated
        # rounding drift and excluding the endpoint D=2.
        count = int(np.floor((2 - 1e-12) / interval_d))
        event_indices = {max(1, min(steps-1, round(k * interval_d * steps / 2)))
                         for k in range(1, count + 1)}
    events = []
    segment_defects = []
    observations = []
    status = 'complete'
    stop_t = None

    def truth(x, t):
        old = ((x - speed * t + length / 2) % length) - length / 2
        return exact.uv(js, old, 0.)

    def metrics(t):
        tu, tv = truth(target, t)
        nu, nv = truth(grid.x, t)
        return {'t': float(t), 'D': float(abs(speed) * t / width),
                'u_common_error': norm(periodic_interpolate(grid.x, u, target, length) - tu),
                'v_common_error': norm(periodic_interpolate(grid.x, v, target, length) - tv),
                'u_node_error': norm(u - nu), 'v_node_error': norm(v - nv),
                'min_dx': float(min(grid.spacing())), 'min_J': float(min(grid.J)),
                'min_R': float(min(density(u, v, h)))}

    start = time.perf_counter()
    observations.append(metrics(0.))
    for i in range(steps):
        t = i * step
        try:
            def rhs(U, V):
                return -speed * grid.d1(U), -speed * grid.d1(V)
            def rk_step(U, V):
                a, b = rhs(U, V)
                c, d = rhs(U + step * a / 2, V + step * b / 2)
                e, f = rhs(U + step * c / 2, V + step * d / 2)
                g, k = rhs(U + step * e, V + step * f)
                return U + step * (a + 2 * c + 2 * e + g) / 6, \
                       V + step * (b + 2 * d + 2 * f + k) / 6
            u, v = rk_step(u, v)
            if diagnose_defects:
                shadow_u, shadow_v = rk_step(shadow_u, shadow_v)
            now = (i + 1) * step
            if i + 1 in event_indices:
                old_x = grid.x.copy()
                old_truth = truth(old_x, now)
                if diagnose_defects:
                    segment_defects.append({'t_end': float(now),
                                            'u_propagation_defect': norm(shadow_u - old_truth[0]),
                                            'v_propagation_defect': norm(shadow_v - old_truth[1])})
                old_errors = (norm(u - old_truth[0]), norm(v - old_truth[1]))
                u, v = redistribute(grid, u, v, h)
                new_truth = truth(grid.x, now)
                if diagnose_defects:
                    shadow_u, shadow_v = new_truth[0].copy(), new_truth[1].copy()
                new_errors = (norm(u - new_truth[0]), norm(v - new_truth[1]))
                oracle = (periodic_interpolate(old_x, old_truth[0], grid.x, length),
                          periodic_interpolate(old_x, old_truth[1], grid.x, length))
                events.append({'t': float(now), 'D': float(abs(speed) * now / width),
                               'max_displacement': norm(grid.x - old_x),
                               'u_node_error_before': old_errors[0],
                               'v_node_error_before': old_errors[1],
                               'u_node_error_after': new_errors[0],
                               'v_node_error_after': new_errors[1],
                               'u_exact_interpolation_defect': norm(oracle[0] - new_truth[0]),
                               'v_exact_interpolation_defect': norm(oracle[1] - new_truth[1])})
            if not (np.all(np.isfinite(u)) and np.all(np.isfinite(v))):
                raise ValueError('nonfinite state')
            if any(abs((i + 1) / steps - d / 2) < .5 / steps for d in (.5, 1., 2.)):
                observations.append(metrics(now))
        except ValueError as exc:
            status = str(exc)
            stop_t = float(t)
            break
    if diagnose_defects and status == 'complete':
        end_truth = truth(grid.x, final_time)
        segment_defects.append({'t_end': float(final_time),
                                'u_propagation_defect': norm(shadow_u - end_truth[0]),
                                'v_propagation_defect': norm(shadow_v - end_truth[1])})
    return {'status': status, 'stop_t': stop_t, 'nx': nx,
            'dt_nominal': dt, 'dt_actual': step,
            'interval_D_requested': interval_d,
            'event_D_actual': [2 * k / steps for k in sorted(event_indices)],
            'remaps': len(events), 'seconds': time.perf_counter() - start,
            'observations': observations, 'events': events,
            'segment_defects': segment_defects}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    args = parser.parse_args()
    base = ROOT / 'out' / 'moving_mesh'
    geom = json.loads((base / 'route1_geometry.json').read_text(encoding='utf-8'))
    widths = {r['parameter_id']: r['width'] for r in geom['cases']}
    params = (0, 6) if args.quick else PARAMETER_INDICES
    resolutions = (64,) if args.quick else (64, 128, 256)
    intervals = (None, 1., .25) if args.quick else INTERVALS_D
    result = {'scope': {'transport_equation': 'z_t+(p-q)z_x=0, not DLW',
                        'D_final': 2, 'h': .125, 'x_length': 20,
                        'common_x': [-8, 8, 801],
                        'interval_unit': 'wave widths travelled',
                        'infinity': 'initial Gram redistribution, then frozen',
                        'exclude_remap_at_final_time': True,
                        'boundary': 'periodic x'}, 'runs': [], 'dlw_runs': []}
    for idx in params:
        pid = f'P{idx+1}'
        for nx in resolutions:
            for interval in intervals:
                row = transport_run(ALL[idx], widths[pid], nx, .001, interval,
                                    diagnose_defects=(nx == 128))
                row['parameter_id'] = pid
                result['runs'].append(row)
                print('transport', pid, nx, interval, row['status'], row['remaps'], flush=True)
    if not args.quick:
        # Independent time-step check at the central resolution.
        for idx in PARAMETER_INDICES:
            pid = f'P{idx+1}'
            for interval in (None, 1., .25, .0625):
                row = transport_run(ALL[idx], widths[pid], 128, .0005, interval)
                row['parameter_id'] = pid
                result['runs'].append(row)
                print('time-step', pid, interval, row['status'], flush=True)
        # DLW has only a short validated window; retain failures and never
        # infer a long-distance DLW improvement from the transport experiment.
        for idx in PARAMETER_INDICES:
            pid = f'P{idx+1}'
            for model in ('structure', 'fd'):
                for refresh in (None, .02, .01, .005, .0025):
                    mode = 'static_adaptive' if refresh is None else 'intermittent'
                    row = dlw_run(ALL[idx], model, mode, .04, .000125,
                                  refresh=.01 if refresh is None else refresh, nx=128)
                    row['parameter_id'] = pid
                    row['interval_t'] = refresh
                    result['dlw_runs'].append(row)
                    print('DLW', pid, model, refresh, row['status'], flush=True)
    sources = [Path(__file__), ROOT / 'lib/moving_mesh.py',
               ROOT / 'experiments/moving_mesh_route1_transport.py',
               ROOT / 'experiments/moving_mesh_route1_coupled.py']
    result['source_sha256'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sources}
    dest = base / ('interval_quick.json' if args.quick else 'interval_study.json')
    dest.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
