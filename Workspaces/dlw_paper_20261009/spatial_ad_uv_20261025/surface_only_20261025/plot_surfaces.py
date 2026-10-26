"""Transparent surface-only comparisons from stored T=.01 error fields.

All three methods share one Poly3DCollection per component so their triangles
are sorted together in projected depth. No raw-point markers or sectional
curves are drawn. The optional mesh uses faint sparse lines on the surfaces.
Surface geometry is piecewise linear through selected native grid nodes;
every x sample is retained, with up to 201 native y rows plus the peak row.
There is no smoothing, height offset or method-specific scaling. Near the
common zero plane only opacity fades, to avoid three colored background planes.
"""
from pathlib import Path
import argparse,json,hashlib,math,gc
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from PIL import Image

HERE=Path(__file__).resolve().parent;PROJECT=HERE.parent
DATA=PROJECT.parent/'report_refresh_20261024/natural_selection_20261025/figures/data'
OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
CASES=['A','D','Gaussian','Sinusoidal']
WINDOWS={'A':(-5,5),'D':(-30,30),'Gaussian':(-18,18),'Sinusoidal':(-12,12)}
NAMES={'A':'One-soliton','D':'Two-soliton','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}
METHODS=[('endpoint','Endpoint-SD','#3479B8'),('centered','Centered-SD','#E28A3B'),('fd','FD','#38A58B')]
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
    'axes.linewidth':.65,'savefig.facecolor':'white','figure.facecolor':'white','path.simplify':False})

def triangles(x,y,z):
    X,Y=np.meshgrid(x,y);v=np.stack([X,Y,z],axis=-1)
    a=v[:-1,:-1].reshape(-1,3);b=v[:-1,1:].reshape(-1,3)
    c=v[1:,1:].reshape(-1,3);d=v[1:,:-1].reshape(-1,3)
    return np.concatenate([np.stack([a,b,c],axis=1),np.stack([a,c,d],axis=1)])

def draw(case,mesh=False,opacity=.32):
    source=DATA/(case+'.npz');d=np.load(source)
    mask=(d['x']>=WINDOWS[case][0])&(d['x']<=WINDOWS[case][1]);x=d['x'][mask]
    fig=plt.figure(figsize=(11,5.35));grid=fig.add_gridspec(1,2,left=.02,right=.95,bottom=.025,top=.80,wspace=.08)
    records=[]
    for qi,q in enumerate(['u','v']):
        parts=[dict(prefix=p,name=n,color=c,y=d[p+'_y_'+q],z=abs(d[p+'_error_final_'+q][:,mask])) for p,n,c in METHODS]
        high=max(float(r['z'].max()) for r in parts);exponent=math.floor(math.log10(high));scale=10.**exponent
        ymax=max(float(r['y'].max()) for r in parts);ymin=min(float(r['y'].min()) for r in parts)
        allfaces=[];allcolors=[];lines=[];linecolors=[]
        for r in parts:
            y=r['y'];z=r['z'];peak=np.unravel_index(z.argmax(),z.shape)
            iy=np.unique(np.r_[np.linspace(0,len(y)-1,min(201,len(y))).round().astype(int),peak[0]])
            faces=triangles(x,y[iy],z[iy]/scale)
            assert float(faces[:,:,2].max())==float(z.max())/scale
            # Gentle diffuse illumination in displayed-box coordinates.
            normalized=faces/np.array([x[-1]-x[0],ymax-ymin,high/scale])
            normals=np.cross(normalized[:,1]-normalized[:,0],normalized[:,2]-normalized[:,0])
            normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-30)
            light=np.array([-.3,-.4,.8660254]);strength=.82+.18*np.maximum(normals@light,0)
            rgb=np.array(to_rgb(r['color']))[None,:]*strength[:,None]
            meanheight=faces[:,:,2].mean(axis=1)*scale
            alpha=opacity*np.clip(meanheight/(high*1e-4),0,1)
            allfaces.append(faces);allcolors.append(np.c_[rgb,alpha])
            if mesh:
                for j in np.linspace(0,len(y)-1,7).round().astype(int):
                    lines.append(np.c_[x,np.full_like(x,y[j]),z[j]/scale]);linecolors.append((*to_rgb(r['color']),.18))
                for j in np.linspace(0,len(x)-1,9).round().astype(int):
                    lines.append(np.c_[np.full_like(y,x[j]),y,z[:,j]/scale]);linecolors.append((*to_rgb(r['color']),.18))
            records.append(dict(case=case,field=q,method=r['name'],native_shape=list(z.shape),display_shape=[len(iy),len(x)],
                native_y_indices=iy.tolist(),all_x_samples_used=True,maximum=float(z.max()),common_height_scale=scale,
                opacity=opacity,zero_plane_fade_height=high*1e-4,mesh=mesh))
        ax=fig.add_subplot(grid[0,qi],projection='3d')
        collection=Poly3DCollection(np.concatenate(allfaces),facecolors=np.concatenate(allcolors),edgecolors='none',linewidths=0,antialiaseds=False,zsort='average')
        ax.add_collection3d(collection)
        if mesh:ax.add_collection3d(Line3DCollection(lines,colors=linecolors,linewidths=.23),autolim=False)
        ax.set_proj_type('ortho');ax.view_init(29,-58);ax.set_box_aspect((1.2,1,.83))
        ax.set(xlim=WINDOWS[case],ylim=(ymin,ymax),zlim=(0,high/scale*1.045),xlabel='$x$',ylabel='$y$')
        ax.xaxis.labelpad=2;ax.yaxis.labelpad=2
        for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
            axis.pane.set_facecolor((1,1,1,0));axis.pane.set_edgecolor((.88,.9,.92,.55))
            axis._axinfo['grid']['color']=(.82,.85,.88,.45);axis._axinfo['grid']['linewidth']=.4
        ax.xaxis.set_major_locator(MaxNLocator(4,prune='both'));ax.yaxis.set_major_locator(MaxNLocator(4,prune='both'));ax.zaxis.set_major_locator(MaxNLocator(3))
        ax.tick_params(labelsize=10,pad=1)
        ax.set_title('('+chr(97+qi)+') $|'+q+r'_h-'+q+r'^*|$  ($10^{'+str(exponent)+'}$)',pad=5,fontsize=13)
    fig.suptitle(NAMES[case]+' case  |  $T=0.01$, RK4',fontsize=15,y=.985)
    fig.legend(handles=[Patch(facecolor=c,edgecolor='none',alpha=.65,label=n) for _,n,c in METHODS],
        loc='upper center',bbox_to_anchor=(.5,.925),ncol=3,frameon=False,fontsize=12,handlelength=1.4,columnspacing=2.4)
    stem=('mesh_' if mesh else 'plain_')+case
    render=OUT/(stem+'_supersampled.png');path=OUT/(stem+'.png')
    fig.savefig(render,dpi=360,bbox_inches='tight',pad_inches=.12);plt.close(fig)
    with Image.open(render) as im:
        im.resize((im.width//2,im.height//2),Image.Resampling.LANCZOS).save(path,dpi=(180,180))
    gc.collect()
    return dict(case=case,mode='mesh' if mesh else 'plain',T=.01,quantity='absolute physical-field error',
        png=path.name,png_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        surface_collection='one globally depth-sorted triangle collection per field',records=records,camera=[29,-58],
        source_values_smoothed=False,methodwise_offsets=False,section_lines=False,raw_point_markers=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--cases',nargs='+',default=CASES);ap.add_argument('--modes',nargs='+',default=['plain','mesh']);args=ap.parse_args()
    path=HERE/'manifest.json';rows=json.loads(path.read_text()) if path.exists() else []
    rows=[r for r in rows if not(r['case'] in args.cases and r['mode'] in args.modes)]
    for c in args.cases:
        for m in args.modes:
            rows.append(draw(c,m=='mesh'));print(c,m,flush=True)
            path.write_text(json.dumps(rows,indent=2),encoding='utf-8')
