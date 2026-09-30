"""Plot reviewed saved fields against the analytic solution; no new evolution."""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from four_scheme_results import HERE, SOURCE, exact, sha

def main():
    out=HERE/'four_scheme_figures';out.mkdir(exist_ok=True)
    data=json.loads((SOURCE/'out/results.json').read_text(encoding='utf-8'))
    audit=json.loads((HERE/'four_scheme_review/review.json').read_text(encoding='utf-8'))
    assert sha(SOURCE/'out/results.json')==audit['results_sha256']
    rows=list(data['rows'].values()); panels=[]; checked=0
    plt.rcParams.update({'font.family':'DejaVu Serif','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    for method,label in [('rk4','RK4'),('euler','Euler'),('heun','Heun'),('rk8','RK8 (DOP853)')]:
        for t in (.5,.25):
            fig,axes=plt.subplots(4,3,figsize=(13,12),layout='constrained')
            fig.suptitle(f'{label} | N=400 | dt=0.003125 | t={t}',fontsize=17)
            for j,p in enumerate((5,12,22)):
                xx,*ref=exact(p,t);xx=xx[::2];ref=[a[::2] for a in ref]
                for i,field in enumerate(('u','rho')):
                    ax=axes[i,j];ax.plot(xx,ref[i],color='black',lw=1.4,label='Exact')
                    ax.set(title=f'p={p}',ylabel=field,xlabel='physical x')
                    err=axes[i+2,j];err.set(xlabel='physical x',ylabel=f'absolute {field} error')
                    for route,name,color,marker in [('integrable_original','S1: original + moving','#994455','s'),('integrable_calibrated','S2: calibrated + moving','#b36521','o'),('difference_paper_ale','S3: FD + moving','#228855','+'),('difference_fixed','S4: FD + fixed','#276ba5','x')]:
                        matches=[r for r in rows if all(r['spec'][k]==v for k,v in dict(p=p,route=route,method=method,n=400,dt=.003125).items())]
                        assert len(matches)==1
                        r=matches[0];assert sha(r['profile'])==r['profile_sha256']
                        with np.load(r['profile']) as z:
                            x=z[f't{t}_'+('x' if field=='u' else 'rho_x')];v=z[f't{t}_{field}']
                            use=np.flatnonzero((x>=-2)&(x<=2))[::4]
                            ax.plot(x[use],v[use],ls='none',marker=marker,ms=3.5,mfc='none',color=color,label=name)
                            e=np.abs(np.interp(xx,x,v)-ref[i])
                        assert abs(e.max()-r['snapshots'][str(t)]['16001'][field])<5e-13
                        err.semilogy(xx,np.where(e>0,e,np.nan),color=color,lw=1,label=name);checked+=1
                    for a in (ax,err):
                        a.set_xlim(-2,2);a.grid(alpha=.18)
                    err.set_ylim(bottom=1e-12)
                    if j==0:ax.legend(fontsize=9);err.legend(fontsize=9)
            name=f'{method}_t{str(t).replace(".","p")}'
            for ext in ('png','pdf'):fig.savefig(out/f'{name}.{ext}',dpi=170)
            plt.close(fig)
            title=f'{label} · S1 原可积·动格 / S2 校准·动格 / S3 差分·动格 / S4 差分·固定格 · t={t}'
            figure=f'<figure><img src="Workspaces/gsg_project/dlw_report/four_scheme_figures/{name}.png" alt="{title}：双场波形和逐点绝对误差"></figure>'
            panels.append(f'<h4>{title}</h4>\n{figure}')
    (out/'figures.html').write_text('\n\n'.join(panels),encoding='utf-8')
    (out/'validation.json').write_text(json.dumps(dict(checked_error_curves=checked,results_sha256=audit['results_sha256'],evaluation_points=16001,p=[5,12,22],N=400,dt=.003125)),encoding='utf-8')
    print(f'Generated 8 PNG/PDF figures; {checked} error curves match reviewed metrics.')

if __name__=='__main__':main()
