"""Common-u/v SD2: independent readback, before/after, matched baselines."""
import json
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_corrected import HERE,OUT,SOURCES,old
from reference import CASES,TwoExact
io=old.previous

def main():
    data=json.loads((OUT/'results.json').read_text(encoding='utf-8'));new=data['runs'];assert len(new)==68
    for path,digest in data['sources'].items():assert io.sha(path)==digest,path
    previous=[]
    for path in SOURCES:
        d=json.loads(path.read_text(encoding='utf-8'))
        for r in d['runs']:
            r=dict(r,spec=dict(r['spec'],method='Euler' if 'euler' in str(path) else 'RK4'))
            previous.append(r)
    baseline=[r for r in previous if r['spec']['model']!='SD2'];combined=baseline+new
    for r in previous+new:assert io.sha(r['profile'])==r['profile_sha256']
    def get(method,case,model,mesh,variant='main',old_sd2=False):
        rr=previous if old_sd2 else combined
        return next(r for r in rr if all(r['spec'][k]==v for k,v in dict(method=method,case=case,model=model,mesh=mesh,variant=variant).items()))
    def snap(r,t):return next((h for h in r['history'] if abs(h['t']-t)<1e-12),None)
    def grid(s):return np.linspace(-s['eval_half'],s['eval_half'],8001 if s['case']=='fig5' else 4001)
    def field(z,t,f,xx,y=None):
        a=CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(xx)
        if y is not None and len(y)!=len(z['y']):a=CubicSpline(z['y'],a,axis=0)(y)
        return a
    rows=[];before=[];initial=[];readback=0.;lower_boundary=0.;eval_change=0.;scales={};controls=[];orders=[]
    for case in CASES:
        s=get('RK4',case,'SD','fixed')['spec'];g=TwoExact(CASES[case],.125)
        scales[case]=dict(zip(('u','v'),[float(abs(a).max()) for a in g.uv(np.arange(-12,12),np.linspace(-s['eval_half'],s['eval_half'],16001),0.)]))
    for r in new:
        s=r['spec'];ref=TwoExact(CASES[s['case']],s['h']);js=np.arange(-round(1.5/s['h']),round(1.5/s['h']))
        p=get(s['method'],s['case'],'SD2',s['mesh'],s['variant'],old_sd2=True)
        b=get(s['method'],s['case'],'SD',s['mesh'],s['variant'])
        if s['mesh']=='fixed':assert r['moved_steps']==0
        elif r['status']=='completed':assert r['moved_steps']==round(.02/s['dt'])
        xx=grid(s)
        with np.load(r['profile']) as z,np.load(b['profile']) as zb:
            diffs={f:float(abs(z['t0_'+f]-zb['t0_'+f]).max()) for f in ('x','u','v')}
            assert max(diffs.values())<1e-10,diffs
            initial.append(dict(method=s['method'],case=s['case'],mesh=s['mesh'],variant=s['variant'],**diffs))
            for h in r['history']:
                t=h['t'];exact=ref.uv(js,xx,t)
                bu=ref.uv([js[0]],z[f't{t:g}_x'],t)[0][0]
                lower_boundary=max(lower_boundary,float(abs(z[f't{t:g}_u'][0]-bu).max()))
                for f,e in zip(('u','v'),exact):
                    err=float(abs(field(z,t,f,xx)-e).max());readback=max(readback,abs(err-h['errors'][f]))
                    rows.append(dict(method=s['method'],case=s['case'],model='SD2',mesh=s['mesh'],variant=s['variant'],t=t,field=f,error=err))
                    ph=snap(p,t)
                    if ph:before.append(dict(method=s['method'],case=s['case'],mesh=s['mesh'],variant=s['variant'],t=t,field=f,old_SD2_error=ph['errors'][f],common_uv_SD2_error=err,new_over_old=err/ph['errors'][f]))
                    if s['variant']=='main' and t in (0.,.01,.02):
                        x2=np.linspace(xx[0],xx[-1],2*len(xx)-1);ee=ref.uv(js,x2,t)[0 if f=='u' else 1]
                        err2=float(abs(field(z,t,f,x2)-ee).max());eval_change=max(eval_change,abs(err2/err-1))
    assert readback<1e-12 and lower_boundary<1e-10
    table=[]
    for method in ('RK4','Euler'):
        for case in CASES:
            for mesh in ('fixed','moving'):
                for t in (0.,.01,.02):
                    row=dict(method=method,case=case,mesh=mesh,t=t)
                    for model in ('SD','SD2','FD'):
                        h=snap(get(method,case,model,mesh),t)
                        row.update({model+'_'+f:h['errors'][f] if h else None for f in ('u','v')})
                    table.append(row)
                for model in ('SD','SD2','FD'):
                    main=get(method,case,model,mesh);xx=grid(main['spec'])
                    variants=['time_half','x_half','y_half','domain_double']
                    if method=='Euler':variants.append('time_quarter')
                    if case=='fig4' and mesh=='moving':variants.append('x_half_time_half')
                    with np.load(main['profile']) as z0:
                        for variant in variants:
                            r=get(method,case,model,mesh,variant)
                            with np.load(r['profile']) as z:
                                for t in (.001,.005,.01,.02):
                                    h=snap(main,t);hc=snap(r,t)
                                    for f in ('u','v'):
                                        if h and hc:
                                            diff=float(abs(field(z0,t,f,xx)-field(z,t,f,xx,z0['y'])).max())
                                            er=hc['errors'][f];base=h['errors'][f]
                                            passed=bool(max(er,base)/scales[case][f]<=.01 and diff/scales[case][f]<=.001)
                                        else:diff=er=base=None;passed=False
                                        controls.append(dict(method=method,case=case,model=model,mesh=mesh,variant=variant,t=t,field=f,main_error=base,control_error=er,field_difference=diff,initial_peak=scales[case][f],pass_old_threshold=passed))
                a=get('Euler',case,'SD2',mesh);b=get('Euler',case,'SD2',mesh,'time_half');c=get('Euler',case,'SD2',mesh,'time_quarter')
                if method=='Euler':
                    with np.load(a['profile']) as z1,np.load(b['profile']) as z2,np.load(c['profile']) as z4:
                        for t in (.01,.02):
                            if not all(snap(r,t) for r in (a,b,c)):continue
                            for f in ('u','v'):
                                va,vb,vc=[field(z,t,f,grid(a['spec'])) for z in (z1,z2,z4)]
                                da=float(abs(va-vb).max());db=float(abs(vb-vc).max())
                                orders.append(dict(case=case,mesh=mesh,t=t,field=f,dt_vs_half=da,half_vs_quarter=db,order=float(np.log2(da/db))))
    for filename,rr in (('comparison.csv',table),('SD2_before_after.csv',before),('SD2_error_time.csv',rows),('initial_uv_matching.csv',initial),('control_comparisons.csv',controls),('Euler_time_order.csv',orders)):
        io.csvout(OUT/filename,rr)
    status=[dict(**r['spec'],status=r['status'],reached=r['reached'],reason=r['reason']) for r in new];io.csvout(OUT/'status.csv',status)
    passing=[dict(method=method,case=case,model=model,mesh=mesh,anchors=[t for t in (.001,.005,.01,.02) if all(r['pass_old_threshold'] for r in controls if r['method']==method and r['case']==case and r['model']==model and r['mesh']==mesh and r['t']==t)]) for method in ('RK4','Euler') for case in CASES for model in ('SD','SD2','FD') for mesh in ('fixed','moving')]
    v=dict(new_SD2_runs=len(new),completed=sum(r['status']=='completed' for r in new),reused_SD_FD_runs=len(baseline),old_SD2_comparison_runs=len(previous)-len(baseline),profile_hashes_verified=len(previous)+len(new),new_error_values_readback=len(rows),readback_max=readback,initial_uv_node_match_max=max(max(r[f] for f in ('x','u','v')) for r in initial),lower_u_boundary_error_max=lower_boundary,evaluation_double_max_relative_change=eval_change,Euler_order_range=[min(r['order'] for r in orders),max(r['order'] for r in orders)],boundary_linear_residual_max=max(r['boundary_solve_max_residual'] for r in new),passing_anchors=passing)
    io.dump(OUT/'validation.json',v)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    colors={'SD':'#D55E00','SD2':'#009E73','FD':'#0072B2'}
    for method in ('RK4','Euler'):
        fig,axes=plt.subplots(3,2,figsize=(12,10.5),sharex=True,layout='constrained')
        for i,case in enumerate(CASES):
            for j,f in enumerate(('u','v')):
                ax=axes[i,j]
                for model in ('SD','SD2','FD'):
                    for mesh,style in (('fixed','-'),('moving','--')):
                        r=get(method,case,model,mesh)
                        ax.plot([h['t'] for h in r['history']],[h['errors'][f] for h in r['history']],color=colors[model],ls=style,lw=1.8,label=f'{model} / {mesh}')
                ax.set_yscale('log');ax.set_xlim(0,.0202);ax.set_xticks([0,.005,.01,.015,.02]);ax.axvline(.01,color='.6',ls=':',lw=.7)
                ax.set_xlabel('Time t');ax.set_ylabel(f'Maximum absolute {f} error');ax.grid(alpha=.2);ax.set_title(f'Paper Fig. {case[-1]}, {method}: common u,v initialization')
        handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False)
        fig.supxlabel('SD2: discrete u/v lift + consistent lower u boundary. Total error retained. Spatial controls in report.',fontsize=9)
        for ext in ('png','svg'):fig.savefig(HERE/f'{method.lower()}_error_vs_time.{ext}',dpi=180)
        plt.close(fig)
    def fmt(x):return '未到达' if x is None else f'{x:.6e}'
    mainlines=[]
    for r in table:
        if r['t']==0:continue
        mainlines.append(f"| {r['method']} | {r['case']} | {r['mesh']} | {r['t']:.2f} | "+' | '.join(' / '.join(fmt(r[m+'_'+f]) for f in ('u','v')) for m in ('SD','SD2','FD'))+' |')
    beforelines=[]
    for method in ('RK4','Euler'):
        for case in CASES:
            for mesh in ('fixed','moving'):
                a=snap(get(method,case,'SD2',mesh,old_sd2=True),.02);b=snap(get(method,case,'SD2',mesh),.02)
                if not a or not b:continue
                beforelines.append(f"| {method} | {case} | {mesh} | "+' | '.join(' / '.join(f"{h['errors'][f]:.6e}" for f in ('u','v')) for h in (a,b))+' |')
    passlines=[f"| {r['method']} | {r['case']} | {r['mesh']} | {', '.join(map(str,r['anchors'])) or '无'} |" for r in passing if r['model']=='SD2']
    report=f'''# SD2：统一离散u/v初始化与相容边界后的复算

## 范围与变化

本轮针对当前三组原文零背景二孤子（图3/4/5），重跑SD2的fixed/moving、RK4/Euler及对应控制，共68条；复用136条SD/FD轨道。旧68条SD2数据保留作前后对照，不覆盖历史数据。未另跑此前单孤子算例，也未纳入图6周期背景。

图3参数(a,p1,q1,p2,q2)=(2,6,-5,4,-3)，图4=(2,1,2,4,-3)，图5=(2,7/4,-5/3,1,-4/5)，c1=c2=1、相位全零。所有物理参数、主分辨率、时间步和评价区间与上一轮一致。

此次同时修改**初始离散逆变换**与**最低y层物理边界的一致性**。不能将全部前后变化仅归因于初始化；没有改变第21式内部Q/R方程，没有扣减E(0)，没有内部精确场重置。

## 离散逆变换

共用SD/FD的离散u0,v0及初始节点。在各y层，求Q0和远场跳跃k，使

    Dxi Q + b k = (J u0 / 2) Q,    Q_left = 1,
    R0 = [1 - (v0 - Dy u0)/4] / Q0.

Dxi为原四阶周期中心差分，b为加性远场跳跃进入该差分的系数，Dx=J^-1 Dxi；k是额外未知量而非强行固定的解析跳跃。用稀疏带边界线性系统联立解Q,k。验收检查正Q、正右远场及实际2DxQ/Q恢复残差。没有用连续积分替代离散反求，也没有只覆盖输出的初始u/v。

24种不同参数/网格/分辨率初值配置全部通过，最大初始物理场误差约1.6e-12。正式68轨道与对应SD初态（含控制组）逐点对比最大差为{v['initial_uv_node_match_max']:.3e}。初始三次样条误差仍存在，但各方案共用；不再有SD2独有的Q/R采样到u/v转换误差。

## 持续边界与动网格

每个RK/Euler级只在最低y层反求给定物理u边界对应的Q；内部Q/R直接按第21式演化。固定Q_left=1规范，对离散边界方程求导。移动坐标上

    A [Q_dot, k_dot] = [(J_dot u + J(u_t+V u_x)) Q / 2, 0],
    J_dot = Dxi V,    Q_t_physical = Q_dot - V Dx Q.

边界u_t,u_x由解析边界数据计算。Q_t_physical用于闭合M_x的积分常数，内部照常加ALE传输项。右远场各y层按最低层右远场的共同时间因子变化，R远场取倒数，保证QR远场为1；没有一边更新Q边界、一边保留不相容旧跳跃。

6组固定/移动坐标的边界方向差分核对通过；18组实际内部RHS对有限h精确二孤子时间导数核对仍呈约四阶x残差下降，见implementation_checks.json。正式轨道保存时刻的最低层u对共同物理边界的最大差{lower_boundary:.3e}；边界线性恢复残差最大{v['boundary_linear_residual_max']:.3e}。

## 配置与验证

主dt=.000125、h=.125、y∈[-1.5,1.5]的24个中点层。图3/4为L40,nx256、评价[-10,10]4001点；图5为L640,nx1024、评价[-100,100]8001点。动网格初始节点与旧方案一致，随后按当前场的共同监测公式持续更新。

RK4共31条：六主/半时间步/细x/细y/扩域各6条，图4moving细x再减半时间步1条。Euler共37条，另加六个四分之一时间步配置。{v['completed']}/68条完成至.02；失败或停止也保留。控制仍看.001/.005/.01/.02主/控制总误差≤初峰1%、场差≤初峰0.1%，只表示有限数值检查。

新轨道{len(rows)}项误差独立读回差{readback:.3e}，新旧272份原始场哈希核对通过。主锚点评价点加倍最大相对变化{eval_change:.3e}。新SD2的Euler三步长公共场差观测阶范围{v['Euler_order_range'][0]:.4f}–{v['Euler_order_range'][1]:.4f}。时间阶不以总误差比计算；RK4不被当作连续精确解。

## 更新主表（每格u / v总误差）

| 时间法 | 原图 | 网格 | t | SD | SD2：统一uv | FD |
|---|---|---|---:|---:|---:|---:|
'''+ '\n'.join(mainlines)+'''

## SD2修正前后，t=.02（每格u / v）

| 时间法 | 原图 | 网格 | 原SD2 | 统一uv及边界后 |
|---|---|---|---:|---:|
'''+ '\n'.join(beforelines)+'''

## 新SD2通过全部控制的采样时刻

| 时间法 | 原图 | 网格 | 通过锚点 |
|---|---|---|---|
'''+ '\n'.join(passlines)+'''

## 结论口径与交付

初始化干扰已消除到舍入/线性求解容差，但不能据此预设SD2更优。图3Euler旧SD2主配置中的u优势在本次修正后不再优于FD；图4误差降低但仍须看空间控制。新SD2与SD连续x层面的等价不意味着完全差分后的乘积/商法则或Euler时间误差相同。

- rk4_error_vs_time.png/svg、euler_error_vs_time.png/svg：更新后的六方案时间误差曲线。
- out/comparison.csv：两时间法的SD/新SD2/FD双场并列表，含t=0/.01/.02。
- out/SD2_before_after.csv：所有匹配轨道/时刻/物理量的旧SD2与新SD2误差和比值。
- out/initial_uv_matching.csv：68轨道初值逐点对齐检查；SD2_error_time.csv：新曲线全部误差。
- out/control_comparisons.csv、Euler_time_order.csv、status.csv、validation.json：控制、时间阶和状态。
- out/results.json、out/RK4/*.npz、out/Euler/*.npz：新参数/源码哈希、场和节点；旧SD/FD引用原文件并核对哈希。
- consistent_sd2.py、verify.py、implementation_checks.json：实际实现与一致性核对；probe_lift.py是保留的初步反求检查。

复现顺序verify.py → run_corrected.py → make_report.py。初始数据、边界与演化误差分开说明，不将改边界后的结果当成仅换初值的严格单因素实验。根HTML、旧求解器与旧数据均未修改。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')
    print(json.dumps({k:v[k] for k in ('new_SD2_runs','completed','readback_max','initial_uv_node_match_max','lower_u_boundary_error_max','evaluation_double_max_relative_change','Euler_order_range')},indent=2))

if __name__=='__main__':main()
