"""Line-only manuscript figures. Overlap classification affects stroke style only."""
from pathlib import Path
import sys, importlib.util, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/(name+'.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
mesh=load('plot_mesh');time=load('plot_time_history')

def curves(ax,groups,log=False):
    # Compare screen-scale separation only to select solid/dashed strokes.
    transform=lambda y:np.log10(np.maximum(y,1e-300)) if log else y
    ys=np.concatenate([transform(g[1]) for g in groups]);tol=.008*(ys.max()-ys.min())
    for k,(x,y,color,label) in enumerate(groups):
        near=np.zeros(len(x),bool)
        for q,(xx,yy,_,_) in enumerate(groups):
            if q==k:continue
            other=np.interp(x,xx,transform(yy))
            near|=(x>=xx[0])&(x<=xx[-1])&(abs(transform(y)-other)<tol)
        # Segment classification leaves every original line segment in place.
        flags=near[:-1]&near[1:]
        bounds=np.r_[0,np.flatnonzero(flags[1:]!=flags[:-1])+1,len(flags)]
        for a,b in zip(bounds[:-1],bounds[1:]):
            ax.plot(x[a:b+1],y[a:b+1],color=color,lw=1.25,
                ls=((4*k,(4,4*(len(groups)-1))) if flags[a] else '-'),zorder=3,
                solid_capstyle='butt',dash_capstyle='butt')
    return [Line2D([0],[0],color=c,lw=1.25,label=l) for _,_,c,l in groups]

def mesh_fig(case):
    model=mesh.Model(case,'Centered-SD',.1,.1);r=mesh.HALF_WIDTHS[case]
    fig,axes=plt.subplots(1,2,figsize=(7,2.75))
    for ax,field in zip(axes,['u','v']):
        groups=[]; yy=model.y if field=='u' else (model.y[1:]+model.y[:-1])/2
        for mode,color,label in [('uniform',mesh.ORANGE,'Uniform mesh'),('moving',mesh.BLUE,'Adaptive mesh')]:
            d=np.load(mesh.SRC/f'{case}_{mode}_0.0001.npz');x=d['x']
            exact=model.profile(yy,.01,x)[0 if field=='u' else 1]
            profile=abs(d[field]-exact)[abs(yy)<r].max(axis=0);sel=abs(x)<=r
            groups.append((x[sel],profile[sel],color,label))
        handles=curves(ax,groups);mesh.axes_style(ax)
        ax.set_xlim(-r,r);ax.set_xlabel('$x$');ax.set_title('(a) $u$' if field=='u' else '(b) $v$')
        if field=='u':ax.set_ylabel(rf'max$_{{|y|<{r:g}}}|u_h-u^*|$');ax.legend(handles=handles,loc='upper right',fontsize=8)
    fig.subplots_adjust(left=.115,right=.985,bottom=.185,top=.905,wspace=.24)
    for ext in ['png','pdf']:fig.savefig(BASE/f'mesh_profile_{case}.{ext}',dpi=300,bbox_inches='tight',pad_inches=.05)
    plt.close(fig)

def time_fig(field):
    fig,axes=plt.subplots(2,2,figsize=(7,4.75),sharex=True)
    for k,(ax,case) in enumerate(zip(axes.ravel(),time.CASES)):
        d=np.load(time.SRC/f'{case}_time.npz');t=d['t'][1:];groups=[]
        for key,label,color,*_ in time.METHODS:groups.append((t,d['errors_'+key][1:,0 if field=='u' else 1],color,label))
        handles=curves(ax,groups,True)
        vals=np.concatenate([g[1] for g in groups]);time.style(ax,vals.min()/1.7,vals.max()*1.9)
        ax.set_title(f'({chr(97+k)}) {time.TITLES[case]}',pad=6)
    for ax in axes[:,0]:ax.set_ylabel(rf'$E_{field}(t)$')
    for ax in axes[1,:]:ax.set_xlabel('$t$')
    fig.legend(handles=handles,loc='upper center',ncol=3,bbox_to_anchor=(.5,1.005),frameon=False)
    fig.subplots_adjust(left=.095,right=.985,bottom=.105,top=.865,hspace=.40,wspace=.245)
    for ext in ['png','pdf']:fig.savefig(BASE/f'time_error_{field}.{ext}',dpi=300,bbox_inches='tight',pad_inches=.05)
    plt.close(fig)
for c in ['A','D']:mesh_fig(c)
for f in ['u','v']:time_fig(f)
(HERE/'validation.json').write_text(json.dumps({'markers':False,'data_offsets':False,'overlap_threshold':'0.8% of transformed ordinate range','interpolation':'stroke classification only; plotted coordinates unchanged','outputs':['mesh_profile_A','mesh_profile_D','time_error_u','time_error_v']},indent=2))
