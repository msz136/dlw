"""Computed data only. Aligned small multiples follow gallery oa-tech-pone-0116670-f16.
Keep the established LDG blue/orange; distinguish FD by green/purple/red.
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze_comparison import HERE,records,label,evaluator
from mch.exact import profile

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight'})
data=json.loads((HERE/'analysis/comparison.json').read_text());rows=data['rows']
styles={'LDG-c':('#2166ac','o','-'),'LDG-d':('#d6604d','s','--'),'FD2 aligned':('#542788','^',':'),'FD4 aligned':('#9970ab','v',':'),
        'FD2 half-cell':('#238b45','^','-'),'FD4 half-cell':('#66a61e','v','--'),'FD-Rusanov':('#a50f15','D','-.')}
out=HERE/'figures';out.mkdir(exist_ok=True)
def standard_rows(case,t,method):
    return sorted([r for r in rows if r['case']==case and r['t']==t and r['method']==method and abs(r['dt']-(.0005 if case=='5.1' else .00025))<1e-12],key=lambda r:r['dof'])

fig,axes=plt.subplots(1,2,figsize=(11,4.3),layout='constrained')
for name in ['LDG-c','LDG-d','FD2 aligned','FD4 aligned','FD-Rusanov']:
    rr=standard_rows('5.1',.5,name);color,marker,ls=styles[name]
    for ax,metric in zip(axes,['l2_u','sampled_linf_u']):
        ax.loglog([r['dof'] for r in rr],[r[metric] for r in rr],color=color,marker=marker,ls=ls,label=name,ms=4)
for ax,y in zip(axes,[r'$L^2$ error of $u$',r'Sampled $L^\infty$ error of $u$']):
    ax.set(xlabel='Evolved scalar degrees of freedom',ylabel=y);ax.grid(alpha=.17)
axes[0].legend(frameon=False,fontsize=8)
fig.suptitle('Smooth soliton, t = 0.5 | same domain, RK4, common physical-field evaluation')
for ext in ['png','pdf']:fig.savefig(out/f'smooth_fd_ldg.{ext}',dpi=300)
plt.close(fig)

fig,axes=plt.subplots(2,2,figsize=(12,8),layout='constrained')
allrec=records()
for j,t in enumerate([.5,5.]):
    ax=axes[0,j];xx=np.linspace(-1.5,7.5,5001)
    ax.plot(xx,profile('5.4',xx,t)[0],color='black',lw=1.4,label='Exact')
    names=['LDG-c','LDG-d','FD4 half-cell','FD-Rusanov']+(['FD4 aligned'] if t==.5 else [])
    for name in names:
        candidates=[r for r in allrec if r['config']['case']=='5.4' and label(r)==name and r['config']['n']==(640 if r['kind']=='LDG' else 2560) and abs(r['config']['dt']-.00025)<1e-12]
        r=candidates[0];a=np.load(Path(r['path'])/'trajectory.npz');i=np.argmin(abs(a['t']-t))
        color,marker,ls=styles[name];ax.plot(xx,evaluator(r,a['u'][i])(xx),color=color,ls=ls,lw=1.2,label=name)
    ax.set(xlabel='x',ylabel='u',title=f't = {t:g} | 2560 evolved degrees of freedom',ylim=(-.7 if t==.5 else -.1,1.65 if t==.5 else 1.35))
    ax.legend(frameon=False,fontsize=8,loc='upper right' if t==.5 else 'upper left')
for name in ['LDG-c','LDG-d','FD2 half-cell','FD4 half-cell','FD-Rusanov']:
    rr=standard_rows('5.4',5.,name);color,marker,ls=styles[name]
    axes[1,0].loglog([r['dof'] for r in rr],[r['l2_u'] for r in rr],color=color,marker=marker,ls=ls,label=name,ms=4)
    axes[1,1].semilogx([r['dof'] for r in rr],[r['peak_position_error'] for r in rr],color=color,marker=marker,ls=ls,label=name,ms=4)
axes[1,0].set(xlabel='Evolved scalar degrees of freedom',ylabel=r'$L^2$ error of $u$',title='t = 5 | completed runs only')
axes[1,1].set(xlabel='Evolved scalar degrees of freedom',ylabel='Peak-position error',title='t = 5 | signed displacement')
axes[1,1].axhline(0,color='#888888',lw=.6)
for ax in axes[1]:ax.grid(alpha=.17)
handles,names=axes[1,0].get_legend_handles_labels()
fig.legend(handles,names,frameon=False,fontsize=9,loc='lower center',bbox_to_anchor=(.5,-.045),ncol=5)
fig.suptitle('Peakon | mesh phase changes direct-difference behaviour',fontsize=14)
for ext in ['png','pdf']:fig.savefig(out/f'peak_fd_ldg.{ext}',dpi=300)
plt.close(fig)
print('Two figure sets generated from computed trajectories.')
