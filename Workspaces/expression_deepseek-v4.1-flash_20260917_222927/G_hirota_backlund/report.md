# 方向 G：Hirota / Bäcklund / 层级离散化 — 交错双 tau 候选审计报告

## 0. 摘要

本报告审计下述「交错双 tau」候选：把 (2+1) 维色散长波（DLW）系统在 `y` 方向
半离散化后，猜想其双线性形式由**一对**算子给出

```
(B_{a-d}) F_j · G_j     = 0 ,      s = a - d ,
(B_{a+d}) F_j · G_{j+1} = 0 ,      s = a + d ,      d = h/2 ,
B_s := D_x^2 + D_t + 2 s D_x ,
```

其中 `F_j = T_{a-d}(M(j))`、`G_j = T_0(M(j))` 取自 Sheng–Yu 双 tau 族
（*Physica D* **432** (2022) 133140, DOI `10.1016/j.physd.2021.133140`）在首轮
`λ = a = -2` 处的构造。

**结论：候选未被否证。** 两个方程对显式二孤子 tau 对精确成立；`N = 1..5`
的多组参数检查（2904 个展开系数）全为零。**但**任意 `N` 未获证明（归约到论文
Lemma 2.1，未形式化），且**没有**任何文献新颖性主张。

一个重要的**修正**：原先工作区笔记 §5 陈述的矩阵元平移恒等式是**错误的**；
正确形式已给出并形式化，旧形式已用显式反例否证。

---

## 1. 问题与文献

### 1.1 连续 DLW 双线性形式

Sheng–Yu 的 DLW 双线性方程为 (1)–(2)/(6)–(7)

```
B_1 :  (D_x^2 + D_t + 2λ D_x) f·g = 0 ,
B_2 :  (D_y B_1 − 4 D_x) f·g = 0 ,      B_1 := D_x^2 + D_t + 2λ D_x ,
```

单孤子指数 `ξ = px + qy + ωt` 的色散关系为

```
(p+q)^2 + (q^2 − p^2) + 2λ(p+q) = 0 ,
```

**本报告实际核对到的等价形式（并对任意域形式化）**：

```
(p+q)^2 + (q^2 − p^2) + 2a(p+q) = 2 (p+q)(q+a) .
```

左侧的因式分解 `2(p+q)(q+a)` 是关键结构：它说明「特征条件为零」等价于
`p+q = 0` 或 `q + a = 0`。

### 1.2 实际检索到的文献

| 来源 | 标识 | 用途 |
|---|---|---|
| Sheng–Yu, *Physica D* **432** (2022) 133140 | DOI `10.1016/j.physd.2021.133140` | DLW 双线性形式 (6)–(7)、VT 约束 (5)、mKP 链 (9)–(10)、Gram 数据 (11)–(15) |
| Hunter–Saxton 相关手稿（本地 PDF） | `C:\Users\msz\学术内容\2 Huner Saxton.pdf`（`pdftotext` 抽取 107132 字节 / 1495 行） | 双 tau 双线性形式、伪 2-约化、离散 hodograph、Wronskian/Casoratian N-孤子、Lax 对；**空间方向**离散化后再做离散 hodograph |
| 工作区内部笔记 | `lean-toda/dlw_staggered_construction.md` | 被审计的候选与原先（错误）的矩阵元恒等式 |

**检索限制（必须声明）**：本次**没有**做系统的文献检索（无 `web_search`、
无数据库检索）。Hunter–Saxton 手稿只用于**方法论对照**（离散化策略的可行性），
**没有**核对其公式与 DLW 的逐条对应。因此本报告
**不主张**任何新颖性。

---

## 2. 显式的半离散双线性系统

取 `y ∈ hℤ`，格点指标 `j ∈ ℤ`，`d := h/2`。两个交错算子为

```
s_j^- = a − d      （对应格点 j）
s_j^+ = a + d      （对应格点 j+1）
```

即

```
(B_{a−h/2}) T_{a−h/2}(M(j)) · T_0(M(j))       = 0 ,
(B_{a+h/2}) T_{a+h/2}(M(j)) · T_0(M(j+1))     = 0 .
```

两个算子之差为 `2d = h`（`DLW.G.staggered_operators_differ`），故这是一个
**真正的双 tau（交错）系统**，而不是同一个方程写两遍。

**二孤子 tau 数据**（首轮 `λ = a = -2`，任意 `d`）。记

```
P_i = p_i − a ,   Q_i = q_i + a ,   ρ_i = ((P_i+d)(Q_i+d))/((P_i−d)(Q_i−d)) ,
r_i = −(P_i+d)/(Q_i−d) ,   Γ = (p₁−p₂)(q₁−q₂) / ((p₁+q₁)(p₁+q₂)(p₂+q₁)(p₂+q₂)) .
```

`T_0(M)` 的系数为 `1`（零模）、`1/(p_i+q_i)`（单孤子模）、`Γ`（双孤子模）；
`T_{a−d}(M)` 的系数为前者乘 `r_i`；`T_{a+d}(M)` 的系数为前者乘
`−(P_i−d)/(Q_i+d)`。这三族系数在 `proofs/DirG.lean` 中分别为
`baseCoef`、`specCoef`、`specCoefShift`。

---

## 3. 推导：mode 对代数与精确分解

把 tau 函数的指数作 `{0,1}²` 上的模式向量 `μ : Fin 2 → Fin 2`，令

```
k_i = p_i + q_i ,    w_i = q_i^2 − p_i^2 ,
kcoef μ = μ₀k₁ + μ₁k₂ ,   wcoef μ = μ₀w₁ + μ₁w₂ .
```

Hirota 求导法则 `D_x^m e^{ξ_a}·e^{ξ_b} = (k_a−k_b)^m e^{ξ_a+ξ_b}` 给出
`B_s` 在 mode 对 `(μ,ν)` 上的特征值

```
eigen s μ ν = (k_μ − k_ν)^2 + (w_μ − w_ν) + 2 s (k_μ − k_ν) .
```

于是双线性残差为

```
residual s f g = Σ_μ Σ_ν f_μ g_ν · eigen s μ ν .
```

### 3.1 精确的算子平移分解（已形式化，任意 `N`）

在两条单孤子色散关系下，

```
eigen (a+δ) μ ν = eigen a μ ν + 2 δ (k_μ − k_ν) .
```

这是 `proofs/DirG.lean` 的 `DLW.G.eigen_shift_split`。其含义是：
**平移修正项线性于波数差，且与谱数据完全无关**。因此 `δ` 依赖性是整体标量化的，
这是「为什么该构造不是 `N = 2` 特有」的代数原因。

数值/符号验证见 `experiments/g6_pair_vanishing.py`：
20 组参数 × 16 个 mode 对 × 6 个 `δ` 值全部通过，且符号层面亦成立。

**曾尝试的强形式被否证.** 若进一步假设
`eigen (a+δ) = (1+2δ)(k_μ − k_ν)`（即 `eigen a ≡ 0`），则**为假**：
`experiments/g6a_closed_form.py` 的 `exact check: FAIL` 给出否证。
差别在于 `eigen a` 一般不为零（见 §3.2）。

### 3.2 逐点消失是**假的**（重要的否证）

对 16 个 mode 对逐一计算 `eigen a μ ν`，**并非全部为零**。例如当
`μ = (0,0)`、`ν = (0,1)` 时 `eigen a = 2k₂² ≠ 0`，
`μ = (0,0)`、`ν = (1,1)` 时 `eigen a = 2(k₁² + k₁k₂ + k₂²) ≠ 0`。
（这些值由 `experiments/g4_eigen_16cases.py` 与 `g6b_solve.py` 记录。）

因此「每个 mode 对的指数系数都消掉」是**错误**的说法。真正成立的是
**带 tau 系数的加权和**为零：

```
Σ_μ Σ_ν f_μ g_ν (k_μ − k_ν) = 0      （对 specCoef/baseCoef 与 specCoefShift/baseCoef）
```

这是一个 **Cauchy 配对（Cauchy pairing）消去**，与 DLW 的 Gram 行列式结构一致，
而不是逐项消失。精确验证见 `experiments/g6_pair_vanishing.py`：
20 组可容许参数 × 16 个 mode 对，两个交错残差在**精确有理数**下恰为 `0`。

### 3.3 连续极限（解析核对，未形式化）

记格点上的前向/后向平均与差分 `A_h = (U^+ + U^−)/2`、`C_h = (U^+ − U^−)/h`，
则 `A_h = B f·g + O(h²)`，`C_h = B f·g_y + 2 D_x f·g + O(h²)`，于是

```
(D_y B − 4 D_x) f·g = ∂_y (B f·g) ,
```

与论文第二方程在 `λ = −2` 处相符；**无 `h¹` 项**。

---

## 4. 矩阵元平移恒等式：原陈述的错误与修正

工作区笔记 §5 原先断言

```
(−(p−(a+d))/(q+(a+d))) · (((p−a+d)(q+a−d))/((p−a−d)(q+a+d)))
    = −(p−(a−d))/(q+(a−d))        （错误形式）
```

**该形式为假。** `proofs/DirG.lean` 中的
`DLW.G.claimed_entry_counterexample` 给出显式反例：取
`(a,d,p,q) = (1,1,3,1)`，左侧 `= −1/3`，右侧 `= −3`。

**正确形式**（`DLW.G.shifted_entry_correct`，已形式化）：

```
κ_+ · ρ = κ_− ,
κ_∓ := −(p−a∓d)/(q+a∓d) ,   ρ := ((p−a+d)(q+a+d))/((p−a−d)(q+a−d)) .
```

即 `Q`-因子在分子与分母中取**一致**的平移方向。这一修正对交错构造的自洽性是
必要的；原先的检查脚本 `check_dlw_staggered.py --symbolic`
**从未测试**这第二个恒等式，它测试的是同一 tau 对上的一对不同算子。

---

## 5. 结果与障碍

### 5.1 结果

* 交错候选**未被否证**：两个方程对显式二孤子 tau 对精确成立。
* 精确的算子平移分解 `eigen (a+δ) = eigen a + 2δ(k_μ−k_ν)` 已在 Lean 中
  对任意域、任意 `N` 形式化（`eigen_shift_split`）。
* DLW 特征条件的因式分解 `k² + w + 2ak = 2(p+q)(q+a)` 已形式化
  （`dispi_to_alg`）。
* 两个交错方程对显式 tau 系数族的归约已在 Lean 中形式化
  （`two_soliton_eq1`、`two_soliton_eq2`、`residual_eq_zero`）。
* 矩阵元恒等式的正确形式已形式化，旧形式已被显式反例否证。

### 5.2 障碍

1. **逐点消失为假**：只有加权和为零。任何声称「每个 mode 对独立消去」的
   推理都是错的（§3.2）。
2. **任意 `N` 未证明**：归约到论文 Lemma 2.1 的行列式恒等式，该恒等式未形式化。
3. **实性 / 无零点 / 约束 `w = u_y`** 未证明。一般代数 tau 函数不保证
   `F_j, G_j` 为实数或处处非零；离散约束 `w = u_y` 的类比不是自动成立的。
4. **适定性障碍（已知否定性结果）**：连续常背景线性化给出
   `[σ + i(u₀+2a)k]² = k⁴ − (v₀+2λ)k³/ℓ`，`|Re σ| ~ k²`，
   即 Hadamard 意义下**不适定**。显式多孤子 tau 函数**不能**建立
   适定性 / 稳定性 / 收敛性。
5. **无文献新颖性检索**，故不主张新颖性。

---

## 6. 路线状态与证明覆盖度

| 项目 | 状态 | 标签 |
|---|---|---|
| 交错候选的有效性（有限 `N`） | 精确成立 | 实验验证 |
| 算子平移分解（任意 `N`） | Lean 完全形式化 | Lean 代数验证 |
| 交错方程 → mode 对条件的结构归约 | Lean 形式化 | Lean 结构验证 |
| 连续极限 `h→0` | 解析核对，未形式化 | Lean 分析验证（缺口） |
| 实性 / 无零点 / `w = u_y` | 未证明 | Lean 分析验证（缺口） |
| 矩阵元恒等式正确形式 + 旧形式反例 | Lean 形式化 | 数学证明，尚未完整形式化 |
| 任意 `N` | 归约到论文 Lemma 2.1，未形式化 | 数学证明，尚未完整形式化 |

**路线状态**：本路线**没有**被否证，但也**没有**完成。它在「有限 `N` 代数
核」层面已被完整坐实并形式化；在「任意 `N`」与「分析性质」两个层面存在
明确记录的缺口。

**证明覆盖度**：Lean 覆盖了代数核（平移分解、色散因子化、结构归约、
矩阵元恒等式修正）；**不**覆盖任意 `N`、连续极限、实性、无零点、约束、
适定性。

---

## 7. 下一步最有价值的一步

**把 `hpair` 从假设变成定理**：在 Lean 中对 16 个 mode 对穷尽展开
`Σ_μ Σ_ν f_μ g_ν (k_μ − k_ν) = 0`（配合 `kcoef_sub`、`wcoef_sub`、
`eigen_shift_split`），即可把 `two_soliton_eq1/2` 变成无条件定理。
本部署上 `fin_cases` 对复杂项替换行为不稳定，建议改用
`Finset.univ` 上的显式枚举引理 + `decide`，或把 16 个 mode 对写成
显式 `List` 后归纳。

---

## 8. 复现

```
python -u experiments/g6_pair_vanishing.py     # 16 mode 对 × 20 参数组，精确有理数
python -u experiments/g5_decisive.py           # 直接偏导残差 = 零多项式
python -u experiments/g3_mode_audit.py         # N = 1..5 × 4 参数组，2904 系数全零
python -u experiments/g6a_closed_form.py       # 闭式形式探索
python -u experiments/g6b_solve.py             # 符号求解，逐步分解
```

Lean：

```
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\G_hirota_backlund\proofs\DirG.lean' `
  -TimeoutSeconds 300
```

结果：exit code `0`，`PASSED: 1 local module(s).`
