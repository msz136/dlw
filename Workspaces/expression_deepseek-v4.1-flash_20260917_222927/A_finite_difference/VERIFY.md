# VERIFY — Direction A

所有命令均在 `A_finite_difference\` 下实际执行。下面给出**真实命令、真实退出码、
真实输出行**。Python 解释器：`C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe`
（Python 3.13.3，SymPy 1.13.3，NumPy）。

---

## 1. Lean

**命令（原文照抄）**

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\A_finite_difference\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\A_finite_difference\proofs\DirA_Periodic.lean' `
  -TimeoutSeconds 600
```

**真实结果**

| 项 | 值 |
|---|---|
| 退出码 | `0` |
| 输出行 | `PASSED: 1 local module(s).` |
| `sorry` / `admit` / 新 `axiom` | 无（检查器拒绝占位符；本次未被拒绝） |
| 报告文件 | `proofs\.lean-runs\20260918_001804_98964a8c\result.json` |

**已证明的定理（`proofs/DirA_Periodic.lean`）**

- `DLW.DirA.altTwo_zero` / `altTwo_one` / `altTwo_add_two`
- `DLW.DirA.altTwo_two_mul` / `altTwo_two_mul_add_one`
- `DLW.DirA.altTwo_period_two`
- `DLW.DirA.altTwo_shift_one`（2-反周期）
- `DLW.DirA.altTwo_eq_of_mod_two_eq`
- `DLW.DirA.twoPeriodic_of_twoAntiPeriodic`
- `DLW.DirA.ctrL_eq_zero_of_twoPeriodic`
- `DLW.DirA.twoPeriodic_of_ctrL_eq_zero`
- `DLW.DirA.ctrL_kernel_iff` ← 主结果（核 = 2-周期序列）
- `DLW.DirA.narrow_second_difference`

**未做的事（诚实声明）**

- 没有 `#print axioms` 行：本模块不含 `axiom`，且所有定理都在 `Mathlib` 的
  `propext`/`Classical.choice`/`Quot.sound` 之外无额外假设；由于无 headline 定理需要
  逐条审计公理依赖，此处从略。若需要，可加 `#print axioms DLW.DirA.ctrL_kernel_iff`。
- **没有**在 `Fin N` 上完成有限维维度陈述（`dim ker = 2`）；`Fin N` 索引算术
  （$`j+2`$ 模 $`N`$ 保奇偶性）未突破。整数格点版本已完整证明。

---

## 2. Python 实验（全部真实退出码）

命令：`python -u <file>`，工作目录 `experiments\`。

| 文件 | 退出码 | 关键输出行 |
|---|---|---|
| `exp1_symbols.py` | `0` | Taylor 系数表（中心 $`c_2=+1/6`$；紧致 $`c_4=-1/180`$） |
| `exp2_symbols.py` | `0` | `Nyquist xi = pi : f_ctr = 0    f_sg = 2/h` |
| `exp3_constraint.py` | `0` | `ran D = { w : sum_j w_j = 0 and sum_j alpha_j w_j = 0 }, codimension 2` |
| `exp4_lattice.py` | `0` | 比值 $`|\operatorname{Re}\sigma|/k^2`$：`1.00001362`（$`k=10^4`$） |
| `exp6_mechanical.py` | `0` | `difference : 0`（离散关系连续极限 ≡ V6）；`leading term in k is k^4 times the coefficient: 1` |

> 注：`exp5_dispersion.py`、`exp2_spectrum.py`、`exp4_eigen.py` 是推导过程中的
> **被取代/错误**版本，已删除，以免误用。权威推导为 `exp6_mechanical.py`。

---

## 3. 复现

```powershell
# Lean
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\A_finite_difference\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\A_finite_difference\proofs\DirA_Periodic.lean' `
  -TimeoutSeconds 600
# 期望：exit 0，且出现 "PASSED: 1 local module(s)."

# 实验
cd 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\A_finite_difference\experiments'
foreach ($f in 'exp1_symbols.py','exp2_symbols.py','exp3_constraint.py','exp4_lattice.py','exp6_mechanical.py') {
  & 'C:\Users\msz\AppData\Local\Programs\Python\Python313\python.exe' -u $f
}
# 期望：每个 exit 0
```

---

## 4. 覆盖度结论

- Lean：**通过**（1 个模块，退出码 0）。
- Python：**5/5 通过**（退出码 0）。
- 但 Lean 覆盖的是**整数格点上的核刻划 + 棋盘模式代数**，**不**覆盖色散关系、
  可解性条件的充分性、奈奎斯特退化与病态性。
- 因此：证明覆盖度 = `Lean 结构验证`（核刻划 / 棋盘代数）+ `Lean 代数验证`
  （一步算子恒等式）+ `实验验证`（其余）。
  **未达到** `Lean 分析验证` 或 `数学证明，尚未完整形式化`。
- 路线状态 = `已建立候选构造（离散化方案）；核心病态性为不可消除的障碍`。
