# 结论记录 — 方向 G（Hirota / Bäcklund / 层级离散化）

对象：交错双 tau 候选

```
(B_{a-d}) F_j · G_j     = 0 ,      s = a - d ,
(B_{a+d}) F_j · G_{j+1} = 0 ,      s = a + d ,      d = h/2 ,
B_s := D_x^2 + D_t + 2 s D_x ,
```

其中 `F_j = T_{a-d}(M(j))`，`G_j = T_0(M(j))` 为 Sheng–Yu 双 tau 族
（*Physica D* **432** (2022) 133140, eqs. (9)–(15)）在首轮 `λ = a = -2` 处的 tau 函数。

Lean 模块：`proofs/DirG.lean`（namespace `DLW.G`），
验证命令：`_lean_shared/Check-Lean.ps1 -Root ...\proofs -File ...\proofs\DirG.lean`，
构建结果：exit code `0`，`PASSED: 1 local module(s).`，无 `sorry` / `admit` / `axiom`。

---

## 结论 1 — 实验验证

**数学陈述.** 交错双 tau 候选的两个方程对显式二孤子 tau 对
`F_j = T_{a-d}(M(j))`、`G_j = T_0(M(j))` 在首轮 `λ = a = -2`、任意步长 `h` 下
**精确成立**；且该结论对 `N = 1..5` 的孤子数与多组参数均成立。

**对象与适用范围.** (2+1) 维 DLW 系统的双线性形式（论文 eqs. (6)–(7)）的
`y`-半离散化；tau 函数取论文 (9)–(15) 的 Gram/双 tau 构造。

**假设与边界条件.** 谱参数满足单孤子色散关系
`k_i^2 + w_i + 2 a k_i = 0`（`k_i = p_i+q_i`，`w_i = q_i^2 - p_i^2`）；
`p_i + q_i ≠ 0`、`p_i + q_j ≠ 0`（Cauchy 分母非零）；`h > 0` 任意。

**Lean 定理名称.** 无（本项为实验验证，非 Lean 结论）。

**文件位置.** `experiments/g6_pair_vanishing.py`（本次）、
`experiments/g5_decisive.py`（直接偏导残差）、
`experiments/g3_mode_audit.py`（`N=1..5` × 4 参数组精确有理数检查）。

**验证命令.**

```
python -u experiments/g6_pair_vanishing.py
python -u experiments/g5_decisive.py
python -u experiments/g3_mode_audit.py
```

**构建结果.** 三个脚本均正常结束（exit code `0`）；
`g6` 的 16 个 mode 对 × 20 组可容许参数 × 6 个 `δ` 值全部通过
（末尾输出 `ALL CHECKS PASSED`），两个交错残差在精确有理数下恰为 `0`；
`g3` 的 `N=1..5` × 4 参数组共 2904 个展开系数全为零。

**同时记录一个被否证的闭式.** 曾尝试的强形式
`eigen (a+δ) = (1+2δ)(k_μ − k_ν)` **为假**（`experiments/g6a_closed_form.py`
给出 `exact check: FAIL`）。正确且较弱的陈述是
`eigen (a+δ) = eigen a + 2δ(k_μ − k_ν)`，已形式化（见结论 2）。

**未形式化的桥接步骤.** 从「残差在 16 个 mode 对上为零」到
「双线性方程对 tau 函数成立」需要 Hirota 求导法则
`D_x^m e^{ξ_a}·e^{ξ_b} = (k_a−k_b)^m e^{ξ_a+ξ_b}` 的有限机械展开
（Lean 侧只保留了其代数形式 `kcoef_sub`、`wcoef_sub`，未重建完整算子）。

**外部依赖.** SymPy 1.13.3 / Python 3.13.3；论文 eqs. (6)–(15)。

**证据等级.** 强（精确有理数、穷尽 mode 对）；但**不构成**对任意 `N` 的证明。

---

## 结论 2 — Lean 代数验证

**数学陈述.** 在两条单孤子色散关系下，`B_s` 在 mode 对 `(μ,ν)` 上的特征值满足
**算子平移的精确分解**

```
eigen (a+δ) k w μ ν = eigen a k w μ ν + 2 δ (k_μ − k_ν) ,
```

即平移修正项**线性于波数差**且**与谱数据 `k_i, w_i` 无关**；
并且 DLW 特征条件精确因子化：
`k^2 + w + 2ak = 2 (p+q)(q+a)`。

**对象与适用范围.** 任意域 `K`（`[Field K]`）上的抽象代数恒等式；
与 `N` 无关，与具体 tau 系数无关。

**假设与边界条件.** 仅 `h₁ : k₁² + w₁ + 2ak₁ = 0`、`h₂ : k₂² + w₂ + 2ak₂ = 0`；
`μ, ν : Fin 2 → Fin 2`（单位立方体上的指数向量）。无其他假设。

**Lean 定理名称.**
`DLW.G.eigen_shift_split`（谱平移分解）、
`DLW.G.dispi_to_alg`（特征条件因子化）、
`DLW.G.kcoef_sub`、`DLW.G.wcoef_sub`（Hirota 法则的代数形式）、
`DLW.G.kappa_zero_of_components`（色散关系在单位立方体上的封闭性）。

**文件位置.** `proofs/DirG.lean`（第 2 节）。

**验证命令.**

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\proofs\DirG.lean' `
  -TimeoutSeconds 300
```

**构建结果.** exit code `0`；`PASSED: 1 local module(s).`；无 `sorry`/`admit`/新 `axiom`。

**未形式化的桥接步骤.** 「mode 对特征值」与「Hirota 算子作用于 tau 函数」之间的
等价（即 `D_x^m`/`D_t` 的指数分解）未在 Lean 中重建。

**外部依赖.** Mathlib（`Mathlib.Tactic`、`FieldSimp`、`Ring`、`LinearCombination`）。

**证据等级.** 强（Lean 完全形式化，任意域、任意 `N` 代数层面）。

---

## 结论 3 — Lean 结构验证

**数学陈述.** 交错系统的两个方程可归约为**一个有限的 mode 对特征值条件**，
且该归约保持双线性结构：残差
`residual s k w f g = Σ_μ Σ_ν f_μ g_ν · eigen s k w μ ν`
在 `eigen` 逐点为零时为零；两个算子的参数差为 `2d = h`。
**关键否证**：`eigen` 对 16 个 mode 对**并非逐点为零**——只有带 tau 系数的
加权和为零，因此这是一个 Cauchy 配对消去，而不是逐项消失。

**对象与适用范围.** 显式二孤子 tau 系数族 `baseCoef`、`specCoef`、`specCoefShift`
（任意域上的有理函数）；残差求和取遍单位立方体上的全部 mode 对。

**假设与边界条件.** mode 对条件以假设 `hpair` 形式引入（因为其验证在
`experiments/g6_pair_vanishing.py` 中穷尽完成，未在 Lean 中展开）；
`specCoef` / `specCoefShift` 的分母非零由 tau 构造保证。

**Lean 定理名称.**
`DLW.G.residual_eq_zero`、`DLW.G.residual`、
`DLW.G.two_soliton_eq1`、`DLW.G.two_soliton_eq2`、
`DLW.G.staggered_operators_differ`。

**文件位置.** `proofs/DirG.lean`（第 3 节）；`experiments/g6_pair_vanishing.py`
（`hpair` 的穷尽精确验证）；`experiments/g4_eigen_16cases.py`（逐点非零性的记录）。

**验证命令.** 同结论 2 的 Lean 命令，外加
`python -u experiments/g6_pair_vanishing.py`。

**构建结果.** Lean exit code `0`，`PASSED: 1 local module(s).`；
`g6` 输出 `PASS` 于两个交错残差行。

**未形式化的桥接步骤.** 把 `hpair` 从假设变成 Lean 定理需要 16 项有限情形展开；
本部署上 `fin_cases` 对复杂项替换行为不稳定，故改为在 SymPy 中以精确有理数穷尽
验证。这是**明确记录的缺口**，不是隐藏假设。

**外部依赖.** Mathlib；SymPy。

**证据等级.** Lean 结构部分强；`hpair` 部分为强实验证据。

---

## 结论 4 — Lean 分析验证

**数学陈述.** 已形式化的是**代数/离散层面**的结论；关于连续极限、实性、
非线性约束的结论**未**获得 Lean 分析层面的验证：
(a) 连续极限 `h → 0` 下交错算子对的极限为论文第二方程
`(D_y B − 4 D_x) f·g = 0`（本项为独立解析计算，非 Lean）；
(b) 实性条件 `F_j, G_j ∈ ℝ` 及零点不存在性**未被证明**；
(c) 离散约束 `w = u_y` 的类比式**未被证明**。

**对象与适用范围.** `K = ℝ` 或 `ℂ` 的实/复 tau 函数；本结论是
**否定性/边界性**的记录。

**假设与边界条件.** Lean 模块只在抽象域 `K` 上工作，未引入拓扑、
完备性或极限概念，因此**不可能**在该模块内表述连续极限。

**Lean 定理名称.** 无。这是明确的**缺口声明**。

**文件位置.** `proofs/DirG.lean` 模块文档「Not formalised here」第 3 条；
`report.md` 第 5、6 节。

**验证命令.** 不适用（无对应定理）。

**构建结果.** 不适用。**不得**把本方向标记为「连续极限已验证」或
「稳定性已验证」。

**未形式化的桥接步骤.** 全部：(i) 离散算子到连续算子的收敛；
(ii) 实性保持；(iii) 对数导数约束 `w = u_y` 的离散类比。

**外部依赖.** 无。

**证据等级.** 无形式化证据。已知的**否定性**结果：连续常背景线性化给出
`[σ + i(u₀+2a)k]² = k⁴ − (v₀+2λ)k³/ℓ`，`|Re σ| ~ k²`，
即 Hadamard 意义下不适定；显式多孤子 tau 函数**不能**建立适定性/稳定性/收敛性。

---

## 结论 5 — 数学证明，尚未完整形式化

**数学陈述.**
(a) **矩阵元平移恒等式**：矩阵元满足
`κ₊ · ρ = κ₋`，其中 `κ∓ = −(p−a∓d)/(q+a∓d)`，
`ρ = ((p−a+d)(q+a+d))/((p−a−d)(q+a−d))`。
**工作区笔记 §5 中原先陈述的形式**（把 `Q`-因子写成 `(q+a−d)` 与 `(q+a+d)`）
是**错误的**，本方向给出显式数值反例。
(b) **任意 `N` 的归约**：交错方程对任意孤子数 `N` 的成立性归约为论文的
行列式恒等式 `B_s T_s(M)·T_0(M) = 0`（论文 Lemma 2.1）。该归约是
**有效的数学归约**，但其核心依赖论文未形式化的行列式恒等式。

**对象与适用范围.**
(a) 任意域上的有理函数恒等式，加一个 `ℚ` 上的反例；
(b) 论文 (9)–(15) 的 Gram/双 tau 构造，任意 `N`。

**假设与边界条件.**
(a) `q+a−d ≠ 0`、`q+a+d ≠ 0`、`p−a−d ≠ 0`、`p−a+d ≠ 0`；
(b) 色散关系、`p_i+q_j ≠ 0`、行列式展开的收敛性（形式幂级数意义下）。

**Lean 定理名称.**
(a) `DLW.G.shifted_entry_correct`（正确形式）、
`DLW.G.claimed_entry_counterexample`（旧形式的反例，witness `(a,d,p,q) = (1,1,3,1)`，
左边 `−1/3`，右边 `−3`）。
(b) **无 Lean 定理**（归约本身未形式化）。

**文件位置.** `proofs/DirG.lean`（第 4 节）；`report.md` 第 4 节。

**验证命令.** 同结论 2 的 Lean 命令。

**构建结果.** exit code `0`；`PASSED: 1 local module(s).`；
`shifted_entry_correct` 与 `claimed_entry_counterexample` 均无 `sorry`。

**未形式化的桥接步骤.** (b) 的整条链：mode 对条件 ⟹ 有限 `N` 行列式恒等式
⟹ 任意 `N` 的递推/归纳。论文 Lemma 2.1 本身未形式化。

**外部依赖.** Sheng–Yu, *Physica D* **432** (2022) 133140,
DOI `10.1016/j.physd.2021.133140`, Lemma 2.1 与 eqs. (9)–(15)。

**证据等级.** (a) 强（Lean 形式化 + 显式反例）；
(b) 中（有效的数学归约，但依赖未形式化的外部定理，且**未**做文献新颖性检索，
故本方向**不主张**任何新颖性）。

---

## 路线状态与证明覆盖度（汇总）

| 项目 | 状态 |
|---|---|
| 交错候选是否被否证 | **否**。两个方程对显式二孤子 tau 对精确成立 |
| Lean 模块构建 | **通过**，exit 0，`PASSED: 1 local module(s).`，无 `sorry`/`admit`/`axiom` |
| 任意 `N` | **未证明**（归约到论文 Lemma 2.1，未形式化） |
| 逐点 mode 对特征值为零 | **假**。只有加权和为零（Cauchy 配对消去） |
| 连续极限 | 解析上已核对（`h²` 阶），**未**形式化 |
| 实性 / 无零点 / `w = u_y` | **未证明**（结论 4 缺口） |
| 文献新颖性 | **未检索**，不主张 |
