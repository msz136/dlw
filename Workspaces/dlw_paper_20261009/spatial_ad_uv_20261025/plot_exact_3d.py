"""Exact initial physical fields, accompanying the existing case introductions.

Uses the same stored continuous initial arrays as exact_{case}.png.
Style follows the paper's STIX/jet 3D candidates, with a separate u,v panel.
Physical values, coordinates and sign are unchanged. Both extrema survive
display-mesh thinning. No numerical-method surfaces enter these figures.
"""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator, ScalarFormatter

HERE=Path(__file__).resolve().parent
DATA=HERE.parent/'report_refresh_20261024/natural_selection_20261025/figures/data'
OUT=HERE/'figures'
CASES=['A','D','Gaussian','Sinusoidal']
NAMES={'A':'One-soliton case','D':'Two-soliton case','Gaussian':'Gaussian case','Sinusoidal':'Sinusoidal case'}
WINDOWS={'A':(-5,5),'D':(-30,30),'Gaussian':(-18,18),'Sinusoidal':(-12,12)}
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,
 'axes.linewidth':.65,'savefig.facecolor':'white','figure.facecolor':'white',
 'pdf.fonttype':42,'ps.fonttype':42})

def draw(case):
    source=DATA/(case+'.npz')
    with np.load(source) as d:
        mask=(d['x']>=WINDOWS[case][0])&(d['x']<=WINDOWS[case][1])
        x=d['x'][mask]; y=d['exact_initial_y']; records=[]
        fig=plt.figure(figsize=(10.6,5.0))
        grid=fig.add_gridspec(1,2,left=.025,right=.94,bottom=.035,top=.82,wspace=.10)
        for i,q in enumerate(['u','v']):
            z=d['exact_initial_'+q][:,mask]
            lo=np.unravel_index(np.argmin(z),z.shape);hi=np.unravel_index(np.argmax(z),z.shape)
            iy=np.unique(np.r_[np.linspace(0,z.shape[0]-1,min(241,z.shape[0])).round().astype(int),lo[0],hi[0]])
            ix=np.unique(np.r_[np.linspace(0,z.shape[1]-1,min(401,z.shape[1])).round().astype(int),lo[1],hi[1]])
            X,Y=np.meshgrid(x[ix],y[iy]);Z=z[np.ix_(iy,ix)]
            assert float(Z.min())==float(z.min()) and float(Z.max())==float(z.max())
            low,high=float(z.min()),float(z.max());padding=.06*(high-low)
            ax=fig.add_subplot(grid[0,i],projection='3d')
            ax.plot_surface(X,Y,Z,cmap='jet',norm=Normalize(low,high),rstride=1,cstride=1,
                linewidth=0,antialiased=False,shade=False,rasterized=True)
            ax.set(xlim=WINDOWS[case],ylim=(float(y.min()),float(y.max())),zlim=(low-padding,high+padding))
            ax.set_xlabel('$x$',labelpad=2);ax.set_ylabel('$y$',labelpad=2)
            ax.set_title('('+chr(97+i)+') $'+q+r'^*(x,y,0)$',pad=8)
            ax.view_init(28,-62);ax.set_box_aspect((1.15,1,.78))
            for axis in [ax.xaxis,ax.yaxis,ax.zaxis]:
                axis.set_major_locator(MaxNLocator(4));axis.pane.set_facecolor((.98,.98,.98,1))
                axis._axinfo['grid']['color']=(.82,.84,.87,.7);axis._axinfo['grid']['linewidth']=.5
            ax.xaxis.set_major_locator(MaxNLocator(4,prune='both'))
            ax.yaxis.set_major_locator(MaxNLocator(4,prune='both'))
            fmt=ScalarFormatter(useMathText=True,useOffset=False);fmt.set_scientific(False)
            ax.zaxis.set_major_formatter(fmt);ax.tick_params(labelsize=10,pad=1)
            records.append(dict(field=q,key='exact_initial_'+q,minimum=low,maximum=high,
                original_shape=list(z.shape),display_shape=list(Z.shape),ix=ix.tolist(),iy=iy.tolist(),
                minimum_and_maximum_preserved=True,physical_values_unshifted=True))
        fig.suptitle(NAMES[case]+'  |  Exact physical fields at $t=0$',fontsize=14,y=.98)
        stem='exact_3d_'+case;png=OUT/(stem+'.png');pdf=OUT/(stem+'.pdf')
        fig.savefig(png,dpi=300,bbox_inches='tight',pad_inches=.12)
        fig.savefig(pdf,dpi=220,bbox_inches='tight',pad_inches=.12);plt.close(fig)
    (OUT/(stem+'.py')).write_text("from pathlib import Path\nimport sys\nsys.path.insert(0,str(Path(__file__).resolve().parent.parent))\nfrom plot_exact_3d import draw\ndraw("+repr(case)+")\n",encoding='utf-8')
    return dict(case=case,time=0,quantity='exact physical fields',stage='exact',
        source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        png=png.name,pdf=pdf.name,png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),
        pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),x_window=WINDOWS[case],camera=[28,-62],records=records)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('cases',nargs='*');args=parser.parse_args()
    path=OUT/'exact_3d_manifest.json';items=json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    selected=args.cases or CASES;items=[r for r in items if r['case'] not in selected]
    for c in selected:
        items.append(draw(c));print('Rendered exact fields:',c,flush=True)
    path.write_text(json.dumps(items,indent=2),encoding='utf-8')
