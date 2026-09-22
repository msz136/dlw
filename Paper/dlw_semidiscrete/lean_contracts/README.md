# DLW Lean 命题接口与验收

2026-09-22。用户已授权在原冻结接口基础上继续实现证明，并整合数值分析与系统转换。

- 人读入口：根目录 `lean_verification.html`，独立于原两份 HTML。
- 命题源：`Contracts.lean`。`def C01 : Prop := ...` 定义一个目标，**不是该目标的证明**。
- C01–C25 为数学命题；N01–N07 为数值方法验收的基础命题。
- 数值四项复审修复已运行验收；见 `../numerics/REPORT.md`。形式化证据与数值证据分开记录。
- **类型检查状态：PASSED（2026-09-22 更新）。** 两处障碍已排除，详见下方「进度更新」。冻结后的 `Contracts.lean` SHA-256 = `e70876c538d52939b030e7813a6b1c60917a79e56e28b29146d22df8da98d656`。
- 起始/最终命题**一字未改**：C01–C25 / N01–N07 的陈述原样保留，未削弱、未加假设、未重述。唯一的接口差异是 `PowBound` 里 `0<|h|` → `0 < |h|` 的**纯空白修正**（见下）。

## 当前进度（2026-09-22：32 / 32）

**已证明 32 / 32**，由标准入口 `_lean_shared/Check-Lean.ps1` 在整合模块 `Main.lean` 上一次性 PASSED：

```
& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs' `
  -File 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\Main.lean' -TimeoutSeconds 1200
→ PASSED: 39 local module(s).   退出码 0   (run 20260922_221626_2fd722e0)
```

证明根 `Workspaces\lean_contracts\proofs\`：

| 包 | 目标 | 说明 |
|---|---|---|
| `PkgContinuous.lean` | C01 | 含一条 Mathlib 原本缺失的混合偏导交换引理，由 `ContDiffAt.isSymmSndFDerivAt` 搭出 |
| `PkgGramEntry.lean` | C04, C05, C06, C10 | 矩阵元参数移位、提升到任意 N、x/t 导数、两孤子相互作用系数 |
| `PkgQuotientRate.lean` | C13, C12, C24 | Hirota 商恒等式、对数速率二阶误差（显式常数）、插值与整数格点一致 |
| `PkgTrivial.lean` | C03, C21, N02–N07 | 模板偏移、平均模态见证、数值基础引理 |
| `PkgC11.lean` | C11 | 固定物理 y 的两壁一致性；两个合取项共用同一次二阶 Taylor 展开 |
| `PkgNonlinear.lean` | C14, C15 | 双线性残差 → 物理残差的精确恒等式；`SemiPair ⇒ NonlinearPair` |
| `PkgC02.lean` | C02 | λ=−2 连续 DLW；乘子只有 ±1（`c1=2∂ₓ∂ᵧR`、`c2=2∂ₓ∂ᵧR−2∂ₓS`） |
| `PkgNumeric.lean` / `PkgRK4Complete.lean` | N01 | Euler、非线性含时间依赖 RK4、梯形缺陷阶完整证明；`n01_proved : N01` |

新增已验收包：

| 包 | 目标 | 说明 |
|---|---|---|
| `PkgC17.lean` | C17 | 真实采样恒等式与物理观测点态二阶一致性 |
| `PkgC09Complete.lean` | C09 | 任意 N Gram 的正性、合法性、联合光滑性 |
| `PkgGramBridges.lean` / `Main.lean` | 条件桥 | 保留条件桥；现在 PkgGramComplete 已接入真实 C07，导出 C08/C16 完整目标 |
| `PkgRK4.lean` | N01 辅助 | 乘积 jet、复合导数、线性 RHS 精确 RK4 多项式；一般非线性部分已由 PkgRK4Complete 闭合 |

新增 `PkgC18Complete.lean` 完成 C18：N1 在 y−h/2、N2 在 y 处的真实非线性算子二阶一致性。

整体保证的边界及接口外任务见 [INTEGRATION_STATUS.md](INTEGRATION_STATUS.md)。
页面构建器会核对成功整合运行的全依赖源码哈希、目标类型和公理输出，拒绝用旧日志为已修改源码显示绿灯。


新增 `PkgC22Complete.lean`、`PkgC23Complete.lean`：一致二阶极限和连续 Gram 起点均已闭合。关键中间结论、对应模块和适用范围见 [C22_C23_PROOF_NOTES.md](C22_C23_PROOF_NOTES.md)。

逐目标 `#print axioms` 只报 `propext / Classical.choice / Quot.sound`，**无 `sorryAx`、无新增公理**。

**冻结的 32 项全部已证明**，没有剩余未证明目标。C22 完成任意固定物理盒上一致二阶极限；C23 完成连续 Gram 的两条双线性方程。`PkgC07Complete.lean` 已证明任意 N 双线性链；`PkgGramComplete.lean` 已按冻结原始假设导出 C08/C16。

**C02 的两条更正（沿用旧记录的读者请注意）**：旧的第二条标量假设 `E2 = β_y(S_xx+(D_x)²+D_t+2a·D_x)+2B_x` **是错的**——`β_y` 把 (x,t) 上的对象和 (x,y,t) 上的对象混在一起了。正确形式（`PkgC02.lean` docstring 里逐字给出）是 `E2 = (A_y−B_y)·R + S`。精确恒等式为 `cdybil − 4·chx = sy(cbil a f g) − 2·(cbil a f (sy g) + 2·chx)`，因此 `E+2Bₓ=0` 是从 `ContinuousPair` 的第一条假设**推出来的**，不是额外假设。

**C07 一族的原因已单独查清**：`Workspaces\lean_contracts\audit_c07.py` 用 `fractions.Fraction`（无浮点、无单点判零）在 N=1..4、j=0..2、n=0..2、三组参数上，把 `bil(τ_{n+1}, τ_n)` 按**实际指数向量** `(Λ_S+Λ_T, M_S+M_T)` 合并后逐组检查，全部合并系数精确为 `Fraction(0)`。**这些有限样例通过，但不构成任意 N 命题的证明**。完整证明现已完成：行列式微分、秩一/秩二更新、Plücker 恒等式和特征多项式有限根给出的连续延拓，解除可逆性限制后接回实际矩阵元。

### 两处障碍及处置（需接口负责人复核）

1. **`_lean_shared/runtime.json` 迁移遗留**：`workspace` 与 10 条 `lean_paths` 原指向迁移前 `C:\Users\msz\学术内容`，入口在进入 Lean 编译前即返回 1（`Root must be a dedicated subdirectory ...`）。已**只改路径**重指向 `C:\Users\msz\aca`；原文备份 `_lean_shared/runtime.json.bak_pre_aca_migration`。未改工具链、Mathlib 提交或任何证明语义。
2. **`Contracts.lean` 词法缺陷**：`PowBound` 中 `0<|h|` 被 Lean 词法器读成 `<|` 管道算子，报 `Function expected at 0` 与 `unexpected token '|'; expected command`（第 153 行），文件根本无法类型检查。已提交**最小词法差异** `0 < |h|`（仅一个空格，数学内容不变）。原字节备份 `Trash\lean_contracts_pre_syntax_fix_20260922\Contracts.lean.orig`，SHA-256 `40a624c24046bf0b91436fca15feafeef67ccecbf15a23d6b1145dc2a2bc16ac`。

## 统一语义

函数参数顺序：`XT` 是 x,t；`XYT` 是 x,y,t；`Lattice` 是 j,x,t，j∈ℤ。
导数为 Mathlib `deriv`，不是无解释的 jet 数字；`SmoothXT/Smooth3` 使用冻结的 `ContDiff ℝ ⊤`。当前 Mathlib 的阶数类型为 ℕ∞ω，⊤ 表示解析阶 ω，强于通常的 C∞；此前仅称 C∞ 不准确，不能据此扩大已证结论的适用范围。冻结文件保持不变。
首轮非线性化覆盖全局光滑正实 τ，是一般非零局部 τ 结论的明确子范围。
Gram 层使用真实 `Matrix.det (I + K)`；j,n 为整数，`Admissible/LayerOK` 排除负幂的零基底和全部相关分母。
`sampleF/sampleG` 固定交错位置；C11/C18 在固定物理 y 附近取极限，C22 为紧盒上一致界。

## 给证明 Agent 的共同指令

1. 先读根 AGENTS.md、此文件、专题 HTML 与权威数学报告；按依赖图领取一个包。
2. 不改 Contracts.lean，不引入新数学公理，不把关键结论当作假设，不把 ℝ/任意 N/实际导数降为有限有理样例。
3. 在自己的 `Workspaces/lean_<任务>/proofs/` 中写证明，不改共享环境、`lean-toda` 或其他 Agent 的目录。本轮未创建这些 Agent 或证明目录。
4. 初次类型检查如需修正接口，提交最小接口差异，标明是否改变数学语义；由接口负责人审查后统一冻结新哈希。数学上不成立的目标应给反例，不强行证明。
5. 证明导出形状是 `theorem c15_proved : DLWContract.C15 := <完整证明项>`。这里尖括号只是 README 的说明，不是交付代码；交付文件必须有完整证明。一个命题可以由多个辅助引理完成。
6. 各 Agent 使用相同字节的 Contracts.lean 快照；最终整合必须导入单一权威模块。复制代码片段后改定义再同名证明，不予验收。
7. 标准验证入口示例（先由环境维护者处理迁移）：

```powershell
& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\aca\Workspaces\lean_<任务>\proofs' `
  -File 'C:\Users\msz\aca\Workspaces\lean_<任务>\proofs\Main.lean'
```

`Root` 内放统一 Contracts.lean 快照及证明模块，不把整个项目作为 Root。不得自行新建 Lake 工程或重装环境。

## 每个包必须交付的证据

- 目标编号、导出的定理名、完整 theorem type、定义版本 SHA-256。
- 输入假设的逐条数学解释；依赖定理列表；适用域、未覆盖边界。
- 标准入口返回 0 且 PASSED 的 result.json/build.log；完整本地依赖的源码哈希。
- 对每个导出定理输出 `#print axioms`，只允许标准逻辑依赖 `propext/Classical.choice/Quot.sound` 的子集；不能仅依赖编译器退出码。
- 至少核验一个允许的非退化参数族；C09 可用 a=4,p=1,q=2,rho=3,h=1/4 的 N=1 数据。这是排查空假设，不代替任意参数定理。
- 对不应成立的加强版写出明确拒绝理由：任意连续解采样不自动成为有限 h 精确解；有限 N 扫描不证明任意 N；点值 O(h²) 不自动给紧集一致界；一致性不等于稳定收敛。

## 派工与依赖

| 包 | 目标 | 前置 | 交付边界 |
|---|---|---|---|
| A 语义与连续层 | C01,C02,C03,C23 | 共享定义类型检查 | 连续方程真实导数与变量变换；不声称唯一离散化 |
| B Gram 精确性 | C04–C10 | 共享定义；C06→C07→C08 | 任意 N 完整行列式，不留 Reservoir 假设；C09 单独证明正则性 |
| C 分析与极限 | C11,C12,C17,C18,C22,C24 | A；C09；C24→C22 | 真正余项界、固定物理位置；紧集界及导数控制 |
| D 非线性桥 | C13–C16,C19–C21,C25 | C13→C14→C15；C08,C09→C16 | 先残差恒等式后解映射；周期求和不推出平均模态演化 |
| E 数值方法基础 | N01–N07 | 共享有限维语义；D 的边界说明 | 只验有限维算法/误差组合；不能以这些基础定理宣称已完成 DLW 求解器 |
| F 集成验收 | 各包导出定理与实验专属证书 | A–E 按需 | 复跑、核对目标、实例化实际网格/边界/步长、数据证书；状态表只按证据更新 |

## 尚需单独设计接口的扩展

这些项目在专题里明确标为“接口待定”，没有冒充已具备 Lean 命题：局部开链反向 τ 重构与积分规范、完整复谱 Darboux/波函数、渐近相移的实际峰位对应、线性化到 Fourier 模态的桥接和色散关系、全局边界通量积分、指定 x 算子与边界闭合的截断界、指定求解器的稳定常数与非线性迭代误差、经认证的 Gram/exp/log 数值区间。

N01 的阶数是**一步缺陷阶**（Euler 2、RK4 5、梯形残差 3）。全局时间阶 1/4/2 还需在实际有限维初边值模型上证明一步稳定性、统一局部缺陷并实例化 N02；正增长支的常数可以随空间分辨率恶化。N04 不自动验证 Python/NumPy，它只在真值区间已经证明时给有限样本误差界。

## 页面与记录维护

运行 `build_dashboard.py` 更新专题源、证据清单和根 `lean_verification.html`。它读取旧验证日志并核对源码哈希，**不会运行 Lean，不会把 def : Prop 标为证明**。旧日志的 PASSED 只支持其原始 theorem type。
本轮原 `index.html`、`numerical_analysis.html` 及其权威源保持不变；仅增加专题，并在 AGENTS.md 加入口。
