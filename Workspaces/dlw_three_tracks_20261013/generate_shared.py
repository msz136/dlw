"""Generate real paper-solver trajectories without changing the notebook.

Outputs contain native-grid physical fields and the continuous exact reference.
No interpolation or denoising is used. Default: A/C, SD/FD RK4, plus SD half dt.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import gc
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SHARED = HERE / 'shared'
NOTEBOOK = ROOT / 'notebook' / 'DLW数值分析report.ipynb'
CELL_IDS = ('imports', 'config', 'reference', 'spatial', 'sd_fd', 'sd', 'fd', 'time')


def load_solver():
    SHARED.mkdir(parents=True, exist_ok=True)
    frozen = SHARED / 'solver_cells.json'
    if frozen.exists():
        bundle = json.loads(frozen.read_text(encoding='utf-8'))
    else:
        raw = NOTEBOOK.read_bytes()
        nb = json.loads(raw)
        cells = {c.get('id'): ''.join(c.get('source', [])) for c in nb['cells']}
        bundle = {'notebook': str(NOTEBOOK), 'notebook_sha256': hashlib.sha256(raw).hexdigest(),
                  'cells': {key: cells['dlw-' + key] for key in CELL_IDS}}
        frozen.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding='utf-8')
    ns = {}
    for key in CELL_IDS:
        source = bundle['cells'][key].replace('from IPython.display import display',
                                               'display = lambda *args, **kwargs: None')
        exec(compile(source, str(frozen) + ':' + key, 'exec'), ns)
    return ns, bundle


def run(ns, bundle, case, model, half=False):
    cfg = ns['case_config'](case)
    if half:
        cfg['dt'] /= 2
    label = f'{case}_{model}_RK4' + ('_halfdt' if half else '')
    dest = SHARED / (label + '.npz')
    receipt = SHARED / (label + '.json')
    if dest.exists() and receipt.exists():
        print('EXISTS', label, flush=True)
        return
    obj = ns['SDModel' if model == 'SD' else 'FDModel'](case, model, cfg)
    state = obj.initial()
    nsteps = round(cfg['T'] / cfg['dt'])
    assert nsteps % 20 == 0 and np.isclose(nsteps * cfg['dt'], cfg['T'])
    stride = nsteps // 20
    ix = np.flatnonzero(abs(obj.X.x) <= cfg['eval_half'] + 1e-10)
    iy = np.flatnonzero(abs(obj.y) < cfg['eval_yhalf'])
    fields = {key: [] for key in ('u', 'v', 'exact_u', 'exact_v')}
    times = []
    full_errors = []
    initial = state.copy()
    t0 = time.perf_counter()
    print('START', label, cfg, flush=True)
    for n in range(nsteps + 1):
        t = n * cfg['dt']
        if n % stride == 0:
            uv = obj.fields(state, t)
            exact = obj.G.uv(obj.js, obj.X.x, t)
            for key, value in zip(fields, (*uv, *exact)):
                fields[key].append(value[np.ix_(iy, ix)].copy())
            full_errors.append([float(np.max(abs(uv[k] - exact[k]))) for k in range(2)])
            times.append(t)
        if n == nsteps:
            break
        with np.errstate(over='raise', invalid='raise', divide='raise'):
            state = ns['step'](obj.rhs, t, state, cfg['dt'], 'RK4')
        assert np.isfinite(state).all() and abs(state).max() < 1000
    arrays = {key: np.stack(value) for key, value in fields.items()}
    meta = {'label': label, 'case': case, 'model': model, 'method': 'RK4', 'mesh': 'fixed',
            'config': cfg, 'reference': 'continuous Gram exact physical u,v from paper notebook',
            'sampling': 'native uniform grid, unfiltered and uninterpolated, 21 actual times',
            'x_boundary': 'periodic numerical x stencil on buffered computational domain',
            'y_boundary': 'paper prescribed lower trace and upper error extrapolation',
            'notebook_sha256': bundle['notebook_sha256'],
            'solver_cells_sha256': hashlib.sha256((SHARED / 'solver_cells.json').read_bytes()).hexdigest(),
            'shape_tyx': list(arrays['u'].shape), 'seconds_evolution': time.perf_counter() - t0}
    meta['initial_max_error'] = {f: float(abs(arrays[f][0] - arrays['exact_' + f][0]).max()) for f in ('u', 'v')}
    meta['terminal_native_error'] = {f: float(abs(arrays[f][-1] - arrays['exact_' + f][-1]).max()) for f in ('u', 'v')}
    saved = ROOT / 'Workspaces/dlw_paper_20261009/buffered_run' / (f'{case}_{model}_RK4_fixed_state.npz')
    if not half and saved.exists():
        with np.load(saved) as old:
            delta = float(abs(old['state'][:-obj.X.n] - state).max())
        meta['archived_terminal_state_max_difference'] = delta
        assert delta < 1e-10, (label, delta)
    np.savez_compressed(dest, x=obj.X.x[ix], y=obj.y[iy], t=np.array(times),
                        metadata_json=json.dumps(meta, ensure_ascii=False), **arrays)
    np.savez_compressed(SHARED / (label + '_endpoints.npz'), initial=initial, final=state,
                        x=obj.X.x, y=obj.y, full_domain_errors=np.array(full_errors))
    meta['npz_sha256'] = hashlib.sha256(dest.read_bytes()).hexdigest()
    receipt.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print('DONE', label, json.dumps(meta['terminal_native_error']), 'seconds', round(time.perf_counter() - t0, 2), flush=True)
    del arrays, fields, state, initial
    gc.collect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['A', 'C', 'all'], default='all')
    args = parser.parse_args()
    ns, bundle = load_solver()
    for case in (['A', 'C'] if args.case == 'all' else [args.case]):
        for model, half in [('SD', False), ('FD', False), ('SD', True)]:
            run(ns, bundle, case, model, half)
