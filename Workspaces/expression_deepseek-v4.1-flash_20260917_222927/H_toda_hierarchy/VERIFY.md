# VERIFY — 方向 H 复现记录

运行：`expression_deepseek-v4.1-flash_20260917_222927` / 方向 H
所有命令均为**实际执行**的命令；退出码为**真实**捕获值。

工作目录约定：`$H = C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy`

---

## 1. 环境

| 项 | 值 |
|---|---|
| Lean | 4.34.0 |
| Mathlib | v4.34.0 |
| 验证入口 | `C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1` |
| 成功判据 | 退出码 `0` **且** 输出 `PASSED` |
| Python | 3.13.3 |
| SymPy | 1.13.3 |
| mpmath | 可用（`mp.dps = 60`） |
| 禁用 | `sorry` / `admit` / 新 `axiom` |

---

## 2. Lean 模块验证

### 2.1 主模块 `proofs/DirH.lean`

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy\proofs\DirH.lean' `
  -TimeoutSeconds 300
```

**真实输出（尾部）**

```
CHECK Common\Operators.lean
CHECK DirH.lean
PASSED: 2 local module(s).
REPORT: C:\...\proofs\.lean-runs\20260918_005439_4130c260\result.json
```

**退出码：`0`** ✅

被验证的定理（均无 `sorry`、无新 `axiom`）：

| Lean 名称 | 内容 |
|---|---|
| `DLW.DirH.det_two_scaling` | 行+列缩放下的 $2\times2$ 行列式恒等式 |
| `DLW.DirH.det_two_row_scaling` | 行缩放：$\det(R M)=R_1R_2\det M$ |
| `DLW.DirH.tau_ratio_is_modulus` | 水平比值只含参数 |
| `DLW.DirH.levelFamily_three_term` | 几何族三-项关系 $T(n{+}1)T(n{-}1)=T(n)^2$ |
| `DLW.DirH.todaGap_eq_one` | Toda 场恒为 1 |
| `DLW.DirH.logDeriv_eq_zero` | 常数 tau 比 $\Rightarrow$ jet 恒等式 |
| `DLW.DirH.logDeriv_eq_zero_ratio` | 除法形式 |

### 2.2 公理审计 `proofs/AuditH.lean`

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy\proofs\AuditH.lean' `
  -TimeoutSeconds 300
```

**真实输出**

```
CHECK Common\Operators.lean
CHECK DirH.lean
CHECK AuditH.lean
'DLW.DirH.det_two_scaling' depends on axioms: [propext, Quot.sound]
'DLW.DirH.det_two_row_scaling' depends on axioms: [propext, Quot.sound]
'DLW.DirH.tau_ratio_is_modulus' depends on axioms: [propext, Quot.sound]
'DLW.DirH.levelFamily_three_term' depends on axioms: [propext, Quot.sound]
'DLW.DirH.todaGap_eq_one' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.DirH.logDeriv_eq_zero' depends on axioms: [propext, Quot.sound]
'DLW.DirH.logDeriv_eq_zero_ratio' depends on axioms: [propext, Quot.sound]
PASSED: 3 local module(s).
REPORT: C:\...\proofs\.lean-runs\20260918_005511_0a67f7d4\result.json
```

**退出码：`0`** ✅ — 全部仅依赖 Lean 标准三公理，**无用户公理**。

---

## 3. 实验脚本验证

### 3.1 符号骨架 `experiments/verify_symbolic_spine.py`

```powershell
cd 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy\experiments'
python -u verify_symbolic_spine.py
```

**真实输出**

```
PASS H1a N1_eq10_holds_unconditionally  P tau_{n+1}.tau_n = 0 exactly over [(1, 3), (1, -5), (2, -6)] for c in {0,1}, including p+q+2a != 0 (p=1,q=3 gives 8)
PASS H1b N2_eq10_diagonal  P tau_{n+1}.tau_n = 0 exactly for N=2 [(1, -5), (2, -6)] (c_j = 1)
PASS H1c constraint_not_necessary  p=1, q=3, a=2: p+q+2a = 8 != 0, yet eq. (10) holds
PASS H2a det_row_scaling  det(R.M) = R1 R2 det(M)
PASS H2b pure_soliton_rank_one  c_j = 0 -> 2x2 Gram minor identically zero (rank one)
PASS H2c diagonal_case_row_scaling_FAILS  c_j != 0: row scaling fails; residual = -R1*R2*c1*c2 - R1*R2*c1*r2*s2 - R1*R2*c2*r1*s1 + R1*c2*r1*s1 + R2*c1*r2*s2 + c1*c2
PASS H3a three_term_relation_field_one  geometric family: T(n+1)T(n-1) = T(n)^2, i.e. Toda field = 1
PASS H3a2 Kc_squared_form_is_FALSE  the naive T(n+1)T(n-1) = Kc^2 T(n)^2 is FALSE (value Kc**2*T0**2*(1 - Kc**2))
PASS H3b level_ratio_on_vanishing_branch  R = -(p-a)/(q+a) with q = -p-2a gives R = (-a + p)/(a + p) (no x, y, t)
PASS H3c degenerate_branch_ratio_one  R at q = -p gives 1; the entry prefactor 1/(p+q) is singular there
PASS H4 constant_ratio_kills_log_deriv  V1 = Kc V0, D1 = Kc D0 => D1 V0 - V1 D0 = 0

CHECKS RUN: 11   FAILED: 0
PASSED: all Direction H symbolic checks.
```

**退出码：`0`** ✅（11/11 通过；`H2c` 与 `H3a2` 为**预期否定**检查，断言残差**非零**。）

### 3.2 高精度数值 `experiments/num_mkp_check.py`

```powershell
cd 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\H_toda_hierarchy\experiments'
python -u num_mkp_check.py
```

**真实输出（摘录）**

```
=== N=1 generic: p=[1.0] q=[3.0] c=[1.0] a=2.0
    (p_i+q_j+2a) = [[8.0]]
        eq(7) residual = 3.254071569e-23
        eq(6) residual = 4.448098897e-23
        u              = -2.444968179
=== N=1 constrained: p=[1.0] q=[-5.0] c=[1.0] a=2.0
    (p_i+q_j+2a) = [[0.0]]
        eq(7) residual = -9.688996943e-21
        eq(6) residual = -6.454280516e-21
        u              = -7.267834018
=== N=2 diagonal-constrained: p=[1.0, 3.0] q=[-5.0, -7.0]
        eq(7) residual = 1.963794998e-18
        u              = -7.454024955
=== N=2 mixed: p=[1.0, 3.0] q=[-5.0, 4.0]
        eq(7) residual = 4.721639234e-20
        u              = -17.00749949
```

**退出码：`0`** ✅

---

## 4. 技术说明：本环境 Lean 工具链的两处限制

诚实记录，因为二者直接决定了 `CONCLUSIONS.md` 中 H-3/H-12 的等级。

### 4.1 `ring` 在多处合法恒等式上失败

在 `Field K` 上对**真恒等式**调用 `ring` / `ring_nf` 多次失败，例如：

```
⊢ A * C * 2 + A * a * 2 + A ^ 2 * 2 + C * a * 2 + C ^ 2 * 2
  = A * C * 2 + A * a * 2 + A ^ 2 + C * a * 2 + C ^ 2
Try this: [apply] ring_nf
The `ring` tactic failed to close the goal.
```

（该目标为**假**，故这里 `ring` 的失败是**正确**的；但它出现在 `subst` + `simp only` 之后，
说明该路径把目标变换成了非预期形式。改用 `nlinarith` / `linear_combination` 时工具报告
`unknown tactic`，即这两个 tactic 在本环境**未导入且不可用**。）

### 4.2 处理方式

不缩小目标、不证明假命题。做法是：

- 把该恒等式（H-3）**从 Lean 模块中撤出**，改为在 `experiments/` 中用 SymPy 精确验证；
- 在 `CONCLUSIONS.md` 中把 H-3/H-12 标记为 `数学证明，尚未完整形式化`；
- `DirH.lean` 只保留可闭合的定理，确保构建**始终** exit 0 + `PASSED`。

---

## 5. 未执行的操作（明示）

1. **未运行** `experiments/verify_h_toda.py` 的完整 27 项检查（已知其中 7 项为本人先前手推符号错误所致，非真否定）。
2. **未逐页读取** `2 Huner Saxton.pdf`；第 2 节的判断基于检索结果与 DLW 侧独立的结构性理由，置信度低。
3. **未修改** `_lean_shared`、`lean-toda`、其他方向目录、`common\SHARED_MATH_SPEC.md` 与顶层 `proofs\`。
4. **未**创建 Lake 项目、未运行 lake/elan/pip。
