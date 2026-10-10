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
from matplotlib.ticker import ScalarFormatter, MaxNLocator
fig,axs=plt.subplots(4,2,figsize=(11,16))
fig.subplots_adjust(left=.09,right=.98,bottom=.045,top=.94,wspace=.24,hspace=.34)
styles=[('Euler','#D55E00','-',1.4),('RK4','#0072B2','-',2.1),('CN','#6A3D9A',(0,(7,5)),1.3)]
for row,case in enumerate('ABCD'):
 d=profiles[case]; x=d['x']
 for col,f in enumerate('uv'):
  ax=axs[row,col]; ref=d[f'RK4_fixed_{f}']; peak=x[ref.argmax()]
  half=.10 if case=='A' else .15 if case=='D' else .65
  mask=abs(x-peak)<=half
  ins=ax.inset_axes([.51,.59,.46,.35])
  curves=[]
  for method,color,ls,lw in styles:
   y=d[f'{method}_fixed_{f}']; curves.append(y)
   ax.plot(x,y,color=color,ls=ls,lw=lw,label=method.replace('CN','C–N'))
   ins.plot(x[mask],y[mask],color=color,ls=ls,lw=lw)
  ax.set_xlim(x[0],x[-1]); ax.set_ylim(0,max(y.max() for y in curves)*1.95)
  ymin=min(y[mask].min() for y in curves); ymax=max(y[mask].max() for y in curves); pad=(ymax-ymin)*.18
  ins.set_xlim(x[mask][0],x[mask][-1]); ins.set_ylim(ymin-pad,ymax+pad)
  ins.set_title('Near the error peak',fontsize=10,pad=4)
  for a in [ax,ins]:
   fmt=ScalarFormatter(useMathText=True); fmt.set_scientific(True); fmt.set_powerlimits((0,0)); fmt.set_useOffset(False); a.yaxis.set_major_formatter(fmt)
   a.grid(alpha=.13);a.yaxis.set_major_locator(MaxNLocator(4));a.xaxis.set_major_locator(MaxNLocator(3 if a==ins else 6))
  ins.tick_params(labelsize=9); ins.yaxis.get_offset_text().set_fontsize(9)
  ax.indicate_inset_zoom(ins,edgecolor='#777777',alpha=.5,lw=.7)
  ax.text(.035,.90,'C–N and RK4\nnearly coincide',transform=ax.transAxes,va='top',fontsize=10,color='#444444')
  ax.set_xlabel('$x$');ax.set_ylabel(r'$\max_j|'+f.upper()+r'_m-'+f.upper()+r'_*|$')
  name=TITLES['ABCD'.index(case)].replace('\n',' ')
  ax.set_title(f'({chr(97+row*2+col)}) {name}: ${f}$',fontsize=12,pad=12)
handles,labels=axs[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.985),ncol=3,frameon=False,handlelength=3.5)
save(fig,'PE_time_profiles')

fig,axs=plt.subplots(4,2,figsize=(11,14),layout='constrained')
for row,case in enumerate('ABCD'):
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
        ax.set_ylabel(r'$\max_j|'+field.upper()+r'_{\rm num}-'+field.upper()+r'_*|$')
        title=TITLES['ABCD'.index(case)].replace('\n',' ')
        ax.set_title(f'({chr(97+row*2+col)}) '+title+f': ${field}$',fontsize=12)
        ax.set_xlabel('$x$');ax.grid(alpha=.15)
handles,labels=axs[0,0].get_legend_handles_labels()
handles[0]=Line2D([],[],color='#D55E00',ls=(0,(8,5)),lw=1.5,marker='o',ms=3.5,mfc='white')
fig.legend(handles,labels,loc='outside upper center',ncol=2,frameon=False,handlelength=4)
save(fig,'PE_mesh_profiles')
