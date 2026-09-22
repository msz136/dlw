/-
  MAIN-AGENT CROSS-CUTTING RESULT (no-go theorem)

  Claim.  No consistent discretisation of the `y` variable can restore
  well-posedness of the DLW system on a constant background.

  Structure of the argument, formalised below:

  * `semidiscrete_elimination` (exact algebra, over `ℂ`):
    in the semi-discrete linearisation about a constant background, replacing
    the continuous symbol `i*ell` of `d/dy` by an arbitrary lattice symbol
    `i*mu`, the two linearised equations eliminate to EXACTLY

        (sigma + i (u0 + 2a) k)^2  =  k^4 - (v0 + 2*lambda) k^3 / mu .

    So `y`-discretisation enters ONLY through the factor `1/mu`; the `k^4` term
    -- the source of the instability -- is produced by the `x`-derivative
    structure and is untouched.

  * `growth_lower_bound` / `growth_unbounded` (over `ℝ`):
    for every fixed lattice symbol `mu > 0` the unstable branch grows at least
    like `k^2/2`, and the growth is unbounded as `k -> infinity`.

  Consequence: implicitness, conservation, SBP, finite elements, DG or a
  symplectic structure cannot remove this obstruction, because it is a property
  of the *continuous* symbol, not of the discretisation.  Every stability claim
  must therefore be conditional (band-limited data, fixed truncation, analytic
  data, or a named exact-solution family).

  Evidence grade: Lean 代数验证 for `semidiscrete_elimination`; Lean 分析验证 for
  the growth theorems.  The bridge from "unbounded growth of a linearised mode"
  to "Hadamard ill-posedness of the nonlinear problem" is standard but is NOT
  formalised here, and is recorded as an open bridge step.

  Implementation notes (all discovered by probing this exact Mathlib):
  * `ring` / `ring_nf` do NOT know `Complex.I * Complex.I = -1`; only `simp`
    and the explicit `rw [mul_pow, Complex.I_sq]` route do.  We therefore
    isolate `i` into the abstract symbol `K := i*k` and record the single
    algebraic fact `K^2 = -k^2` as a hypothesis, rewriting it away BEFORE the
    polynomial normalisation.  After that, `ring` only ever sees `i` to the
    first power (a single overall factor), which is legitimate.
  * The correct elimination identity carries a `1/k^2`.  An earlier draft
    asserted `E2 = (i*mu*uh) * charFun`, which is FALSE: the true value is
    `(i*mu*uh/k^2) * charFun`.  The `1/k^2` is exactly the factor removed by
    the first equation, so it must be retained.
  * `growth_lower_bound` takes `c <= 3*k*mu/4` rather than `4*c/(3*mu) <= k`
    to keep the arithmetic division-free; the two are equivalent for `mu > 0`
    and `growth_unbounded` discharges that conversion.
  * `Real.le_sqrt_of_sq_le` takes a SINGLE argument, the squared inequality.
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Basic.Complex.Basic
import Mathlib.Analysis.Real.Sqrt

noncomputable section

namespace DLW.MainNoGo

open Complex

/-! ## 0. The only complex-algebra fact we need -/

/-- The physical lattice symbol of `d/dx`: `(i*k)^2 = -k^2`. -/
theorem Ik_sq (k : ℂ) : (I * k) ^ 2 = -k ^ 2 := by
  rw [mul_pow, Complex.I_sq]
  ring

/-- A general linear symbol `K` with `K = i*k` squares to `-k^2`. -/
theorem K_sq_of_eq (K k : ℂ) (h : K = I * k) : K ^ 2 = -k ^ 2 := by
  rw [h, Ik_sq]

/-! ## 1. Exact elimination of the semi-discrete linearisation -/

/-- Residual of the linearised first equation
    `w_t + d_x[v_x + (u+2a) w] = 0` for the mode `exp(sigma t + i(k x + ell y))`,
    with `K` the symbol of `d/dx` (`K = i k`). -/
def E1 (s K u0 a wh vh : ℂ) : ℂ :=
  wh * s + K ^ 2 * vh + (u0 + 2 * a) * K * wh

/-- Residual of the linearised second equation
    `v_t + d_x[(u+2a) v + w_x + 2 lam u] = 0`. -/
def E2 (s K u0 a lam v0 uh vh wh : ℂ) : ℂ :=
  vh * s + K * (v0 * uh + (u0 + 2 * a) * vh + K * wh + 2 * lam * uh)

/-- The semi-discrete characteristic function, in terms of the abstract
    frequency symbol `D := s + i k (u0 + 2a)` and the lattice symbol `mu`. -/
def charFun (D k mu lam v0 : ℂ) : ℂ :=
  D ^ 2 - k ^ 4 + (v0 + 2 * lam) * k ^ 3 / mu

/-- **Exact elimination.**  With the lattice symbol `wh = i*mu*uh` of the discrete
    `d/dy`, with `vh` forced by the first linearised equation, and with
    `D := s + i k (u0 + 2a)`, the first equation vanishes identically and the
    second becomes exactly `(i*mu*uh/k^2)` times the characteristic function.

    Hence the semi-discrete dispersion relation is the continuous one with
    `ell` replaced by `mu`: the mesh only rescales the `1/ell` factor and never
    touches the `k^4` term. -/
theorem semidiscrete_elimination
    (s k mu u0 a lam v0 uh wh vh K D : ℂ)
    (hKI : K = I * k)
    (hwh : wh = I * mu * uh)
    (hD : D = s + K * (u0 + 2 * a))
    (hvh : vh = wh * D / k ^ 2)
    (hk : k ≠ 0) (hmu : mu ≠ 0) :
    E1 s K u0 a wh vh = 0 ∧
      E2 s K u0 a lam v0 uh vh wh
        = (I * mu * uh / k ^ 2) * charFun D k mu lam v0 := by
  have hK : K ^ 2 = -k ^ 2 := K_sq_of_eq K k hKI
  subst hwh
  subst hD
  subst hvh
  unfold E1 E2 charFun
  rw [hK]
  constructor
  · field_simp
    ring
  · field_simp
    ring_nf
    rw [hK]
    rw [hKI]
    ring

/-! ## 2. The unstable branch: unconditional lower bound on the growth rate -/

/-- **Growth lower bound.**  For a fixed lattice symbol `mu > 0`, whenever
    `c <= 3*k*mu/4` (with `c = v0 + 2*lambda`), the unstable branch of the
    semi-discrete dispersion relation grows at least like `k^2 / 2`.  The
    growth rate is therefore unbounded in `k`, uniformly in the mesh:
    **refining the mesh does not help.** -/
theorem growth_lower_bound (mu c k : ℝ) (hmu : 0 < mu) (hk : 0 < k)
    (hck : c ≤ 3 * k * mu / 4) :
    k ^ 2 / 2 ≤ Real.sqrt (k ^ 4 - c * k ^ 3 / mu) := by
  have hk3 : (0 : ℝ) ≤ k ^ 3 := by positivity
  have hstep : c * k ^ 3 / mu ≤ 3 * k ^ 4 / 4 := by
    rw [div_le_iff₀ hmu]
    nlinarith [mul_le_mul_of_nonneg_right hck hk3]
  have hsq : (k ^ 2 / 2) ^ 2 ≤ k ^ 4 - c * k ^ 3 / mu := by nlinarith
  exact Real.le_sqrt_of_sq_le hsq

/-- **No uniform stability.**  For every fixed lattice symbol `mu > 0`, every real
    `c` and every bound `M` there is an `x`-frequency `k > 0` whose semi-discrete
    linear growth rate exceeds `M`.  No consistent `y`-discretisation can
    therefore be uniformly stable: ill-posedness survives discretisation.

    (The hypothesis `c > 0` is not needed for the inequality itself; it is the
    physically relevant case `c = v0 + 2*lambda > 0`, where this branch is the
    genuinely unstable one.  The statement is therefore given for all real `c`.) -/
theorem growth_unbounded (mu c : ℝ) (hmu : 0 < mu) (M : ℝ) :
    ∃ k : ℝ, 0 < k ∧ M < Real.sqrt (k ^ 4 - c * k ^ 3 / mu) := by
  refine ⟨max (max 1 (M + 1)) (4 * c / (3 * mu)), ?_, ?_⟩
  · have h1 : (1 : ℝ) ≤ max (max 1 (M + 1)) (4 * c / (3 * mu)) :=
      le_trans (le_max_left 1 (M + 1)) (le_max_left _ _)
    linarith
  · have hk : (0 : ℝ) < max (max 1 (M + 1)) (4 * c / (3 * mu)) := by
      have h1 : (1 : ℝ) ≤ max (max 1 (M + 1)) (4 * c / (3 * mu)) :=
        le_trans (le_max_left 1 (M + 1)) (le_max_left _ _)
      linarith
    have hkle : 4 * c / (3 * mu) ≤ max (max 1 (M + 1)) (4 * c / (3 * mu)) :=
      le_max_right _ _
    have hck : c ≤ 3 * (max (max 1 (M + 1)) (4 * c / (3 * mu))) * mu / 4 := by
      have hmu3 : (0 : ℝ) < 3 * mu := by linarith
      have h := hkle
      rw [div_le_iff₀ hmu3] at h
      nlinarith
    have hbound := growth_lower_bound mu c (max (max 1 (M + 1)) (4 * c / (3 * mu)))
      hmu hk hck
    rcases lt_or_ge M 0 with hM | hM
    · have hpos : (0 : ℝ) < (max (max 1 (M + 1)) (4 * c / (3 * mu))) ^ 2 / 2 := by
        positivity
      linarith
    · have hkge : M + 1 ≤ max (max 1 (M + 1)) (4 * c / (3 * mu)) :=
        le_trans (le_max_right 1 (M + 1)) (le_max_left _ _)
      have h0 : (0 : ℝ) ≤ M + 1 := by linarith
      have hsq : (M + 1) ^ 2 ≤ (max (max 1 (M + 1)) (4 * c / (3 * mu))) ^ 2 := by
        nlinarith
      have hquad : M < (M + 1) ^ 2 / 2 := by nlinarith [sq_nonneg M]
      linarith

end DLW.MainNoGo
