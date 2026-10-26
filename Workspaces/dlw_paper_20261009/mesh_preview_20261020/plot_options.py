"""Four layout sketches from actual case-C SAMM data.
Reference: oa-geo-esd-15-527-2024-f12: aligned field panels and contour overlay.
Other layouts are original proposals outside the gallery. No synthetic data.
"""
from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
P=Path(__file__).resolve().parent
d=np.load(P/'case_C_mesh.npz');m=json.loads((P/'metrics.json').read_text(encoding='utf-8'))
plt.rcParams.update({'font.family':'STIXGeneral','mathtext.fontset':'stix','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.7})
blue='#0072B2';orange='#D55E00';gray='#767676'
fig=plt.figure(figsize=(15,10),layout='constrained');outer=fig.add_gridspec(2,2,wspace=.10,hspace=.17)
g=outer[0,0].subgridspec(1,2,wspace=.04)
axes=[]
for c,(key,title) in enumerate([('uniform','Uniform mesh'),('xf','SAMM, $t=0.01$')]):
 ax=fig.add_subplot(g[0,c]);axes.append(ax)
 im=ax.pcolormesh(d['xfield'],d['yfield'],d['u'],cmap='Blues',shading='auto',vmin=0,vmax=d['u'].max(),rasterized=True)
 x=d[key][::12];x=x[(x>=-30)&(x<=30)]
 ax.vlines(x,-30,30,color='#303030',lw=.42,alpha=.7)
 ax.hlines(np.arange(-29.95,30,2.4),-30,30,color='#303030',lw=.38,alpha=.6)
 ax.set(xlim=(-30,30),ylim=(-30,30),xlabel='$x$',title=title)
 if c==0:ax.set_ylabel('$y$')
 else:ax.set_yticklabels([])
fig.colorbar(im,ax=axes,label='Exact $u$ (same field)',shrink=.65,pad=.02)
axes[0].text(0,1.17,'A  Wave field + mesh | recommended',transform=axes[0].transAxes,fontweight='bold',fontsize=13)
axes[0].text(0,-.22,'Every 12th x line and 24th y line shown; identical index selection.',transform=axes[0].transAxes,fontsize=9)

g=outer[0,1].subgridspec(2,1,height_ratios=[3,1.4],hspace=.03)
ax=fig.add_subplot(g[0]); ax.plot(d['xf'],d['rho'],color=blue,lw=2)
ax.set(xlim=(-30,30),ylabel=r'$\bar\rho(x,T)$',title='B  Density + node strips | recommended');ax.title.set_fontweight('bold')
ax.tick_params(labelbottom=False);ax.grid(alpha=.12)
bx=fig.add_subplot(g[1],sharex=ax)
for k,y,c,name in [('uniform',1,orange,'Uniform'),('xf',0,blue,'SAMM')]:
 x=d[k][::8]; x=x[(x>=-30)&(x<=30)]
 bx.plot(x,np.full(len(x),y),'|',ms=17,color=c)
bx.set(yticks=[0,1],yticklabels=['SAMM','Uniform'],ylim=(-.65,1.65),xlabel='$x$');bx.spines['left'].set_visible(False)
bx.text(.01,-.46,'Every 8th x node shown, selected by the same indices.',transform=bx.transAxes,fontsize=9)

ax=fig.add_subplot(outer[1,0]);xf=d['xf'];xmid=(xf[1:]+xf[:-1])/2
ax.plot(xmid,np.diff(xf)/m['config']['h'],color=blue,lw=2,label='SAMM at $T$')
ax.plot((d['x0'][1:]+d['x0'][:-1])/2,np.diff(d['x0'])/.1,color=gray,ls='--',lw=1,label='Adaptive initial mesh')
ax.axhline(1,color=orange,ls=':',lw=1.4,label='Uniform')
ax.set(xlim=(-30,30),xlabel='$x$',ylabel=r'Local spacing / uniform spacing',title='C  Local spacing | recommended');ax.title.set_fontweight('bold');ax.grid(alpha=.12);ax.legend(frameon=False,fontsize=10,loc='upper right')
ax.text(.03,.08,'Below 1: more nodes per unit length',transform=ax.transAxes,fontsize=10,color=blue)

ax=fig.add_subplot(outer[1,1]);ids=np.where(abs(d['x0'])<30)[0][::32]
for i in ids: ax.plot(d['times'],d['xs'][:,i]-d['x0'][i],color=plt.cm.viridis((d['x0'][i]+30)/60),lw=1)
ax.axhline(0,color=gray,lw=.6);ax.set(xlabel='$t$',ylabel=r'$x_i(t)-x_i(0)$',title='D  Actual node motion | supporting panel');ax.title.set_fontweight('bold');ax.grid(alpha=.12)
ax.ticklabel_format(axis='y',style='sci',scilimits=(0,0))
ax.text(.03,.93,'Initial redistribution removed; every 32nd node shown',transform=ax.transAxes,fontsize=9,va='top')
fig.suptitle('Two-soliton case C: $(p,q)=(6,-5),(4,-3)$  |  PE + RK4  |  800 shared x nodes\nLayout sketches from computed meshes; uniform y lattice, $h=0.1$, $T=0.01$',fontsize=15)
fig.savefig(P/'mesh_options.png',dpi=170)
plt.close(fig)
