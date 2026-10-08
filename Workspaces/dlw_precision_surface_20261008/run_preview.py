"""Real wide-domain numerical/analytic field overlays for DLW A, B, C.

The current notebook is read only. Spatial/time steps are kept at their
existing values; only the actual computational extent is enlarged.
"""
from pathlib import Path
import hashlib
import json
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
PATH=ROOT/'notebook/DLW数值分析report.ipynb'
source_hash=hashlib.sha256(PATH.read_bytes()).hexdigest()
nb=json.loads(PATH.read_text(encoding='utf-8'))
cells={c['id']:''.join(c['source']) for c in nb['cells']}
ns={}
for name in ('imports','config','reference','spatial','sd_fd','sd','sd2_lift',
             'sd2_evolution','fd','mesh','time'):
    exec(cells['dlw-'+name],ns)
config=dict(ns['CONFIG'],L=80.,nx=512,yhalf=30.,eval_half=30.,eval_points=1201)
plt.rcParams.update({'font.family':'serif','font.serif':['STIXGeneral'],
                     'mathtext.fontset':'stix','font.size':12})
reports=[]
for case in ('A','B','C'):
    cache=HERE/f'case_{case}.npz';meta=HERE/f'case_{case}.json'
    if cache.exists() and meta.exists():
        saved=np.load(cache);r=json.loads(meta.read_text())
        assert r['source_sha256']==source_hash and r['config']==json.loads(json.dumps(config))
        x,y=saved['x'],saved['y'];numerical=[saved['u'],saved['v']]
        exact=[saved['exact_u'],saved['exact_v']]
    else:
        started=time.perf_counter()
        print(f'Start case {case}',flush=True)
        result=ns['solve'](case,'SD2','RK4','fixed',config)
        if not result['completed']:raise RuntimeError(f"Case {case}: {result['reason']}, reached {result['reached']}")
        x,y=result['x'],result['y'];numerical=result['fields'];exact=result['exact']
        r=dict(case=case,model='SD2',method='RK4',mesh='fixed',config=config,
               source_sha256=source_hash,completed=True,reached=float(result['reached']),
               elapsed_seconds=time.perf_counter()-started,min_J=float(result['min_J']),
               initial_node_error=float(result['initial_error']))
        np.savez_compressed(cache,x=x,y=y,u=numerical[0],v=numerical[1],
                            exact_u=exact[0],exact_v=exact[1])
        meta.write_text(json.dumps(r,indent=2),encoding='utf-8')
    errors=[abs(n-e) for n,e in zip(numerical,exact)]
    r['max_errors']={k:float(v.max()) for k,v in zip(('u','v'),errors)}
    meta.write_text(json.dumps(r,indent=2),encoding='utf-8')
    print(json.dumps(r),flush=True)
    X,Y=np.meshgrid(x,y)
    fig=plt.figure(figsize=(12,8.5),layout='constrained');grid=fig.add_gridspec(2,2)
    for row,key in enumerate(('u','v')):
        for col in (0,1):
            ax=fig.add_subplot(grid[row,col],projection='3d')
            z=numerical[row] if col==0 else errors[row]
            step=3
            ax.plot_surface(X[:,::step],Y[:,::step],z[:,::step],
                cmap='viridis' if col==0 else 'magma',linewidth=0,antialiased=True,
                rcount=len(y),ccount=401)
            if col==0:
                # Sparse analytic mesh at original sample coordinates, no height shift.
                ax.plot_wireframe(X,Y,exact[row],rstride=60,cstride=120,
                                  color='#202020',linewidth=.45,alpha=.65)
                ax.legend(handles=[Line2D([0],[0],color='#1776bc',lw=4,label='Numerical surface'),
                                   Line2D([0],[0],color='#202020',lw=.8,label='Exact mesh')],
                          loc='upper left',fontsize=9,frameon=False)
            else:
                exponent=int(np.floor(np.log10(max(float(z.max()),1e-300))))
                scale=10.**exponent
                ax.zaxis.set_major_formatter(FuncFormatter(lambda value,pos,s=scale:f'{value/s:g}'))
                ax.text2D(.83,.93,rf'$\times10^{{{exponent}}}$',transform=ax.transAxes,fontsize=10)
            ax.set(xlabel='$x$',ylabel='$y$',zlabel=f'${key}$' if col==0 else f'$e_{key}$',
                   xlim=(-30,30),ylim=(-30,30))
            ax.zaxis.set_rotate_label(False);ax.zaxis.label.set_rotation(0);ax.zaxis.labelpad=3
            ax.view_init(elev=29,azim=-58);ax.set_box_aspect((1.25,1,.85))
            for axis in (ax.xaxis,ax.yaxis,ax.zaxis):axis.set_major_locator(MaxNLocator(4))
            ax.tick_params(labelsize=9,pad=1)
            ax.set_title(f'{key}: numerical / exact overlay' if col==0 else rf'$|{key}_h-{key}_*|$',fontsize=13)
    fig.suptitle(f'Case {case} | '+('two solitons' if case=='C' else 'one soliton')+
        '\nSD2 + RK4, fixed mesh | t=0.01 | '+r'$\Delta x=0.15625,\ h=0.125$',fontsize=15)
    fig.savefig(HERE/f'case_{case}_comparison.png',dpi=175,bbox_inches='tight',pad_inches=.6)
    plt.close(fig);reports.append(r)
assert source_hash==hashlib.sha256(PATH.read_bytes()).hexdigest()
(HERE/'validation.json').write_text(json.dumps(dict(notebook_unchanged=True,
    source_sha256=source_hash,config=config,runs=reports,
    plot_definition='Numerical colored surface plus exact unshifted wire mesh; right column absolute error at the same x,y,t.',
    gsg_variables='Physical variables x,t; y,tau are transformed coordinates, not a second physical spatial dimension.'),indent=2),encoding='utf-8')
print('All cases complete',flush=True)
