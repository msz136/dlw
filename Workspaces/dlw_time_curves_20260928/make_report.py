"""Scientific error-time figures, checked CSVs and Markdown-only handoff."""
import json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import run_curves as run
OUT=run.OUT;HERE=OUT.parent
def main():
    d=json.loads((OUT/'results.json').read_text());assert len(d['runs'])==16
    prior_path=run.BASE/'reliability/results.json';prior=json.loads(prior_path.read_text())
    prior_validation=json.loads((run.BASE/'reliability/summary.json').read_text())
    assert .01 in prior_validation['common_passing_sample_times'] and .02 in prior_validation['common_passing_sample_times']
    rows=[];max_readback=max_eval=max_prior=max_time=0.
    for r in d['runs']:
        assert r['status']=='completed' and run.previous.sha(r['profile'])==r['profile_sha256']
        assert len(r['history'])==41
        s=r['spec'];ref=run.previous.PaperExact(run.previous.CASES[s['case']],.125,True)
        if s['mesh']=='fixed':assert r['moved_steps']==0
        else:assert r['moved_steps']==round(.02/s['dt'])
        with np.load(r['profile']) as z:
            for h in r['history']:
                t=h['t'];xx=np.linspace(-10,10,4001);exact=ref.uv(np.arange(-12,12),xx,t)
                for f,ee in zip(('u','v'),exact):
                    value=CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(xx)
                    err=float(np.max(abs(value-ee)));max_readback=max(max_readback,abs(err-h['errors'][f]))
                    rows.append(dict(case=s['case'],model=s['model'],mesh=s['mesh'],variant=s['variant'],dt=s['dt'],t=t,field=f,absolute_error=err,nodal_error=h['nodal_errors'][f]))
                if any(abs(t-tt)<1e-12 for tt in (0.,.01,.02)):
                    grid=np.linspace(-10,10,8001);exact2=ref.uv(np.arange(-12,12),grid,t)
                    for f,ee in zip(('u','v'),exact2):
                        err=float(np.max(abs(CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(grid)-ee)))
                        max_eval=max(max_eval,abs(err/h['errors'][f]-1))
        pp=next(p for p in prior['runs'] if p['spec']['case']==s['case'] and p['spec']['model']==s['model'] and p['spec']['mesh']==s['mesh'] and p['spec']['variant']==('base' if s['variant']=='main' else 'time_half'))
        for t in (.005,.01,.02):
            a=next(h['errors'] for h in r['history'] if abs(h['t']-t)<1e-12);b=next(h['errors'] for h in pp['history'] if abs(h['t']-t)<1e-12)
            max_prior=max(max_prior,*(abs(a[f]-b[f]) for f in ('u','v')))
    assert max_readback<1e-12 and max_prior<1e-10
    run.previous.csvout(OUT/'error_time.csv',rows)
    def get(case,model,mesh,variant):return next(r for r in d['runs'] if all(r['spec'][k]==v for k,v in dict(case=case,model=model,mesh=mesh,variant=variant).items()))
    schemes=[('structure','fixed','SD / fixed','#D55E00','-'),('structure','moving','SD / moving','#D55E00','--'),('fd','fixed','FD / fixed','#0072B2','-'),('fd','moving','FD / moving','#0072B2','--')]
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,2,figsize=(11,7),sharex=True,layout='constrained')
    chosen=[]
    for i,case in enumerate(('fig1a','fig1b')):
        for j,field in enumerate(('u','v')):
            ax=axes[i,j]
            for model,mesh,label,color,style in schemes:
                main=get(case,model,mesh,'main');half=get(case,model,mesh,'time_half')
                ts=np.array([h['t'] for h in main['history']]);es=np.array([h['errors'][field] for h in main['history']]);hs=np.array([h['errors'][field] for h in half['history']])
                max_time=max(max_time,float(np.max(abs(hs/es-1))))
                ax.plot(ts,es,color=color,ls=style,lw=1.9,label=label)
                for t in (.01,.02):
                    k=int(np.argmin(abs(ts-t)));ax.plot(ts[k],es[k],'o',color=color,ms=4)
                    if j==0:
                        h=main['history'][k];chosen.append(dict(case=case,model=model,mesh=mesh,t=t,u_error=h['errors']['u'],v_error=h['errors']['v']))
            ax.set_yscale('log');ax.set_xlim(0,.0204);ax.set_xticks([0,.005,.01,.015,.02]);ax.axvline(.01,color='.6',lw=.8,ls=':')
            ax.grid(True,which='major',alpha=.22);ax.set_xlabel('Time t');ax.set_ylabel(f'Maximum absolute {field} error')
            ax.set_title(f"Paper Fig. 1({'a' if i==0 else 'b'}): (a,p,q) = {'(2,1,2)' if i==0 else '(2,4,-3)'}")
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=4,frameon=False)
    fig.savefig(HERE/'error_vs_time.png',dpi=200);fig.savefig(HERE/'error_vs_time.pdf');fig.savefig(HERE/'error_vs_time.svg');plt.close(fig)
    run.previous.csvout(OUT/'t001_t002.csv',chosen)
    validation=dict(runs=16,samples_per_run=41,profiles_verified=16,all_moving_steps_updated=True,readback_max=max_readback,previous_control_anchor_max_difference=max_prior,evaluation_double_max_relative_at_anchors=max_eval,time_half_max_relative_error_change=max_time,prior_control_results_sha256=run.previous.sha(prior_path),cutoff=.02,cutoff_reason='Common passing nonzero sample horizon from existing time/space/domain controls; .05 is not a common passing point. No claim that .02 is exact instability onset.')
    run.previous.dump(OUT/'validation.json',validation)
    lines=[f"| {r['case']} | {'SD' if r['model']=='structure' else 'FD'} | {r['mesh']} | {r['t']:.2f} | {r['u_error']:.6e} | {r['v_error']:.6e} |" for r in chosen]
    report=f'''# DLW 原文参数：误差随时间曲线

原文图1(a)固定a=2,p=1,q=2；图1(b)固定a=2,p=4,q=-3。均c1=1、xi10=eta10=0。只改变数值设置，不扫描或优化物理参数。

## 图与数据

- error_vs_time.png / .pdf / .svg：两行对应两个原文算例，两列对应u/v；橙色结构半离散SD，蓝色普通差分FD；实线固定网格，虚线持续动网格。纵轴为最大绝对误差的对数刻度，标出t=.01/.02。
- out/error_time.csv：完整曲线及节点误差；out/t001_t002.csv：两个指定时刻的双场表。
- out/results.json：16条轨道（8主＋8减半步长）、原始场及源码/轨道哈希；out/validation.json：读回、时间和评价点核对。

## 为什么画到t=.02

已有48组时间/空间/扩域核对中，八种组合在t=.005/.01/.02均通过共同检查，t=.05不能全部通过。因此统一保守截到.02，不按各方法的好坏分别剪线。每隔.0005保存，含t0共41个点；保留初始重构误差，不减去E(0)。.02是已核对的共同短时终点，不是精确的不稳定起始时刻；不能把这些曲线称为t=1的成功传播。

此前核对口径：各数值配置对连续解误差≤各场初始峰值1%，与主配置的场差≤相同峰值0.1%；加密y时插值到共同层。该标准是有限配置的数值检查，不是严格误差界或统计显著性。

## 数值方法

RK4，主dt=.000125、控制dt=.0000625；x∈[-20,20)、256点，y格距.125、24个中点层覆盖[-1.5,1.5]。公共误差区x∈[-10,10]、4001点，对各y层取最大值；使用三次样条重构，与2HS线性插值指标不同。

动网格沿用R=平均[1-(v-Dy u)/4]及其通量Q，V=(Q-Q_left)/R，初始等质量布点，各RK级与当前场耦合更新。未加入滤波、阻尼、解析内部重置或缺陷强迫。**已修正固定组停止条件：固定组直接推进原物理RHS、V=0，不再要求动网格监测密度为正；只有动网格组保留该条件。** 本短窗内新旧误差锚点最大差{max_prior:.3g}，修正未改变已验证短时轨道。

全部16条到达.02，16个剖面哈希及所有1312个单场误差读回通过，最大差{max_readback:.3g}。主/半步长整条误差曲线最大相对变化{100*max_time:.4g}%；t0/.01/.02评价点4001→8001最大相对变化{100*max_eval:.4g}%。动网格每一步均有节点更新，固定组移动步数为0。

## 指定时刻数据

| 原图 | 方法 | 网格 | t | u误差 | v误差 |
|---|---|---|---:|---:|---:|
{chr(10).join(lines)}

本报告可支持原文参数点的短时误差比较；不支持长期稳定、任意参数优越性或一般收敛定理。旧长时失败数据保留在dlw_paper_cases_20260927中，不用本图覆盖或隐藏。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8');print(json.dumps(validation,indent=2))

if __name__=='__main__':main()
