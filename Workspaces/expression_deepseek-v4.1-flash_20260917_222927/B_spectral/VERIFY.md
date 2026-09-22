# VERIFY.md — 方向 B 验证记录（真实命令 / 真实退出码 / 真实输出行）

工作根：`C:\Users\msz\学术内容`
方向目录：`C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\B_spectral\`

未修改 `_lean_shared`、`lean-toda`、`common\SHARED_MATH_SPEC.md`、顶层 `proofs\` 或任何 sibling 方向目录。
本方向所有写入均在其自身目录 `B_spectral\` 内。未使用任何被禁命令（无 `lake`、无 `elan install`、
无 Mathlib 克隆/重编译、无 `pip`/`npm`、未创建 Lake 工程）。

---

## 1. Lean 验证（唯一允许入口）

### 命令

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\B_spectral\proofs' `
  -File 'C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\B_spectral\proofs\DirB.lean' `
  -TimeoutSeconds 600
```

文件内无 `sorry`、无 `admit`、无新增 `axiom`。工具链：`leanprover/lean4:v4.34.0`，
Mathlib commit `5ed2965256430c3649e86755f9576b54eca72435`（见最终 run 的 `result.json`）。

### 迭代过程中的失败运行（如实记录）

**失败 1 — `Spectral\Growth.lean:74:2: error: No goals to be solved`**
（run `20260917_234031_ca829f1e`，`LEAN_CHECK_FAILED: Spectral\Growth.lean.`，退出码 1）
原因：`dispersion_relation` 末尾 `rw [hX]; field_simp; ring` 中 `field_simp` 已关闭目标，`ring` 无目标可解。
修正：删除多余的 `ring`。

**失败 2 — `Spectral\Aliasing.lean:53:42: error: Tactic 'rewrite' failed: Did not find an occurrence of the pattern ζ ^ M`**
（run `20260917_234207_42d27739`，退出码 1；目标形如 `(ζ ^ l) ^ j * (ζ ^ (M * t)) ^ j = (ζ ^ l) ^ j`）
原因：`rw [add_mul, pow_add, pow_mul, pow_mul, hζ.pow_eq_one]` 中第二个 `pow_mul` 无法作用于
外层已带指数 `^ j` 的 `ζ ^ (M * t)`。
修正：先单独证明 `ζ ^ ((M * t) * j) = 1`（`show (M*t)*j = M*(t*j)` + `pow_mul` + `hζ.pow_eq_one` + `one_pow`），
再 `rw [add_mul, pow_add, hzero, mul_one]`。

**失败 3 — `Spectral\Growth.lean:227:8: error(lean.unknownIdentifier): Unknown identifier 'div_le_div_iff'`**
（run `20260917_234813_89aea708`，退出码 1）
原因：新增的单侧稳定阈值证明使用了 Mathlib 中不存在的引理名。
修正：改用实际存在的 `div_le_div_iff_of_pos_left (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) : a / b ≤ a / c ↔ c ≤ b`
（`Mathlib/Algebra/Order/GroupWithZero/Basic.lean:1261`），即
`(div_le_div_iff_of_pos_left hc hNr hl).mpr (by exact_mod_cast hlN)`。

**较早的失败**：`Spectral\Growth.lean` 中 `modeIdx` 未定义（缺 `import Spectral.Multiplier`）、
`linear_combination` 无法在自由交换环中完成 `i² = −1` 的代换（残留 `Complex.I ^ 2`、`Complex.I ^ 3` 项）
（run `20260917_234031_ca829f1e` 之前）。修正：`import Spectral.Multiplier`；并新增引理 `I_factor`
`i ℓ s − A k ℓ = i ℓ (s + i A k)`（内部用 `1 + I^2 = 0` 证明），在 `linear_combination` 中作为**额外假设项**
传入，使校验重新成为自由交换环恒等式。

### 中间通过运行

```
CHECK Spectral\Multiplier.lean
... (仅 warning：if_neg 弃用、simpa/unusedVariables)
CHECK Spectral\Growth.lean
CHECK Spectral\Aliasing.lean
CHECK Common\Operators.lean
CHECK DirB.lean
...
PASSED: 5 local module(s).
REPORT: C:\Users\msz\学术内容\...\proofs\.lean-runs\20260917_234402_5405af8b\result.json
```
（run `20260917_234402_5405af8b`，退出码 0 —— 首次全绿，但当时尚无单侧阈值与 `N`-一致不稳定定理。）

### 最终通过运行（本方向最终文件状态）

run id：`20260918_000017_481edb1e`，**退出码 0**。

（此前还有一次全绿运行 `20260917_235557_54694482`，退出码 0；其后的唯一改动是 `DirB.lean`
头部注释中的交叉引用与一条 headline 摘要（纯注释，无证明改动），因此重新完整验证了一次，
下表与上文输出均取自 `20260918_000017_481edb1e`。命令输出在两次运行中逐字相同，
仅 `REPORT` 行中的 run id 不同。）

```
CHECK Spectral\Multiplier.lean
... (warning only)
CHECK Spectral\Growth.lean
CHECK Spectral\Aliasing.lean
CHECK Common\Operators.lean
CHECK DirB.lean
@Common.ctr_kernel : ∀ {K : Type} [inst : Field K] (w : ℤ → K) (h : K),
  (∀ (j : ℤ), w (j + 1) = w (j - 1)) → Common.ctr w h = fun x => 0
@Common.ctr_const : ∀ {K : Type} [inst : Field K] (c h : K), Common.ctr (fun x => c) h = fun x => 0
@Common.sbp_fwd : ∀ {K : Type} [inst : Field K] (u v : ℕ → K) (h : K),
  h ≠ 0 → ∀ (N : ℕ), (∑ j ∈ Finset.range N, (u (j + 1) - u j) / h * v j) * h +
    (∑ j ∈ Finset.range N, u (j + 1) * ((v (j + 1) - v j) / h)) * h = u N * v N - u 0 * v 0
'DLW.Spectral.mult_eq_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.kernel_eq_zero_mode_line' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.invMult_mult' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.mult_invMult' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.mult_comp_modeProj' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.modeProj_comp_mult' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.dispersion_relation' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.nontrivial_dispersion_relation' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.mode_of_dispersion_relation' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.growth_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.exists_growing_mode' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.mode_of_nonneg_discriminant' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.neutral_mode_of_negative_discriminant' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.band_stability_threshold' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.band_instability_threshold' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.band_unstable_uniform_in_N' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.band_contains_growing_mode' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.sample_alias' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.out_of_band_folds_into_band' depends on axioms: [propext, Quot.sound]
'DLW.Spectral.three_point_collision' depends on axioms: [propext, Classical.choice, Quot.sound]
'DLW.Spectral.aliasing_breaks_projected_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
PASSED: 5 local module(s).
REPORT: C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\B_spectral\proofs\.lean-runs\20260918_000017_481edb1e\result.json
```

**成功判据满足**：退出码 `0` **且** 输出含 `PASSED`。

`result.json` 机器可读记录（节选）：

```json
{ "run_id": "20260918_000017_481edb1e",
  "toolchain": "leanprover/lean4:v4.34.0",
  "mathlib_commit": "5ed2965256430c3649e86755f9576b54eca72435",
  "status": "PASSED",
  "files": [
    {"file": "...\\Spectral\\Multiplier.lean", "exit_code": 0, "passed": true, "sha256": "e09ae50973154ae5c8416cd42a179d780a2da22b4ff766c9fc2a4f227d9ea113"},
    {"file": "...\\Spectral\\Growth.lean",     "exit_code": 0, "passed": true, "sha256": "54ebcf0c9880f4212f2cd36abed21611c2ea48436b0d2909bc9f80123a86c05d"},
    {"file": "...\\Spectral\\Aliasing.lean",   "exit_code": 0, "passed": true, "sha256": "fb8119e53394ff517331e744852f570693250e2bdac6c6362b6058a2d09c0ddf"},
    {"file": "...\\Common\\Operators.lean",    "exit_code": 0, "passed": true, "sha256": "5eb6b6b746c068c38e3ac565886643b42e4a3fd637c663291c76f0d31aa0b954"},
    {"file": "...\\DirB.lean",                "exit_code": 0, "passed": true, "sha256": "9e135c70cf366ac57a299bce9b806ae51cd3f46f217f635d0028984c4caa894c"}
  ],
  "limitation": "Compiler success does not audit theorem assumptions or establish research claims." }
```

公理检查：21 条 headline 定理全部只依赖 `propext, Classical.choice, Quot.sound`（标准基础），
**无 `sorryAx`**、无新增公理。`out_of_band_folds_into_band` 只依赖 `propext, Quot.sound`（`omega` 生成，
更强）。`Common.Operators` 的三条共享定理被 `#check`（非本方向所证，仅引用）。

### 文件与定理

| 文件 | 内容 |
|---|---|
| `proofs/Spectral/Multiplier.lean` | `modeIdx`/`zeroIdx` 及其单射性；`multLin`（对角乘子）与 `mult_eq_zero_iff`、`kernel_eq_zero_mode_line`；`zeroMean` 与 `invMultLin`、`invMult_mult`、`mult_invMult`；`modeProj` 与 `mult_comp_modeProj`、`modeProj_comp_mult`、`mult_modeProj_zero`、`mean_mult` |
| `proofs/Spectral/Growth.lean` | `I_factor`；`dispersion_relation`、`nontrivial_dispersion_relation`、`mode_of_dispersion_relation`；`discriminant_nonneg`、`sqrt_growth_lower_bound`、`growth_lower_bound`、`mode_of_nonneg_discriminant`、`exists_growing_mode`、`I_mul_sq`、`neutral_mode_of_negative_discriminant`；`band_stability_threshold`、`band_instability_threshold`；`mode_one_mem_band`、`mode_neg_one_mem_band`、`band_unstable_uniform_in_N`、`band_contains_growing_mode` |
| `proofs/Spectral/Aliasing.lean` | `sample_alias`、`out_of_band_folds_into_band`；`omega3`/`omega3_primitive`/`omega3_cube`/`three_point_collision`/`alias_offset`；`I_pow_four/three/six/nine`；`three_point_sum`、`four_point_sum`、`aliasing_breaks_projected_identity` |
| `proofs/DirB.lean` | 汇总模块：`import` 上述模块 + `Common.Operators`，`#check` 共享定理，21 行 `#print axioms` |
| `proofs/Common/Operators.lean` | **共享模块，未修改**（只读引用 `Common.ctr_kernel`、`ctr_const`、`sbp_fwd`、`telescoping`、`sbp_fwd_undivided`、`sum_range_ctr`、`fwd`/`bwd`/`ctr`/`ctr2`、`ctr_kernel`） |

说明：早期用于探查 Mathlib API 的临时文件 `proofs/Probe.lean` 已删除（其问题已由
`Spectral/Multiplier.lean` 覆盖）；它从未被 `DirB.lean` 引用，也不在最终验证的 5 个模块中。

遗留 warning（**不影响通过**，仅出现在 `Multiplier.lean`）：`if_neg` 弃用提示 ×6、
`simpa`→`simp` 建议 ×2、`ha` 未显式引用 ×2。已确认构建以退出码 0 通过。

---

## 2. 实验（Python 3.13 + SymPy，精确有理/符号）

### 一行运行命令

```
python -u "C:\Users\msz\学术内容\Workspaces\expression_deepseek-v4.1-flash_20260917_222927\B_spectral\experiments\spectral_diagnostic.py"
```

最终运行退出码 **0**，输出 **61/61 checks passed**、`RESULT: OK`，完整输出已保存为
`experiments/run_log.txt`（153 行），机器可读摘要为 `experiments/spectral_diagnostic_summary.json`。

### 首次运行的失败（如实记录，且**驱动了一次数学更正**）

首轮为 **55/60 通过、退出码 1**。5 处失败中 4 处是**校验式本身写错**：
`Sec1` 的 `ℓ=0` 检查未先代入 `V = 0`；`Sec2` 的反对称检查只取了 `u u_xy` 一半（正确的抵消出现在
`u u_xy + u_x u_y` 之和上，而该项已被"`(1)` 的 `ℓ=0` 恰为 `∂_x²v̂_0`"覆盖）；`Sec4` 的符号样本表把
`kℓ < 0`（**永远不稳定**）误标为中性；`Sec5` 的阈值锋利性用随机系数作见证，`N = 6` 时恰好无污染。

**第 5 处是真正的数学更正**：原检查断言"截断 `N` 的稳定 `k`-带恰为 `0 < k ≤ c/N`"，
实测 `k* = 0`。原因是全带中 `ℓ = −sgn(k)` 的模对**任意** `k ≠ 0` 都不稳定
（`R = k⁴ + ck³/|ℓ| > 0`），故全带根本没有稳定区间；原断言只对**单侧扇区** `ℓ ≥ 1` 成立。
据此我们：
1. 把实验改为两个分开的命题（全带 = `N`-一致不稳定；单侧扇区 = 阈值 `c/N`）；
2. 在 Lean 中**新增** `mode_neg_one_mem_band` 与 `band_unstable_uniform_in_N`
   （`N`-一致不稳定，`Re σ = √(k⁴+ck³) ≥ k²`，陈述中不含 `N`），并把
   `band_stability_threshold` 的文档明确限定为**单侧**扇区。

### 关键输出（原文摘录）

```
Sec 1  exact linearisation and the dispersion relation
PASS  Sec1 linearised (1) equals (i l s)U - k^2 V - (u0+2a)k l U
PASS  Sec1 linearised (2) equals (s+i(u0+2a)k)V + i(v0+2 lam)kU - i k^2 l U
PASS  Sec1 elimination of V gives (s+i(u0+2a)k)^2 = k^4 - (v0+2 lam)k^3/l   | residual = 0
PASS  Sec1 l=0: (1L) forces V = 0
PASS  Sec1 l=0: (2L) with V = 0 forces (v0+2 lam) U = 0   | (2L)|l=0 with V=0 is I*U*k*(2*lam + v0)

Sec 2  the l = 0 sector of the nonlinear system (exact Fourier computation)
PASS  Sec2 l=0 of (1) is exactly d_x^2 v_0 (no u_0, no nonlinearity)   | residual = 0
PASS  Sec2 l=0 of (2) is d_t v_0 + d_x[<uv> + 2a v_0 + 2 lam u_0]   | residual = 0
PASS  Sec2 the quadratic pair u u_xy + u_x u_y contributes zero to l=0 (antisymmetry)   | residual = 0
PASS  Sec2 (V7) v = -2 lam, u = U(x,t) arbitrary solves (1) exactly (all l)
PASS  Sec2 (V7) same family solves (2) exactly (all l)
PASS  Sec3 truncated (N=1) l=0 identities hold exactly        (N=2,3 同)

Sec 4  exact sign analysis: stable x-band is 0 < sgn(l) k < c/|l|
PASS  Sec4 l * disc factors as k^3 (k l - c)   | l*disc = k**3*(-c + k*l)
PASS  Sec4 sign(disc) matches the predicted neutral/unstable regions (c=1)
PASS  Sec4 neutral region 0 < sgn(l) k < c/|l| has disc <= 0

Sec 5  aliasing quantified (exact, no floating point)
PASS  Sec5 root-of-unity filter: sum_j w^{tj} = M if M|t else 0 (M=3/4/5)
PASS  Sec5 N=1: mode -1 of (top mode)^2 is 0 exactly, 0 under 3-point collocation   (N=2..8 同)
PASS  Sec5 N=8, M=2N+1: aliasing contaminates the nonzero modes, never l=0   | contaminated modes: [-8,...,-1,2,...,8]
PASS  Sec5 N=1..8, M=3N+1: collocation reproduces the exact Galerkin coefficients
PASS  Sec5 N=1..8, M=3N: the top mode still aliases onto mode -N (threshold is sharp at M >= 3N+1)
PASS  Sec5 the alias error is O(1) in the data: corrupted coefficient 1 vs exact 0 (amplitude 1)

Sec 6  spectral diagnostic: finite-band growth vs continuous growth
  (a) max over the retained band |l| <= N of Re sigma, c = 1
         k | N=1      N=2      N=4      N=8      N=16     N=32     | sqrt(k^4+c k^3)
      0.25 | 0.1398   0.1398   0.1398   0.1398   0.1398   0.1398   |     0.1398
      1.00 | 1.4142   1.4142   1.4142   1.4142   1.4142   1.4142   |     1.4142
     64.00 | 4127.8760 ... 4127.8760 |  4127.8760
PASS  Sec6 (a) every truncation N >= 1 is unstable at EVERY k > 0 (the mode l = -1 is retained in every band)
PASS  Sec6 (a) the band maximum is attained at l = -1 and is completely independent of the truncation N
  (b) ratio max Re sigma / k^2 : k=16 -> 1.0308, k=32 -> 1.0155, k=64 -> 1.0078 (every N)
PASS  Sec6 (b) the finite-band growth shows the same k^2 rate ... uniformly in N
  (c) ONE-SIDED sector l >= 1 only: threshold in k is c/N
    N= 1 : measured k* = 1.00000 , c/N = 1.00000
    N= 2 : measured k* = 0.50000 , c/N = 0.50000
    N= 8 : measured k* = 0.12490 , c/N = 0.12500
    N=16 : measured k* = 0.06250 , c/N = 0.06250
PASS  Sec6 (c) the positive-ell modes are neutral exactly for k <= c/N ...
  (d) fixed k = 1, l -> 0^- :  l=-1e-1 -> 3.3166 ; -1e-3 -> 31.6386 ; -1e-6 -> 1000.0005 (asymptote 1000)
PASS  Sec6 (d) for fixed k the CONTINUOUS growth is unbounded as l -> 0^- ...
PASS  Sec6 (d) hence the y-truncation regularises the l -> 0 direction but NOT the k -> infinity direction

Sec 7  centred-difference kernel on Z/M
     M |  nullity | expected
     3 |        1 | 1        (M=4:2, 5:1, 6:2, 7:1, 8:2, 9:1, 10:2)
PASS  Sec7 odd M (in particular M = 2N+1) gives a ONE-dimensional kernel, even M gives a spurious second zero mode

summary
61/61 checks passed
RESULT: OK
wrote ...\experiments\spectral_diagnostic_summary.json
```

**成功判据**：退出码 `0` **且** 输出含 `RESULT: OK`。所有 `Sec 5` 的系数比较均为精确整数/有理算术
（无浮点），`Sec 1–4` 为 SymPy 符号精确，`Sec 6–7` 的浮点仅用于数值诊断（阈值扫描容差 `2e-3`）。

解读：
* `Sec 5` 的 `M = 2N+1` 情形中，**被污染的模集合精确等于理论预测**
  （`N=1: {−1}`；`N=2: {±1,±2}`；…），且 `ℓ = 0` 永不出现 —— 与`结论 29` 一致。
* `Sec 6(a)` 的每一列在 `N = 1..32` 上**逐位相同**，即 `N`-无关性；`(d)` 表明连续符号在 `ℓ → 0⁻` 无界。

---

## 3. 未做的事（防止误读）

* **没有**任何非线性或长时间行为的结论：本方向全部是线性化层面 + 单步非线性求值层面。
* **没有**形式化谱投影误差界 `‖u − P_N u‖ ≲ N^{−s}`，也**没有**形式化 `N → ∞` 的收敛定理。
* **没有**形式化"带内最大值上界 `G(k,N) ≤ √(k⁴+ck³)`"（Lean 只给下界与 `ℓ = −1` 的精确值）。
* **没有**形式化一般 `N` 的混淆反例族（Lean 给一般恒等式 + 一般算术 + `N = 1` 显式反例；一般 `N` 由实验覆盖）。
* **没有**处理 `x`-方向的离散化或有限区间；`x` 连续，`k ∈ ℝ`。
* **没有**给出 Chebyshev 情形的定量结论（仅在 `report.md` §5 作可行性讨论）。
* **不主张**消除 Hadamard 不适定：`report.md` §8 与 `CONCLUSIONS.md` 结论 20/23 明确说明
  `y`-截断只正则化 `ℓ → 0` 方向，`|Re σ| ~ k²` 在每个固定截断上依旧成立且与 `N` 无关。
* **没有**做独立文献检索，**不主张**新颖性。
