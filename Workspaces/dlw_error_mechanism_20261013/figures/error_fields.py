"""Actual A v errors and independently propagated predictions, no fitted data.

Layout: aligned spatial panels as in oa-geo-bg-21-811-2024-f02.
Color: blue-white-red signed field; each row shares actual/prediction scale.
Residual: own prominently labelled color scale, never shared implicitly.
Typography: the project's existing DejaVu Serif scientific figure style.
Inputs are read only; no smoothing, interpolation or error-field fitting.
"""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import ScalarFormatter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / 'transport/A_T0.040_dt0.000100'
plt.rcParams.update({'font.family': 'DejaVu Serif', 'font.size': 9,
    'axes.linewidth': .6, 'xtick.direction': 'in', 'ytick.direction': 'in',
    'savefig.dpi': 300, 'pdf.fonttype': 42})
CMAP = LinearSegmentedColormap.from_list('dlw_signed', ['#312b84', '#8b95d4', '#ffffff', '#ffb5b5', '#b82b36'])


def main():
    fig = plt.figure(figsize=(10.6, 10.4), layout='constrained')
    grid = fig.add_gridspec(4, 5, width_ratios=[1, 1, .045, 1, .045], hspace=.12, wspace=.04)
    rows = []
    for row, (kind, step, t) in enumerate([('SD', 100, .01), ('FD', 100, .01), ('SD', 400, .04), ('FD', 400, .04)]):
        path = DATA / f'frame_{step:05d}.npz'
        with np.load(path) as archive:
            assert float(archive['t']) == t
            x, y = archive['x'].copy(), archive['y'].copy()
            actual = archive[f'actual_{kind}'][1].copy()
            predicted = archive[f'{kind}_from_{kind}'][1].copy()
        assert actual.shape == predicted.shape == (100, 101)
        assert np.all(np.isfinite(actual)) and np.all(np.isfinite(predicted))
        residual = actual - predicted
        common_scale = float(max(np.max(abs(actual)), np.max(abs(predicted))))
        residual_scale = float(np.max(abs(residual)))
        rel = float(np.linalg.norm(residual) / np.linalg.norm(actual))
        vals = [actual, predicted, residual]
        name = 'PE' if kind == 'SD' else 'FD'
        axes = [fig.add_subplot(grid[row, col]) for col in (0, 1, 3)]
        for col, (ax, val) in enumerate(zip(axes, vals)):
            scale = common_scale if col < 2 else residual_scale
            im = ax.pcolormesh(x, y, val, cmap=CMAP, vmin=-scale, vmax=scale,
                              shading='nearest', rasterized=True)
            ax.set_xlim(x[0], x[-1]); ax.set_ylim(y[0], y[-1])
            ax.set_aspect('equal')
            ax.set_xticks([-5, 0, 5]); ax.set_yticks([-4, 0, 4])
            ax.set_xlabel('x', labelpad=1)
            if col == 0:
                ax.set_ylabel(f'{name}, t = {t:.2f}\ny', labelpad=4)
            else:
                ax.set_yticklabels([])
            if row == 0:
                ax.set_title(['Actual error', 'Linear prediction', 'Actual − prediction'][col], fontsize=11, pad=10)
            ax.text(.025, .975, f'({chr(97 + 3 * row + col)})', transform=ax.transAxes,
                    ha='left', va='top', fontsize=9, bbox=dict(facecolor='white', alpha=.8, edgecolor='none', pad=1))
            if col == 1:
                cax = fig.add_subplot(grid[row, 2])
                cb = fig.colorbar(im, cax=cax)
                cb.ax.set_title('Shared', fontsize=8, pad=6)
            elif col == 2:
                cax = fig.add_subplot(grid[row, 4])
                cb = fig.colorbar(im, cax=cax)
                cb.ax.set_title('Own scale', fontsize=8, pad=6, color='#9a2727')
                ax.text(.5, -.22, f'Relative residual: {100 * rel:.4g}%',
                        transform=ax.transAxes, ha='center', va='top', fontsize=8.5, color='#9a2727')
            else:
                continue
            cb.set_ticks([-scale, 0., scale])
            formatter = ScalarFormatter(useMathText=True)
            formatter.set_powerlimits((0, 0))
            cb.formatter = formatter
            cb.update_ticks()
            cb.ax.tick_params(labelsize=7.5, length=2)
        rows.append(dict(model=kind, field='v', t=t,
            actual_rms=float(np.sqrt(np.mean(actual ** 2))),
            predicted_rms=float(np.sqrt(np.mean(predicted ** 2))),
            residual_rms=float(np.sqrt(np.mean(residual ** 2))),
            relative_field_residual=rel,
            common_color_limit=common_scale, residual_color_limit=residual_scale,
            source_file=str(path), source_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    fig.suptitle('Case A: spatial evolution of the v error', fontsize=13)
    fig.savefig(HERE / 'error_fields.png', dpi=300, bbox_inches='tight')
    fig.savefig(HERE / 'error_fields.pdf', bbox_inches='tight')
    plt.close(fig)
    with (HERE / 'error_fields_metrics.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    checks = []
    with (DATA / 'timeseries.csv').open(newline='', encoding='utf-8') as stream:
        recorded = list(csv.DictReader(stream))
    for row in rows:
        for label, key in [(f'actual_{row["model"]}', 'actual_rms'), (f'{row["model"]}_from_{row["model"]}', 'predicted_rms')]:
            item = next(r for r in recorded if r['label'] == label and float(r['t']) == row['t'])
            difference = abs(float(item['v_rms']) - row[key])
            assert difference < 1e-15
            checks.append(dict(model=row['model'], t=row['t'], label=label, rms_record_difference=difference))
    validation = dict(input_type='actual solver and independently generated linear-prediction fields',
        field_index=1, field='v', data_shape=[100, 101], rows=rows,
        same_row_actual_prediction_color_limits=True, residual_separate_color_scale=True,
        smoothing=False, interpolation=False, checks=checks, passed=True)
    (HERE / 'error_fields_validation.json').write_text(json.dumps(validation, indent=2), encoding='utf-8')
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
