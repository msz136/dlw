"""User layout: columns PE/PF/FD; rows u surface, u contours, v surface, v contours.
Existing jet palette and viewing angle retained; common scales across methods.
"""
from pathlib import Path
import json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator,ScalarFormatter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
    'axes.linewidth':.65,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
stats=[]
for case in (sys.argv[1] if len(sys.argv)>1 else 'ABC'):
    datasets={m:np.load(ROOT/f'Workspaces/dlw_precision_surface_20261008/case_{case}.npz' if m=='PF' else HERE/f'comparison_fields/{case}_{m}.npz') for m in ['PE','PF','FD']}
    d=datasets['PF'];xlim=(-3,4) if case=='A' else (-30,30);ylim=(-3,3) if case=='A' else (-30,30)
    xm=(d['x']>=xlim[0])&(d['x']<=xlim[1]);ym=(d['y']>=ylim[0])&(d['y']<=ylim[1])
    x,y=d['x'][xm],d['y'][ym];X,Y=np.meshgrid(x,y)
    for error in ([sys.argv[2]=='errors'] if len(sys.argv)>2 else [False,True]):
        fig=plt.figure(figsize=(11.6,14.8),layout='constrained')
        gs=fig.add_gridspec(4,5,width_ratios=[1,1,1,.15,.045],height_ratios=[1,1,1,1])
        for fidx,field in enumerate(['u','v']):
            zz=[(abs(datasets[m][field]-datasets[m]['exact_'+field]) if error else datasets[m][field])[np.ix_(ym,xm)] for m in ['PE','PF','FD']]
            low=0 if error else min(float(z.min()) for z in zz);high=max(float(z.max()) for z in zz)
            norm=Normalize(low,high);levels=np.linspace(low,high,13)[1:-1]
            for col,(m,z) in enumerate(zip(['PE','PF','FD'],zz)):
                label=rf'e_{{{field}}}' if error else field
                ax=fig.add_subplot(gs[2*fidx,col],projection='3d')
                sy=max(1,len(y)//100);sx=max(1,len(x)//160)
                ax.plot_surface(X[::sy,::sx],Y[::sy,::sx],z[::sy,::sx],cmap='jet',norm=norm,
                    rcount=len(y[::sy]),ccount=len(x[::sx]),linewidth=0,antialiased=False,shade=False,rasterized=True)
                ax.set(xlabel='$x$',ylabel='$y$',zlabel=f'${label}$',xlim=xlim,ylim=ylim,zlim=(low,high))
                ax.view_init(28,-62);ax.set_box_aspect((1.15,1,.85))
                ax.set_title(f'({chr(97+6*fidx+col)}) {m}: ${label}$',pad=7)
                for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:axis.set_major_locator(MaxNLocator(3))
                ax.tick_params(labelsize=9,pad=1)
                if error:ax.ticklabel_format(axis='z',style='sci',scilimits=(0,0),useMathText=True)
                ax=fig.add_subplot(gs[2*fidx+1,col])
                ax.contour(x,y,z,levels=levels,cmap='jet',norm=norm,linewidths=.85)
                ax.set(xlabel='$x$',ylabel='$y$',xlim=xlim,ylim=ylim)
                ax.set_title(f'({chr(100+6*fidx+col)}) {m}: ${label}$ contours')
                ax.set_box_aspect(1);ax.grid(color='#dddddd',linewidth=.4,alpha=.45)
                ax.xaxis.set_major_locator(MaxNLocator(4));ax.yaxis.set_major_locator(MaxNLocator(4))
                stats.append(dict(case=case,kind='error' if error else 'field',method=m,field=field,min=float(z.min()),max=float(z.max())))
            for row in [2*fidx,2*fidx+1]:
                cb=fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap='jet'),cax=fig.add_subplot(gs[row,4]))
                if error:cb.formatter=ScalarFormatter(useMathText=True);cb.formatter.set_powerlimits((0,0));cb.update_ticks()
                cb.set_label(f'${label}$')
        name={'A':'One-soliton A','B':'One-soliton B','C':'Two-soliton'}[case]
        fig.suptitle(name+(' | Absolute errors' if error else ' | Numerical fields')+'\nRK4, fixed mesh, $T=0.01$',fontsize=15)
        stem=f'{case}_'+('errors' if error else 'fields')
        fig.savefig(OUT/(stem+'.png'),dpi=300)
        fig.savefig(OUT/(stem+'.pdf'),dpi=180)
        (OUT/(stem+'.py')).write_text("from pathlib import Path\nimport runpy,sys\nsys.argv=['plot_comparison_fields.py','"+case+"','"+('errors' if error else 'fields')+"']\nrunpy.run_path(str(Path(__file__).resolve().parents[1]/'plot_comparison_fields.py'),run_name='__main__')\n",encoding='utf-8')
        plt.close(fig);print('Rendered '+stem,flush=True)
(OUT/('plot_validation.json' if len(sys.argv)==1 else 'plot_validation_'+sys.argv[1]+'_'+sys.argv[2]+'.json')).write_text(json.dumps(dict(rows=['u_surface','u_contours','v_surface','v_contours'],columns=['PE','PF','FD'],common_scales=True,stats=stats),indent=2),encoding='utf-8')
