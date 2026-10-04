"""Refactor the existing reviewed numerics into explicit persistent-state cells.

Mathematical expressions come verbatim from error_material; only execution
boundaries and named shared state are added. Never edits the original material.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / "error_material"

LEADS = {
    "hs-prepare": "检查计算所需的数学函数和双精度数组。",
    "hs-config": "设置网格、RK4 时间步长和误差评价点。",
    "hs-reference": "定义单孤子解析解，并构造初始物理网格。",
    "hs-spatial": "定义两种空间格式，并由三对角方程从 m 恢复 u。",
    "hs-rk4": "定义一次 RK4 更新，依次计算空间方程的四个阶段。",
    "hs-evolve": "从解析初值出发，将两种方案推进至 T。",
    "hs-error": "将重构场与解析解比较，计算并绘制误差。",
    "error-prepare": "检查残差计算所需的数学函数和双精度数组。",
    "error-config": "设置孤子参数、纵向格距 h 和相位采样点。",
    "error-profile": "定义连续单孤子剖面及其对相位的解析导数。",
    "error-coefficient": "定义二阶残差主系数及全波形上界。",
    "error-residual": "定义有限格距 h 下的 SD 和 FD 方程残差。",
    "error-main": "计算采样主系数，核对上界并测量连续方程残差。",
    "error-convergence": "逐次减半格距，比较并绘制缩放残差与主系数。",
}

# Preserve mathematical annotations while moving procedural descriptions to leads.
COMMENTS = {
    "浏览器原生数学支持；这里运行的是 JavaScript。": "IEEE 754 双精度运算。",
    "重建本组共享状态；后续单元将定义和计算结果存入 lab.hs。": "",
    "重建本组共享状态；后续单元将定义和计算结果存入 lab.dlw。": "",
    "式（24）的单孤子固定 p=5、q=1.25、c=1、零初相位。": "式（24）：p=5、q=1.25、c=1，初相位为零。",
    "加密同一辅助区间时，应同时将 N 加倍、a 减半。": "a：X 方向格距；dt：时间步长；T：终止时间。",
    "式（24）：辅助坐标 X → 物理坐标 x；m=u_xx+2。": "式（24）：X 到 x 的映射，m=u_xx+2。",
    "由 d/dx=J⁻¹d/dX 求 u_xx，供 FD 解析边界使用。": "链式法则：d/dx=(1/J)d/dX，其中 J=dx/dX。",
    "dx/dX=1+0.5625 sech²(θ/2)>0：60 次二分有唯一反解。": "dx/dX>0；反解区间为 [x+0.2,x+0.8]。",
    "两种格式覆盖相同物理端点；FD 在该区间均匀布点。": "固定网格与初始动网格共用物理端点。",
    "Integrable 状态为 [b_0,…,b_(N−1), d_0,…,d_(N−1), x_0]。": "可积格式状态：[b_0,...,b_(N-1), d_0,...,d_(N-1), x_0]。",
    "式（25）：从节点 u 恢复胞元 b、d 的时间导数。": "式（25）：b、d 和 x_0 的时间导数。",
    "Thomas 消元解 u_(i−1)−2u_i+u_(i+1)=Δx²(m_i−2)。": "三对角消元解：u_(i-1)-2u_i+u_(i+1)=dx^2*(m_i-2)。",
    "FD 只推进内部 [m_1,…,m_(N−1), ρ_1,…,ρ_(N−1)]。": "FD 状态为内部 m 与 rho，边界取解析值。",
    "式（28）：固定网格中心差分；解析边界已在 fdFields 中补入。": "式（28）：固定网格上的一阶中心差分。",
    "连续初值确定 b、d；FD 的初始 m 用同一 D₂ 模板计算。": "初始 m=D2(u)+2，与演化使用同一二阶差分模板。",
    "有序节点上的逐段线性插值，覆盖检查不以端点外推代替。": "物理节点上的分段线性重构。",
    "式（29）：每一级都在相应 RHS 内恢复物理场和解析边界。": "式（29）：每一级重新恢复场值和解析边界。",
    "两种方案均由连续初值出发，实际运行至 T；不读取已保存轨道。": "时间层：t_n=n*dt，T=steps*dt。",
    "式（30）：在同一物理评价网格重构两场，再与连续解比较。": "式（30）：公共物理网格上的最大绝对误差。",
    "图中每个点为一个物理小区间的误差最大值，保留全网格最大误差。": "每个绘图区间保留其评价点上的最大误差。",
    "10⁻¹⁶ 仅为对数图的显示下限；误差表使用未经截断的数值。": "对数图显示下限为 1e-16；误差范数不截断。",
    "原表仅作为同配置的回归核对；不参与演化、不替代现场误差。": "仅原配置使用原表误差作回归核对。",
    "DLW 连续单孤子；A: (a,p,q)=(2,1,2)，B: (2,4,-3)。": "孤子参数 (a,p,q)：A=(2,1,2)，B=(2,4,-3)。",
    "h 是 y 方向格距，z 是无量纲相位。x,t 导数保持解析。": "h：y 方向格距；z：无量纲相位；x、t 导数保持解析。",
    "sigmoid 的解析导数：s^(n)=s(1-s) P_n(s)。": "S 形函数的解析导数：s^(n)=s(1-s)*P_n(s)。",
    "P_(n+1)=(1-2s)P_n+s(1-s)P_n'；不做数值微分。": "多项式递推：P_(n+1)=(1-2s)*P_n+s(1-s)*P_n'。",
    "u[n]、v[n] 为对相位 z 的第 n 阶导数。": "u[n]、v[n] 表示对 z 的 n 阶导数。",
    "两分量二阶主系数，编号对应 DLW 两条物理场方程。": "数组下标 0、1 对应 DLW 的两条方程。",
    "B=(s″)²+s′s‴，即 ½[(s′)²]″；其符号保留在主系数中。": "乘积项：B=(s'')^2+s'*s'''=0.5*((s')^2)''。",
    "全波形解析上界；不依赖 points 或所选相位区间。": "覆盖全部实相位 z 的上界。",
    "连续解代入有限 h 的 SD/FD 方程；第一式在交错中点求值。": "",
    "D=δ₀u，W=v−δ₀u；每个偏移节点都重新恢复 W。": "差分重构：D=δ₀u，W=v−δ₀u。",
    "第一式位于相邻节点中点；第二式位于 j=0。": "r1 位于交错中点；r2 位于节点 j=0。",
    "同一相位网格比较：R_h / h² → τ；采样最大值不当作连续上界。": "tau[S][i]：方案 S 第 i 分量的相位采样值。",
    "连续两式逐项相加；分母为 1+各项绝对值之和。": "归一化残差：abs(sum(terms))/(1+sum(abs(terms)))。",
    "逐级将 h 减半，比较 R_h/h² 与同一相位上的二阶主系数。": "余量：R_h/h²−tau=O(h²)。",
    "相邻两档差值的 log₂ 比；二阶余量对应 rate≈2。": "观测阶数=log2(2h 档误差/h 档误差)。",
}


def concise_source(code):
    lines = []
    for line in code.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("//"):
            old_comment = stripped[2:].strip()
            if old_comment not in COMMENTS:
                raise ValueError(f"Unclassified source comment: {old_comment}")
            replacement = COMMENTS[old_comment]
            if not replacement:
                continue
            line = line[:len(line)-len(stripped)] + "// " + replacement
        if not line.strip() and (not lines or not lines[-1].strip()):
            continue
        lines.append(line.rstrip())
    return "\n".join(lines).strip() + "\n"


def old(name):
    return (OLD / name).read_text(encoding="utf-8")


def before_emit(code):
    return code.rsplit('emit({type:"text"', 1)[0].rstrip() + "\n"


def measured_outputs(code):
    """Keep numerical tables/plots; omit the original one-line status prose."""
    return "\n".join(line for line in code.splitlines()
                     if not line.lstrip().startswith('emit({type:"text"')) + "\n"


def comment_at(code, anchor, comment):
    if anchor not in code:
        raise ValueError(f"Missing comment anchor: {anchor}")
    return code.replace(anchor, comment + "\n" + anchor, 1)


def guard(group, stage, label):
    return f'if (!lab.{group}?.ready?.{stage}) throw Error("先运行{label}。");\n'


def ready(group, stages):
    return "ready:{" + ",".join(stage + ":true" for stage in stages) + "}"


def assign(group, members, stages):
    return f"Object.assign(lab.{group},{{{members},{ready(group, stages)}}});\n"


def cell(id, title, note, code, prior=None):
    return {"id": id, "title": title, "note": note, "lead": LEADS[id],
            "requires": [prior] if prior else [], "code": concise_source(code)}


def prepare(group):
    return f'''// 浏览器原生数学支持；这里运行的是 JavaScript。
if (typeof Math.exp !== "function" || typeof Float64Array !== "function")
  throw Error("当前环境缺少 Math 或 Float64Array。");
// 重建本组共享状态；后续单元将定义和计算结果存入 lab.{group}。
lab.{group} = {{ready:{{prepare:true}}, language:"JavaScript"}};
'''


hs = [cell("hs-prepare", "准备数值环境", "原生数学函数与双精度数组用于本页计算。", prepare("hs"))]
hs_config = guard("hs", "prepare", "准备环境") + old("hs_config.js") + assign(
    "hs", "cfg:hsCfg,...hsCfg,steps,Xright", ["prepare", "config"])
hs.append(cell("hs-config", "设置网格与时间步长", "默认配置对应原表 1；加密同一辅助区间时，同时增大 N、减小 a。", hs_config, hs[-1]["id"]))

hs_reference = guard("hs", "config", "网格与时间配置") + "const {N,a,Xleft,xMin,xMax}=lab.hs;\n" + old("hs_reference.js") + assign(
    "hs", "exactX,exactPhysical,initial,left,right,dx,fixedX", ["prepare", "config", "reference"])
hs_reference = comment_at(hs_reference, "  const uxx=", "  // 由 d/dx=J⁻¹d/dX 求 u_xx，供 FD 解析边界使用。")
hs_reference = comment_at(hs_reference, "const initial=", "// 两种格式覆盖相同物理端点；FD 在该区间均匀布点。")
hs.append(cell("hs-reference", "定义连续参考解与物理网格", "解析边界与误差参考采用式（24）；物理坐标由严格单调映射反解。", hs_reference, hs[-1]["id"]))

spatial, remaining = before_emit(old("hs_core.js")).split("// 式（29）：", 1)
rk4, state_helpers = remaining.split("function initialStates()", 1)
hs_spatial = guard("hs", "reference", "连续参考解") + "const {N,a,Xleft,left,right,dx,fixedX,initial,exactX,exactPhysical}=lab.hs;\n" + spatial + "function initialStates()" + state_helpers + assign(
    "hs", "integrableFields,integrableRHS,recoverU,fdFields,fdRHS,initialStates,interpolate", ["prepare", "config", "reference", "spatial"])
hs_spatial = comment_at(hs_spatial, "function integrableRHS", "// 式（25）：从节点 u 恢复胞元 b、d 的时间导数。")
hs_spatial = comment_at(hs_spatial, "function fdRHS", "// 式（28）：固定网格中心差分；解析边界已在 fdFields 中补入。")
hs_spatial = comment_at(hs_spatial, "function initialStates", "// 连续初值确定 b、d；FD 的初始 m 用同一 D₂ 模板计算。")
hs.append(cell("hs-spatial", "定义空间格式与场恢复", "Integrable 推进胞元变量；FD 推进内部节点变量，再由 Thomas 消元恢复 u。", hs_spatial, hs[-1]["id"]))

hs_rk4 = guard("hs", "spatial", "空间格式") + "// 式（29）：" + rk4 + assign("hs", "rk4Step", ["prepare", "config", "reference", "spatial", "rk4"])
hs.append(cell("hs-rk4", "定义四阶时间步", "一个时间步内依次计算四个阶段；本段登记算法，下一段推进状态。", hs_rk4, hs[-1]["id"]))

evolution, error = old("hs_compare.js").split("const xx=Float64Array", 1)
hs_evolution = guard("hs", "rk4", "四阶时间步") + "const {steps,dt,T,initialStates,rk4Step,integrableRHS,fdRHS,integrableFields,fdFields}=lab.hs;\n" + evolution
hs_evolution += assign("hs", "integrable,fd,liveFields", ["prepare", "config", "reference", "spatial", "rk4", "evolve"])
hs_evolution += '''emit({type:"table",columns:["方案","已推进步数","当前时间","物理节点数"],
  rows:Object.entries(liveFields).map(([name,f])=>[name,steps,T,f.x.length])});
'''
hs_evolution = measured_outputs(hs_evolution)
hs.append(cell("hs-evolve", "从初值实际推进至 T", "本段调用已经定义的空间格式与 RK4；每次运行从当前配置的连续初值开始。", hs_evolution, hs[-1]["id"]))

hs_error = guard("hs", "evolve", "实际演化") + "const {N,a,Xleft,dt,T,steps,xMin,xMax,evaluationPoints,liveFields,exactPhysical,interpolate}=lab.hs;\nconst xx=Float64Array" + error
hs_error = measured_outputs(hs_error).replace("} else {\n}\n", "}\n")
hs_error = comment_at(hs_error, "const xx=", "// 式（30）：在同一物理评价网格重构两场，再与连续解比较。")
hs_error = comment_at(hs_error, "    series.push", "    // 10⁻¹⁶ 仅为对数图的显示下限；误差表使用未经截断的数值。")
hs_error += assign("hs", "xx,reference,hsResults,resultRows", ["prepare", "config", "reference", "spatial", "rk4", "evolve", "error"])
hs.append(cell("hs-error", "计算终点误差并画图", "在相同物理评价点比较数值场与连续参考解；默认配置同时核对原表四项误差。", hs_error, hs[-1]["id"]))

dlw = [cell("error-prepare", "准备残差计算环境", "解析导数与有限格距残差均由原生 JavaScript 计算。", prepare("dlw"))]
dlw_config = guard("dlw", "prepare", "准备环境") + old("config.js") + assign("dlw", "cfg,...cfg,K,P,Q,ell,Gamma,Omega,zeta,zs", ["prepare", "config"])
dlw.append(cell("error-config", "设置谱参数与相位点", "参数 A 为默认示例；修改为 p=4、q=−3 可检查参数 B。", dlw_config, dlw[-1]["id"]))

profile, coeff = before_emit(old("core.js")).split("// 两分量二阶主系数", 1)
coeff, residual = coeff.split("// 连续解代入有限 h", 1)
dlw_profile = guard("dlw", "config", "谱参数配置") + "const {K,ell,Gamma}=lab.dlw;\n" + profile + assign("dlw", "sigmoidJet,profile", ["prepare", "config", "profile"])
dlw_profile = comment_at(dlw_profile, "function profile", "// u[n]、v[n] 为对相位 z 的第 n 阶导数。")
dlw.append(cell("error-profile", "定义连续剖面与解析导数", "按同一相位变量 z 计算两场及导数，避免数值微分。", dlw_profile, dlw[-1]["id"]))

dlw_coeff = guard("dlw", "profile", "连续剖面") + "const {profile,zeta}=lab.dlw;\n// 两分量二阶主系数" + coeff + assign("dlw", "coefficient,bounds", ["prepare", "config", "profile", "coefficient"])
dlw_coeff = comment_at(dlw_coeff, "  const B =", "  // B=(s″)²+s′s‴，即 ½[(s′)²]″；其符号保留在主系数中。")
dlw.append(cell("error-coefficient", "定义二阶主系数与解析上界", "主系数对应两条物理场方程；解析上界覆盖整个单孤子波形。", dlw_coeff, dlw[-1]["id"]))

dlw_residual = guard("dlw", "coefficient", "二阶主系数") + "const {a,K,ell,Omega,profile}=lab.dlw;\n// 连续解代入有限 h" + residual + assign("dlw", "residual", ["prepare", "config", "profile", "coefficient", "residual"])
dlw_residual = comment_at(dlw_residual, "    const D=", "    // D=δ₀u，W=v−δ₀u；每个偏移节点都重新恢复 W。")
dlw_residual = comment_at(dlw_residual, "  const plus=node(1/2)", "  // 第一式位于相邻节点中点；第二式位于 j=0。")
dlw.append(cell("error-residual", "定义有限格距方程残差", "连续场代入离散方程；横向与时间导数保持解析。", dlw_residual, dlw[-1]["id"]))

main, convergence = old("compare.js").split("const convergence=[]", 1)
dlw_main = guard("dlw", "residual", "有限格距残差") + "const {zs,a,K,ell,Omega,h,coefficient,profile,bounds}=lab.dlw;\n" + main + assign("dlw", "tau,continuumDefect,maxAbs,coeffRows", ["prepare", "config", "profile", "coefficient", "residual", "main"])
dlw_main = comment_at(dlw_main, "  const terms1=", "  // 连续两式逐项相加；分母为 1+各项绝对值之和。")
dlw_main += 'emit({type:"text",text:`continuumDefect = ${continuumDefect}`});\n'
dlw.append(cell("error-main", "计算主系数并核对解析上界", "表中同时列出当前相位采样最大值和全波形解析上界。", dlw_main, dlw[-1]["id"]))

dlw_convergence = guard("dlw", "main", "主系数计算") + "const {h,levels,zs,tau,residual,maxAbs,continuumDefect}=lab.dlw;\nconst convergence=[]" + convergence + assign("dlw", "convergence,finest", ["prepare", "config", "profile", "coefficient", "residual", "main", "convergence"])
dlw_convergence = measured_outputs(dlw_convergence)
dlw_convergence = comment_at(dlw_convergence, "const convergence=", "// 逐级将 h 减半，比较 R_h/h² 与同一相位上的二阶主系数。")
dlw_convergence = comment_at(dlw_convergence, "      const rate=", "      // 相邻两档差值的 log₂ 比；二阶余量对应 rate≈2。")
dlw.append(cell("error-convergence", "减半格距并画残差剖面", "现场计算 R_h/h² 与主系数之差，检查二阶收敛并保留曲线正负号。", dlw_convergence, dlw[-1]["id"]))

for name, cells in [("hs_cells.json", hs), ("cells.json", dlw)]:
    (HERE / name).write_text(json.dumps(cells, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in cells:
        (HERE / (item["id"] + ".js")).write_text(item["code"], encoding="utf-8")

hs_intro = '''<p>从准备环境、设置参数、定义连续参考解开始，逐段建立空间格式与 RK4，再实际推进单孤子，最后计算终点误差。每次点击 ▶ 只执行眼前这一段；已运行的定义保存在同一数值会话中。修改前面的代码后，依次重新运行受影响的后段。</p>
<p>默认采用原表的 $N=1600$、$a=0.005$、$\\Delta t=0.003125$、$T=0.5$ 与 32001 个评价点。密度在 Integrable 的胞元中点与 FD 的节点上分别重构。以下可编辑代码均以 JavaScript 在本地计算；原表仅用于默认配置的回归核对。误差图每点取一个物理小区间的最大值，低于 $10^{-16}$ 的读数在图中共用显示下限。</p>
'''
dlw_intro = old("intro.html")
dlw_intro = dlw_intro[:dlw_intro.rfind("<p>先修改谱参数")]
dlw_intro += '''<p>先准备数值环境，再设置谱参数，定义解析剖面、主系数与有限格距残差，最后分别计算主系数表与格距收敛图。每次点击 ▶ 只执行当前可见代码，前段定义在同一会话中供后段使用。采样最大值覆盖配置中的相位点，解析上界覆盖整个波形。减半格距时，$\\|\\mathcal R_h/h^2-\\tau_y\\|$ 应约缩小至四分之一。完整推导见 <a href="report/dlw_error_theory.html">DLW 误差理论</a>。</p>
'''
if "--cells-only" not in sys.argv:
    (HERE / "hs_intro.html").write_text(hs_intro, encoding="utf-8")
    (HERE / "intro.html").write_text(dlw_intro, encoding="utf-8")
print(json.dumps({"hs_cells": [item["id"] for item in hs], "dlw_cells": [item["id"] for item in dlw]}, ensure_ascii=False))
