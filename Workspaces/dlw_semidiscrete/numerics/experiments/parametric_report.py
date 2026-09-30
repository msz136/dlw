"""Generate the new research report from actual data, preserving prior reports."""
from parametric_study import ROOT,OUT,PARAMS,save
from parametric_assess import read,at
import numpy as np
import os
os.environ.setdefault('MPLCONFIGDIR',str(OUT/'mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import statistics
from parametric import Exact

FIG=ROOT/'figures'
def fmt(x):return f'{x:.3e}'
def pct(x):return f'{100*x:.3g}%'
def table(headers,rows):return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']*len(headers))+'|\n'+'\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n'
def label(c):return ('SD' if c['model']=='structure' else 'FD')+('/C' if c['closure']=='compatible' else '')+('/B' if c.get('balanced') else '')
def same(p,q):return all(p[k]==v for k,v in q.items())

def route1_summary():
    base=ROOT/'out/moving_mesh'
    geometry=json.loads((base/'route1_geometry.json').read_text(encoding='utf-8'))
    coupled=json.loads((base/'route1_coupled.json').read_text(encoding='utf-8'))
    perturb=json.loads((base/'route1_perturb.json').read_text(encoding='utf-8'))
    cost=json.loads((base/'route1_cost.json').read_text(encoding='utf-8'))
    transport=json.loads((base/'route1_transport.json').read_text(encoding='utf-8'))
    transport_dt=json.loads((base/'route1_transport_dt.json').read_text(encoding='utf-8'))
    dlw_gate=json.loads((base/'route1_dlw_gate.json').read_text(encoding='utf-8'))
    lookup={(r['parameter_id'],r['model'],r['T'],r['mode']):r
            for r in coupled['runs']}
    def ratios(t,mode,base_mode,field):
        values=[]
        for pid in ('P1','P2','P7','P10'):
            for model in ('structure','fd'):
                a=lookup[pid,model,t,mode]['observations'][-1][field]
                b=lookup[pid,model,t,base_mode]['observations'][-1][field]
                values.append(a/b)
        return f'{statistics.median(values):.3f}；{sum(v<1 for v in values)}/8 降低'
    rows=[]
    for t in (.02,.04):
        rows.append([f'{t:.2f}',ratios(t,'static_adaptive','uniform','u_error'),
                     ratios(t,'static_adaptive','uniform','v_error'),
                     ratios(t,'moving','static_adaptive','u_error'),
                     ratios(t,'moving','static_adaptive','v_error')])
    geo_rows=[]
    for case in geometry['cases']:
        r=next(row for row in case['rows'] if row['D']==2)
        a=r['metrics']['moving_gram_oracle'];b=r['metrics']['frozen_gram']
        geo_rows.append([case['parameter_id'],f"{a['u']/b['u']:.3f}",
                         f"{a['v']/b['v']:.3f}"])
    bad=sum(r['status']!='complete' for r in coupled['runs'] if r['T']==.08)
    refmax=max(row['reference_check'][field]['relative']
               for row in perturb['rows'] for field in ('u','v'))
    costs=[]
    for pid in ('P1','P7'):
        for model in ('structure','fd'):
            sub={r['mode']:r['median_seconds'] for r in cost['rows']
                 if r['parameter_id']==pid and r['model']==model}
            costs.append(sub['moving']/sub['static_adaptive'])
    tr={(r['parameter_id'],r['nx'],r['mode']):r for r in transport['runs']}
    transport_rows=[];strong=[]
    for pid in ('P1','P2','P7','P10'):
        a=tr[pid,128,'moving']['observations'][-1]
        b=tr[pid,128,'static_adaptive']['observations'][-1]
        transport_rows.append([pid,f"{a['u_common_error']/b['u_common_error']:.3f}",
                               f"{a['v_common_error']/b['v_common_error']:.3f}",
                               f"{a['u_node_error']/b['u_node_error']:.3f}",
                               f"{a['v_node_error']/b['v_node_error']:.3f}"])
        strong.append(pid if all(
            tr[pid,nx,'moving']['observations'][-1][f'{field}_common_error']/
            tr[pid,nx,'static_adaptive']['observations'][-1][f'{field}_common_error']<.8
            for nx in (64,128,256) for field in ('u','v')) else None)
    dtmax=max(v['relative'] for r in transport_dt['rows']
              for v in r['error_metric_changes_at_D2'].values())
    gate_max=max(r['last_checked']['D'] for r in dlw_gate['runs'])
    return rf'''## 路线一：共同 x 网格的初始加密与持续移动

由守恒密度 \(\rho_j=1-(v_j-\delta_0u_j)/4\) 与有限 \(h\) Gram 坐标势构造所有 \(y\) 层共用的 \(x\) 网格。数值实验必须分开两个问题：**精确场经过位移后，移动节点能否更好地采样；实际耦合推进能否保持足够准确，并把这种几何作用转为 \(u,v\) 误差收益。**详细构造、逐组结果和失败记录见[路线一专题](MOVING_MESH_ROUTE1_REPORT.md)。

在有限 \(h\) **精确场采样几何**实验中，以 \(\mathcal D=|p-q|T/\ell\) 衡量位移相对初始波宽。\(\mathcal D=2\) 时，同点数的移动 Gram / 初始冻结 Gram 三次样条重建误差如下；四组的两场都降低，但该网格由精确轨道驱动，不能算作求解器误差结果。

{table(['参数','u 比值','v 比值'],geo_rows)}

实际场实验固定 \(h=.125,n_x=128,\Delta t=.000125\)，四组参数 × SD/FD，两模型内部各比较均匀、初始加密冻结、每个 RK4 级持续移动、每 0.01 重分布。对相同有限 \(h\) Gram 真值的最大误差，比值中位数及降低组数为：

{table(['T','冻结/均匀 u','冻结/均匀 v','移动/冻结 u','移动/冻结 v'],rows)}

初始重分布有短时收益；持续移动相对冻结网格没有一致额外 \(u,v\) 收益。\(T=.04\) 的共同物理 \(x\) 点复核也给出接近 1 的移动/冻结比值。最远 \(T=.08\) 只移动约 0.036–0.109 个波宽，32 组中有 {bad} 组提前停止或状态失败，其余部分也已有较大场误差；尚未达到几何实验显示稳定收益的约一个波宽。FD 的有限 \(h\) Gram 参照不是其精确解，故这里只比较每个模型自身的网格方案。

高频非零扰动的 8 组短时响应对照均完成；各模型 \(n_x=384/512\) 参照最大相对差异为 {100*refmax:.3f}%，移动相对冻结仍接近 1。SD/FD 生成网格轨迹的自重放状态差为 0，交叉重放未显示短时网格来源的结构独占收益。与相同点数、初始最小点距的平滑梯度监控相比，Gram 网格也没有全参数最优保证。固定方案不收取每个 RK 级的监控计算后，P1/P7 的持续移动/冻结中位成本比为 {min(costs):.2f}–{max(costs):.2f}。

**长距离场推进的单独检验：** 为排除“只有精确场重采样有效”，另把有限 \(h\) Gram \(u,v\) 剖面当初态，数值求解受控输运方程 \(z_t+(p-q)z_x=0\)。监控密度由当前数值场计算，冻结与移动从完全相同的初始节点出发；在 801 个共同物理点以及各自节点上，对照精确平移剖面。位移两个波宽、\(n_x=128\) 的移动/冻结场误差比值：

{table(['参数','共同点 u','共同点 v','自身节点 u','自身节点 v'],transport_rows)}

若把“两场都至少降低 20%”作为描述性幅度门槛，{', '.join(x for x in strong if x)} 在 \(n_x=64,128,256\) 全部满足，P10 不满足；48 条轨道全部完成。自身节点误差也下降，排除了纯粹由末时刻插值造成的解释。\(n_x=128\) 时间步减半后两场误差指标最大相对变化 {dtmax:.2e}。**这个结果验证移动网格在受控输运方程中的长距离场收益，不是 DLW 的长距离场收益。** 原 DLW 全耦合方程另按两场各 1% 初始峰值的观察门槛试图推进至一个波宽；四参数 × SD/FD × 冻结/移动的 16 条轨道均在位移不超过 {gate_max:.3f} 个波宽时首次未通过。因此当前 DLW 求解器仍没有可验证的长距离移动场收益；精确几何、受控输运和原 DLW 是三个不同的证据层次。

![精确场几何收益与实际耦合误差](figures/fig19_route1_mesh.png)
![受控输运长距离场误差与 DLW 短时门槛](figures/fig20_route1_transport.png)

原始数据与源码哈希见 [`route1_validation.json`](out/moving_mesh/route1_validation.json)；这一专题没有修改原生产求解器、Gram 或 Lean。
'''.replace(r'\(', '$').replace(r'\)', '$')

def interval_summary():
    path=ROOT/'out/moving_mesh/interval_validation.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    study=json.loads((ROOT/'out/moving_mesh/interval_study.json').read_text(encoding='utf-8'))
    p2={r['interval_D_requested']:r for r in study['runs']
        if r['parameter_id']=='P2' and r['nx']==128 and r['dt_nominal']==.001}
    def sum_defect(r,kind):
        key='u_propagation_defect' if kind=='propagation' else 'u_exact_interpolation_defect'
        rows=r['segment_defects'] if kind=='propagation' else r['events']
        return sum(x[key] for x in rows)
    rows=[]
    for r in data['all_parameter_medians_nx128']:
        rows.append([f"{r['interval_D']:.4g}",
                     f"{r['median_u_ratio']:.3f}",f"{r['median_v_ratio']:.3f}",
                     f"{r['both_fields_lower_count']}/16",
                     f"{r['both_fields_20pct_lower_count']}/16"])
    dt=data['checks']['max_dt_halving_relative_metric_change']
    return f'''## 路线一延伸：重分布间隔如何影响误差

详细实验、逐次插值误差记录与精确逐段误差递推见[重分布间隔专题](MESH_REFRESH_INTERVAL_REPORT.md)。令间隔为波移动的宽度数；无穷大表示只在初始布点，随后冻结。定期方案与冻结方案从**完全相同的初始节点和场**出发。在受控输运方程中推进两个波宽，终点不做额外重映射。16 组正则参数、128 个 x 点的最终共同物理点误差相对冻结网格为：

{table(['间隔/波宽','u 中位比','v 中位比','两场降低','两场至少降低 20%'],rows)}

较频繁的重分布通常有效，但不是越频繁越好：P2/P10 在 1/4 或 1/2 附近达到本扫描的较小误差，继续缩短间隔反而变差；P7 到 1/16 仍改善。另对 P1/P2/P7/P10 在 64/128/256 点全档复核；名义时间步减半的最终四项误差指标最大相对变化为 {dt:.2e}。16 组中包含相位变化而形状相近的参数，计数不是统计独立样本或显著性检验。184 条受控输运轨道全部完成，间隔为两个波宽与冻结结果逐项完全一致。

原 DLW 的 40 条 SD/FD 短时轨道仅推进到 T=.04。P1/P7 在双场 1% 精度门槛内，但刷新带来的差别只有几个百分点且方向不一；P2/P10 此时不通过门槛。**因此，本表量化的是受控输运中的长距离间隔效应，不能称作原 DLW 的长距离最优刷新间隔。**逐段精确误差恒等式将固定网格推进缺陷与每次重映射的插值缺陷分离。P2 从间隔 1/4 缩到 1/16 时，u 的逐段推进缺陷最大范数之和由 {sum_defect(p2[.25],'propagation'):.5f} 增到 {sum_defect(p2[.0625],'propagation'):.5f}，插值缺陷之和却由 {sum_defect(p2[.25],'interpolation'):.5f} 降到 {sum_defect(p2[.0625],'interpolation'):.5f}。因此过密刷新变差不能一概归因于插值次数；新网格也会改变后续差分误差。缺少统一稳定性条件时，仍不能推出通用最优值。

![受控输运的重分布间隔扫描](figures/fig21_mesh_refresh_interval.png)

原始数据、源码及图像哈希见 [`interval_validation.json`](out/moving_mesh/interval_validation.json)。
'''

def main():
    scan=read('parametric_scan');finite=read('parametric_finite_h');assess=read('parametric_assessment');op=read('parametric_open')
    oc=read('parametric_open_controls');parameter_sweep=read('parametric_open_parameter_sweep')
    for g in op:
        c=next(c for c in oc if c['pars']==g['pars'] and c['mode']==g['mode'] and c['eps']==g['eps'])
        g['controls']['y']=c['y'];g['controls']['dt']=c['dt']
    parameter_keys={tuple(sorted(p.__dict__.items())):f'P{i+1}' for i,p in enumerate(PARAMS)}
    all_open=op+parameter_sweep
    def pid(g):return parameter_keys[tuple(sorted(g['pars'].items()))]
    def method_values(g,t,field):
        values={}
        for v in g['variants']:
            key=('SD' if v['config']['model']=='structure' else 'FD')+(' balanced' if v['config']['balanced'] else ' raw')
            obs=at(v['comparison'],t)
            values[key]=obs[field]['relative_response_error'] if obs else None
        return values
    def control_values(g,t,field):
        obs=[at(g['controls'][k],t) for k in ('x','y','dt','model')]
        return [o[field]['relative_response_error'] for o in obs] if all(o is not None for o in obs) else None
    def ref_peak(g,t,field):
        # Original open study: ref[2]; expanded sweep: ref[3]. Both are the
        # balanced FD solution at h=1/64, nx=512, dt=1/16000.
        index=3 if 'parameter_id' in g else 2
        array=np.load(OUT/g['references'][index]['file'])
        k=0 if field=='u' else 1
        matches=np.flatnonzero(abs(array['times']-t)<1e-12)
        return float(np.max(abs(array['fields'][matches[0],k]))) if len(matches) else None
    def error_table(groups,field,t=.01):
        rows=[]
        for g in groups:
            values=method_values(g,t,field);controls=control_values(g,t,field)
            peak=ref_peak(g,t,field)
            rows.append([pid(g),g['mode'],f"{g['eps']:.0e}",fmt(peak) if peak is not None else '—']+
                        [pct(values[k]) if values[k] is not None else '—' for k in ('SD raw','SD balanced','FD raw','FD balanced')]+
                        [pct(sum(controls)) if controls else '—'])
        return table(['参数','方向','幅度','参照峰值','SD 原','SD 平衡','FD 原','FD 平衡','参照检查和'],rows)
    low=sorted([g for g in all_open if g['mode']=='low' and g['eps']==.001],key=lambda g:int(pid(g)[1:]))
    other=sorted([g for g in op if g['mode'] in ('high','vonly') and g['eps']==.001],key=lambda g:(int(pid(g)[1:]),g['mode']))
    amplitude=sorted([g for g in op if pid(g)=='P1' and g['mode'] in ('low','high')],key=lambda g:(g['mode'],g['eps']))
    assert len(low)==10 and len(other)==6 and len(amplitude)==4
    quality_rows=[]
    for g in low:
        u=control_values(g,.01,'u');v=control_values(g,.01,'v')
        quality_rows.append([pid(g),g['pars']['a'],g['pars']['p'],g['pars']['q'],g['pars']['rho']]+
                            ([pct(sum(u)),pct(v[0]),pct(v[1]),pct(v[2]),pct(v[3]),pct(sum(v)),
                              '通过' if sum(u)<.05 and sum(v)<.05 else '未通过'] if u and v else ['—']*6+['未到达']))
    quality_table=table(['参数','a','p','q','ρ','u 检查和','v x','v y','v Δt','v 模型','v 检查和','5% 检查'],quality_rows)
    parameter_gates=[]
    for g in low:
        for t in (.005,.01):
            sums={field:(sum(control_values(g,t,field)) if control_values(g,t,field) else None) for field in ('u','v')}
            parameter_gates.append({'parameter_id':pid(g),'t':t,'mode':g['mode'],'eps':g['eps'],
                                    'reference_check_sums':sums,
                                    'passed':all(value is not None and value<.05 for value in sums.values())})
    save('parametric_parameter_gates',parameter_gates)
    # A compact fixed-scale chart of balanced response errors across all ten backgrounds.
    fig,ax=plt.subplots(1,2,figsize=(12,5.8),layout='constrained')
    for k,field in enumerate(('u','v')):
        matrix=np.array([[100*method_values(g,.01,field)[key] for key in ('SD balanced','FD balanced')] for g in low])
        lo,hi=((-3.5,0) if field=='u' else (-1,1))
        im=ax[k].imshow(np.log10(np.maximum(matrix,1e-8)),aspect='auto',vmin=lo,vmax=hi,cmap='YlOrRd')
        ax[k].set_title(field+' response discrepancy (%)')
        ax[k].set_xticks((0,1),('SD balanced','FD balanced'))
        ax[k].set_yticks(range(10),[pid(g) for g in low])
        for i in range(10):
            for j in range(2):ax[k].text(j,i,f'{matrix[i,j]:.2g}',ha='center',va='center',fontsize=8,color='black')
        fig.colorbar(im,ax=ax[k],label='log10(percent)',shrink=.8)
    fig.savefig(FIG/'fig14_parameter_perturbation_matrix.png',dpi=170);plt.close(fig)
    maxlin=max(r['linear_v_relative_mismatch'] for s in scan for r in s['history'])
    original=[s for s in scan if s['config']['model']=='structure' and s['config']['closure']=='original']
    boundary=sum(abs(s['history'][0]['v_peak_y'])>1.25 for s in original)
    tab=[]
    scales=[]
    for i,p in enumerate(PARAMS):
        pars=p.__dict__;vals=[]
        exact=Exact(p,.125);xx=np.linspace(-20,20,20001);uu=abs(exact.uv([0],xx,0)[0][0])
        above=xx[uu>=max(uu)/2];width=above[-1]-above[0]
        endpoints=exact.uv(np.arange(-12,12),[-10,10],0)
        mismatch=max(float(np.max(abs(z[:,1]-z[:,0]))) for z in endpoints)
        scales.append([f'P{i+1}',f'{width:.3f}',f'{width/(20/256):.1f}',abs(p.p-p.q),f'{exact.chi/.125:.3f}',fmt(mismatch)])
        for model in ('structure','fd'):
            r=next(s for s in scan if same(s['config']['pars'],pars) and s['config']['nx']==256 and s['config']['h']==.125 and s['config']['model']==model and s['config']['closure']=='original')['history'][0]
            vals.extend([fmt(r['u']),fmt(r['v']),f"{r['v_peak_y']:.3f}"])
        tab.append([f'P{i+1}',p.a,p.p,p.q,p.rho]+vals)
    # Parameter map: absolute errors and the reported peak locations.
    fig,ax=plt.subplots(1,2,figsize=(11,4))
    for mo,color in [('structure','tab:blue'),('fd','tab:orange')]:
        rows=[next(s for s in scan if s['config']['pars']==p.__dict__ and s['config']['nx']==256 and s['config']['h']==.125 and s['config']['model']==mo and s['config']['closure']=='original')['history'][0] for p in PARAMS]
        for j,k in enumerate(('u','v')):ax[j].semilogy(range(1,11),[r[k] for r in rows],'o-',label=mo,color=color);ax[j].set_title(k+' error, t=.005');ax[j].set_xlabel('parameter set');ax[j].legend()
    fig.tight_layout();fig.savefig(FIG/'fig11_parameter_errors.png',dpi=160);plt.close(fig)
    # Predictive relative mismatch for both physical fields, all parameter configs.
    fig,ax=plt.subplots(1,2,figsize=(11,4))
    for mo,cl,mark in [('structure','original','o'),('structure','compatible','x'),('fd','original','+')]:
        rows=[r for s in scan if s['config']['model']==mo and s['config']['closure']==cl for r in s['history']]
        for j,f in enumerate(('u','v')):
            ax[j].loglog([r[f] for r in rows],[max(r['linear_'+f+'_relative_mismatch'],1e-12) for r in rows],mark,alpha=.4,label=mo+'/'+cl)
            ax[j].set_xlabel(f+' actual error');ax[j].set_ylabel('forced-linear relative mismatch');ax[j].legend(fontsize=7)
    fig.tight_layout();fig.savefig(FIG/'fig12_forced_prediction.png',dpi=160);plt.close(fig)
    # Open vs fixed-ghost refined model disagreement, with explicit full/interior split.
    fig,ax=plt.subplots(1,2,figsize=(11,4));openrows=[]
    for i,g in enumerate(op):
        r=at(g['controls']['model'],.01)
        if r:
            openrows.append([i+1,g['pars']['a'],g['pars']['p'],g['mode'],g['eps'],fmt(r['u']['relative_response_error']),fmt(r['v']['relative_response_error']),fmt(r['v']['interior_error'])])
            ax[0].semilogy(i+1,r['v']['relative_response_error'],'o',color='tab:green')
        fixed=next((s for s in assess if s['pars']==g['pars'] and s['mode']==g['mode'] and s['eps']==g['eps']),None)
        if fixed:
            fr=at(fixed['controls']['model_agreement'],.01)
            if fr:ax[0].semilogy(i+1,fr['v']['relative_response_error'],'x',color='tab:red')
        for v in g['variants']:
            vr=at(v['comparison'],.01)
            if vr:ax[1].semilogy(i+1,vr['v']['relative_response_error'],'o' if v['config']['balanced'] else 'x',color='tab:blue' if v['config']['model']=='structure' else 'tab:orange')
    ax[0].set_title('Refined SD/FD disagreement: fixed (red), open (green)');ax[1].set_title('Coarse v discrepancy to refined FD: balanced o, raw x')
    for a in ax:a.set_xlabel('perturbation group');a.set_ylabel('relative response discrepancy')
    fig.tight_layout();fig.savefig(FIG/'fig13_boundary_perturbations.png',dpi=160);plt.close(fig)
    fdpass=sum(d['fd_resolution_gate'] for g in assess for d in g['gates']);joint=sum(d['joint_gate'] for g in assess for d in g['gates'])
    # Open reference checks have their own criteria; report passes without erasing failures.
    ogates=[]
    for g in op:
        for t in (.005,.01):
            cc=[at(g['controls'][k],t) for k in ('x','y','dt','model')]
            passed=all(c is not None for c in cc) and all(sum(c[f]['relative_response_error'] for c in cc)<.05 for f in ('u','v'))
            ogates.append({'pars':g['pars'],'mode':g['mode'],'eps':g['eps'],'t':t,'passed':bool(passed)})
    (OUT/'parametric_open_gates.json').write_text(json.dumps(ogates,indent=2),encoding='utf-8')
    fp=[]
    for i,p in enumerate(PARAMS):
        rr=[next(s for s in finite if s['pars']==p.__dict__ and s['h']==h)['result'] for h in (.25,.125,.0625)]
        fp.append([f'P{i+1}']+[f"{2*h*r['v']/max(r['u'],1e-30):.3f}" for h,r in zip((.25,.125,.0625),rr)])
    costpath=OUT/'parametric_cost.json'
    costtext='受控重复计时尚未完成；并行扫描中的 seconds 仅作运行记录，不用于方法效率结论。'
    if costpath.exists():
        cost=read('parametric_cost');costtext=table(['模型','边界','背景平衡','推进秒数中位数','重复次数'],[[r['model'],r['closure'],r['balanced'],f"{np.median(r['seconds']):.4f}",len(r['seconds'])] for r in cost])
    report=f'''# 参数相关的 u/v 误差、边界重构与扰动计算

2026-09-23。本轮研究覆盖两种模型、正则单孤子参数族及非解族扰动。核心结果是：**固定右幽灵值与累积重构会产生显式的边界放大；背景缺陷修正与边界相容处理分别作用于误差注入和误差传播。**新增二次外推属于新的边界近似，不能计作原固定边界问题的等价改进。

## 1. 范围、参数及实验口径

10 组参数覆盖 a=2/3/4/6、不同 p/q、ρ 的十倍变化以及较接近正则区边缘的背景；均检查 p−a<−h/2、q+a>h/2、p+q>0、ρ>0。它们是定向参数研究，不是所有正则参数或任意初值的穷尽。P1/P2 对应此前 A/B，其他行扩展其范围。改变 p/q 的联合算例不能解释为单一参数的因果效应。

主扫描：10 参数 × 3 档 h × 2 档 nx × 3 模型/闭合组合 = {len(scan)} 组，全部完成到 T=.02；这仅指推进完成。共同连续初边值、L=20、y 半宽 1.5、RK4 dt=.000125。四个观察时刻为 .005/.010/.015/.020。另有 30 组有限 h 精确背景推进、360 个离散缺陷样本、18 组时间/扩域控制，以及原/改进扰动实验。无过滤、附加阻尼或内部精确解重置。

下表是共同连续参照在 h=.125、nx=256、t=.005 的绝对误差及 v 最大误差位置。

{table(['编号','a','p','q','ρ','SD u','SD v','SD 峰值 y','FD u','FD v','FD 峰值 y'],tab)}

![参数误差](figures/fig11_parameter_errors.png)

为区分参数作用和实际分辨率，以下另列 h=.125 时 j=0 的 u 半高全宽（密集采样近似）、每波宽 x 网格数、固定 j 速度绝对值、格点相位斜率及解析场两端周期不匹配。小尾部不匹配也是该周期实现缺陷的一部分，不能从参数扫描中自动排除。

{table(['参数','u 波宽','每波宽点数 nx256','|p−q|','logχ/h','x 两端不匹配'],scales)}

实际误差随 a、波形与位置变化；同一网格下宽度与采样改变也参与其中。该表支持参数相关性，不能单独支持全参数区域的单调规律或结构模型全面优越。

## 2. 重构放大的精确定位

令 ε 是 P 误差，ω 是 W 误差，n 为内点数，ℓ=(n−1)h。相同基值下 η_j=hΣ ε_i，故 ||η||∞≤ℓ||ε||∞。内部 δ₀η 等于相邻 ε 的平均，右端却等于 −Σ_(i=1…n−2)ε_i/2。因此原物理输出满足

    ||e_v||∞ ≤ ||ω||∞ + max(1,(n−2)/2)||ε||∞。

这是精确算子关系；1/h 的最坏放大在固定物理长度的右端，而非所有内部格点。{len(original)} 个原结构配置中，{boundary} 个在首个观察时刻的 v 峰值位于 |y|>1.25。FD 直接推进 v，没有相同输出放大，但 δ₀u 仍进入其演化，因此也必须分析边界传播。

有限 h 精确背景的独立推进给出下列 2h E_v/E_u；接近 1 仅是实测尺度关系，不把不同位置的最大值当逐点恒等式。

{table(['参数','h=.25','h=.125','h=.0625'],fp)}

原半离散的外侧 P 独立给定；将其改成由当前内部 u 与同一幽灵 u 推导的相容值，只修正一个边界通量，**并不消除上述累加重构项**。原方案与这一候选均完整保留。

## 3. 受迫误差预测与参数相关理论估计

沿采样背景构造 r=F(Z̄)−Z̄_t，解析求时间导数，代数展开雅可比 A。推进 eL_t=AeL+r，并与独立的完整非线性推进误差比较。全部主扫描观察点中，v 的最大相对预测偏差为 {maxlin:.4%}。这是短时、小误差范围的预测结果，不是长期线性近似定理。

![受迫线性预测](figures/fig12_forced_prediction.png)

理论文件 [PARAMETRIC_THEORY.md](PARAMETRIC_THEORY.md) 给出精确二次误差方程、传播算子表示、对数范数界和参数显式的 K/C 上界。9 组小网格完整雅可比/冻结传播算子检查及 18 组新边界精化检查独立验证范数估计。冻结矩阵指数不是非自治孤子传播算子。严格上界通常远比受迫数值预测保守，不能混用。

## 4. 未知扰动：共同数据与参照失败记录

三个背景 × 三种扰动方向/频率 × 两档幅度 = 18 组。扰动在 y 内部紧支撑，x 用高斯包络乘余弦；包含低频、高频和仅 v 扰动。未来扰动轨道不输入算法。每组比较原 SD、仅外侧 P 相容 SD、仅背景平衡 SD、两者结合 SD、原 FD、背景平衡 FD。

初次同时加密 x/y 的 nx=1024 参照存在提前失败或更差结果，保留原数组与日志。随后采用固定 h 加密 x、固定 x 加密 h、时间步减半和两模型交叉对照。插值使用严格插值的张量三次样条；初版比较的迭代插值绝对容差不适合微小扰动，已从原始场重新评估，权威比较为 parametric_assessment.json，原比较字段仅保留历史。

在共 {2*len(assess)} 个“参数/扰动/幅度/时刻”中，FD 的分辨率对照误差和小于响应幅度 1% 的有 {fdpass} 个；同时通过两模型差异低于 5% 的联合检查有 {joint} 个。这是有限观察的经验门槛，不是严格参考解误差界。未过联合门槛时，表中相对于细 FD 的数值只能称为差异，不能当作已确证的连续真解误差。

零扰动被平衡算法保持是构造性质。背景平衡在共同连续背景下还会修正半离散的有限 h 模型缺陷，不能宣称它在有限 h 上完全保持原方程。原固定右幽灵条件下，即使背景缺陷消除，非零扰动的右端差异仍可能显著；全域和固定内部区域分别记录，未裁掉边界后宣布成功。

## 5. 二次外推的相容边界：两模型同步改进

候选规则是右幽灵扰动 η_n=3η_(n−1)−3η_(n−2)+η_(n−3)，叠加解析背景值。两模型采用完全相同的物理边界近似。此时右端 δ₀η=1.5ε_(n−1)−0.5ε_(n−2)，所以输出范数从 O(n) 降为 2；光滑扰动的边界导数近似为二阶。

利用离散乘积恒等式，还可获得固定 Δx、固定链长且背景有界时不随 h 加密发散的局部 K/C 估计。**这不消除 Δx 高频增长，也不保证长期稳定。**边界改变的作用与背景缺陷修正分别测试，不能归为同一个因素。

新边界原有 {len(op)} 组扰动对照包含 P1、P2、P10 的低频/高频/仅 v 方向及 P1 的幅度对照。本次再固定低频和幅度 .001，补齐 P3–P9 共 {len(parameter_sweep)} 组，以隔离背景参数的变化。这样**低频表覆盖全部 10 组背景**；高频和仅 v 方向各覆盖三组代表背景，不能将其外推到其他七组。所有粗网格方法均用 h=.125、nx=256、dt=.000125，观察 t=.01；其余 t=.005 数据在 JSON 中。

下表的每个数是扰动全域最大范数差异

    100 × ||响应_粗网格 − 响应_细FD参照||∞ / ||响应_细FD参照||∞。

细参照采用同一新边界的背景平衡 FD，h=.015625、nx=512、dt=.0000625；不同 y 格点由严格三次样条映射到粗格点。**u、v 各按自身的参照响应峰值归一化**；仅 v 初始扰动的 u 响应很小，故其百分数可能很大。原/平衡表示有无背景缺陷修正，SD/FD 表示两种模型；四列始终使用共同的初始物理扰动与边界规则。最后一列是 x、y、时间步及模型四项参照检查的相对差异之和，它是经验诊断量，**不是严格误差上界**。

先看固定低频扰动下的参数变化（幅度 .001，t=.01）。

**u 响应的相对差异**

{error_table(low,'u')}

**v 响应的相对差异**

{error_table(low,'v')}

![十组参数的扰动对照](figures/fig14_parameter_perturbation_matrix.png)

图 14 仅画平衡方法的低频结果，颜色为百分差异的对数，格内保留原始百分数。表中保留未经背景平衡的结果，避免只展示改进成功的配置。参数 P3/P4 改变 a，P8/P9 改变 ρ；P5/P6/P7/P10 还改变波宽或正则性裕量。它们是定向比较，不能由单一表格辨认所有参数之间的交互作用。

这十组低频背景里，平衡 FD 的 u 数值差异在十组均小于平衡 SD；平衡 SD 的 v 数值差异在九组较小，P10 则由 FD 较小。**这些是表中数值的排序，不是经过严格误差界认证的胜率。**例如 P1 的 v 为 SD 0.597%、FD 0.759%，两者相差 0.162 个百分点，而该行的参照检查和为 0.198%；不能据此认定 SD 在 P1 的 v 上有可靠优势。P10 的 v 则为 SD 2.91%、FD 0.886%，该行检查和为 0.226%，显示这一参数下优势方向确实可能反转。固定同一扰动，P3/P4 与 P1 的比较体现 a 改变的影响；P8/P9 的较小变化体现 ρ 移动孤子后有限域误差的变化。它们仍限于当前网格和观察时刻。

再看 P1、P2、P10 的高频及仅 v 初始扰动，设置及参照与上表相同。这一表检验方法对扰动方向的敏感性，不把“所有参数”与“所有扰动方向”混为一组全因子试验。

**高频／仅 v：u 响应**

{error_table(other,'u')}

**高频／仅 v：v 响应**

{error_table(other,'v')}

P1 的幅度缩小十倍另作重复；完整四方法和参照检查如下，不能将“相对差异接近”误读成一般扰动线性定理。

{error_table(amplitude,'v')}

P1 低频的未平衡 SD 在幅度从 .001 降到 .0001 时，v 相对差异从 4.31% 增至 41.6%；平衡 SD 约为 0.597%，两档基本一致。这与原方案的背景缺陷相对扰动变得更大的解释相符；高频一行也显示平衡后仍保留显著误差，说明修正背景不能代替扰动的空间分辨率。

参照检查的各项也应透明展示。以下为十组低频背景在 t=.01 的各项百分差异；只有两场检查和均低于 5% 才称为“通过参照交叉检查”。通过表示参照之间一致，**不表示任一粗网格方法的误差小于 5%**。

{quality_table}

原有 {len(op)} 组在 t=.005/.01 共 {len(ogates)} 个观察中，通过这项参照检查的有 {sum(g['passed'] for g in ogates)} 个；低频十组参数共 {len(parameter_gates)} 个观察中通过 {sum(g['passed'] for g in parameter_gates)} 个。后者逐时刻判断见 `out/parametric_parameter_gates.json`。该检查不能证明细 FD 等于真实连续解，尤其当不同离散方法共同存在系统性偏差时。

为了直接观察边界机制，以下另列原有 11 组在 t=.01 的**细网格两模型响应差异**。这是 SD 与 FD 彼此的差异，不是上方粗网格对细参照的误差；完整全域/内部误差、其他时刻保存在 JSON。

{table(['组','a','p','扰动','幅度','u 相对差异','v 相对差异','v 内部绝对差异'],openrows)}

![边界与扰动对照](figures/fig13_boundary_perturbations.png)

图中蓝/橙为 SD/FD，圆点为背景平衡、叉号为原演化；左图比较原固定幽灵与新边界下的细网格两模型差异。两种边界定义不同问题，跨边界图用于机制研究；同一边界内的方案才是直接方法对照。

具体例子：P1 低频、幅度 .001、t=.01，细网格 v 差异从原固定幽灵条件下约 26% 降到新边界下约 0.075%。新边界粗网格的 SD 原推进/背景平衡相对细 FD 参照的 v 差异约为 4.31%/0.597%，FD 的相应值约为 4.75%/0.759%。这支持该例中的改进，不表示所有指标都由 SD 获胜；其他组按上表和原始对照逐项判断。

## 6. 成本、结论与研究边界

{costtext}

本轮已将数值主线从 A/B 验证推进到“参数相关缺陷 → 受迫误差增长 → 右端重构放大 → 共同边界改进”。理论给出了可检查的放大关系和条件性估计，实验同时包括有限差分、半离散及两者的背景平衡版本。**不预设半离散模型优于 FD，也不把通用背景修正的作用独占归因于半离散结构。**

结论限于所测正则单孤子背景附近、指定有限区域和短时扰动。一般初值适定性、长距离传播和完整两孤子数值散射仍不在本轮完成范围。新闭合的局部二阶一致性与范数控制也不能替代完整初边值问题的收敛定理。

## 7. 复现与证据

新增实现与实验均在 lib/parametric*.py 和 experiments/parametric*.py，未修改原生产 solver、Gram 实现或 Lean。先执行 study、bounds、controls、perturb、reference、open_study、open_bounds，再执行 assess、cost、report、validate。运行环境使用应用提供的 Python，SciPy/mpmath 安装于 numerics/.research_deps；见 [PARAMETRIC_RUN.md](PARAMETRIC_RUN.md)。

原始数据 out/parametric_*.json、parametric_*.npz、perturb_*.npz；每次失败日志保留。最终验收、源码/产物哈希与范围见 [parametric_validation_manifest.json](out/parametric_validation_manifest.json)。旧报告保留于下方附录及原文件。
'''
    (ROOT/'PARAMETRIC_REPORT.md').write_text(report,encoding='utf-8')
    backup=ROOT/'PRE_PARAMETRIC_REPORT_20260923.md'
    if not backup.exists():backup.write_bytes((ROOT/'REPORT.md').read_bytes())
    old=backup.read_text(encoding='utf-8')
    multi=(ROOT/'MULTISOLITON_REPORT.md').read_text(encoding='utf-8')
    manifold=(ROOT/'MANIFOLD_SCATTERING_REPORT.md').read_text(encoding='utf-8')
    injection='''## 固定网格 SD：误差注入、传播放大与配置规则

新[专题报告](INJECTION_AMPLIFICATION_REPORT.md)以有限 h Gram 精确场为背景，将实际 RK4 求解误差逐步分成一步注入、线性传播和后验非线性余项。P5 在 h=1/8、T=.01 从 nx=256 加到 512 时，u/v 误差由 8.40e-7/3.97e-7 增到 4.12e-3/2.51e-3；步长减半影响低于 0.1%，高频传播占主导。P10 在所测配置主要受有限 h 模型差控制。原固定幽灵与二次外推闭合的对照是不同边界问题。

解析模型差加初始缺陷的配置规则先锁定，再对 T=.01 的四组及 T=.02 的两组全新谱参数共 36 个候选真实推进。六个锁定建议都通过双场各 0.1% 门槛；T=.01 有三个保守的通过/失败误判，H1 因此多付约 1.72 倍推进时间，计入六候选诊断后为 2.57 倍。T=.02 的 H6 有五个候选实际误差超过预测量，故该量不是跨时间保守上界，规则也尚非成本最优。N2 的三个独立短时窗口与匹配 N1 控制已检查；完整碰撞轨道未验收。数据、两个锁定文件、源码哈希及 163 项检查见 [`out/injection_amplification/`](out/injection_amplification/validation.json)。移动网格仍待原 DLW 固定网格可信传播约一个波宽后继续。
'''
    (ROOT/'REPORT.md').write_text(report+'\n\n'+injection+'\n\n'+route1_summary()+'\n\n'+interval_summary()+'\n\n'+multi.replace('# Gram 两孤子结构','## Gram 两孤子结构',1)+'\n\n'+manifold.replace('# 路线 3：','## 路线 3：',1)+'\n\n## 历史附录：此前的动力学与基础验收\n\n'+old.replace('# 从精确半离散结构到可验证的孤子动力学','### 从精确半离散结构到可验证的孤子动力学',1),encoding='utf-8')
    print('report generated',len(scan),len(assess),len(op),'parameter sweep',len(parameter_sweep),flush=True)

if __name__=='__main__':main()
