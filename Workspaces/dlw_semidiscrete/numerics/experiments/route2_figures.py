"""Rebuild route-two scientific figures from the validated JSON artifacts."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'out/route2'
FIG = ROOT / 'figures'
FIG.mkdir(exist_ok=True)

budget = json.loads((OUT / 'budget.json').read_text(encoding='utf-8'))
adjoint = json.loads((OUT / 'adjoint.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'savefig.dpi': 180})


def budget_figure():
    fig, axs = plt.subplots(3, 2, figsize=(10.6, 10.3), sharex=True)
    for i, case in enumerate(('P1', 'P6', 'P10')):
        for j, field in enumerate(('u', 'v')):
            ax = axs[i, j]
            rows = sorted((r for r in budget['runs'] if r['config']['case'] == case and
                           r['config']['nx'] == 256 and r['config']['initial'] == 'finite' and
                           r['config']['model'] == 'structure'),
                          key=lambda r: r['config']['h'])
            h = [r['config']['h'] for r in rows]
            for key, label, color, style in (
                ('total_vs_continuous', 'total', '#17324d', '-'),
                ('model', 'finite-h model', '#c56d24', '--'),
                ('solver_vs_finite', 'solver', '#26877b', ':')):
                ax.loglog(h, [r['errors'][field][key] for r in rows], marker='o',
                          color=color, linestyle=style, lw=1.9, label=label)
            d = next(d for d in budget['prospective_balances'] if d['case'] == case and d['field'] == field)
            if min(h) <= d['predicted_h_balance'] <= max(h):
                ax.axvline(d['predicted_h_balance'], color='#777777', alpha=.6, lw=1)
            ax.set_title(f'{case} · {field}    pilot balance h={d["predicted_h_balance"]:.3g}')
            ax.grid(alpha=.22, which='both')
            ax.set_xlim(.055, .28)
            ax.xaxis.set_major_locator(FixedLocator([.0625, .125, .25]))
            ax.xaxis.set_major_formatter(FixedFormatter(['1/16', '1/8', '1/4']))
            ax.xaxis.set_minor_formatter(NullFormatter())
            if j == 0:
                ax.set_ylabel('maximum field error')
            if i == 2:
                ax.set_xlabel('y spacing h; x nodes = 256')
    handles, labels = axs[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(.5, 1.01))
    fig.suptitle('Where does the short-time error come from?  T = 0.01', y=1.045, fontsize=13)
    fig.tight_layout()
    path = FIG / 'fig18_route2_budget.png'
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path


def adjoint_figure():
    rows = [r for r in adjoint['results'] if r['config']['dt'] == .0005]
    fig, axs = plt.subplots(3, 2, figsize=(10.6, 9.3))
    for i, r in enumerate(rows):
        label = f'{r["case"]} · {r["config"]["model"]}'
        t = [x['t'] for x in r['by_time']]
        signed = [x['spatial_goal_signed'] for x in r['by_time']]
        absolute = [x['spatial_goal_absolute_cells'] for x in r['by_time']]
        ax = axs[i, 0]
        ax.plot(t, signed, marker='o', ms=3, color='#17324d', label='signed contribution')
        ax.plot(t, absolute, ls='--', color='#c56d24', label='cellwise absolute sum')
        ax.set_title(label + ' · one-step goal attribution')
        ax.set_ylabel('phase contribution')
        ax.grid(alpha=.22)
        if i == 2:
            ax.set_xlabel('step start time')
        ax = axs[i, 1]
        vals = [r['target']['linear_proxy_predicted'],
                r['target']['linear_proxy_actual'],
                r['target']['profile_fit_actual']['shift'],
                r['linear_absolute_bound']]
        ax.bar(range(4), vals, color=['#26877b', '#17324d', '#7593af', '#c56d24'])
        ax.set_yscale('log')
        ax.set_xticks(range(4), labels=['linear\nprediction', 'linear\nactual',
                                          'profile\nfit', 'absolute\nsum'])
        ax.set_title(label + ' · prediction, measured shift, bound')
        ax.grid(alpha=.22, axis='y')
    fig.suptitle('Discrete RK4 adjoint for a smooth position target', fontsize=13)
    fig.tight_layout()
    path = FIG / 'fig19_route2_adjoint.png'
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)
    return path


if __name__ == '__main__':
    print(budget_figure())
    print(adjoint_figure())
