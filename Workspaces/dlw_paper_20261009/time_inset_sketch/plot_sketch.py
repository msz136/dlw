from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, MaxNLocator
HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7})
fig,axs=plt.subplots(2,2,figsize=(11,8.2))
fig.subplots_adjust(left=.09,right=.98,bottom=.08,top=.89,wspace=.24,hspace=.34)
styles=[('Euler','#D55E00','-',1.4),('RK4','#0072B2','-',2.1),('CN','#6A3D9A',(0,(7,5)),1.3)]
for row,case in enumerate('AC'):
 d=np.load(HERE.parent/'results_revision'/f'{case}_profiles.npz'); x=d['x']
 for col,f in enumerate('uv'):
  ax=axs[row,col]; ref=d[f'RK4_fixed_{f}']; peak=x[ref.argmax()]
  half=.10 if case=='A' else .65
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
  ax.set_xlabel('$x$');ax.set_ylabel(r'$\mathcal{E}_'+f+r'(x)=\max_j|e_'+f+r'(x,y_j,T)|$')
  name='One-soliton (1, 2)' if case=='A' else 'Two-soliton (6, −5; 4, −3)'
  ax.set_title(f'({chr(97+row*2+col)}) {name}: ${f}$',fontsize=12,pad=12)
handles,labels=axs[0,0].get_legend_handles_labels()
fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.985),ncol=3,frameon=False,handlelength=3.5)
fig.savefig(HERE/'PE_time_inset_sketch.png',dpi=180,facecolor='white')

