"""Audit the expanded p scan and produce paired-field, one-p-per-row tables."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

import run_parameter_calibration as base
from scan_calibration_parameters import HERE, OUT, PS, ROUTES, plan


def main():
    data=json.loads((OUT/"results.json").read_text(encoding="utf-8"))
    hashes=base.source_hashes()
    hashes["scan_calibration_parameters.py"]=hashlib.sha256(
        (HERE/"scan_calibration_parameters.py").read_bytes()).hexdigest()
    assert data["source_hashes"]==hashes and set(data["rows"])==set(plan())
    rows=data["rows"]
    failed=[key for key,row in rows.items() if row["status"]!="completed"]
    if failed:
        raise RuntimeError(f"Incomplete/failed records retained: {failed}")
    def get(p,route,n=400,dt=base.DT,L=4.):
        return rows[base.case_key(dict(p=p,route=route,n=n,dt=dt,halfwidth=L,method="rk4"))]
    def error(p,route,t=.5,n=400,dense=False,dt=base.DT,L=4.):
        return get(p,route,n,dt,L)["snapshots"][str(t)]["eval_16001" if dense else "errors"]

    # Independent scalar inversion of the analytic centered c=1 travelling wave.
    reference_diff=0.
    for p in PS:
        sol=base.Soliton((p,),c=1.,shift=-(1-2/p)/2)
        s=1-2/p; beta=p-p/(p-1); speed=(1-s*s)/4
        grid=np.linspace(-2,2,41)
        for t in (0.,*base.TIMES):
            theta=np.array([brentq(lambda th:th/beta+s*np.tanh(th/2)/2+speed*t-x,
                        beta*(x-speed*t-s/2)-1e-10,beta*(x-speed*t+s/2)+1e-10,
                        xtol=5e-15) for x in grid])
            sech2=1/np.cosh(theta/2)**2
            exact_u=s*s*sech2/4
            exact_rho=1/(1+s*s/(1-s*s)*sech2)
            u,rho,_,_=base.reference(sol,grid,t)
            reference_diff=max(reference_diff,float(max(abs(u-exact_u))),float(max(abs(rho-exact_rho))))
    assert reference_diff<2e-11

    eval_max=0.; eval_worst=None; readback=0.; csv_rows=[]
    for row in rows.values():
        spec=row["spec"]
        assert row["min_h"]>0 and row["min_rho"]>0 and row["c_phys"]==1.
        if spec["route"]=="difference_rm":assert row["min_Rm"]>0
        sol=base.Soliton((spec["p"],),c=1.,shift=-(1-2/spec["p"])/2)
        with np.load(row["profile"]) as arch:
            for t in base.TIMES:
                arrays=tuple(arch[f"t{t}_{name}"] for name in ("x","u","rho_x","rho"))
                assert np.all(np.diff(arrays[0])>0) and np.all(arrays[3]>0)
                measured=base.measure(sol,arrays,t)
                dense=base.measure(sol,arrays,t,16001)
                for field in ("u","rho"):
                    saved=row["snapshots"][str(t)]["errors"][field]
                    readback=max(readback,abs(measured[field]-saved))
                    assert np.isclose(measured[field],saved,rtol=1e-12,atol=1e-15)
                    assert np.isclose(dense[field],row["snapshots"][str(t)]["eval_16001"][field],rtol=1e-12,atol=1e-15)
                    delta=abs(dense[field]-saved)/saved
                    if delta>eval_max:
                        eval_max=delta;eval_worst=dict(spec=spec,time=t,field=field)
                csv_rows.append({**{k:v for k,v in spec.items() if k!="purposes"},
                                 "time":t,**measured,"C":row["C"],"a":row["a"]})
    with (OUT/"all_errors.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(csv_rows[0]));w.writeheader();w.writerows(csv_rows)

    convergence=[];time_checks=[];domain=[];ratios=[];wide_csv=[]
    for p in PS:
        for n in (400,800):
            assert len({get(p,r,n)["initial_state_sha256"] for r in base.MOVING})==1
        for route in ROUTES:
            for t in base.TIMES:
                for field in ("u","rho"):
                    coarse=error(p,route,t)[field];fine=error(p,route,t,n=800)[field]
                    halved=error(p,route,t,n=800,dt=base.DT/2)[field]
                    convergence.append(dict(p=p,route=route,time=t,field=field,
                                            order=float(np.log2(coarse/fine))))
                    time_checks.append(dict(p=p,route=route,time=t,field=field,
                                             relative_change=abs(halved-fine)/fine))
                    if p in (3.,20.):
                        extended=error(p,route,t,n=500,L=5.)[field]
                        domain.append(dict(p=p,route=route,time=t,field=field,
                                           relative_change=abs(extended-coarse)/coarse))
        for t in base.TIMES:
            ratios.append(dict(p=p,time=t,**{
                field:error(p,"integrable_calibrated",t)[field]/error(p,"difference_matched",t)[field]
                for field in ("u","rho")}))
            entry=dict(p=p,time=t)
            for route in ROUTES:
                for field in ("u","rho"):
                    entry[f"{route}_{field}"]=error(p,route,t)[field]
            wide_csv.append(entry)
    with (OUT/"comparison_by_p.csv").open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(wide_csv[0]));w.writeheader();w.writerows(wide_csv)

    # Check whether local superiority directions survive fine grid/time/evaluation controls.
    direction_checks=[]
    for p in PS:
        for t in base.TIMES:
            for field in ("u","rho"):
                results=[]
                for n,dt,dense in ((400,base.DT,False),(800,base.DT,False),
                                   (800,base.DT/2,False),(400,base.DT,True)):
                    r=error(p,"integrable_calibrated",t,n,dense,dt)[field]/error(
                        p,"difference_matched",t,n,dense,dt)[field]
                    results.append(r)
                direction_checks.append(dict(p=p,time=t,field=field,ratios=results,
                                              direction_consistent=len({v<1 for v in results})==1))

    audit=dict(status="passed",records=len(rows),new_trajectories=sum(
        row["provenance"]=="new evolution" for row in rows.values()),
        reused_trajectories=sum(row["provenance"]!="new evolution" for row in rows.values()),
        reference_max_difference=reference_diff,readback_max_difference=readback,
        evaluation_max_relative_change=eval_max,evaluation_worst=eval_worst,
        time_max_relative_change=max(x["relative_change"] for x in time_checks),
        domain_max_relative_change=max(x["relative_change"] for x in domain),
        source_hashes=hashes,direction_checks=direction_checks)
    base.dump(OUT/"validation.json",audit)
    base.dump(OUT/"summary.json",dict(convergence=convergence,time_checks=time_checks,
              domain_checks=domain,calibrated_over_matched=ratios))

    pair=lambda e:f"{e['u']:.3e} / {e['rho']:.3e}"
    names={"integrable_original":"原可积（未校准）","integrable_calibrated":"可积（已校准）",
           "difference_matched":"普通差分（同网格）","difference_fixed":"普通固定差分",
           "difference_rm":"普通差分＋R_m","difference_rho":"普通 ALE＋rho"}
    main_routes=("integrable_original","integrable_calibrated","difference_matched",
                 "difference_fixed","difference_rm")
    lines=["# 参数扩展比较：每个 p 一行，u / rho 并列", "", "2026-09-26。"
        "按同一口径实际比较 p=3,4,5,6,8,10,12,16,20。每格为 **u 总误差 / rho 总误差**，越小越好；"
        "原可积、校准可积和普通差分横向放在同一行。", "",
        "固定 c=1，N=400，RK4 dt=.003125；连续精确解参照、共同物理核心 [-2,2]、8001 评价点、分段线性输出。"
        "校准参数 C=.02+sqrt(1+.02²)=1.0201999800。各路线都从同一连续初值采样，未减去初始或重构误差。", "",
        "普通差分（同网格）为 Dρ*：与两种可积方案使用同变量、同初始质量网格、同密度位置和同左端边界，"
        "是检验校准方案相对普通离散化最直接的对照。另列普通固定差分和普通 R_m 动网格，以保留实际方法排名。"
        "后两者属于两端 Poisson 边界的 ALE 框架，跨框架排名不应唯一归因于可积性。", "",
        "这些 p 都属于 c=1、p>2 的非退化光滑单孤子分支，q=p/(p-1)。p 可以连续取值；"
        "这组选点覆盖较宽至较陡波形，不代表九种不同方程，也不是随机统计样本。"]
    for t in base.TIMES:
        lines += ["",f"## t={t:g}","","| p | "+" | ".join(names[r] for r in main_routes)+" |",
                  "|---:|"+"---:|"*len(main_routes)]
        for p in PS:
            lines.append(f"| {p:g} | "+" | ".join(pair(error(p,r,t)) for r in main_routes)+" |")
    lines += ["", "## 校准与同网格普通差分直接比较", "",
              "下表为“校准误差 / 普通差分误差”，每格仍是 u / rho。小于 1 表示校准可积式更好。", "",
              "| p | t=.25 比值 | t=.5 比值 |", "|---:|---:|---:|"]
    for p in PS:
        vals=[next(x for x in ratios if x["p"]==p and x["time"]==t) for t in base.TIMES]
        lines.append(f"| {p:g} | "+" | ".join(f"{x['u']:.3f} / {x['rho']:.3f}" for x in vals)+" |")
    lines += ["", "本批结果：t=.25 时 p=10、12、16、20 的校准 u 误差低于同网格普通差分；"
              "t=.5 时优势出现在 p=16、20，分别降低约 12.2%、33.7%。"
              "rho 在九个参数、两个时刻均略差于同网格普通差分；校准式也未超过主表中普通固定差分和 R_m 路线。", "",
              "观察到的优势仅对应表中指定的参数、时刻和物理量；u 获益不能替代 rho 获益。"
              "本轮没有对参数总体作显著性检验。", "",
              "## 网格加密核查", "", "下表为 N=400→800 的观测阶，仍为 u / rho；使用相同小时间步。", "",
              "| p | t | 原可积 | 校准可积 | 普通差分（同网格） |", "|---:|---:|---:|---:|---:|"]
    for p in PS:
        for t in base.TIMES:
            vals=[]
            for route in ("integrable_original","integrable_calibrated","difference_matched"):
                orders=[next(x["order"] for x in convergence if x["p"]==p and x["time"]==t
                             and x["route"]==route and x["field"]==f) for f in ("u","rho")]
                vals.append(f"{orders[0]:.3f} / {orders[1]:.3f}")
            lines.append(f"| {p:g} | {t:g} | "+" | ".join(vals)+" |")
    unstable=[x for x in direction_checks if not x["direction_consistent"]]
    lines += ["", "## 核验与范围", "",
        f"- 共 {len(rows)} 条记录：新运行 {audit['new_trajectories']} 条，复用原实验完全匹配的 {audit['reused_trajectories']} 条。全部完成；新结果另存，旧源码与数据未覆盖。",
        f"- 9 个参数、初始及两个时刻的独立括区间反演核对，双场最大差 {reference_diff:.3e}。",
        f"- 全量末态回读误差差 {readback:.3e}；评价点 8001→16001 最大相对变化 {100*eval_max:.3f}%。",
        f"- N=800 时间步减半，全部误差最大相对变化 {audit['time_max_relative_change']:.3e}。",
        f"- 扩展端点 p=3、20 做半宽 4→5、N400→500 控制，全部路线误差最大变化 {100*audit['domain_max_relative_change']:.2f}%；评价核心始终相同。",
        f"- 校准相对同网格差分的 36 项单场方向中，{len(unstable)} 项在空间/时间/评价加密复核中改变方向。每项比值保存在 validation.json；接近 1 的差异不能按打印舍入值判优。", "",
        "扩域时原生三路线保留质量格距及核心初始节点；普通 ALE 的等质量初始布点会随全域归一变化，"
        "故后者是整体设置敏感性，并非纯边界误差分解。低 p 的波形较宽，精确边界和有限评价区域仍构成适用条件。", "",
        "## 补充：原 rho 的普通 ALE 实现", "",
        "这一普通差分与主表的同变量差分不是同一种实现；单独列出，避免混淆。", "",
        "| p | t=.25，u / rho | t=.5，u / rho |", "|---:|---:|---:|"]
    for p in PS:
        lines.append(f"| {p:g} | "+" | ".join(pair(error(p,"difference_rho",t)) for t in base.TIMES)+" |")
    lines += ["", "## 数据", "",
        "- [按 p 横向排列的 CSV](out/calibration_parameter_scan/comparison_by_p.csv)：18 行（9 参数 × 2 时刻），各方法的 u/rho 独立数值列。",
        "- [全部轨道与控制 CSV](out/calibration_parameter_scan/all_errors.csv)。",
        "- [原始结果](out/calibration_parameter_scan/results.json)、[收敛与比值](out/calibration_parameter_scan/summary.json)、[核验](out/calibration_parameter_scan/validation.json)。",
        "- [原四时间算法报告](PARAMETER_CALIBRATION_REPORT.md)。本次固定 RK4 扩展 p，未把九参数与所有时间算法重新交叉。", "",
        "复现：`python Workspaces/hs_conserved_mesh_20260925/scan_calibration_parameters.py`，再运行 "
        "`python Workspaces/hs_conserved_mesh_20260925/report_calibration_parameter_scan.py`。", ""]
    (HERE/"CALIBRATION_PARAMETER_SCAN_REPORT.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps({k:v for k,v in audit.items() if not isinstance(v,(list,dict))},indent=2))
    for x in ratios:
        print(f"p={x['p']:g},t={x['time']}: calibrated/matched {x['u']:.6f}/{x['rho']:.6f}")


if __name__=="__main__":
    main()
