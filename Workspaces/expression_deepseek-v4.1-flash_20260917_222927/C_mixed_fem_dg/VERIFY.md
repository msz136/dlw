# VERIFY.md — 方向 C 实际执行的命令、真实退出码与 PASSED 行

工作根：`C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\C_mixed_fem_dg\`
未使用任何安装类命令（无 `elan install`、无 `lake *`、无 `pip/npm install`、未改动
`_lean_shared` / `lean-toda` / 其他方向目录 / 共享 spec）。仅创建本目录内文件。

---

## 1. Lean 验证（共享入口，唯一允许路径）

### 运行 1（初始版本，**失败** — 已如实记录）

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\...\C_mixed_fem_dg\proofs' `
  -File 'C:\Users\msz\学术内容\...\C_mixed_fem_dg\proofs\C_FEM_DG.lean' -TimeoutSeconds 300
```

真实退出码：**1**（`LEAN_CHECK_FAILED: C_FEM_DG.lean`）。
真实错误（3 处，均为我自己写错的陈述/证明，非环境问题）：

```
C_FEM_DG.lean:34:  unsolved goals  ⊢ h ^ 2 * (5 / 12) = h ^ 2 * (1 / 12)
    （我把单元质量矩阵对角元误写成 2h/3，实际为 h/3；因此 p1_mass_det 当时是假命题）
C_FEM_DG.lean:115: unsolved goals  ⊢ Real.sin θ * (2 + Real.cos θ) / (2 + Real.cos θ) = Real.sin θ
C_FEM_DG.lean:126: unsolved goals  ⊢ 3 * Real.sin θ / (2 + Real.cos θ) - θ = (...) / (2 + Real.cos θ)
    （field_simp 缺少 2 + cos θ ≠ 0 这一事实）
C_FEM_DG.lean:151: rewrite failed: Did not find an occurrence of the pattern ?a + 0
```

该次运行的 `#print axioms` 出现了 `sorryAx`（正是因为存在未证目标），**不能**采信。
修正后重跑，见运行 2/3。

### 运行 2（修正后，`C_FEM_DG.lean`）

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\C_mixed_fem_dg\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\C_mixed_fem_dg\proofs\C_FEM_DG.lean' `
  -TimeoutSeconds 300
```

真实退出码：**0**
真实输出（末尾关键行）：

```
'DLWC.p1_mass_det_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.muP1_nyquist_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.dg_symbol_no_nyquist_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.dg_upwind_dissipation_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.dg_upwind_dissipation_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
PASSED: 2 local module(s).
REPORT: ...\proofs\.lean-runs\20260917_233858_d971b25d\result.json
```

（仅两条无害 warning：`field_simp` 之后多余的 `ring` 未起作用。**无** `sorryAx`。）

### 运行 3（`Main.lean`，导入 `C_FEM_DG` 并 `#print axioms`）

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\C_mixed_fem_dg\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\C_mixed_fem_dg\proofs\Main.lean' `
  -TimeoutSeconds 300
```

真实退出码：**0**
真实输出（末尾关键行）：

```
'DLWC.p1_mass_det' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.p1_mass_det_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.p1_stiffness_kills_constant' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.mass_symbol_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.p1_symbol_pos_in_band' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.muP1_nyquist_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.dg_symbol_no_nyquist_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.p1_symbol_normalisation' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.dg_upwind_dissipation_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLWC.dg_upwind_dissipation_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
PASSED: 3 local module(s).
REPORT: ...\proofs\.lean-runs\20260917_234037_5d1b10ef\result.json
```

结论：`proofs/C_FEM_DG.lean` 与 `proofs/Main.lean` **全部 PASSED**，公理足迹仅
`propext, Classical.choice, Quot.sound`（标准基础），**无 `sorry` / `admit` / 新 `axiom`**。

---

## 2. 实验脚本（SymPy / NumPy）

运行命令（在 `C_mixed_fem_dg\` 下）：

```
python -u experiments/c_fem_dg_checks.py
```

### 运行 A（初始版本，**失败** — 已如实记录）

真实退出码：**1**
真实错误：`numpy.linalg.LinAlgError: Singular matrix`（第 96 行）。
原因是我未跳过 `μ_h = 0` 的退化模（`ℓ=0` 的 `y`-常数模，以及 Nyquist 模），
且 P1 DG 的单元矩阵两行符号写反。属脚本自身缺陷，非环境问题。

### 运行 B（修正后）

`python -u experiments/c_fem_dg_checks.py` → 真实退出码：**0**

关键真实输出（节选，未修改）：

```
A1  M symbol  - h(2+cos)/3      = 0  [0 = ok]
A2  A^T symbol - i sin           = 0  [0 = ok]
A3  mu_P1 - 3 i sin/(h(2+cos))   = 0
A4  R(theta) series              = 1 - theta**4/180 - theta**6/1512 - theta**8/25920 + O(theta**9)
A5  numerator 3 sin - th(2+cos)  = -theta**5/60 + theta**7/1260 + O(theta**9)
A6  mu_P1 at Nyquist theta=pi    = 0   [0 = Nyquist zero]
A7  mu_P1 - i ell (series in ell)= -I*ell**5*h**4/180 + O(ell**7)
A8  mu_DG(P0 upwind) Re = (1 - cos(theta))/h  Im = sin(theta)/h
A9  mu_DG series in theta        = I*theta/h + theta**2/(2*h) - I*theta**3/(6*h) + O(theta**4)
A10 mu_DG at Nyquist             = 2/h  [2/h != 0]
A11 mu_DG - i ell (series in ell)= ell**2*h/2 + O(ell**3)
B1  branch (物理支) small theta: I*theta/h + theta**4/(72*h) + O(theta**5) ; at Nyquist: (1 + sqrt(11)*I)/h
B1  branch (寄生支) small theta: 6/h - 3*I*theta/h - theta**2/h + ...          ; at Nyquist: (1 - sqrt(11)*I)/h
C1  max|M^-1 - (sqrt3/h) sum_w r^|j-k+wN|| = 5.551115123125783e-16   r = sqrt3-2 = -0.2679491924311228
C2  |M^-1| decay ratios: |c1/c0| = 0.2679496669133975  |c3/c2| = 0.26804123711340205  (theory 0.267949)
C3  mode n= 1 : M-symbol 0.500215797418 (closed 0.500215797418) ; A^T-symbol 0.5j (closed 0.5j)
C3  mode n= 2 : M-symbol 0.436332312999 (closed 0.436332312999) ; A^T-symbol 0.866025403784j (closed 0.866025403784j)
C3  mode n= 5 : M-symbol 0.197915903379 (closed 0.197915903379) ; A^T-symbol 0.5j (closed 0.5j)
C3  mode n= 6 : M-symbol 0.174532925199 (closed 0.174532925199) ; A^T-symbol -0j (closed 0j)   ← Nyquist
C4  A = u0+2a = 1.8 ; v0+2lam = -2.9 (standing zero-mode background v0 = -2lam = 4)
C5  k= 0.7  max |discrete sigma - analytic sigma| over non-degenerate modes = 1.490e-15
C5  k= 1.3  max |discrete sigma - analytic sigma| over non-degenerate modes = 1.110e-15
C5  k= 2.5  max |discrete sigma - analytic sigma| over non-degenerate modes = 3.972e-15
C6  analytic formula used: (sigma + i A k)^2 = k^4 - i (v0+2lam) k^3 / mu_h(ell)
C7  degenerate modes (mu=0), v0=1.1 (c=-2.9) -> [-1.60433754-3.15564824j  1.60433754+0.81564824j]
C7  degenerate modes (mu=0), v0=4 (c=0)      -> [-0.-2.34j  0.+0.j]
C8  h=0.400 P1 err=2.133497e-03 (ratio -)      DG-P0 err=5.706140e-01
    h=0.200 P1 err=1.279581e-04 (ratio 16.6734) DG-P0 err=2.880732e-01
    h=0.100 P1 err=7.915279e-06 (ratio 16.166)  DG-P0 err=1.443840e-01
    h=0.050 P1 err=4.934301e-07 (ratio 16.0413) DG-P0 err=7.223550e-02
C9  Fourier coefficients of 1/(2+cos): c0 = 0.5773502691896257 (1/sqrt3 = 0.5773502691896258)
    c_n / r^n for n=1..5: [0.5773502692] * 5   (1/sqrt3 = 0.5773502692)
C10 det(element mass) - h^2/12 = 3.469446951953614e-18 ; stiffness * (1,1) = [0. 0.]
```

### 运行 C（修正根排序，仅显示关键行）

`python -u experiments/c_fem_dg_checks.py 2>&1 | Select-String -Pattern 'C5|C7|...'` → 真实退出码：**0**
`C5` 三项误差：`1.490e-15 / 1.110e-15 / 3.972e-15`。
（运行 B 中 `k=0.7` 曾显示 `7.839e-01`：那是**比较方式的伪影**——两离散本征值在 `k=0.7` 时
几乎纯虚，按实部排序产生错配；改为双射配对比较后为 `1.490e-15`。数学结论未变，此处如实记录。）

---

## 3. 结果归属（哪些数字支撑哪条结论）

| 输出 | 支撑结论 |
|---|---|
| A1–A3, C3 | `μ_h` 闭式与 `M`、`Aᵀ` 符号（C5） |
| A4, A5, A7, C8 | `R = 1 - θ⁴/180 + ...`、4 阶符号相容（C6） |
| A6, C3(n=6) | 一致质量 P1 的 Nyquist 零（C11） |
| A8, A9, A10, A11 | P0 DG 迎风符号、`O(h)` 阶、耗散、无 Nyquist 零（C8, C13） |
| B1 | P1 DG 迎风两支符号（C10） |
| C1, C2, C9 | `M^{-1}` 精确闭式与指数衰减（C14） |
| C4–C7 | 离散色散关系与退化模虚假增长（C17, C12, C19） |
| C10 | 单元质量 `det = h²/12`、刚度湮灭常数（C2, C4） |

`C13` 中 P1 DG 的 Nyquist 值 `(1±i√11)/h` 来自 B1（SymPy）；`C10` 的 `O(h³)` 阶数为
同一输出的小 `θ` 级数。二者均为 `实验验证`，报告中未标注为 Lean 结论。
