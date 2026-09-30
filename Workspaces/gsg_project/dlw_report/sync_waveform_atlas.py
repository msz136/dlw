"""Read the frozen atlas; build S5/S6 figures and report tables, without evolution."""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
ATLAS=ROOT/'Workspaces/hs_waveform_atlas_20260927'
OUT=HERE/'atlas_update'

def main():
    OUT.mkdir(exist_ok=True)
    data=json.loads((ATLAS/'out/results.json').read_text(encoding='utf-8'))
    summary=json.loads((ATLAS/'out/summary.json').read_text(encoding='utf-8'))
    rows=list(data['rows'].values())
    selected=[r for r in rows if r['spec']['route'] in ('difference_rm','difference_fixed')]
    for r in selected:
        assert r['status']=='completed'
        assert hashlib.sha256(Path(r['profile']).read_bytes()).hexdigest()==r['profile_sha256']
    def get(p,route,purpose='main'):
        return next(r for r in selected if r['spec']['p']==p and r['spec']['route']==route and r['spec']['purpose']==purpose)
    ratios=[r for r in summary['ratios'] if r['numerator']=='difference_rm' and r['region']=='core']
    for r in ratios:
        for field in ('u','rho'):
            for suffix,purpose in [('', 'main'),('_half','time_half')]:
                a=get(r['p'],'difference_rm',purpose)['snapshots'][str(r['time'])]['errors']['core'][field]
                b=get(r['p'],'difference_fixed',purpose)['snapshots'][str(r['time'])]['errors']['core'][field]
                assert np.isclose(a/b,r[field+suffix],rtol=1e-12,atol=0)
    counts=['| 时刻 | u 改善：主步长 | u 改善：减半步长 | rho 改善：主步长 | rho 改善：减半步长 |','|---|---:|---:|---:|---:|']
    examples=['| p | 时刻 | S5：直接差分＋Rm，u / rho | S6：直接差分＋均匀，u / rho | u 误差比 S5/S6 | rho 误差比 S5/S6 |','|---:|---:|---:|---:|---:|---:|']
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
    fig,axes=plt.subplots(2,2,figsize=(12,7.5),layout='constrained')
    for j,t in enumerate((.25,.5)):
        subset=sorted([r for r in ratios if r['time']==t],key=lambda r:r['p'])
        assert len(subset)==39
        counts.append('| '+str(t)+' | '+' | '.join(f'{sum(r[f]<1 for r in subset)}/39' for f in ['u','u_half','rho','rho_half'])+' |')
        for i,field in enumerate(('u','rho')):
            ax=axes[i,j]
            ax.plot([r['p'] for r in subset],[r[field] for r in subset],label='dt = 0.003125',color='#b36521')
            ax.plot([r['p'] for r in subset],[r[field+'_half'] for r in subset],ls='--',label='dt = 0.0015625',color='#276ba5')
            ax.axhline(1,color='black',lw=.8);ax.grid(alpha=.15)
            ax.set(xlabel='soliton parameter p',ylabel=f'{field} error ratio: S5 / S6',title=f'Euler, t = {t}; below 1: Rm better')
            ax.legend(fontsize=9)
        for p in (5,14,22):
            r=next(r for r in subset if r['p']==p)
            es=[get(p,route)['snapshots'][str(t)]['errors']['core'] for route in ('difference_rm','difference_fixed')]
            examples.append(f'| {p} | {t} | '+ ' | '.join(f'{e["u"]:.3e} / {e["rho"]:.3e}' for e in es)+f' | {r["u"]:.3f} | {r["rho"]:.3f} |')
    fig.savefig(OUT/'s5_s6_parameter_ratios.png',dpi=170);plt.close(fig)
    samples=np.load(ATLAS/'out/waveform_samples_t0.5.npz')
    fig,axes=plt.subplots(2,3,figsize=(14,6),layout='constrained')
    for j,p in enumerate((5,14,22)):
        idx=int(np.flatnonzero(samples['p']==p)[0])
        for i,field in enumerate(('u','rho')):
            ax=axes[i,j]
            for route,label,color in [('difference_rm','S5: FD + Rm','#b36521'),('difference_fixed','S6: FD + uniform','#276ba5')]:
                e=samples[route+'_abs_error'][idx,i]
                assert np.array_equal(e,np.abs(samples[route][idx,i]-samples['exact'][idx,i]))
                with np.load(get(p,route)['profile']) as profile:
                    coords=profile['t0.5_x' if field=='u' else 't0.5_rho_x']
                    assert np.allclose(np.interp(samples['x'],coords,profile['t0.5_'+field]),samples[route][idx,i],rtol=0,atol=1e-14)
                ax.semilogy(samples['x'],np.where(e>0,e,np.nan),label=label,color=color)
            ax.set(xlabel='physical x',ylabel=f'absolute {field} error',title=f'Euler, p={p:g}, t=0.5',ylim=(1e-12,1e-2))
            ax.grid(alpha=.15);ax.legend(fontsize=9)
    fig.savefig(OUT/'s5_s6_error_x.png',dpi=170);plt.close(fig)
    result={'counts_table':'\n'.join(counts),'examples_table':'\n'.join(examples),'checked_profiles':len(selected),
            'ratio_rows':len(ratios),'source_results_sha256':hashlib.sha256((ATLAS/'out/results.json').read_bytes()).hexdigest()}
    (OUT/'integration.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Checked {len(selected)} profile hashes, {len(ratios)} ratio rows, and 12 sampled curves against saved fields.')

if __name__=='__main__':main()
