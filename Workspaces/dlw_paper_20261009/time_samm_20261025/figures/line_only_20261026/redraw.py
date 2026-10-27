"""Line-only manuscript figures. Overlap classification affects stroke style only."""
from pathlib import Path
import sys, importlib.util, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/(name+'.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
mesh=load('plot_mesh');time=load('plot_time_history')

def curves(ax,groups,log=False):
    # Compare screen-scale separation only to select solid/dashed strokes.
    transform=lambda y:np.log10(np.maximum(y,1e-300)) if log else y
    ys=np.concatenate([transform(g[1]) for g in groups]);span=ys.max()-ys.min()
    xmin=min(g[0].min() for g in groups);xspan=max(g[0].max() for g in groups)-xmin
    def smooth(v):
        v=np.clip(v,0,1);return v*v*(3-2*v)
    for k,(x,y,color,label) in enumerate(groups):
        # Subdivide the original polyline, retaining all native vertices.
        # Interpolation in log coordinates preserves the original log-axis geometry.
        xd=np.unique(np.r_[x,np.linspace(x[0],x[-1],2401)])
        yt=np.interp(xd,x,transform(y));distance=np.full(len(xd),np.inf)
        for q,(xx,yy,_,_) in enumerate(groups):
            if q==k:continue
            other=np.interp(xd,xx,transform(yy))
            distance=np.minimum(distance,np.where((xd>=xx[0])&(xd<=xx[-1]),abs(yt-other),np.inf))
        fill=smooth((distance/span-.004)/.018)
        mid=(xd[:-1]+xd[1:])/2
        # One fixed phase across the entire x domain: no dash restart at a split.
        phase=((mid-xmin)/(xspan*.060)*len(groups)-k)%len(groups)
        ink=smooth(phase/.10)*smooth((1-phase)/.10)
        alpha=(fill[:-1]+fill[1:])/2
        alpha=ink+(1-ink)*alpha
        yd=10**yt if log else yt
        points=np.column_stack([xd,yd]);segments=np.stack([points[:-1],points[1:]],axis=1)
        rgba=np.tile(to_rgba(color),(len(segments),1));rgba[:,3]=alpha
        lc=LineCollection(segments,colors=rgba,linewidths=1.25,capstyle='round',zorder=3)
        ax.add_collection(lc);ax.update_datalim(points);ax.autoscale_view()
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
(HERE/'validation.json').write_text(json.dumps({'markers':False,'data_offsets':False,'transition':'smooth gap opacity over 0.4%-2.2% ordinate separation; global x dash phase','interpolation':'subdivision of original polyline only; no curve smoothing; native vertices retained','outputs':['mesh_profile_A','mesh_profile_D','time_error_u','time_error_v']},indent=2))
