"""Main-paper heatmap repair, 2026-10-25.
Derived from ../plot_figures.py. Only final comparison figures are rendered.
Read saved arrays and CSV maxima; no solver or reference evaluator is imported.
Original layouts, sections, native sites and shared logarithmic limits retained.
"""
"""Four actual cases. Exact sections use lines, numerical sections markers;
error curves join every computed x sample, without fitting or smoothing.
Each comparison includes native two-dimensional error maps of all methods.
"""
from pathlib import Path
import sys,json,hashlib,argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import MaxNLocator,ScalarFormatter,LogLocator,NullFormatter

HERE=Path(__file__).resolve().parent
OLD=HERE.parents[1]/'report_refresh_20261024/natural_selection_20261025/figures'
OUT=HERE/'figures';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(OLD))
from plot_comparisons import max_table
CASES=['A','D','Gaussian','Sinusoidal']
LABELS={'A':'One-soliton case','D':'Two-soliton case','Gaussian':'Gaussian case','Sinusoidal':'Sinusoidal case'}
SLICE={'A':(-5,5),'D':(-8,8),'Gaussian':(-18,18),'Sinusoidal':(-12,12)}
MAP={'A':(-5,5),'D':(-30,30),'Gaussian':(-18,18),'Sinusoidal':(-12,12)}
METHODS=[('endpoint','Endpoint-SD','#2878B5','o'),('centered','Centered-SD','#E07A23','s'),('fd','FD','#299568','^')]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':10,
 'axes.titlesize':10,'xtick.labelsize':9,'ytick.labelsize':9,'axes.linewidth':.65,
 'xtick.direction':'out','ytick.direction':'out','pdf.fonttype':42,'ps.fonttype':42,
 'savefig.facecolor':'white','figure.facecolor':'white','axes.facecolor':'white'})

def sci(z):
    a,b=f'{z:.2e}'.split('e');return a+r'\times10^{'+str(int(b))+'}'

def axes_style(ax,log=False):
    ax.tick_params(length=3,pad=3)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    if not log:
        fm=ScalarFormatter(useMathText=True);fm.set_useOffset(False);fm.set_powerlimits((-3,3))
        ax.yaxis.set_major_formatter(fm);ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    else:
        ax.yaxis.set_major_locator(LogLocator(base=10,numticks=4))
        ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(axis='y',which='major',color='#e5e7eb',lw=.45,zorder=0)

def marker_indices(x,limits,method):
    available=np.flatnonzero((x>=limits[0])&(x<=limits[1]))
    n=min(33,len(available));k=np.arange(n)
    jitter=((k*((np.sqrt(5)-1)/2)+.17*method)%1)-.5
    pos=(k+.5+.35*jitter+.25*(method-1))*len(available)/n
    return available[np.unique(np.clip(np.rint(pos).astype(int),0,len(available)-1))]

def finish(fig,stem,meta):
    png=OUT/(stem+'.png');pdf=OUT/(stem+'.pdf')
    fig.savefig(png,dpi=300,bbox_inches='tight',pad_inches=.08)
    fig.savefig(pdf,dpi=300,bbox_inches='tight',pad_inches=.08)
    plt.close(fig)
    meta.update(png=png.name,pdf=pdf.name,png_sha256=hashlib.sha256(png.read_bytes()).hexdigest(),pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest())
    (OUT/(stem+'.py')).write_text("import sys\nfrom pathlib import Path\nsys.path.insert(0,str(Path(__file__).resolve().parent.parent))\nfrom plot_figures import make\nmake("+repr(meta['case'])+","+repr(meta['stage'])+")\n",encoding='utf-8')
    return meta

def make(case,stage='final'):
    if stage=='exact':return exact(case)
    initial=stage=='rate';table=max_table(stage)
    path=OLD/'data'/(case+'.npz')
    d=np.load(path);x=d['x'];xd=d['line_x']
    fig=plt.figure(figsize=(11.5,10.7))
    grid=fig.add_gridspec(4,8,left=.080,right=.895,bottom=.055,top=.895,hspace=.68,wspace=.95,height_ratios=[1,1,.96,.96])
    legends=[];labs=[];curves=[];maps=[]
    for row,q in enumerate(['u','v']):
        ax=fig.add_subplot(grid[row,:4]);err=fig.add_subplot(grid[row,4:])
        symmetry=case in ['Gaussian','Sinusoidal'] and q=='v'
        f=q+'_t' if initial else q
        ref=d[f'exact_line_{stage}_{q}']
        black,=ax.plot(xd,ref,color='#181818',lw=1.25,zorder=2)
        if row==0:legends.append(black);labs.append('Continuous reference')
        all_error=[]
        for i,(prefix,name,color,marker) in enumerate(METHODS):
            idx=marker_indices(x,SLICE[case],i)
            vals=d[f'{prefix}_line_{stage}_{q}']
            art,=ax.plot(x[idx],vals[idx],ls='none',marker=marker,ms=4.3,mfc='none',mec=color,mew=.85,zorder=3)
            if row==0:legends.append(art);labs.append(name)
            e=abs(d[f'{prefix}_line_error_{stage}_{q}'])
            line,=err.plot(x,e,color=color,lw=1.25,ls=('--' if prefix=='fe' else '-'),marker=None,zorder=3)
            assert line.get_marker() in [None,'None','']
            all_error.append(e[(x>=SLICE[case][0])&(x<=SLICE[case][1])])
            curves.append(dict(field=q,method=name,maximum=float(e.max()),marker=False,all_x_points=len(x),source_key=f'{prefix}_line_error_{stage}_{q}'))
        ax.set_title('('+chr(97+2*row)+') $'+f+'$ at $y=0$',loc='left',pad=10)
        err.set_title('('+chr(98+2*row)+') Section error at $y=0$',loc='left',pad=10)
        ax.set_ylabel('$'+f+'$');err.set_ylabel('$|{'+f+r'}_h-{'+f+r'}^*|$')
        for aa in [ax,err]:aa.set_xlim(SLICE[case]);aa.set_xlabel('$x$')
        axes_style(ax)
        if symmetry:
            base=0 if initial else 4
            ax.set_ylim(base-.005,base+.005)
            ax.text(.04,.86,'Central reference: $'+f+('=0$' if initial else '=4$'),transform=ax.transAxes,fontsize=9)
            peak=max(float(e.max()) for e in all_error)
            err.set_ylim(0,max(1e-15,peak*1.5));axes_style(err)
            err.text(.04,.83,'Section maximum $'+sci(peak)+'$',transform=err.transAxes,fontsize=8.4)
        else:
            err.set_yscale('log')
            peak=max(float(e.max()) for e in all_error)
            positive=np.concatenate(all_error);positive=positive[positive>0]
            lower=max(peak*1e-5,float(np.quantile(positive,.025)))
            err.set_ylim(lower,peak*1.8);axes_style(err,True)
    # A single logarithmic color range per physical component across methods.
    crop=(x>=MAP[case][0])&(x<=MAP[case][1]);xx=x[crop]
    cmap=plt.get_cmap('viridis').copy();cmap.set_under(cmap(0.0))
    for row,q in enumerate(['u','v']):
        vmax=max(table[case,name,q] for _,name,_,_ in METHODS)
        vmin=max(vmax*1e-4,1e-13)
        norm=LogNorm(vmin=vmin,vmax=vmax,clip=True)
        for i,(prefix,name,color,marker) in enumerate(METHODS):
            ax=fig.add_subplot(grid[row+2,2*i:2*i+2])
            yy=d[f'{prefix}_y_{q}'];z=abs(d[f'{prefix}_error_{stage}_{q}'])[:,crop]
            im=ax.pcolormesh(xx,yy,z,cmap=cmap,norm=norm,shading='auto',rasterized=True)
            ax.axhline(0,color='white',lw=.7,ls='--',alpha=.85)
            ax.set_xlim(MAP[case]);ax.set_ylim(float(yy.min()),float(yy.max()))
            ax.set_xlabel('$x$')
            if i==0:ax.set_ylabel('$y$')
            ax.set_title('('+chr(101+4*row+i)+') '+name+'\n$E_{'+('u_t' if initial and q=='u' else 'v_t' if initial else q)+r',\infty}='+sci(table[case,name,q])+'$',loc='left',fontsize=9,pad=9)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=4));ax.yaxis.set_major_locator(MaxNLocator(nbins=4));ax.tick_params(length=3,pad=3)
            maps.append(dict(field=q,method=name,vmin=vmin,vmax=vmax,native=True,source_key=f'{prefix}_error_{stage}_{q}',below_color_minimum=int(np.sum(z<vmin)),zero_values=int(np.sum(z==0)),low_end_policy='clip to lowest viridis color, including zero',lower_color_rgba=list(cmap(0.0)),colorbar_threshold_label='<= '+format(vmin,'.2e')))
        box=ax.get_position();cax=fig.add_axes([.916,box.y0,.014,box.height])
        cb=fig.colorbar(im,cax=cax,extend='min',format=matplotlib.ticker.LogFormatterMathtext())
        # All finite errors at or below the threshold (including exact zero)
        # share the lowest viridis color. Source errors are never modified.
        exponents=np.arange(np.ceil(np.log10(vmin)),np.floor(np.log10(vmax))+1)
        decades=10.**exponents
        ticks=[vmin]+[float(t) for t in decades if t>vmin*(1+1e-10)]
        # Avoid a near-duplicate decade label immediately above the threshold.
        if len(ticks)>1 and np.log10(ticks[1]/vmin)<.35:
            ticks.pop(1)
        formatter=matplotlib.ticker.LogFormatterMathtext()
        labels=[r'$\leq '+sci(vmin)+'$']+[formatter(t) for t in ticks[1:]]
        cb.set_ticks(ticks,labels=labels)
        cb.ax.minorticks_off();cb.ax.tick_params(labelsize=8,length=3)
        cb.set_label('$|{'+(q+'_t' if initial else q)+r'}_h-{'+(q+'_t' if initial else q)+r'}^*|$',fontsize=9)
    fig.suptitle(LABELS[case]+('  |  Initial time derivatives' if initial else '  |  $T=0.01$'),fontsize=12,y=.985)
    fig.legend(legends,labs,loc='upper center',bbox_to_anchor=(.5,.962),ncol=5,frameon=False,fontsize=9,columnspacing=1.1,handlelength=1.5)
    stem=('initial_' if initial else 'spatial_')+case
    meta=dict(case=case,label=LABELS[case],stage=stage,section_y=0,section_xlim=SLICE[case],heatmap_xlim=MAP[case],section_error='absolute y=0 section error; all native x samples connected',color_scale='logarithmic, common per component across methods; values at or below vmin share the lowest viridis color, including zero; threshold labeled <= vmin',curves=curves,maps=maps,source=str(path),source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    return finish(fig,stem,meta)

def exact(case):
    d=np.load(OLD/'data'/(case+'.npz'))
    x=d['x'];xd=d['line_x'];yy=d['exact_initial_y']
    # Use the stored exact fields and lines already checked in the source figure pipeline.
    fig,axs=plt.subplots(2,2,figsize=(9.8,5.8),gridspec_kw={'width_ratios':[1,1.06]})
    fig.subplots_adjust(left=.08,right=.93,bottom=.09,top=.89,hspace=.5,wspace=.38)
    crop=(x>=MAP[case][0])&(x<=MAP[case][1])
    for row,q in enumerate(['u','v']):
        ax,hm=axs[row];z=d[f'exact_initial_{q}'];ref=d[f'exact_line_initial_{q}']
        ax.plot(xd,ref,color='#181818',lw=1.3);ax.set(xlim=SLICE[case],xlabel='$x$',ylabel='$'+q+'$')
        ax.set_title('('+chr(97+2*row)+') $'+q+'(x,0,0)$',loc='left');axes_style(ax)
        if q=='v' and case in ['Gaussian','Sinusoidal']:
            ax.set_ylim(3.995,4.005);ax.text(.04,.85,'Central section: $v=4$',transform=ax.transAxes,fontsize=9)
        im=hm.pcolormesh(x[crop],yy,z[:,crop],shading='auto',cmap='viridis',rasterized=True)
        hm.axhline(0,color='white',ls='--',lw=.8)
        hm.set(xlim=MAP[case],xlabel='$x$',ylabel='$y$');hm.set_title('('+chr(98+2*row)+') $'+q+'(x,y,0)$',loc='left')
        hm.xaxis.set_major_locator(MaxNLocator(4));hm.yaxis.set_major_locator(MaxNLocator(4))
        cb=fig.colorbar(im,ax=hm,pad=.025,fraction=.045);cb.ax.tick_params(labelsize=8)
    fig.suptitle(LABELS[case]+'  |  Exact initial fields',fontsize=12,y=.98)
    return finish(fig,'exact_'+case,dict(case=case,label=LABELS[case],stage='exact',section_xlim=SLICE[case],heatmap_xlim=MAP[case],source='previously verified exact initial arrays'))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('cases',nargs='*');args=ap.parse_args();entries=[]
    for c in args.cases or CASES:
        for stage in ['final']:
            entries.append(make(c,stage));print('Rendered',c,stage,flush=True)
    p=OUT/'manifest.json';old=json.loads(p.read_text(encoding='utf-8')) if p.exists() else []
    old=[e for e in old if e['case'] not in (args.cases or CASES)]+entries
    p.write_text(json.dumps(old,indent=2),encoding='utf-8')
if __name__=='__main__':main()
