"""Render the measured N=2 Gram-background defect refinement."""
from pathlib import Path
import json
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'out/multisoliton_study.json').read_text(encoding='utf-8'))
fig,axes=plt.subplots(1,2,figsize=(9,3.5),sharex=True)
for h,style in ((.25,'-'),(.125,'--')):
    for model,color in (('structure','#175aa2'),('fd','#c45029')):
        rows=sorted((r for r in data['defect_refinement'] if r['h']==h and r['model']==model),key=lambda r:r['nx'])
        for ax,field in zip(axes,('u','v')):
            ax.loglog([r['nx'] for r in rows],[r[field+'_inf'] for r in rows],
                      marker='o',linestyle=style,color=color,label=f'{model}, h={h:g}')
for ax,field in zip(axes,('u','v')):
    ax.set_title(f'{field}: exact two-soliton tangent defect')
    ax.set_xlabel('x grid points')
    ax.grid(True,which='both',alpha=.25)
axes[0].set_ylabel('full-grid maximum norm')
axes[1].legend(fontsize=8)
fig.tight_layout()
out=root/'figures/fig15_multisoliton_defect.png'
fig.savefig(out,dpi=180)
print(out)
