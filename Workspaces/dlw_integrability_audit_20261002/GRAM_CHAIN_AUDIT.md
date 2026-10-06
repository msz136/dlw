# DLW 双线性—Gram—物理系统—连续极限证据审计

审计日期：2026-10-02。只读核对定理定义、证明调用、编译日志与当前源码 SHA-256；没有重新编译大型 Lean 工程，没有修改研究源码、根报告或进度索引。

## 1. 可直接采用的结论

DLW 已完成一条严格的前向构造链：连续 Gram 起点、指定交错双线性离散化、任意有限 N 的精确行列式解、正参数区间下无零点的物理场、SD 与 SDR 两路非线性表示，以及实际精确解族在固定物理紧盒中的一致二阶连续极限。任意 N 的结论已经具有无 Reservoir 前提、无矩阵可逆性前提的 Lean 证明，不能再把它降格为有限 N 数值检验。

这条链尚不能作为一般初值的 IST、任意非线性解的全局反向 τ 重构、周期全局等价、完整谱理论或全离散求解器可积性的证明。具体 Lax／Darboux 证据需与专门谱审计合并；本文不从 Gram 解族独自推出它们，也不判定全系统不可积。

## 2. 对象、参数与假设

冻结定义见 `Workspaces/lean_contracts/proofs/Contracts.lean`：

- `ContinuousPair`（43 行）是 `B_a f·g=0` 与 `D_y B_a f·g−4D_x f·g=0`。第二式不是 `B_a f·g_y−4D_x f·g=0`。
- `SemiPair`（45 行）是同一个 F 同时满足 `B_(a−h/2) F_j·G_j=0`、`B_(a+h/2) F_j·G_(j+1)=0`。
- `entry`、`tau`（109、113 行）是真实 `det(I+K)`，包含单位矩阵项；层数 n 和格点 j 为整数，空间／时间使用真实 `Real.exp` 与 `deriv`。
- `F=τ_1(a−h/2)`、`G=τ_0(a)`。τ_0 与辅助参数无关。构造只含 x,t,j，没有随辅助参数 s 变化的额外连续 y 相位。
- `PositiveData`（106 行）为 `h>0`、p/q 严格递增，且每个 `0<p_i<a−h/2`、`q_i>0`、`rho_i>0`。这是正实无奇点解族的充分条件；没有覆盖一般复谱、breather 或退化有理极限。
- `SmoothXT`、`Smooth3`（30、31 行）的裸 `ContDiff ℝ ⊤` 在当前 Mathlib 的 `ℕ∞ω` 类型中是解析阶 ω。普遍 τ→物理场端点的已验收范围强于普通 C∞，不能改写为已经形式化了任意局部非零或复对数分支版本。

物理变换固定为

\[
u_j=\partial_x\log\frac{F_j^2}{G_jG_{j+1}},\qquad
v_j=\frac4h\partial_x\log\frac{G_{j+1}}{G_j}+\delta_0u_j.
\]

F 及物理 u/v 位于 `(j+1/2)h`，G 位于 `jh`。连续系统系数固定为原文的 λ=−2。

## 3. 核心端点逐项核对

| 步骤 | 真实已证明的类型／结论 | 证据 | 范围和限制 |
|---|---|---|---|
| 参数—格点恒等式 | 任意 N,n,j 的真实矩阵元及行列式满足 `τ_n(j;a−h/2)=τ_n(j+n;a+h/2)` | C04/C05；`PkgGramEntry.lean`；Contracts 119–127 行 | `Admissible`；整数负幂所需非零条件保留 |
| 固定参数的任意 N 双线性链 | `bil s (tau(n+1)) (tau n)=0` | C07；`PkgC07Complete.lean:9`；Contracts 134 行 | 任意有限 N、整数 n,j、所有实 x,t；只假设 Admissible+LayerOK；不假设双线性方程成立 |
| 两壁精确半离散方程 | 同一 F/G 满足 SemiPair | C08；`PkgGramComplete.lean:7`；`PkgGramBridges.lean` | 真正接入 `c07_proved`，并非只保留 `c08_of_c07` 条件桥 |
| 全域正性／光滑性 | Admissible、F/G>0、SmoothL F/G | C09；`PkgC09Complete.lean:725` | 任意 N，所有整数 j、所有实 x,t；假设 PositiveData |
| 精确残差桥 | 无方程成立前提下，将 n1/n2 写为归一化双线性残差 A,C 的差分／导数 | C14；`PkgNonlinear.lean:1282`；Contracts 174 行 | 防止把所需结论塞入前提；正实解析 F/G、h≠0 |
| 双线性→物理非线性 | SemiPair 推出 physU/physV 满足 NonlinearPair | C15；`PkgNonlinear.lean:1336`；Contracts 182 行 | 单向前向映射 |
| 实际 Gram→物理非线性 | `PositiveData → NonlinearPair` | C16；`PkgGramComplete.lean:9`；Contracts 185 行 | 只剩 PositiveData；没有假设 N1/N2、SemiPair 或 C07 的前提 |
| 连续 Gram→连续双线性 | 实际 tau0 的 n=1,0 满足 ContinuousPair | C23；`PkgC23Complete.lean:75`；Contracts 236 行 | 任意 N，固定 PositiveData；没有调用原论文事实作为公理 |
| 连续双线性→连续物理 DLW | ContinuousPair 推出 c1=c2=0 | C01/C02；`PkgContinuous.lean`、`PkgC02.lean` | 正 τ、真实混合偏导，λ=−2；连续 τ 正性也可由 extF/extG 正性及 extension_zero 接入 |

### C07 消除可逆性限制的实际结构

`PkgC07Complete` 把实际指数矩阵的 x/t 导数、层更新、秩一因子接到 `GramDeterminant.bil_det_of_jets`。该引理在 `PkgGramHirota.lean:33` 使用真实行列式导数；其代数核心 `matrix_hirota` 不假设 A 可逆。

中间秩二更新在可逆矩阵上计算，但最终 `PkgGramIdentity.lean:48` 的 `plucker_identity` 通过 `continuous_identity_of_invertible` 延拓到所有矩阵。`PkgGramDeterminant.lean:93` 使用特征多项式有限根证明 `A+zI` 在 z→0 时最终可逆。因而 τ 为零的点仍满足双线性恒等式；物理对数变换则由 C09 正性另行保证合法。

## 4. SD 与 SDR 两路非线性化

项目命名对应见 `Workspaces/dlw_factor_model_20260930/REPORT.md:24`：SD 是 Report 式（7）／（8）的消势两场形式；SDR 即数值代码 SD2，是式（21）／（22）的 Q/R/M 形式。它们来自同一个有限 h 双线性系统。将 x,t 再离散后，差分乘积规则和时间换元会产生额外误差，不能把两条实际算法判为逐步等价。

`ReportEndpoints.lean` 的定理为：

- `bilinear_to_report7`（48 行）：正实解析 F/G、h≠0、SemiPair → 式（7）的 u/未缩放 ω 系统。
- `bilinear_to_report21_22`（54 行）：同样起点 → 式（21）的 Q/R 两演化式和 M 格点约束，连同式（22）的全部物理重构身份。
- `bilinear_to_both`（61 行）：上述两路及中心正平方根比值 `Q=F/sqrt(G_j G_(j+1))` 一起推出。

其中 `ω=(log G_(j+1)−log G_j)_x`，`Q=exp(log F−(log G_j+log G_(j+1))/2)`，`M=(log G)_x`，`R=(1−ω/h)/Q`。R 可以为零或变号；证明 R 方程只取消始终正的 Q。

SDR 的 Q 方程由 `residualQ=Q(A+C)/2` 直接使用双线性信息取得。它没有从 `∂x(某式)=0` 随意抹掉积分常数。R 方程使用 `residualProduct=R·residualQ+Q·residualR` 及 ω 方程。

ReportEndpoints 没有另加一个名为“Gram→SD/SDR”的集成定理；但 C08+C09 已提供其全部前提，故两路端点都可直接实例化于任意 N 正实 Gram 家族。这里的“物理重构”是从已定义 Q/R/M 恢复由同一 τ 产生的 u/v；不是从任意 u/v 解反向构造 τ 的定理。

## 5. 连续极限的四层证据不可混淆

| 层次 | 已证明 | 边界 |
|---|---|---|
| 格点相位速率 | C12：`log λ_h(P)/h−1/P=O(h²)` | P≠0 的局部速率；单独不足以得到物理场收敛 |
| 物理位置与变换 | C17：采样物理场与插值表达式严格对应，interpU/V 对连续 cu/cv 二阶一致；C24：实际 Gram tauI 精确采样回 F/G | F offset=1/2、G offset=0；须保留 γ 的步长依赖 |
| 方程一致性 | C11：两壁半和／除 h 的差均 O(h²)；C18：非线性 N1 在 y−h/2、N2 在 y 的连续残差 O(h²) | 这是方程残差／光滑采样结论 |
| 实际精确解族收敛 | C22：实际 Gram 插值的 u/v 对连续 Gram 物理场 `UniformBoxO2` | 固定数据 D,N 与 h0，任意固定有界 x,y,t 盒；不是一般初值求解器收敛 |

C22 的量词为：对每个 R>0，存在 C≥0、ε>0，使 `0<h<ε` 且 `|x|,|y|,|t|≤R` 时，两场误差分别 ≤Ch²。C 和 ε 可以依赖 D、N、h0、R，不依赖趋零 h；没有对 N 或整个无限时空一致的结论。

实际证明 `PkgC22Complete.lean:83` 将冻结 tauI 接到偶解析延拓。u 误差的一阶导数为零；v 的带 h 分子是奇函数，减去 h·cv 后零、一、二阶 jet 为零。`PkgCenteredUniform.lean` 利用盒紧性取得共同步长和统一导数界，先得到 u 的 O(h²)、h·v 的 O(h³)，再除 h 得 v 的 O(h²)。这确实控制求导后的物理场，强于仅在某个点取相位极限。

## 6. 编译与当前源码证据

本次重新计算 SHA-256，与既有成功 run 的每个记录逐项比较：

| 入口 | 既有成功 run | 当前源码核对 | 公理足迹 |
|---|---|---|---|
| `Main.lean` | `20260922_221626_2fd722e0`，PASSED，39 本地模块 | 39/39 一致，0 个 hash mismatch | C07/C08/C09/C16/C22/C23 等冻结端点仅 propext/Classical.choice/Quot.sound |
| `ReportEndpoints.lean` | `20261002_120733_d51ae3c5`，PASSED，9 本地模块 | 9/9 一致，0 个 hash mismatch | 四个合并端点均仅上述标准三公理 |

完整记录：

- `Workspaces/lean_contracts/proofs/.lean-runs/20260922_221626_2fd722e0/result.json`、`build.log`；日志 C07/C08/C16/C23/C22 依赖查询在 642–659 行。
- `Workspaces/lean_contracts/proofs/.lean-runs/20261002_120733_d51ae3c5/result.json`、`build.log`；四个 ReportEndpoints 依赖查询在 168–171 行。
- `Paper/dlw_semidiscrete/lean_contracts/status.json`：32 已证／0 未证是冻结 C01–C25、N01–N07 的完成率，不是所有 DLW 可积性研究任务的完成率。
- `Paper/dlw_semidiscrete/lean_contracts/INTEGRATION_STATUS.md` 与 `C22_C23_PROOF_NOTES.md` 的当前摘要与上述类型吻合。

`Contracts.lean` 本身只定义命题，导入成功不构成证明。旧 `c08_of_c07`、`c16_of_c07` 条件桥仍可用；最终 `c08_proved`、`c16_proved` 已接真正证明，不能据辅助条件桥的存在说核心未完成。

## 7. 反向链路与旧文档的正确读法

`NONLINEAR_CLOSURE.md:201`（§5）给出局部开链／无限格点的反向积分与规范修正推导：递推 β_x、恢复 α_x、共同规范消去 j 独立残差，再以时间函数消去剩余 A/C。这是明确的数学构造路线；它没有在当前冻结 Lean 接口中形成反向定理。周期格点、周期 x、指定衰减边界仍需要整体相容条件，不能提升为全域同边界的双向等价或唯一重构。

`GRAM_INTEGRABILITY_REASSESSMENT.md` 的手工任意 N 证明与 200 组双线性、54 组直接非线性精确检查是较早证据。当前任意 N 的主证据是 C07/C08/C16 的真实 Lean 终点，而非有限参数扫描。文首和末尾的谱未完成说明需结合后续 `S_INTEGRABILITY_STATUS.md`／专门谱审计解读，不能停留在 9 月 19 日边界。

旧混合构造添加了随 s 变化的连续 y 相位，F/G 层不共享同一指数；其反例不能否定只含 x,t,j 的冻结纯格点 Gram 构造。旧无谱矩阵的 `zf_all` 只证明所选无谱模型的属性，不能排除其他谱表示。

## 8. 与 2HS 方法步骤的对应（DLW 一侧）

| 2HS 方法步骤所要求的结构 | DLW 当前对应状态 |
|---|---|
| 用 τ／行列式表达连续解并接到原连续物理系统 | 已完成：C23+C01+C02；正实参数家族，λ=−2 |
| 将双线性结构离散化并保留精确行列式解 | 已完成：指定两壁模板，C03–C08；任意有限 N、整数层／格点 |
| 非线性化后保留两物理分量 | 已完成：C13–C16；两路 SD/SDR 正向端点及全部物理恢复 |
| 无奇点参数范围与实际连续极限 | 已完成：C09、C17、C22、C24；固定正则解族紧盒一致二阶 |
| 用 Lax 相容性证明完整模型的可积结构 | 本审计的 Gram／物理端点不证明这一项；需引入专门谱审计并核对“相容性覆盖整个物理系统”的范围 |
| 一般初值反演、IST、全局反向 τ 等价 | 当前冻结端点未证明；不能用任意 N 孤子家族代替 |
| 实际全离散算法、动网格和精度保证 | 不由上述结构自动推出；必须分别检验差分、时间推进、边界、误差传播与网格规则 |

