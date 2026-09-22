# RUN_CONTEXT — DLW 沿 y 方向八类离散化方法的并行研究

- 运行目录：`expression_deepseek-v4-flash_20260917_220258`
- 开始时间：2026-09-17 22:02（本地）
- 主 Agent 模型：DeepSeek V4 Flash（用户确认）；slug：`deepseek-v4-flash`（空格替换为连字符）
- 工具链：Lean 4.34.0（`leanprover/lean4:v4.34.0`，Lake 5.0.0-src），Python 3.13.3，SymPy 1.13.3；`lean --version` 与 `lake --version` 已核对
- 参考材料（只读）：`PhysD-published.pdf`（Sheng & Yu, Physica D 432 (2022) 133140，DOI 10.1016/j.physd.2021.133140）、`hirota-book-new.pdf`、`2 Huner Saxton.pdf`、`lean-toda/`（已有推导与 Lean 模块，仅作参考，不修改）
- 论文提取文本：`tmp/PhysD.txt`（0 成本局部页码的来源；PDF 页码以论文印刷页码为准）

## 研究假设（首轮约定）

1. 只离散 y；x, t 保持连续。任何对 x 或 t 的进一步离散必须单独标注层级别，不得混淆。
2. 首轮取 λ = −2（论文第 2 节第 134 行的约定），保留任意 a。其他参数约化必须在各方向报告里说明。
3. 连续系统（论文 (1)–(2)）：
   - u_yt + v_xx + u u_xy + u_x u_y + 2a u_xy = 0
   - v_t + (u v)_x + u_xxy + 2a v_x + 2λ u_x = 0
4. 变量变换（论文 (5)）：u = 2 (ln(f/g))_x，v = 2 (ln(f g))_xy。
5. 双线性系统（论文 (6)–(7)），B = D_x^2 + D_t + 2a D_x：
   - (D_y B + 2λ D_x) f·g = 0，B f·g = 0。
6. 主 Agent 已独立核对上述公式与论文提取文本一致（PhysD.txt 第 81-82、119-124 行附近）。
7. 常数背景线性化（待各方向核对）：扰动 e^{s t + i(k x + ℓ y)}，ℓ ≠ 0：
   [s + i(u_0 + 2a)k]^2 = k^4 − (v_0 + 2λ) k^3/ℓ 。
   高频增长对一般初值稳定性与收敛理论的限制必须正视，不得以隐式/守恒/有限元/辛等理由声明该障碍消失。
8. 已有交错 tau 系统（应独立审查，不视为已完成证明）：
   (B − h D_x) F_j·G_j = 0，(B + h D_x) F_j·G_{j+1} = 0，
   G_j 在 y=jh，F_j 在 y=(j+1/2)h。
   已有材料：`lean-toda/dlw_staggered_construction.md` 及其 SymPy/Lean 检验（任意 N 的依据是归约到论文行列式恒等式，未整体形式化到 Lean）。本运行中对其新颖性不做断言。

## 目录职责

- `common/`：共享数学规格与统一载体（主 Agent 维护；Sub Agent 只读复制，不直接修改后将变更交给主 Agent）
- `A_finite_difference/` … `H_toda_hierarchy/`：八个方向各自的工作目录（Sub Agent 只写自己的目录）
- `lean/`：跨方向共享的独立 Lean 项目（主 Agent 整合；也允许各方向以独立 lake 项目快速验证）
- `experiments/`、`reports/`：实验与最终报告

## 隔离规则

- 默认只读 `PhysD-published.pdf`、`hirota-book-new.pdf`、`2 Huner Saxton.pdf`、`lean-toda/`；不在其中修改或覆盖任何文件。
- Sub Agent 只写入分配给它的目录；共享模块的修改统一提交给主 Agent 整合。
- 每次重要结论必须记录结论编号、数学陈述、对象与适用范围、假设、Lean 定理名、文件位置、验证命令、构建结果、未形式化的桥接步骤、外部定理依赖、证据等级。