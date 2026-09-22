# VERIFY.md — 方向 D（守恒差分 / SBP）验证记录

所有命令均在 `C:\Users\msz\学术内容` 下执行。以下记录为**实际执行**的命令与**实际观察**到的输出。

---

## 1. Lean 形式化验证

### 命令

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
    -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\D_conservative_sbp\proofs' `
    -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\D_conservative_sbp\proofs\DirD.lean' `
    -TimeoutSeconds 300
```

### 实际输出（逐字）

```
CHECK Common\Operators.lean
CHECK DirD.lean
'DLW.DirD.d_avg_mul' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirD.avg_sbp' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirD.avg_sbp_divided' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirD.d_skew_adjoint' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirD.d_skew_adjoint_divided' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirD.constraint_sbp_balance' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirD.constraint_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]
PASSED: 2 local module(s).
REPORT: C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\D_conservative_sbp\proofs\.lean-runs\20260918_001609_9a3b35cf\result.json
```

### 结果

* **exit code: 0**
* **`PASSED: 2 local module(s).`**
* Axiom 审计：每个 head-line 定理只依赖 `propext`、`Classical.choice`、`Quot.sound`（Mathlib 标准三件套）。
* **没有** `sorryAx`。文件中**没有** `sorry` / `admit` / 新增 `axiom`。

### 环境

* Lean 4.34.0，Mathlib v4.34.0（commit `5ed2965256430c3649e86755f9576b54eca72435`）
* 只读共享模块 `proofs/Common/Operators.lean` 被 `import Common.Operators` 使用，未修改。

### 模块清单

| 文件 | 定理数 | 状态 |
|---|---|---|
| `proofs/Common/Operators.lean` | （只读，预先 PASSED） | 未改动 |
| `proofs/DirD.lean` | 8 条定理 | PASSED |

`proofs/DirD.lean` 中的定理（全部通过）：

1. `DLW.DirD.d_avg_mul` — 对称离散乘积法则
2. `DLW.DirD.avg_sbp` — 非线性项 SBP 边界恒等式（未除形式）
3. `DLW.DirD.avg_sbp_divided` — 同上（除形式，因子 `2h`）
4. `DLW.DirD.d_skew_adjoint` — 前向差分 SBP / 反对称性
5. `DLW.DirD.d_skew_adjoint_divided` — 同上（除形式）
6. `DLW.DirD.constraint_sbp_balance` — 离散守恒律 / 精确边界平衡
7. `DLW.DirD.D_shift_comm` + `DLW.DirD.avg_shift_comm` — 位移交换性
8. `DLW.DirD.constraint_kernel` + `DLW.DirD.conserved_density_trivial_on_constants` — 守恒量无正定性

---

## 2. 实验验证（Python 3.13 + SymPy）

解释器：`C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe`（Python 3.13.3，SymPy 1.13.3）。

### 2.1 `experiments/e1_exact_identities.py`

```powershell
python -u e1_exact_identities.py
```

* **exit code: 0**
* 输出结尾：`ALL CHECKS PASSED`
* 覆盖：乘积法则 A1/A2、telescoping B1/B2、DLW 非线性通量 C1（`a = 0, 1, 3/2` 及符号 `a`）/C2、通量 telescoping D1/D2、守恒泛函符号讨论 E。

### 2.2 `experiments/e2_linear_symbol.py`

```powershell
python -u e2_linear_symbol.py
```

* **exit code: 0**
* 输出结尾（逐字）：

```
checks   : 8  failures: 0
OVERALL  : ALL CHECKS PASSED
```

* 覆盖：
  * `A0a/A0b/A0c` — 格点符号 `ν = e^{iαh/2}cos(αh/2)`，`μ − iα = O(h)`，`ν → 1`（相容性）
  * `A1a/A1b` — 格点最大模 `α = 2/h` 处 `Re σ > 0` 对每个 `h` 成立，且随 `h` 减小严格增大
  * `B1/B2/B3` — 大根引理 `Re(w²+iakw) = x²−y²−aky`、`Im = x(2y+ak)`，以及分支 `2y+ak=0` 上的约化 `x² + a²k²/4 = k⁴ + bk³`

  增长率表（`h·Re σ → |sin 2|/2 = 0.454648713412841`，故 `Re σ ~ O(1/h)`）：

  | `h` | `Re σ` | `h·Re σ` |
  |---|---|---|
  | 0.1 | 3.8342919861223663 | 0.3834291986122367 |
  | 0.05 | 5.257075962057958 | 0.26285379810289794 |
  | 0.02 | 8.154892279008452 | 0.16309784558016904 |
  | 0.01 | 11.45869599718454 | 0.1145869599718454 |
  | 0.001 | 36.02503758018004 | 0.03602503758018004 |

> **重要范围说明**：`e2` 早期草稿曾把离散 `σ²` 与主 agent 关系 V6 逐项对照并报出不一致。那些检查基于对线性化对的**错误转写**（v-项上多了一个 `μ`，且约束 `w = D u` 代入不一致），已被**删除而非修补**。`e2` 中保留的全部检查均已独立验证通过。离散格式的守恒 / 约束保持结构**不需要**色散计算——它由 Lean 证明（`DLW.DirD.constraint_sbp_balance`、`DLW.DirD.D_shift_comm`）。

---

## 3. 未通过 / 已删除的内容（诚实记录）

以下命题在开发过程中被判定为**假**并**删除**，从未以 `sorry` 蒙混：

| 名称 | 初版陈述 | 反例 | 处置 |
|---|---|---|---|
| `d_mul_left` | `D(xy)_j = (Dx)_j(y_j + avg y_j) + x_j(Dy)_j` | `x_j=1, x_{j+1}=3, y_j=2, y_{j+1}=5, h=1`：左端 `19`，右端 `10` | 删除 |
| `flux_gauge_identity` | `D(xy)_j = x_j(Dy)_j + (avg x_j)(Dy)_j + (Dx)_j(avg y_j)` | 同左：右端含多余项 `x_j(Dy)_j` | 删除 |

正确的单边形式 `D(xy)_j = x_{j+1}(Dy)_j + avg(y)_j(Dx)_j`（同一反例两端同为 `19`）在预算内未能完成 Lean 证明，故**不纳入**已证清单，仅在此记录。

**当前 `DirD.lean` 是绿的**；上述删除后的文件状态即上表 §1 所记录的状态。

---

## 4. 复现步骤（从零）

```powershell
$D = 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\D_conservative_sbp'

# 1) Lean
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' -Root "$D\proofs" -File "$D\proofs\DirD.lean" -TimeoutSeconds 300
#   期望：exit code 0 且 PASSED: 2 local module(s).

# 2) 实验
cd "$D\experiments"
python -u e1_exact_identities.py    # 期望 exit 0 + ALL CHECKS PASSED
python -u e2_linear_symbol.py       # 期望 exit 0
```

---

## 5. 已知限制

* 本方向**没有**形式化任何分析性结论（连续极限、色散关系、病态性）。这些仅有 SymPy 精确符号证据，标签为 `实验验证`。
* `constraint_sbp_balance` 是**抽象**通量-散度定理；候选方程 `(E1)` 的具体通量代入未形式化，因为 `x`、`t` 是连续变量。
* 全部守恒/稳定性主张均为**条件性**的：守恒只在边界通量为零时成立；且 D-5 证明该守恒量**不能**给出稳定性。
