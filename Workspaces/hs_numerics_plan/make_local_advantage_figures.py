"""Figures for the local adaptive-grid and model-error study."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'out';FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
read=lambda name:json.loads((OUT/name).read_text())['rows']
mesh=read('local_advantage.json')
model=read('model_factor.json')
rich=read('richardson_model.json')
times=read('local_time_comparison.json')
plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.22,
                     'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})

fig,ax=plt.subplots(1,2,figsize=(11,4))
for field,axis in (('u_linf',ax[0]),('rho_linf',ax[1])):
    for gamma,marker in ((0.,'o'),(2.,'s')):
        rows=sorted((r for r in mesh if r['p']==5 and r['n']==201 and r['gamma']==gamma),key=lambda r:r['T'])
        axis.semilogy([r['T'] for r in rows],[r[field] for r in rows],'-'+marker,
                      label='uniform labels' if gamma==0 else 'curvature-adapted labels')
    axis.set(xlabel='time',ylabel=f'max {field.split("_")[0]} error',
             title='Actual moving-grid integration, N=201')
    axis.legend(fontsize=8)
fig.tight_layout();fig.savefig(FIG/'fig11_adaptive_dynamic.png');plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(11,4))
for p in (4.5,5.,5.5):
    rr=sorted((r for r in model if r['p']==p and r['T']==.5),key=lambda r:r['a'])
    ax[0].loglog([r['a'] for r in rr],[r['u_linf'] for r in rr],'-o',label=f'p={p:g}')
    ax[1].loglog([r['a'] for r in rr],[r['rho_linf'] for r in rr],'-o',label=f'p={p:g}')
for a in ax:
    a.set(xlabel='lattice spacing a',ylabel='max model error',title='Finite-a exact vs continuous exact')
    a.legend()
ax[0].set_title('u: spacing and soliton parameter')
ax[1].set_title('rho: spacing and soliton parameter')
fig.tight_layout();fig.savefig(FIG/'fig12_model_factors.png');plt.close(fig)

fig,ax=plt.subplots(1,2,figsize=(11,4))
rr=sorted((r for r in rich if r['p']==5 and r['T']==.5),key=lambda r:r['a_fine'])
for field,axis in (('u',ax[0]),('rho',ax[1])):
    axis.loglog([r['a_fine'] for r in rr],[r[field+'_fine'] for r in rr],'-o',label='single fine lattice')
    axis.loglog([r['a_fine'] for r in rr],[r[field+'_extrap'] for r in rr],'-s',label='Richardson combination')
    axis.set(xlabel='fine lattice spacing',ylabel=f'max {field} continuous error',
             title='Actual RK4 trajectories, p=5, T=0.5')
    axis.legend()
fig.tight_layout();fig.savefig(FIG/'fig13_richardson.png');plt.close(fig)
print('Wrote figures 11-13')
