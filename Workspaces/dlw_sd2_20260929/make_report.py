import json
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run_sd2 import OUT,HERE,BASE,previous

def main():
    oldpath=BASE/'dlw_time_curves_20260928/out/results.json'
    old=json.loads(oldpath.read_text())['runs']
    new=json.loads((OUT/'results.json').read_text())['runs']+json.loads((OUT/'controls.json').read_text())['runs']
    assert len(new)==28
    rows=[];readback=0.;eval_change=0.
    for r in old+new:
        assert previous.sha(r['profile'])==r['profile_sha256']
        assert r['status']=='completed' and len(r['history'])==41
        s=r['spec'];ref=previous.PaperExact(previous.CASES[s['case']],s['h'],True)
        js=np.arange(-round(1.5/s['h']),round(1.5/s['h']))
        assert r['moved_steps']==(0 if s['mesh']=='fixed' else round(.02/s['dt']))
        with np.load(r['profile']) as z:
            for h in r['history']:
                t=h['t'];xx=np.linspace(-10,10,4001);ee=ref.uv(js,xx,t)
                for f,e in zip(('u','v'),ee):
                    cs=CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)
                    err=float(abs(cs(xx)-e).max());readback=max(readback,abs(err-h['errors'][f]))
                    rows.append(dict(case=s['case'],model=s['model'],mesh=s['mesh'],variant=s['variant'],nx=s['nx'],h=s['h'],dt=s['dt'],t=t,field=f,error=err))
                    if s['model']=='SD2' and s['variant']=='main' and t in (0.,.01,.02):
                        xxx=np.linspace(-10,10,8001);ev=ref.uv(js,xxx,t)[0 if f=='u' else 1]
                        er=float(abs(cs(xxx)-ev).max());eval_change=max(eval_change,abs(er/err-1))
    assert readback<1e-12
    previous.csvout(OUT/'error_time_all.csv',rows)
    def get(case,model,mesh,variant='main'):
        return next(r for r in old+new if all(r['spec'][k]==v for k,v in dict(case=case,model=model,mesh=mesh,variant=variant).items()))
    def err(r,t):return next(h['errors'] for h in r['history'] if abs(h['t']-t)<1e-12)
    table=[];init=[];control=[];time_changes=[]
    for case in previous.CASES:
        for mesh in ('fixed','moving'):
            for t in (0.,.01,.02):
                row=dict(case=case,mesh=mesh,t=t)
                for name,model in (('SD','structure'),('SD2','SD2'),('FD','fd')):
                    e=err(get(case,model,mesh),t)
                    row.update({name+'_'+f:e[f] for f in ('u','v')})
                table.append(row)
            for pair in (('main','time_half'),('x_half','x_half_time_half')):
                a,b=[get(case,'SD2',mesh,p) for p in pair]
                change=max(abs(hb['errors'][f]/ha['errors'][f]-1) for ha,hb in zip(a['history'],b['history']) for f in ('u','v'))
                time_changes.append(dict(case=case,mesh=mesh,pair='/'.join(pair),maximum_relative_error_change=change))
            base=get(case,'SD2',mesh)
            ref=previous.PaperExact(previous.CASES[case],.125,True)
            scales=[abs(v).max() for v in ref.uv(np.arange(-12,12),np.linspace(-10,10,4001),0.)]
            with np.load(base['profile']) as zb:
                for variant in ('time_half','x_half','y_half','domain_double','xy_half'):
                    r=get(case,'SD2',mesh,variant)
                    with np.load(r['profile']) as z:
                        for t in (.005,.01,.02):
                            for f,scale in zip(('u','v'),scales):
                                xx=np.linspace(-10,10,4001)
                                bv=CubicSpline(zb[f't{t:g}_x'],zb[f't{t:g}_{f}'],axis=-1)(xx)
                                vv=CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(xx)
                                if len(z['y'])!=len(zb['y']):vv=CubicSpline(z['y'],vv,axis=0)(zb['y'])
                                diff=float(abs(vv-bv).max());e=err(r,t)[f];be=err(base,t)[f]
                                control.append(dict(case=case,mesh=mesh,variant=variant,t=t,field=f,error=e,base_error=be,field_difference=diff,initial_peak=float(scale),relative_field_difference=diff/scale,pass_old_threshold=bool(max(e,be)/scale<=.01 and diff/scale<=.001)))
    previous.csvout(OUT/'comparison.csv',table);previous.csvout(OUT/'control_comparisons.csv',control)
    previous.csvout(OUT/'time_checks.csv',time_changes)
    mainrows=[r for r in rows if r['variant']=='main']
    schemes=[('structure','SD','#D55E00'),('SD2','SD2','#009E73'),('fd','FD','#0072B2')]
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
    fig,axes=plt.subplots(2,2,figsize=(12,7.6),sharex=True,layout='constrained')
    for i,case in enumerate(previous.CASES):
        for j,f in enumerate(('u','v')):
            ax=axes[i,j]
            for model,name,color in schemes:
                for mesh,style in (('fixed','-'),('moving','--')):
                    r=get(case,model,mesh);ts=[h['t'] for h in r['history']];es=[h['errors'][f] for h in r['history']]
                    ax.plot(ts,es,color=color,ls=style,lw=1.8,label=f'{name} / {mesh}')
            ax.set_yscale('log');ax.set_xlim(0,.02);ax.set_xticks([0,.005,.01,.015,.02]);ax.axvline(.01,color='.7',ls=':',lw=.7)
            ax.set_xlabel('Time t');ax.set_ylabel(f'Maximum absolute {f} error');ax.grid(alpha=.2)
            ax.set_title(f"Paper Fig. 1({'a' if i==0 else 'b'}), (a,p,q)={'(2,1,2)' if i==0 else '(2,4,-3)'}")
    handles,labels=axes[0,0].get_legend_handles_labels();fig.legend(handles,labels,loc='outside upper center',ncol=3,frameon=False)
    fig.supxlabel('SD2: Eq. (21), including initial reconstruction error. Spatial controls do not validate all SD2 curves to t=0.02.',fontsize=9)
    for ext in ('png','pdf','svg'):fig.savefig(HERE/f'comparison_vs_time.{ext}',dpi=200)
    plt.close(fig)
    checks=dict(new_runs=28,reused_runs=16,profile_hashes_verified=44,readback_max=readback,evaluation_double_relative_change_at_anchors=eval_change,max_time_relative_change=max(r['maximum_relative_error_change'] for r in time_changes),old_results_sha256=previous.sha(oldpath),common_passing_anchors=[t for t in (.005,.01,.02) if all(r['pass_old_threshold'] for r in control if r['t']==t)])
    previous.dump(OUT/'validation.json',checks)
    tlines=[]
    for r in table:
        if r['t']==0:continue
        vals=[' / '.join(f"{r[name+'_'+f]:.6e}" for f in ('u','v')) for name in ('SD','SD2','FD')]
        tlines.append(f"| {r['case']} | {r['mesh']} | {r['t']:.2f} | "+' | '.join(vals)+' |')
    ilines=[]
    for r in table:
        if r['t']!=0:continue
        ilines.append(f"| {r['case']} | {r['mesh']} | {r['SD2_u']:.6e} | {r['SD2_v']:.6e} |")
    clines=[]
    for case in previous.CASES:
        for mesh in ('fixed','moving'):
            for variant in ('main','x_half','y_half','xy_half','domain_double'):
                e=err(get(case,'SD2',mesh,variant),.02)
                clines.append(f"| {case} | {mesh} | {variant} | {e['u']:.6e} | {e['v']:.6e} |")
    report='''# SD2：Report 第21式的独立数值实现

## 范围与结论

按用户要求新增 SD2，直接推进第21式的 Q,R，通过第22式恢复 u,v。保留旧 SD、FD 作为对照，不覆盖旧数据、不改HTML。固定原文图1(a) a=2,p=1,q=2 与图1(b) a=2,p=4,q=-3；均 c1=1、零相位。后者原图t=0，正时间演化是本项目扩展。

SD2在连续x层面是旧SD的变量改写，不是已证明的另一种可积模型。有限差分不满足精确乘积/商法则，所以完全离散实现可以有不同误差。主配置中SD2没有显示相对旧SD的稳定双场优势；空间加密对部分结果影响较大，不能宣称SD2具有已验证的整体精度优势或劣势。

## 方程与闭合（必须随结果引用）

令 w=QR，H=h²(w²-1)/4，A_j=(M_j+M_{j+1})_x。直接计算

    Q_t = -Dxx Q - 2a Dx Q - (A+H) Q
    R_t =  Dxx R - 2a Dx R + (A+H) R
    M_{j+1,x} - M_{j,x} = -h Dx(QR)
    u = 2 Dx(Q)/Q; v = 4(1-QR) + Dy(u)

由第三式累加恢复 M_x；M 本身含不影响方程的纯t常数。下边界 Q_0(x,t)由连续解析tau比值给定（只在最低y层），利用其 Q_t 固定累加常数，使最低层Q方程成立。其余Q与全部R独立演化。R无需y外侧值。v重构的下u ghost用解析边界，上ghost用背景相对二次外推。这与旧SD固定最低层u的边界在连续x层面相容，但有限x差分下恢复u边界有O(dx^4)差异；不能称严格同离散边界的单因素实验。

Q的左右远场是1和k=exp(gamma0)，R是1和1/k。对Q/R采用加性远场延拓 f(x+L)=f(x)+jump，分别jump=k-1、1/k-1；对一阶导数再应用零跳跃D1得到D2。不能对原始Q/R直接周期回绕。四阶中心D1与旧求解器同阶；在动网格上Dx=J^{-1}Dxi。扩域控制用于检查远场闭合影响。

初始Q取连续tau比值；初始QR=1-(v_exact-Dy u_exact)/4，与旧SD的连续初值监测量一致。由于离散Dx(Q)/Q不精确等于连续u，SD2恢复的初始u,v有误差，表中完整保留。没有将精确内部场重置，没有滤波、阻尼、解析缺陷强迫；解析数据只用于初值、y边界和误差参照。

持续动格沿用相同的密度及速度公式：监测密度为mean_y(QR)，通量为mean_y((u+2a)QR-Dx(QR)-2a)，V=(flux-flux_left)/density；每个RK级联合推进Q,R、节点，并加V Dx(Q)、V Dx(R)。初始节点与旧SD/FD动格相同，此后根据各自场演化，节点轨迹不强行一致。固定组V=0。

## 配置与核对

主配置RK4，dt=.000125，nx256、x∈[-20,20)、h=.125、24个y中点层；评价x∈[-10,10]、4001点，三次样条重构后跨x及全部y层取最大绝对误差。t=0…0.02每.0005保存一次。旧SD/FD沿用已核对的16条轨道，新增28条SD2轨道（四组合×七配置）。

控制：时间减半；nx512配dt=.0000625；再减细网格时间步；h减半；x/y同时加密；L80且nx512保持dx。所有28条完成，固定组节点不动，动格每步更新。独立读回44份原始场和全部误差，并核对哈希；详细数值见out/validation.json。

check_equations.py做两类验证：(1)光滑制造场第21式到第7式的差分残差随x加密约四阶；(2)将独立有限h精确tau的Q,R和解析时间导数代入实际SD2 RHS，在两参数与固定/变形坐标下均得到约四阶残差下降。共18项配置。这验证方程实现的一致性，不是完全离散可积性的证明。

此前旧SD/FD在t=.02的共同检查不能自动转移给SD2。当前图保留相同时间范围以便对照；SD2未在所有空间控制上满足此前“总误差≤初峰1%、场差≤初峰0.1%”标准。尤其图1(a)动格x加密后终点误差增大，不能只凭小时间步就称可靠。完整控制失败同样保留，不选择有利分辨率替换主结果。

## 主表（每格 u / v 最大绝对误差）

| 原文参数 | 网格 | t | SD | SD2 | FD |
|---|---|---:|---:|---:|---:|
'''+ '\n'.join(tlines)+'''

## SD2初始重构误差（未扣除）

| 参数 | 网格 | u | v |
|---|---|---:|---:|
'''+ '\n'.join(ilines)+'''

## SD2空间控制，t=.02

| 参数 | 网格 | 配置 | u | v |
|---|---|---|---:|---:|
'''+ '\n'.join(clines)+'''

## 交付

- comparison_vs_time.png/pdf/svg：六条方案误差时间曲线，含初始重构误差。
- out/comparison.csv：t=0/.01/.02，SD/SD2/FD的u/v并列表。
- out/error_time_all.csv：主与控制完整误差曲线。
- out/control_comparisons.csv：公共物理点评价、y插值到共同层、旧门槛的逐项通过/失败。
- out/results.json、controls.json、*.npz：28条SD2轨道及原始Q/R/u/v/节点；validation.json、time_checks.csv、equation_checks.json：核对。

建议下步首先针对SD2的Q/R初值到物理场的重构与边界闭合做一致性改进，再判断是否存在优势。不能将本次主表的差异单独归因为可积性，也不能将旧SD可靠终点直接标为SD2可靠终点。
'''
    (HERE/'HANDOFF.md').write_text(report,encoding='utf-8')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
