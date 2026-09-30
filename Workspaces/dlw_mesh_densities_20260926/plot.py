"""Scientific illustration of density geometry, not a time-evolution result."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
d = np.load(HERE / 'p6_profiles.npz')
raw = json.loads((HERE / 'snapshots.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'savefig.dpi': 180})
fig, axs = plt.subplots(3, 1, figsize=(8.2, 8.4), sharex=True,
                        gridspec_kw={'height_ratios': [1, 1.15, 0.75]})
x = d['x']
axs[0].plot(x, d['u'], color='#263b50', label=r'$u$')
axs[0].plot(x, d['v'], color='#a76037', label=r'$v$')
axs[0].set_ylabel('Physical field')
axs[0].legend(loc='lower right', ncol=2)
colors = {'minus': '#278077', 'plus': '#b95b40', 'symmetric': '#725a9b'}
labels = {'minus': r'$r_-=1-(v-u_y)/4$',
          'plus': r'$r_+=1-(v+u_y)/4$',
          'symmetric': r'$r_0=1-v/4$'}
for key in colors:
    axs[1].plot(x, d[key], color=colors[key], label=labels[key])
axs[1].set_ylabel('Continuous density')
axs[1].legend(loc='upper right', fontsize=9)
center = raw['analytic_profiles']['P6']['u_center']
for ax in axs[:2]:
    ax.axvline(center, color='#999999', linewidth=0.8, linestyle=':')
    ax.grid(axis='y', alpha=0.18)
meshes = {r['density']: np.asarray(r['grid_nodes'])
          for r in raw['rows'] if r['case'] == 'P6' and r['coefficients'] == 'original'}
for level, key, label in [(2, None, 'Uniform'), (1, 'symmetric', r'Symmetric $\beta=1$'),
                           (0, 'symmetric_strength4', r'Symmetric $\beta=4$')]:
    nodes = np.linspace(-10, 10, 257) if key is None else meshes[key]
    axs[2].vlines(nodes, level - .22, level + .22,
                  color='#777777' if key is None else colors['symmetric'], linewidth=.8)
axs[2].set_yticks([0, 1, 2], [r'Sym. $\beta=4$', r'Sym. $\beta=1$', 'Uniform'])
axs[2].set_ylim(-.55, 2.55)
axs[2].set_xlim(-1.6, 1.9)
axs[2].set_xlabel(r'$x$')
fig.suptitle('DLW P6: density geometry at $t=0$\n'
             r'$(a,p,q)=(4,1,3)$; top panels: $y=0$', fontsize=13)
fig.text(.5, .015, 'Node rows: 256 cells on [-10,10], common x mesh averaged over 22 y layers.\n'
         'Initial equidistribution only; no PDE evolution or accuracy comparison.',
         ha='center', fontsize=9, color='#555555')
fig.tight_layout(rect=[0, .065, 1, .95])
fig.savefig(HERE / 'density_geometry.png')
fig.savefig(HERE / 'density_geometry.pdf')
print('Saved density_geometry.png and density_geometry.pdf')
