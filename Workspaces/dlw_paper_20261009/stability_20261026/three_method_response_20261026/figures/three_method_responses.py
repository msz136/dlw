"""Plot actual native-grid response histories for the three DLW spatial methods.

Data input is the locally exported figure_curves.json alongside this script.
No smoothing, filtering, offsetting, or rescaling beyond the stated division
by the prescribed epsilon is applied to a trajectory.
"""
from pathlib import Path
import argparse
import hashlib
import json
import string
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, ScalarFormatter

HERE=Path(__file__).resolve().parent
CASES=['A','D','Gaussian','Sinusoidal']
NAMES={'A':'One-soliton','D':'Two-soliton','Gaussian':'Gaussian','Sinusoidal':'Sinusoidal'}
METHODS=['Endpoint-SD','Centered-SD','FD']
COLORS={'Endpoint-SD':'#2878B5','Centered-SD':'#E07A23','FD':'#299568'}
STYLES={'Endpoint-SD':'-','Centered-SD':(0,(5.0,2.5)),'FD':(0,(6.0,2.0,1.3,2.0))}
WIDTHS={'Endpoint-SD':1.8,'Centered-SD':1.8,'FD':1.65}
TICKS=[0,.0025,.005,.0075,.01]

plt.rcParams.update({
    'font.family':'DejaVu Serif','font.size':11.5,
    'mathtext.fontset':'dejavuserif','axes.titlesize':12,
    'axes.labelsize':12,'xtick.labelsize':10.5,'ytick.labelsize':10.5,
    'axes.linewidth':.65,'lines.dash_capstyle':'butt','lines.solid_capstyle':'round',
    'pdf.fonttype':42,'ps.fonttype':42,'savefig.facecolor':'white',
})

def load(require_all=True):
    data=json.loads((HERE/'figure_curves.json').read_text(encoding='utf-8'))
    curves={}
    for r in data['curves']:
        t=np.array(r['time'],dtype=float)
        y=np.array(r['max_normalized'],dtype=float)
        assert y.shape==(len(t),2) and np.isfinite(y).all()
        assert np.all(np.diff(t)>0) and t[0]==0 and t[-1]<=.0100000001
        curves[(r['case'],r['method'],r['input'])]=(t,y)
    if require_all:assert set(curves)=={(c,m,p) for c in CASES for m in METHODS for p in ['u','v']}
    return data,curves

def style_axis(ax,values,response,bottom=True):
    all_values=np.concatenate(values)
    lo,hi=float(all_values.min()),float(all_values.max())
    span=hi-lo
    if lo<.1*max(hi,1e-12):
        lo=0;hi=max(hi*1.08,1e-12)
    else:
        pad=max(.10*span,.002*max(hi,1))
        lo=max(0,lo-pad);hi+=pad
    ax.set_xlim(0,.01);ax.set_ylim(lo,hi)
    ax.set_xticks(TICKS)
    ax.set_xticklabels(['0','0.0025','0.005','0.0075','0.01'])
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4,min_n_ticks=3))
    fmt=ScalarFormatter(useMathText=True);fmt.set_powerlimits((-3,4));fmt.set_useOffset(False)
    ax.yaxis.set_major_formatter(fmt)
    ax.tick_params(direction='out',length=3.2,width=.6,pad=4)
    ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
    ax.grid(axis='y',color='#e5e7eb',linewidth=.45,zorder=0)
    ax.set_ylabel(r'$\|\delta '+response+r'_h(t)\|_\infty/\varepsilon$',labelpad=7)
    if bottom:ax.set_xlabel('$t$')
    else:ax.tick_params(axis='x',labelbottom=False)

def draw_panel(ax,curves,case,input_field,response_index,title,bottom):
    plotted=[]
    for method in METHODS:
        t,y=curves[(case,method,input_field)]
        line,=ax.plot(t,y[:,response_index],color=COLORS[method],linestyle=STYLES[method],
                     linewidth=WIDTHS[method],label=method,zorder=2+METHODS.index(method))
        assert np.array_equal(line.get_ydata(),y[:,response_index])
        plotted.append(y[:,response_index])
    style_axis(ax,plotted,['u','v'][response_index],bottom)
    ax.set_title(title,loc='left',pad=10)

def legend(fig,y=.965):
    handles=[Line2D([0],[0],color=COLORS[m],linestyle=STYLES[m],linewidth=WIDTHS[m],label=m) for m in METHODS]
    fig.legend(handles=handles,ncol=3,loc='upper center',bbox_to_anchor=(.52,y),
               frameon=False,handlelength=3.5,columnspacing=2.6,fontsize=11.5)

def save(fig,name):
    for suffix in ['png','pdf']:
        fig.savefig(HERE/(name+'.'+suffix),dpi=300,bbox_inches='tight',pad_inches=.10)
    plt.close(fig)

def primary(curves,component):
    fig,axes=plt.subplots(4,2,figsize=(10.4,12.5),sharex=True)
    fig.subplots_adjust(left=.105,right=.985,bottom=.055,top=.90,hspace=.43,wspace=.27)
    fig.suptitle(r'Initial perturbation in $'+component+r'$ only',x=.52,y=.995,fontsize=16)
    legend(fig,.97)
    for i,case in enumerate(CASES):
        for j,response in enumerate(['u','v']):
            letter=string.ascii_lowercase[2*i+j]
            draw_panel(axes[i,j],curves,case,component,j,
                       f'({letter}) {NAMES[case]}: $'+response+'$ response',i==3)
    save(fig,'response_'+component+'_input')

def overview(curves):
    fig,axes=plt.subplots(4,4,figsize=(18.0,12.6),sharex=True)
    fig.subplots_adjust(left=.065,right=.987,bottom=.055,top=.90,hspace=.43,wspace=.33)
    fig.suptitle('Independent initial perturbations: three spatial formulations',x=.52,y=.995,fontsize=17)
    legend(fig,.97)
    pairs=[('u',0),('u',1),('v',0),('v',1)]
    for i,case in enumerate(CASES):
        for j,(comp,response) in enumerate(pairs):
            letter=string.ascii_lowercase[4*i+j]
            title=f'({letter}) {NAMES[case]}: $'+comp+r'\to '+['u','v'][response]+'$'
            draw_panel(axes[i,j],curves,case,comp,response,title,i==3)
    save(fig,'response_overview')

def preview(case):
    data,curves=load(require_all=False)
    assert all((case,m,p) in curves for m in METHODS for p in ['u','v'])
    fig,axes=plt.subplots(2,2,figsize=(10.4,6.8),sharex=True)
    fig.subplots_adjust(left=.105,right=.985,bottom=.10,top=.79,hspace=.43,wspace=.27)
    fig.suptitle(NAMES[case]+' — independent initial perturbations',x=.52,y=.985,fontsize=15)
    legend(fig,.94)
    for i,component in enumerate(['u','v']):
        for j,response in enumerate(['u','v']):
            title='('+string.ascii_lowercase[2*i+j]+') $'+component+r'\to '+response+'$'
            draw_panel(axes[i,j],curves,case,component,j,title,i==1)
    save(fig,'preview_'+case)

def main(which='all'):
    data,curves=load()
    if which in ['all','u']:primary(curves,'u')
    if which in ['all','v']:primary(curves,'v')
    if which in ['all','overview']:overview(curves)
    outputs=[p for p in HERE.glob('response_*.png')]+[p for p in HERE.glob('response_*.pdf')]
    validation={'curve_count':len(curves),'source':data.get('source'),
                'normalization':data.get('normalization'),'time_range':[0,.01],
                'no_data_smoothing':True,'method_colors':COLORS,'three_distinct_line_styles':True,
                'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in outputs}}
    (HERE/'figure_validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
    print(json.dumps(validation,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--which',choices=['all','u','v','overview'],default='all')
    ap.add_argument('--preview-case',choices=CASES)
    args=ap.parse_args()
    if args.preview_case:preview(args.preview_case)
    else:main(args.which)
