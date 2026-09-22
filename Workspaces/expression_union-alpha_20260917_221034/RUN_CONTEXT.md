# RUN_CONTEXT — Union Alpha 主 Agent 运行记录

- 运行目录：`expression_union-alpha_20260917_221034`
- 开始时间：2026-09-17 22:10（本地）
- 主 Agent 模型：Union Alpha（用户系统提示中给出的代号；maker 匿名，无正式模型名。slug 采用 `union-alpha`；运行开始时无法确认正式产品名，故额外注明）
- 工具链：Lean 4.34.0（leanprover/lean4:v4.34.0，Lake 5.0.0-src）；Python 3.13.3；SymPy 1.13.3 可用、pypdf 6.9.1 可用；pymupdf 不可用
- 工作根：`C:\Users\msz\学术内容`
- 参考材料（只读）：`PhysD-published.pdf`、`hirota-book-new.pdf`（文本层不可提取，使用 `_hirota_pages\` 图像）、`2 Huner Saxton.pdf`、`lean-toda/`
- 论文提取文本：`tmp\PhysD.txt`（Sheng & Yu, Physica D 432 (2022) 133140，DOI 10.1016/j.physd.2021.133140）
- 无适用的 AGENTS.md（已检查工作根、祖先目录、lean-toda；见主 Agent 探索记录）

## 研究假设（主 Agent 已核对）

1. 只离散 y；x、t 保持连续。若实验需要进一步离散 x/t，必须单独标注层级，不与半离散结论混淆。
2. 首轮 λ = −2（论文后续使用），保留任意 a。其他参数约化必须说明。
3. 连续系统（论文 (1)-(2)）：
   - u_yt + v_xx + u u_xy + u_x u_y + 2a u_xy = 0
   - v_t + (u v)_x + u_xxy + 2a v_x + 2λ u_x = 0
4. 变量变换（论文 (5)）：u = 2 (ln(f/g))_x，v = 2 (ln(f g))_xy。
5. 双线性系统（论文 (6)-(7)），B = D_x² + D_t + 2a D_x：
   - B f·g = 0
   - (D_y B + 2λ D_x) f·g = 0
6. 非线性改写（用户材料）：w = u_y，
   - w_t + ∂_x[v_x + (u+2a)w] = 0
   - v_t + ∂_x[(u+2a)v + w_x + 2λ u] = 0
   - 沿 y 离散时，w = u_y 的核空间、均值条件与恢复 u 的方式是核心问题。
7. 常数背景线性化（待各方向核对，不得直接采信）：扰动 e^{st+i(kx+ℓy)}、ℓ≠0，
   [s + i(u_0+2a)k]² = k⁴ − (v_0+2λ)k³/ℓ。高频增长必须正视，不得以隐式/守恒/有限元/辛为由声称消失。
8. 已有交错 tau 系统（独立审查，不视为已完成 Lean 证明，不主张新颖性）：
   (B−hD_x)F_j·G_j = 0，(B+hD_x)F_j·G_{j+1} = 0；G_j 在 y=jh，F_j 在 y=(j+1/2)h。
   参考材料：`lean-toda/dlw_staggered_construction.md`；任意 N 的依据是归约到论文行列式恒等式，未整体形式化。

## 与 lean-toda 既有材料的关系

- `lean-toda` 只读参考；本次验证全部在 `expression_union-alpha_20260917_221034\lean\` 独立 Lake 项目中复现（主 Agent 已在 lean-toda 执行过一次 `lake build TodaFormalization` 以确认基线可编译，注意该操作更新了其 `.lake` 构建缓存但未改动任何源文件）。
- 既有 Lean 结论的覆盖范围（主 Agent 已逐行审查）：
  - `DLWStaggered.shifted_matrix_entry`：参数移位恒等式（特征零域，一般参数）→ G 方向的结构证据。
  - `centered_equivalence` / `centered_mean_coefficients` / `centered_difference_coefficients`：形式 Taylor 系数层面，非带余项相容性。
  - `DLWOneSoliton.lean`：完整残差展开（单指数），覆盖一孤子；未覆盖双孤子。
  - `DLWSemidiscrete.lean`：中心差分候选的形式二阶相容 + Cayley 色散；含"连续双孤子相互作用系数不可保留"的精确反例。

## 目录职责与隔离规则

- `common/`：共享数学规格与统一载体约定（主 Agent 维护；Sub Agent 只读复制）
- `A_finite_difference/` … `H_toda_hierarchy/`：八个方向工作目录；Sub Agent 只写自己的目录
- `lean/`：主 Agent 维护的独立共享 Lake 项目（DLWCommon + 各方向模块）；各方向可在自己目录内建独立 lake 项目快速迭代
- `experiments/`、`reports/`：实验与报告
- 不修改其他模型目录（`expression_deepseek-v4-flash_20260917_220258` 保持只读）
- 不覆盖根目录下任何既有文件

## Lean 验证规范（全项目强制）

1. 定理给出明确对象、参数、网格、边界与非零条件。
2. 禁止 `sorry`/`admit`/新增结论性公理/暗中假设待证结论。
3. 已知数学定理可作为显式假设做条件证明，但必须醒目标注，不计作无条件完成。
4. 区分形式导数数据（Jet 代数）与真实函数微积分。
5. 区分有限样本验证与一般参数定理。
6. 区分 Taylor 系数恒等式与带余项相容性。
7. 区分半离散守恒与全离散守恒。
8. 区分线性化稳定、有限频带稳定、一般非线性稳定。
9. 记录自动化工具依赖（grind/simp 等），检查关键定理公理依赖。
10. 假设审计：排除矛盾假设、空参数域、零空间退化导致的空洞成功。

## 并发与 Sub Agent 记录

- 环境支持 Task 工具（subagent_type=general/explore），八条路线分批并行执行；每批 2–4 个并发槽位。
- 每条路线交付：`report.md`、Lean 模块（在共享 lean/ 项目内由主 Agent 集成编译）、实验脚本、结论清单（按统一格式）。
- 主 Agent 独立复核：线性谱公式、tau→连续极限、约束闭合、Lean 假设审计。
