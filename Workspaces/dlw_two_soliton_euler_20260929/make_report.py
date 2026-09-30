"""Euler total-error tables, matched RK4 comparison, temporal field convergence."""
import json
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_euler import HERE,PRIOR,OUT,old
from reference import CASES,TwoExact
io=old.previous

def main():
    data=json.loads((OUT/'results.json').read_text(encoding='utf-8'));runs=data['runs']
    rkpath=PRIOR/'out/results.json';rk=json.loads(rkpath.read_text(encoding='utf-8'))['runs']
    assert len(runs)==len(data['plan'])==111
    for p,digest in data['sources'].items():assert io.sha(p)==digest,p
    def get(case,model,mesh,variant='main',method='Euler'):
        return next(r for r in (runs if method=='Euler' else rk) if all(r['spec'][k]==v for k,v in dict(case=case,model=model,mesh=mesh,variant=variant).items()))
    def snap(r,t):return next((h for h in r['history'] if abs(h['t']-t)<1e-12),None)
    def grid(s):return np.linspace(-s['eval_half'],s['eval_half'],8001 if s['case']=='fig5' else 4001)
    def values(z,t,f,xx,y=None):
        v=CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(xx)
        if y is not None and len(y)!=len(z['y']):v=CubicSpline(z['y'],v,axis=0)(y)
        return v
    rows=[];readback=0.;eval_change=0.;scales={};statuses=[]
    for case in CASES:
        s=get(case,'SD','fixed')['spec'];g=TwoExact(CASES[case],.125)
        scales[case]=dict(zip(('u','v'),[float(abs(a).max()) for a in g.uv(np.arange(-12,12),np.linspace(-s['eval_half'],s['eval_half'],16001),0.)]))
    for r in runs:
        s=r['spec'];assert io.sha(r['profile'])==r['profile_sha256']
        if s['mesh']=='fixed':assert r['moved_steps']==0
        elif r['status']=='completed':assert r['moved_steps']==round(.02/s['dt'])
        statuses.append(dict(**s,status=r['status'],reached=r['reached'],reason=r['reason']))
        g=TwoExact(CASES[s['case']],s['h']);js=np.arange(-round(1.5/s['h']),round(1.5/s['h']));xx=grid(s)
        with np.load(r['profile']) as z:
            for h in r['history']:
                t=h['t'];exact=g.uv(js,xx,t)
                for f,e in zip(('u','v'),exact):
                    er=float(abs(values(z,t,f,xx)-e).max());readback=max(readback,abs(er-h['errors'][f]))
                    rows.append(dict(case=s['case'],model=s['model'],mesh=s['mesh'],variant=s['variant'],method='Euler',dt=s['dt'],nx=s['nx'],h=s['h'],L=s['L'],t=t,field=f,error=er))
                    if s['variant']=='main' and t in (0.,.01,.02):
                        x2=np.linspace(xx[0],xx[-1],2*len(xx)-1);e2=g.uv(js,x2,t)[0 if f=='u' else 1]
                        er2=float(abs(values(z,t,f,x2)-e2).max());eval_change=max(eval_change,abs(er2/er-1))
    assert readback<1e-12
    io.csvout(OUT/'error_time_all.csv',rows);io.csvout(OUT/'status.csv',statuses)
    table=[];compare=[];orders=[];controls=[];initial_max=0.;fine=[]
    for case in CASES:
        for mesh in ('fixed','moving'):
            for t in (0.,.01,.02):
                row=dict(case=case,mesh=mesh,t=t)
                for model in ('SD','SD2','FD'):
                    h=snap(get(case,model,mesh),t)
                    row.update({model+'_'+f:h['errors'][f] if h else None for f in ('u','v')})
                table.append(row)
            for model in ('SD','SD2','FD'):
                main=get(case,model,mesh);half=get(case,model,mesh,'time_half');quarter=get(case,model,mesh,'time_quarter');ref=get(case,model,mesh,method='RK4')
                assert io.sha(ref['profile'])==ref['profile_sha256']
                xx=grid(main['spec'])
                with np.load(main['profile']) as z1,np.load(half['profile']) as z2,np.load(quarter['profile']) as z4,np.load(ref['profile']) as zr:
                    for f in ('x','u','v'):initial_max=max(initial_max,float(abs(z1['t0_'+f]-zr['t0_'+f]).max()))
                    for t in (.01,.02):
                        h=snap(main,t);hr=snap(ref,t)
                        if not h or not hr:continue
                        for f in ('u','v'):
                            compare.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,Euler_error=h['errors'][f],RK4_error=hr['errors'][f],Euler_over_RK4=h['errors'][f]/hr['errors'][f]))
                            if not snap(half,t) or not snap(quarter,t):continue
                            a,b,c,d=[values(z,t,f,xx) for z in (z1,z2,z4,zr)]
                            d12=float(abs(a-b).max());d24=float(abs(b-c).max())
                            orders.append(dict(case=case,model=model,mesh=mesh,t=t,field=f,dt_vs_half=d12,half_vs_quarter=d24,observed_order=float(np.log2(d12/d24)) if d12>0 and d24>0 else None,Euler_vs_RK4_field=float(abs(a-d).max()),half_vs_RK4_field=float(abs(b-d).max()),quarter_vs_RK4_field=float(abs(c-d).max())))
                    variants=['time_half','time_quarter','x_half','y_half','domain_double']
                    if case=='fig4' and mesh=='moving':variants.append('x_half_time_half')
                    for variant in variants:
                        r=get(case,model,mesh,variant)
                        with np.load(r['profile']) as z:
                            for t in (.001,.005,.01,.02):
                                h=snap(main,t);hc=snap(r,t)
                                for f in ('u','v'):
                                    if h and hc:
                                        diff=float(abs(values(z1,t,f,xx)-values(z,t,f,xx,z1['y'])).max());er=hc['errors'][f];base=h['errors'][f]
                                        passed=bool(max(er,base)/scales[case][f]<=.01 and diff/scales[case][f]<=.001)
                                    else:diff=er=base=None;passed=False
                                    controls.append(dict(case=case,model=model,mesh=mesh,variant=variant,t=t,field=f,main_error=base,control_error=er,field_difference=diff,initial_peak=scales[case][f],pass_old_threshold=passed))
    assert initial_max<1e-12
    for model in ('SD','SD2','FD'):
        a=get('fig4',model,'moving','x_half');b=get('fig4',model,'moving','x_half_time_half')
        for t in (.01,.02):
            ha,hb=snap(a,t),snap(b,t)
            if ha and hb:
                fine.append(dict(model=model,t=t,maximum_relative_error_change=max(abs(hb['errors'][f]/ha['errors'][f]-1) for f in ('u','v'))))
    common={case:[t for t in (.001,.005,.01,.02) if all(r['pass_old_threshold'] for r in controls if r['case']==case and r['t']==t)] for case in CASES}
    schemes=[dict(case=case,model=model,mesh=mesh,passing_anchors=[t for t in (.001,.005,.01,.02) if all(r['pass_old_threshold'] for r in controls if r['case']==case and r['model']==model and r['mesh']==mesh and r['t']==t)]) for case in CASES for model in ('SD','SD2','FD') for mesh in ('fixed','moving')]
    for filename,rr in (('comparison.csv',table),('euler_vs_rk4.csv',compare),('time_order.csv',orders),('control_comparisons.csv',controls),('fine_time_checks.csv',fine)):io.csvout(OUT/filename,rr)
    val=dict(runs=len(runs),completed=sum(r['status']=='completed' for r in runs),readback_error_values=len(rows),readback_max=readback,profile_hashes_verified=len(runs)+18,Euler_RK4_initial_max_difference=initial_max,evaluation_double_max_relative_change=eval_change,observed_order_range=[min(r['observed_order'] for r in orders if r['observed_order'] is not None),max(r['observed_order'] for r in orders if r['observed_order'] is not None)],common_passing_anchors=common,scheme_checks=schemes,RK4_results_sha256=io.sha(rkpath))
    io.dump(OUT/'validation.json',val)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    colors={'SD':'#D55E00','SD2':'#009E73','FD':'#0072B2'}
    for kind in ('euler','time_comparison'):
        fig,axes=plt.subplots(3,2,figsize=(12,10.5),sharex=True,layout='constrained')
        for i,case in enumerate(CASES):
            for j,f in enumerate(('u','v')):
                ax=axes[i,j]
                if kind=='euler':
                    entries=[(get(case,m,mesh),f'{m} / {mesh}',colors[m],style) for m in ('SD','SD2','FD') for mesh,style in (('fixed','-'),('moving','--'))]
                else:
                    entries=[(get(case,m,'moving',method=method),f'{m} / {method}',colors[m],style) for m in ('SD','SD2','FD') for method,style in (('Euler','-'),('RK4','--'))]
                for r,label,color,style in entries:
                    ax.plot([h['t'] for h in r['history']],[h['errors'][f] for h in r['history']],color=color,ls=style,lw=1.8,label=label)
                ax.set_yscale('log');ax.set_xlim(0,.0202);ax.set_xticks([0,.005,.01,.015,.02]);ax.axvline(.01,color='.6',ls=':',lw=.7)
                ax.set_xlabel('Time t');ax.set_ylabel(f'Maximum absolute {f} error');ax.grid(alpha=.2)
                ax.set_title(f'Paper Fig. {case[-1]}: '+('Euler, fixed / moving' if kind=='euler' else 'moving mesh, Euler / RK4'))
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False)
        fig.supxlabel('Same original two-soliton parameters; dt=0.000125. Total error includes initial reconstruction; validation in report.',fontsize=9)
        for ext in ('png','svg'):fig.savefig(HERE/f'{kind}_error_vs_time.{ext}',dpi=180)
        plt.close(fig)
    def fmt(x):return '未到达' if x is None else f'{x:.6e}'
    tablines=[]
    for r in table:
        if r['t']==0:continue
        tablines.append(f"| {r['case']} | {r['mesh']} | {r['t']:.2f} | "+' | '.join(' / '.join(fmt(r[m+'_'+f]) for f in ('u','v')) for m in ('SD','SD2','FD'))+' |')
    slines=[f"| {s['case']} | {s['model']} | {s['mesh']} | {', '.join(map(str,s['passing_anchors'])) or '无'} |" for s in schemes]
    report=f'''# DLW二孤子：Euler六方案对照

沿用原文图3/4/5零背景二孤子，SD/SD2/FD×fixed/moving；参数、解析解、初值、空间离散、边界、持续动网格、误差指标全部沿用上一轮。只把时间更新替换成显式Euler：z_new=z+dt F(t,z)，场和节点同时用当前级更新。原RK4代码和数据未改；Euler在独立进程内替换时间步函数，输出另存。

## 参数与配置

三组均a=2、c1=c2=1、相位全零。图3：(p1,q1,p2,q2)=(6,-5,4,-3)；图4：(1,2,4,-3)；图5：(7/4,-5/3,1,-4/5)。完整二孤子tau参照不是单孤子叠加；参照/PDE/实际SD2 RHS核对见 ../dlw_two_soliton_20260929/reference_checks.json。图6周期背景未纳入。

主dt=.000125，t=0至.02，每.0005保存；h=.125、y条带[-1.5,1.5]。图3/4：L40、nx256、评价x∈[-10,10]4001点；图5：L640、nx1024、评价[-100,100]8001点。双场经三次样条到公共物理x点，与连续解析解比较，跨x及所有y层取最大绝对误差。保留初始重构误差，尤其SD2的Dx(Q)/Q重构误差；SD2边界闭合与旧SD的有限x差别沿用前轮。

共111条Euler轨道：18主配置，18减半时间步，18时间步四分之一，18x加密并减半时间步，18y加密，18同dx扩域，另图4三种moving在细x网格再减半时间步3条。{val['completed']}条完成到.02；停止记录不删除。控制保存0/.001/.005/.01/.02。

## 验证与解释

原始场读回{len(rows)}项误差，最大差{readback:.3e}；核对111个Euler与18个RK4主轨道哈希。Euler/RK4初始节点与物理场最大差{initial_max:.3e}；固定组不动、完成的动格组每步更新。主锚点评价点数加倍最大相对变化{eval_change:.3e}。

时间阶使用同一空间网格的“数值场之间的差”衡量：log2(||U_dt-U_dt/2||∞ / ||U_dt/2-U_dt/4||∞)，均在公共物理点、相同t上计算，不用总误差之比冒充时间收敛阶。所有三参数/六方案/双场在.01/.02上的观测阶范围为{val['observed_order_range'][0]:.4f}至{val['observed_order_range'][1]:.4f}。另保存各时间步数值场与相同空间配置RK4主解之间的差；RK4只是时间参照，不是连续精确解。

Euler总误差可能因时间和空间误差抵消而比RK4更小，因此不能把“更低阶却更小的单个总误差”解释成普遍优势。时间减步后的总误差、场差、排序必须一起阅读。

共同通过门槛沿用：各场误差≤初始峰值1%，主/控制场差≤该峰值0.1%；只对采样时刻及所测分辨率成立。各算例全部六方案的共同通过锚点：{common}。这不是严格误差界或统计显著性。

## Euler主表（每格u / v）

| 原图 | 网格 | t | SD | SD2 | FD |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(tablines)+'''

## 各方案通过全部控制的采样时刻

| 原图 | 离散化 | 网格 | 通过锚点 |
|---|---|---|---|
'''+ '\n'.join(slines)+'''

## 交接文件

- euler_error_vs_time.png/svg：Euler三算例、双场、六方案图。
- time_comparison_error_vs_time.png/svg：moving下Euler/RK4时间法对照；fixed对应数据也完整包含在CSV中。
- out/comparison.csv：Euler的0/.01/.02双场并列表，与上一轮RK4表同结构。
- out/euler_vs_rk4.csv：全部18配置在.01/.02的Euler/RK4总误差及比值。
- out/time_order.csv：三时间步的公共场差、观测阶、对RK4场差。
- out/control_comparisons.csv、fine_time_checks.csv、error_time_all.csv、status.csv：控制、全曲线与完成状态。
- out/results.json、validation.json、*.npz：计划、参数、源码/轨道哈希和原始场。

复现：run_euler.py → make_report.py，依赖前轮冻结reference.py/models.py及旧求解器。主实验使用两个本地计算进程。根HTML未修改。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')
    print(json.dumps({k:val[k] for k in ('runs','completed','readback_max','evaluation_double_max_relative_change','observed_order_range','common_passing_anchors')},indent=2))

if __name__=='__main__':main()
