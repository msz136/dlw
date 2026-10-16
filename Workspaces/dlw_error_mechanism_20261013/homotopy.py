"""Intervene on the actual common-physical-coordinate PE/FD update difference.

Intermediate maps are numerical controls; no claim of their nonintegrability.
All initial fields, boundary closures, grid and time are fixed.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / 'dlw_three_tracks_20261013/shared'
spec = importlib.util.spec_from_file_location('paper_frozen_generator', SHARED.parent / 'generate_shared.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
NS, BUNDLE = generator.load_solver()
OUT = HERE / 'intervention'
OUT.mkdir(exist_ok=True)


def native_to_common(model, native, t):
    p, _ = model.unpack(native)
    _, v = model.fields(native, t)
    return model.pack(p, v)


def common_to_native(model, common, t):
    if model.kind == 'FD':
        return common.copy()
    p, v = model.unpack(common)
    u = model.recover_u(p, t)
    ghosts = NS['ghost_u'](model.G, model.js, model.X.x, t, u)
    return model.pack(p, v - NS['delta0'](u, ghosts, model.h))


def mapped_step(model, common, t, dt):
    native = common_to_native(model, common, t)
    native = NS['step'](model.rhs, t, native, dt, 'RK4')
    return native_to_common(model, native, t + dt)


def common_fields(model, common, t):
    p, v = model.unpack(common)
    return model.recover_u(p, t), v


def metrics(model, state, t, iy, ix):
    uv = common_fields(model, state, t)
    exact = model.G.uv(model.js[iy], model.X.x[ix], t)
    errors = [u[np.ix_(iy, ix)] - r for u, r in zip(uv, exact)]
    return dict(u_rms=float(np.sqrt(np.mean(errors[0] ** 2))),
                v_rms=float(np.sqrt(np.mean(errors[1] ** 2))),
                joint_rms=float(np.sqrt(np.mean(errors[0] ** 2) + np.mean(errors[1] ** 2))),
                u_linf=float(np.max(np.abs(errors[0]))),
                v_linf=float(np.max(np.abs(errors[1])))), errors


def run(case, lam, halfdt=False, reuse_endpoints=False):
    cfg = NS['case_config'](case)
    if halfdt:
        cfg['dt'] /= 2
    tag = f'{case}_lambda{lam:.2f}' + ('_halfdt' if halfdt else '')
    receipt = OUT / (tag + '.json')
    if receipt.exists():
        print('EXISTS', tag, flush=True)
        return json.loads(receipt.read_text(encoding='utf-8'))
    sd = NS['SDModel'](case, 'SD', cfg)
    fd = NS['FDModel'](case, 'FD', cfg)
    initial = fd.initial()
    sd_initial_common = native_to_common(sd, sd.initial(), 0.)
    initial_mismatch = float(np.max(np.abs(sd_initial_common - initial)))
    assert initial_mismatch < 1e-12
    state = initial.copy()
    iy = np.flatnonzero(np.abs(fd.y) < cfg['eval_yhalf'])
    ix = np.flatnonzero(np.abs(fd.X.x) <= cfg['eval_half'] + 1e-10)
    steps = round(cfg['T'] / cfg['dt'])
    rows = []
    started = time.perf_counter()
    if reuse_endpoints and lam in (0, 1) and not halfdt:
        kind = 'FD' if lam == 0 else 'SD'
        model = fd if kind == 'FD' else sd
        with np.load(SHARED / f'{case}_{kind}_RK4_endpoints.npz') as archive:
            state = native_to_common(model, archive['final'], cfg['T'])
        values, errors = metrics(fd, state, cfg['T'], iy, ix)
        rows = [dict(case=case, lam=lam, dt=cfg['dt'], t=cfg['T'], **values)]
        np.savez_compressed(OUT / (tag + '.npz'), state=state, x=fd.X.x[ix], y=fd.y[iy],
                            error_u=errors[0], error_v=errors[1])
        result = dict(case=case, lam=lam, config=cfg, initial_mismatch=initial_mismatch,
                      final=rows[-1], seconds=time.perf_counter()-started,
                      reused_archived_endpoint=True,
                      source_sha256=hashlib.sha256((SHARED / 'solver_cells.json').read_bytes()).hexdigest())
        receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print('REUSED', tag, values, flush=True)
        return result
    print('START', tag, flush=True)
    for n in range(steps + 1):
        t = n * cfg['dt']
        if n % max(1, steps // 20) == 0:
            values, errors = metrics(fd, state, t, iy, ix)
            rows.append(dict(case=case, lam=lam, dt=cfg['dt'], t=t, **values))
        if n == steps:
            break
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            if lam == 0:
                state = mapped_step(fd, state, t, cfg['dt'])
            elif lam == 1:
                state = mapped_step(sd, state, t, cfg['dt'])
            else:
                a = mapped_step(fd, state, t, cfg['dt'])
                b = mapped_step(sd, state, t, cfg['dt'])
                state = a + lam * (b - a)
        assert np.all(np.isfinite(state)) and np.max(np.abs(state)) < 1000
    with (OUT / (tag + '.csv')).open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = dict(case=case, lam=lam, config=cfg, initial_mismatch=initial_mismatch,
                  final=rows[-1], seconds=time.perf_counter() - started,
                  source_sha256=hashlib.sha256((SHARED / 'solver_cells.json').read_bytes()).hexdigest())
    if lam in (0, 1) and not halfdt:
        model = 'FD' if lam == 0 else 'SD'
        with np.load(SHARED / f'{case}_{model}_RK4_endpoints.npz') as archive:
            old = archive['final']
        old_common = native_to_common(fd if model == 'FD' else sd, old, cfg['T'])
        result['regression_common_linf'] = float(np.max(np.abs(old_common - state)))
        assert result['regression_common_linf'] < 1e-10
    np.savez_compressed(OUT / (tag + '.npz'), state=state, x=fd.X.x[ix], y=fd.y[iy],
                        error_u=errors[0], error_v=errors[1])
    receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('DONE', tag, rows[-1], flush=True)
    return result


def collect():
    results = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(OUT.glob('*_lambda*.json'))]
    rows = [{**r['final'], 'halfdt': r['config']['dt'] < 1e-4} for r in results]
    if rows:
        with (OUT / 'summary.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['A', 'C'], required=True)
    parser.add_argument('--lambdas', type=float, nargs='+', default=[0, .25, .5, .75, 1])
    parser.add_argument('--halfdt', action='store_true')
    parser.add_argument('--reuse-endpoints', action='store_true')
    args = parser.parse_args()
    for lam in args.lambdas:
        run(args.case, lam, args.halfdt, args.reuse_endpoints)
    collect()
