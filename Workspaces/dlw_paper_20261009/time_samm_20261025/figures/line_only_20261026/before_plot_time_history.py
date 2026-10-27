"""Error histories for Centered-SD with forward Euler, RK4 and Crank-Nicolson.

Two figures, one per physical field. Each figure has four panels, one per test
problem, and three curves per panel. Values come from the recorded maximum
absolute errors at every integer time step, joined without smoothing.
"""
from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, LogLocator, LogFormatterMathtext, NullFormatter

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SRC = PROJECT / 'time'
OUT = HERE
CASES = ['A', 'D', 'Gaussian', 'Sinusoidal']
TITLES = {'A': 'One-soliton case', 'D': 'Two-soliton case',
          'Gaussian': 'Gaussian case', 'Sinusoidal': 'Sinusoidal case'}
METHODS = [('Euler', 'Forward Euler', '#E07A23', '-', 1.1, 3),
           ('RK4', 'RK4', '#2878B5', '-', 1.7, 0),
           ('CN', 'Crank-Nicolson', '#299568', (0, (5.2, 3.0)), 1.3, 0)]

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.labelsize': 9,
                     'axes.titlesize': 9.5, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
                     'axes.linewidth': .65, 'xtick.direction': 'out', 'ytick.direction': 'out',
                     'pdf.fonttype': 42, 'ps.fonttype': 42, 'mathtext.fontset': 'dejavusans',
                     'savefig.facecolor': 'white', 'figure.facecolor': 'white',
                     'axes.facecolor': 'white', 'legend.frameon': False})


def style(ax, lo, hi):
    ax.tick_params(length=3, pad=3)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.set_yscale('log')
    ax.set_ylim(lo, hi)
    ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.,), numticks=4))
    ax.yaxis.set_major_formatter(LogFormatterMathtext())
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10) * .1))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(axis='y', which='major', color='#e5e7eb', lw=.5, zorder=0)
    ax.set_xlim(0, 0.0101)


def figure(field, summary):
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 4.75), sharex=True)
    handles = []
    col = 0 if field == 'u' else 1
    for k, (ax, case) in enumerate(zip(axes.ravel(), CASES)):
        d = np.load(SRC / f'{case}_time.npz')
        t = d['t']
        lo, hi = 1, 0
        for order, (key, label, colour, ls, lw, every) in enumerate(METHODS):
            e = d['errors_' + key][:, col]
            line, = ax.plot(t[1:], e[1:], color=colour, ls=ls, lw=lw, label=label,
                            zorder=3 + order, solid_capstyle='round', dash_capstyle='round',
                            marker='^' if every else None, markevery=every, ms=3.2,
                            mfc=colour, mec=colour, mew=.4)
            if case == 'A':
                handles.append(line)
            lo = min(lo, e[1:].min())
            hi = max(hi, e[-1])
        style(ax, lo / 1.7, hi * 1.9)
        ax.set_title(f'({chr(97 + k)}) {TITLES[case]}', pad=6)
        summary.setdefault(case, {})[field] = {
            key: float(d['errors_' + key][-1, col]) for key in ('Euler', 'RK4', 'CN')}
    for ax in axes[:, 0]:
        ax.set_ylabel(rf'$E_{field}(t)$', labelpad=2)
    for ax in axes[1, :]:
        ax.set_xlabel(r'$t$', labelpad=2)
    labels = [entry[1] for entry in METHODS]
    fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.005),
               handlelength=2.2, columnspacing=2.4, borderaxespad=0., fontsize=9)
    fig.subplots_adjust(left=.095, right=.985, bottom=.105, top=.865, hspace=.40, wspace=.245)
    png = OUT / f'time_error_{field}.png'
    pdf = OUT / f'time_error_{field}.pdf'
    fig.savefig(png, dpi=300, bbox_inches='tight', pad_inches=.05)
    fig.savefig(pdf, dpi=300, bbox_inches='tight', pad_inches=.05)
    plt.close(fig)
    meta = dict(field=field, png=png.name, pdf=pdf.name,
                png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),
                pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
    print(json.dumps(meta), flush=True)
    return meta


if __name__ == '__main__':
    summary = {}
    meta = [figure('u', summary), figure('v', summary)]
    (OUT / 'time_summary.json').write_text(json.dumps(dict(meta=meta, terminal=summary), indent=2), encoding='utf-8')
