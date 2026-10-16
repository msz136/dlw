"""Frozen snapshot protocol; no time evolution or fitted propagator here."""
from pathlib import Path
import argparse
import csv
import gc
import hashlib
import json
import time
import numpy as np
from common_sources import load_solver, source_parts, exact_jets, physical_qt

HERE = Path(__file__).resolve().parent


def norms(z):
    return {'linf': float(np.max(np.abs(z))), 'rms': float(np.sqrt(np.mean(z * z)))}


def write_csv(path, rows):
    if rows:
        with path.open('w', newline='', encoding='utf-8-sig') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)


def jet_validation(ns):
    records = []
    for case in ('A', 'C'):
        obj = ns['SDModel'](case, 'SD', ns['case_config'](case))
        js = obj.js[::max(1, len(obj.js) // 15)]
        x = np.linspace(-ns['case_config'](case)['eval_half'], ns['case_config'](case)['eval_half'], 25)
        t = .004
        jets = exact_jets(obj, t, x, js)
        uv = obj.G.uv(js, x, t)
        records.append({'case': case, 'check': 'uv_identity', 'epsilon': 0,
                        'u': float(abs(jets['u'] - uv[0]).max()), 'v': float(abs(jets['v'] - uv[1]).max())})
        for eps in (.002, .001, .0005):
            xm, xp = obj.G.uv(js, x - eps, t), obj.G.uv(js, x + eps, t)
            tm, tp = obj.G.uv(js, x, t - eps), obj.G.uv(js, x, t + eps)
            for typ, numeric in [('x1', [(xp[k] - xm[k]) / (2 * eps) for k in range(2)]),
                                 ('x2', [(xp[k] - 2 * uv[k] + xm[k]) / eps**2 for k in range(2)]),
                                 ('t1', [(tp[k] - tm[k]) / (2 * eps) for k in range(2)])]:
                suffix = {'x1': 'x', 'x2': 'xx', 't1': 't'}[typ]
                records.append({'case': case, 'check': typ, 'epsilon': eps,
                                **{f: float(abs(numeric[k] - jets[f + suffix]).max()) for k, f in enumerate(('u', 'v'))}})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=['A', 'C', 'all'], default='all')
    parser.add_argument('--quick', action='store_true')
    parser.add_argument('--resume', action='store_true', help='Load durable CSV rows and run only missing configurations.')
    args = parser.parse_args()
    ns, bundle = load_solver()
    jet_checks = jet_validation(ns)
    write_csv(HERE / 'jet_validation.csv', jet_checks)
    allmetrics, correlations, algebra, checks = [], [], [], []
    if args.resume:
        for stem, rows in [('source_metrics', allmetrics), ('source_correlations', correlations),
                           ('sd_fd_algebra', algebra), ('identity_checks', checks)]:
            path = HERE / f'{stem}_{args.case}.csv'
            if path.exists():
                with path.open(encoding='utf-8-sig', newline='') as f:
                    for row in csv.DictReader(f):
                        for key in list(row):
                            if key not in ('case', 'scan', 'model', 'region', 'field', 'source', 'backend', 'term'):
                                row[key] = float(row[key])
                        rows.append(row)
    def completed(case, scan, value, kind):
        return any(r['case'] == case and r['scan'] == scan and float(r['value']) == float(value)
                   and r['model'] == kind for r in checks)
    cases = ('A', 'C') if args.case == 'all' else (args.case,)
    start = time.perf_counter()
    for case in cases:
        base = ns['case_config'](case)
        runs = [('snapshot', t, dict(base), t) for t in (0, .005, .01)]
        if not args.quick:
            for h in (.2, .05, .025):
                cfg = dict(base, h=h)
                runs.append(('h_refine', h, cfg, 0.))
            for dx in (.2, .05, .025):
                cfg = dict(base, nx=round(base['L'] / dx))
                runs.append(('dx_refine', dx, cfg, 0.))
            for extra in (5., 10.):
                cfg = dict(base, L=base['L'] + 2 * extra, nx=round((base['L'] + 2 * extra) / .1))
                runs.append(('x_buffer', extra, cfg, 0.))
                cfg = dict(base, yhalf=base['yhalf'] + extra)
                runs.append(('y_buffer', extra, cfg, 0.))
        for scan, value, cfg, t in runs:
            print('RUN', case, scan, value, 'h=', cfg['h'], 'nx=', cfg['nx'], flush=True)
            for kind in ('SD', 'FD'):
                if completed(case, scan, value, kind):
                    print('EXISTS', case, scan, value, kind, flush=True)
                    continue
                obj = ns[kind + 'Model'](case, kind, cfg)
                result = source_parts(obj, t, details=True)
                meta = dict(case=case, scan=scan, value=value, t=t, model=kind,
                            h=obj.h, dx=obj.X.dx, L=cfg['L'], yhalf=cfg['yhalf'])
                checks.append(dict(meta, **result['checks']))
                for field in ('p', 'u', 'v'):
                    y = (obj.y[:-1] + obj.y[1:]) / 2 if field == 'p' else obj.y
                    ix = np.flatnonzero(abs(obj.X.x) <= cfg['eval_half'] + 1e-10)
                    iy = np.flatnonzero(abs(y) < cfg['eval_yhalf'])
                    mask = np.ix_(iy, ix)
                    for region in ('observation', 'full'):
                        fs = {k: v[field][mask] if region == 'observation' else v[field]
                              for k, v in result['fields'].items()}
                        for name, z in fs.items():
                            allmetrics.append(dict(meta, region=region, field=field, source=name, **norms(z)))
                        yv, xv = fs['y_model'].ravel(), fs['x_stencil'].ravel()
                        yn, xn = np.linalg.norm(yv), np.linalg.norm(xv)
                        correlations.append(dict(meta, region=region, field=field,
                            cosine_y_x=float(yv @ xv / (yn * xn)) if yn * xn else 0.,
                            rms_total=norms(fs['total'])['rms'], rms_y=norms(fs['y_model'])['rms'],
                            rms_x=norms(fs['x_stencil'])['rms'], rms_wrap=norms(fs['x_wrap'])['rms'],
                            cancellation_ratio=float(np.linalg.norm(fs['total']) / sum(np.linalg.norm(fs[k]) for k in ('y_model', 'x_stencil', 'x_wrap')))))
                # SD-FD differences are computed together at exactly the same physical state.
                if kind == 'SD':
                    for backend, rhs in result['backend_rhs'].items():
                        for field, entries in [('p', {'nonlinear_flux_N': rhs['N'], 'reconstruction_G': rhs['G'], 'difference': rhs['sd_minus_fd_p']}),
                                               ('v', {'FD_compatibility_C': rhs['C'], 'recovered_qt_difference': rhs['qt_difference'], 'difference': rhs['sd_minus_fd_v']})]:
                            y = (obj.y[:-1] + obj.y[1:]) / 2 if field == 'p' else obj.y
                            mask = np.ix_(np.flatnonzero(abs(y) < cfg['eval_yhalf']), np.flatnonzero(abs(obj.X.x) <= cfg['eval_half'] + 1e-10))
                            for name, z in entries.items():
                                algebra.append(dict(meta, backend=backend, field=field, term=name, **norms(z[mask])))
                del result, obj
                gc.collect()
            # Durable incremental output after every completed configuration.
            write_csv(HERE / f'source_metrics_{args.case}.csv', allmetrics)
            write_csv(HERE / f'source_correlations_{args.case}.csv', correlations)
            write_csv(HERE / f'sd_fd_algebra_{args.case}.csv', algebra)
            write_csv(HERE / f'identity_checks_{args.case}.csv', checks)
    receipt = {'case_selection': args.case, 'quick': args.quick, 'resumed': args.resume, 'seconds_this_run': time.perf_counter() - start,
               'frozen_notebook_sha256': bundle['notebook_sha256'],
               'frozen_solver_sha256': hashlib.sha256((HERE.parents[1] / 'dlw_three_tracks_20261013/shared/solver_cells.json').read_bytes()).hexdigest(),
               'common_sources_sha256': hashlib.sha256((HERE / 'common_sources.py').read_bytes()).hexdigest(),
               'protocol_sha256': hashlib.sha256((HERE / 'PROTOCOL.md').read_bytes()).hexdigest(),
               'metric_rows': len(allmetrics), 'identity_rows': len(checks),
               'max_checks': {key: max(r[key] for r in checks) for key in result_check_keys()},
               'max_uv_identity': max(max(r['u'], r['v']) for r in jet_checks if r['check'] == 'uv_identity')}
    (HERE / f'validation_{args.case}.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False), flush=True)


def result_check_keys():
    return ('actual_rhs_max_difference', 'sum_source_max_difference',
            'sd_fd_p_algebra_max_difference', 'sd_fd_v_algebra_max_difference')


if __name__ == '__main__':
    main()
