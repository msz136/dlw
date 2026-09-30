"""Summarize the paper two-soliton run on the report's physical interval."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[2]/'Workspaces/hs_two_soliton_short_20260928/main'
OUT=HERE/'submission_report'
sys.path.insert(0,str(HERE.parents[2]/'Workspaces/hs_numerics_plan'))
from hs_exact import Soliton

def main():
    doc=json.loads((SOURCE/'results.json').read_text(encoding='utf-8'))
    cfg=doc['configuration']
    assert cfg['p']==[1.1,1.25] and cfg['q']==[11,5]
    assert cfg['a']==.005 and cfg['dt']==.003125 and cfg['method']=='rk4'
    assert cfg['t0']==0. and cfg['t1']==.5 and cfg['evaluation_bounds']==[-1,1]
    sol=Soliton((1.1,1.25),phase=(np.log(6.5),)*2,shift=-(1/11+1/5))
    xx=np.linspace(-1,1,32001)
    times=(.5,)
    cases=(('S1','可积半离散（动网格）','Integrable + moving','#994455','--'),
           ('S4','中心差分（固定网格）','FD + fixed','#276ba5',':'),
           ('S3','中心差分（动网格）','FD + moving','#b36521','-.'))
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11})
    fig,ax=plt.subplots(figsize=(7.2,4.5),layout='constrained')
    rows=['| 空间方案 | $E_u$ | $E_\\rho$ |','|---|---:|---:|']
    checks=0;max_delta=0.;metrics={}
    for t in times:
        ref=sol.continuous_x(xx,t)[:2]
        for scheme,title,label,color,style in cases:
            result=doc['results'][scheme]
            assert result['status']=='completed' and result['last_time']==.5
            path=SOURCE/result['profile']
            assert hashlib.sha256(path.read_bytes()).hexdigest()==result['profile_sha256']
            values={}
            with np.load(path) as z:
                for i,field in enumerate(('u','rho')):
                    key=f't{t}_'+('x' if field=='u' else 'rho_x')
                    coords=z[key];profile=z[f't{t}_{field}']
                    assert coords[0]<-1 and coords[-1]>1
                    error=np.abs(np.interp(xx,coords,profile)-ref[i])
                    delta=abs(float(error.max())-result['metrics'][str(t)][field])
                    max_delta=max(max_delta,delta);checks+=1
                    assert delta<5e-13,(scheme,t,field,delta)
                    values[field]=float(error.max())
                    if field=='rho':
                        bins=np.minimum(np.floor((xx+1)/.02).astype(int),99)
                        envelope=np.array([error[bins==k].max() for k in range(100)])
                        assert envelope.max()==error.max()
                        centers=-1+(np.arange(100)+.5)*.02
                        ax.semilogy(centers,np.maximum(envelope,1e-16),color=color,ls=style,lw=.9,label=label)
            metrics[f'{scheme}_t{t}']=values
            rows.append(f'| {title} | {values["u"]:.4e} | {values["rho"]:.4e} |')
        ax.set(xlabel='x',xlim=(-1,1),ylim=(1e-10,1e-2),ylabel=r'Local maximum of $|\rho_h-\rho|$')
        ax.grid(alpha=.15)
    ax.legend(fontsize=10)
    for field in ('u','rho'):
        assert metrics['S4_t0.5'][field]<metrics['S3_t0.5'][field]<metrics['S1_t0.5'][field]
    comparison=(f'三种方法均计算至 $t=0.5$。固定网格差分的双场误差最小，其次为动网格差分，可积半离散格式最大。'
                f'后两者的 $\\rho$ 误差分别为固定网格差分的 '
                f'{metrics["S3_t0.5"]["rho"]/metrics["S4_t0.5"]["rho"]:.2f} 倍和 '
                f'{metrics["S1_t0.5"]["rho"]/metrics["S4_t0.5"]["rho"]:.1f} 倍。')
    for ext in ('png','pdf'):fig.savefig(OUT/f'two_soliton_error.{ext}',dpi=190)
    plt.close(fig)
    summary={'table':'\n'.join(rows),'comparison':comparison,'metrics':metrics,'checked_saved_metrics':checks,
             'max_saved_metric_difference':max_delta,'evaluation_bounds':[-1,1],
             'evaluation_points':32001,'time_bounds':[0.,.5],'display_times':times,
             'source_sha256':hashlib.sha256((SOURCE/'results.json').read_bytes()).hexdigest(),
             'figure':'submission_report/two_soliton_error.png'}
    (OUT/'two_soliton_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Two-soliton: {checks} saved metrics verified; max difference {max_delta:.3g}.')

if __name__=='__main__':main()
