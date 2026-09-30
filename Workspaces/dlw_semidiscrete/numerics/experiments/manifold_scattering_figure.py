"""Plot measured route-3 manifold defects and independently restarted bursts."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'out/manifold_scattering.json').read_text(encoding='utf-8'))
colors={'structure':'#176895','fd':'#c45329'}
labels={'structure':'SD','fd':'FD'}
fig,axs=plt.subplots(1,3,figsize=(12.8,3.7),constrained_layout=True)
for model in colors:
    rows=sorted((r for r in d['n2'] if r['h']==.25 and r['nx']==256 and r['model']==model),key=lambda r:r['t'])
    xx=[r['t'] for r in rows]
    axs[0].semilogy(xx,[r['defect']['normal_weighted_l2'] for r in rows],'-o',color=colors[model],label=labels[model])
    axs[1].plot(xx,[r['defect']['normal_fraction'] for r in rows],'-o',color=colors[model],label=labels[model])
    bursts=[r for r in rows if 'burst' in r]
    axs[2].semilogy([r['t'] for r in bursts],[r['burst']['u_inf'] for r in bursts],'-o',color=colors[model],label=labels[model]+' u')
    axs[2].semilogy([r['t'] for r in bursts],[r['burst']['v_inf'] for r in bursts],'--s',color=colors[model],label=labels[model]+' v')
axs[0].set(title='Normal component of instantaneous defect',xlabel='restart time',ylabel='weighted L2')
axs[1].set(title='Normal / total defect',xlabel='restart time',ylabel='fraction',ylim=(.995,1.0001))
axs[2].set(title='Independent 0.005-time bursts',xlabel='restart time',ylabel='full-domain maximum error')
for a in axs:
    a.grid(alpha=.25)
    a.legend(frameon=False,fontsize=8)
out=ROOT/'figures/fig17_manifold_scattering.png'
fig.savefig(out,dpi=180)
print(out)
