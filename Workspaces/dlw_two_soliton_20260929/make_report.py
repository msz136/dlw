"""Read back all profiles, compare six schemes, retain failed controls."""
import json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from models import previous,BASE
from reference import CASES,TwoExact
HERE=Path(__file__).resolve().parent;OUT=HERE/'out'

def main():
    data=json.loads((OUT/'results.json').read_text(encoding='utf-8'));runs=data['runs']
    assert len(runs)==len(data['plan'])==90
    extra=json.loads((OUT/'fine_time.json').read_text(encoding='utf-8'))
    assert len(extra['runs'])==3
    runs=runs+extra['runs']
    for path,digest in data['sources'].items():assert previous.sha(path)==digest,path
    for path,digest in extra['sources'].items():assert previous.sha(path)==digest,path
    rows=[];readback=0.;eval_change=0.;time_changes=[];initial=[];tails=[]
    def get(case,model,mesh,variant='main'):
        return next(r for r in runs if all(r['spec'][k]==v for k,v in dict(case=case,model=model,mesh=mesh,variant=variant).items()))
    def snapshot(r,t):return next((h for h in r['history'] if abs(h['t']-t)<1e-12),None)
    scales={}
    for case in CASES:
        s=get(case,'SD','fixed')['spec'];g=TwoExact(CASES[case],.125)
        grid=np.linspace(-s['eval_half'],s['eval_half'],16001)
        scales[case]=dict(zip(('u','v'),[float(abs(a).max()) for a in g.uv(np.arange(-12,12),grid,0.)]))
        for t in (0.,.02):
            uv=g.uv(np.arange(-13,13),np.array([-s['L']/2,s['L']/2]),t)
            tails.append(dict(case=case,t=t,u_boundary_peak=float(abs(uv[0]).max()),v_boundary_peak=float(abs(uv[1]).max())))
    for r in runs:
        s=r['spec'];assert previous.sha(r['profile'])==r['profile_sha256']
        g=TwoExact(CASES[s['case']],s['h']);js=np.arange(-round(1.5/s['h']),round(1.5/s['h']))
        if s['mesh']=='fixed':assert r['moved_steps']==0
        elif r['status']=='completed':assert r['moved_steps']==round(.02/s['dt'])
        neval=8001 if s['case']=='fig5' else 4001
        with np.load(r['profile']) as z:
            for h in r['history']:
                t=h['t'];xx=np.linspace(-s['eval_half'],s['eval_half'],neval);exact=g.uv(js,xx,t)
                for f,e in zip(('u','v'),exact):
                    cs=CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)
                    er=float(abs(cs(xx)-e).max());readback=max(readback,abs(er-h['errors'][f]))
                    rows.append(dict(case=s['case'],model=s['model'],mesh=s['mesh'],variant=s['variant'],nx=s['nx'],L=s['L'],h=s['h'],dt=s['dt'],t=t,field=f,error=er,relative_initial_peak=er/scales[s['case']][f]))
                    if s['variant']=='main' and t in (0.,.01,.02):
                        xx2=np.linspace(-s['eval_half'],s['eval_half'],2*neval-1)
                        ee=g.uv(js,xx2,t)[0 if f=='u' else 1]
                        er2=float(abs(cs(xx2)-ee).max());eval_change=max(eval_change,abs(er2/er-1))
    assert readback<1e-12
    previous.csvout(OUT/'error_time_all.csv',rows)
    table=[];controls=[];ranking=[]
    for case in CASES:
        for mesh in ('fixed','moving'):
            # Common initial nodes, SD/FD physical fields and SD2 reconstruction.
            with np.load(get(case,'SD',mesh)['profile']) as a,np.load(get(case,'FD',mesh)['profile']) as b,np.load(get(case,'SD2',mesh)['profile']) as c:
                nodes=max(float(abs(a['t0_x']-z['t0_x']).max()) for z in (b,c))
                shared=max(float(abs(a['t0_'+f]-b['t0_'+f]).max()) for f in ('u','v'))
                assert nodes<1e-12 and shared<1e-12
                initial.append(dict(case=case,mesh=mesh,node_difference=nodes,SD_FD_initial_field_difference=shared,SD2_u_difference=float(abs(a['t0_u']-c['t0_u']).max()),SD2_v_difference=float(abs(a['t0_v']-c['t0_v']).max())))
            for t in (0.,.01,.02):
                row=dict(case=case,mesh=mesh,t=t)
                for model in ('SD','SD2','FD'):
                    h=snapshot(get(case,model,mesh),t)
                    row.update({model+'_'+f:h['errors'][f] if h else None for f in ('u','v')})
                table.append(row)
            for model in ('SD','SD2','FD'):
                main=get(case,model,mesh);s=main['spec']
                with np.load(main['profile']) as a:
                    for variant in ('time_half','x_half','y_half','domain_double'):
                        r=get(case,model,mesh,variant)
                        with np.load(r['profile']) as b:
                            for t in (.001,.005,.01,.02):
                                aa=snapshot(main,t);bb=snapshot(r,t)
                                for f in ('u','v'):
                                    scale=scales[case][f]
                                    if aa and bb:
                                        xx=np.linspace(-s['eval_half'],s['eval_half'],8001 if case=='fig5' else 4001)
                                        av=CubicSpline(a[f't{t:g}_x'],a[f't{t:g}_{f}'],axis=-1)(xx)
                                        bv=CubicSpline(b[f't{t:g}_x'],b[f't{t:g}_{f}'],axis=-1)(xx)
                                        if len(a['y'])!=len(b['y']):bv=CubicSpline(b['y'],bv,axis=0)(a['y'])
                                        diff=float(abs(av-bv).max());er=bb['errors'][f];base=aa['errors'][f]
                                        passed=bool(max(er,base)/scale<=.01 and diff/scale<=.001)
                                    else:diff=er=base=None;passed=False
                                    controls.append(dict(case=case,model=model,mesh=mesh,variant=variant,t=t,field=f,base_error=base,control_error=er,field_difference=diff,initial_peak=scale,relative_field_difference=diff/scale if diff is not None else None,pass_old_threshold=passed))
                                    if variant=='time_half' and aa and bb:time_changes.append(abs(er/base-1))
            for variant in ('main','time_half','x_half','y_half','domain_double'):
                for field in ('u','v'):
                    values={model:snapshot(get(case,model,mesh,variant),.02) for model in ('SD','SD2','FD')}
                    values={k:v['errors'][field] for k,v in values.items() if v}
                    ranking.append(dict(case=case,mesh=mesh,variant=variant,field=field,order=' < '.join(sorted(values,key=values.get))))
    previous.csvout(OUT/'comparison.csv',table);previous.csvout(OUT/'control_comparisons.csv',controls);previous.csvout(OUT/'rankings.csv',ranking)
    statuses=[dict(**r['spec'],status=r['status'],reached=r['reached'],reason=r['reason']) for r in runs]
    previous.csvout(OUT/'status.csv',statuses)
    common={case:[t for t in (.001,.005,.01,.02) if all(r['pass_old_threshold'] for r in controls if r['case']==case and r['t']==t)] for case in CASES}
    by_scheme=[dict(case=case,model=model,mesh=mesh,passing_anchors=[t for t in (.001,.005,.01,.02) if all(r['pass_old_threshold'] for r in controls if r['case']==case and r['model']==model and r['mesh']==mesh and r['t']==t)]) for case in CASES for model in ('SD','SD2','FD') for mesh in ('fixed','moving')]
    fine_checks=[]
    for model in ('SD','SD2','FD'):
        a=get('fig4',model,'moving','x_half');b=get('fig4',model,'moving','x_half_time_half')
        change=max(abs(hb['errors'][f]/ha['errors'][f]-1) for ha,hb in zip(a['history'],b['history']) for f in ('u','v'))
        fine_checks.append(dict(case='fig4',model=model,mesh='moving',max_relative_error_change=change))
    previous.csvout(OUT/'fine_time_checks.csv',fine_checks)
    validation=dict(runs=len(runs),completed=sum(r['status']=='completed' for r in runs),profile_hashes_verified=len(runs),error_values_readback=len(rows),readback_max=readback,evaluation_double_max_relative_change=eval_change,time_half_max_relative_error_change=max(time_changes),fine_time_checks=fine_checks,common_passing_anchors_by_case=common,scheme_passing_anchors=by_scheme,initial_checks=initial,exact_boundary_tails=tails,criterion='At sampled anchors only: main and each control error <=1% of each field initial peak; common-field difference <=0.1% of that peak. Numerical evidence, not strict bound or statistical significance.')
    previous.dump(OUT/'validation.json',validation)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    fig,axes=plt.subplots(3,2,figsize=(12,10.5),sharex=True,layout='constrained')
    colors={'SD':'#D55E00','SD2':'#009E73','FD':'#0072B2'}
    for i,case in enumerate(CASES):
        for j,f in enumerate(('u','v')):
            ax=axes[i,j]
            for model in ('SD','SD2','FD'):
                for mesh,style in (('fixed','-'),('moving','--')):
                    r=get(case,model,mesh);ts=[h['t'] for h in r['history']];es=[h['errors'][f] for h in r['history']]
                    ax.plot(ts,es,color=colors[model],ls=style,lw=1.8,label=f'{model} / {mesh}')
                    for t in (.01,.02):
                        h=snapshot(r,t)
                        if h:ax.plot(t,h['errors'][f],'o',color=colors[model],ms=3)
            ax.set_yscale('log');ax.set_xlim(0,.0202);ax.set_xticks([0,.005,.01,.015,.02]);ax.axvline(.01,color='.6',ls=':',lw=.7)
            ax.set_xlabel('Time t');ax.set_ylabel(f'Maximum absolute {f} error');ax.grid(alpha=.2)
            ax.set_title(f'Paper Fig. {case[-1]}: two solitons, {f}')
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False)
    fig.supxlabel('Total error includes initial reconstruction. Same parameters and evaluation window within each case; spatial controls in report.',fontsize=9)
    for ext in ('png','svg'):fig.savefig(HERE/f'error_vs_time.{ext}',dpi=180)
    plt.close(fig)
    def fmt(x):return 'not reached' if x is None else f'{x:.6e}'
    tlines=[]
    for r in table:
        if r['t']==0:continue
        vals=[' / '.join(fmt(r[m+'_'+f]) for f in ('u','v')) for m in ('SD','SD2','FD')]
        tlines.append(f"| {r['case']} | {r['mesh']} | {r['t']:.2f} | "+' | '.join(vals)+' |')
    ilines=[]
    for r in table:
        if r['t']!=0:continue
        vals=[' / '.join(fmt(r[m+'_'+f]) for f in ('u','v')) for m in ('SD','SD2','FD')]
        ilines.append(f"| {r['case']} | {r['mesh']} | "+' | '.join(vals)+' |')
    plines=[f"| {r['case']} | {r['model']} | {r['mesh']} | {', '.join(str(t) for t in r['passing_anchors']) or 'none'} |" for r in by_scheme]
    conclusion=[]
    for case in CASES:
        winners=[]
        for f in ('u','v'):
            items=[(snapshot(get(case,model,mesh),.02)['errors'][f],model,mesh) for model in ('SD','SD2','FD') for mesh in ('fixed','moving') if snapshot(get(case,model,mesh),.02)]
            e,model,mesh=min(items);winners.append(f'{f}最小为{model}/{mesh}（{e:.6e}）')
        conclusion.append(f"- {case}，t=.02主配置："+'；'.join(winners)+'。')
    maxref=max(r['reference_error'] for r in json.loads((HERE/'reference_checks.json').read_text())['independent_determinant_and_pde'])
    report=f'''# DLW 原文零背景二孤子：SD / SD2 / FD × fixed / moving

## 范围与参数

只使用原文 §3.2、图3/4/5的三组零背景二孤子。PDF印刷页7已目视核对；原文三图均为t=0，本实验从该初态推进到正时间，属于数值扩展。原文图6是周期背景上的二孤子，需要不同背景与边界，本轮不混入。

| 原图 | a | p1 | q1 | p2 | q2 | c1,c2 | 相位 |
|---|---:|---:|---:|---:|---:|---|---|
| 3 | 2 | 6 | -5 | 4 | -3 | 1,1 | 全零 |
| 4 | 2 | 1 | 2 | 4 | -3 | 1,1 | 全零 |
| 5 | 2 | 7/4 | -5/3 | 1 | -4/5 | 1,1 | 全零 |

引用：H.-H. Sheng, G.-F. Yu, Physica D 432 (2022) 133140，Paper/sources/PhysD-published.pdf，式(29)–(31)、图3–5。

## 主配置结果概览

{chr(10).join(conclusion)}

这些是当前主配置的误差排名，可靠性和空间控制见下文。特别是图4动网格的细x控制存在误差增大，不能只报主配置较小的结果。图3/5也应把u、v分别比较，不以某一个场代表全部求解质量。

## 解析参照与初值

直接使用二孤子完整tau式：g=1+exp(zeta1)/(p1+q1)+exp(zeta2)/(p2+q2)+C exp(zeta1+zeta2)，C=(p1-p2)(q1-q2)/[(p1+q1)(p1+q2)(p2+q1)(p2+q2)]；f的单项系数分别乘-(pi-a)/(qi+a)，交叉项乘二者乘积。zeta_i=(pi+qi)x+(qi²-pi²)t+[1/(pi-a)+1/(qi+a)]y。不是两个单孤子场的相加。

连续场u=2(log f-log g)_x，v=2(log f+log g)_xy；四个指数项用稳定对数求和与解析导数计算，适用于三组正tau系数。独立50位精度2×2行列式及数值符号微分核对9个点，场最大差{maxref:.3e}，连续PDE残差<1e-40。实际SD2 RHS对有限h精确二孤子Q/R时间导数的18组网格/坐标检查通过，x加密残差约四阶下降；见reference_checks.json。

SD/FD从完全相同的连续u,v和节点出发；SD2从同一连续tau比值Q=f/g及QR=1-(v-Dy u)/4出发。由于用离散Dx(Q)/Q恢复场，SD2的初始u,v不与连续采样完全相同；不扣除初始误差。本比较是三套完整实现的总误差比较，不是纯可积性或纯换变量因果实验。

## 六方案与数值设置

- SD：沿用旧两场结构半离散；FD：沿用连续方程普通交错差分；SD2：沿用Report式(21)，推进Q/R，通过式(22)恢复u/v。旧求解器源码未修改。
- fixed：均匀固定x节点；moving：相同连续初始监测密度等质量布点，Rmesh=mean_y[1-(v-Dy u)/4]，速度V=(flux-flux_left)/Rmesh，各RK级联合更新场与节点并加入ALE项；SD2内部等价地用QR。没有只在初始移动的组。
- 六方案均RK4，主dt=.000125，h=.125，24个y中点层位于[-1.5,1.5]。该横向条带沿用此前实验，未复现原论文整张二维图的全部y范围；不能用本实验判断完整远场碰撞相移。
- 图3/4：x域[-20,20)，nx256；公共评价[-10,10]、4001点。图5波形宽，扩大为x域[-320,320)，nx1024；评价[-100,100]、8001点。物理参数不变，同一算例内六方案使用完全相同数值设置。不同算例之间不作相同成本比较。
- x四阶中心D1，D2=D1∘D1；动坐标Dx=J^-1 Dxi。SD/FD周期远场截断，SD2对Q/R使用已知常数远场跳跃的加性延拓。y边界保留已有解析下边界和背景相对二次上ghost。SD2固定最低层解析Q并用它闭合M_x，其恢复u边界与旧SD仅在连续x层面相容，保留前轮的边界差异。
- 总误差：三次样条到公共物理x点评价，与连续精确解作差，再跨x和所有y层取最大绝对值。保留t=0重构误差，无滤波、阻尼、内部解析重置或缺陷强迫。

## 实验与核对结果

共93条轨道：3原文参数×3离散化×2网格×5配置，共90条；另对图4的三种动格方案，在细x网格上再次减半时间步补3条。5配置为主配置、时间步减半、x加密两倍并减半时间步、y步长减半、x域及点数同加倍保持dx。{validation['completed']}条完成至.02；所有状态与未完成原因保留在out/status.csv。主曲线含41个时刻，控制采样0/.001/.005/.01/.02。图4细网格再减半时间步的最大相对误差变化为{max(r['max_relative_error_change'] for r in fine_checks):.3e}，见fine_time_checks.csv。

{len(runs)}个原始场哈希、{len(rows)}项误差独立读回通过，最大差{readback:.3e}。所有固定组节点不动、完成的动格组每步均更新；六组初始节点一致、SD/FD初始场一致核对通过。减半时间步在控制锚点引起的误差最大相对变化{max(time_changes):.3e}；主锚点评价点数加倍最大相对变化{eval_change:.3e}。扩域同时改变动格的全域质量归一化，不能把该控制变化全部解释成边界反射。

可靠性沿用旧门槛：各场总误差≤初始精确峰值1%，主/控制公共场差≤该峰值0.1%。这是有限配置、有限时刻的数值检查，不是严格误差界、统计显著性或整个时间段的保证。三算例全部六方案的共同通过锚点为：{common}。不能把所有推进完成的值称为已收敛。

## 主表（每格u / v最大绝对误差）

| 原图 | 网格 | t | SD | SD2 | FD |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(tlines)+'''

## 初始重构误差（未扣除）

| 原图 | 网格 | SD u/v | SD2 u/v | FD u/v |
|---|---|---:|---:|---:|
'''+ '\n'.join(ilines)+'''

## 各方案通过所有控制的采样时刻

| 原图 | 方法 | 网格 | 通过锚点 |
|---|---|---|---|
'''+ '\n'.join(plines)+'''

## 交付与解释限制

- error_vs_time.png/svg：三算例、双场、六方案时间误差图；主图固定0至.02以便比较，通过状态以上表为准。
- out/comparison.csv：t=0/.01/.02的SD/SD2/FD双场并列表。
- out/error_time_all.csv、control_comparisons.csv、rankings.csv：完整主/控制误差、公共场差和不同配置的排序；status.csv含全部成功/失败。
- out/results.json、fine_time.json、*.npz：参数、源码/轨道哈希，保存的u/v/x及SD2在0/.01/.02的Q/R；validation.json与reference_checks.json：读回和解析核对。

应结合初始误差、空间控制及排序翻转读取主表。该短时二维条带实验不能支撑长期稳定、碰撞相移保持或普遍优越性；没有采样自选物理参数来寻找优势。图6周期背景不在本轮范围。

复现顺序：verify.py → run_experiments.py → refine_time.py → make_report.py。依赖NumPy、SciPy、mpmath、Matplotlib；主实验使用两个本地计算进程。已有结果按参数和源码哈希匹配后续跑，禁止用改变后的源码覆盖既有轨道。旧SD/FD包装与原MovingProblem在六个测试配置中的RHS最大差为0。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')
    print(json.dumps({k:validation[k] for k in ('runs','completed','readback_max','evaluation_double_max_relative_change','time_half_max_relative_error_change','common_passing_anchors_by_case')},indent=2))

if __name__=='__main__':main()
