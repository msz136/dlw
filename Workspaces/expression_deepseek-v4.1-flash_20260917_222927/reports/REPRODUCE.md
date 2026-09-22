# REPRODUCE — 复现指南

运行目录（下称 `$run`）：

```
C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927
```

---

## 1. 环境（已固定，本次运行未做任何环境安装）

| 项 | 值 |
|---|---|
| Lean | 4.34.0 |
| Mathlib | v4.34.0，commit `5ed2965256430c3649e86755f9576b54eca72435` |
| Mathlib 源码（只读，供查 API） | `C:\Users\msz\学术内容\_lean_shared\mathlib\Mathlib` |
| **唯一 Lean 检查入口** | `C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1` |
| Python | 3（`sympy` 必需，`numpy`/`scipy` 用于方向 B/D 的实验） |
| 已有只读工作 | `C:\Users\msz\学术内容\lean-toda\`（前序工作，**只读**） |

### 1.1 硬性纪律（本次运行严格遵守）

* 只写 `.lean` 文件；**不**运行 `elan install` / `lake init` / `lake update` /
  `lake exe cache get` / `lake build Mathlib`；**不**新建 Lake 项目；
  **不**克隆、复制或重编译 Mathlib；**不**新建工具链。
* **不**修改 `_lean_shared`、`lean-toda`、其他模型目录；**不**修改全局 PATH 或执行策略。
* 成功判据：**退出码 0 且输出含 `PASSED`**。
* `sorry` / `admit` / 新 `axiom` 一律不被接受，不得绕过。
* **构建通过 ≠ 研究结论成立。** 必须区分：
  代数恒等式 / 结构定理 / 实函数分析 / 有限样本 / 一般参数 / 条件性 / 无条件。

---

## 2. Lean 验证

```powershell
$run = 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927'
$ck  = 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1'
```

检查器会编译 `-Root` 下的**全部**本地模块并运行其中的 `#print axioms`。
结果落在 `<Root>\.lean-runs\<run-id>\result.json` 与 `build.log`。

### 2.1 主控跨方向 no-go 模块

```powershell
& $ck -Root "$run\proofs" -File "$run\proofs\Smoke.lean" -TimeoutSeconds 300
```

期望输出（末行）：

```
PASSED: 2 local module(s).
```

其中 `MainNoGo.lean` 的 `#print axioms` 应为
`[propext, Classical.choice, Quot.sound]`（`semidiscrete_elimination`、
`growth_lower_bound`、`growth_unbounded` 三者皆然）。

### 2.2 各方向模块

| 方向 | 检查命令（`-Root` 均为 `<方向目录>\proofs`，`-File` 为其主模块） |
|---|---|
| **A** 有限差分 | `DirA_Periodic.lean` |
| **B** 谱方法 | `DirB.lean`（并覆盖 `Spectral\Multiplier.lean`、`Spectral\Aliasing.lean`、`Spectral\Growth.lean`） |
| **C** 混合 FEM/DG | `Main.lean`（并覆盖 `C_FEM_DG.lean`） |
| **D** 守恒/SBP | `DirD.lean` |
| **E** Hamiltonian/Poisson | `E_Poisson.lean` |
| **F** 变分/多辛 | `F_Multisymplectic.lean` |
| **G** Hirota/Bäcklund | `DirG.lean` |
| **H** Toda 嵌入 | `DirH.lean`（另可跑 `AuditH.lean`，`PASSED: 3 local module(s).`） |

示例：

```powershell
& $ck -Root "$run\C_mixed_fem_dg\proofs" -File "$run\C_mixed_fem_dg\proofs\Main.lean" -TimeoutSeconds 300
& $ck -Root "$run\F_variational_multisymplectic\proofs" -File "$run\F_variational_multisymplectic\proofs\F_Multisymplectic.lean" -TimeoutSeconds 300
```

**已由主控独立确认的期望末行（八方向 + 跨方向全部 `exit 0`）**：

```
MainNoGo     → PASSED: 2 local module(s).      (proofs\Smoke.lean)
A            → PASSED: 1 local module(s).      (DirA_Periodic.lean)
B            → PASSED: 5 local module(s).      (DirB.lean)
C            → PASSED: 3 local module(s).      (Main.lean)
D            → PASSED: 2 local module(s).      (DirD.lean)
E            → PASSED: 1 local module(s).      (E_Poisson.lean)
F            → PASSED: 1 local module(s).      (F_Multisymplectic.lean)
G            → PASSED: 1 local module(s).      (DirG.lean)
H            → PASSED: 2 local module(s).      (DirH.lean)  /  AuditH.lean → PASSED: 3
```

全部 `#print axioms` 只出现 `propext, Classical.choice, Quot.sound`，**无 `sorryAx`**，
无 `sorry` / `admit` / 新 `axiom`。

---

## 3. SymPy 独立验证（主控跨方向）

```powershell
python -u "$run\common\MAIN_verify_core.py" v2 v3 v5 v6 v7 v10   # 全部 PASS
python -u "$run\common\MAIN_verify_core.py" v9                   # PASS：2904 系数全零
python -u "$run\common\MAIN_verify_core.py" v4                   # 慢；单独跑
python -u "$run\common\MAIN_verify_core.py" v8                   # 全符号；很慢；单独后台跑
```

**已确认的期望输出**：

```
[PASS] V2  D_y(P f.g) = d_y(P f.g) - 2 P(f.g_y)  for all tested P
[PASS] V3  (D_yB-4D_x)f.g + 2[B f.g_y + 2 D_x f.g] = d_y(B f.g) => on {B f.g=0}: 论文 (6) at lam=-2
[PASS] V5  w=u_y: (1) == w_t + d_x[v_x+(u+2a)w]
[PASS] V5  w=u_y: (2) == v_t + d_x[(u+2a)v+w_x+2*lam*u]
[PASS] V6  线性化 [sigma + i(u0+2a)k]^2 = k^4 - (v0+2*lam) k^3/ell
[PASS] V7  v == -2*lam 且 u = U(x,t) 任意（u_y = 0）为精确解 => y-无关零模
[PASS] V10 A_h = Bf.g + h^2(...) + O(h^4)     (无 h^1 项)
[PASS] V10 C_h = Bf.g_y + 2 Dx f.g + h^2(...) + O(h^4)
ALL REQUESTED CHECKS PASSED
```

V9 期望：

```
[PASS] V9  staggered tau family: exact rational N=1..5 x 4 parameter sets,
       2904 coefficients, all zero, arbitrary theta constants a=1..3, h in (0,1/2)
```

> ⚠ **运行 V9 前请注意**：该检查曾在**校验器自身有缺陷**时给出假阴性。
> 详见 `reports/MAIN_VERIFICATION.md` §3.2–§3.3 与
> `common/SHARED_MATH_SPEC.md` §3.3。当前脚本已修正。

**执行器注意**：单次 pwsh 调用上限 600 秒。`v4`/`v8` 会超时，
必须**单独**或**后台**运行。

---

## 4. 主控跨方向不适定性分析

```powershell
python -u "$run\experiments\MAIN_discrete_dispersion.py"
```

期望末行：

```
ALL CROSS-CUTTING CHECKS PASSED
```

覆盖 D1–D5：连续色散、半离散色散（一般格点符号）、`|Re σ|/k² → 1`、
具体格点符号的 Nyquist 零点、`ℓ=0` 零模扇区。

---

## 5. 各方向实验脚本

| 方向 | 脚本 |
|---|---|
| A | `experiments\exp1_symbols.py`、`exp2_symbols.py`、`exp3_constraint.py`、`exp4_lattice.py`、`exp6_mechanical.py` |
| B | `experiments\spectral_diagnostic.py`（摘要：`spectral_diagnostic_summary.json`） |
| C | `experiments\c_fem_dg_checks.py` |
| D | `experiments\e1_exact_identities.py`、`e2_linear_symbol.py` |
| E | `experiments\e1_poisson_search.py`、`e2_poisson_antisym.py` |
| F | `experiments\f_multisymplectic_checks.py`（主控亲自编写） |
| G | `experiments\g1_sympy_core.py`、`g2_degeneracy_audit.py`、`g3_mode_audit.py` |
| H | `experiments\verify_h_toda.py`、`diagnose_mkp_tau.py` |

每个方向目录内另有 `VERIFY.md`，记录该方向**真实的退出码与 `PASSED` 行**，
以及（按要求）**该方向自身发现的错误与修正**。

---

## 6. 阅读顺序建议

1. `reports\FINAL_REPORT.md` — 总报告与推荐排序
2. `reports\CLAIMS_AND_PROOFS.md` — 全部结论编号 + 证明覆盖度
3. `reports\MAIN_VERIFICATION.md` — 主控验证记录（**含主控自身错误的如实记录**）
4. `common\SHARED_MATH_SPEC.md` — 共享契约（§2 不适定性；§2.0 格点符号约定）
5. 各方向 `report.md` / `VERIFY.md`
