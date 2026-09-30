"""Validate saved Euler trajectories and compare total/time error to unchanged RK4."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np

import run_parameter_calibration as base
from run_euler_comparison import HERE, OUT, DTS, PS, ROUTES, plan


def main():
    data=json.loads((OUT/"results.json").read_text(encoding="utf-8"))
    hashes=base.source_hashes()
    hashes["run_euler_comparison.py"]=hashlib.sha256((HERE/"run_euler_comparison.py").read_bytes()).hexdigest()
    assert hashes==data["source_hashes"] and set(data["rows"])==set(plan())
    ref_path=Path(data["configuration"]["rk4_reference"])
    assert hashlib.sha256(ref_path.read_bytes()).hexdigest()==data["configuration"]["rk4_reference_sha256"]
    old=json.loads(ref_path.read_text(encoding="utf-8"))
    rows=data["rows"]
    failures=[key for key,r in rows.items() if r["status"]!="completed"]
    if failures:raise RuntimeError(f"Failed records retained: {failures}")
    def key(p,route,method,dt):
        return base.case_key(dict(p=p,route=route,method=method,dt=dt,n=400,halfwidth=4.))
    def euler(p,route,dt):return rows[key(p,route,"euler",dt)]
    def rk4(p,route):return old["rows"][key(p,route,"rk4",base.DT)]
    def errors(row,t,dense=False):return row["snapshots"][str(t)]["eval_16001" if dense else "errors"]
    grid=np.linspace(-2,2,8001)
    def profile(row,t):
        with np.load(row["profile"]) as arch:
            return tuple(arch[f"t{t}_{name}"].copy() for name in ("x","u","rho_x","rho"))
    def interpolate(arrays):
        return (np.interp(grid,arrays[0],arrays[1]),np.interp(grid,arrays[2],arrays[3]))

    readback=0.;eval_change=0.;all_csv=[];cache={};evaluation_worst=None;refined=[]
    for k,row in rows.items():
        s=row["spec"]
        assert row["min_h"]>0 and row["min_rho"]>0
        if s["route"]=="difference_rm":assert row["min_Rm"]>0
        reference_row=rk4(s["p"],s["route"])
        assert row["initial_state_sha256"]==reference_row["initial_state_sha256"]
        assert row["C"]==reference_row["C"] and row["a"]==reference_row["a"]
        sol=base.Soliton((s["p"],),c=1.,shift=-(1-2/s["p"])/2)
        for t in base.TIMES:
            fields=profile(row,t)
            cache[(k,t)]=interpolate(fields)
            exact=base.reference(sol,grid,t)[:2]
            measured={f:float(np.max(abs(cache[(k,t)][i]-exact[i]))) for i,f in enumerate(("u","rho"))}
            denser=base.measure(sol,fields,t,16001)
            for f in ("u","rho"):
                saved=errors(row,t)[f]
                readback=max(readback,abs(saved-measured[f]))
                assert np.isclose(saved,measured[f],rtol=1e-12,atol=1e-15)
                assert np.isclose(denser[f],errors(row,t,True)[f],rtol=1e-12,atol=1e-15)
                delta=abs(denser[f]-saved)/saved
                if delta>eval_change:
                    eval_change=delta;evaluation_worst=dict(key=k,time=t,field=f)
            if (s["method"]=="euler" and
                (max(abs(denser[f]/measured[f]-1) for f in ("u","rho"))>.005 or
                 (s["p"]==10. and s["route"] in ("integrable_calibrated","difference_matched")
                  and s["dt"]==base.DT and t==.25))):
                refined.append(dict(key=k,time=t,errors_64001=base.measure(sol,fields,t,64001),
                                    errors_8001=measured,errors_16001=denser))
            all_csv.append({**{k:v for k,v in s.items() if k!="purposes"},"time":t,**measured})
    with (OUT/"all_errors.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(all_csv[0]));w.writeheader();w.writerows(all_csv)

    reference_controls=[];temporal=[];comparisons=[];changes=[];wide=[]
    for p in PS:
        for route in ROUTES:
            ref=rk4(p,route)
            for t in base.TIMES:
                ref_vals=interpolate(profile(ref,t))
                if p in (3.,12.,20.):
                    half=rows[key(p,route,"rk4",.0015625)]
                    fine_vals=cache[(key(p,route,"rk4",.0015625),t)]
                    reference_controls.append(dict(p=p,route=route,time=t,
                        field_differences={field:float(max(abs(fine_vals[i]-ref_vals[i])))
                                           for i,field in enumerate(("u","rho"))},
                        relative_error_changes={field:abs(errors(half,t)[field]-errors(ref,t)[field])/
                                                errors(ref,t)[field] for field in ("u","rho")}))
                vals=[]
                for dt in DTS:
                    k=key(p,route,"euler",dt)
                    difference={f:float(max(abs(cache[(k,t)][i]-ref_vals[i])))
                                for i,f in enumerate(("u","rho"))}
                    vals.append(difference)
                    comparisons.append(dict(p=p,route=route,time=t,dt=dt,
                        euler_over_rk4={f:errors(rows[k],t)[f]/errors(ref,t)[f] for f in ("u","rho")},
                        time_difference_over_rk4_total={f:difference[f]/errors(ref,t)[f]
                                                       for f in ("u","rho")}))
                orders={f:[float(np.log2(vals[i][f]/vals[i+1][f])) for i in range(len(DTS)-1)]
                        for f in ("u","rho")}
                temporal.append(dict(p=p,route=route,time=t,errors=vals,orders=orders,dts=DTS))
        for t in base.TIMES:
            for dt in DTS:
                r={f:errors(euler(p,"integrable_calibrated",dt),t)[f]/errors(euler(p,"difference_matched",dt),t)[f]
                   for f in ("u","rho")}
                r4={f:errors(rk4(p,"integrable_calibrated"),t)[f]/errors(rk4(p,"difference_matched"),t)[f]
                    for f in ("u","rho")}
                changes.append(dict(p=p,time=t,dt=dt,euler_ratio=r,rk4_ratio=r4,
                                    changed={f:(r[f]<1)!=(r4[f]<1) for f in ("u","rho")}))
                wide_row=dict(p=p,time=t,dt=dt)
                for route in ROUTES:
                    for f in ("u","rho"):
                        wide_row[f"{route}_{f}"]=errors(euler(p,route,dt),t)[f]
                wide.append(wide_row)
    with (OUT/"comparison_by_p.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(wide[0]));w.writeheader();w.writerows(wide)
    dense_direction_changes=[]
    for p in PS:
        for t in base.TIMES:
            for dt in DTS:
                a=euler(p,"integrable_calibrated",dt);b=euler(p,"difference_matched",dt)
                for field in ("u","rho"):
                    original=errors(a,t)[field]/errors(b,t)[field]
                    dense=errors(a,t,True)[field]/errors(b,t,True)[field]
                    if (original<1)!=(dense<1):
                        dense_direction_changes.append(dict(p=p,time=t,dt=dt,field=field,original=original,dense=dense))
    summary=dict(temporal=temporal,euler_vs_rk4=comparisons,ranking_changes=changes,
                 reference_controls=reference_controls,refined_evaluation=refined)
    base.dump(OUT/"summary.json",summary)
    all_orders=[q for v in temporal for f in ("u","rho") for q in v["orders"][f]]
    counts={str(dt):sum(v["changed"][f] for v in changes if v["dt"]==dt for f in ("u","rho")) for dt in DTS}
    primary=[v for v in comparisons if v["dt"]==base.DT]
    audit=dict(status="passed",trajectories=len(rows),euler_trajectories=216,
        rk4_halfstep_controls=len(rows)-216,readback_max_difference=readback,
        evaluation_max_relative_change=eval_change,evaluation_worst=evaluation_worst,
        dense_evaluation_ranking_flips=dense_direction_changes,
        time_order_range=[min(all_orders),max(all_orders)],
        rk4_reference_max_field_difference=max(v for x in reference_controls for v in x["field_differences"].values()),
        rk4_reference_max_relative_error_change=max(v for x in reference_controls for v in x["relative_error_changes"].values()),
        calibrated_vs_matched_changed_directions_of_36=counts,source_hashes=hashes)
    base.dump(OUT/"validation.json",audit)

    main_routes=("integrable_original","integrable_calibrated","difference_matched","difference_fixed","difference_rm")
    names=dict(integrable_original="原可积（未校准）",integrable_calibrated="可积（已校准）",
               difference_matched="普通差分（同网格）",difference_fixed="普通固定差分",difference_rm="普通差分＋R_m")
    pair=lambda e:f"{e['u']:.3e} / {e['rho']:.3e}"
    text=["# 2HS 一阶 Euler：九参数误差与时间步敏感性", "",
        "2026-09-26。按要求把上一份九参数表的 RK4 换成一阶显式 Euler。"
        "空间路线、c=1、p=3/4/5/6/8/10/12/16/20、N=400、连续初值、边界和共同评价核心保持原设置。"
        "这是沿用 GSG 一阶时间更新的比较思路，不是逐式复刻 GSG 方程或其全套五格式。", "",
        f"**结果：Euler 时间观测阶为 {min(all_orders):.3f}–{max(all_orders):.3f}。"
        "相同 dt=.003125 下，校准式相对同网格差分在 t=.25 的 p=12/16/20、t=.5 的 p=16/20 有 u 优势；"
        "rho 均无优势。较粗 dt=.0125 时有 7/36 项胜负方向偏离 RK4，最细 .0015625 时为 0/36。**", "",
        "## 实验口径", "",
        "主表 dt=.003125，与上一份 RK4 表相同，直接观察只换时间方法的影响。"
        "另计算 .0125、.00625、.0015625，防止仅靠一档步长判断优劣。两物理量和网格在同一 Euler 步中共同更新。", "",
        "每格为 **u / rho 的连续总 L∞ 误差**；分段线性输出到 [-2,2] 的相同 8001 点。"
        "校准参数仍是 C=.02+sqrt(1+.02²)，参照连续物理参数仍为 1。"
        "原可积、校准可积和同网格普通差分共享变量位置与边界；固定/R_m 路线属于另一 ALE 边界框架。", "",
        "若误差传播稳定且解光滑，校准式和二阶普通差分的误差预算一般包含 O(h²)+O(dt)，"
        "未校准式还含已识别的 O(a) 空间项。Euler 时间误差可能掩盖空间差异，也可能与空间误差抵消；"
        "因此低阶时间推进本身不保证比较更公平或更不公平，结论必须连同步长报告。"]
    for t in base.TIMES:
        text += ["",f"## 主表：t={t:g}，Euler dt=.003125", "",
                 "| p | "+" | ".join(names[r] for r in main_routes)+" |",
                 "|---:|"+"---:|"*len(main_routes)]
        for p in PS:text.append(f"| {p:g} | "+" | ".join(pair(errors(euler(p,r,base.DT),t)) for r in main_routes)+" |")
    text += ["", "## 相同时间步：校准可积 / 同网格普通差分", "",
             "比值小于 1 表示校准式误差更低，每格仍为 u / rho。", "",
             "| p | t=.25 RK4 | t=.25 Euler | t=.5 RK4 | t=.5 Euler |",
             "|---:|---:|---:|---:|---:|"]
    for p in PS:
        vals=[]
        for t in base.TIMES:
            v=next(x for x in changes if x["p"]==p and x["time"]==t and x["dt"]==base.DT)
            vals += [f"{v[k]['u']:.3f} / {v[k]['rho']:.3f}" for k in ("rk4_ratio","euler_ratio")]
        text.append(f"| {p:g} | "+" | ".join(vals)+" |")
    text += ["", "## 时间步改变后，排名是否改变？", "",
             "统计校准可积式相对同网格普通差分的胜负方向，9 参数 × 2 时刻 × 2 场共 36 项；"
             "这些相关指标不是 36 个独立统计样本。", "",
             "| Euler dt | 相对小步 RK4 改变方向的项数 |", "|---:|---:|"]
    for dt in DTS:text.append(f"| {dt:g} | {counts[str(dt)]}/36 |")
    for t in base.TIMES:
        text += ["",f"### t={t:g}：校准 / 普通的比值随步长变化", "",
                 "| p | dt=.0125 | dt=.00625 | dt=.003125 | dt=.0015625 |", "|---:|---:|---:|---:|---:|"]
        for p in PS:
            vals=[next(x["euler_ratio"] for x in changes if x["p"]==p and x["time"]==t and x["dt"]==dt) for dt in DTS]
            text.append(f"| {p:g} | "+" | ".join(f"{v['u']:.3f} / {v['rho']:.3f}" for v in vals)+" |")
    text += ["", "## Euler 相对 RK4 本身的误差变化", "",
             "以下为 dt=.003125、t=.5 的 Euler总误差/RK4总误差，比值小于1不等于时间求解更准确。", "",
             "| p | 校准可积 | 同网格普通差分 | 普通固定差分 | R_m 差分 |", "|---:|---:|---:|---:|---:|"]
    for p in PS:
        vals=[next(x["euler_over_rk4"] for x in primary if x["p"]==p and x["route"]==r and x["time"]==.5)
              for r in ("integrable_calibrated","difference_matched","difference_fixed","difference_rm")]
        text.append(f"| {p:g} | "+" | ".join(f"{x['u']:.3f} / {x['rho']:.3f}" for x in vals)+" |")

    text += ["", "## 时间误差与核验", "",
        "同空间小步 RK4 解作为时间参照，以共同物理评价点上的两数值解之差估计时间离散影响，"
        "没有把连续解总误差相减当作时间误差。p=3、12、20 的所有六路线另做 RK4 时间减半核验。", "",
        f"- 216 条 Euler 轨道、18 条 RK4 参照减步控制，全部完成。原九参数 RK4 数据按文件哈希核对后复用。",
        f"- Euler 相对各自空间参照的相邻时间步减半观测阶范围 {min(all_orders):.3f}–{max(all_orders):.3f}（含两场和两个时刻）。",
        f"- RK4 参照减半时，两数值场最大差 {audit['rk4_reference_max_field_difference']:.3e}；总误差最大相对变化 {audit['rk4_reference_max_relative_error_change']:.3e}。",
        f"- 评价点 8001→16001 的全部误差最大相对变化 {100*eval_change:.3f}%；保存状态读回误差差 {readback:.3e}。",
        f"- 上述加密下校准/同网格差分的胜负方向改变 {len(dense_direction_changes)} 项（四档步长全部检查）。"
        "最大评价差来自粗 Euler 下误差较小的 R_m u；对变化超过 .5% 的案例以及临界 p10/.25 主步长比较，额外保存 64001 点核验于 summary.json。",
        "- 每条 Euler 轨道与对应 RK4 的初态哈希、离散参数、格距完全相同；主阶段与接受步沿用原求解器正性/有限性检查，保存格距与rho均为正，Rm路线Rm为正。", "",
        "此次没有扩展空间网格、时间窗口或更换边界；既有边界/重构限制仍然存在。"
        "全部结论仅是指定参数与步长下的确定性比较，不是新的参数总体显著性检验。", "",
        "## 数据与复现", "",
        "- [按 p 和步长横向排列 CSV](out/euler_comparison/comparison_by_p.csv)。",
        "- [全量误差 CSV](out/euler_comparison/all_errors.csv)、[原始记录](out/euler_comparison/results.json)、[时间误差/排名汇总](out/euler_comparison/summary.json)、[核验](out/euler_comparison/validation.json)。",
        "- [原 RK4 九参数表](CALIBRATION_PARAMETER_SCAN_REPORT.md)。原 rho ALE 的完整结果亦在 CSV 中。", "",
        "复现：`python Workspaces/hs_conserved_mesh_20260925/run_euler_comparison.py`，再运行 "
        "`python Workspaces/hs_conserved_mesh_20260925/report_euler_comparison.py`。", ""]
    (HERE/"EULER_COMPARISON_REPORT.md").write_text("\n".join(text),encoding="utf-8")
    print(json.dumps({k:v for k,v in audit.items() if k!="source_hashes"},indent=2))
    for v in changes:
        if v["dt"]==base.DT:print(v)


if __name__=="__main__":main()
