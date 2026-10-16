"""Actual computed data. Layout follows paper Figure 3: profiles and energy histories.
Reference: black; conservative: blue; dissipative: orange. No smoothed data.
Run from project root: python figures/plot_results.py
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze import load_index
from mch.ldg import LDG
from mch.exact import profile

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight'})
colors={'conservative':'#2166ac','dissipative':'#d6604d'}
figdir=Path('figures');figdir.mkdir(exist_ok=True)
base=load_index('suite_peakon_*.json')
fig,axes=plt.subplots(2,3,figsize=(13,7),layout='constrained')
for row in base:
 c=row['config'];d=LDG(**{k:c[k] for k in ['n','k','left','right','kappa','flux']});z=np.load(Path(row['path'])/'trajectory.npz')
 for j,t in enumerate([0,2,5]):
  i=np.argmin(abs(z['t']-t));xx=np.linspace(-3,8,2201)
  if row==base[0]:axes[0,j].plot(xx,profile('5.4',xx,t)[0],color='black',lw=1.2,label='Exact')
  axes[0,j].plot(xx,d.sample(z['u'][i],xx),color=colors[c['flux']],ls='--' if c['flux']=='dissipative' else '-',lw=1.1,label='LDG '+c['flux'])
  axes[0,j].set(xlabel='x',ylabel='u',title=f't = {t}',ylim=(-.05,1.32))
 hist=json.loads((Path(row['path'])/'history.json').read_text());tt=np.array([r['t'] for r in hist]);EE=np.array([r['energy'] for r in hist])
 axes[1,0].plot(tt,EE[0]-EE,color=colors[c['flux']],label=c['flux'])
 if c['flux']=='conservative':
  axes[1,1].plot(tt,EE[0]-EE,color=colors[c['flux']],label=r'$\Delta t=5\times10^{-4}$')
 else:axes[1,2].plot(tt,np.sqrt(EE[0])-np.sqrt(EE),color=colors[c['flux']],label=r'Computed $\sqrt{E(0)}-\sqrt{E(t)}$')
for row in load_index('suite_timecheck_*.json'):
 if row['config']['flux']=='conservative':
  hist=json.loads((Path(row['path'])/'history.json').read_text())
  axes[1,1].plot([r['t'] for r in hist],[r['energy_loss'] for r in hist],ls='--',color='#4393c3',label=r'$\Delta t=2.5\times10^{-4}$')
paper=np.loadtxt('search/figure3_dissipative_digitized.csv',delimiter=',',skiprows=1)
axes[1,2].plot(paper[:,0],paper[:,1],color='black',ls=':',label='Paper Fig. 3 (vector path)')
axes[1,0].set(xlabel='t',ylabel=r'$E(0)-E(t)$',title='Squared energy, full domain')
axes[1,1].set(xlabel='t',ylabel=r'$E(0)-E(t)$',title='Conservative: time-step control')
axes[1,2].set(xlabel='t',ylabel='Ordinate',title='Metric comparison (unconfirmed)')
for ax in axes.ravel():ax.legend(fontsize=8,frameon=False)
fig.suptitle('Example 5.4 | P3, N = 640 | First reproduction',fontsize=14)
for ext in ['png','pdf']:fig.savefig(figdir/f'peakon_first.{ext}',dpi=300)
plt.close(fig)

fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
for k,ax in zip((1,2,3),axes):
 for group,pattern,style in [('Original interval','suite_smooth_*.json','--'),('Expanded interval','control_domain_*.json','-')]:
  for flux in colors:
   rows=[r for r in load_index(pattern) if r['config']['k']==k and r['config']['flux']==flux]
   rows.sort(key=lambda r:r['config']['n'])
   h=[(r['config']['right']-r['config']['left'])/r['config']['n'] for r in rows]
   e=[r['final']['energy_error'] for r in rows]
   ax.loglog(h,e,style,marker='o' if flux=='conservative' else 's',ms=4,color=colors[flux],label=group+', '+flux)
 ax.set(xlabel='h',ylabel=r'$\sqrt{\|U-u\|^2+\|R-r\|^2}$',title=f'Example 5.1, P{k}')
 ax.invert_xaxis();ax.grid(alpha=.2)
axes[0].legend(fontsize=7,frameon=False)
fig.suptitle('Boundary sensitivity at matched cell widths | periodic truncation',fontsize=13)
for ext in ['png','pdf']:fig.savefig(figdir/f'smooth_convergence.{ext}',dpi=300)
plt.close(fig)

fig,axes=plt.subplots(1,3,figsize=(12,4.1),layout='constrained')
for j,case in enumerate(['5.2','5.3','5.5']):
 for row in [r for r in load_index('suite_other_*.json') if r['config']['case']==case]:
  c=row['config'];d=LDG(**{k:c[k] for k in ['n','k','left','right','kappa','flux']});z=np.load(Path(row['path'])/'trajectory.npz')
  xl,xr=((-10,20) if case=='5.2' else ((-5,35) if case=='5.3' else (-3*np.pi,3*np.pi)))
  xx=np.linspace(xl,xr,2201)
  if c['flux']=='conservative':axes[j].plot(xx,profile(case,xx,5,alpha=c['alpha'],kappa=c['kappa'])[0],color='black',lw=1,label='Exact')
  axes[j].plot(xx,d.sample(z['u'][-1],xx),color=colors[c['flux']],lw=1,ls='--' if c['flux']=='dissipative' else '-',label=c['flux'])
 axes[j].set(xlabel='x',ylabel='u',title=f'Example {case}, t = 5')
 axes[j].legend(fontsize=8,frameon=False,loc='upper center',bbox_to_anchor=(.5,-.19),ncol=3,columnspacing=.8)
fig.suptitle('Other benchmark entry points | first grid only',fontsize=13)
for ext in ['png','pdf']:fig.savefig(figdir/f'other_cases.{ext}',dpi=300)
print('Three figure sets written from saved trajectories.')
