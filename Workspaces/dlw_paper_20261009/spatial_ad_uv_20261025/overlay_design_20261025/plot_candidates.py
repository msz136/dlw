"""Real-data drafts for clearer three-method overlays; does not publish the paper.

Design sources: current DLW overlays (paired u/v, method colors), gallery
oa-geo-tc-20-5365-2026-f10 (distinct continuous/line-style profiles), and
oa-geo-tc-20-5365-2026-f02 (large spatial view + compact quantitative view).
There is no directly matching 3D-overlay example in the gallery.

Lines use every stored x sample and nearest native y to seven target levels.
Faint surfaces retain every x sample and up to 61 y rows plus extrema rows.
No smoothing, offsets or per-method amplitude normalization are applied.
The common display floor is 1e-4 of the largest error of each component.
Below-floor surface patches are omitted; logarithmic line segments are also
omitted below that floor. Linear line values are unchanged.
"""
from pathlib import Path
import sys, json, math, hashlib, argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator,LogLocator,NullFormatter

HERE=Path(__file__).resolve().parent;PROJECT=HERE.parent
DATA=PROJECT.parent/'report_refresh_20261024/natural_selection_20261025/figures/data'
OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
METHODS=[('endpoint','Endpoint-SD','#356EAE','-'),('centered','Centered-SD','#DA7B21','--'),('fd','FD','#16866A','-.')]
WINDOWS={'D':(-30,30),'Gaussian':(-18,18),'A':(-5,5),'Sinusoidal':(-12,12)}
NAMES={'D':'Two-soliton','Gaussian':'Gaussian','A':'One-soliton','Sinusoidal':'Sinusoidal'}
TITLES={'light':'B  Light surfaces + sparse profiles','profiles':'C  Sparse profiles only','log':'D  Common logarithmic height','summary':'E  Linear 3D + transverse maxima','zoom':'F  Full height + low-height detail'}
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
    'axes.linewidth':.65,'savefig.facecolor':'white','figure.facecolor':'white','path.simplify':False})

def load(case):
    path=DATA/(case+'.npz');d=np.load(path);mask=(d['x']>=WINDOWS[case][0])&(d['x']<=WINDOWS[case][1]);x=d['x'][mask]
    rows={q:[dict(prefix=p,name=n,color=c,ls=ls,x=x,y=d[p+'_y_'+q],z=np.abs(d[p+'_error_final_'+q][:,mask])) for p,n,c,ls in METHODS] for q in ['u','v']}
    return rows,dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def format_axes(ax,case,ys,limits,log=False):
    ax.set_proj_type('ortho');ax.view_init(33,-57)
    ax.set_box_aspect((1.25,1,.72))
    ax.set(xlim=WINDOWS[case],ylim=ys,zlim=limits,xlabel='$x$',ylabel='$y$')
    ax.xaxis.labelpad=1;ax.yaxis.labelpad=1
    for a in [ax.xaxis,ax.yaxis,ax.zaxis]:
        a.pane.set_visible(False);a._axinfo['grid']['color']=(.8,.83,.86,.45);a._axinfo['grid']['linewidth']=.4
    ax.xaxis.set_major_locator(MaxNLocator(4,prune='both'))
    ax.yaxis.set_major_locator(MaxNLocator(4,prune='both'))
    if not log:ax.zaxis.set_major_locator(MaxNLocator(3))
    ax.tick_params(labelsize=10,pad=1)

def draw_component(ax,case,q,parts,mode,cap=None):
    maxval=max(float(r['z'].max()) for r in parts);floor=maxval*1e-4
    display_max=cap if cap is not None else maxval
    exponent=math.floor(math.log10(display_max));scale=10.**exponent
    log=mode=='log';ys=(min(float(r['y'].min()) for r in parts),max(float(r['y'].max()) for r in parts))
    loglim=(math.log10(floor),math.log10(maxval)+.05)
    limits=loglim if log else (0,display_max/scale*1.06)
    format_axes(ax,case,ys,limits,log)
    if log:
        ticks=np.arange(math.ceil(loglim[0]),math.floor(loglim[1])+1)
        ax.set_zticks(ticks);ax.set_zticklabels(['$10^{'+str(int(t))+'}$' for t in ticks])
    title='$|'+q+r'_h-'+q+r'^*|$'+('  (log scale)' if log else '  ($10^{'+str(exponent)+'}$)')
    if cap is not None:title+='  [height zoom]'
    ax.set_title(title,pad=3,fontsize=13)
    targets=np.linspace(ys[0]+.08*(ys[1]-ys[0]),ys[1]-.08*(ys[1]-ys[0]),7)
    records=[]
    # Each method is represented by one-direction curves, never crossing meshes.
    for mi,r in enumerate(parts):
        z=r['z'];y=r['y'];x=r['x'];peak=np.unravel_index(z.argmax(),z.shape)
        iy=np.unique(np.r_[np.linspace(0,len(y)-1,min(61,len(y))).round().astype(int),peak[0]])
        line_indices=np.unique([np.argmin(abs(y-t)) for t in targets])
        if mode=='light':
            X,Y=np.meshgrid(x,y[iy]);Z=z[iy,:]
            visible=np.where(Z>=floor,Z,np.nan)
            height=np.log10(visible) if log else visible/scale
            ax.plot_surface(X,Y,height,color=r['color'],alpha=.045,
                rstride=1,cstride=1,linewidth=0,edgecolor='none',antialiased=True,shade=False,rasterized=True)
        for j in line_indices:
            line=z[j,:]
            vals=np.where(line>=floor,np.log10(np.maximum(line,np.finfo(float).tiny)),np.nan) if log else line/scale
            if cap is not None:vals=np.where(line<=cap*1.06,vals,np.nan)
            ax.plot(x,np.full_like(x,y[j]),vals,color=r['color'],ls=r['ls'],lw=1.05,alpha=.92)
        records.append(dict(method=r['name'],field=q,maximum=float(z.max()),minimum=float(z.min()),
            display_floor=floor,all_native_x_used=True,surface_native_y_indices=iy.tolist(),line_native_y_indices=line_indices.tolist(),
            line_native_y_values=y[line_indices].tolist(),common_scale=scale,log_height=log,source_shape=list(z.shape),height_zoom_cap=cap))
    return records

def draw(case,mode):
    rows,source=load(case);summary=mode=='summary';zoom=mode=='zoom'
    fig=plt.figure(figsize=(11.6,9.3 if zoom else 7.4 if summary else 5.6))
    grid=fig.add_gridspec(2 if summary or zoom else 1,2,left=.07 if summary else .02,right=.95,bottom=.08 if summary else .035,top=.86 if zoom else .82,
        wspace=.18 if summary else .10,hspace=.08 if zoom else .12,height_ratios=[1,1] if zoom else [3.0,1] if summary else [1])
    records=[]
    for qi,q in enumerate(['u','v']):
        ax=fig.add_subplot(grid[0,qi],projection='3d')
        records+=draw_component(ax,case,q,rows[q],mode)
        if summary:
            flat=fig.add_subplot(grid[1,qi])
            for r in rows[q]:
                env=r['z'].max(axis=0)
                flat.plot(r['x'],env,color=r['color'],ls=r['ls'],lw=1.4)
                records.append(dict(method=r['name'],field=q,summary='maximum over all native y at each x',global_maximum=float(env.max())))
            maxval=max(float(r['z'].max()) for r in rows[q]);flat.set_yscale('log');flat.set_ylim(maxval*1e-4,maxval*2)
            flat.set_xlim(WINDOWS[case]);flat.set_xlabel('$x$',labelpad=2)
            flat.set_ylabel(r'$\max_y |'+q+r'_h-'+q+r'^*|$',labelpad=4)
            flat.yaxis.set_major_locator(LogLocator(base=10,numticks=4));flat.yaxis.set_minor_formatter(NullFormatter())
            flat.tick_params(labelsize=10,length=3);flat.spines[['top','right']].set_visible(False)
            flat.grid(axis='y',lw=.4,color='.86');flat.xaxis.set_major_locator(MaxNLocator(5))
        if zoom:
            detail=fig.add_subplot(grid[1,qi],projection='3d')
            cap=sorted(float(r['z'].max()) for r in rows[q])[1]*1.08
            records+=draw_component(detail,case,q,rows[q],'profiles',cap=cap)
    fig.suptitle(NAMES[case]+' case  |  $T=0.01$, RK4',fontsize=15,y=.98)
    fig.legend([Line2D([0],[0],color=c,ls=ls,lw=1.8) for _,_,c,ls in METHODS],[n for _,n,_,_ in METHODS],
        loc='upper center',bbox_to_anchor=(.5,.925),ncol=3,frameon=False,fontsize=12,handlelength=2.8,columnspacing=2.2)
    stem=mode+'_'+case;path=OUT/(stem+'.png');fig.savefig(path,dpi=180,bbox_inches='tight',pad_inches=.13);plt.close(fig)
    return dict(case=case,mode=mode,title=TITLES[mode],png=path.name,png_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source=source,
        records=records,camera=[33,-57],projection='orthographic',data_smoothed=False,method_offsets=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--cases',nargs='+',default=['D','Gaussian']);ap.add_argument('--modes',nargs='+',default=['light','profiles','log','summary']);a=ap.parse_args()
    file=HERE/'manifest.json';entries=json.loads(file.read_text()) if file.exists() else []
    entries=[r for r in entries if not(r['case'] in a.cases and r['mode'] in a.modes)]
    for c in a.cases:
        for mode in a.modes:
            entries.append(draw(c,mode));print(c,mode,flush=True)
    file.write_text(json.dumps(entries,indent=2),encoding='utf-8')
