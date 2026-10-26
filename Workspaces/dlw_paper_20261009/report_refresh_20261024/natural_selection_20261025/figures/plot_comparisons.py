"""Paper figures for the selected three spatial formulations.

Real computed fields are loaded from data/{case}.npz, prepared by figure_data.py.
The two current report CSVs supply the complete-region maximum errors.
Numerical markers are thinned for display only; source arrays are unchanged.
Style: selected ESD reference esd-14.png, two field rows, white background,
Matplotlib blue/orange/green, black exact profile, shared linear viridis scales.
"""
from pathlib import Path
import argparse,csv,hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator,ScalarFormatter

HERE=Path(__file__).resolve().parent
REPORT=HERE.parent.parent
CASES=['A','B','C','D','Gaussian','Sinusoidal']
METHODS=[('endpoint','Endpoint-SD','#1f77b4','o'),('centered','Centered-SD','#ff7f0e','s'),('fd','FD','#2ca02c','^')]
TITLES={'A':'Case A: one soliton','B':'Case B: one soliton','C':'Case C: two solitons','D':'Case D: two solitons','Gaussian':'Periodic Gaussian','Sinusoidal':'Sinusoidal wave'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.labelsize':11,
    'axes.titlesize':11,'legend.fontsize':10,'xtick.labelsize':10,'ytick.labelsize':10,
    'axes.linewidth':.65,'xtick.major.width':.65,'ytick.major.width':.65,
    'xtick.direction':'out','ytick.direction':'out','axes.grid':False,
    'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white',
    'pdf.fonttype':42,'ps.fonttype':42,'mathtext.fontset':'dejavusans'})


def max_table(stage):
    name='table1_initial_derivative_errors.csv' if stage=='rate' else 'table2_final_field_errors.csv'
    rows=list(csv.DictReader((REPORT/name).open(encoding='utf-8-sig')))
    mk='method' if stage=='rate' else 'space'
    keys=['error_ut','error_vt'] if stage=='rate' else ['error_u','error_v']
    return {(r['case'],r[mk],q):float(r[k]) for r in rows for q,k in zip(['u','v'],keys)}


def sci(value):
    if value==0:return '0'
    m,e=f'{value:.3e}'.split('e')
    return rf'{m}\times10^{{{int(e)}}}'


def sfmt(ax):
    fm=ScalarFormatter(useMathText=True);fm.set_powerlimits((-3,3));fm.set_useOffset(False)
    ax.yaxis.set_major_formatter(fm)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))
    for spine in ax.spines.values():spine.set_linewidth(.65)
    ax.tick_params(length=3.0,pad=3)


def marks(n,im):
    count=min(54,n)
    i=np.arange(count)
    # Quasi-uniform stratified sampling avoids selecting only one parity of
    # an oscillatory numerical mode when a regular marker stride is even.
    golden=(np.sqrt(5)-1)/2
    jitter=((i*golden+.17*im)%1)-.5
    target=(i+.5+.45*jitter+.24*(im-1))*n/count
    return np.unique(np.clip(np.rint(target).astype(int),0,n-1))


def save(fig,stem,title):
    png=HERE/(stem+'.png');pdf=HERE/(stem+'.pdf')
    fig.savefig(png,dpi=300,bbox_inches='tight',pad_inches=.08)
    fig.savefig(pdf,bbox_inches='tight',pad_inches=.08,metadata={'Title':title,'Creator':'Matplotlib'})
    plt.close(fig)
    return {'png':png.name,'pdf':pdf.name,'png_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}


def slices(case,data,stage,table):
    initial=stage=='rate'
    stem=('initial_'+case+'_rates') if initial else ('final_'+case+'_sections')
    fig,axes=plt.subplots(2,2,figsize=(10,6.5))
    fig.subplots_adjust(left=.092,right=.974,bottom=.09,top=.855,wspace=.29,hspace=.43)
    x=np.asarray(data['x']);xd=np.asarray(data['line_x'])
    legend=[];labels=[];indices={}
    for iq,q in enumerate(['u','v']):
        ax,er=axes[iq]
        shift=4 if (not initial and case in ['Gaussian','Sinusoidal'] and q=='v') else 0
        exact=np.asarray(data[f'exact_line_{stage}_{q}'])-shift
        line,=ax.plot(xd,exact,color='black',lw=1.15,zorder=2,label='Continuous reference')
        if iq==0:legend.append(line);labels.append('Continuous reference')
        for im,(prefix,name,color,marker) in enumerate(METHODS):
            idx=marks(len(x),im);indices[prefix]=idx.tolist()
            values=np.asarray(data[f'{prefix}_line_{stage}_{q}'])-shift
            error=abs(np.asarray(data[f'{prefix}_line_error_{stage}_{q}']))
            assert len(values)==len(x)==len(error)
            art,=ax.plot(x[idx],values[idx],linestyle='none',marker=marker,markersize=4.6,
                markerfacecolor='none',markeredgecolor=color,markeredgewidth=.9,color=color,zorder=3,label=name)
            er.plot(x[idx],error[idx],linestyle='none',marker=marker,markersize=4.2,
                markerfacecolor='none',markeredgecolor=color,markeredgewidth=.85,color=color)
            if iq==0:legend.append(art);labels.append(name)
        field=q+'_t' if initial else q
        ax.set_ylabel('$'+field+('-4' if shift else '')+'$')
        er.set_ylabel('$|'+field+r'^{\mathrm{num}}-'+field+r'^{*}|$')
        ax.set_title(f'({chr(97+iq*2)}) '+('$'+field+('-4' if shift else '')+'$')+' at $y=0$',loc='left',pad=11)
        er.set_title(f'({chr(98+iq*2)}) Absolute section error',loc='left',pad=11)
        for aa in (ax,er):
            aa.set_xlim(float(x[0]),float(x[-1]));aa.set_xlabel('$x$');sfmt(aa)
        er.set_ylim(bottom=0)
        if q=='v' and case in ['Gaussian','Sinusoidal']:
            native_scale=max(table[case,name,q] for _,name,_,_ in METHODS)
            ax.set_ylim(-1.05*native_scale,1.05*native_scale)
            er.set_ylim(0,1.05*native_scale)
    labeltime='$t=0$' if initial else '$T=0.01$'
    fig.suptitle(TITLES[case]+'  |  '+labeltime,fontsize=12,y=.995)
    fig.legend(legend,labels,loc='upper center',bbox_to_anchor=(.5,.962),ncol=4,frameon=False,
               columnspacing=1.5,handletextpad=.5,handlelength=1.8)
    title=TITLES[case]+(': initial time-derivative sections' if initial else ': final physical-field sections')
    info=save(fig,stem,title)
    what='initial time derivatives' if initial else 'physical fields at T=0.01'
    caption=f'{TITLES[case]}. Sections of the {what} at y=0. The black curve is the continuous reference; open circles, squares and triangles show Endpoint-SD, Centered-SD and FD. The right column gives the absolute errors of the same reconstructed sections. Numerical sections are reconstructed from native field values; the comparison data retain all grid points.'
    if not initial and case in ['Gaussian','Sinusoidal']:
        caption+=' The lower-left panel shows v-4; the continuous reference satisfies v(x,0,t)=4.'
    if case in ['Gaussian','Sinusoidal']:
        caption+=' The exact central v equals 4 (v_t=0 initially); the full-region field-error scale is used for this symmetry-line panel and its error panel.'
        caption+=' The display window is -24<=x<=24; tabulated maxima use the full periodic x domain.'
    info.update(case=case,kind=('initial_rates' if initial else 'final_sections'),caption=caption,
        x_display=[float(x[0]),float(x[-1])],section_y=0,marker_indices=indices,
        marker_only=True,maximum_marker_count=max(len(i) for i in indices.values()),
        background_subtracted_lower_left=(not initial and case in ['Gaussian','Sinusoidal']))
    return info


def heatmaps(case,data,stage,table):
    initial=stage=='rate';stem=('initial_' if initial else 'final_')+case+'_errors'
    fig,axes=plt.subplots(2,3,figsize=(11.4,6.5))
    fig.subplots_adjust(left=.068,right=.875,bottom=.09,top=.86,wspace=.23,hspace=.43)
    x=np.asarray(data['x']);limits={};maxima={}
    for iq,q in enumerate(['u','v']):
        vmax=max(table[case,name,q] for _,name,_,_ in METHODS);limits[q]=[0,vmax]
        norm=Normalize(0,vmax)
        image=None
        for im,(prefix,name,_,_) in enumerate(METHODS):
            ax=axes[iq,im]
            y=np.asarray(data[f'{prefix}_y_{q}']);z=abs(np.asarray(data[f'{prefix}_error_{stage}_{q}']))
            assert z.shape==(len(y),len(x)),(case,prefix,q,z.shape,len(y),len(x))
            maximum=table[case,name,q];maxima[f'{prefix}_{q}']=maximum
            assert np.max(z)<=maximum+1e-14,(case,name,q,float(np.max(z)),maximum)
            image=ax.pcolormesh(x,y,z,shading='auto',cmap='viridis',norm=norm,rasterized=True)
            ax.set_title(f'({chr(97+iq*3+im)}) {name}\n$E_\\infty={sci(maximum)}$',fontsize=10.5,pad=8)
            ax.set_xlim(float(x[0]),float(x[-1]))
            all_y=np.concatenate([data[f'{p}_y_{q}'] for p,_,_,_ in METHODS])
            dy=np.min(np.diff(np.unique(np.round(all_y,12))))
            pad=.05 if case in ['Gaussian','Sinusoidal'] else .05
            # Show each method at its own native coordinates within a common row extent.
            ax.set_ylim(float(np.min(all_y)-pad),float(np.max(all_y)+pad))
            ax.set_xlabel('$x$')
            if im==0:ax.set_ylabel('$y$')
            ax.xaxis.set_major_locator(MaxNLocator(nbins=4));ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
            ax.tick_params(length=3,pad=3)
        pos=axes[iq,-1].get_position()
        cax=fig.add_axes([.897,pos.y0,.016,pos.height])
        fm=ScalarFormatter(useMathText=True);fm.set_powerlimits((-3,3))
        cb=fig.colorbar(image,cax=cax,format=fm)
        cb.ax.tick_params(labelsize=9,length=3,width=.65)
        cb.outline.set_linewidth(.65)
        f=q+'_t' if initial else q
        cb.set_label('$|'+f+r'^{\mathrm{num}}-'+f+r'^{*}|$',fontsize=10,labelpad=9)
    title=TITLES[case]+('  |  Initial time-derivative errors' if initial else '  |  Field errors at $T=0.01$')
    fig.suptitle(title,fontsize=12,y=.985)
    info=save(fig,stem,title.replace('$',''))
    caption=f'{TITLES[case]}. Absolute '+('initial time-derivative errors' if initial else 'physical-field errors at T=0.01')+' for Endpoint-SD, Centered-SD and FD. Rows show the u and v components at their native field positions. Each row uses one shared linear colour scale. Panel labels report the maximum over the complete table region.'
    if case in ['Gaussian','Sinusoidal']:caption+=' The displayed x window is [-24,24]; the table region contains the full periodic x interval [-96,96).'
    info.update(case=case,kind=('initial_errors' if initial else 'final_errors'),caption=caption,
        x_display=[float(x[0]),float(x[-1])],color_scale='linear',color_limits=limits,
        table_maxima=maxima,native_positions=True)
    return info


def main():
    ap=argparse.ArgumentParser();ap.add_argument('cases',nargs='*',default=CASES);args=ap.parse_args()
    cases=args.cases or CASES
    rtab=max_table('rate');ftab=max_table('final')
    entries=[]
    for case in cases:
        path=HERE/'data'/f'{case}.npz'
        with np.load(path) as data:
            entries.extend([slices(case,data,'final',ftab),heatmaps(case,data,'final',ftab),
                            slices(case,data,'rate',rtab),heatmaps(case,data,'rate',rtab)])
        for info in entries[-4:]:
            stem=info['png'][:-4]
            mode='rate' if info['kind'].startswith('initial') else 'final'
            func='heatmaps' if info['kind'].endswith('errors') else 'slices'
            source=(f'from plot_comparisons import *\n\n'
                    f'if __name__ == "__main__":\n'
                    f'    with np.load(HERE/"data"/"{case}.npz") as data:\n'
                    f'        {func}("{case}",data,"{mode}",max_table("{mode}"))\n')
            (HERE/(stem+'.py')).write_text(source,encoding='utf8')
            info['script']=stem+'.py'
            info['data']=str(path.relative_to(HERE))
            info['data_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        print('Rendered',case,flush=True)
    manifest=HERE/'comparison_figure_manifest.json'
    old=json.loads(manifest.read_text(encoding='utf8')) if manifest.exists() else {'figures':[]}
    old['figures']=[e for e in old['figures'] if e['case'] not in cases]+entries
    old.update(script='plot_comparisons.py',date='2026-10-25',style_reference='reference/esd-14.png',
               real_numerical_data=True,all_raw_data_retained=True,png_dpi=300,pdf='vector text and markers; rasterized heatmap meshes')
    manifest.write_text(json.dumps(old,indent=2),encoding='utf8')
    (HERE/'comparison_captions.md').write_text('\n\n'.join('### '+e['png']+'\n\n'+e['caption'] for e in old['figures']),encoding='utf8')

if __name__=='__main__':main()
