"""Plot measured two-soliton continuum and u/v error budgets."""
from pathlib import Path
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'out/two_error_budget.json').read_text(encoding='utf-8'))
scan=sorted((r for r in data['exact_model_scan'] if r['t']==.01),key=lambda r:r['h'])
fig,axes=plt.subplots(1,3,figsize=(12,3.6))
h=[r['h'] for r in scan]
for field,color in (('u','#175aa2'),('v','#c45029')):
    axes[0].loglog(h,[r[field]['inf'] for r in scan],'o-',label=field,color=color)
axes[0].loglog(h,[.06*z*z for z in h],':',color='gray',label='0.06 h²')
axes[0].set_title('Exact Gram → continuous Gram')
axes[0].set_ylabel('maximum model error')
axes[0].legend(fontsize=8)
runs={(r['h'],r['model']):r['observations'][-1] for r in data['finite_initial_runs'] if r['nx']==256}
hh=sorted({a for a,m in runs})
for ax,field in zip(axes[1:],('u','v')):
    def vals(model,kind):return [runs[(z,model)]['fields'][field][kind]['inf'] for z in hh]
    ax.loglog(hh,vals('structure','model'),'o-',color='gray',label='model, both')
    ax.loglog(hh,vals('structure','solver'),'o-',color='#175aa2',label='SD solver')
    ax.loglog(hh,vals('fd','solver'),'o--',color='#c45029',label='FD vs finite h')
    ax.loglog(hh,vals('structure','total'),'s-',color='black',label='SD total')
    ax.loglog(hh,vals('fd','total'),'s--',color='#a23830',label='FD total')
    ax.set_title(field+' error at t=0.01, nx=256')
    ax.set_ylabel('full-grid maximum norm')
    ax.legend(fontsize=7)
for ax in axes:
    ax.set_xlabel('h')
    ax.set_xticks([1/32,1/16,1/8,1/4])
    ax.set_xticklabels(['1/32','1/16','1/8','1/4'])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True,which='both',alpha=.25)
fig.tight_layout()
out=root/'figures/fig16_two_error_budget.png'
fig.savefig(out,dpi=180)
print(out)
