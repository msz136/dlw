"""Validate and plot the refresh-interval sweep from its saved trajectories."""
from pathlib import Path
import hashlib
import json
import os
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'out' / 'moving_mesh' / 'interval_study.json'
EXTENDED = ROOT / 'out' / 'moving_mesh' / 'interval_extended.json'
OUT = ROOT / 'out' / 'moving_mesh' / 'interval_validation.json'
FIG = ROOT / 'figures' / 'fig21_mesh_refresh_interval.png'
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'out' / 'mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PIDS = ('P1', 'P2', 'P7', 'P10')
INTERVALS = (None, 2., 1., .5, .25, .125, .0625)
FIELDS = ('u_common_error', 'v_common_error', 'u_node_error', 'v_node_error')


def main():
    data = json.loads(DATA.read_text(encoding='utf-8'))
    extended = json.loads(EXTENDED.read_text(encoding='utf-8'))
    runs = {(r['parameter_id'], r['nx'], r['dt_nominal'], r['interval_D_requested']): r
            for r in data['runs']}
    assert len(data['runs']) == 100 and len(runs) == 100
    assert len(data['dlw_runs']) == 40
    assert all(r['status'] == 'complete' for r in data['runs'] + data['dlw_runs'])
    assert len(extended['runs']) == 84
    assert all(r['status'] == 'complete' for r in extended['runs'])
    max_frozen_difference = 0.
    max_initial_difference = 0.
    minimum_spacing = float('inf')
    minimum_j = float('inf')
    minimum_r = float('inf')
    main_rows = []
    for pid in PIDS:
        for nx in (64, 128, 256):
            frozen = runs[pid, nx, .001, None]
            no_event = runs[pid, nx, .001, 2.]
            assert frozen['remaps'] == no_event['remaps'] == 0
            for f in FIELDS:
                max_frozen_difference = max(max_frozen_difference,
                    abs(frozen['observations'][-1][f] - no_event['observations'][-1][f]))
            for interval in INTERVALS:
                row = runs[pid, nx, .001, interval]
                assert abs(row['observations'][-1]['D'] - 2.) < 1e-12
                if interval not in (None, 2.):
                    assert row['remaps'] == int((2 - 1e-12) // interval)
                for f in FIELDS:
                    max_initial_difference = max(max_initial_difference,
                        abs(row['observations'][0][f] - frozen['observations'][0][f]))
                for o in row['observations']:
                    minimum_spacing = min(minimum_spacing, o['min_dx'])
                    minimum_j = min(minimum_j, o['min_J'])
                    minimum_r = min(minimum_r, o['min_R'])
                if interval not in (None, 2.):
                    ratios = {f: row['observations'][-1][f] / frozen['observations'][-1][f]
                              for f in FIELDS}
                    main_rows.append({'parameter_id': pid, 'nx': nx, 'interval_D': interval,
                                      'remaps': row['remaps'], 'ratios': ratios,
                                      'sum_u_exact_remap_defect': sum(e['u_exact_interpolation_defect']
                                                                      for e in row['events']),
                                      'sum_v_exact_remap_defect': sum(e['v_exact_interpolation_defect']
                                                                      for e in row['events'])})
    assert max_frozen_difference == max_initial_difference == 0.
    all128 = {(r['parameter_id'], r['interval_D_requested']): r
              for r in data['runs'] if r['nx'] == 128 and r['dt_nominal'] == .001}
    all128.update({(r['parameter_id'], r['interval_D_requested']): r
                   for r in extended['runs']})
    assert len(all128) == 16 * len(INTERVALS)
    extended_frozen_difference = 0.
    extended_initial_difference = 0.
    median_rows = []
    for pid in (f'P{i}' for i in range(1, 17)):
        base = all128[pid, None]
        pair = all128[pid, 2.]
        for f in FIELDS:
            extended_frozen_difference = max(extended_frozen_difference,
                abs(base['observations'][-1][f] - pair['observations'][-1][f]))
        for interval in INTERVALS:
            row = all128[pid, interval]
            assert len(row['segment_defects']) == row['remaps'] + 1
            for f in FIELDS:
                extended_initial_difference = max(extended_initial_difference,
                    abs(base['observations'][0][f] - row['observations'][0][f]))
    assert extended_frozen_difference == extended_initial_difference == 0.
    for interval in (1., .5, .25, .125, .0625):
        ratios = []
        for pid in (f'P{i}' for i in range(1, 17)):
            base = all128[pid, None]['observations'][-1]
            obs = all128[pid, interval]['observations'][-1]
            ratios.append((obs['u_common_error']/base['u_common_error'],
                           obs['v_common_error']/base['v_common_error']))
        median_rows.append({'interval_D': interval,
                            'median_u_ratio': statistics.median(x[0] for x in ratios),
                            'median_v_ratio': statistics.median(x[1] for x in ratios),
                            'both_fields_lower_count': sum(u<1 and v<1 for u,v in ratios),
                            'both_fields_20pct_lower_count': sum(u<.8 and v<.8 for u,v in ratios)})
    max_dt_difference = 0.
    for pid in PIDS:
        for interval in (None, 1., .25, .0625):
            coarse = runs[pid, 128, .001, interval]['observations'][-1]
            fine = runs[pid, 128, .0005, interval]['observations'][-1]
            for field in FIELDS:
                max_dt_difference = max(max_dt_difference,
                    abs(coarse[field]-fine[field])/max(abs(fine[field]), 1e-30))

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.2), sharex=True)
    colors = {'P1':'#177e89', 'P2':'#d17a22', 'P7':'#5e8b3d', 'P10':'#804fa4'}
    for ax, field, name in zip(axes, FIELDS[:2], ('u', 'v')):
        for pid in PIDS:
            points = [r for r in main_rows if r['parameter_id'] == pid and r['nx'] == 128]
            ax.plot([0] + [r['remaps'] for r in points],
                    [1] + [r['ratios'][field] for r in points],
                    'o-', color=colors[pid], label=pid, lw=1.7, ms=4)
        ax.axhline(1, ls='--', color='0.45', lw=1)
        ax.set_xscale('symlog', linthresh=1)
        ax.set_xticks((0, 1, 3, 7, 15, 31), labels=('0', '1', '3', '7', '15', '31'))
        ax.set_xlabel('Remaps before two pulse widths')
        ax.set_ylabel(f'{name} common-point error / frozen-grid error')
        ax.grid(alpha=.23)
    axes[0].legend(ncol=2, fontsize=9)
    fig.suptitle('Refresh interval scan: controlled transport, $n_x=128$ (not DLW)')
    fig.tight_layout()
    FIG.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG, dpi=170)
    plt.close(fig)

    result = {'scope': {'transport_runs': len(data['runs'])+len(extended['runs']),
                        'dlw_runs': len(data['dlw_runs']),
                        'parameters': [f'P{i}' for i in range(1,17)], 'nx': [64, 128, 256],
                        'intervals_D': INTERVALS,
                        'final_remap_excluded': True},
              'checks': {'all_runs_complete': True,
                         'frozen_equals_interval_2_exactly': max_frozen_difference,
                         'all_initial_errors_identical': max_initial_difference,
                         'extended_frozen_equals_interval_2_exactly': extended_frozen_difference,
                         'extended_initial_errors_identical': extended_initial_difference,
                         'min_observed_spacing': minimum_spacing,
                         'min_observed_J': minimum_j,
                         'min_observed_R': minimum_r,
                         'max_dt_halving_relative_metric_change': max_dt_difference},
              'transport_ratios': main_rows,
              'all_parameter_medians_nx128': median_rows,
              'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (Path(__file__), ROOT / 'experiments/moving_mesh_interval_study.py',
                                          ROOT / 'experiments/moving_mesh_interval_extended.py')},
              'artifact_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (DATA, EXTENDED, FIG)}}
    OUT.write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result['checks'], indent=2))
    for f in FIELDS[:2]:
        print(f, 'lower than frozen:', sum(r['ratios'][f] < 1 for r in main_rows), '/', len(main_rows))


if __name__ == '__main__':
    main()
