"""Summarize the paper two-soliton run on the report's physical interval."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'Workspaces/hs_two_soliton_point_20260928'
OUT=HERE/'submission_report'
sys.path.insert(0,str(HERE.parents[2]/'Workspaces/hs_numerics_plan'))
from hs_exact import Soliton

def main():
    doc=json.loads((SOURCE/'four_schemes_results.json').read_text(encoding='utf-8'))
    cfg=doc['configuration']
    assert cfg['p']==[1.1,1.25] and cfg['q']==[11,5]
    assert cfg['a']==.005 and cfg['dt']==.003125 and cfg['method']=='rk4'
    sol=Soliton((1.1,1.25),phase=(np.log(6.5),)*2,shift=-(1/11+1/5))
    xx=np.linspace(-1,1,32001)
    old_x=np.linspace(-2.5,1.5,16001)
    times=(-2.5,0.,3.)
    cases=(('S1','原可积半离散＋论文动网格','Integrable + moving','#994455','--'),
           ('S4','直接差分＋均匀固定网格','FD + fixed','#276ba5',':'),
           ('S3','直接差分＋论文动网格','FD + moving','#b36521','-.'))
    fig,axes=plt.subplots(3,1,figsize=(7.2,7.2),layout='constrained',sharex=True,sharey=True)
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10})
    rows=['| 时间 | 空间方案 | $E_u$ | $E_\\rho$ |','|---:|---|---:|---:|']
    checks=0;max_delta=0.;metrics={}
    for col,t in enumerate(times):
        ref=sol.continuous_x(xx,t)[:2]
        old_ref=sol.continuous_x(old_x,t)[:2]
        ax=axes[col]
        for scheme,title,label,color,style in cases:
            result=doc['results'][scheme]
            if str(t) not in result['metrics']:
                rows.append(f'| {t:g} | {title} | — | — |')
                continue
            path=SOURCE/result['profile']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==result['profile_sha256']
            values={}
            with np.load(path) as z:
                for i,field in enumerate(('u','rho')):
                    key=f't{t}_'+('x' if field=='u' else 'rho_x')
                    coords=z[key];profile=z[f't{t}_{field}']
                    assert coords[0]<-1 and coords[-1]>1
                    error=np.abs(np.interp(xx,coords,profile)-ref[i])
                    old_error=float(np.max(np.abs(np.interp(old_x,coords,profile)-old_ref[i])))
                    delta=abs(old_error-result['metrics'][str(t)][field])
                    max_delta=max(max_delta,delta);checks+=1
                    assert delta<5e-13,(scheme,t,field,delta)
                    values[field]=float(error.max())
                    if field=='rho':
                        bins=np.minimum(np.floor((xx+1)/.02).astype(int),99)
                        envelope=np.array([error[bins==k].max() for k in range(100)])
                        assert envelope.max()==error.max()
                        centers=-1+(np.arange(100)+.5)*.02
                        ax.semilogy(centers,np.maximum(envelope,1e-12),color=color,ls=style,lw=1.2,label=label)
            metrics[f'{scheme}_t{t}']=values
            rows.append(f'| {t:g} | {title} | {values["u"]:.3e} | {values["rho"]:.3e} |')
        ax.set(xlim=(-1,1),ylim=(1e-8,1),title=f't = {t:g}',ylabel=r'Local max. of $|\rho_h-\rho|$')
        ax.grid(alpha=.15)
    axes[-1].set_xlabel('physical x')
    assert doc['results']['S1']['status']=='failed'
    assert abs(doc['results']['S1']['last_time']-(-1.684375))<1e-6
    axes[0].legend(fontsize=8,loc='upper left')
    axes[1].text(.98,.96,'Integrable run stopped before this time',transform=axes[1].transAxes,fontsize=8,ha='right',va='top')
    axes[2].text(.98,.96,'Integrable run stopped before this time',transform=axes[2].transAxes,fontsize=8,ha='right',va='top')
    for ext in ('png','pdf'):fig.savefig(OUT/f'two_soliton_error.{ext}',dpi=190)
    plt.close(fig)
    summary={'table':'\n'.join(rows),'metrics':metrics,'checked_saved_metrics':checks,
             'max_saved_metric_difference':max_delta,'evaluation_bounds':[-1,1],
             'evaluation_points':32001,'source_sha256':hashlib.sha256((SOURCE/'four_schemes_results.json').read_bytes()).hexdigest(),
             'figure':'submission_report/two_soliton_error.png'}
    (OUT/'two_soliton_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Two-soliton: {checks} saved metrics verified; max difference {max_delta:.3g}.')

if __name__=='__main__':main()
