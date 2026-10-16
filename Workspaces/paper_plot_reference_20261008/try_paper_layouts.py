"""Read-only paper-inspired previews: exact morphology and real numerical errors."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.special import logsumexp
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
paths=[ROOT/'notebook'/n for n in ('DLW数值分析report.ipynb','2HS数值分析report.ipynb')]
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
cells=[{c['id']:''.join(c['source']) for c in json.loads(p.read_text(encoding='utf-8'))['cells']} for p in paths]
ns=dict(np=np,logsumexp=logsumexp,CASES={'A':((1.,),(2.,)),'B':((4.,),(-3.,)),'C':((6.,4.),(-5.,-3.))})
exec(cells[0]['dlw-reference'],ns)
G=ns['Exact']('C',.125)
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],
                     'mathtext.fontset':'stix','font.size':12})
x=np.linspace(-30,30,501);y=np.linspace(-30,30,501)
fields=G.uv(y/.125-.5,x,0)
fig=plt.figure(figsize=(12,8),layout='constrained');grid=fig.add_gridspec(2,2)
X,Y=np.meshgrid(x,y)
for row,key in enumerate(('u','v')):
    z=fields[row]
    ax=fig.add_subplot(grid[row,0],projection='3d')
    ax.plot_surface(X,Y,z,cmap='jet',rstride=3,cstride=3,linewidth=0,antialiased=True)
    ax.view_init(30,-58);ax.set(xlabel='$x$',ylabel='$y$',zlabel=f'${key}$',title=f'({chr(97+row*2)}) {key}: surface')
    ax.set_box_aspect((1.2,1,.75));ax.tick_params(labelsize=9)
    ax=fig.add_subplot(grid[row,1])
    im=ax.pcolormesh(x,y,z,cmap='jet',shading='auto',rasterized=True)
    ax.add_patch(Rectangle((-5,-1.5),10,3,fill=False,edgecolor='white',linewidth=1.3))
    ax.set(xlabel='$x$',ylabel='$y$',title=f'({chr(98+row*2)}) {key}: density map')
    ax.set_aspect('equal');fig.colorbar(im,ax=ax,shrink=.8,label=f'${key}$')
fig.suptitle('DLW Case C | exact fields at t=0 | Physica D Fig. 3 layout\nWhite rectangle: previous local window',fontsize=15)
fig.savefig(HERE/'dlw_paper_layout.png',dpi=170,bbox_inches='tight',pad_inches=.5);plt.close(fig)

hs=dict(np=np)
exec(cells[1]['hs-two-reference'],hs)
fig,axes=plt.subplots(2,2,figsize=(10,6),sharex=True,sharey=True,layout='constrained')
xx=np.linspace(-15,15,2001)
for ax,t in zip(axes.ravel(),(-50.,-20.,20.,50.)):
    exact=hs['hs_two_exact_physical'](xx,t)
    ax.plot(xx,exact['u'],color='red',lw=1.3,label='$u$')
    ax.plot(xx,exact['rho'],color='blue',lw=1.3,label=r'$\rho$')
    ax.set(xlim=(-15,15),ylim=(-.2,1.2),xlabel='$x$',ylabel=r'$u,\rho$',title=f'$t={t:g}$')
    ax.legend(frameon=True,fontsize=10);ax.grid(False)
fig.suptitle('2HS two solitons | exact profiles | Fig. 2 layout\nExtended times show analytic fields only',fontsize=15)
fig.savefig(HERE/'hs_paper_layout.png',dpi=170,bbox_inches='tight');plt.close(fig)

# GSG Fig. 1/2 idiom: numerical/exact profiles and absolute errors.
d=np.load(ROOT/'Workspaces/paired_field_preview_20261008/data.npz')
i=int(np.argmin(abs(d['dlw_y'])));yy=float(d['dlw_y'][i]);xx=d['dlw_x']
exact=G.uv([yy/.125-.5],xx,.01)[0][0]
hxx=d['hs_x'];ht=float(d['hs_t'][-1]);hexact=hs['hs_two_exact_physical'](hxx,ht)['u']
fig,axes=plt.subplots(2,2,figsize=(11,6),layout='constrained')
for row, (xx,num,ref,title) in enumerate([
    (xx,d['dlw_u'][i],exact,f'DLW: t=0.01, y={yy:g}'),
    (hxx,d['hs_u'][-1],hexact,'2HS: t=0.5')]):
    axes[row,0].plot(xx,ref,'r-',lw=1.5,label='Exact')
    ids=np.arange(0,len(xx),max(1,len(xx)//90))
    axes[row,0].plot(xx[ids],num[ids],'b.',ms=3,label='Numerical')
    axes[row,0].set(xlabel='$x$',ylabel='$u$',title=title+' | physical field')
    axes[row,0].legend(frameon=False)
    axes[row,1].plot(xx,abs(num-ref),color='#1776bc',lw=1.2)
    axes[row,1].set(xlabel='$x$',ylabel='$|u_h-u_*|$',title=title+' | absolute error')
    axes[row,1].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
    for ax in axes[row]:ax.grid(alpha=.12)
fig.suptitle('GSG Fig. 1/2 layout adapted to our numerical results',fontsize=15)
fig.savefig(HERE/'numerical_paper_layout.png',dpi=170,bbox_inches='tight');plt.close(fig)

# Original published panels beside the real-data adaptation.
canvas=Image.new('RGB',(1900,1260),'white');draw=ImageDraw.Draw(canvas)
font=ImageFont.truetype('C:/Windows/Fonts/times.ttf',32)
for row,(paper,box,ours,title) in enumerate([
    ('dlw_p7.png',(.10,.055,.85,.275),'dlw_paper_layout.png','DLW: fixed t, x-y surface + density map'),
    ('hs_p10.png',(.13,.22,.84,.605),'hs_paper_layout.png','2HS: x profiles at several times')]):
    im=Image.open(HERE/paper).convert('RGB');w,h=im.size
    crop=im.crop(tuple(int(v*s) for v,s in zip(box,(w,h,w,h))))
    crop.thumbnail((850,535));canvas.paste(crop,((900-crop.width)//2,row*630+80))
    im=Image.open(HERE/ours).convert('RGB');im.thumbnail((990,545))
    canvas.paste(im,(905+(990-im.width)//2,row*630+65))
    draw.text((25,row*630+10),'Paper original',fill='black',font=font)
    draw.text((930,row*630+10),'Our preview',fill='black',font=font)
    draw.text((25,row*630+590),title,fill='black',font=font)
canvas.save(HERE/'paper_vs_preview.png')
for p in paths:assert hashes[p.name]==hashlib.sha256(p.read_bytes()).hexdigest()
(HERE/'validation.json').write_text(json.dumps(dict(notebooks_unchanged=True,hashes=hashes,
    sources={'2HS':'PDF p10 Fig2; p18 Fig4','DLW':'PDF p7 Fig3','GSG':'PDF p15 Fig1/2'},
    dlw_morphology_domain=[-30,30],dlw_morphology_time=0,
    hs_morphology_times=[-50,-20,20,50],
    scope='Morphology uses exact analytic fields; numerical comparison reads prior real solver samples. No numerical error outside the computed domain.'),indent=2),encoding='utf-8')
print('Paper-layout previews complete; notebooks unchanged')
