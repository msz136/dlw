"""Exact physical fields at t=0; ESD slice/heatmap arrangement."""
from pathlib import Path
import sys,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from figure_data import CASES,exact_fields,display_limits
HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
    'axes.titlesize':11,'axes.labelsize':11,'xtick.labelsize':10,'ytick.labelsize':10,
    'axes.linewidth':.7,'lines.linewidth':1.5,'pdf.fonttype':42,'savefig.facecolor':'white'})
TITLES={'A':'A: one soliton (1, 2)','B':'B: one soliton (4, -3)',
    'C':'C: two solitons (6, -5), (4, -3)','D':'D: two solitons (1, 2), (4, -3)',
    'Gaussian':'Periodic Gaussian initial data','Sinusoidal':'Sinusoidal initial data'}
def main(case):
    xlim,ylim=display_limits(case)
    if case in ('Gaussian','Sinusoidal'):ylim=(-2.,2.)
    x=np.linspace(*xlim,801);y=np.linspace(*ylim,401)
    physical=exact_fields(case,x,y,0.)
    section=exact_fields(case,x,np.array([0.]),0.)
    fig,axs=plt.subplots(2,2,figsize=(10.4,6.4),layout='constrained',width_ratios=[1,1.15])
    details=[]
    for row,field in enumerate(('u','v')):
        line=section[row][0];z=physical[row]
        ax=axs[row,0];ax.plot(x,line,'k-',lw=1.5)
        ax.set(xlabel='$x$',ylabel='$'+field+'$',xlim=xlim,
               title=f'({chr(97+2*row)}) '+ '$'+field+'(x,0,0)$')
        if field=='v' and case in ('Gaussian','Sinusoidal'):
            ax.set_ylim(3.995,4.005);ax.ticklabel_format(useOffset=False)
            ax.text(.04,.9,'Central section: $v=4$',transform=ax.transAxes,fontsize=10)
        ax=axs[row,1];im=ax.pcolormesh(x,y,z,cmap='viridis',shading='auto',rasterized=True)
        ax.axhline(0,color='white',ls='--',lw=.8,alpha=.9)
        ax.set(xlabel='$x$',ylabel='$y$',xlim=xlim,ylim=ylim,
               title=f'({chr(98+2*row)}) '+'$'+field+'(x,y,0)$')
        cb=fig.colorbar(im,ax=ax,pad=.025,fraction=.046)
        cb.ax.tick_params(labelsize=9);cb.ax.yaxis.get_offset_text().set_fontsize(9)
        details.append(dict(field=field,minimum=float(z.min()),maximum=float(z.max()),
            central_range=[float(line.min()),float(line.max())],
            central_grid_difference=float(np.max(abs(z[len(y)//2]-line)))))
    fig.suptitle(TITLES[case],fontsize=13)
    stem=f'exact_{case}_initial'
    fig.savefig(HERE/(stem+'.png'),dpi=300)
    fig.savefig(HERE/(stem+'.pdf'),dpi=300)
    plt.close(fig)
    (HERE/(stem+'.py')).write_text("from plot_initial_profiles import main\nmain("+repr(case)+")\n",encoding='utf8')
    return dict(case=case,t=0,xlim=xlim,ylim=ylim,nx=len(x),ny=len(y),fields=details,
                png=stem+'.png',pdf=stem+'.pdf',source='Continuous exact fields; no numerical time stepping.')
if __name__=='__main__':
    cases=sys.argv[1:] or CASES
    out=[main(c) for c in cases]
    (HERE/'initial_profile_manifest.json').write_text(json.dumps(out,indent=2),encoding='utf8')
    print('Saved exact profile figures:',', '.join(cases))
