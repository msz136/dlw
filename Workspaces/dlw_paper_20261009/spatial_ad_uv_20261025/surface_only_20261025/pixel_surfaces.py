"""Surface-only previews with alpha composited once per visible method sheet.

Preserves native field errors; uses piecewise-linear triangle geometry and
smooth vertex lighting. The optional grid is a faint texture on the surface,
not separately overlaid sectional curves. No fitting or error smoothing.
"""
from pathlib import Path
import argparse,json,hashlib,math,subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
from plot_surfaces import DATA,CASES,NAMES,WINDOWS,METHODS

HERE=Path(__file__).resolve().parent;OUT=HERE/'figures';INTER=HERE/'render_data';INTER.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,'figure.facecolor':'white','axes.linewidth':.6})

def draw(case,opacity=.34):
    source=DATA/(case+'.npz');d=np.load(source);mask=(d['x']>=WINDOWS[case][0])&(d['x']<=WINDOWS[case][1]);x=d['x'][mask]
    fig=plt.figure(figsize=(11,5.35),dpi=360);grid=fig.add_gridspec(1,2,left=.02,right=.95,bottom=.025,top=.80,wspace=.08)
    axes=[];data=[];records=[]
    for qi,q in enumerate(['u','v']):
        parts=[dict(prefix=p,name=n,color=c,y=d[p+'_y_'+q],z=abs(d[p+'_error_final_'+q][:,mask])) for p,n,c in METHODS]
        high=max(float(r['z'].max()) for r in parts);exponent=math.floor(math.log10(high));scale=10.**exponent
        ymax=max(float(r['y'].max()) for r in parts);ymin=min(float(r['y'].min()) for r in parts)
        ax=fig.add_subplot(grid[0,qi],projection='3d');ax.set_proj_type('ortho');ax.view_init(29,-58);ax.set_box_aspect((1.2,1,.83))
        ax.set(xlim=WINDOWS[case],ylim=(ymin,ymax),zlim=(0,high/scale*1.045),xlabel='$x$',ylabel='$y$')
        ax.xaxis.labelpad=2;ax.yaxis.labelpad=2
        for a in [ax.xaxis,ax.yaxis,ax.zaxis]:
            a.pane.set_facecolor((1,1,1,0));a.pane.set_edgecolor((.88,.9,.92,.6));a._axinfo['grid']['color']=(.82,.85,.88,.5);a._axinfo['grid']['linewidth']=.4
        ax.xaxis.set_major_locator(MaxNLocator(4,prune='both'));ax.yaxis.set_major_locator(MaxNLocator(4,prune='both'));ax.zaxis.set_major_locator(MaxNLocator(3));ax.tick_params(labelsize=10,pad=1)
        ax.set_title('('+chr(97+qi)+') $|'+q+r'_h-'+q+r'^*|$  ($10^{'+str(exponent)+'}$)',pad=5,fontsize=13)
        axes.append(ax);data.append((q,parts,high,scale,ymin,ymax))
    fig.suptitle(NAMES[case]+' case  |  $T=0.01$, RK4',fontsize=15,y=.985)
    fig.legend(handles=[Patch(facecolor=c,edgecolor='none',alpha=.65,label=n) for _,n,c in METHODS],loc='upper center',bbox_to_anchor=(.5,.925),ncol=3,frameon=False,fontsize=12,handlelength=1.4,columnspacing=2.4)
    fig.canvas.draw();width,height=fig.canvas.get_width_height();background=INTER/(case+'_axes.png');fig.savefig(background,dpi=360)
    arrays=[];scenes=[];offset=0
    for ax,(q,parts,high,scale,ymin,ymax) in zip(axes,data):
        meshes=[];coords=[]
        for r in parts:
            y=r['y'];z=r['z'];peak=np.unravel_index(z.argmax(),z.shape)
            iy=np.unique(np.r_[np.linspace(0,len(y)-1,min(241,len(y))).round().astype(int),peak[0]])
            yy=y[iy];zz=z[iy];X,Y=np.meshgrid(x,yy)
            px,py,pz=proj3d.proj_transform(X.ravel(),Y.ravel(),(zz/scale).ravel(),ax.get_proj());xy=ax.transData.transform(np.c_[px,py]);xy[:,1]=height-xy[:,1]
            # Smooth lighting from normals, retaining the unmodified heights.
            gy,gx=np.gradient(zz/high,yy/(ymax-ymin),x/(x[-1]-x[0]));normal=np.stack([-gx,-gy,np.ones_like(gx)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
            light=np.array([-.3,-.4,.8660254]);shade=.80+.20*np.maximum(normal@light,0)
            rgb=shade[...,None]*np.array(to_rgb(r['color']))
            alpha=opacity*np.clip(zz/(high*1e-4),0,1)
            U=(X-x[0])/(x[-1]-x[0]);V=(Y-ymin)/(ymax-ymin)
            a=np.c_[xy,pz,rgb.reshape(-1,3),alpha.ravel(),U.ravel(),V.ravel()].astype('<f4')
            meshes.append(dict(offset=offset,rows=len(yy),cols=len(x),method=r['name']));offset+=a.size;arrays.append(a);coords.append(xy)
            records.append(dict(field=q,method=r['name'],maximum=float(z.max()),source_shape=list(z.shape),display_shape=list(zz.shape),
                native_y_indices=iy.tolist(),all_native_x=True,common_height_scale=scale,zero_plane_fade_height=high*1e-4,opacity=opacity))
        xy=np.concatenate(coords);bounds=[max(0,int(np.floor(xy[:,0].min()))-1),max(0,int(np.floor(xy[:,1].min()))-1),min(width-1,int(np.ceil(xy[:,0].max()))+1),min(height-1,int(np.ceil(xy[:,1].max()))+1)]
        scenes.append(dict(meshes=meshes,bounds=bounds))
    plt.close(fig)
    binary=INTER/(case+'_vertices.bin');np.concatenate(arrays).tofile(binary)
    outputs=[INTER/(case+'_plain.rgba'),INTER/(case+'_mesh.rgba')]
    meta=dict(case=case,width=width,height=height,vertices=str(binary),scenes=scenes,outputs=[str(p) for p in outputs])
    metafile=INTER/(case+'_render.json');metafile.write_text(json.dumps(meta),encoding='utf-8')
    subprocess.run(['node','--expose-gc',str(HERE/'render_surface_pixels.cjs'),str(metafile)],check=True)
    entries=[]
    for mode,path in zip(['plain','mesh'],outputs):
        front=Image.frombytes('RGBA',(width,height),path.read_bytes());base=Image.open(background).convert('RGBA');result=Image.alpha_composite(base,front)
        final=OUT/(mode+'_'+case+'.png');result.convert('RGB').resize((width//2,height//2),Image.Resampling.LANCZOS).save(final,dpi=(180,180))
        entries.append(dict(case=case,mode=mode,png=final.name,png_sha256=hashlib.sha256(final.read_bytes()).hexdigest(),source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            T=.01,quantity='absolute physical-field error',records=records,camera=[29,-58],renderer='per-pixel depth compositing of visible method sheets',
            section_lines=False,raw_point_markers=False,source_values_smoothed=False,methodwise_offsets=False,mesh='faint surface texture, 8 by 6 cells' if mode=='mesh' else 'none'))
    return entries

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--cases',nargs='+',default=CASES);a=ap.parse_args();path=HERE/'manifest.json';records=json.loads(path.read_text()) if path.exists() else []
    records=[r for r in records if r['case'] not in a.cases]
    for c in a.cases:
        records+=draw(c);path.write_text(json.dumps(records,indent=2),encoding='utf-8');print('Completed',c,flush=True)
