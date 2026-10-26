"""Preview only: analytic fields and freshly integrated case A. Does not edit the manuscript."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent
ROOT=PROJECT.parents[1]
sys.path.insert(0,str(PROJECT))
from plot_exact_solutions import exact,CASES
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7})
def save(fig,name):
    fig.savefig(HERE/(name+'.png'),dpi=220)
    fig.savefig(HERE/(name+'.svg'))
    plt.close(fig)
records=[]
for code,(key,(p,q,xlim,ylim,title)) in zip('ABCD',CASES.items()):
    x=np.linspace(*xlim,1001); y=np.linspace(*ylim,601); X,Y=np.meshgrid(x,y)
    fields=exact(p,q,X,Y,0)
    fig,axs=plt.subplots(2,2,figsize=(11,7.2),layout='constrained',width_ratios=[1,1.1])
    for row,f in enumerate('uv'):
        z=fields[row]
        line=exact(p,q,x[None,:],np.zeros((1,len(x))),0)[row][0]
        assert np.allclose(z[len(y)//2],line,atol=1e-12)
        ax=axs[row,0]; ax.plot(x,line,color='#0072B2',lw=1.8)
        ax.set(xlabel='$x$',ylabel=f'${f}_*$',title=f'({chr(97+2*row)}) Exact section: $y=0$, $t=0$',xlim=xlim);ax.grid(alpha=.16)
        ax=axs[row,1]; im=ax.pcolormesh(x,y,z,cmap='viridis',shading='auto',rasterized=True)
        ax.axhline(0,color='white',ls='--',lw=1.1)
        ax.set(xlabel='$x$',ylabel='$y$',title=f'({chr(98+2*row)}) ${f}_*(x,y,0)$',xlim=xlim,ylim=ylim)
        fig.colorbar(im,ax=ax,label=f'${f}_*$')
    fig.suptitle(title+'\nContinuous exact solution; no time integration',fontsize=15)
    save(fig,f'{code}_exact_heatmap_section')
    records.append({'case':code,'type':'continuous exact','t':0,'xlim':xlim,'ylim':ylim})
    print('Exact',code,flush=True)
# Reuse notebook definitions without running its experiments or changing its cells.
nbpath=ROOT/'notebook/DLW数值分析report.ipynb'
nb=json.loads(nbpath.read_text(encoding='utf8')); cells={c.get('id'):''.join(c['source']) for c in nb['cells']}
ns={}
for key in ('imports','config','reference','spatial','sd_fd','sd','sd2_lift','sd2_evolution','fd','mesh','time'):
    exec(cells['dlw-'+key].replace('from IPython.display import display','display=lambda *args,**kwargs:None'),ns)
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':12})
data={};stats=[]
for method,model in [('PE','SD'),('PF','SD2'),('FD','FD')]:
    file=HERE/f'A_{method}.npz'
    if not file.exists():
        print('Integrating',method,flush=True)
        r=ns['solve']('A',model,'RK4','fixed');assert r['completed'],r['reason']
        np.savez_compressed(file,x=r['x'],y=r['y'],u=r['fields'][0],v=r['fields'][1],exact_u=r['exact'][0],exact_v=r['exact'][1])
    data[method]=dict(np.load(file))
    d=data[method];assert all(np.isfinite(v).all() for v in d.values())
    stats.append({'method':method,'max_error':{f:float(abs(d[f]-d['exact_'+f]).max()) for f in 'uv'},'nearest_y':float(d['y'][np.argmin(abs(d['y']))])})
x,y=data['PE']['x'],data['PE']['y']
fig,axs=plt.subplots(2,3,figsize=(12,7),layout='constrained')
for row,f in enumerate('uv'):
    high=max(abs(d[f]-d['exact_'+f]).max() for d in data.values())
    for col,(method,d) in enumerate(data.items()):
        assert np.array_equal(x,d['x']) and np.array_equal(y,d['y'])
        im=axs[row,col].pcolormesh(x,y,abs(d[f]-d['exact_'+f]),vmin=0,vmax=high,cmap='magma',shading='auto',rasterized=True)
        axs[row,col].axhline(0,color='cyan',ls='--',lw=.8)
        axs[row,col].set(xlabel='$x$',ylabel='$y$',title=f'{method}: $|{f}-{f}_*|$')
    cb=fig.colorbar(im,ax=axs[row,:],shrink=.85);cb.formatter.set_powerlimits((0,0));cb.update_ticks()
fig.suptitle('A: one soliton (1,2) | RK4, fixed mesh, $T=0.01$\nShared linear color scale within each field',fontsize=15)
save(fig,'A_error_heatmaps')
fig,axs=plt.subplots(2,2,figsize=(11,7),layout='constrained')
colors=['#0072B2','#D55E00','#009E73'];styles=['-','--',':']
ref=ns['Exact']('A',.1,2).uv(np.array([-.5]),x,.01)
for row,f in enumerate('uv'):
    axs[row,0].plot(x,ref[row][0],color='black',lw=1.7,label='Exact')
    for (method,d),color,ls in zip(data.items(),colors,styles):
        section=CubicSpline(y,d[f],axis=0)(0.)
        err=abs(section-ref[row][0])
        axs[row,0].plot(x,section,color=color,ls=ls,lw=1.2,label=method)
        axs[row,1].plot(x,err,color=color,ls=ls,lw=1.6,label=method)
        bias=float(abs(CubicSpline(y,d['exact_'+f],axis=0)(0.)-ref[row][0]).max())
        stats.append({'method':method,'field':f,'section_max_error':float(err.max()),'exact_interpolation_control':bias})
    for col in range(2):
        axs[row,col].set(xlabel='$x$',ylabel=f'${f}$' if col==0 else f'$|{f}-{f}_*|$',xlim=(-5,5),title=('Wave profile' if col==0 else 'Absolute error')+f': ${f}(x,0,T)$');axs[row,col].grid(alpha=.16)
    axs[row,1].ticklabel_format(axis='y',style='sci',scilimits=(0,0),useMathText=True)
axs[0,0].legend(frameon=False);axs[0,1].legend(frameon=False)
fig.suptitle('A: $y=0$ sections at $T=0.01$\nCubic reconstruction in $y$; exact reference evaluated at $y=0$',fontsize=15)
save(fig,'A_numerical_y0_sections')
(HERE/'validation.json').write_text(json.dumps({'analytic':records,'numerical':stats,'config':ns['case_config']('A'),'notebook_sha256':hashlib.sha256(nbpath.read_bytes()).hexdigest(),'section_rule':'CubicSpline of numerical field in y evaluated at zero; subtract analytic y=0 reference. Not max over y.'},indent=2),encoding='utf8')
print('DONE',flush=True)
