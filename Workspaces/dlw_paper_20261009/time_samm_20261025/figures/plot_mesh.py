"""Mesh distribution and terminal error profiles for the fixed/adaptive comparison.

Spacing is shown normalized by the uniform spacing at interval midpoints.
Profiles are the maximum absolute field error over the transverse layers at each
native x node, so the curves are drawn at their own node positions.
"""
from pathlib import Path
import sys, json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SRC = PROJECT / 'samm_periodic'
sys.path.insert(0, str(PROJECT.parents[0] / 'spatial_audit_20261023'))
from run import Model, HALF_WIDTHS

OUT = HERE
CASES = ['A', 'D']
TITLE = {'A': '(a) One-soliton case', 'D': '(b) Two-soliton case'}
BLUE, ORANGE, GREY = '#2878B5', '#E07A23', '#8a8f98'

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9, 'axes.labelsize': 9,
                     'axes.titlesize': 9.5, 'xtick.labelsize': 8, 'ytick.labelsize': 8,
                     'axes.linewidth': .65, 'xtick.direction': 'out', 'ytick.direction': 'out',
                     'pdf.fonttype': 42, 'ps.fonttype': 42, 'mathtext.fontset': 'dejavusans',
                     'savefig.facecolor': 'white', 'figure.facecolor': 'white',
                     'axes.facecolor': 'white', 'legend.frameon': False})


def axes_style(ax):
    ax.tick_params(length=3, pad=3)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    fm = ScalarFormatter(useMathText=True)
    fm.set_useOffset(False)
    fm.set_powerlimits((-3, 3))
    ax.yaxis.set_major_formatter(fm)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.grid(axis='y', which='major', color='#e5e7eb', lw=.45, zorder=0)


def spacing_figure():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75))
    for ax, case in zip(axes, CASES):
        d = np.load(SRC / f'{case}_moving_0.0001.npz')
        dx = 0.1
        L = len(d['x']) * dx
        for key, colour, ls, lw, zorder, label in (('x', BLUE, '-', 1.15, 3, r'$T=0.01$'),
                                                   ('x0', GREY, (0, (3.4, 2.0)), 1.5, 4, r'$t=0$')):
            x = d[key]
            spacing = np.diff(np.r_[x, x[0] + L])
            mid = x + spacing / 2
            ax.plot(mid, spacing / dx, color=colour, ls=ls, lw=lw, label=label, zorder=zorder)
        ax.axhline(1.0, color=ORANGE, lw=1.0, ls=(0, (1.2, 1.8)), zorder=2)
        axes_style(ax)
        ax.set_xlim(-L / 2, L / 2)
        ax.set_title(TITLE[case], pad=6)
        ax.set_xlabel(r'$x$', labelpad=2)
    axes[0].set_ylabel(r'spacing / $\Delta x$')
    axes[0].legend(loc='lower right', fontsize=8.5, handlelength=2.2, borderaxespad=.2)
    fig.subplots_adjust(left=.105, right=.985, bottom=.185, top=.905, wspace=.22)
    for stem in ('mesh_spacing',):
        png, pdf = OUT / (stem + '.png'), OUT / (stem + '.pdf')
        fig.savefig(png, dpi=300, bbox_inches='tight', pad_inches=.05)
        fig.savefig(pdf, dpi=300, bbox_inches='tight', pad_inches=.05)
        print(json.dumps(dict(png=png.name, sha=hashlib.sha256(png.read_bytes()).hexdigest())), flush=True)
    plt.close(fig)


def profiles(case):
    m = Model(case, 'Centered-SD', .1, .1)
    r = HALF_WIDTHS[case]
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.75))
    for ax, field in zip(axes, ('u', 'v')):
        yv = (m.y[1:] + m.y[:-1]) / 2
        for mode, colour, ls, mfc, label in (('uniform', ORANGE, (0, (4, 2)), 'none', 'Uniform mesh'),
                                             ('moving', BLUE, '-', BLUE, 'Adaptive mesh')):
            d = np.load(SRC / f'{case}_{mode}_0.0001.npz')
            x = d['x']
            if field == 'u':
                exact = m.profile(m.y, 0.01, x)[0]
                err = np.abs(d['u'] - exact)
                keep = abs(m.y) < r
                prof = err[keep].max(axis=0)
            else:
                exact = m.profile(yv, 0.01, x)[1]
                err = np.abs(d['v'] - exact)
                keep = abs(yv) < r
                prof = err[keep].max(axis=0)
            sel = abs(x) <= r
            ax.plot(x[sel], prof[sel], color=colour, ls=ls, lw=1.1, marker='o', ms=2.2,
                    mfc=mfc, mec=colour, mew=.5, markevery=1, label=label, zorder=3)
        axes_style(ax)
        ax.set_xlabel(r'$x$', labelpad=2)
        ax.set_title(rf'({"ab"[0 if field == "u" else 1]}) {"$u$" if field == "u" else "$v$"}', pad=6)
        ax.set_ylabel(rf'max$_{{|y|<{r:g}}}|{field}_h-{field}^*|$' if field == 'u' else '')
        ax.set_xlim(-r, r)
    axes[0].legend(loc='upper right', fontsize=8.5, handlelength=2.2, borderaxespad=.2)
    fig.subplots_adjust(left=.115, right=.985, bottom=.185, top=.905, wspace=.24)
    stem = f'mesh_profile_{case}'
    png, pdf = OUT / (stem + '.png'), OUT / (stem + '.pdf')
    fig.savefig(png, dpi=300, bbox_inches='tight', pad_inches=.05)
    fig.savefig(pdf, dpi=300, bbox_inches='tight', pad_inches=.05)
    print(json.dumps(dict(png=png.name, sha=hashlib.sha256(png.read_bytes()).hexdigest())), flush=True)
    plt.close(fig)


if __name__ == '__main__':
    spacing_figure()
    for c in CASES:
        profiles(c)
