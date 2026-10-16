"""Replot saved final-state error envelopes without running a PDE solver."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
FIG=HERE/'figures'
profiles={case:dict(np.load(HERE/'results_revision'/f'{case}_profiles.npz')) for case in 'ABCD'}
TITLES=['One-soliton\n$(1,2)$','One-soliton\n$(4,-3)$','Two-soliton\n$(6,-5;\\,4,-3)$','Two-soliton\n$(1,2;\\,4,-3)$']
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
 'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7,'savefig.facecolor':'white'})
def save(fig,stem):
    fig.savefig(FIG/(stem+'.png'),dpi=300,bbox_inches='tight')
    fig.savefig(FIG/(stem+'.pdf'),bbox_inches='tight')
    plt.close(fig)
    (FIG/(stem+'.py')).write_text("from pathlib import Path\nimport runpy\nrunpy.run_path(str(Path(__file__).resolve().parents[1]/'plot_result_profiles.py'),run_name='__main__')\n",encoding='utf8')

# Same method colors and aligned small multiples, inspired by gallery
# oa-bio-plos-pcbi-1007396-f04; no decorative icons or aggregate score inset.
fig,axs=plt.subplots(2,4,figsize=(12,6.1),layout='constrained')
for col,case in enumerate('ABCD'):
    d=profiles[case]
    for row,field in enumerate('uv'):
        ax=axs[row,col]
        for method,color,ls in [('Euler','#d47b19','-'),('RK4','#1776bc','-'),('CN','#282828','--')]:
            ax.plot(d['x'],d[f'{method}_fixed_{field}'],color=color,ls=ls,lw=1.25,label=method.replace('CN','C–N'))
        ax.set_xlim(d['x'][[0,-1]]);ax.set_ylim(bottom=0)
        ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
        ax.set_ylabel(r'$\\max_j |e_'+field+r'(x,y_j,T)|$')
        ax.set_title(f'({chr(97+row*4+col)}) '+(TITLES[col] if row==0 else '$v$'))
        ax.set_xlabel('$x$');ax.grid(alpha=.15)
fig.legend(*axs[0,0].get_legend_handles_labels(),loc='outside upper center',ncol=3,frameon=False)
save(fig,'PE_time_profiles')

fig,axs=plt.subplots(3,4,figsize=(12,8.5),layout='constrained')
for col,case in enumerate('ABCD'):
    d=profiles[case];ax=axs[0,col]
    ax.axhline(.1,color='#777777',ls='--',lw=1.2,label='Fixed mesh')
    ax.plot(d['mesh_x'],d['mesh_spacing'],color='#1776bc',lw=1.4,label='Moving mesh')
    ax.set_ylabel(r'$x_{i+1}-x_i$');ax.set_title(f'({chr(97+col)}) '+TITLES[col]);ax.set_xlim(d['x'][[0,-1]])
    for row,field in enumerate('uv',1):
        ax=axs[row,col]
        for mesh,color,ls in [('fixed','#777777','--'),('moving','#1776bc','-')]:
            ax.plot(d['x'],d[f'RK4_{mesh}_{field}'],color=color,ls=ls,lw=1.3)
        ax.set_xlim(d['x'][[0,-1]]);ax.set_ylim(bottom=0)
        ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
        ax.set_ylabel(r'$\\max_j |e_'+field+r'(x,y_j,T)|$');ax.set_title(f'({chr(97+row*4+col)}) ${field}$')
    for ax in axs[:,col]:ax.set_xlabel('$x$');ax.grid(alpha=.15)
fig.legend(*axs[0,0].get_legend_handles_labels(),loc='outside upper center',ncol=2,frameon=False)
save(fig,'PE_mesh_profiles')
