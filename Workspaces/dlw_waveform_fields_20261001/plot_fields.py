"""Plot current index DLW experiments from saved physical fields, without evolution."""
from pathlib import Path
import csv
import hashlib
import importlib.util
import json

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.special import expit
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, PowerNorm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / 'Workspaces'
FIG = HERE / 'figures'
FIG.mkdir(parents=True, exist_ok=True)
T = .01
XX = np.linspace(-10., 10., 4001)
YY = (np.arange(-12, 12) + .5) / 8
EXTENT = (XX[0]-(XX[1]-XX[0])/2, XX[-1]+(XX[1]-XX[0])/2, -1.5, 1.5)
SLICE = 11  # An actual saved layer, y=-1/16, not an invented y=0 layer.
CASES = {'fig1a': ('A', 'One-soliton A', 1., 2.),
         'fig1b': ('B', 'One-soliton B', 4., -3.),
         'fig3': ('C', 'Two-soliton C', None, None)}
MODELS = ('SD', 'SD2', 'FD')
FIELDS = ('u', 'v')
COLORS = {'SD': '#1776bc', 'SD2': '#009E73', 'FD': '#8b5aaa'}
MARKERS = {'SD': 'o', 'SD2': 's', 'FD': '^'}
MANIFESTS = [BASE / p / 'out/results.json' for p in (
    'dlw_single_aligned_20260929', 'dlw_two_soliton_20260929',
    'dlw_two_soliton_euler_20260929', 'dlw_sd2_uv_init_20260929')]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reference(case, x, y, t):
    if case != 'fig3':
        _, _, p, q = CASES[case]
        a = 2.
        S, omega, ell = p + q, q*q-p*p, 1/(p-a)+1/(q+a)
        zeta = S*x[None, :] + omega*t + ell*y[:, None] - np.log(S)
        sf, sg = expit(zeta + np.log(-(p-a)/(q+a))), expit(zeta)
        return {'u': 2*S*(sf-sg),
                'v': 2*S*ell*(sf*(1-sf)+sg*(1-sg))}
    path = BASE / 'dlw_two_soliton_20260929/reference.py'
    spec = importlib.util.spec_from_file_location('dlw_plot_reference', path)
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolves the declaring module via sys.modules.
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    ref = module.TwoExact(module.CASES['fig3'], .125, continuous=True)
    return dict(zip(FIELDS, ref.uv(y/.125-.5, x, t)))


def saved_runs():
    runs = []
    for path in MANIFESTS:
        data = json.loads(path.read_text(encoding='utf-8'))
        for r in data['runs']:
            s = dict(r['spec'])
            s.setdefault('method', 'Euler' if 'euler' in path.parts[-3] else 'RK4')
            if s['variant'] != 'main' or s['case'] not in CASES:
                continue
            if s['case'] == 'fig3':
                if s['model'] == 'SD2' and 'dlw_sd2_uv_init_20260929' not in path.parts:
                    continue
                if s['model'] != 'SD2' and 'dlw_sd2_uv_init_20260929' in path.parts:
                    continue
            runs.append(dict(r, spec=s, manifest=str(path)))
    keys = [(r['spec']['case'], r['spec']['method'], r['spec']['mesh'], r['spec']['model']) for r in runs]
    assert len(runs) == len(set(keys)) == 36
    return dict(zip(keys, runs))


def export(fig, stem, vector=False):
    paths = []
    for ext in ('png', 'pdf', *(['svg'] if vector else [])):
        path = FIG / f'{stem}.{ext}'
        fig.savefig(path, dpi=180)
        paths.append(str(path.relative_to(ROOT)).replace('\\', '/'))
    plt.close(fig)
    return paths


def model_label(case, method, mesh, model):
    return model + ('†' if case == 'fig1a' and mesh == 'fixed' and model == 'SD2' else '')


def profile_plot(case, method, mesh, values, refs, metrics):
    fig, axes = plt.subplots(2, 2, figsize=(10.6, 6.6), layout='constrained')
    for j, field in enumerate(FIELDS):
        ax, err = axes[0, j], axes[1, j]
        ax.plot(XX, refs[case][field][SLICE], color='#d64a3b', lw=1.25, label='Analytical')
        for model in MODELS:
            d = values[case, method, mesh, model]
            native = np.flatnonzero((d['x'] >= XX[0]) & (d['x'] <= XX[-1]))[::2]
            line, = ax.plot(d['x'][native], d['native'][field][SLICE, native],
                ls='none', marker=MARKERS[model], ms=3.2, mfc='none', mew=.7,
                color=COLORS[model], label=model_label(case, method, mesh, model))
            assert np.array_equal(line.get_ydata(), d['native'][field][SLICE, native])
            err.plot(XX, d['error'][field][SLICE], color=COLORS[model], lw=1.15,
                     label=model_label(case, method, mesh, model))
            metrics[case, method, mesh, model, field]['plotted_native_markers'] = len(native)
        ax.set(title=f'Waveform ${field}$', ylabel=f'${field}$')
        err.set(title=f'Absolute error in ${field}$ at the same layer',
                ylabel=f'$|{field}_h-{field}_*|$', ylim=(0, None))
        err.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        for a in (ax, err):
            a.set(xlim=(-10, 10), xlabel='$x$')
            a.set_xticks([-10, -5, 0, 5, 10])
            a.grid(alpha=.16, lw=.5)
        ax.legend(frameon=False, fontsize=8.5, ncol=2)
    fig.suptitle(f'{CASES[case][1]} | {method} / {mesh} | t=0.01, y=-0.0625', fontsize=12)
    return export(fig, f'{case}_{method.lower()}_{mesh}_profiles', vector=True)


def maps(case, method, mesh, values, refs, scales, metrics):
    fig, axes = plt.subplots(2, 4, figsize=(12.8, 6.6), layout='constrained', sharex=True, sharey=True)
    for row, field in enumerate(FIELDS):
        norm = Normalize(*scales[case][field]['wave'])
        for col, label in enumerate(('Analytical', *MODELS)):
            arr = refs[case][field] if col == 0 else values[case, method, mesh, label]['sampled'][field]
            ax = axes[row, col]
            im = ax.imshow(arr, extent=EXTENT, origin='lower',
                           interpolation='nearest', aspect='auto', cmap='RdBu_r', norm=norm)
            ax.set(title=f'{label if col==0 else model_label(case, method, mesh, label)}: ${field}$', xlabel='$x$', ylabel='$y$')
            ax.tick_params(labelleft=True)
            ax.set_xlim(-10, 10)
            ax.set_xticks([-10, 0, 10]); ax.set_yticks([-1.5, 0, 1.5])
        fig.colorbar(im, ax=axes[row], shrink=.85, label=f'${field}$')
    fig.suptitle(f'{CASES[case][1]} | {method} / {mesh} | t=0.01', fontsize=12)
    wave_paths = export(fig, f'{case}_{method.lower()}_{mesh}_wavefields')

    fig, axes = plt.subplots(2, 3, figsize=(11.8, 6.8), layout='constrained', sharex=True, sharey=True)
    for row, field in enumerate(FIELDS):
        norm = PowerNorm(.5, vmin=0, vmax=scales[case][field]['error'])
        for col, model in enumerate(MODELS):
            ax = axes[row, col]
            d = values[case, method, mesh, model]
            m = metrics[case, method, mesh, model, field]
            im = ax.imshow(d['error'][field], extent=EXTENT, origin='lower',
                           interpolation='nearest', aspect='auto', cmap='magma', norm=norm)
            ax.plot(m['max_x'], m['max_y'], '+', color='#4edcc5', ms=8, mew=1.)
            ax.set(title=f'{model_label(case, method, mesh, model)}: max={m["full_max"]:.3e}',
                   xlabel='$x$', ylabel=f'$y$; $|{field}_h-{field}_*|$')
            ax.tick_params(labelleft=True)
            ax.set_xlim(-10, 10)
            ax.set_xticks([-10, 0, 10]); ax.set_yticks([-1.5, 0, 1.5])
        fig.colorbar(im, ax=axes[row], shrink=.85, label=f'$|{field}_h-{field}_*|$')
    fig.suptitle(f'{CASES[case][1]} | {method} / {mesh} | absolute errors, t=0.01 (sqrt color scale)', fontsize=12)
    return wave_paths, export(fig, f'{case}_{method.lower()}_{mesh}_errorfields')


def main():
    plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10,
        'axes.linewidth': .7, 'xtick.direction': 'in', 'ytick.direction': 'in',
        'axes.spines.top': False, 'axes.spines.right': False, 'svg.fonttype': 'none',
        'pdf.fonttype': 42, 'savefig.facecolor': 'white'})
    runs = saved_runs()
    refs = {case: reference(case, XX, YY, T) for case in CASES}
    values, metrics, archive = {}, {}, {'x': XX, 'y': YY}
    for case, ref in refs.items():
        archive[case+'_exact_u'] = ref['u']; archive[case+'_exact_v'] = ref['v']
    for key, r in runs.items():
        case, method, mesh, model = key
        assert sha(r['profile']) == r['profile_sha256']
        with np.load(r['profile'], allow_pickle=False) as z:
            x, y = z['t0.01_x'].copy(), z['y'].copy()
            assert np.array_equal(y, YY) and np.all(np.diff(x) > 0)
            native = {f: z['t0.01_'+f].copy() for f in FIELDS}
        assert x[0] <= XX[0] and x[-1] >= XX[-1]
        sampled = {f: CubicSpline(x, native[f], axis=-1)(XX) for f in FIELDS}
        error = {f: np.abs(sampled[f]-refs[case][f]) for f in FIELDS}
        hist = next(h for h in r['history'] if abs(h['t']-T) < 1e-12)
        for f in FIELDS:
            assert np.isfinite(sampled[f]).all()
            maximum = float(error[f].max())
            assert abs(maximum-hist['errors'][f]) < 1e-12
            j, i = np.unravel_index(np.argmax(error[f]), error[f].shape)
            metrics[(*key, f)] = dict(case=case, method=method, mesh=mesh, model=model, field=f,
                full_max=maximum, slice_max=float(error[f][SLICE].max()),
                max_x=float(XX[i]), max_y=float(YY[j]), history_max=hist['errors'][f],
                history_difference=maximum-hist['errors'][f], profile=r['profile'],
                profile_sha256=r['profile_sha256'], manifest=r['manifest'])
            archive['_'.join(key)+'_'+f] = sampled[f]
            archive['_'.join(key)+'_abs_error_'+f] = error[f]
        values[key] = dict(x=x, native=native, sampled=sampled, error=error)
    np.savez_compressed(HERE / 'plotted_fields.npz', **archive)
    scales = {}
    for case in CASES:
        scales[case] = {}
        for f in FIELDS:
            all_values = [refs[case][f]]+[v['sampled'][f] for k, v in values.items() if k[0] == case]
            scales[case][f] = dict(wave=[float(min(a.min() for a in all_values)),
                                        float(max(a.max() for a in all_values))],
                error=float(max(v['error'][f].max() for k, v in values.items() if k[0] == case)))
    figures = []
    for case in CASES:
        for method, mesh in (('RK4', 'fixed'), ('RK4', 'moving'), ('Euler', 'fixed'), ('Euler', 'moving')):
            profile = profile_plot(case, method, mesh, values, refs, metrics)
            waves, errors = maps(case, method, mesh, values, refs, scales, metrics)
            figures.append(dict(case=case, method=method, mesh=mesh, profiles=profile, wavefields=waves, errorfields=errors))
            print(f'Plotted {case} {method} {mesh}', flush=True)
    records = list(metrics.values())
    with (HERE / 'field_errors.csv').open('w', newline='', encoding='utf-8-sig') as h:
        writer = csv.DictWriter(h, fieldnames=list(records[0]))
        writer.writeheader(); writer.writerows(records)
    result = dict(time=T, x_points=len(XX), y_points=len(YY), slice_y=float(YY[SLICE]),
        source_runs=36, verified_error_fields=72, png_figures=36, pdf_figures=36, svg_profiles=12,
        reconstruction='CubicSpline(x, native_field, axis=-1), default not-a-knot; no interpolation in y',
        display='Nearest display of the 24 saved y layers; shared color scales across all methods and meshes for each case and field; errors use gamma=0.5 PowerNorm, with ticks in original absolute-error units',
        maximum_history_difference=max(abs(r['history_difference']) for r in records),
        sources=[dict(path=str(p), sha256=sha(p)) for p in MANIFESTS],
        reference_sources=[dict(path=str(p), sha256=sha(p)) for p in [Path(__file__), BASE/'dlw_two_soliton_20260929/reference.py']],
        scales=scales, figures=figures, records=records)
    (HERE / 'plot_validation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('source_runs', 'verified_error_fields', 'png_figures', 'maximum_history_difference')}))


if __name__ == '__main__':
    main()
