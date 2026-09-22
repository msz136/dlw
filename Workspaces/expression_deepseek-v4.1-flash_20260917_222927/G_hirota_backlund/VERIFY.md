# VERIFY — 方向 G（Hirota / Bäcklund / 层级离散化）

所有命令在 `C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\`
下执行。下方 **exit code** 与 **PASSED/FAIL 行** 均为实际观测值。

Python：`C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe`（3.13.3, SymPy 1.13.3）

---

## 1. Lean 模块（主要交付物）

### 命令

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\proofs\DirG.lean' `
  -TimeoutSeconds 300
```

### 实际输出

```
CHECK DirG.lean
PASSED: 1 local module(s).
REPORT: ...\proofs\.lean-runs\20260918_004924_24b8fe42\result.json
```

### 结果

* **exit code: `0`**
* **`PASSED: 1 local module(s).`**
* 无 `sorry`、无 `admit`、无新增 `axiom`（checker 对占位符会输出
  `PROOF_PLACEHOLDER_REJECTED`，本次未出现）

### `DirG.lean` 中已形式化的定理（全部无占位符）

| 定理 | 内容 |
|---|---|
| `DLW.G.dispi_to_alg` | DLW 特征条件精确因子化：`(p+q)^2+(q^2-p^2)+2a(p+q) = 2·dispi`，`dispi = (p+q)(q+a)` |
| `DLW.G.kappa_zero_of_components` | 色散关系在单位立方体（`Fin 2 → Fin 2`）上封闭 |
| `DLW.G.kcoef_sub` | Hirota 法则的代数形式：`k_μ − k_ν = k₁Δ₀ + k₂Δ₁` |
| `DLW.G.wcoef_sub` | 同上，对 `w` |
| `DLW.G.eigen_shift_split` | **算子平移的精确分解**：`eigen (a+δ) = eigen a + 2δ(k_μ − k_ν)`（任意域、任意 `N`） |
| `DLW.G.residual_eq_zero` | 残差逐 mode 消去 |
| `DLW.G.two_soliton_eq1` | 第一交错方程 → 有限 mode 对条件 |
| `DLW.G.two_soliton_eq2` | 第二交错方程 → 同一有限 mode 对条件 |
| `DLW.G.staggered_operators_differ` | `(a+d) − (a−d) = 2d = h` |
| `DLW.G.shifted_entry_correct` | **正确的**矩阵元平移恒等式 `κ₊·ρ = κ₋` |
| `DLW.G.claimed_entry_counterexample` | 旧形式（笔记 §5）在 `(a,d,p,q)=(1,1,3,1)` 处为假的显式反例 |

---

## 2. 实验脚本

### 2.1 `experiments/g6_pair_vanishing.py` — 交错残差的精确穷尽验证

```powershell
cd experiments
& 'C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe' -u g6_pair_vanishing.py
```

**exit code: `0`**。实际输出（尾部）：

```
PASS  eigen (a+delta) = eigen a + 2 delta (k_mu-k_nu): 20 data sets x 16 pairs x 6 deltas

--- symbolic: generic p_i, q_i, a, delta ---
PASS  symbolic identity eigen (a+delta) = eigen a + 2 delta (k_mu-k_nu)

--- staggered residuals for the explicit two-soliton tau pair ---
   residual (a-d) = 0
   residual (a+d) = 0
PASS  staggered residual 1 vanishes: (B_{a-d} F . G) = 0
PASS  staggered residual 2 vanishes: (B_{a+d} F . G^+) = 0

ALL CHECKS PASSED
```

**结论.** 20 组可容许参数（`a = -2`，`d = 1/10`）× 16 个 mode 对：
两个交错残差在**精确有理数**下恰为 `0`；算子平移分解在符号层面亦成立。

### 2.2 `experiments/g5_decisive.py` — 直接偏导残差

```powershell
& '...\python.exe' -u g5_decisive.py
```

**exit code: `0`**。该脚本对显式二孤子 `F_j, G_j` 做**直接偏微分**（不经 mode 展开），
残差在 `E1, E2` 中的全部多项式系数为零，9 个并集 mode 上的和式亦全为零。

### 2.3 `experiments/g3_mode_audit.py` — `N = 1..5` 系数审计

```powershell
& '...\python.exe' -u g3_mode_audit.py
```

**exit code: `0`**。`N = 1..5` × 4 组参数，展开系数共 2904 个，**全为零**。

### 2.4 `experiments/g4_eigen_16cases.py` — 逐点非零性的记录

```powershell
& '...\python.exe' -u g4_eigen_16cases.py
```

**exit code: `0`**。该脚本记录 16 个 mode 对中 `eigen a μ ν` 的**非零**情形，
即「逐点消失为假、只有加权和为零」的证据。

### 2.5 `experiments/g6a_closed_form.py` — **失败的假设**（保留为证据）

```powershell
& '...\python.exe' -u g6a_closed_form.py
```

**exit code: `0`，但检查行为 `FAIL`。** 该脚本检验候选闭式

```
eigen (a+δ) μ ν = (1+2δ)(k_μ − k_ν) + k₁²d₀(d₀−1) + k₂²d₁(d₁−1)
```

输出：

```
  K + P1 (P1=d0(d0-1)k1^2+d1(d1-1)k2^2): FAIL on [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 0), (1, 1))]
   FAIL 1 1 (0, 0) (0, 1) 0 18 15
   ...
   exact check: FAIL
```

**结论.** 该候选闭式**被否证**。正确陈述是较弱的
`eigen (a+δ) = eigen a + 2δ(k_μ − k_ν)`（已在 Lean 中形式化），
而 `eigen a` 本身对 16 个 mode 对**不**全为零。此文件保留，作为
「不成立的形式」的记录。

### 2.6 `experiments/g6b_solve.py` — 符号分解表

```powershell
& '...\python.exe' -u g6b_solve.py
```

**exit code: `0`**。输出 `eigen a` 在 16 个 mode 对上的**显式值**，以及
`δ` 系数表（每个非对角对的系数恰为 `2δ`），和
`eigen(a+δ) − (1+2δ)K` 的余项表。

### 2.7 `experiments/g1_sympy_core.py`、`g2_degeneracy_audit.py`

```powershell
& '...\python.exe' -u g1_sympy_core.py          # exit code: 0
& '...\python.exe' -u g2_degeneracy_audit.py    # exit code: 0
```

核心双线性恒等式与退化性审计。

---

## 3. 汇总

| 检查 | 命令 | exit code | 结果行 |
|---|---|---|---|
| Lean 模块 | `Check-Lean.ps1 ... DirG.lean` | `0` | `PASSED: 1 local module(s).` |
| 交错残差（精确有理数） | `python -u g6_pair_vanishing.py` | `0` | `ALL CHECKS PASSED` |
| 直接偏导残差 | `python -u g5_decisive.py` | `0` | 全系数为零 |
| `N=1..5` 系数审计 | `python -u g3_mode_audit.py` | `0` | 2904 系数全零 |
| 16 mode 对逐点值 | `python -u g4_eigen_16cases.py` | `0` | 记录非零值 |
| 候选闭式（否证） | `python -u g6a_closed_form.py` | `0` | `exact check: FAIL`（预期） |
| 符号分解表 | `python -u g6b_solve.py` | `0` | 表输出 |

**未通过的检查（如实记录）：**
`g6a_closed_form.py` 的闭式假设 `eigen(a+δ) = (1+2δ)(k_μ−k_ν)` **为假**，
其 `FAIL` 行为是**正确**的否证结果，不是脚本错误。
Lean 侧不包含该形式。

---

## 4. 明确**未**验证的内容

* **任意 `N`**：仅归约到论文 Lemma 2.1 的行列式恒等式，未形式化、未独立验证。
* **连续极限 `h → 0`**：仅有解析核对（`h²` 阶），无 Lean 或数值验证脚本。
* **实性 `F_j, G_j ∈ ℝ`、零点不存在性**：未验证。
* **离散约束 `w = u_y` 的类比**：未验证。
* **适定性 / 稳定性 / 收敛性**：**未**验证，且已知连续常背景线性化给出
  Hadamard 意义下的不适定性（`|Re σ| ~ k²`）。
* **文献新颖性**：未做检索，不主张。
