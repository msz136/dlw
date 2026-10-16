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
from matplotlib.lines import Line2D
fig,axs=plt.subplots(2,2,figsize=(9.2,6.8),layout='constrained')
for row,case in enumerate('AC'):
    d=profiles[case]
    for col,field in enumerate('uv'):
        ax=axs[row,col]
        ax.axhline(0,color='#333333',lw=.8,label='RK4 reference')
        for method,color in [('Euler','#D55E00'),('CN','#6A3D9A')]:
            difference=d[f'{method}_fixed_{field}']-d[f'RK4_fixed_{field}']
            ax.plot(d['x'],difference,color=color,lw=1.25,label=method.replace('CN','C–N')+' − RK4')
        ax.set_yscale('symlog',linthresh=1e-10,linscale=.45)
        ax.set_ylim(-2e-5,2e-5)
        ax.set_yticks([-1e-5,-1e-7,-1e-9,0,1e-9,1e-7,1e-5])
        ax.set_xlim(d['x'][[0,-1]])
        ax.set_ylabel(r'$\delta\mathcal{E}_{'+field+r'}(x)$')
        title=TITLES['ABCD'.index(case)].replace('\n',' ')
        ax.set_title(f'({chr(97+row*2+col)}) '+title+f': ${field}$',fontsize=12)
        ax.set_xlabel('$x$');ax.grid(alpha=.15)
handles,labels=axs[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False,handlelength=3)
save(fig,'PE_time_profiles')

fig,axs=plt.subplots(2,2,figsize=(9.2,6.5),layout='constrained')
for row,case in enumerate('AC'):
    d=profiles[case]
    for col,field in enumerate('uv'):
        ax=axs[row,col]
        for mesh,color,ls,lw in [('fixed','#D55E00',(0,(8,5)),1.5),('moving','#0072B2','-',1.8)]:
            ax.plot(d['x'],d[f'RK4_{mesh}_{field}'],color=color,ls=ls,lw=lw,label=mesh.title()+' mesh')
        ids=np.unique(np.linspace(0,len(d['x'])-1,15,dtype=int))[1:-1]
        ax.plot(d['x'][ids],d[f'RK4_fixed_{field}'][ids],ls='none',marker='o',ms=3.5,
                mfc='white',mec='#D55E00',mew=.9,zorder=5)
        ax.set_xlim(d['x'][[0,-1]]);ax.set_ylim(bottom=0)
        ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
        ax.set_ylabel(r'$\max_j |e_'+field+r'(x,y_j,T)|$')
        title=TITLES['ABCD'.index(case)].replace('\n',' ')
        ax.set_title(f'({chr(97+row*2+col)}) '+title+f': ${field}$',fontsize=12)
        ax.set_xlabel('$x$');ax.grid(alpha=.15)
handles,labels=axs[0,0].get_legend_handles_labels()
handles[0]=Line2D([],[],color='#D55E00',ls=(0,(8,5)),lw=1.5,marker='o',ms=3.5,mfc='white')
fig.legend(handles,labels,loc='outside upper center',ncol=2,frameon=False,handlelength=4)
save(fig,'PE_mesh_profiles')
