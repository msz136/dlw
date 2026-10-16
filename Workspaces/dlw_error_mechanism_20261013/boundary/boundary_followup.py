"""Prespecified lower-trace intervention in the actual frozen A solver."""
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
SHARED = HERE.parents[1] / 'dlw_three_tracks_20261013/shared'
spec = importlib.util.spec_from_file_location('boundary_frozen_solver', SHARED.parent / 'generate_shared.py')
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
NS, BUNDLE = generator.load_solver()


def run(kind):
    cfg = NS['case_config']('A')
    assert cfg['yhalf'] == 10 and cfg['L'] == 20 and cfg['nx'] == 200
    cfg['yhalf'] = 20
    obj = NS['SDModel' if kind == 'SD' else 'FDModel']('A', kind, cfg)
    state = obj.initial()
    iy = np.flatnonzero(abs(obj.y) < cfg['eval_yhalf'])
    ix = np.flatnonzero(abs(obj.X.x) <= cfg['eval_half'] + 1e-10)
    x, y = obj.X.x[ix], obj.y[iy]
    with np.load(SHARED / f'A_{kind}_RK4.npz') as arc:
        old = {key: arc[key].copy() for key in ('x', 'y', 't', 'u', 'v', 'exact_u', 'exact_v')}
    assert np.array_equal(x, old['x']) and np.array_equal(y, old['y'])
    assert x.size == 101 and y.size == 100
    nt = round(cfg['T'] / cfg['dt'])
    assert nt == 100
    values = {key: [] for key in ('u', 'v', 'exact_u', 'exact_v')}
    rows = []
    exact_max = 0.
    started = time.perf_counter()
    print('START', kind, obj.shape, flush=True)
    for n in range(nt + 1):
        t = n * cfg['dt']
        if n % 5 == 0:
            frame = n // 5
            assert t == old['t'][frame]
            uv = obj.fields(state, t)
            ex = obj.G.uv(obj.js[iy], x, t)
            for f, field, ref in zip(('u', 'v'), uv, ex):
                field = field[np.ix_(iy, ix)]
                values[f].append(field.copy())
                values['exact_' + f].append(ref.copy())
                exact_max = max(exact_max, float(np.max(abs(ref - old['exact_' + f][frame]))))
                assert np.array_equal(ref, old['exact_' + f][frame])
                err = field - ref
                eold = old[f][frame] - ref
                delta = err - eold
                energy = float(np.mean(delta ** 2))
                projected = float(np.mean(np.mean(delta, axis=0) ** 2))
                old_rms = float(np.sqrt(np.mean(eold ** 2)))
                rows.append(dict(model=kind, field=f, t=t,
                    old_error_rms=old_rms, new_error_rms=float(np.sqrt(np.mean(err ** 2))),
                    delta_error_rms=float(np.sqrt(energy)),
                    delta_relative_old_error=float(np.sqrt(energy) / old_rms) if old_rms > 1e-13 else None,
                    y_constant_squared_fraction=projected / energy if energy > 1e-26 else None,
                    delta_y_residual_rms=float(np.sqrt(max(0., energy - projected))),
                    delta_error_linf=float(np.max(abs(delta)))))
        if n == nt:
            break
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            state = NS['step'](obj.rhs, t, state, cfg['dt'], 'RK4')
        assert np.all(np.isfinite(state)) and np.max(abs(state)) < 1000
    arrays = {key: np.stack(value) for key, value in values.items()}
    np.savez_compressed(HERE / f'A_{kind}_yhalf20.npz', x=x, y=y, t=old['t'],
                        delta_error_u=arrays['u'] - old['u'], delta_error_v=arrays['v'] - old['v'], **arrays)
    with (HERE / f'A_{kind}_timeseries.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = dict(model=kind, config=cfg, seconds=time.perf_counter() - started,
                  exact_reference_max_difference=exact_max,
                  target_grid_identical=True, target_times_identical=True,
                  initial_max_error={f: float(np.max(abs(arrays[f][0] - arrays['exact_' + f][0]))) for f in ('u', 'v')},
                  protocol_sha256=hashlib.sha256((HERE / 'PROTOCOL.md').read_bytes()).hexdigest(),
                  solver_sha256=hashlib.sha256((SHARED / 'solver_cells.json').read_bytes()).hexdigest(),
                  terminal=rows[-2:])
    (HERE / f'A_{kind}_validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('DONE', json.dumps(result), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', choices=['SD', 'FD'], required=True)
    run(parser.parse_args().kind)
