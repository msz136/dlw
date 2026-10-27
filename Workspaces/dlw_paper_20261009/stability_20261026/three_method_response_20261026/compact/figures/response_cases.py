"""Actual native-node histories; staggered dash phases and markers, no data offsets."""
from pathlib import Path
import json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, ScalarFormatter

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'native'
METHODS=['Endpoint-SD','Centered-SD','FD']
COLORS=['#2878B5','#E07A23','#299568']
MARKERS=['o','s','^']
plt.rcParams.update({'font.family':'DejaVu Serif','mathtext.fontset':'dejavuserif','font.size':9,
 'axes.labelsize':9,'axes.titlesize':9,'xtick.labelsize':8,'ytick.labelsize':8,
 'axes.linewidth':.65,'pdf.fonttype':42,'savefig.facecolor':'white'})

def draw(case):
    d=np.load(SOURCE/(case+'.npz')); t=d['t']; y=d['response_normalized']
    assert y.shape==(len(t),3,2,2) and np.isfinite(y).all()
    fig,axs=plt.subplots(2,2,figsize=(7.1,4.4))
    fig.subplots_adjust(left=.10,right=.98,bottom=.11,top=.85,hspace=.55,wspace=.33)
    handles=[Line2D([0],[0],color=c,lw=1.5,linestyle=(0,(4,8)),
                       markersize=4,label=n) for n,c,m in zip(METHODS,COLORS,MARKERS)]
    fig.legend(handles=handles,loc='upper center',bbox_to_anchor=(.53,.99),ncol=3,
               frameon=False,handlelength=3.0,columnspacing=2)
    for i in range(2):
        for j in range(2):
            ax=axs[i,j]
            for k in range(3):
                line,=ax.plot(t,y[:,k,i,j],color=COLORS[k],lw=1.5,
                    linestyle=(4*k,(4,8)),
                    zorder=3)
                assert np.array_equal(line.get_ydata(),y[:,k,i,j])
            lo,hi=y[:,:,i,j].min(),y[:,:,i,j].max()
            pad=max((hi-lo)*.12,.0003)
            ax.set_ylim(max(0,lo-pad),hi+pad)
            ax.set_xlim(0,.01);ax.set_xticks([0,.005,.01]);ax.set_xticklabels(['0','0.005','0.01'])
            ax.yaxis.set_major_locator(MaxNLocator(4));fmt=ScalarFormatter(useMathText=True);fmt.set_useOffset(False)
            ax.yaxis.set_major_formatter(fmt)
            ax.set_xlabel('$t$',labelpad=2)
            ax.set_ylabel(r'$\|\delta '+['u','v'][j]+r'_h\|_\infty/\varepsilon$',labelpad=5)
            ax.set_title('('+chr(97+2*i+j)+') '+['$u_0$ perturbed','$v_0$ perturbed'][i]+r': $'+['u','v'][j]+'$ response',loc='left',pad=6)
            ax.spines[['right','top']].set_visible(False)
            ax.tick_params(direction='out',width=.6,length=3)
    for ext in ['png','pdf']:fig.savefig(HERE/f'response_{case}.{ext}',dpi=300,bbox_inches='tight',pad_inches=.06)
    plt.close(fig)
    return hashlib.sha256((SOURCE/(case+'.npz')).read_bytes()).hexdigest()

if __name__=='__main__':
    hashes={c:draw(c) for c in ['A','D','Gaussian','Sinusoidal']}
    (HERE/'validation.json').write_text(json.dumps({'source_hashes':hashes,'all_plotted_values_match_source':True,
       'data_offset':False,'interpolation':False,'smoothing':False,'markers':False,
       'dash_phases':'equal width and duty cycle, shifted phase'},indent=2))
