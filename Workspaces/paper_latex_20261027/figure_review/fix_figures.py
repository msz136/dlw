"""Redraw from saved numerical arrays; no evolution, smoothing or value offsets.
Keep existing layouts/colors. Solid nested strokes replace interleaved DLW dashes.
2HS prescribed boundary zeros are excluded only from logarithmic error lines;
boundary-adjacent mesh cells are isolated points, never joined to interior cells.
"""
from pathlib import Path
import sys, json, hashlib, shutil, importlib.util
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgba
from matplotlib.ticker import MaxNLocator, ScalarFormatter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=HERE/'figures'; OUT.mkdir(exist_ok=True)
BACK=HERE/'before'; BACK.mkdir(exist_ok=True)
HS=ROOT/'Workspaces/hs_paper_20261026'
DLW=ROOT/'Workspaces/dlw_paper_20261009'
sys.path.insert(0,str(ROOT/'Workspaces/hs_numerics_plan'))
from hs_exact import Soliton

sources={}; checks={}; assets=[]

def crossed_overlap(ax,x,ys,colors,log=False):
    """Alternate colors only where their true polylines coincide on the page.
    Subdivision retains every native vertex and the original display geometry.
    Distance/ink change opacity only; isolated branches become fully solid.
    """
    x=np.asarray(x);ys=np.asarray(ys)
    xd=np.unique(np.r_[x,np.linspace(x[0],x[-1],2401)])
    transform=lambda a:np.log10(a) if log else a
    yt=np.array([np.interp(xd,x,transform(y)) for y in ys])
    mid=(yt[:,:-1]+yt[:,1:])/2
    ylim=transform(np.array(ax.get_ylim()))
    height_pt=ax.get_position().height*ax.figure.get_figheight()*72
    values_pt=(mid-ylim[0])*height_pt/(ylim[1]-ylim[0])
    xp=(xd[:-1]+xd[1:])/2
    width_pt=ax.get_position().width*ax.figure.get_figwidth()*72
    # Fixed phase tied to physical horizontal distance, never reset at a split.
    phase=(xp-x[0])/(x[-1]-x[0])*width_pt/12
    count=len(ys);alphas=np.ones_like(mid)
    def smooth(v):
        v=np.clip(v,0,1);return v*v*(3-2*v)
    for seg in range(len(xp)):
        dist=np.abs(values_pt[:,seg,None]-values_pt[None,:,seg]);np.fill_diagonal(dist,np.inf)
        # Connected overlap groups, with stable method order within each group.
        groups=[{i} for i in range(count)]
        for i in range(count):
            for j in range(i):
                if dist[i,j]<2.0:
                    a=next(g for g in groups if i in g);b=next(g for g in groups if j in g)
                    if a is not b:a.update(b);groups.remove(b)
        for group in groups:
            if len(group)==1:continue
            ordered=sorted(group)
            for rank,k in enumerate(ordered):
                local=(phase[seg]*len(group)-rank)%len(group)
                ink=float(0<=local<1)
                fill=float(smooth((dist[k].min()-.7)/1.3))
                alphas[k,seg]=ink+(1-ink)*fill
    for k,y in enumerate(ys):
        yd=10**yt[k] if log else yt[k]
        pts=np.column_stack([xd,yd]);segments=np.stack([pts[:-1],pts[1:]],axis=1)
        rgba=np.tile(to_rgba(colors[k]),(len(segments),1));rgba[:,3]=alphas[k]
        ax.add_collection(LineCollection(segments,colors=rgba,linewidths=1.25,capstyle='round',zorder=3+k))
        native=np.searchsorted(xd,x)
        assert np.allclose(yd[native],y,rtol=2e-14,atol=0)
    return {'native_vertices_preserved':True,'data_offsets':False,'solid_if_separated_by_pt':2.0,'crossed_if_within_pt':.7}
def data(path):
    sources[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return np.load(path)

def finish(fig,paper,number):
    stem=f'{paper}-figure-{number:02d}'
    for ext in ['png','pdf']:
        fig.savefig(OUT/f'{stem}.{ext}',dpi=300,bbox_inches='tight',pad_inches=.06)
    dest=ROOT/f'pdf/{paper}/images/figure-{number:02d}.pdf'
    shutil.copy2(OUT/f'{stem}.pdf',dest)
    assets.append({'paper':paper,'number':number,'source':str((OUT/f'{stem}.pdf').relative_to(ROOT)),
                   'file':f'images/figure-{number:02d}.pdf','sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    plt.close(fig)

def dlw_response():
    plt.rcParams.update({'font.family':'DejaVu Sans','mathtext.fontset':'dejavusans','font.size':9,
        'axes.labelsize':9,'axes.titlesize':9,'xtick.labelsize':8,'ytick.labelsize':8,
        'axes.linewidth':.65,'axes.grid':False,'pdf.fonttype':42})
    colors=['#2878B5','#E07A23','#299568']; names=['Endpoint-SD','Centered-SD','FD']; widths=[1.25]*3
    for case,num in [('A',13),('D',14)]:
        d=data(DLW/f'stability_20261026/three_method_response_20261026/native/{case}.npz')
        t=d['t'];y=d['response_normalized'];assert np.all(np.diff(t)>0)
        fig,axs=plt.subplots(2,2,figsize=(7.1,4.4))
        fig.subplots_adjust(left=.10,right=.98,bottom=.11,top=.85,hspace=.55,wspace=.33)
        fig.legend(handles=[Line2D([0],[0],color=c,lw=w,label=n) for c,w,n in zip(colors,widths,names)],
            loc='upper center',bbox_to_anchor=(.53,.99),ncol=3,frameon=False,handlelength=3,columnspacing=2)
        for i in range(2):
            for j in range(2):
                ax=axs[i,j]
                lo,hi=y[:,:,i,j].min(),y[:,:,i,j].max();pad=max((hi-lo)*.12,.0003)
                ax.set_ylim(max(0,lo-pad),hi+pad);ax.set_xlim(0,.01)
                stroke=crossed_overlap(ax,t,y[:,:,i,j].T,colors)
                ax.set_xticks([0,.005,.01],['0','0.005','0.01']);ax.yaxis.set_major_locator(MaxNLocator(4))
                fmt=ScalarFormatter(useMathText=True);fmt.set_useOffset(False);ax.yaxis.set_major_formatter(fmt)
                ax.set_xlabel('$t$',labelpad=2);ax.set_ylabel(r'$\|\delta '+['u','v'][j]+r'_h\|_\infty/\varepsilon$',labelpad=5)
                ax.set_title('('+chr(97+2*i+j)+') '+['$u_0$ perturbed','$v_0$ perturbed'][i]+r': $'+['u','v'][j]+'$ response',loc='left',pad=6)
                ax.spines[['right','top']].set_visible(False);ax.tick_params(direction='out',width=.6,length=3)
        checks[f'dlw_{num}']={'terminal_panel_d':y[-1,:,1,1].tolist(),'unchanged_values':True,'stroke':stroke}
        finish(fig,'dlw',num)

def dlw_time():
    spec=importlib.util.spec_from_file_location('history',DLW/'time_samm_20261025/figures/plot_time_history.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    for field,num in [('u',9),('v',10)]:
        fig,axes=plt.subplots(2,2,figsize=(7,4.75),sharex=True);term={}
        fig.subplots_adjust(left=.095,right=.985,bottom=.105,top=.865,hspace=.40,wspace=.245)
        for k,(ax,case) in enumerate(zip(axes.ravel(),mod.CASES)):
            d=data(mod.SRC/f'{case}_time.npz');t=d['t'][1:];assert np.all(np.diff(t)>0)
            vals=[];handles=[]
            for order,(key,label,color,*_) in enumerate(mod.METHODS):
                e=d['errors_'+key][1:,0 if field=='u' else 1];assert np.all(e>0)
                vals.append(e);handles.append(Line2D([0],[0],color=color,lw=1.25,label=label))
            mod.style(ax,np.min(vals)/1.7,np.max(vals)*1.9);ax.set_title(f'({chr(97+k)}) {mod.TITLES[case]}',pad=6)
            stroke=crossed_overlap(ax,t,vals,[item[2] for item in mod.METHODS],log=True)
            term[case]=[float(v[-1]) for v in vals]
        for ax in axes[:,0]:ax.set_ylabel(rf'$E_{field}(t)$')
        for ax in axes[1,:]:ax.set_xlabel('$t$')
        fig.legend(handles=handles,loc='upper center',ncol=3,bbox_to_anchor=(.5,1.005),frameon=False)
        fig.subplots_adjust(left=.095,right=.985,bottom=.105,top=.865,hspace=.40,wspace=.245)
        checks[f'dlw_{num}']={'terminal_values_Euler_RK4_CN':term,'unchanged_values':True,'stroke':stroke}
        finish(fig,'dlw',num)

def hs_spatial():
    plt.rcParams.update({'font.family':'DejaVu Sans','mathtext.fontset':'dejavusans','font.size':10,'axes.spines.top':False,
        'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,'lines.linewidth':1.6})
    d=data(HS/'data/case_figures.npz');colors=['#2878B5','#E47C25']
    for ci,p in enumerate([(5.,),(1.1,1.25)]):
        ref=Soliton(p);fig,ax=plt.subplots(2,2,figsize=(9,5.4),layout='constrained');stats=[]
        for j,q in enumerate(['u','rho']):
            lows=[];highs=[]
            for mi,kind in enumerate(['sd','fixed']):
                x=d[f'{ci}_{kind}_{q}_x'];v=d[f'{ci}_{kind}_{q}'];e=abs(d[f'{ci}_{kind}_{q}_error'])
                assert np.isfinite(x).all() and np.all(np.diff(x)>0) and len(x)==len(v)==len(e)
                ax[0,j].plot(x[::12],v[::12],ls='none',marker=['o','s'][mi],mfc='none',ms=3,color=colors[mi],label=['Integrable SD','FD'][mi])
                mask=np.ones(len(x),dtype=bool)
                if kind=='fixed':mask[[0,-1]]=False
                elif q=='u':mask[0]=False # Prescribed left velocity trace.
                mask &= e>0
                plotted=np.where(mask,e,np.nan)
                line,=ax[1,j].plot(x,plotted,color=colors[mi],ls=['-','--'][mi])
                assert np.array_equal(line.get_ydata()[mask],e[mask])
                ax[1,j].set_yscale('log',nonpositive='mask')
                lows.append(float(e[mask].min()));highs.append(float(e[mask].max()))
                stats.append({'method':kind,'field':q,'min_dx':float(np.diff(x).min()),'omitted_boundary_indices':np.flatnonzero(~mask).tolist(),'remaining_values_exact':True})
            xref=np.linspace(min(d[f'{ci}_sd_u_x'][0],-4),max(d[f'{ci}_sd_u_x'][-1],4),1401)
            ax[0,j].plot(xref,ref.continuous_x(xref,.125)[j],'k-',lw=1,label='Continuous exact',zorder=0)
            ax[0,j].set(xlabel='$x$',ylabel=['$u$',r'$\rho$'][j]);ax[1,j].set(xlabel='$x$',ylabel='Absolute error',ylim=(min(lows)/2,max(highs)*2))
        ax[0,0].legend(fontsize=8);checks[f'2hs_{ci+3}']=stats;finish(fig,'2hs',ci+3)

def hs_mesh():
    d=data(HS/'data/conserved_mesh.npz')
    for ci in [0,1]:
        fig,ax=plt.subplots(1,3,figsize=(11,3.2),layout='constrained');stats=[]
        for mi in [0,1]:
            x=d[f'{ci}_{mi}_x'];assert np.all(np.diff(x)>0)
            mid=(x[1:]+x[:-1])/2;width=np.diff(x);color=['#2878b5','#e78123'][mi];ls=['-','--'][mi]
            ax[0].plot(mid[1:-1],width[1:-1],color=color,ls=ls,label=['Fixed FD','Conserved-density moving FD'][mi])
            ax[0].plot(mid[[0,-1]],width[[0,-1]],linestyle='none',marker='o',ms=3,mfc='white',mec=color)
            mask=abs(x)<=2.5
            for j,key in [(1,'eu'),(2,'er')]:
                e=d[f'{ci}_{mi}_{key}'];line,=ax[j].plot(x[mask],e[mask],color=color,ls=ls,lw=1.5)
                assert np.array_equal(line.get_ydata(),e[mask])
            stats.append({'method':mi,'min_dx':float(width.min()),'all_cell_widths_retained':True,'isolated_boundary_cells':[0,len(width)-1],'errors_unchanged':True})
        for j in range(3):
            ax[j].set(xlabel='$x$',ylabel=['Cell width',r'$|u_h-u_*|$',r'$|\rho_h-\rho_*|$'][j])
            if j:ax[j].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
        fig.legend(loc='outside upper center',ncol=2,frameon=False,fontsize=9)
        checks[f'2hs_{ci+7}']=stats;finish(fig,'2hs',ci+7)

if __name__=='__main__':
    for paper,nums in [('dlw',[9,10,13,14]),('2hs',[3,4,7,8])]:
        folder=BACK/paper;folder.mkdir(exist_ok=True)
        for path in [ROOT/f'pdf/{paper}/main.tex',ROOT/f'pdf/{paper}/main.pdf']+[ROOT/f'pdf/{paper}/images/figure-{n:02d}.pdf' for n in nums]:
            if not (folder/path.name).exists():shutil.copy2(path,folder/path.name)
    dlw_response();dlw_time();hs_spatial();hs_mesh()
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in sources.items())
    (HERE/'redraw_validation.json').write_text(json.dumps({'source_sha256':sources,'checks':checks,'assets':assets,'raw_data_unchanged':True},indent=2),encoding='utf-8')
    print('Redrew 8 figures; all plotted numerical ordinates verified against original data.')


