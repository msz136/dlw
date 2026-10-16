"""Merge recovery results into the topic and the shared progress/index files.

No files are deleted. Original shared files were backed up in before/.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
TOPIC = ROOT / "刘维尔可积性"
HERE = Path(__file__).resolve().parent
STATE = r'''# 当前证据与继续研究入口

2026-10-11。持续目标是原半离散 DLW 在一般物理场上的完整 Liouville 可积性，**尚未完成**。以下区分形式层级、真实解流、辛结构与完备性；不以有限维特殊族替代一般场。阅读入口：[简明研究报告](../../report/dlw_liouville_recovery_20261011.html)、[检查点](../research_checkpoint.md)、[持续目标](../GOAL.md)。

## 本轮故障恢复与独立复核

此前 16 份研究文件已定位，恢复哈希与修改前副本保存在 [恢复工作目录](../../Workspaces/dlw_recovery_20261011/)。原脚本及 JSON 的三个 SHA-256 对照一致，没有重新启动旧检查。原文保持可追溯；当前审查以以下新文件为准。

| 结果 | 适用域与已证内容 | 尚不能推出 |
|---|---|---|
| [任意平均通量的中心化层级](unfixed_flux_hierarchy_20261011.md) | 任意有限 M≥2、周期 x、c≠0。KΓ=K₀+(Γ/c)P−hMLΓ²/(2c)；任意 Γ(t) 的实际解与零通量规范双向对应。Ĉₙ=Tr(LΓ−Γ/(2c))ⁿ/n 全阶形式对合、沿实际解守恒；30 项新精确检查通过，独立二审通过 | 固定周期域的实际等谱；逆谱与完备性。实际 Floquet 数据须同时中心化 λ 和 exp(−fL)ρ |
| [局部状态逆与完整 Floquet 通道](spectral_independent_review_20261011.md) | 全 M、c≠0、固定组件均值，均匀背景附近或跨根分离实常场。有限 2(M−1) 个 Lax 系数在实际物理像上非线性可逆；完整固定基点 Floquet 矩阵线性共振采样恢复全部非零 Fourier 方向；谱迹与动量分离有限通道 | 无约束 Banach 开数据逆；谱不变量与角数据的非线性逆；物理辛匹配 |
| [全频线性层级闭包](spectral_independent_review_20261011.md) §4 | 0<|hc/8|<(π/L)tan(π/(2M))，明确正指数权重。全频共振边端点不重叠，多项式频率差在加权 ℓ² 中稠密；指数矩/Fourier 唯一性证明经独立二审核对；谱脚本 48 组检查通过 | 物理拓扑中的非线性最大各向同性、作用角坐标 |
| [真实混合解及有限共同层级](mixed_independent_review_20261011.md) | 全 M、c≠0、一般光滑函数输入。原二阶中心/微分/端点唯一性与弱辛性复核通过；X_Cₙ 的常系数主部与低一阶余项全阶推导；每个有限奇前缀有真实共同多时间解和中心 germ 局部共同流；21 组检查通过 | 新高阶共同域弱非退化；无限层级一致域非平凡性与内在物理刻画。固定窗口 Sobolev/C∞ 参数开集仍有高频可微 Cauchy 流障碍 |
| [共同实际域上的有限积分块独立](mixed_independent_review_20261011.md) §7.1 | 包含均匀态的组件零空间均值叶；每个有限前缀的测试 Fourier 中心变分可由实际混合输入实现，Hessian Vandermonde 给 P、C₁、C₃、… 独立的非空开区及局部解析泛性 | 同一状态全部无限微分独立；所有均值叶上的全域泛性与谱完备性 |
| [c=0、Γ≠0 独立复核](c0_independent_review_20261011.md) | 原方程强制 Γ_t=0，Γ 是初值动量而非 Casimir；非恒定 q 模 Dirac 张量；平方根形式谱迹全阶对合守恒。每个 M、每个有限积分块在 Γ 正负扇区有非空相对开独立区；固定见证组件均值；31 组检查通过 | 严格每组件均值全零叶或任意固定均值叶的泛性；一般非线性共同解与完备性 |
| [c=Γ=0、χ=κ≠0 次约束层](singular_branch_review_20261011.md) | 权三恒等式 X_Fχ=−fχ_x−3f_xχ；主、次非零模交叉 −3κD 可逆；ρ=Dη，真实一致性强制 κ_t=0 与 b=(η−平均η)/(3κ)+B(t)。M≥3 有非恒定函数约束点；首项 a₃=hMκ/16，三次根形式谱迹的分级 Dirac 证明已写出 | 真实时间流存在/唯一、统一 Sobolev 张量、全局弱辛商；κ=0 更深约束层。三次根全阶证明的独立二审正在进行 |
| [实全线混合候选审计](mixed_bvp_audit.md) | M=2、m=Ax、A>0、有限时间窗；指定线性逆、端点迹、负移位拼接及三次估计有补证 | 未复核矩归纳、非线性中心单射及其 Liouville 主张；不认证整份候选报告 |

## 不同平均分支的准确闭合

令 β=h²/32，R 为格点反对称矩阵。在 c=0、U=b+p、w=s、Πp=Πs=0 时，

$$
q_t=-bq_x-2qb_x+Dχ,
\qquad
χ=-\Pi(p^2s)-\frac{2β}{3}\Pi s^3
+\Pi(ps_x-sp_x)-\Pi(sRs_x)=-2e+q_x.
$$

周期兼容先给 q_x=0，再给 Γ_t=0；不能从 c≠0 分支外推这一结论。Γ≠0 时，平均共同场为零的 Dirac H₀ 流对应 b=(χ−平均χ)/(2Γ)。跨状态固定 raw 积分常数与固定 mean b 不能混同。

Γ=0 时必须继续约束链。χ=κ≠0 层的 κ 守恒由次约束一致性推出；非恒定主、次约束二类配对后，零动量水平仍有空间平移核，正则局部弱辛商需要再约去这一方向。常数场属于另一个奇异层。三次根高阶守恒不自动提供此层的实际辅助流。

## 实际共同流与谱路线的连接点

原二阶混合域有中心单射、微分单射及弱非退化拉回形式。高阶辅助 lift 在 Xᵣ=Hᵣ×Hᵣ⁺¹ 上为常系数阶 n+1 主部加 Xᵣ→Xᵣ⁻ⁿ 解析余项；奇 n 的半群积分损失指数 n/(n+1)<1，故可逐层构造实际共同解。复时间解析性只给内点中心唯一性，不能偷换高阶端点唯一性。

有限共同域随新增时间嵌套；它们各有一般函数参数，但尚不能证明无限交集除平衡点外宽广。全频谱稠密性目前属于明确权重的线性通道空间；需要证明完整 Floquet 通道对物理弱辛形式的匹配，再接非线性逆谱。

## 原始推导与恢复证据

- [线性标量忠实性](scalar_monodromy_linearization.md)、[脚本](verify_scalar_monodromy_linearization.py)、[17 项旧检查](scalar_monodromy_linearization_checks.json)。
- [原非线性局部像逆](completeness_routes.md)、[核验说明](nonlinear_inverse_checks.md)、[脚本](nonlinear_inverse_checks.py)、[旧记录](nonlinear_inverse_checks.json)；[本轮逆像独立审查](../../Workspaces/dlw_recovery_20261011/spectral_local_inverse_audit.md)。
- [全 M 周期结构](periodic_structure_audit.md)、[原二阶实际解](full_m_mixed_flow.md)、[原混合弱辛性](mixed_phase_symplecticity.md)、[静态物理像 Poisson 商](scalar_poisson_quotient.md)。
- [原零平均审计](c0_branch_audit.md)、[旧脚本](verify_zero_mean_branch.py)、[旧记录](zero_mean_branch_checks.json)。本轮平均规范、独立性与主符号以新独立复核为准。
- [任意通量二审](../../Workspaces/dlw_recovery_20261011/unfixed_flux_independent_audit.md)。所有新证书与报告源位于 [恢复工作目录](../../Workspaces/dlw_recovery_20261011/)。
- [归档历史](../progress.md)、[原混合候选报告](../sources/2026-10-11_mixed_bvp_candidate.md) 保留原样，不把报告作者声称当作本轮认证结果。

## 接续任务

1. 完成新增高阶共同域的弱非退化及一般函数无限层级一致域；继续核对端点问题，不能用内点解析性绕过。
2. 计算完整 Floquet 线性通道的物理辛形式与高频映射阶数，再构造非线性谱/角数据局部逆及极大各向同性。
3. c=0、Γ≠0 的一般非线性约束混合流；c=Γ=0 的次约束层实际流与更深分层；非周期仿射平均另行推进。

每获得可核验结果即保存，依照 [GOAL.md](../GOAL.md) 继续，不以候选失败、局部结论或特定拓扑下初值障碍作为主目标完成。
'''

CHECKPOINT = '''# 研究检查点

2026-10-11。原半离散 DLW 一般物理场上的完整 Liouville 目标仍未完成；持续授权与要求见 [GOAL.md](GOAL.md)。当前证明、适用域及缺口以 [research/STATE.md](research/STATE.md) 为入口，[用户阅读报告](../report/dlw_liouville_recovery_20261011.html) 概述本轮结果。

## 故障恢复与执行状态

- 已定位本专题原有 16 份研究文件、旧检查点和三份完成的脚本证书，没有虚构 research_work/ 继承结果。[哈希清单](../Workspaces/dlw_recovery_20261011/recovered_manifest.json) 与 `before/` 修改前副本保存恢复时状态；旧脚本 SHA-256 与三份 JSON 一致。
- 工作区 HEAD 为 e2ee3cc6a022c0afc723e3324b3cc57a0fa5b143；既存修改保留。本轮不提交、不推送、不删除文件，也没有重启旧任务已完成的检查。
- PowerShell、Python 3.13.3、SymPy 1.13.3 可用，rg 不可用。工作区及用户目录未找到 `.agents/skills`。进程名称查询未检出 Python/Lean/Lake/Node 核验进程；CIM 详情查询受限，不能据此宣称完整系统进程审计。
- 接口没有当前根任务模型/思考/速度的可核验字段。本地默认配置不用于推断实际任务模型；新复核子任务显式指定 GPT-6.1 Sol/Ultra，速度无可设置字段。没有调用外部 Chat/Pro 或启动其他昂贵模型。没有原生 Goal 工具，使用 GOAL.md 跟进。

## 新增结果与证据

1. [任意 Γ(t) 的全 M 中心化层级](research/unfixed_flux_hierarchy_20261011.md)：准确 Hamiltonian 分解、真实解双向平移对应、全阶中心化谱迹守恒/对合、原谱迹漂移与非自治 Lax 公式。30 项新检查通过，[独立二审](../Workspaces/dlw_recovery_20261011/unfixed_flux_independent_audit.md) 通过；实际 Floquet 数据需同时中心化 λ 与连续空间 multiplier。
2. [c=0、Γ≠0 的独立复核](research/c0_independent_review_20261011.md)：原流强制 Γ 守恒；平方根层级与正确 mean-b Dirac 规范；全 M 任意有限积分块在正负 Γ 扇区有非空相对开独立区；约束主符号和线性真实混合解。31 组证书通过，一般非线性共同流仍缺。
3. [全 M 真实有限共同层级](research/mixed_independent_review_20261011.md)：二阶 Carleman/弱辛依赖通过复核；全阶常系数主部；高阶混合收缩与复时间中心唯一性；一般函数输入的任意有限奇前缀真实共同解和中心 germ 共同局部流。21 组证书通过。新增高阶域弱非退化与无限层级一致域仍待证。
4. [谱逆与全频线性闭包](research/spectral_independent_review_20261011.md)：实际物理像有限系数非线性局部逆补齐 Jordan 旗标/共同均值/有限导数预算；完整 framed Floquet 通道线性可恢复；小背景阈值下指数权重全频频率稠密，独立二审通过。48 组证书通过；非线性逆谱、物理辛匹配与最大各向同性仍缺。
5. [c=Γ=0、χ=κ≠0 层](research/singular_branch_review_20261011.md)：主次约束二类配对、权三律、ρ=Dη、自动 κ 守恒、二阶共同场闭合、非恒定 M≥3 约束点、三次根形式层级。新证书已保存，独立二审仍在进行。κ=0 更深层不升级为已完成定理。

## 恢复原稿的审查范围

原二阶混合解及弱辛性以新的独立审查为准。原有限系数状态逆是实际像上的逆，不是完整谱不变量逆。原 M=2、m=Ax 外部候选仅有 [指定线性逆、迹与三次估计的补证](research/mixed_bvp_audit.md)，未完整认证矩归纳和后续 Liouville 主张。[归档 progress.md](progress.md) 与外部报告保留原样。

## 当前接续任务

新增高阶共同域的弱非退化、无限层级一般函数一致域；framed Floquet 通道的物理辛匹配及非线性逆谱；零平均正则/次约束层的真实共同流和更深约束分层。当前谱代理继续计算线性物理辛匹配，混合域代理继续攻击高阶端点/Hessian 问题，奇异层正在独立二审；这些活动不会重跑旧任务。

落盘脚本及证书位于 [Workspaces/dlw_recovery_20261011](../Workspaces/dlw_recovery_20261011/)。交付前更新本检查点与验证记录，保存准确停止点；候选失败、局部进展或技术故障均不记为主目标完成。
'''

PROGRESS_PARAGRAPH = '''> **2026-10-11（DLW 一般场可积性：故障恢复与新增证明）：** 已定位并备份此前16份研究材料，原检查脚本哈希一致；保留既存改动，无删除、提交或推送。全M、c≠0分支移除固定平均通量闭合：真实解可双向平移恢复任意Γ(t)，中心化谱迹全阶形式对合且沿实际解守恒，30项新精确检查及二审通过。已构造任意有限奇前缀的一般函数真实共同多时间解与中心germ局部共同流，原二阶弱辛性复核通过，21组新检查通过；新增高阶联合域弱非退化及无限层级一致域仍待证。全M实际像局部状态逆补齐，完整framed Floquet变分可恢复全部非零Fourier方向；明确小背景/指数权重下全频线性层级稠密，48组检查及独立二审通过，尚非非线性逆谱或最大各向同性。c=0、Γ≠0的任意有限奇积分块在正负Γ扇区有非空相对开独立区，31组检查通过；c=Γ=0新增χ=κ≠0主次约束层、自动κ守恒与二阶共同场闭合，三次根形式层级正在二审。完整一般场Liouville定理尚未完成。阅读 [研究报告](report/dlw_liouville_recovery_20261011.html)，接续 [研究检查点](刘维尔可积性/research_checkpoint.md) 与 [STATE](刘维尔可积性/research/STATE.md)。
'''


def write(path, content):
    path.write_text(content, encoding="utf-8")


def upgrade_current_results():
    """Incorporate proofs completed after the temporary disconnection."""
    global STATE, CHECKPOINT, PROGRESS_PARAGRAPH
    rows = {
        "| [全频线性层级闭包]": "| [全频线性辛匹配与最大性](spectral_independent_review_20261011.md) §§4、7–10 | 0<|hc/8|<(π/L)tan(π/(2M))。完整 framed Floquet 共振坐标精确拉回物理 Ω，并有 Hˢ→hˢ⁺½ 有界同构；全部谱迹加动量的线性/二次分布在明确权重下最大各向同性。强衰减 Fréchet 序列域承载全族真实共同线性流；原 48 组、新 332 项精确/数值检查通过 | 仅奇谱迹加一个动量严格遗漏相位方向；线性强衰减域尚未与原非线性实际域识别；非线性逆谱、作用角及最大性仍缺 |",
        "| [真实混合解及有限共同层级]": "| [全部谱迹的真实有限共同弱辛域](mixed_independent_review_20261011.md) §§11–12 | 全 M、c≠0、一般光滑函数输入。奇层级用实混合、偶层级用虚时间 Fourier 混合及反射得到真实实时间流；每个有限全部谱迹前缀有共同 germ 局部流。所有可缩窗口联合域以切向密度及无 ghost 证明弱辛非退化；21 组原主符号检查通过 | 不是每个固定图的端点唯一性/弱辛性；不是普通 Sobolev/C∞ 开 Cauchy 域；无限域统一弱辛性仍缺 |",
        "| [共同实际域上的有限积分块独立]": "| [全部有限积分块的实际独立性](mixed_independent_review_20261011.md) §§14–15 | 明确小背景、包含均匀态的组件平均叶。每个有限 C₁,…,Cₙ、P 块在真实共同域有非空相对开独立区；全通道 Hessian 多项式给满秩，紧参数对角构造将见证提升到全部可数层级相容的光滑族 | 不等于同一基点的无限切向稠密性；一般组件平均叶、非线性谱极大性仍缺 |",
        "| [c=Γ=0、χ=κ≠0 次约束层]": "| [c=Γ=0、χ=κ≠0 次约束层](singular_branch_review_20261011.md) | 权三律、ρ=Dη、自动 κ 守恒与二阶 b 闭合；主次非零模二类配对、三次根形式谱迹全阶对合守恒。独立二审核对通过并补 N 降为一阶、χ 三次根密度 Diff 平坦化及自由平移局部弱辛商；33 项原新证据与 81 项独立算子/常背景主符号 assert 通过 | 普通 Sobolev 非线性真实共同流、谱独立与完备性；κ=0 更深层及全局商图册 |",
    }
    lines = STATE.splitlines()
    for index, line in enumerate(lines):
        for prefix, replacement in rows.items():
            if line.startswith(prefix):
                lines[index] = replacement
    STATE = "\n".join(lines) + "\n"
    insertion = "| [无限相容共同 germ 的存在与密度](mixed_independent_review_20261011.md) §13 | 对已固定有限复合逐层选正窗口，尾序列在每个半范数 Cauchy 且极限严格留在各源域；构造全部谱迹相容实际共同解，共享每个时间坐标的正宽。在各有限前缀生成像中 ambient C∞ 稠密；每个层级真实局部流保持此相容域 | 点态密度不等于切向密度；无限域 internal tangent、统一弱辛性与 Liouville 极大性仍待证 |\n"
    STATE = STATE.replace("| [全部有限积分块的实际独立性]", insertion + "| [全部有限积分块的实际独立性]")
    STATE = STATE.replace("高阶辅助 lift 在 Xᵣ=Hᵣ×Hᵣ⁺¹ 上为常系数阶 n+1 主部加 Xᵣ→Xᵣ⁻ⁿ 解析余项；奇 n 的半群积分损失指数 n/(n+1)<1，故可逐层构造实际共同解。复时间解析性只给内点中心唯一性，不能偷换高阶端点唯一性。", "高阶辅助 lift 在 Xᵣ=Hᵣ×Hᵣ⁺¹ 上为常系数阶 n+1 主部加 Xᵣ→Xᵣ⁻ⁿ 解析余项。奇层级实混合与偶层级虚时间 Fourier 混合均以 n/(n+1)<1 的可积核构造真实共同解；偶层级反射保证实时间轴上的场为实。缩窗切向密度及共同图去 ghost 证明有限联合 germ 域弱辛，无需高阶端点唯一性。")
    STATE = STATE.replace("有限共同域随新增时间嵌套；它们各有一般函数参数，但尚不能证明无限交集除平衡点外宽广。全频谱稠密性目前属于明确权重的线性通道空间；需要证明完整 Floquet 通道对物理弱辛形式的匹配，再接非线性逆谱。", "有限共同域随新增时间嵌套。对角构造已建立非平凡的无限相容共同域及其在各有限生成像中的点态稠密性，不能据此直接传递有限域的辛切向结构。谱侧已有全频线性物理辛匹配、明确权重下全部谱迹的线性/二次最大各向同性；仅奇谱迹加动量严格遗漏相位方向。接续仍需无限实际域的统一弱辛性与非线性逆谱。")
    STATE = STATE.replace("1. 完成新增高阶共同域的弱非退化及一般函数无限层级一致域；继续核对端点问题，不能用内点解析性绕过。", "1. 在已存在的无限相容共同 germ 域上构造合法 internal tangent/plots 与统一弱辛结构；有限域结果不能未经补证搬到无限域。")
    STATE = STATE.replace("2. 计算完整 Floquet 线性通道的物理辛形式与高频映射阶数，再构造非线性谱/角数据局部逆及极大各向同性。", "2. 将已算出的全频线性物理辛规范及全部谱迹线性最大性接到非线性谱/角数据局部逆与原场极大各向同性。")
    STATE = STATE.replace("- [任意通量二审]", "- [零通量次约束层二审](../../Workspaces/dlw_recovery_20261011/singular_branch_independent_audit.md)：N 的全 M 精确公式、三次密度 Diff 切片与归一化余切对合链。\n- [任意通量二审]")
    CHECKPOINT = CHECKPOINT.replace("3. [全 M 真实有限共同层级]", "3. [全 M 全部谱迹的真实有限共同层级]")
    CHECKPOINT = CHECKPOINT.replace("一般函数输入的任意有限奇前缀真实共同解和中心 germ 共同局部流。21 组证书通过。新增高阶域弱非退化与无限层级一致域仍待证。", "一般函数输入的任意有限全部谱迹前缀真实共同解、中心 germ 局部共同流及联合域弱辛性。§12 补偶谱迹的虚时间反射构造；§13 以逐层有限复合连续性预算建立非平凡且逐有限图点态稠密的无限相容域，共享逐坐标正窗口。21 组原证书通过。无限域统一辛切向结构仍待证。")
    CHECKPOINT = CHECKPOINT.replace("新证书已保存，独立二审仍在进行。", "33 项新证据通过；[独立二审](../Workspaces/dlw_recovery_20261011/singular_branch_independent_audit.md) 已通过，并新增 N 降阶与三次密度 Diff 静态弱辛商。离线前启动的附加算子脚本恢复后读得 25 assert 通过、哈希一致，未重跑。")
    CHECKPOINT = CHECKPOINT.replace("48 组证书通过；非线性逆谱、物理辛匹配与最大各向同性仍缺。", "48 组原证书及 332 项新精确/数值检查通过；§§7–10 建立全频线性物理辛匹配、全部谱迹线性/二次最大性和共同真实线性流域，并证明奇谱迹加动量的相位遗漏。原非线性逆谱、无限实际域辛匹配与最大各向同性仍缺。")
    CHECKPOINT = CHECKPOINT.replace("κ=0 更深层不升级为已完成定理。", "另 56 assert 独立核验兼容常背景的 ±i/√3 与 ±1 主符号（该审稿合计 81 assert）；常背景为动量临界点，不能直接报正则商的流反例。κ=0 更深层不升级为已完成定理。")
    CHECKPOINT = CHECKPOINT.replace("新增高阶共同域的弱非退化、无限层级一般函数一致域；framed Floquet 通道的物理辛匹配及非线性逆谱；零平均正则/次约束层的真实共同流和更深约束分层。当前谱代理继续计算线性物理辛匹配，混合域代理继续攻击高阶端点/Hessian 问题，奇异层正在独立二审；这些活动不会重跑旧任务。", "无限相容域的统一辛切向结构；全谱迹线性最大性向原非线性谱坐标/作用角的提升；零平均正则/次约束层的真实共同流和更深约束分层。离线期间没有重复本地调用，恢复后先生成报告与同步检查点，再保存补充证明；已完成证书不重跑。谱侧的新线性辛/最大性与共同线性流域正在落盘，奇异层继续研究 M=3 色散桥及全 M 主符号。")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("任意有限奇前缀的一般函数真实共同多时间解与中心germ局部共同流", "全部谱迹（含偶层级）的任意有限前缀一般函数真实共同多时间解与中心germ局部共同流")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("新增高阶联合域弱非退化及无限层级一致域仍待证", "所有可缩窗口联合域已证弱辛，逐层对角构造建立在各有限前缀像中稠密的无限相容共同germ域；其统一辛切向结构仍待证")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("三次根形式层级正在二审", "三次根形式层级独立二审通过；补三次密度Diff局部弱辛商与25项次约束算子检查")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("明确小背景/指数权重下全频线性层级稠密，48组检查及独立二审通过，尚非非线性逆谱或最大各向同性", "明确小背景下全频线性物理辛匹配及全部谱迹线性/二次最大性成立；只有奇谱迹加动量会遗漏相位方向。强衰减序列域承载共同真实线性流，原48组及新332项检查通过，尚非原非线性逆谱或最大各向同性")
    m3_row = "| [零通量 M=3 的原物理实际流](singular_m3_actual_flow_20261011.md) §§1–3 | c=Γ=0、κ≠0；r*>0、d=hr*/8、a*>2d、a*≠6d 的实非共振背景附近。精确三阶分母变为实 good Boussinesq；半线性 Schrödinger 给共同光滑时间窗，正实 labelled Floquet 旗标及一般六因子微分逆回拉原 PDE。任意 B(t) 以平移加共同 U 加量恢复；42 项主稿与 15 项独立因子断言通过 | 是无限维兼容物理局部图，不覆盖图外、所有平均叶或 M>3；全部辅助真实流、谱独立与完备性仍缺 |\n"
    STATE = STATE.replace("| [实全线混合候选审计]", m3_row + "| [实全线混合候选审计]")
    STATE = STATE.replace("33 项原新证据与 81 项独立算子/常背景主符号 assert 通过", "33 项原新证据与 81 项独立算子/常背景主符号 assert 通过；完整变量系数消元证明所有正则 κ 层的主符号为 (λ²+1/3)(λ²−1)^(M−3)，66 项新检查及独审通过")
    tail = "固定均匀背景的 raw framed 采样有非线性代数尾项。谱稿 §11 在 M=2 的有限 Fourier 原場证明 companion Q_raw,k~const·k^(−5/2)，阻断 s≥3/2 的同阶映射；未校准原始 frame 更有 k^(−3/2) 尾，阻断 s≥1/2（含端点）的 Hˢ→hˢ⁺½。六次实际 monodromy 积分及独立审稿核对通过。§11.3 在开放 Cᴿ 源域证明首项重整化为真实解析序列图，目标正则性提高一阶且保留背景前二 jet；它还不是同阶 Sobolev 逆。后续须控制移动 holonomy/gap/frame 或重整化的统一 Sobolev 余项。"
    STATE = STATE.replace("## 原始推导与恢复证据", tail + "\n\n## 原始推导与恢复证据")
    STATE = STATE.replace("- [零通量次约束层二审]", "- [M=3 实际流独立审稿](../../Workspaces/dlw_recovery_20261011/singular_m3_flow_independent_audit.md)：直接原 PDE 因子 Lax、一般六系数互逆微分、周期规范及共同 U 恢复。\n- [零通量次约束层二审]")
    CHECKPOINT = CHECKPOINT.replace("## 恢复原稿的审查范围", "6. [零通量 M=3 原物理实际流](research/singular_m3_actual_flow_20261011.md)：指定实非共振无限维兼容图内的双向局部光滑存在唯一性。三阶分母精确 good Boussinesq、共同 L² 时间窗上的所有阶保持、实标号 Floquet 图及一般六因子微分逆已补齐；42 项新 exact 检查与[独立 15 项因子审稿](../Workspaces/dlw_recovery_20261011/singular_m3_flow_independent_audit.md)通过。任意共同 B(t) 同时恢复平移与 U 加量，不冒充全 M 结果。\n7. 全 M、所有非恒定正则 κ≠0 背景的主符号已由完整 D³φ 消元证明，导数项 −4(S_x,T_x) 吸收 Wronskian 后仍为 (λ²+1/3)(λ²−1)^(M−3)。66 项兼容 first-jet 检查及独立手推通过；尚未据此宣称真实流不适定。\n8. 混合稿 §§14–15 将全部有限谱迹块独立见证提升到可数相容共同域的光滑参数族。谱稿 §11 证明 companion/raw 原始 frame 的非线性尾项分别阻断 s≥3/2 与 s≥1/2 的同阶 Banach 逆；六次真实 monodromy 积分及[独立审稿](../Workspaces/dlw_recovery_20261011/spectral_fixed_frame_tail_independent_audit.md)通过。开放 Cᴿ 上的真实首项重整化解析引理已证明，还不是同阶 Sobolev 逆。\n9. [全 M 实有理背景的非空性](research/real_rational_background_20261011.md)：取实简单 Q、K 且无共同根，R=Q+aK 保留实简单根并精确满足 c=q=0、κ=16a/(hM)≠0。一般函数 flag 图非空；新证书通过116项 exact 断言。\n\n## 恢复原稿的审查范围")
    CHECKPOINT = CHECKPOINT.replace("谱侧的新线性辛/最大性与共同线性流域正在落盘，奇异层继续研究 M=3 色散桥及全 M 主符号。", "谱侧线性辛/最大性、共同线性域、raw frame 尾项障碍均已保存；M=3 实际流和全 M 变量主符号已完成独审。当前进一步攻击无限共同域同一基点的合法弱辛切向结构与修正非线性谱图。")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("完整一般场Liouville定理尚未完成。", "全部有限积分块独立见证已提升到可数相容光滑族。零通量M=3指定无限维物理图内的双向局部光滑流独审通过（42+15项）；全M非恒定κ层主符号证明与66项检查通过。固定背景raw谱采样的非线性k^(-5/2)尾项阻断高正则同阶逆，路线转向移动frame或渐近减项。完整一般场Liouville定理尚未完成。")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("固定背景raw谱采样的非线性k^(-5/2)尾项阻断高正则同阶逆，路线转向移动frame或渐近减项。", "companion与未校准原始frame的非线性尾项分别阻断s≥3/2及s≥1/2同阶逆；已证开放Cᴿ域首项重整化解析引理，六次实际monodromy积分及二审通过。全M正则零通量实有理图非空证明与116项exact检查保存。")


    # The strong infinite-domain result is stronger than the earlier density note.
    final_rows = {
        "| [无限相容共同 germ 的存在与密度]": "| [无限实际共同域的合法弱辛结构](mixed_independent_review_20261011.md) §§13、16 | 全 M、c≠0 的强 mixed-coherent 一般函数域。相对 compact-family 延拓精确保留既有基点与约束曲线；坐标轴合成有限切向和、Hadamard 抛物线延拓排除内部 ghost，同基点真无限 plots 切向稠密，故物理 Ω 为内部弱辛形式。全部谱迹有真实逐坐标共同 Hamiltonian 时间 germs | 只覆盖有固定逐坐标复 presentation 的强子域，不覆盖任意仅实 coherent 族；不是普通 Sobolev 开 Cauchy 域；非线性 Liouville 极大性及逆谱仍缺 |",
    }
    lines = STATE.splitlines()
    for index, line in enumerate(lines):
        for prefix, replacement in final_rows.items():
            if line.startswith(prefix):
                lines[index] = replacement
    STATE = "\n".join(lines) + "\n"
    STATE = STATE.replace("不是普通 Sobolev/C∞ 开 Cauchy 域；无限域统一弱辛性仍缺", "不是普通 Sobolev/C∞ 开 Cauchy 域；更大的仅实 coherent 域不自动继承 §16 强域结构")
    STATE = STATE.replace("有限共同域随新增时间嵌套。对角构造已建立非平凡的无限相容共同域及其在各有限生成像中的点态稠密性，不能据此直接传递有限域的辛切向结构。", "有限共同域随新增时间嵌套。对角构造建立非平凡的无限相容共同域；§16 在强复 mixed presentation 子域上进一步证明同一基点真切向稠密及内部无 ghost，给合法无限弱辛结构，没有用点态密度替代切向密度。")
    STATE = STATE.replace("接续仍需无限实际域的统一弱辛性与非线性逆谱。", "主要接续是同一实际弱辛域上的非线性逆谱与极大各向同性。")
    STATE = STATE.replace("1. 在已存在的无限相容共同 germ 域上构造合法 internal tangent/plots 与统一弱辛结构；有限域结果不能未经补证搬到无限域。", "1. 在已证强 mixed-coherent 无限弱辛域上推进同一状态的全部守恒微分独立与非线性极大各向同性；更大的仅实 coherent 域仍另需研究。")
    CHECKPOINT = CHECKPOINT.replace("无限域统一辛切向结构仍待证。", "§16 已用相对延拓、同基点真实切向密度与内部 ghost 消除建立强 mixed-coherent 子域的真正无限弱辛结构及全部逐坐标 Hamiltonian 时间 germs；不覆盖任意仅实 coherent 域。")
    CHECKPOINT = CHECKPOINT.replace("无限相容域的统一辛切向结构；", "强无限弱辛域上同一状态的全族微分独立；")
    CHECKPOINT = CHECKPOINT.replace("当前进一步攻击无限共同域同一基点的合法弱辛切向结构与修正非线性谱图。", "§16 强无限域弱辛结构已保存；当前进一步攻击同一状态全族微分独立、修正非线性谱图及零通量全 M 实际混合流。")
    PROGRESS_PARAGRAPH = PROGRESS_PARAGRAPH.replace("所有可缩窗口联合域已证弱辛，逐层对角构造建立在各有限前缀像中稠密的无限相容共同germ域；其统一辛切向结构仍待证", "有限可缩窗联合域弱辛；强mixed-coherent无限共同域已通过同基点真切向稠密与内部ghost消除证明真正弱辛，承载全部逐坐标实际Hamiltonian时间germs")


def merge_progress():
    path = ROOT / "PROGRESS_LOG.md"
    text = path.read_text(encoding="utf-8")
    begin, end = "<!-- DLW_HAMILTON_BEGIN -->", "<!-- DLW_HAMILTON_END -->"
    assert text.count(begin) == text.count(end) == 1
    start, stop = text.index(begin), text.index(end) + len(end)
    block = text[start:stop]
    # Replace only this run's paragraph when repeated, preserving all history.
    block = re.sub(r'> \*\*2026-10-11（DLW 一般场可积性：故障恢复与新增证明）：\*\*[^\n]*\n?', '', block)
    block = begin + "\n" + PROGRESS_PARAGRAPH + "\n" + block[len(begin):].lstrip("\n")
    remaining = text[:start] + text[stop:]
    write(path, block + "\n\n" + remaining.lstrip("\n"))


def merge_index():
    path = ROOT / "FILE_INDEX.md"
    text = path.read_text(encoding="utf-8")
    begin = "<!-- DLW_LIOUVILLE_RECOVERY_INDEX_BEGIN -->"
    end = "<!-- DLW_LIOUVILLE_RECOVERY_INDEX_END -->"
    if begin in text:
        start, stop = text.index(begin), text.index(end) + len(end)
        text = text[:start] + text[stop:]
    paths = [TOPIC / name for name in ("README.md", "GOAL.md", "progress.md", "research_checkpoint.md")]
    paths += sorted((TOPIC / "research").glob("*"))
    paths += sorted(HERE.glob("*"))
    paths += sorted((ROOT / "Paper/refs/akns_transfer_20261011").glob("*"))
    paths += [ROOT / "report/dlw_liouville_recovery_20261011.html", ROOT / "report/dlw_m2_conditional_theorem_20261011.html", ROOT / "report/dlw_m2_regular_liouville_20261011.html", HERE / "delivery_validation.json"]
    lines = [begin, "## DLW 一般场可积性研究与故障恢复（2026-10-11）", ""]
    seen = set()
    for item in paths:
        if item.name == "__pycache__":
            continue
        rel = item.relative_to(ROOT).as_posix()
        if rel in seen:
            continue
        seen.add(rel)
        if item.is_dir():
            rel += "/"
        lines.append(f"- [{rel}]({rel})")
    lines += [end, "", ""]
    write(path, "\n".join(lines) + text.lstrip("\n"))


if __name__ == "__main__":
    upgrade_current_results()
    write(TOPIC / "research/STATE.md", STATE)
    write(TOPIC / "research_checkpoint.md", CHECKPOINT)
    readme = TOPIC / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = text.replace("本专题汇总现有结果、前提与缺口；本次仅整理文档，未开展新证明、数值研究或重跑历史核验。", "本专题保留原归档与后续研究；本轮已开展独立复核和新证明，未重启历史检查。")
    old = "后续研究已独立核验并保存：全 M 非线性局部状态逆、周期混合解中心唯一性，以及 c=0、Γ≠0 的约束谱迹层级。最新证据和下一步见 [research/STATE.md](research/STATE.md)；这些结果仍未完成完整 Liouville 定理。"
    new = "本轮新增任意 Γ(t) 的中心化守恒层级、全部谱迹任意有限前缀的真实共同弱辛域、非平凡无限相容共同解、全频线性谱辛匹配，以及零平均约束层的独立性和次约束分析。阅读 [简明研究报告](../report/dlw_liouville_recovery_20261011.html)；完整证明与缺口见 [research/STATE.md](research/STATE.md)，恢复接续见 [research_checkpoint.md](research_checkpoint.md)。以下原路线表及 M=2、m=Ax 公式保留归档范围，不代表当前主线锁定该分支。"
    text = text.replace(old, new)
    text = re.sub(r"本轮新增任意 Γ\(t\) 的中心化守恒层级、[^\n]+以下原路线表及 M=2、m=Ax 公式保留归档范围，不代表当前主线锁定该分支。", new, text)
    text = text.replace("## 下一步\n", "## 原归档接续路线（当前任务以 STATE 为准）\n")
    write(readme, text)
    merge_progress()
    merge_index()
    print("Merged STATE, checkpoint, README, PROGRESS_LOG and FILE_INDEX.")
