"""Separate 2x2 panels: red analytical lines and dense blue numerical points."""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / 'submission_report'
sys.path.insert(0, str(ROOT / 'Workspaces/hs_numerics_plan'))
from hs_exact import Soliton
from generate_submission_report import exact as one_soliton_exact


def marker_indices(x):
    """Choose 121 actual saved points across the displayed physical interval."""
    targets = np.linspace(-1., 1., 121)
    inside = np.flatnonzero((x >= -1) & (x <= 1))
    return np.unique([inside[np.argmin(abs(x[inside]-target))] for target in targets])


def main():
    one_dir = ROOT / 'Workspaces/hs_four_schemes_20260927/paper_point'
    two_dir = ROOT / 'Workspaces/hs_two_soliton_short_20260928/main'
    one = json.loads((one_dir / 'results.json').read_text())
    two = json.loads((two_dir / 'results.json').read_text())
    sources = {
        'one': {s: (Path(one['rows'][f'{s}_rk4_0.003125']['profile']), one['rows'][f'{s}_rk4_0.003125']['sha256']) for s in ('S1', 'S4')},
        'two': {s: (two_dir / two['results'][s]['profile'], two['results'][s]['profile_sha256']) for s in ('S1', 'S4')},
    }
    solitons = [Soliton((5.,), phase=(0.,), shift=-.8),
                Soliton((1.1, 1.25), phase=(np.log(6.5),)*2, shift=-(1/11+1/5))]
    plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 10,
                         'axes.linewidth': .7, 'xtick.direction': 'in', 'ytick.direction': 'in'})
    xx = np.linspace(-1., 1., 32001)
    audit = []
    for case, sol in zip(('one', 'two'), solitons):
        fig, axes = plt.subplots(2, 2, figsize=(8.6, 6.2), sharex=True, sharey='row', layout='constrained')
        ref = sol.continuous_x(xx, .5)[:2]
        for row, field in enumerate(('u', 'rho')):
            for col, (scheme, label) in enumerate([('S1', 'Integrable'), ('S4', 'FD')]):
                ax = axes[row, col]
                ax.plot(xx, ref[row], color='#d64a3b', lw=.8, label='Analytical', zorder=1)
                path, sha = sources[case][scheme]
                assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
                with np.load(path) as z:
                    x = z['t0.5_' + ('x' if field == 'u' else 'rho_x')]
                    values = z['t0.5_' + field]
                assert np.isfinite(values).all() and (np.diff(x) > 0).all()
                indices = marker_indices(x)
                assert len(indices) == 121
                artist, = ax.plot(x[indices], values[indices], ls='none', marker='.',
                                 ms=2.2, color='#1776bc', markeredgewidth=0, label=label, zorder=3)
                assert len(ax.lines) == 2
                assert np.array_equal(artist.get_xdata(), x[indices])
                assert np.array_equal(artist.get_ydata(), values[indices])
                metric = float(np.abs(np.interp(xx, x, values)-ref[row]).max())
                expected = (float(np.abs(np.interp(xx, x, values)-one_soliton_exact(xx, .5)[row]).max())
                            if case == 'one' else two['results'][scheme]['metrics']['0.5'][field])
                assert abs(expected-metric) < 5e-13
                audit.append(dict(case=case, field=field, scheme=scheme, marker_count=len(indices),
                                  profile_sha256=sha, max_error=metric, marker_indices=indices.tolist()))
                ax.set(xlim=(-1, 1), ylabel='$u$' if field == 'u' else r'$\rho$')
                ax.set_xticks([-1, -.5, 0, .5, 1])
                ax.tick_params(labelleft=True)
                if row == 0:
                    ax.set_title(label, fontsize=11)
                else:
                    ax.set_xlabel('$x$')
                ax.margins(y=.12)
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], fontsize=8, loc='best',
                          frameon=True, fancybox=False, edgecolor='.8', framealpha=.9)
        title = 'One-soliton' if case == 'one' else 'Two-soliton'
        fig.suptitle(title + r', $t=0.5$', fontsize=12)
        for ext in ('png', 'svg'):
            fig.savefig(OUT / f'{case}_soliton_waveforms.{ext}', dpi=240)
        plt.close(fig)
    (OUT/'waveform_validation.json').write_text(json.dumps(dict(time=.5, x_bounds=[-1,1],
        method='each soliton has a 2x2 figure: columns Integrable/FD, rows u/rho; red analytical line and 121 blue points in each panel',
        plotted_coordinates='unmodified saved physical coordinates and field values',
        reference_style='GSG Fig. 1 and Fig. 5, pp. 365 and 367', records=audit), indent=2)+'\n')
    print('Waveforms: 8 marker series match saved fields; full-data errors match report.')


if __name__ == '__main__':
    main()
