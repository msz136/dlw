"""Compare saved fields under independent numerical-setting changes."""
import json
import numpy as np
from scipy.interpolate import CubicSpline
import reliability as study

def main():
    d=json.loads((study.OUT/'results.json').read_text());assert len(d['runs'])==48
    by={tuple(r['spec'][k] for k in ('case','model','mesh','variant')):r for r in d['runs']}
    comparisons=[];table=[];accepted=[];checks=0
    for r in d['runs']:
        assert study.previous.sha(r['profile'])==r['profile_sha256'];checks+=1
    for case in study.previous.CASES:
        for model in ('structure','fd'):
            for mesh in ('fixed','moving'):
                base=by[case,model,mesh,'base']
                ref=study.previous.PaperExact(study.previous.CASES[case],.125,True)
                js=np.arange(-12,12);xx=np.linspace(-10,10,4001)
                peaks=np.array([np.max(abs(v)) for v in ref.uv(js,xx,0.)])
                valid=[]
                with np.load(base['profile']) as zb:
                    for t in (.005,.01,.02,.05):
                        b=next((v for v in base['history'] if abs(v['t']-t)<1e-12),None)
                        if b is None:continue
                        bfields=np.array([CubicSpline(zb[f't{t:g}_x'],zb[f't{t:g}_{f}'],axis=-1)(xx) for f in ('u','v')])
                        good=max(b['errors'][f]/pk for f,pk in zip(('u','v'),peaks))<=.01
                        for variant in ('time_half','x_half','y_half','y_quarter','domain_double'):
                            r=by[case,model,mesh,variant];snap=next((v for v in r['history'] if abs(v['t']-t)<1e-12),None)
                            row=dict(case=case,model=model,mesh=mesh,t=t,variant=variant,available=snap is not None,u_error=None,v_error=None,u_change_over_peak=None,v_change_over_peak=None)
                            if snap is None:good=False;comparisons.append(row);continue
                            with np.load(r['profile']) as z:
                                values=np.array([CubicSpline(z[f't{t:g}_x'],z[f't{t:g}_{f}'],axis=-1)(xx) for f in ('u','v')])
                                if len(z['y'])!=len(zb['y']):values=CubicSpline(z['y'],values,axis=1)(zb['y'])
                            diff=np.max(abs(values-bfields),axis=(1,2))/peaks
                            reference=ref.uv(js,xx,t)
                            err=np.array([np.max(abs(v-e)) for v,e in zip(values,reference)])
                            row.update(u_error=float(err[0]),v_error=float(err[1]),u_change_over_peak=float(diff[0]),v_change_over_peak=float(diff[1]))
                            good=bool(good and max(diff)<=.001 and max(err/peaks)<=.01)
                            comparisons.append(row)
                        if good:valid.append(t)
                        table.append(dict(case=case,model=model,mesh=mesh,t=t,u_error=b['errors']['u'],v_error=b['errors']['v'],passes_checks=good))
                accepted.append(dict(case=case,model=model,mesh=mesh,passing_sample_times=valid))
    study.previous.csvout(study.OUT/'control_comparisons.csv',comparisons);study.previous.csvout(study.OUT/'main_errors.csv',table)
    common=sorted(set.intersection(*(set(r['passing_sample_times']) for r in accepted)))
    long=[r for r in d['runs'] if r['spec']['variant']=='domain_double']
    summary=dict(profiles_verified=checks,acceptance_definition='Every tested configuration error <=1% of initial exact field peak; every field change from base on common points <=0.1% of same peak',accepted=accepted,common_passing_sample_times=common,domain_double_t1_success=sum(r['status']=='completed' for r in long),domain_double_stop_times=[dict(case=r['spec']['case'],model=r['spec']['model'],mesh=r['spec']['mesh'],reached=r['reached'],status=r['status'],reason=r['reason']) for r in long])
    study.previous.dump(study.OUT/'summary.json',summary)
    chosen=max(common) if common else .005
    lines=[f"| {r['case']} | {r['model']} | {r['mesh']} | {r['u_error']:.6e} | {r['v_error']:.6e} | {'通过' if r['passes_checks'] else '未通过'} |" for r in table if r['t']==chosen]
    text=f'''# DLW 原文参数不变：可靠性核对

## 结论

原文两组a/p/q/c1/零相位及连续初值均保持不变；只调整计算区间、空间分辨率和时间步。本轮48条配置全部尝试并保存。进一步将区间扩大为[-40,40)、保持dx不变的8条长时实验，到达t=1的为{summary['domain_double_t1_success']}条。**之前粗网格t=1值只作失真诊断，不能作为最终精度结论。**

本轮八种原文参数×SD/FD×固定/持续动网格组合，共同通过下面数值核对的采样时刻为：{common}。这只是本次有限配置验证，不是连续时间保证、严格误差界或一般收敛证明。

## 可操作数值设置

基准Lx=40,nx256,h_y=.125,dt=.000125,RK4；检查dt减半、nx512、h_y=.0625和.03125，以及Lx80/nx512（保持dx）。所有检查保持同一物理参数与同一PDE。前五组跑到.05，扩域组尝试到1。监测密度、ALE规则及未滤波的原方程同 ../long_moving/HANDOFF.md；边界仍为既有背景相对二次外推，x周期边界远置，未使用解析内部重置或强迫。

采用明确的报告筛选判据：在共同物理点上，各配置的u/v误差均不超过各自初始解析峰值1%，与基准数值场的差均不超过相同峰值0.1%。y网格不嵌套，先对细y场三次插值到基准y层；x场也在共同[-10,10]的4001点评价。原生层误差和读回剖面仍保留。该判据为本次数值核对口径，不是统计显著性声明。

## t={chosen:g} 主配置实测误差

| 原图 | 模型 | 网格 | u误差 | v误差 | 数值核对 |
|---|---|---|---:|---:|---|
{chr(10).join(lines)}

若某行未通过，只能引用其当前配置实测值，不纳入可靠排名。main_errors.csv列出全部采样时刻，control_comparisons.csv列出每项数值变化对场的影响，summary.json列出各组合的通过时刻和扩域停止时刻。全部48个轨道哈希已核对；没有对参数作优化或挑选新孤子。

关于t=1：不能通过继续缩小dt或选择更粗网格来证明可靠。若当前长时验收未通过，最终报告应明确“尚未获得可信t=1结果”，并以通过数值检查的共同短时结果作为已完成证据，而非补造终点表。改变方程、增加耗散或按解析解约束轨道会构成新的实验，不能与这批原方程比较混用。
'''
    (study.OUT/'HANDOFF.md').write_text(text,encoding='utf-8');print(json.dumps(summary,indent=2));print('\n'.join(lines))

if __name__=='__main__':main()
