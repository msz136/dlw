"""Scientific figures from saved experiments, including unsuccessful controls."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from run import CASES,OUT

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
main=json.loads((OUT/'main.json').read_text())['rows']
sup=json.loads((OUT/'supplement.json').read_text())['rows']

fig,ax=plt.subplots(figsize=(10,5.3))
labels=[];data=[]
for route in ('fd','sd'):
    for branch in ('minus','plus'):
        for field in ('u','v'):
            labels.append(f'{route.upper()}, '+('$r_-$' if branch=='minus' else '$r_+$')+f', {field}')
            data.append([main[f'{case}_{route}_{branch}_main']['snapshots']['0.01']['errors'][field]/main[f'{case}_{route}_fixed_main']['snapshots']['0.01']['errors'][field] for case in CASES])
data=np.array(data)
im=ax.imshow(data,cmap='RdBu_r',norm=TwoSlopeNorm(vmin=.15,vcenter=1,vmax=1.2),aspect='auto')
for i in range(data.shape[0]):
    for j in range(data.shape[1]):ax.text(j,i,f'{data[i,j]:.3f}',ha='center',va='center',color='white' if data[i,j]<.45 else '#222222',fontsize=9)
ax.set_xticks(range(len(CASES)),CASES);ax.set_yticks(range(len(labels)),labels)
ax.axhline(3.5,color='white',linewidth=2)
ax.set_title('Moving / fixed total error, within each spatial method\n'
             r'Euler; $T=0.01$, $N_x=512$, $L=40$, $h_y=1/8$')
fig.colorbar(im,ax=ax,label='Error ratio (< 1 is better)',shrink=.83)
fig.tight_layout();fig.savefig(HERE/'main_error_ratios.png');fig.savefig(HERE/'main_error_ratios.pdf')

fig,axs=plt.subplots(1,3,figsize=(14,4.1))
for branch,color,label in [('minus','#267b73',r'$r_-$'),('plus','#b45c42',r'$r_+$')]:
    r=main[f'P6_sd_{branch}_main'];a=np.load(OUT/r['profile'])
    disp=np.max(abs(a['mesh_history']-a['s0'][None,:]),axis=1)
    axs[0].plot(a['history_times'],1000*disp,label=label,color=color)
axs[0].set_ylabel(r'$10^3\max_i|X_i(t)-X_i(0)|$')
axs[0].set_title('P6 SD: continuous node motion');axs[0].legend()
for route,color in [('fd','#267b73'),('sd','#b45c42')]:
    for suffix,style,label in [('fine_half','-',f'{route.upper()}, baseline'),('fine_seed','--',f'{route.upper()}, seeded')]:
        r=sup[f'P2_{route}_plus_{suffix}']
        ts=[x['t'] for x in r['traces']];es=[x['bands']['v']['high_band_nodal'] for x in r['traces']]
        axs[1].semilogy(ts,es,color=color,linestyle=style,label=label)
    for branch,style in [('minus','-'),('plus','--')]:
        r=sup[f'P10_{route}_{branch}_fine_half']
        axs[2].semilogy([x['t'] for x in r['traces']],[x['bands']['v']['high_band_nodal'] for x in r['traces']],
                        color=color,linestyle=style,label=route.upper()+', '+('$r_-$' if branch=='minus' else '$r_+$'))
axs[1].set_title(r'P2 $r_+$: $10^{-12}$ input perturbation')
axs[2].set_title('P10: growth before termination')
for ax in axs:
    ax.set_xlabel('Time');ax.grid(alpha=.2)
for ax in axs[1:]:
    ax.set_ylabel('High-band v error (computational grid)');ax.legend(fontsize=8)
fig.suptitle('Actual motion and fine-grid sensitivity; no filtering used in evolution',fontsize=12)
fig.tight_layout(rect=[0,0,1,.93]);fig.savefig(HERE/'motion_and_growth.png');fig.savefig(HERE/'motion_and_growth.pdf')
print('Saved two PNG/PDF figures')
