# Agent brief — proving the DLW endpoint contracts in Lean

## What exists

* Frozen contract file: `C:\Users\msz\aca\Workspaces\lean_contracts\proofs\Contracts.lean`
  SHA-256 `e70876c538d52939b030e7813a6b1c60917a79e56e28b29146d22df8da98d656`
  (this is the frozen revision: the 2026-09-22 original differed only by two spaces in
  the lexical spacing of `0 < |h|`, which previously mis-lexed as the `<|` pipe operator;
  the mathematical content is unchanged).
  It defines `C01 … C25`, `N01 … N07` as `Prop`s, plus every shared definition
  (`bil`, `entry`, `tau`, `dm`, `d0`, `lap`, `physU`, `n1`, `n2`, …).
* **Do not modify `Contracts.lean`.** The starting and final statements are frozen.
  If you believe a target is *false*, do not "fix" it: report a counterexample.
* Proof root for the whole project: `C:\Users\msz\aca\Workspaces\lean_contracts\proofs`.
  Put your own file(s) in that directory only. Do not edit another agent's file.
* `PkgTrivial.lean` in that directory is a **worked example** that already passes
  (it proves `C03`, `C21`, `N02`–`N07`). Read it first: it shows the export convention
  and the tactic vocabulary that works here.

## The only accepted verification command

```powershell
& 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
  -Root 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs' `
  -File 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\<YourFile>.lean' `
  -TimeoutSeconds 900
```

Success = exit code 0 **and** the last line `PASSED: n local module(s).`
`sorry`, `admit` and `axiom` are rejected by the checker; so is a nonzero exit code.
The runner re-elaborates the import closure each time; a full Mathlib-importing file
takes roughly 1–4 minutes. Do not create a Lake project, do not touch `_lean_shared`,
do not run `lake`, `elan`, or any installer.

## Export convention

Every target `Cxx` must be exported under exactly this name and type:

```lean
theorem c07_proved : C07 := by
  ...
```

(inside `namespace DLWContract`, after `import Contracts`). One target may be split
into any number of auxiliary lemmas; the exported name must match
`c<nn>_proved` / `n<nn>_proved` (e.g. `c12_proved`, `n01_proved`).

Useful imports: `Mathlib.Tactic` (pulls `ring`, `linarith`, `nlinarith`, `field_simp`,
`positivity`, `norm_num`, `gcongr`, `fun_prop`), plus
`Mathlib.Analysis.SpecialFunctions.ExpDeriv`, `Mathlib.Analysis.SpecialFunctions.Log.Deriv`,
`Mathlib.Analysis.Calculus.ContDiff.Basic`, `Mathlib.Analysis.Calculus.Deriv.Basic`,
`Mathlib.LinearAlgebra.Matrix.Determinant.Basic`. Prefer targeted imports over
`import Mathlib` (much slower).

## Hard rules for this project

1. **No floating point reasoning, no "numerically it looks like 0".** The targets are
   statements about `ℝ` with `deriv`, arbitrary `N : ℕ`, arbitrary `h ≠ 0`.
2. Do not strengthen or weaken the statement. Do not add hypotheses that make the goal
   trivial (e.g. don't assume the conclusion).
3. Do not introduce new `axiom`s, or `Classical.choice`-style shortcuts to the *content*
   of the theorem (using classical logic for intermediate steps is fine).
4. If you need for a target `X` a lemma that another agent is proving, **prove your own
   local copy** inside your file rather than importing their file (avoids conflicts).
5. Report honestly: a file that compiles but silently proves a weaker statement is worse
   than an unproved target. If you cannot close a target, say so explicitly and state the
   exact remaining goal.

## Mathematician's hints (verified by hand on paper — trust but re-derive)

* `bil a f g = f_xx g - 2 f_x g_x + f g_xx + f_t g - f g_t + 2a(f_x g - f g_x)`.
  It is bilinear in `(f,g)`, and for plane waves `f = e^{λx+μt}`, `g = e^{λ'x+μ't}` it is
  `[(λ-λ')² + (μ-μ') + 2a(λ-λ')]·f·g`. It vanishes on `(1,1)` and on equal plane waves.
* `hx f g = f_x g - f g_x`; for `f = e^{λx}`, `g = e^{λ'x}` it is `(λ-λ')fg`.
* `γ_{ik} = -(p_i-s)/(q_k+s)` and `χ_{ik} = λ_h(p_i-a)·λ_h(q_k+a)` with
  `λ_h(z) = (z+h/2)/(z-h/2)`. **Key exact identity (C04):** `γ_{ik}(a-h/2) = γ_{ik}(a+h/2)·χ_{ik}`.
* `entry = δ_{ik} + c_{ik}γ^n χ^j e^{(p_i+q_k)x + ((q_k)²-(p_i)²)t}`, and `∂ₓ entry = (p_i+q_k)(entry - δ_{ik})`,
  `∂_t entry = ((q_k)²-(p_i)²)(entry - δ_{ik})`, `entry_{n+1} - δ = γ(entry_n - δ)`.
* C13: with `α = log f`, `β = log g`, the exact identity
  `bil a f g/(f g) = (α+β)_xx + ((α-β)_x)² + (α-β)_t + 2a(α-β)_x` holds
  (cross-term coefficient **+1**).
* C14 is a *residual* identity (no equation is assumed): the normalized residuals
  `A = bil(a-h/2)(F_j)(G_j)/(F_j G_j)`, `C = bil(a+h/2)(F_j)(G_{j+1})/(F_j G_{j+1})`
  satisfy `n1 = dm(lx(A+C))` and `n2 = d0(lx(A+C)) + (4/h)·lx(A-C)`.
* C19: `n1 = 0` gives `∂_t W + ∂_x J_W = 0`; `n2 = 0` gives `∂_t v + ∂_x J_V = 0`,
  with `J_W`, `J_V` exactly the `JW`/`JV` defined in `Contracts.lean`.
* C20: sum `n1` over one period. `∑ dm = 0` and `∑ lap = 0` telescope by periodicity,
  and `∑_j mm v_j = ∑_j v_j` under `PeriodicL m v`; hence `∂_x² ∑ v = 0`.
  There is **no** mean-mode evolution equation — do not manufacture one.
* The `(0 : Lattice)` and `(0 : XT)` functions are `Pi`-zero; `simp [dm, d0, lap]`
  reduces them, and `deriv_const` (via `simp [dx]`, `simp [dt]`) kills x/t-constant
  `XT`s. `fun _ _ t => c t` is *j-constant definitionally*, so `dm`/`d0`/`lap` of it are
  `0` by beta reduction + `sub_self`.
