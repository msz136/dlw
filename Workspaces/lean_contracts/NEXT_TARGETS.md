# 剩余目标作战计划（C07 / C08 / C09 / C16 / C22 / C23 / N01）

> 写于 2026-09-22，round 2。用途：context 被压缩后，这份文件就是耐久记忆。
> 当前状态 **23 / 32**，PASSED run `20260922_123007_8274bbe0`（`PASSED: 11 local module(s).`）。
> 所有目标陈述以 `Paper\dlw_semidiscrete\lean_contracts\Contracts.lean`（冻结，SHA-256 `e70876c5…8d656`）为唯一权威。
> **禁止修改任何目标陈述。**

---

## 0. 这一轮（round 2）已经移交的工作

`PkgC17.lean`、`PkgC18.lean` 已派给两个 agent（C17/C18 与已过的 C11 同族，都是 `PowBound 2` 的
「格点/离散算子 vs 连续算子」一致性）。本文件记录**其余**目标的路线，其中 C09 的路线本轮已经被我
手工打通到"只差一个经典引理"的地步（见 §3）。

---

## 1. C07 / C08 —— 任意 N 的 Gram 双线性恒等式

```
def C07 : Prop := ∀ (N : ℕ) (D : Data N) (h s : ℝ),
  Admissible D h → LayerOK D s → ∀ n j,
  bil s (tau D h s (n+1) j) (tau D h s n j)=0
def C08 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ),
  Admissible D h → SemiPair D.a h (F D h) (G D h)
```
其中 `F D h = tau D h (D.a-h/2) 1`、`G D h = tau D h D.a 0`，
`SemiPair a h F G := ∀ j, bil (a-h/2) (F j) (G j) = 0 ∧ bil (a+h/2) (F j) (G (j+1)) = 0`。

**已确认的事实**：C07 用 `fractions.Fraction`（无浮点）在 N=1..4、j=0..2、n=0..2、三组参数上
按实际指数向量合并检验，全部合并系数精确为 `Fraction(0)` → **命题为真**。脚本
`Workspaces\lean_contracts\audit_c07.py`。

**注意 C08 不是 C07 的实例**：C07 里两个 `tau` 用**同一个** `s`，而 C08 的两个壁用的是
`tau D h (a-h/2)` 与 `tau D h a`（不同 `s`）。所以 C08 必须独立证明。

### 关键结构（本轮新发现，务必先看这一条）

`entry` 的每一项都是**秩一结构**，这把手推变成初等代数：

```
gamma D s i k = -(D.p i - s)/(D.q k + s) = (-(D.p i - s)) * (D.q k + s)⁻¹        -- i 因子 × k 因子
chi   D h i k = lam h (D.p i - D.a) * lam h (D.q k + D.a)                        -- i 因子 × k 因子
exp((p_i+q_k)x + (q_k²-p_i²)t) = exp(p_i x - p_i² t) * exp(q_k x + q_k² t)       -- i 因子 × k 因子
```
所以，对固定 `(x,t)`，
```
entry D h s n j i k = δ_ik + A_i * B_k / (D.p i + D.q k)
A_i = D.rho i * (-(D.p i - s))^n * (lam h (D.p i - D.a))^j * Real.exp (D.p i * x - (D.p i)^2 * t)
B_k = (D.q k + s)^(-n) * (lam h (D.q k + D.a))^j * Real.exp (D.q k * x + (D.q k)^2 * t)
```
即 `Matrix (Fin N) (Fin N) ℝ = 1 + diag(A) · Cauchy · diag(B)`，其中 `Cauchy i k = 1/(p_i + q_k)`。

**这条路线的价值**：`tau = det(1 + diag(A)·K·diag(B))` 是**柯西矩阵的行列式**，
它是 Toda/离散 KP 的 τ 函数，双线性恒等式 `bil s τ_{n+1} τ_n = 0` 就是该 τ 函数的
Toda 双线性方程。经典证明链条：
1. `Matrix.det (1 + A*B) = Matrix.det (1 + B*A)`；
2. **Cauchy–Binet / 主子式展开**：`det (1 + M) = ∑_{S} det (M.submatrix S S)`；
3. **Desnanot–Jacobi（Jacobi 恒等式）**：把 `bil` 里的二阶导/二阶差分改写成余子式之比；
4. **指数线性无关**：`∑ C_{ik} e^{(p_i+q_k)x+(q_k²-p_i²)t} ≡ 0 ⟹ 所有 C_{ik}=0`
   （需要 `p+q` 的不同取值两两不同 —— 由 `Admissible` 的 `p_i+q_k ≠ 0` 与 `StrictMono` 支持）。

**Mathlib 支持情况（本轮实测）**：
- **没有** Cauchy 行列式公式（`grep -i cauchy` 在 `Mathlib\LinearAlgebra\Matrix\` 下无命中；
  只有 `Analysis\Complex\CauchyIntegral.lean` 等无关文件）。
- **没有** Desnanot–Jacobi / `jacobi` 任何命中（`Mathlib\LinearAlgebra\Matrix\**` 下 0 命中）。
- **有** 主子式展开的零件：`Mathlib\LinearAlgebra\Matrix\Charpoly\Coeff.lean`
  - `Matrix.coeff_det_one_add_X_smul_eq_sum_minors (M) (k)`：`det(1 + X • M.map C)` 的 k 次系数
    = 全部 k×k 主子式之和；
  - `Matrix.det_piecewise_one_eq_submatrix_det`：把 `s` 外的行换成单位行后行列式 = 主子式行列式；
  - `Matrix.det_eq_sign_charpoly_coeff`；
  - 但**没有**直接的 `det (1 + M) = ∑ s, det (M.submatrix s s)`，需要自己从上面两条 + 在 `X=1` 取值推。

**结论**：C07/C08 是研究级工程。**建议顺序：先做 C09（§3），因为它只需要"柯西主子式为正"这一条，
而 C07/C08 还需要额外的 Jacobi/Plücker 层。** 做完 C09 会顺带把柯西矩阵的行列式工具建起来，
C07/C08 可以直接复用。

---

## 2. C16 / C22 / C23 —— C08 的下游（不要先做）

```
def C16 : Prop := ∀ (N) (D : Data N) (h), PositiveData D h →
  NonlinearPair D.a h (physU (F D h) (G D h)) (physV h (F D h) (G D h))
def C22 : Prop := ∀ (N) (D : Data N) (h₀), PositiveData D h₀ →
  UniformBoxO2 (fun h => interpU h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0) - cu (tau0 D 1) (tau0 D 0)) ∧
  UniformBoxO2 (fun h => interpV h (tauI D h (D.a-h/2) 1 (1/2)) (tauI D h D.a 0 0) - cv (tau0 D 1) (tau0 D 0))
def C23 : Prop := ∀ (N) (D : Data N) (h₀), PositiveData D h₀ →
  ContinuousPair D.a (tau0 D 1) (tau0 D 0)
```
- **C16** = C08 的最后一步：`PkgNonlinear.lean` 的 `c15_proved : C15` 已经给出
  `SemiPair a h F G → NonlinearPair a h (physU F G) (physV h F G)`，所以
  **`c16_proved := fun N D h hPD => c15_proved D.a h (F D h) (G D h) (ne_of_gt hPD.1) …
  (smoothL_of_positiveData …) (positiveL_of_positiveData …) (c08_proved N D h hPD.2.…)`**
  —— 一旦 C08 与 C09 到位，C16 几乎只是接线。**先决：C08 + C09。**
- **C22** = C17（本轮在做）的**一致盒**版本叠在 C16 的 τ 上。注意 `UniformBoxO2` 比 `PowBound`
  强得多（要求对 `|x|,|y|,|t| ≤ R` **一致**的常数，且 `0<h` 单侧）。所以 C17 过了也不等于 C22 过了；
  C22 还需要把 C17 的逐点估计升级成盒上一致的估计，并处理 `tauI`/`tau0` 的具体场。
- **C23** 是 C08 的**连续**版本（用 `tau0` 而不是 `tau D h`，用 `ContinuousPair` 而不是 `SemiPair`）。
  `tau0` 里 `exp(... + y*(1/(p_i-D.a)+1/(D.q k+D.a)))` —— 也是 `i` 因子 × `k` 因子，所以同样是
  柯西型 τ 函数，路线与 C08 相同。

---

## 3. C09 —— 本轮已打通路线，**只差一个经典引理**

```
def C09 : Prop := ∀ (N : ℕ) (D : Data N) (h : ℝ), PositiveData D h →
  Admissible D h ∧ PositiveL (F D h) ∧ PositiveL (G D h) ∧
  SmoothL (F D h) ∧ SmoothL (G D h)
```

### 3.1 容易的部分（先做完，可以独立 PASSED）

- **`Admissible D h`**：`0<h` 给出 `h≠0`。`p_i+q_k>0` 直接由 `0<p_i, 0<q_k`。
  `p_i - a ± h/2 ≠ 0`：由 `p_i < a - h/2` 得 `p_i - a + h/2 < 0` 且 `p_i - a - h/2 < -h < 0`。
  `q_k + a ± h/2 ≠ 0`：`q_k>0`，且由 `0<p_i<a-h/2` 与 `0<h` 得 `a > h/2 > 0`，故 `q_k+a±h/2 > 0`。
- **`SmoothL (F D h)` / `SmoothL (G D h)`**：`entry` 只含 `exp`（与线性函数的复合）、常数、
  以及 `if i=k then 1 else 0`；`Matrix.det` 对每个元素是多项式。
  路线：`Matrix.det_apply`（按 `Equiv.Perm` 求和）→ `ContDiff.sum` / `ContDiff.prod` /
  `ContDiff.const_mul` / `Real.contDiff_exp.comp`（用 `ContDiff.comp` 与 `contDiff_fst` 等）。
  `gamma^n`、`chi^j` 对 `(x,t)` 是**常数**（n,j : ℤ 的幂，不依赖 x,t），只需先证明它们的
  可微性平凡（`contDiff_const`）。**注意**：`Real.exp` 的自变量是
  `(p_i+q_k)*x + (q_k²-p_i²)*t` 与 `tau0` 里多出的 `y*(...)`，都是 `(x,t)`（或 `(x,y,t)`）的线性函数。

### 3.2 `PositiveL` —— 全部归结为一条引理

对**任意** `s`（`s = D.a` 或 `s = D.a - h/2`）、**任意** `n j : ℤ`、固定 `(x,t)`，
由 §1 的秩一分解：
```
entry D h s n j i k = δ_ik + A_i B_k / (D.p i + D.q k)
```
**`PositiveData` 保证 `A_i B_k > 0` 对所有 i,k**（因此取 k=i 得 `c_i := A_i B_i > 0`）：
- `gamma D s i k > 0`：`s = a - h/2` 时 `p_i - a + h/2 < 0`（分子取负号后为正）、`q_k + a - h/2 > 0`；
  `s = a` 时 `p_i - a < 0`、`q_k + a > 0`。
- `chi D h i k > 0`：`(p_i-a+h/2)/(p_i-a-h/2)` 分子分母同为负；`(q_k+a+h/2)/(q_k+a-h/2)` 同为正。
- `Real.exp > 0`、`D.rho i > 0`、幂 `zpow` 保号。
（`(x*y)^j = x^j*y^j`（`mul_zpow`）+ `LayerOK` 保证 `q_k+s ≠ 0`。）

于是
```
Matrix.det (fun i k => entry D h s n j i k x t) = Matrix.det (1 + diag A * K * diag B)
```
其中 `K i k = (D.p i + D.q k)⁻¹`，且
```
Matrix.det (1 + diag A * K * diag B) = Matrix.det (1 + K * diag c),  c i = A i * B i > 0
```
（用 `Matrix.det_mul` + `det_one_add_mul_comm` 型引理；若 Mathlib 没有现成的，就写
`1 + diag A * K * diag B = diag A * (1 + K * diag B * diag A) * (diag A)⁻¹` 再用 `det_mul` 消掉，
或直接 `Matrix.det_apply` 展开 —— 但**优先找现成引理**，`Matrix.det_one_add_mul_comm` 之类很可能存在，先 grep）。

然后
```
det (1 + K * diag c) = ∑_{S : Finset (Fin N)} det ((K * diag c).submatrix S S)
                     = ∑_{S} det (K.submatrix S S) * ∏_{i ∈ S} c i
```
第一条是 **主子式展开**（从 Mathlib 的
`Matrix.coeff_det_one_add_X_smul_eq_sum_minors` 在 `X = 1` 取值推出 —— 见 §1 最后一段），
第二条用 `(K * diag c).submatrix S S = (K.submatrix S S) * (diag c).submatrix S S` 与 `Matrix.det_mul`、
`Matrix.det_diagonal`。

**于是 `PositiveL` 归结为唯一一条待证引理**：
```
lemma cauchy_principal_minor_pos {m : ℕ} (p q : Fin m → ℝ)
    (hp : StrictMono p) (hq : StrictMono q) (hp0 : ∀ i, 0 < p i) (hq0 : ∀ i, 0 < q i)
    (S : Finset (Fin m)) :
    0 < (K.submatrix (Subtype.val : S → Fin m) (Subtype.val : S → Fin m)).det
  where K i k = (p i + q k)⁻¹
```

### 3.3 上面那条引理的证明（我已手推完递推，逐步核对过）

对 `S` 按基数的归纳。记 `S = {i_1 < i_2 < … < i_M}`，`i_0 := i_1`（最小元）。消元四步：

1. 行变换 `row i ← row i − row i_0`（`i ≠ i_0`）：`1/(p_i+q_k) − 1/(p_{i_0}+q_k) = (p_{i_0}−p_i)/((p_i+q_k)(p_{i_0}+q_k))`，`det` 不变。
2. 从第 `i` 行提出 `(p_{i_0}−p_i)`；从第 `k` 列提出 `1/(p_{i_0}+q_k)`。
3. 列变换 `col k ← col k − col k_0`（`k ≠ k_0`，`k_0 := i_0` 那一列）：此时第 `i_0` 行全为 `1`，
   故第 `i_0` 行在 `k ≠ k_0` 处归零；其余行给出 `(q_{k_0}−q_k)/((p_i+q_k)(p_i+q_{k_0}))`。
4. 从第 `k` 列提出 `(q_{k_0}−q_k)`；从第 `i` 行提出 `1/(p_i+q_{k_0})`；最后按第 `i_0` 行展开
   （该行只剩 (i_0,k_0) 位置为 1，其余为 0）。

得到**精确递推**：
```
det K_SS = [ ∏_{i∈S,i≠i_0} (p_{i_0} − p_i) · ∏_{k∈S,k≠k_0} (q_{k_0} − q_k) ]
         / [ (p_{i_0}+q_{k_0}) · ∏_{i∈S,i≠i_0} (p_i + q_{k_0}) · ∏_{k∈S,k≠k_0} (p_{i_0} + q_k) ]
         · det K_{S∖{i_0}, S∖{i_0}}
```
**符号**：`StrictMono` 且 `i ≠ i_0` 时 `p_{i_0} − p_i < 0`（因为 `i_0` 最小），故 `∏_{i}(p_{i_0}−p_i)`
有 `M−1` 个负因子，符号 `(−1)^{M−1}`；`q` 同理再乘 `(−1)^{M−1}`；合计 `(+1)`。分母全正。
故 `sign(det K_SS) = sign(det K_{S∖{i_0}})`，归纳到 `M=1`（`1/(p+q) > 0`）得 **`det K_SS > 0`** ✓。

**形式化提示**：这是"经典柯西行列式"的标准归纳。**四步消元所需的 Mathlib 引理我已经逐条查证存在**
（`Mathlib\LinearAlgebra\Matrix\Basic.lean`）：
| 步骤 | 引理 | 位置 |
|---|---|---|
| 行 `i ← row i − row i_0` | `Matrix.det_updateRow_add_smul_self (A) (hij : i ≠ j) (c : R)`，取 `c = -1` | `Basic.lean:473` |
| 从行提出标量 | `Matrix.det_updateRow_smul_left (M) (j) (s) (u)` | `Basic.lean:406` |
| 列 `k ← col k − col k_0` | `Matrix.det_updateCol_add_smul_self (A) (hij) (c)`，取 `c = -1` | `Basic.lean:478` |
| 从列提出标量 | `Matrix.det_updateCol_smul_left (M) (j) (s) (u)` | `Basic.lean:410` |
（另有 `det_updateRow_add`、`det_updateRow_smul`、`det_updateCol_add`、`det_updateCol_smul`、
`det_updateRow_sum`、`det_updateCol_sum` 备用。）

**`det(I + diag A · K · diag B) = det(I + K · diag c)`（`c i = A i * B i`）也有现成的**：
`Matrix.det_one_add_mul_comm (A : Matrix m n α) (B : Matrix n m α) : det (1 + A * B) = det (1 + B * A)`
（Weinstein–Aronszajn 恒等式，`Mathlib\LinearAlgebra\Matrix\SchurComplement.lean:401`）。
取 `A = Matrix.diagonal A_vec`、`B = K * Matrix.diagonal B_vec` 即可，`B * A = K * diagonal c`
（`Matrix.diagonal_mul_diagonal`）。

也可以直接陈述**闭式**再归纳（`∏_{i<i'}(p_i−p_{i'})∏_{k<k'}(q_k−q_{k'})/∏_{i,k}(p_i+q_k)`）。
只要最终拿到 `0 < det K_SS`，走哪条都行。**注意 `S` 上的下标顺序**：用 `Finset.orderIsoOfFin`
把 `S` 换成 `Fin M` 时，"按大小排序"这个置换会带符号 —— **建议直接对"给定严格递增的
`v : Fin M → Fin m`（`StrictMono v`）"陈述引理**，`S = Finset.univ.image v`，避免置换符号问题。

### 3.4 顺序建议
1. 先独立证 `Admissible` 与 `SmoothL`（都可以立即 PASSED，价值确定）。
2. 再证 `cauchy_principal_minor_pos`（这是全部难度所在）。
3. 最后拼 `PositiveL` 与整个 `C09`。
**若第 2 步做不完**：把第 1 步的成果单独交付（`PkgC09.lean` 里保留 `c09_admissible_proved`、
`c09_smooth_proved` 等公开引理），**不要**声称 `c09_proved`。

---

## 4. N01 —— RK4 那一项（`PowBound 5`）

`PkgNumeric.lean` 已有 `n01_euler_part`（`PowBound 2`）与 `n01_trapezoid_part`（`PowBound 3`），
假设与 N01 原文完全一致且已过。缺的是
```
PowBound 5 (fun h => ‖z (t+h) - rk4 f t h (z t)‖)
```
已归约成一条已类型检查的命题 `n01_rk4_of_taylor_poly`（经典 RK4 阶条件：
`Σ b_i = 1`、`Σ b_i c_i = 1/2`、`Σ b_i c_i² = 1/3`、`Σ b_ij a_ij = 1/6` 等）。
补上那条代数条件即可得到 `n01_proved`。**相对便宜，值得做。**

---

## 5. 优先级建议（按"可达性 × 价值"）

1. **C17、C18**（round 2 已派工）—— 与已过的 C11 同族。
2. **C09**（§3）—— 路线已完全打通，只差柯西主子式为正这一条经典引理；且做完后
   C07/C08 能复用工具。
3. **N01** —— 只差 RK4 阶条件的代数验证。
4. **C16** —— C08 + C09 到位后基本是接线（用 `c15_proved`）。
5. **C23** —— 与 C08 同路线（连续版）。
6. **C22** —— C17 + C16 + 一致盒升级，最难。
7. **C07 / C08** —— 需要柯西工具 + Jacobi/Plücker + 指数线性无关，研究级。

**诚实边界**：C16/C22/C23/C07/C08 全部卡在同一块「任意 N 的实际 Gram 双线性恒等式」上；
在 C09 的柯西工具建成之前，不要声称它们"只差接线"。
