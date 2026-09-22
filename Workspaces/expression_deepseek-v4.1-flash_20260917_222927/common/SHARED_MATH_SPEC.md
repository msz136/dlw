# SHARED MATH SPEC — DLW `y`-discretisation programme

Run: `expression_deepseek-v4.1-flash_20260917_222927`
Owner of this file: **main agent**. Subagents may READ it, must NOT edit it.
Send corrections to the main agent instead of silently diverging.

Every statement below marked **[MAIN-VERIFIED]** was re-derived from scratch by the
main agent with `python -u common/MAIN_verify_core.py` (SymPy, exact rational /
symbolic) and cross-checked against the published PDF text in `pdftext/PhysD.txt`.
Do not treat anything else as established.

---

## 1. Source and exact transcription

Source: H.-H. Sheng, G.-F. Yu, *Physica D* **432** (2022) 133140,
DOI `10.1016/j.physd.2021.133140`. Local copy `PhysD-published.pdf`,
extracted text `pdftext/PhysD.txt`.

Equations as printed (page 2 of the PDF; `pdftext/PhysD.txt` lines 81–82):

```
(1)  u_yt + v_xx + u u_xy + u_x u_y + 2a u_xy = 0
(2)  v_t + (u v)_x + u_xxy + 2a v_x + 2 lam u_x = 0
```

`a`, `lam` arbitrary constants. The paper notes that `x -> x - 2at` maps (1)–(2)
onto the `a = 0` system (3)–(4). **We first round use `lam = -2`, `a` arbitrary.**

Variable transformation (eq. (5)):

```
u = 2 (ln(f/g))_x ,        v = 2 (ln(f g))_xy
```

With `D` the Hirota bilinear operator (eq. (8)), and

```
B = D_x^2 + D_t + 2a D_x
```

the bilinear system is (eqs. (6)–(7)):

```
(6)  [D_y B + 2 lam D_x] f . g = 0
(7)  B f . g = 0
```

Chain to the modified-KP hierarchy: eq. (9) is
`(D_{x_{-1}} (D_{x_1}^2 - D_{x_2} + 2a D_{x_1}) - 4 D_{x_1}) tau_{n+1} . tau_n = 0`
and eq. (10) is `(D_{x_1}^2 - D_{x_2} + 2a D_{x_1}) tau_{n+1} . tau_n = 0`, with
`x_{-1} = y`, `x_1 = x`, `x_2 = -t`.

> **Main-agent note (verified by consistency).** Eq. (9) must be read as
> `D_{x_{-1}}(...)`, **not** `D_{x_{-1}}^{-1}(...)`. Reason: if it carried the inverse,
> then with (10) one would get `D_x tau_{n+1} . tau_n = 0`, which fails for the
> paper's own `N = 1` tau pair (`D_x tau_1 . tau_0 = (rho-1) A E` depends on `y`).
> With `D_{x_{-1}}(...)` eq. (9) becomes exactly (6) at `lam = -2`, which is what
> the paper asserts. The layout extraction `pdftext/PhysD.txt` line 136 is
> consistent with this reading.

Gram determinant data (eqs. (11)–(15)):

```
m_ij^{(n)} = c_j delta_ij + (1/(p_i+q_j)) ( -(p_i-a)/(q_j+a) )^n exp(xi_i + eta_j)
xi_i  = p_i x - p_i^2 t + y/(p_i - a) + xi_i0
eta_j = q_j x + q_j^2 t + y/(q_j + a) + eta_j0
f = tau_{n+1},  g = tau_n
```

**[MAIN-VERIFIED — V4]** For `a = 2`, `lam = -2`, `N = 1, 2, 3` with generic
parameters: `tau_n` satisfies (6) and (7); and the induced `(u, v)` from (5)
satisfies (1) and (2) exactly.

### 1.1 Nonlinear rewrite used throughout

With `w = u_y`:

**[MAIN-VERIFIED — V5]**

```
(1)  <=>   w_t + d_x[ v_x + (u + 2a) w ] = 0
(2)  <=>   v_t + d_x[ (u + 2a) v + w_x + 2 lam u ] = 0
```

Both are **exact identities**, coefficient for coefficient. The constraint
`w = u_y` and its kernel are the central difficulty of every `y`-discretisation.

---

## 2. Continuous linearisation: the standing obstruction

**[MAIN-VERIFIED — V6]** Linearise (1)–(2) about the constant background
`(u_0, v_0)` with a mode `exp(sigma t + i(k x + ell y))`. The first equation
eliminates `v_hat`; substituting into the second gives

```
[ sigma + i (u_0 + 2a) k ]^2  =  k^4 - (v_0 + 2 lam) k^3 / ell        (ell != 0)
```

so `sigma = -i(u_0+2a)k +- sqrt( k^4 - (v_0+2 lam) k^3/ell )`.

For **real** `k`, `ell != 0` and `|k| -> infinity`, `k^4` dominates the `k^3/ell`
term, hence `|Re sigma| ~ |k|^2`. The constant-background linearisation therefore
grows like `exp(|k|^2 t)`.

### 2.0 Convention for the lattice symbol — PINNED DOWN (added mid-run)

This was added after an apparent conflict between the main agent's and direction C's
dispersion formulas. **There is no conflict — only a normalisation choice.** It is
pinned down here so that no downstream claim can mix the two.

Let `Lambda_h(ell)` be the **full** symbol of a consistent discrete `d/dy`: the discrete
operator acts on the lattice mode `exp(i ell y_j)` as multiplication by `i Lambda_h(ell)`,
with `Lambda_h(ell) -> ell` as `h -> 0`. Examples:

| scheme | `Lambda_h(ell)` |
|---|---|
| centred `(u_{j+1}-u_{j-1})/(2h)` | `sin(ell h)/h` |
| forward `(u_{j+1}-u_j)/h` | `(exp(i ell h)-1)/h` |
| backward `(u_j-u_{j-1})/h` | `(1-exp(-i ell h))/h` |
| staggered | `2 sin(ell h/2)/h` |
| P1 consistent-mass FEM | `3 sin(ell h)/(h(2+cos ell h))` |

Let `r_h(ell) = Lambda_h(ell)/ell` be the **normalised** symbol, with `r_h -> 1` as
`h -> 0`. (`sin(th)/th`, `(exp(i th)-1)/(i th)`, `2 sin(th/2)/th`,
`3 sin th/(th(2+cos th))` respectively, where `th = ell h`.)

**[MAIN-VERIFIED — V11]** Replace `d/dy` by any such symbol in the `(1')`–`(2')` system
and linearise about a constant background. Using `w = u_y = Lambda_h u` (so
`u_x = i k u = i k w / (i Lambda_h) = (k/Lambda_h) w`), elimination of `v_hat` gives

```
[ sigma + i (u_0 + 2a) k ]^2  =  k^4 - (v_0 + 2 lam) k^3 / Lambda_h(ell)
                              =  k^4 - (v_0 + 2 lam) k^3 / (ell r_h(ell))
```

Equivalently, writing `mu_h(ell) := i Lambda_h(ell)` for the *complex* symbol of `d/dy`
(so `mu_h -> i ell`), the same identity reads

```
[ sigma + i (u_0 + 2a) k ]^2  =  k^4 - i (v_0 + 2 lam) k^3 / mu_h(ell)
```

Both forms are the same statement; the `i` in the second line is the `i` sitting inside
`mu_h`. Direction C's report uses the second convention; the main agent's `D2` check
(`experiments/MAIN_discrete_dispersion.py`) uses the first. **Never mix them in one
claim.** Facts that hold in every convention:

* the coefficient of `k^4` is exactly `1`, so `|Re sigma| ~ k^2` is universal;
* when `v_0 = -2 lam` (i.e. `v_0 = 4` at `lam = -2`) the `k^3` term vanishes
  **identically for every symbol**, so the semi-discrete dispersion relation coincides
  with the continuous one for every `y`-mode and every `h`. This is the strongest
  clean conditional statement available and is NOT a stability theorem;
* `Lambda_h(ell) = 0` (equivalently `r_h = 0`) is a **degenerate wavenumber** where the
  elimination above is invalid and a separate DAE analysis is required; the centred
  difference and the P1 consistent-mass FEM both have such a zero at `ell h = pi`.

**This is Hadamard ill-posedness, not a removable technicality.** Consequences that
every direction must respect:

* No unconditional well-posedness, no grid-uniform stability estimate, and no
  convergence theorem for general initial data can be true for this system.
* **Implicitness, conservation, a symplectic/geometric structure, finite elements
  or SBP dissipation do NOT remove this.** Those are properties of the
  discretisation; the obstruction is a property of the continuous symbol.
* Legitimate stability claims must be **conditional**: restricted frequency band
  (`|k| <= K`), analytic/band-limited data, a fixed truncation dimension, or a
  specific exact solution family.
* Distinguish: *linearised stability*, *finite-band stability*, *nonlinear
  stability*. A proof of one is not a proof of another.

**[MAIN-VERIFIED — V6/V7]** The `ell = 0` (i.e. `y`-independent) sector: the
linearised system forces `v_hat = 0` and `u_hat (v_0 + 2 lam) = 0`. So

* if `v_0 != -2 lam` there is **no** nontrivial `y`-independent linear mode;
* **[MAIN-VERIFIED — V7]** if `v_0 = -2 lam` then `v ≡ -2 lam` together with
  **arbitrary** `u = U(x,t)` (`u_y = 0`) is an **exact** solution of (1)–(2).

That is a genuine infinite-dimensional zero mode / non-uniqueness. For `lam = -2`
it occurs at `v_0 = 4`. Any scheme that inverts `d/dy` (or a difference analogue)
must state how this kernel is handled.

---

## 3. The staggered two-tau system (direction G's candidate)

Existing workspace claim (from `lean-toda/dlw_staggered_construction.md`, to be
independently audited — **not** assumed here):

```
(B - h D_x) F_j . G_j      = 0        G_j at y = jh
(B + h D_x) F_j . G_{j+1}  = 0        F_j at y = (j + 1/2) h
```

with `B = D_x^2 + D_t + 2a D_x`, i.e. `B_s = D_x^2 + D_t + 2s D_x` at
`s = a -+ h/2`.

### 3.1 Continuum limit — main-agent derivation

Put `Y = (j+1/2)h`, `F_j = f(Y)`, `G_j = g(Y - h/2)`, `G_{j+1} = g(Y + h/2)`,
`E_- = (B - hD_x)F_j . G_j`, `E_+ = (B + hD_x)F_j . G_{j+1}`, and the invertible
normalised pair

```
A_h = (E_+ + E_-)/2 ,        C_h = (E_+ - E_-)/h
```

**[MAIN-VERIFIED — V10]** (formal Taylor coefficients, no analytic remainder):

```
A_h = B f.g  + h^2 ( (1/8) B f.g_yy + (1/2) D_x f.g_y ) + O(h^4)
C_h = B f.g_y + 2 D_x f.g + h^2 ( (1/24) B f.g_yyy + (1/4) D_x f.g_yy ) + O(h^4)
```

No `h^1` term: the staggering cancels it. So the scheme is **formally second-order
consistent** for these two normalised residuals. [Note: formal Taylor coefficients
are NOT a remainder estimate; see §6 evidence grading.]

### 3.2 The limit is exactly the paper's system

**[MAIN-VERIFIED — V2]** For any constant-coefficient linear `P`,

```
D_y (P f . g)  =  d_y ( P f . g )  -  2 P ( f . g_y )
```

**[MAIN-VERIFIED — V3]** Consequently

```
(D_y B - 4 D_x) f.g  +  2 [ B f.g_y + 2 D_x f.g ]  =  d_y ( B f.g )
```

so on the locus `B f.g = 0`:

```
(D_y B - 4 D_x) f.g  =  -2 [ B f.g_y + 2 D_x f.g ]
```

i.e. `C_h = 0` is **exactly** the paper's eq. (6) at `lam = -2` (the `D_y B - 4D_x`
equation), and `A_h = 0` is exactly eq. (7). The staggered continuum limit is
therefore the right continuous system, with `lam = -2`.

Caution: the earlier workspace note claims this but the main agent found the naive
reasoning `D_y B f.g = d_y(B f.g)` is **false** (it is off by `2 B(f.g_y)`). The
correct identity is the one above. Do not reproduce the wrong step.

### 3.3 Two-soliton data

```
d = h/2,  P_i = p_i - a,  Q_i = q_i + a
rho_i = ((P_i+d)(Q_i+d)) / ((P_i-d)(Q_i-d))
r_i   = -(P_i+d)/(Q_i-d)
Gamma = (p1-p2)(q1-q2) / ((p1+q1)(p1+q2)(p2+q1)(p2+q2))
E_{i,j} = rho_i^j exp( (p_i+q_i)x + (q_i^2-p_i^2)t + theta_i0 )
G_j = 1 + E_1/(p1+q1) + E_2/(p2+q2) + Gamma E_1 E_2
F_j = 1 + r_1 E_1/(p1+q1) + r_2 E_2/(p2+q2) + Gamma r_1 r_2 E_1 E_2
```

**[V8 — symbolic, STATUS: NOT COMPLETED IN THIS SESSION]** `common/MAIN_verify_core.py v8`
sets up the general-parameter (`p1,p2,q1,q2,a,h` symbolic) 2-soliton check and expands in
`E_1^m E_2^n`. In this session the run did **not finish** (long symbolic `simplify`); it was
moved to a separate background job. An earlier run reportedly showed the
`(B - hD_x)F_j.G_j` branch clean. **Do not cite V8 as established above
`实验验证` until the completed run is quoted with its exit code.**

**[V9 — MAIN-VERIFIED, `实验验证`]** `common/MAIN_verify_core.py v9`, exact rationals,
`N = 1..5`, 4 parameter sets, `a in {1,2,3}`, `h in (0,1/2)`:

```
[PASS] V9  staggered tau family: exact rational N=1..5 x 4 parameter sets,
       2904 coefficients, all zero, arbitrary theta constants a=1..3, h in (0,1/2)
```

⚠ **This PASS was obtained only after fixing TWO defects in the checker itself.**
See `reports/MAIN_VERIFICATION.md` §3.2–§3.3. Both defects caused **false negatives**:

1. Residuals were grouped by `(dk, dw)`. They must be grouped by the **union monomial**
   `tuple(sorted(SF + SG))`: every monomial of the bilinear expansion must vanish as a whole,
   and several `(SF,SG)` pairs feed the *same* monomial with *different* `dk`.
   Grouping by `(dk,dw)` shatters one monomial and manufactures spurious nonzeros.
2. `C_S` double-counted the `1/(p_i+q_i)` factors. Per
   `lean-toda/dlw_staggered_construction.md` §4,

   ```
   C_S = Π_{i∈S} 1/(p_i+q_i) · Π_{i<k} (p_i−p_k)(q_i−q_k) / ((p_i+q_k)(p_k+q_i))
   ```

   The pair factor must contain the **cross** terms `(p_i+q_k)(p_k+q_i)` **only**;
   an earlier version additionally divided by `(p_i+q_i)(p_k+q_k)`, i.e. an extra
   `Π_i (p_i+q_i)^{|S|−1}`. That is exactly why `N=1` passed while every `N≥2`
   interaction term failed.

**Consequence for how this result may be cited**: the staggered two-tau system with the
`C_S` above reproduces all coefficients for `N ≤ 5` at sampled rational parameters.
This is `实验验证`, **not** a proof for arbitrary `N`.

**[V11 — MAIN-VERIFIED]** See §2.0 above for the general lattice-symbol dispersion relation.

### 3.4 What is NOT established about the staggered system

* Arbitrary-`N` determinant identity is a **reduction** to the paper's eq. (10)
  identity, valid as mathematics but **not formalised in Lean** and not
  independently re-proved by the main agent. Do not relabel it as proved.
* The nonlinear (logarithmic) variables for this staggered system are **not
  derived**. "Local nonlinear closed form" is an OPEN problem.
* Novelty is **NOT** claimed. No independent literature search has been run.
* No stability, well-posedness or convergence result.

---

## 4. Conventions to use everywhere

* Only `y` is discretised. `x`, `t` stay continuous unless a direction explicitly
  says otherwise, and then the extra discretisation must be flagged separately
  (rule: never mix the two levels in one claim).
* First round: `lam = -2`, `a` arbitrary. Any other parameter reduction must be
  stated and justified.
* Lattice: `j in Z` for the bi-infinite case, `j = 0..N` for a finite interval.
  `G_j` sits at `y = jh`; `F_j` at `y = (j+1/2)h` in the staggered system.
* `B_s := D_x^2 + D_t + 2 s D_x`, so `B_s = B + 2(s-a) D_x`.
* Two different shifts must never be silently merged: the **lattice site** index
  `j` and any **hierarchy level** index `n` are independent (direction H).

---

## 5. Lean environment — the ONLY allowed route

Shared, already deployed, **do not rebuild**:

```
Lean 4.34.0 ; Mathlib v4.34.0 ; commit 5ed2965256430c3649e86755f9576b54eca72435
```

Single verification entry (run from PowerShell):

```powershell
& 'C:\Users\msz\学术内容\_lean_shared\Check-Lean.ps1' `
  -Root $proofRoot -File $proofFile -TimeoutSeconds 300
```

* Write plain `.lean` files under your own directory. **No Lake project. No new
  toolchain. No `lake` command, ever.** Never run `elan install`, `lake init`,
  `lake update`, `lake exe cache get`, `lake build Mathlib`; never clone/copy
  Mathlib.
* `-Root` is the root for local modules: `import Common.Operators` resolves to
  `$proofRoot\Common\Operators.lean`.
* Multiple agents may call the entry concurrently. **Use your own `$proofRoot`**
  so you never edit a file another agent is compiling.
* Success = return code 0 **and** `PASSED` in the output. Results land in
  `$proofRoot\.lean-runs\<run-id>\result.json` and `build.log`.
* `sorry`, `admit`, and new `axiom`s are **rejected**. There is no way to bypass
  this, and you must not try.
* Add `#print axioms <full.theorem.name>` for each headline theorem. Standard
  foundations (`propext`, `Classical.choice`, `Quot.sound`) are fine and expected;
  anything else must be explained in the report.

### 5.1 API facts specific to this deployment (probed, not guessed)

* Big-operator notation is **`∑ x ∈ s, f x`** with `∈`. The older
  `∑ x in s, f x` form does **not** parse. Needs `open scoped BigOperators`.
* `Finset.sum_range_sub` may be absent; **`Finset.sum_range_sub'` exists**.
  `Finset.sum_mul` lives in `Mathlib.Algebra.BigOperators.Ring.Finset`.
* Module paths that exist: `Mathlib.Analysis.Asymptotics.Defs` (NOT
  `...Asymptotics.Asymptotics`), `Mathlib.Analysis.SpecialFunctions.ExpDeriv`,
  `Mathlib.Analysis.Calculus.Deriv.Basic`, `Mathlib.Data.Matrix.Basic`,
  `Mathlib.Data.Real.Basic` (deprecated alias of `Mathlib.Basic.Real.Basic`),
  `Mathlib.Data.Complex.Basic`, `Mathlib.Algebra.BigOperators.Group.Finset.*`.
* `Matrix.det`, `Matrix.dotProduct` are **not** in `Mathlib.Data.Matrix.Basic`;
  import the determinant module explicitly (e.g.
  `Mathlib.LinearAlgebra.Matrix.Determinant`) or avoid `det`.
* Confirmed present: `HasDerivAt`, `deriv`, `Real.exp`, `Complex.exp`,
  `HasDerivAt.exp`, `hasDerivAt_exp`, `Real.hasDerivAt_exp`, `ContDiff`,
  `HasFTaylorSeriesUpTo`, `Asymptotics.IsBigO`, `Asymptotics.IsLittleO`,
  `Filter.Tendsto`, `Continuous`, `Finset.sum_range_succ`, `Finset.sum_congr`,
  `Finset.sum_add_distrib`, `Finset.prod_range_div'`, `Matrix.transpose`,
  `Matrix.mulVec`, `Matrix.vecMul`.
* Tactic availability: `ring`, `ring_nf`, `field_simp`, `norm_num`, `linarith`,
  `nlinarith`, `simp`, `omega`, `decide`, `grind`, `positivity`, `gcongr`.
* **Prefer targeted imports.** `import Mathlib` loads the whole library and is slow
  on Windows. A slow first load is NOT a reason to reinstall anything.

### 5.2 Shared module you may import

`proofs/Common/Operators.lean` (main agent, **already PASSED**) provides
`DLW.Common.fwd`, `bwd`, `ctr`, `ctr2`, and the verified theorems
`ctr_const`, `ctr_kernel`, `telescoping`, `sbp_fwd_undivided`, `sbp_fwd`,
`sum_range_ctr`. Import it with `import Common.Operators` from your own root by
copying *nothing* — instead put your file under a root that also contains a copy,
or reference the main root. If you need it, ask the main agent; do not edit it.

---

## 6. Evidence grading — use these exact labels

Route status (exactly one per direction):

* `可行候选` — equations explicit, continuum limit correct, substantive structural
  or analytic result present.
* `条件可行` — depends on clearly stated, non-empty, meaningful restrictions.
* `候选被否定` — explicit counterexample or derivation contradiction, with the
  refuted scope stated.
* `尚未解决` — no completed construction or proof; **not** the same as failure.
* `工具阻塞` — environment/dependency problem; record what was attempted.

Proof coverage (choose the highest reached, do not merge levels):

* `实验验证` — floating point, exact sample, or CAS check.
* `Lean 代数验证` — a general algebraic relation formalised, analytic bridge open.
* `Lean 结构验证` — conservation/constraint/operator/variational property proved
  for a concrete discrete object.
* `Lean 分析验证` — remainder estimates, stability or convergence under explicit
  hypotheses.
* `数学证明，尚未完整形式化` — full derivation exists, Lean covers only part.

**Do not conflate.** Specifically forbidden inferences:
compiles ⇒ all goals proved; parameter identity ⇒ arbitrary-`N` determinant theorem;
energy conserved ⇒ grid-uniform stability; formal 2nd-order consistency ⇒ 2nd-order
convergence; antisymmetry ⇒ Poisson/Jacobi; one numerical parameter set ⇒ general
theorem.

Every important conclusion must be recorded as:

```
结论编号 / 数学陈述 / 对象与适用范围 / 假设与边界条件 /
Lean 定理名称 / Lean 文件及位置 / 验证命令 / 构建结果 /
未形式化的桥接步骤 / 所依赖的外部数学定理 / 证据等级
```

---

## 7. Hard rules

1. No `sorry`, `admit`, no new `axiom`, no assuming the goal.
2. **Never** ask Lean to prove a statement that is actually false. If a candidate
   is wrong, formalise the counterexample or a precisely scoped impossibility —
   that counts as success.
3. Keep formal derivative/jet data separate from genuine function calculus. An
   algebraic proof about arbitrary symbols is not a formalisation of real analysis.
4. Formal Taylor-coefficient identities are **not** remainder estimates.
5. Separate semi-discrete from fully discrete conservation.
6. Separate linearised, finite-band and nonlinear stability.
7. Audit every hypothesis set for contradiction, empty parameter domain, or
   degenerate kernel; a vacuously true theorem is a failure, not a success.
8. Do not shrink a target to an unrelated trivial identity to get a green build.
9. Citations must come from sources actually consulted, with DOI/link or local page.
   Do not invent references. Do not claim novelty from finding multi-solitons.
10. Do not modify `_lean_shared`, `lean-toda`, other models' directories, or this
    spec file. Write only inside your own direction directory.
11. **Every numeric/symbolic checker must explicitly exclude degenerate parameter
    sets and must state which ones it excludes.** In this project the paper's Gram
    data (13) contains the singular shifts `p_i - a` and `q_j + a`; the lattice
    symbol `Lambda_h` vanishes at `ell h = pi` for the centred difference AND for
    P1 consistent-mass FEM; and `c = v0 + 2 lambda = 0` kills a whole term.
    **Three separate false negatives occurred in this run purely from sampling a
    degenerate value** (`reports/MAIN_VERIFICATION.md` sections 3.2, 3.3, 3.5) --
    one of which nearly refuted a published paper and one of which nearly refuted
    a correct in-workspace construction. A "failure" caused by a degenerate
    parameter is never evidence about the construction; but a *silent* degenerate
    parameter is also unacceptable in a claimed PASS. State the excluded set.
