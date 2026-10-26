"""Additional 3D choices from the verified T=.01 physical-field arrays.

Default quantity is absolute field error, corresponding to the existing maps.
The separate panels reuse the prior DLW jet/STIX view (28,-62). Overlays use
method colors on native grids; no vertical shift, smoothing or normalization
by method is applied. Display meshes are thinned with their maxima retained.
"""
from pathlib import Path
import argparse,json,hashlib,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D

HERE=Path(__file__).resolve().parent
DATA=HERE.parent/'report_refresh_20261024/natural_selection_20261025/figures/data'
OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
CASES=['A','D','Gaussian','Sinusoidal']
NAMES={'A':'One-soliton case','D':'Two-soliton case','Gaussian':'Gaussian case','Sinusoidal':'Sinusoidal case'}
WINDOWS={'A':(-5,5),'D':(-30,30),'Gaussian':(-18,18),'Sinusoidal':(-12,12)}
METHODS=[('endpoint','Endpoint-SD','#2878B5'),('centered','Centered-SD','#E07A23'),('fd','FD','#299568')]
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
 'axes.linewidth':.65,'savefig.facecolor':'white','figure.facecolor':'white',
 'pdf.fonttype':42,'ps.fonttype':42})

def datasets(case,quantity):
    path=DATA/(case+'.npz');d=np.load(path);x=d['x'];mask=(x>=WINDOWS[case][0])&(x<=WINDOWS[case][1]);rows={}
    for q in ['u','v']:
        rows[q]=[]
        for prefix,name,color in METHODS:
            key=f'{prefix}_error_final_{q}' if quantity=='error' else f'{prefix}_final_{q}'
            z=d[key][:,mask];z=abs(z) if quantity=='error' else z
            rows[q].append(dict(method=name,prefix=prefix,color=color,x=x[mask],y=d[f'{prefix}_y_{q}'],z=z,key=key))
    return rows,dict(path=str(path),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def thin(row):
    z=row['z'];peak=np.unravel_index(np.argmax(abs(z)),z.shape)
    iy=np.unique(np.r_[np.linspace(0,z.shape[0]-1,min(121,z.shape[0])).round().astype(int),peak[0]])
    ix=np.unique(np.r_[np.linspace(0,z.shape[1]-1,min(181,z.shape[1])).round().astype(int),peak[1]])
    X,Y=np.meshgrid(row['x'][ix],row['y'][iy]);Z=z[np.ix_(iy,ix)]
    assert float(abs(Z).max())==float(abs(z).max())
    return X,Y,Z,iy,ix

def style(ax,case,ys,zrange,q,exponent,quantity):
    zlabel=('$|'+q+r'_h-'+q+r'^*|$' if quantity=='error' else '$'+q+'_h$')
    if exponent:zlabel+=' ($10^{'+str(exponent)+'}$)'
    ax.set(xlim=WINDOWS[case],ylim=ys,zlim=zrange)
    ax.set_xlabel('$x$',labelpad=2);ax.set_ylabel('$y$',labelpad=2);ax.set_zlabel(zlabel,labelpad=3)
    ax.view_init(28,-62);ax.set_box_aspect((1.15,1,.78))
    for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
        axis.set_major_locator(MaxNLocator(3));axis.pane.set_facecolor((.98,.98,.98,1));axis._axinfo['grid']['color']=(.82,.84,.87,.7);axis._axinfo['grid']['linewidth']=.5
    ax.tick_params(labelsize=9,pad=1)

def draw(case,kind='separate',quantity='error'):
    rows,source=datasets(case,quantity)
    separate=kind=='separate'
    fig=plt.figure(figsize=(11.6,7.4) if separate else (10.5,5.25))
    if separate:grid=fig.add_gridspec(2,5,left=.015,right=.94,bottom=.03,top=.86,wspace=.02,hspace=.22,width_ratios=[1,1,1,.19,.04])
    else:grid=fig.add_gridspec(1,2,left=.025,right=.94,bottom=.045,top=.76,wspace=.10)
    records=[]
    for qi,q in enumerate(['u','v']):
        parts=rows[q]
        high=max(float(p['z'].max()) for p in parts);low=0 if quantity=='error' else min(float(p['z'].min()) for p in parts)
        exponent=math.floor(math.log10(max(abs(low),abs(high)))) if quantity=='error' else 0
        scale=10.**exponent
        limits=(low/scale,high/scale*1.025) if quantity=='error' else (low-.04*(high-low),high+.04*(high-low))
        ys=(min(float(p['y'].min()) for p in parts),max(float(p['y'].max()) for p in parts))
        norm=Normalize(low/scale,high/scale)
        if not separate:
            ax=fig.add_subplot(grid[0,qi],projection='3d',computed_zorder=False)
            style(ax,case,ys,limits,q,exponent,quantity)
            ax.set_zlabel('')
            title='('+chr(97+qi)+') '+('$|'+q+r'_h-'+q+r'^*|$' if quantity=='error' else '$'+q+'_h$')
            if exponent:title+=' ($10^{'+str(exponent)+'}$)'
            ax.set_title(title,pad=8)
        for mi,p in enumerate(parts):
            X,Y,Z,iy,ix=thin(p)
            if separate:
                ax=fig.add_subplot(grid[qi,mi],projection='3d')
                ax.plot_surface(X,Y,Z/scale,cmap='jet',norm=norm,rstride=1,cstride=1,linewidth=0,antialiased=False,shade=False,rasterized=True)
                style(ax,case,ys,limits,q,exponent,quantity)
                ax.set_title('('+chr(97+3*qi+mi)+') '+p['method'],pad=8,fontsize=12)
            else:
                ax.plot_surface(X,Y,Z/scale,color=p['color'],alpha=.15,linewidth=0,antialiased=False,shade=False,rasterized=True,zorder=2+mi)
                ax.plot_wireframe(X,Y,Z/scale,color=p['color'],rcount=15,ccount=21,linewidth=.55,alpha=.8,rasterized=True,zorder=7+mi)
            records.append(dict(field=q,method=p['method'],key=p['key'],minimum=float(p['z'].min()),maximum=float(p['z'].max()),native_y=True,common_vertical_limits=limits,scale_multiplier=scale,mesh_shape=list(Z.shape),source_shape=list(p['z'].shape),iy=iy.tolist(),ix=ix.tolist(),mesh_extremum_preserved=True))
        if separate:
            cb=fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap='jet'),cax=fig.add_subplot(grid[qi,4]))
            cb.ax.yaxis.set_major_locator(MaxNLocator(4));cb.ax.tick_params(labelsize=9)
            cb.set_label(('$|'+q+r'_h-'+q+r'^*|$' if quantity=='error' else '$'+q+'_h$')+(' ($10^{'+str(exponent)+'}$)' if exponent else ''),fontsize=10)
    description='Absolute physical-field errors' if quantity=='error' else 'Numerical physical fields'
    fig.suptitle(NAMES[case]+'  |  '+description+'\n$T=0.01$, RK4',fontsize=14,y=.985)
    if not separate:
        fig.legend([Line2D([0],[0],color=c,lw=2) for _,_,c in METHODS],[n for _,n,_ in METHODS],loc='upper center',bbox_to_anchor=(.5,.89),ncol=3,frameon=False,fontsize=11)
    stem=('errors' if quantity=='error' else 'fields')+'_3d_'+kind+'_'+case
    png=OUT/(stem+'.png');pdf=OUT/(stem+'.pdf')
    fig.savefig(png,dpi=300,bbox_inches='tight',pad_inches=.12)
    fig.savefig(pdf,dpi=220,bbox_inches='tight',pad_inches=.12);plt.close(fig)
    (OUT/(stem+'.py')).write_text("from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parent.parent))\nfrom plot_3d import draw\ndraw("+repr(case)+","+repr(kind)+","+repr(quantity)+")\n",encoding='utf-8')
    return dict(case=case,stage='final',T=.01,kind=kind,quantity=quantity,png=png.name,pdf=pdf.name,png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),source=source,records=records,camera=[28,-62],x_window=WINDOWS[case],shared_vertical_scale=True,surface_offsets=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--quantity',choices=['error','field'],default='error');ap.add_argument('--cases',nargs='*',default=CASES);args=ap.parse_args()
    path=OUT/'3d_manifest.json';items=json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    items=[e for e in items if not(e['case'] in args.cases and e['quantity']==args.quantity)]
    for c in args.cases:
        for kind in ['separate','overlay']:
            items.append(draw(c,kind,args.quantity));print('Rendered',c,kind,args.quantity,flush=True)
    path.write_text(json.dumps(items,indent=2),encoding='utf-8')
