"""Scientific figures from completed mechanism experiments; no simulated data.

Layout references: oa-tech-pone-0116670-f16 (aligned small multiples),
oa-geo-bg-21-811-2024-f02 (explicitly scaled comparison panels).
Colors follow the existing DLW PE/FD reports, not the references' data colors.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
OUT=HERE/'figures';OUT.mkdir(exist_ok=True)
COLORS={'SD':'#1776bc','FD':'#38965f'}
NAMES={'SD':'PE','FD':'FD'}
plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'axes.linewidth':.7,'xtick.direction':'in',
                     'ytick.direction':'in','savefig.dpi':300,'pdf.fonttype':42})


def transport(case):
    paths=[HERE/f'transport/{case}_T0.010_dt0.000100_parts_cache5',
           HERE/f'transport/{case}_T0.010_dt0.000100_parts',
           HERE/f'transport/{case}_T0.010_dt0.000500_parts_cache5']
    for p in paths:
        if (p/'validation.json').exists():
            return p,json.loads((p/'validation.json').read_text(encoding='utf-8'))
    raise FileNotFoundError(f'No completed transport for {case}')


def save(fig,name):
    fig.savefig(OUT/(name+'.png'),bbox_inches='tight')
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight')
    plt.close(fig)


def main():
    results={c:transport(c) for c in ('A','C')}
    fig,axs=plt.subplots(1,2,figsize=(9,3.6),layout='constrained')
    for ax,(case,field) in zip(axs,[('A','v'),('C','u')]):
        record=results[case][1]
        metrics={r['label']:r for r in record['final_metrics']}
        scale=1e6
        for offset,kind in zip([-.18,.18],['SD','FD']):
            values=[metrics[f'{kind}_part_y_model'][field+'_rms'],
                    metrics[f'{kind}_part_x_stencil'][field+'_rms'],
                    metrics[f'actual_{kind}'][field+'_rms']]
            ax.bar(np.arange(3)+offset,np.array(values)*scale,width=.32,color=COLORS[kind],label=NAMES[kind])
            for x,y in zip(np.arange(3)+offset,np.array(values)*scale):
                ax.text(x,y,f'{y:.2f}',ha='center',va='bottom',fontsize=8)
        angles={r['kind']:r['cosine'] for r in record['final_source_budget'] if r['comparison']=='part_angle_'+field}
        ax.set_title(f'{case}: {field};  cos(PE)={angles["SD"]:+.3f}, cos(FD)={angles["FD"]:+.3f}')
        ax.set_xticks(range(3),['From y model','From x stencil','Actual total'])
        ax.set_ylabel('RMS error '+r'($\times 10^{-6}$)')
        ax.margins(y=.16);ax.legend(frameon=False)
    save(fig,'transported_source_budget')

    fig,axs=plt.subplots(1,2,figsize=(8,3.6),layout='constrained')
    for ax,case in zip(axs,['A','C']):
        m={r['label']:r for r in results[case][1]['final_metrics']}
        baseline=m['actual_FD']['joint_rms']
        values=np.array([[m[f'{p}_from_{s}']['joint_rms']/baseline for s in ('FD','SD')] for p in ('FD','SD')])
        im=ax.imshow(values,cmap='Blues',vmin=.88,vmax=1.2,aspect='equal')
        for i in range(2):
            for j in range(2):
                ax.text(j,i,f'{values[i,j]:.6f}',ha='center',va='center',color='white' if values[i,j]>1.08 else '#111')
        ax.set_xticks([0,1],['FD source','PE source']);ax.set_yticks([0,1],['FD propagation','PE propagation'])
        ax.set_title(f'Case {case}');ax.tick_params(length=0)
    fig.colorbar(im,ax=axs,shrink=.75,label='Predicted joint RMS / actual FD RMS')
    save(fig,'source_propagator_exchange')

    h=pd.read_csv(HERE/'intervention/summary.csv');h=h[~h.halfdt]
    fig,axs=plt.subplots(1,2,figsize=(8.7,3.4),layout='constrained')
    for ax,case in zip(axs,['A','C']):
        d=h[h.case==case].sort_values('lam')
        for field,color,marker in [('joint','#333','o'),('u',COLORS['SD'],'s'),('v',COLORS['FD'],'^')]:
            y=d[field+'_rms'].to_numpy();ax.plot(d.lam,y/y[0],color=color,marker=marker,label=field)
        ax.axhline(1,color='.6',lw=.7,ls=':');ax.set_title(f'Case {case}')
        ax.set_xlabel(r'Update mixture $\lambda$ (0: FD; 1: PE)');ax.set_ylabel('RMS / FD RMS')
        ax.legend(frameon=False)
    save(fig,'update_intervention')

    p=HERE/'transport/A_T0.040_dt0.000100'
    time=pd.read_csv(p/'timeseries.csv');comp=pd.read_csv(p/'comparison.csv')
    fig,axs=plt.subplots(1,2,figsize=(9,3.5),layout='constrained')
    for kind in ('SD','FD'):
        d=time[(time.label=='actual_'+kind)&(time.t>0)]
        q=time[(time.label==f'{kind}_from_{kind}')&(time.t>0)]
        axs[0].semilogy(d.t,d.joint_rms,color=COLORS[kind],label=NAMES[kind]+' actual')
        axs[0].semilogy(q.t,q.joint_rms,color=COLORS[kind],ls='--',label=NAMES[kind]+' prediction')
        g=comp[(comp.propagator==kind)&(comp.source==kind)&(comp.comparison=='against_unpropagated_sum')&(comp.t>0)]
        axs[1].plot(g.t,g.norm_ratio,color=COLORS[kind],label=NAMES[kind])
    axs[0].set_title('A: error growth and independent prediction');axs[0].set_ylabel('Joint RMS error')
    axs[1].set_title('A: effect of propagation');axs[1].set_ylabel('Transported error / accumulated source')
    for ax in axs:ax.set_xlabel('Time');ax.legend(frameon=False,fontsize=8)
    save(fig,'error_evolution')

    refinement=pd.read_csv(HERE/'refinement/comparison.csv')
    fig,axs=plt.subplots(1,2,figsize=(8.7,3.4),layout='constrained')
    for ax,field in zip(axs,['u','v']):
        for kind in ('SD','FD'):
            d=refinement[(refinement.model==kind)&(refinement.field==field)].sort_values('dx',ascending=False)
            ax.plot([0,1],d.rms,color=COLORS[kind],marker='o',label=NAMES[kind])
            for x,y in zip([0,1],d.rms):
                offset=8 if kind=='SD' else -14
                if field=='u' and x==0:
                    offset=-14 if kind=='SD' else 8
                ax.annotate(f'{NAMES[kind]} {y:.3e}',(x,y),textcoords='offset points',xytext=(0,offset),ha='center',fontsize=8,color=COLORS[kind],bbox={'facecolor':'white','edgecolor':'none','pad':1.0})
        ax.set_yscale('log');ax.set_xticks([0,1],[r'$\Delta x=0.1$',r'$\Delta x=0.025$'])
        ax.set_ylabel('Physical RMS error');ax.set_title(f'C: {field}, fixed h=0.1, T=0.001');ax.margins(x=.2,y=.25)
        ax.legend(frameon=False)
    save(fig,'refinement_reversal')
    print(json.dumps({'figures':5,'formats':['PNG 300 dpi','PDF'],'directory':str(OUT)}))


if __name__=='__main__':main()
