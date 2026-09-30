"""Scientific figures comparing the symmetric monitor with both branches."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from analyze import load_rows
from experiment import OUT,CASES

HERE=Path(__file__).resolve().parent
new,_,old=load_rows();rows={**old,**new['rows']}
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
def e(case,route,branch,phase):return rows[f'{case}_{route}_{branch}_{phase}']['snapshots']['0.01']['errors']
fig,ax=plt.subplots(figsize=(9.7,3.9))
vals=[];labels=[]
for route in ('fd','sd'):
    for f in ('u','v'):
        vals.append([e(case,route,'symmetric','main')[f]/e(case,route,'fixed','main')[f] for case in CASES])
        labels.append(route.upper()+', '+f)
vals=np.asarray(vals)
im=ax.imshow(vals,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=.2,vcenter=1,vmax=1.2),aspect='auto')
for i in range(4):
    for j in range(8):ax.text(j,i,f'{vals[i,j]:.3f}',ha='center',va='center',color='white' if vals[i,j]<.4 else '#222222')
ax.set_xticks(range(8),CASES);ax.set_yticks(range(4),labels);ax.axhline(1.5,color='white',lw=2)
ax.set_title('Symmetric moving / fixed total error\n'+r'Euler, $T=0.01$, $N_x=512$, $h_y=1/8$, $\beta=1$')
fig.colorbar(im,ax=ax,label='Ratio (< 1 is better)',shrink=.8)
fig.tight_layout();fig.savefig(HERE/'symmetric_benefits.png');fig.savefig(HERE/'symmetric_benefits.pdf')

fig,axs=plt.subplots(2,2,figsize=(9.6,7.5))
colors={'minus':'#267b73','plus':'#b85f41','symmetric':'#7355a0'}
labels={'minus':r'$r_-$','plus':r'$r_+$','symmetric':r'$r_{\mathrm{sym}}$'}
for i,route in enumerate(('fd','sd')):
    for j,phase in enumerate(('main','fine_quarter')):
        ax=axs[i,j];base=e('P6',route,'fixed',phase)
        for branch in colors:
            ee=e('P6',route,branch,phase);x,y=ee['u']/base['u'],ee['v']/base['v']
            ax.scatter([x],[y],color=colors[branch],s=50)
            offset=(5,5) if branch!='symmetric' else (5,-14)
            ax.annotate(labels[branch],(x,y),xytext=offset,textcoords='offset points',color=colors[branch],fontsize=11)
        ax.axhline(1,color='#888888',ls=':',lw=1)
        ax.axvline(1,color='#888888',ls=':',lw=1)
        ax.grid(alpha=.15)
        ax.set_xlabel(r'$E_u/E_{u,\mathrm{fixed}}$')
        ax.set_ylabel(r'$E_v/E_{v,\mathrm{fixed}}$')
        ax.set_title(route.upper()+(' — main grid' if phase=='main' else ' — fine grid, quarter time step'))
        if phase=='main':ax.set_xlim(.15,.7);ax.set_ylim(.25,.6)
        elif route=='fd':ax.set_xlim(.38,.8);ax.set_ylim(.5,.75)
        else:ax.set_xlim(.76,1.03);ax.set_ylim(.93,1.09)
fig.suptitle('P6: smaller in both coordinates is better; symmetry is a trade-off',fontsize=12)
fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(HERE/'p6_tradeoff.png');fig.savefig(HERE/'p6_tradeoff.pdf')
print('Saved two PNG/PDF figures')
