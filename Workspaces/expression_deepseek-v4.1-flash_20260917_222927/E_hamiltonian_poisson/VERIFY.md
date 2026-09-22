# VERIFY.md — 方向 E 验证记录（真实命令 / 真实退出码 / 真实输出行）

工作根：`C:\Users\msz\学术内容`
方向目录：`C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\`

未修改 `_lean_shared`、`lean-toda`、其它模型目录或任何 sibling 方向目录。本方向所有写入均在其自身目录内。

---

## 1. Lean 验证（唯一允许入口）

### 命令

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\proofs\E_Poisson.lean' `
  -TimeoutSeconds 300
```

未使用任何被禁命令（无 `elan install`、无 `lake`、无 Mathlib 克隆/重编译、无 `pip`/`npm`）。文件内无 `sorry`、无 `admit`、无新增 `axiom`。

### 第 1 次运行（失败 —— 如实记录）

```
CHECK E_Poisson.lean
...E_Poisson.lean:175:2: error: `simp` made no progress
'DLW.E.constant_Q_singular' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
LEAN_CHECK_FAILED: E_Poisson.lean. Correct the proof/import; do not reinstall dependencies.
EXITCODE=1
```

原因：`Theta3_eq_zero_of_w_eq_zero` 末尾的裸 `simp` 在 `rw` 之后无可改写目标；错误恢复引入 `sorryAx`。
修正：改为 `apply Matrix.ext; intro i j; rw [Theta3, theta_entry, hw i, hw j, Matrix.zero_apply]; ring`。
同时把 `constant_Q_singular`（矩阵值推论，需 `!![...]` 化简，脆）替换为 `no_nontrivial_constant_poisson_Q`（命题形式，稳定）。
另修正一处数学笔误：`(1,2)` 分块的 `D_x^1` 系数条件由 `q22 − q11 = 0` 更正为 `q22 + q11 = 0`（由 `(DΦ Q)_{12} = ((DΦ Q)_{21})^*` 直接得到）。

### 第 2 次运行（通过）

```
CHECK E_Poisson.lean
'DLW.E.theta_antisym' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.theta_eq_of_skew' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.Theta3_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.no_invertible_constant_poisson_bracket' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.no_nontrivial_constant_poisson_Q' depends on axioms: [propext, Classical.choice, Quot.sound]
PASSED: 1 local module(s).
REPORT: ...\proofs\.lean-runs\20260917_234438_df1afb40\result.json
EXITCODE=0
```

### 第 3 次运行（最终，含符号更正后）

```
CHECK E_Poisson.lean
'DLW.E.theta_antisym' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.theta_eq_of_skew' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.Theta3_ne_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.no_invertible_constant_poisson_bracket' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.E.no_nontrivial_constant_poisson_Q' depends on axioms: [propext, Classical.choice, Quot.sound]
PASSED: 1 local module(s).
REPORT: C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\proofs\.lean-runs\20260917_234613_56c85104\result.json
EXITCODE=0
```

**成功判据满足**：退出码 `0` **且** 输出含 `PASSED`。

公理检查：5 个 headline 定理全部只依赖 `propext, Classical.choice, Quot.sound`（标准基础），**无** `sorryAx`，**无**非标准公理。

### 文件与定理

* `proofs/E_Poisson.lean`（`namespace DLW.E`，`#print axioms` 已置于文件末尾）
* 定理：`theta_entry`、`theta_antisym`、`theta_eq_of_skew`、`cum3_one_zero`、`cum3_zero_one`、`cum3_two_zero`、`cum3_zero_two`、`Theta3_one_zero`、`Theta3_two_zero`、`Theta3_ne_zero`、`Theta3_eq_zero_forces`、`Theta3_eq_zero_of_w_eq_zero`、`no_invertible_constant_poisson_bracket`、`no_nontrivial_constant_poisson_Q`
* 未创建 `Main.lean`：`#print axioms` 直接放在 `E_Poisson.lean` 末尾，无需第二个模块。
* 未 `import Common.Operators`：本方向文件不需要该模块的任何定义，避免跨根引用风险；共享模块**未被修改**。

---

## 2. 实验（SymPy，精确有理/符号）

### 一行运行命令

```
python -u "C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\experiments\e1_poisson_search.py"
python -u "C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\E_hamiltonian_poisson\experiments\e2_poisson_antisym.py"
```

### `experiments/e1_poisson_search.py`

关键输出（原文摘录）：

```
E1  general CONSTANT symmetric Q (2n x 2n) : Helmholtz blocks
  n=2 seed=7:  solution set = {(0, 0, 0, p1_1, 0, 0, 0, 0)}
  n=2 seed=11: solution set = {(0, 0, 0, p1_1, 0, 0, 0, 0)}
  n=3 seed=7:  solution set = {(0,...,0, p2_2, 0,...,0)}
  n=3 seed=11: solution set = {(0,...,0, p2_2, 0,...,0)}
E2  Theta == A - A^T : True | skew: True | entry w_i C_ij - w_j C_ji: True   (n=2,3,4)
E2  n=3 Theta at w=(1,2,3): [[0, -2, -3], [2, 0, -3], [3, 3, 0]]  nonzero=True
E4  n=3: (E - E^T) at zero mode == 0 : True ; Theta at zero mode != 0 (w=(1,2,3)) : True ; Theta at w==0 : True
DONE
EXITCODE=0
```

解读：单侧累加和约定下唯一残解是 `Q₁₁ = p·E_{last,last}`（**奇异**）。

### `experiments/e2_poisson_antisym.py`

关键输出（原文摘录）：

```
E5  [circulant-asym] n=3 seed=7/11, n=4 seed=7/11  -> sol space dim 0, Q11=0, Q12=0, det=0
E6  [general-asym]  n=2 seed=7, n=3 seed=7          -> sol space dim 0, Q11=0, Q12=0, det=0
E7  [cumsum]        n=3, n=4                        -> Q11 = [[0,..],[..,0, p_{n-1,n-1}]] , det=0
E8  [general-asym-SYM] n=2 SYMBOLIC solution:
      [{p0_0: 0, p0_1: 0, p1_0: 0, p1_1: 0, r0_0: 0, r0_1: 0, r1_0: 0, r1_1: 0}]
DONE
EXITCODE=0
```

解读：`n = 2`、一般反对称 `C`、`w,v,a,λ` 全符号时，Helmholtz 系统唯一解为 `Q = 0`。

两次运行均 `EXITCODE=0`，无异常、无未捕获错误。

---

## 3. 未做的事（防止误读）

* **没有**任何分析层面的 Lean 结果：无余项估计、无稳定性、无收敛定理。
* **没有**形式化"Hamiltonian 存在 ⟹ Helmholtz 三条系数方程"这一变分学桥接；该桥接在 `proofs/E_Poisson.lean` 中作为**假设**取入，并在 `report.md` §6/§7 与 `CONCLUSIONS.md` 结论 7 中显式标注为未形式化。
* **没有**主张 Hamiltonian/Poisson/辛结构消除 `|Re σ| ~ k²` 的 Hadamard 不适定；相反，本方向结论更强（类 𝒞 中无括号）。
* **没有**做独立文献检索，**不主张**新颖性。
