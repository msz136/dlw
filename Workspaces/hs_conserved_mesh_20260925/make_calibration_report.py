"""Generate the calibrated-parameter comparison report directly from audited data."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from run_parameter_calibration import HERE, OUT, ROUTES, METHODS, PS, DT, case_key

LABELS={"integrable_original":"Iρ 原可积", "integrable_calibrated":"ICρ 校准可积",
        "difference_rho":"Dρ 普通 ALE", "difference_rm":"DR 新密度 ALE",
        "difference_fixed":"DF 固定差分", "difference_matched":"Dρ* 同变量差分"}
SHORT={"integrable_original":"Original I", "integrable_calibrated":"Calibrated I",
       "difference_rho":"ALE rho", "difference_rm":"ALE Rm",
       "difference_fixed":"Fixed", "difference_matched":"Matched FD"}
COLORS=dict(zip(ROUTES,("#c44e52","#2a6fbb","#a8a8a8","#22886b","#8172b2","#d58a21")))
PRETTY=dict(euler="Euler",heun="Heun",rk4="RK4",rk8="RK8")


def main():
    data=json.loads((OUT/"results.json").read_text(encoding="utf-8"))
    summary=json.loads((OUT/"summary.json").read_text(encoding="utf-8"))
    audit=json.loads((OUT/"validation.json").read_text(encoding="utf-8"))
    assert audit["status"]=="passed"
    def row(p,route,n=200,method="rk4",dt=DT,L=4.):
        return data["rows"][case_key(dict(p=p,route=route,n=n,method=method,dt=dt,halfwidth=L))]
    def err(p,route,n=200,method="rk4",dt=DT,t=.5):
        return row(p,route,n,method,dt)["snapshots"][str(t)]["errors"]
    def fmt(x):return f"{x:.4e}"
    def pair(x):return f"{x['u']:.3e} / {x['rho']:.3e}"
    def range_orders(route):
        vals=[v for c in summary["convergence"] if c["route"]==route for v in c["orders"]]
        return f"{min(vals):.3f}–{max(vals):.3f}"

    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
    fig,axes=plt.subplots(2,2,figsize=(11,7.5),layout="constrained")
    for i,p in enumerate(PS):
        for j,field in enumerate(("u","rho")):
            ax=axes[i,j]
            for route in ROUTES:
                ns=np.array([200,400,800])
                vals=[err(p,route,n=int(n))[field] for n in ns]
                ax.loglog(ns,vals,"o-",label=SHORT[route],color=COLORS[route],lw=1.8,ms=4)
            ax.set(title=f"p = {p:g}, field {field}",xlabel="Number of intervals N",
                   ylabel="Continuous total error (L-infinity)")
            ax.set_xticks([200,400,800],["200","400","800"])
            ax.grid(True,which="both",alpha=.18)
    handles,labels=axes[0,0].get_legend_handles_labels()
    fig.legend(handles,labels,loc="outside lower center",ncol=3,frameon=False)
    fig.suptitle("Parameter calibration: spatial convergence at T = 0.5\n"
                 "Same continuous c = 1 reference; RK4, dt = 0.003125")
    fig.savefig(OUT/"calibration_convergence.png",dpi=170)
    fig.savefig(OUT/"calibration_convergence.pdf")
    plt.close(fig)

    lines=["# 2HS 参数校准：可积半离散的总误差与时间算法对照", "",
        "后续已扩展至九个 p，按每个参数一行、u/rho 并列展示校准前后与普通差分："
        "[参数扩展横向比较表](CALIBRATION_PARAMETER_SCAN_REPORT.md)。本页保留原两个参数的四时间算法完整实验。", "",
        "2026-09-26。已实现并实际推进参数校准方案，目标连续方程始终固定为 c_phys=1。"
        "**两个代表孤子中，校准将原方案随加密趋近一阶的总误差收敛改善为近二阶，并大幅降低误差。"
        "p=12、t=.25 的 u 相对同变量普通差分低约 27%，且随加密保持；但该优势不延续至 t=.5，"
        "rho 也没有同时改善，更未超过本轮新密度 ALE 路线。**", "",
        "本轮完成 204 条主矩阵/控制轨道，另有 18 条先导轨道、6 条独立右端积分和 2 条有限格距精确孤子核验。"
        "全部完成并通过回读验收；先导轨道与正式矩阵有重复，不计独立证据。"
        "这是 p=5、12 的确定性比较，不是新的随机参数显著性检验。", "",
        "## 校准改变什么", "",
        r"原式取 $C=c_{\rm phys}=1$；新式取 $C(a)=a+\sqrt{c_{\rm phys}^2+a^2}$。"
        "每条轨道内 C 为常数，仅在改变计算格距 a 后重新计算。没有修改原半离散 RHS 的结构，也没有改变目标连续孤子、物理参数或边界参照。", "",
        r"同状态右端差从 $ac_{\rm phys}(1-\rho^2)+\frac{a^2}{2}(\rho^{-1}-\rho)^2$ "
        r"变为 $\frac{a^2}{2}(\rho^{-1}-\rho)^2$。本轮再次符号核对，并直接检查程序实际 RHS，"
        f"最大恒等式残差 {audit['numeric_rhs_identity_max_residual']:.2e}。该恒等式不是全局解误差定理。", "",
        "| N | a（质量坐标格距） | 校准 C |", "|---:|---:|---:|"]
    for n in (200,400,800):
        r=row(5.,"integrable_calibrated",n)
        lines.append(f"| {n} | {r['a']:.3f} | {r['C']:.10f} |")
    lines += ["", "每个固定 a 上仍调用论文原参数族的 sd 公式；参数依赖网格形成新的连续逼近族。"
              "这不等于构造了 GSG 中两套独立的可积半离散方程，也不意味着 RK4/RK8 的完整时间离散仍可积。", "",
        "## 五条主路线，加一个匹配对照", "",
        "| 路线 | 场方程/参数 | 网格与边界 |",
        "|---|---|---|",
        "| Iρ 原可积 | 原半离散，C=1 | 原生 rho 动网格、左端解析 u |",
        "| ICρ 校准可积 | 相同半离散公式，C=C(a) | 与 Iρ 完全相同的初态、网格和边界 |",
        "| Dρ 普通 ALE | 普通二阶差分，c=1 | rho 初始布点与速度，两端解析 Poisson 边界 |",
        "| DR 新密度 ALE | 普通二阶差分，c=1 | R_m 初始布点与持续运动，两端解析 Poisson 边界 |",
        "| DF 固定差分 | 普通二阶差分，c=1 | 均匀固定网格，两端解析 Poisson 边界 |",
        "| Dρ* 匹配对照 | 原变量下的普通差分，c=1 | 与 Iρ/ICρ 相同 v、d、初态、质量网格和左端边界 |", "",
        "Dρ* 用已有 MovingSystem(kind='fd') 实现，专门让右端恒等式中的普通式成为实际演化对照。"
        "它与旧报告的 Dρ（ALE）是不同实现，不应混用误差数字。所有计算都持续推进各自定义的网格，没有加入冻结加密网格因素。", "",
        "时间方法为 Euler、Heun 二阶、RK4、固定步 DOP853 八阶主公式（12 次右端求值）。"
        "每个空间路线都运行三个步长 .0125/.00625/.003125，N=200；观测 t=.25/.5。", "",
        "误差统一对固定 c=1 连续精确解，在共同物理核心 [-2,2] 的 8001 点比较分段线性输出的 L∞ 总误差。"
        "两种可积式和 Dρ* 的 rho=a/d 位于格边并按中点输出；ALE 的 rho 位于节点。"
        "初态密度的单元平均到点值差也计入总误差，没有减去初值或插值误差。", "",
        "ALE 的物理域为 [-4,4]；Iρ/ICρ/Dρ* 的计算质量域为 [-4,4]，映射后的物理端点略有不同且可运动。"
        "因此跨这两个边界框架的绝对排名只能作为完整路线比较；原式、校准式、Dρ* 之间的比较控制更严格。", "",
        "## 主表：空间路线 × 时间方法", "",
        "N=200、dt=.0125；两个观察时刻都列出，每格依次为 u / rho 总误差。另两档步长全量表在 CSV 中。"]
    for p in PS:
        for t in (.25,.5):
            lines += ["",f"### p={p:g}，t={t:g}","","| 路线 | Euler | Heun | RK4 | RK8 |",
                      "|---|---:|---:|---:|---:|"]
            for route in ROUTES:
                vals=[pair(err(p,route,method=m,dt=.0125,t=t)) for m in METHODS]
                lines.append("| "+LABELS[route]+" | "+" | ".join(vals)+" |")
    lines += ["", "Euler 某些格子的总误差较小可能来自时间与空间误差抵消；不能把它作为该空间模型误差更小的证据。"
              "各方法随减步趋向本路线的细时间解。下面的校准判断使用小步 RK4，并有时间减半核验。", "",
              "## 校准收益与空间观测阶", "",
              "下表 N=400、RK4 dt=.003125、T=.5。降低倍数定义为原误差/校准误差。", "",
              "| p | 场 | 原可积误差 | 校准误差 | 降低倍数 | 同变量差分 Dρ* | 校准 / Dρ* |",
              "|---:|---|---:|---:|---:|---:|---:|"]
    for p in PS:
        for field in ("u","rho"):
            ei=err(p,"integrable_original",400)[field]
            ec=err(p,"integrable_calibrated",400)[field]
            ed=err(p,"difference_matched",400)[field]
            lines.append(f"| {p:g} | {field} | {fmt(ei)} | {fmt(ec)} | {ei/ec:.2f} | {fmt(ed)} | {ec/ed:.3f} |")
    lines += ["", "| p | 场 | 路线 | N=200 | N=400 | N=800 | 阶 200→400 | 阶 400→800 |",
              "|---:|---|---|---:|---:|---:|---:|---:|"]
    for p in PS:
        for field in ("u","rho"):
            for route in ("integrable_original","integrable_calibrated","difference_matched"):
                c=next(v for v in summary["convergence"] if v["p"]==p and v["field"]==field
                       and v["route"]==route and v["time"]==.5)
                lines.append(f"| {p:g} | {field} | {LABELS[route]} | "+
                             " | ".join(fmt(v) for v in c["errors"])+
                             " | "+" | ".join(f"{v:.3f}" for v in c["orders"])+" |")
    lines += ["",f"合并两个时刻与两个场：原式观测阶 {range_orders('integrable_original')}，"
              f"校准式 {range_orders('integrable_calibrated')}。"
              "这支持一阶右端差是原方案当前劣势的重要来源；不证明它解释了所有误差。", "",
              "![总误差空间收敛](out/parameter_calibration/calibration_convergence.png)", "",
              "在 t=.5 的两个参数和三个空间分辨率上，Dρ* 两场总误差均更小。"
              "但 t=.25、p=12 的 u 出现校准式的局部优势，应单独报告。", "",
              "## 局部优势：p=12、t=.25 的 u", "",
              "下表使用 RK4 dt=.003125，全部是对同一连续解的总误差。", "",
              "| N | 校准 u 误差 | Dρ* u 误差 | u 降低比例 | 校准/Dρ* 的 rho 比值 |",
              "|---:|---:|---:|---:|---:|"]
    for n in (200,400,800):
        ec=err(12.,"integrable_calibrated",n,t=.25)
        ed=err(12.,"difference_matched",n,t=.25)
        lines.append(f"| {n} | {fmt(ec['u'])} | {fmt(ed['u'])} | {100*(1-ec['u']/ed['u']):.2f}% | {ec['rho']/ed['rho']:.4f} |")
    lines += ["", "该比较的初态、变量位置和边界相同；N=200→400→800 后 u 的收益保持在约 26%–27%。"
              "对 N=400 的扩域复核中，两路线 u 误差变化在舍入量级；时间减半和评价点加密亦未抹去这一幅度。"
              "这是当前找到的局部、单场、相对指定普通格式的优势，不是参数总体显著性结论。", "",
              "限制也必须同时报告：rho 比匹配差分略差；t=.5 时 u 优势消失；"
              "同一 p=12、t=.25 下，校准式 u 误差仍约为 DR 的 7.3 倍，亦高于普通 ALE Dρ 和 DF。"
              "不能据这个局部例子宣称校准可积式全面更优，更不能把误差差异唯一归因于可积性。", "",
              "## 时间推进及可信度核验", "",
              "同空间 RK8 dt=.00078125 为细时间参照；下面是校准式的末态 u 时间差，"
              "它与连续物理解总误差不同。", "",
              "| p | 时间方法 | dt=.0125 | dt=.00625 | dt=.003125 | 首次减半观测阶 |",
              "|---:|---|---:|---:|---:|---:|"]
    for p in PS:
        for method in METHODS:
            rec=next(v for v in summary["temporal"] if v["p"]==p and
                     v["route"]=="integrable_calibrated" and v["method"]==method)
            es=[v[0] for v in rec["errors"]]
            order=f"{np.log2(es[0]/es[1]):.3f}" if min(es[:2])>1e-12 else "舍入地板"
            lines.append(f"| {p:g} | {PRETTY[method]} | "+" | ".join(fmt(e) for e in es)+f" | {order} |")
    independent_max=max(max(v["max_differences"].values()) for v in audit["independent_checks"])
    lattice_max=max(max(v["max_differences"].values()) for v in audit["exact_lattice_checks"])
    for text in [
        f"N=800 的 RK4 时间步再减半，双场总误差最大相对变化 {audit['time_half_max_relative_change']:.3e}。",
        f"全部保存轨道用 8001→16001 共同评价点复核，误差最大相对变化 {100*audit['evaluation_double_max_relative_change']:.3f}%。",
        f"将 RHS 独立改写成 w=v/d 的展开式，再用自适应 DOP853 积分 6 条轨道，节点 x/u/rho 与主计算最大差 {independent_max:.3e}。",
        f"校准 C 对应的有限格距精确孤子另测 2 条轨道，最大 x/u/rho 差 {lattice_max:.3e}。这只核验离散实现，主表没有用它替换连续精确参照。",
        "原可积、校准可积和 Dρ* 在每个 p、N 上初始状态字节哈希相同。校准轨道只换离散参数 C，边界仍来自 c_phys=1。",
        "原生三路线每个 RHS 阶段和接受步检查网格；ALE 原 RHS 检查阶段有限性、格距和 rho，Rm 阶段额外检查 Rm>0。所有轨道完成，保存状态回读无差异。",
        "旧统计实验及时间方法实验的冻结源码哈希仍匹配；没有覆盖旧求解器或旧数据。"]:
        lines += ["", "- "+text]
    lines += ["", "扩域控制：半宽 4→5，同时 N=400→500 保持 a=.02（ALE 为名义 dx=.02），"
              "评价仍在共同 [-2,2]。原生质量网格的核心初始节点保持一致；ALE 等质量布点会随全域归一略变，"
              "所以后者检验的是整个扩域设置，不能把全部变化都归为边界误差。", "",
              "| p | 路线 | u 误差相对变化 | rho 误差相对变化 |", "|---:|---|---:|---:|"]
    for p in PS:
        for route in ROUTES:
            vals=[next(v for v in summary["domain_checks"] if v["p"]==p and
                       v["route"]==route and v["time"]==.5 and v["field"]==field)
                  for field in ("u","rho")]
            lines.append(f"| {p:g} | {LABELS[route]} | "+
                         " | ".join(f"{100*v['relative_change']:.5f}%" for v in vals)+" |")
    lines += ["", "原生校准/匹配差分的本次扩域影响很小；部分 ALE 误差仍有明显变化。"
              "不能据此宣称所有边界闭合都等价，也不能把误差表视为可积性这一单独因素的因果估计。", "",
              "## 本轮可写入结论的内容", "",
              "1. 在固定连续物理参数下，通过离散参数的网格依赖校准，精确消除了已定位的同状态 O(a) 右端差。",
              "2. 在 p=5、12 的光滑单孤子、两个短中时时刻上，校准式实测近二阶；原式随加密趋近一阶。校准明显降低总误差，但未给出一般解收敛定理。",
              "3. p=12、t=.25 的 u 相对同变量普通差分出现经加密/减步/扩域检查的局部优势；rho 和较晚时间不共享此优势，且新密度 ALE 仍更准确。不能声称已经复现 GSG 环孤子的特定优势机制。",
              "4. 这是 GSG 式的完整方案比较表，但原式和校准式属于同一可积半离散参数族，不是两套独立构造的可积离散系统。", "",
              "## 数据与复现", "",
              "- [全量误差 CSV](out/parameter_calibration/all_errors.csv)：204 条轨道 × 两个时刻；含四时间算法、三档步长、空间/时间/扩域控制。",
              "- [原始结果](out/parameter_calibration/results.json)、[观测阶与比值](out/parameter_calibration/summary.json)、[独立核验](out/parameter_calibration/validation.json)。",
              "- [收敛图 PDF](out/parameter_calibration/calibration_convergence.pdf)。", "",
              "依次运行 `python Workspaces/hs_conserved_mesh_20260925/run_parameter_calibration.py`、"
              "`python Workspaces/hs_conserved_mesh_20260925/validate_parameter_calibration.py`、"
              "`python Workspaces/hs_conserved_mesh_20260925/make_calibration_report.py`。"
              "先导轨道入口追加 `--pilot`；旧数据不变。", ""]
    path=HERE/"PARAMETER_CALIBRATION_REPORT.md"
    path.write_text("\n".join(lines),encoding="utf-8")
    print(path)


if __name__=="__main__":
    main()
