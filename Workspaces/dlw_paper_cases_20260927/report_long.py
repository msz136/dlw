"""Read back all long-time fields and disclose accuracy failures explicitly."""
import json
import numpy as np
from scipy.interpolate import CubicSpline
import long_moving as s

def main():
    main=json.loads((s.OUT/'results.json').read_text());half=json.loads((s.OUT/'time_half.json').read_text())
    assert len(main['runs'])==32 and len(half['runs'])==8
    rows=[];readback_max=0.;eval_max=0.;half_max=0.;table=[];status=[]
    for r in main['runs']+half['runs']:
        assert s.previous.sha(r['profile'])==r['profile_sha256']
        spec=r['spec'];ref=s.previous.PaperExact(s.previous.CASES[spec['case']],.125,True)
        with np.load(r['profile']) as z:
            for h in r['history']:
                t=h['t'];js=np.arange(-12,12);x=z[f't{t:g}_x'];uv=[z[f't{t:g}_{f}'] for f in ('u','v')]
                measured=[]
                for size in (4001,8001):
                    xx=np.linspace(-10,10,size);exact=ref.uv(js,xx,t)
                    e={f:float(np.max(abs(CubicSpline(x,a,axis=-1)(xx)-b))) for f,a,b in zip(('u','v'),uv,exact)}
                    measured.append(e)
                readback_max=max(readback_max,*(abs(measured[0][f]-h['errors'][f]) for f in ('u','v')))
                eval_max=max(eval_max,*(abs(measured[1][f]/measured[0][f]-1) for f in ('u','v') if measured[0][f]>1e-12))
        end=r['history'][-1];peaks=[float(np.max(abs(a))) for a in ref.uv(np.arange(-12,12),np.linspace(-10,10,8001),0.)]
        good=r['status']=='completed' and all(end['errors'][f]/peak<.01 for f,peak in zip(('u','v'),peaks))
        status.append({**spec,'reached':r['reached'],'status':r['status'],'reason':r['reason'],'moved_steps':r['moved_steps'],'max_displacement':end['max_displacement'],'t1_under_1pct_both':good})
        if spec['nx']==32 and spec['dt']==.0005:
            rr=next(rr for rr in half['runs'] if all(rr['spec'][k]==spec[k] for k in ('case','model','mesh','nx')))
            if r['status']==rr['status']=='completed':
                ee=rr['history'][-1]['errors'];half_max=max(half_max,*(abs(ee[f]/end['errors'][f]-1) for f in ('u','v')))
            row=dict(case=spec['case'],model=spec['model'],mesh=spec['mesh'],u_error=end['errors']['u'] if r['status']=='completed' else None,v_error=end['errors']['v'] if r['status']=='completed' else None,initial_u_error=r['history'][0]['errors']['u'],initial_v_error=r['history'][0]['errors']['v'],u_relative_initial_peak=end['errors']['u']/peaks[0],v_relative_initial_peak=end['errors']['v']/peaks[1],status=r['status'],reached=r['reached'])
            rows.append(row)
            table.append(f"| {spec['case']} | {spec['model']} | {spec['mesh']} | {row['u_error']:.6g} | {row['v_error']:.6g} | {100*row['u_relative_initial_peak']:.2f}% / {100*row['v_relative_initial_peak']:.2f}% |" if row['u_error'] is not None else f"| {spec['case']} | {spec['model']} | {spec['mesh']} | 未到达 | 未到达 | — |")
    assert readback_max<1e-10
    s.previous.csvout(s.OUT/'t1_table.csv',rows);s.previous.csvout(s.OUT/'status.csv',status)
    validation=dict(profiles_verified=40,readback_max=readback_max,evaluation_4001_to8001_max_relative=eval_max,coarse_time_half_error_max_relative=half_max,completed=sum(r['status']=='completed' for r in status),under_1pct_both=sum(r['t1_under_1pct_both'] for r in status))
    s.previous.dump(s.OUT/'validation.json',validation)
    report=f'''# DLW 原文参数：t=1 与持续动网格

## 结果性质

**已得到两个原文参数点的固定/动网格、SD/FD四种组合的t=1数值；但粗网格误差大，不能称为可靠的长时间求解。** 全部40个试验中{validation['completed']}个推进到t=1，双场误差均低于初始峰值1%的为{validation['under_1pct_both']}个。没有筛掉提前失败的细网格结果。

## 配置与动网格

图1(a)：a2/p1/q2；图1(b)：a2/p4/q−3；c1=1、零相位，连续解析初值。图1(a)原图t=1，图1(b)原图t=0、这里的演化属于扩展。沿用本项目SD/普通交错FD，h=.125、y中点[-1.5,1.5]、背景相对二次外推y边界；共同物理x区间扩大为[-20,20)，内区[-10,10]评价。RK4；没有滤波、额外耗散、解析内部重置或精确解缺陷强迫。

动网格使用既有r_minus方案：R为各y层的[1-(v-Dy u)/4]平均，Q为[(u+2a)r-Dx r-2a]平均，节点速度V=(Q-Q_left)/R。初始按该连续监测密度等质量布点；随后各RK级从当前数值场更新速度与节点，加入ALE输运项。固定组V=0。该监测律在FD下不是声称离散精确守恒。状态均使用(P,W)或(P,v)的既有实现。独立记录每步移动次数、最小Jacobian、正密度和总位移。

尝试nx=32/64/128（dt=.0005）及256（dt=.000125），每个参数/模型/网格各4档，共32条；nx32另补dt=.00025的8条控制。更细空间网格仍可能更早停止，不能挑选能跑完的粗格来宣称收敛。

## t=1共同粗配置表

下面均nx=32、dt=.0005。每格为共同物理x点和全部y格点上的最大绝对误差；百分比除以各场初始精确峰值，并非精确误差界。最后列直接暴露失真量级。

| 原图 | 模型 | 网格 | u误差 | v误差 | 相对初始峰值 u/v |
|---|---|---|---:|---:|---:|
{chr(10).join(table)}

nx32的初始重构误差也单列于t1_table.csv；这些网格对波形分辨率很低。节点误差与公共点重构误差分别保存，不能用“只是插值”解释全部失真。

## 核对与限制

40个剖面哈希及全部保存指标读回通过，最大差{readback_max:.3g}；评价4001→8001点最大相对变化{100*eval_max:.4g}%。nx32时间步减半的终点误差最大相对变化{100*half_max:.4g}%。时间误差小不代表空间结果正确。

上轮L=20的停止记录仍保留，本次L=40是明确的扩域实验，不与上轮误差直接拼接。未提高1000状态阈值来硬撑终点，也未用未到达t=1的最后状态填t=1。停止原因和时刻见status.csv；全过程误差见errors.csv，原始场与几何见results.json和npz。

当前可报告的是“尝试完成、部分配置有t=1输出，但长时精度未通过”。若希望获得可信的t=1方法排名，尚需解决当前空间/边界实现的误差增长，或另行定义并验证正则化方法，不能只减小dt或强行运行更久。
'''
    (s.OUT/'HANDOFF.md').write_text(report,encoding='utf-8')
    print(json.dumps(validation,indent=2));print('\n'.join(table))

if __name__=='__main__':main()
