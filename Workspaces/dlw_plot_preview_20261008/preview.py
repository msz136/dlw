"""Render real analytic DLW u/v previews without modifying the notebook."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import logsumexp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
nb = json.loads((ROOT/'notebook/DLW数值分析report.ipynb').read_text(encoding='utf-8'))
source = next(''.join(c['source']) for c in nb['cells'] if c['id']=='dlw-reference')
ns = dict(np=np, logsumexp=logsumexp,
          CASES={'A':((1.,),(2.,)), 'B':((4.,),(-3.,)), 'C':((6.,4.),(-5.,-3.))})
exec(source, ns)
plt.rcParams.update({'font.family':'serif', 'font.serif':['STIXGeneral'],
                     'mathtext.fontset':'stix', 'font.size':11,
                     'axes.spines.top':False, 'axes.spines.right':False})
x = np.linspace(-5,5,1001)
y = np.linspace(-1.5,1.5,161)
t, h = .01, .125
exact = {c:ns['Exact'](c,h) for c in ns['CASES']}
fig, axs = plt.subplots(2,3,figsize=(12,5.6),layout='constrained')
for col, (c,color) in enumerate(zip(exact,['#1776bc','#d47b19','#38965f'])):
    for row,(key,values) in enumerate(zip(('u','v'),exact[c].uv([-.5],x,t))):
        ax = axs[row,col]
        ax.plot(x,values[0],color=color,lw=1.8)
        ax.set(xlim=(-5,5),xlabel='$x$',ylabel=f'${key}(x,0,t)$')
        ax.grid(alpha=.12)
        if row==0: ax.set_title(f'Case {c}: '+('one soliton' if c!='C' else 'two solitons'))
fig.suptitle('Exact DLW fields | fixed slice y=0 | t=0.01',fontsize=15)
fig.savefig(HERE/'abc_uv_slices.png',dpi=180,bbox_inches='tight')
plt.close(fig)

fields = exact['C'].uv(y/h-.5,x,t)
fig = plt.figure(figsize=(15,11),layout='constrained')
outer = fig.add_gridspec(2,2)
for option in range(4):
    inner = outer[option//2,option%2].subgridspec(1,2)
    for k,key in enumerate(('u','v')):
        ax = fig.add_subplot(inner[0,k],projection='3d' if option==3 else None)
        if option==0:
            ax.plot(x,exact['C'].uv([-.5],x,t)[k][0],lw=1.8,color='#1776bc')
            ax.set(xlabel='$x$',ylabel=f'${key}$',xlim=(-5,5))
        elif option==1:
            ys = np.array([-1.,0.,1.])
            for yi,v,color in zip(ys,exact['C'].uv(ys/h-.5,x,t)[k],['#1776bc','#d47b19','#38965f']):
                ax.plot(x,v,lw=1.5,color=color,label=f'y={yi:g}')
            ax.set(xlabel='$x$',ylabel=f'${key}$',xlim=(-5,5))
            ax.legend(frameon=False,fontsize=9)
        elif option==2:
            im = ax.pcolormesh(x,y,fields[k],shading='auto',cmap='viridis',rasterized=True)
            ax.contour(x,y,fields[k],levels=6,colors='white',linewidths=.35,alpha=.55)
            ax.axhline(0,color='white',lw=.8,ls='--')
            ax.set(xlabel='$x$',ylabel='$y$')
            fig.colorbar(im,ax=ax,shrink=.7,label=f'${key}$')
        else:
            xx, yy = np.meshgrid(x[::5],y[::3])
            ax.plot_surface(xx,yy,fields[k][::3,::5],cmap='viridis',linewidth=0)
            ax.view_init(elev=28,azim=-65)
            ax.set(xlabel='$x$',ylabel='$y$',zlabel=f'${key}$')
            ax.tick_params(labelsize=8,pad=1)
        title = ['A. Fixed slice: y=0','B. Several slices','C. Spatial map','D. Surface'][option]
        ax.set_title((title if k==0 else '')+'\n'+f'${key}$')
        if option<2: ax.grid(alpha=.12)
fig.suptitle('Four ways to show Case C | exact physical fields | t=0.01',fontsize=16)
fig.savefig(HERE/'style_comparison.png',dpi=165,bbox_inches='tight',pad_inches=.25)
plt.close(fig)
