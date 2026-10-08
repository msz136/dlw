/-
Package: N01 — one-step defect orders for the numerical layer.

Verified in this file:

* `n01_euler_part`      : the Euler one-step defect is `O(h^2)`.
* `n01_trapezoid_part`  : the trapezoidal residual is `O(h^3)`.

NOT verified in this file: the RK4 conjunct (`O(h^5)`).  The classical proof needs the
RK4 order condition — one RK4 step reproduces the degree-4 Taylor polynomial of the
exact solution up to `O(h^5)`.  `n01_rk4_of_taylor_poly` records exactly that remaining
obligation as an explicit hypothesis of a checked reduction lemma.  Because that step is
not established, the target `n01_proved : N01` is deliberately NOT declared here; the two
conjuncts that are proved are exported under their own names.

Everything below uses the frozen statements of `Contracts.lean` verbatim (through the
definitions `PowBound`, `euler`, `rk4`, `trapResidual`, `N01`); no hypothesis is added to
any of them and no target is restated.
-/
import Contracts
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Tactic

set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

noncomputable section
open scoped BigOperators Nat Topology
open Filter

namespace DLWContract

/-! ## Generic tools -/

/-- Transfer of a `PowBound` along a pointwise equality of the error function. -/
theorem powBound_congr {p : ℕ} {e₁ e₂ : ℝ → ℝ} (hEq : ∀ h, e₁ h = e₂ h)
    (h₁ : PowBound p e₁) : PowBound p e₂ := by
  obtain ⟨C, hC, ε, hε, hb⟩ := h₁
  exact ⟨C, hC, ε, hε, fun h hh hlt => by rw [← hEq h]; exact hb h hh hlt⟩

/-- Triangle inequality for `PowBound` at a fixed order. -/
theorem powBound_add_of_eq {E : Type*} [SeminormedAddCommGroup E] {p : ℕ} {X Y Z : ℝ → E}
    (hX : PowBound p (fun h => ‖X h‖)) (hY : PowBound p (fun h => ‖Y h‖))
    (hXYZ : ∀ h, X h + Y h = Z h) : PowBound p (fun h => ‖Z h‖) := by
  obtain ⟨CX, hCX, εX, hεX, hXineq⟩ := hX
  obtain ⟨CY, hCY, εY, hεY, hYineq⟩ := hY
  refine ⟨CX + CY, add_nonneg hCX hCY, min εX εY, lt_min hεX hεY, fun h hh hlt => ?_⟩
  have h1 : |h| < εX := lt_of_lt_of_le hlt (min_le_left _ _)
  have h2 : |h| < εY := lt_of_lt_of_le hlt (min_le_right _ _)
  have hX' : ‖X h‖ ≤ CX * |h| ^ p := by
    simpa only [abs_of_nonneg (norm_nonneg (X h))] using hXineq h hh h1
  have hY' : ‖Y h‖ ≤ CY * |h| ^ p := by
    simpa only [abs_of_nonneg (norm_nonneg (Y h))] using hYineq h hh h2
  have hZb : ‖Z h‖ ≤ (CX + CY) * |h| ^ p := by
    rw [← hXYZ h]
    calc ‖X h + Y h‖ ≤ ‖X h‖ + ‖Y h‖ := norm_add_le _ _
      _ ≤ CX * |h| ^ p + CY * |h| ^ p := add_le_add hX' hY'
      _ = (CX + CY) * |h| ^ p := by ring
  simpa only [abs_of_nonneg (norm_nonneg (Z h))] using hZb

/-- Combining an `O(h^3)` term with an `O(h^2)` term weighted by `h/2`. -/
theorem powBound_combine_of_eq {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {A B Z : ℝ → E} (hA : PowBound 3 (fun h => ‖A h‖)) (hB : PowBound 2 (fun h => ‖B h‖))
    (hABZ : ∀ h, A h - (h / 2) • B h = Z h) : PowBound 3 (fun h => ‖Z h‖) := by
  obtain ⟨CA, hCA, εA, hεA, hAineq⟩ := hA
  obtain ⟨CB, hCB, εB, hεB, hBineq⟩ := hB
  refine ⟨CA + CB / 2, by positivity, min εA εB, lt_min hεA hεB, fun h hh hlt => ?_⟩
  have h1 : |h| < εA := lt_of_lt_of_le hlt (min_le_left _ _)
  have h2 : |h| < εB := lt_of_lt_of_le hlt (min_le_right _ _)
  have hA' : ‖A h‖ ≤ CA * |h| ^ 3 := by
    simpa only [abs_of_nonneg (norm_nonneg (A h))] using hAineq h hh h1
  have hB' : ‖B h‖ ≤ CB * |h| ^ 2 := by
    simpa only [abs_of_nonneg (norm_nonneg (B h))] using hBineq h hh h2
  have hsmul : ‖(h / 2) • B h‖ = (|h| / 2) * ‖B h‖ := by
    rw [norm_smul, Real.norm_eq_abs, abs_div, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 2)]
  have hZb : ‖Z h‖ ≤ (CA + CB / 2) * |h| ^ 3 := by
    rw [← hABZ h]
    calc ‖A h - (h / 2) • B h‖ ≤ ‖A h‖ + ‖(h / 2) • B h‖ := norm_sub_le _ _
      _ = ‖A h‖ + (|h| / 2) * ‖B h‖ := by rw [hsmul]
      _ ≤ CA * |h| ^ 3 + (|h| / 2) * (CB * |h| ^ 2) := by
          have h3 : (|h| / 2) * ‖B h‖ ≤ (|h| / 2) * (CB * |h| ^ 2) :=
            mul_le_mul_of_nonneg_left hB' (by positivity)
          linarith
      _ = (CA + CB / 2) * |h| ^ 3 := by ring
  simpa only [abs_of_nonneg (norm_nonneg (Z h))] using hZb

/-- The degree-`j` Taylor polynomial of `f` at `t`, evaluated at `t + h`, written with
ordinary iterated derivatives at the base point. -/
theorem taylorWithinEval_eq_sum {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (f : ℝ → E) (j : ℕ) (t h : ℝ) :
    taylorWithinEval f j Set.univ t (t + h) =
      ∑ k ∈ Finset.range (j + 1), ((k ! : ℝ)⁻¹ * h ^ k) • iteratedDeriv k f t := by
  rw [taylor_within_apply]
  refine Finset.sum_congr rfl fun k _ => ?_
  rw [iteratedDerivWithin_univ, show t + h - t = h by ring]

/-- **One-variable Taylor remainder bound.**  For a `C^{m+1}` function the degree-`m` Taylor
polynomial at `t` approximates `f (t + h)` to order `m + 1`, with a constant that is uniform
on a neighbourhood of `t`. -/
theorem powBound_taylor_poly {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    (m : ℕ) (f : ℝ → E) (t : ℝ) (hf : ContDiff ℝ (m + 1) f) :
    PowBound (m + 1)
      (fun h => ‖f (t + h) - taylorWithinEval f m Set.univ t (t + h)‖) := by
  have hlo : Asymptotics.IsLittleO (𝓝 t)
      (fun x : ℝ => f x - taylorWithinEval f (m + 1) Set.univ t x)
      (fun x : ℝ => (x - t) ^ (m + 1)) := taylor_isLittleO_univ (x₀ := t) hf
  have hev : ∀ᶠ x in 𝓝 t,
      ‖f x - taylorWithinEval f (m + 1) Set.univ t x‖ ≤ 1 * ‖(x - t) ^ (m + 1)‖ :=
    Asymptotics.isLittleO_iff.mp hlo (c := 1) one_pos
  rw [Metric.eventually_nhds_iff] at hev
  obtain ⟨ε, hεpos, hε⟩ := hev
  have hfac : (0 : ℝ) < ((m + 1)! : ℝ) := by positivity
  set C : ℝ := 1 + ((m + 1)! : ℝ)⁻¹ * ‖iteratedDeriv (m + 1) f t‖ with hCdef
  have hC : 0 ≤ C := by rw [hCdef]; positivity
  refine ⟨C, hC, ε, hεpos, ?_⟩
  intro h hh hlt
  show |‖f (t + h) - taylorWithinEval f m Set.univ t (t + h)‖| ≤ C * |h| ^ (m + 1)
  rw [abs_of_nonneg (norm_nonneg (f (t + h) - taylorWithinEval f m Set.univ t (t + h)))]
  have hR : ‖f (t + h) - taylorWithinEval f (m + 1) Set.univ t (t + h)‖ ≤ 1 * |h| ^ (m + 1) := by
    have hd : dist (t + h) t < ε := by simpa [Real.dist_eq] using hlt
    have := hε hd
    simpa [norm_pow, Real.norm_eq_abs] using this
  have hlast : (∑ k ∈ Finset.range (m + 1 + 1),
        ((k ! : ℝ)⁻¹ * h ^ k) • iteratedDeriv k f t)
      = (∑ k ∈ Finset.range (m + 1), ((k ! : ℝ)⁻¹ * h ^ k) • iteratedDeriv k f t) +
        (((m + 1)! : ℝ)⁻¹ * h ^ (m + 1)) • iteratedDeriv (m + 1) f t :=
    Finset.sum_range_succ (fun k => ((k ! : ℝ)⁻¹ * h ^ k) • iteratedDeriv k f t) (m + 1)
  have hstep : taylorWithinEval f (m + 1) Set.univ t (t + h) -
        taylorWithinEval f m Set.univ t (t + h)
      = (((m + 1)! : ℝ)⁻¹ * h ^ (m + 1)) • iteratedDeriv (m + 1) f t := by
    rw [taylorWithinEval_eq_sum f (m + 1) t h, taylorWithinEval_eq_sum f m t h, hlast]
    abel
  have hstepnorm : ‖taylorWithinEval f (m + 1) Set.univ t (t + h) -
        taylorWithinEval f m Set.univ t (t + h)‖
      = ((m + 1)! : ℝ)⁻¹ * |h| ^ (m + 1) * ‖iteratedDeriv (m + 1) f t‖ := by
    rw [hstep, norm_smul, Real.norm_eq_abs, abs_mul, abs_inv, abs_of_pos hfac, abs_pow]
    try ring
  have hsplit : f (t + h) - taylorWithinEval f m Set.univ t (t + h) =
      (f (t + h) - taylorWithinEval f (m + 1) Set.univ t (t + h)) +
      (taylorWithinEval f (m + 1) Set.univ t (t + h) - taylorWithinEval f m Set.univ t (t + h)) := by
    abel
  rw [hsplit]
  calc ‖(f (t + h) - taylorWithinEval f (m + 1) Set.univ t (t + h)) +
          (taylorWithinEval f (m + 1) Set.univ t (t + h) - taylorWithinEval f m Set.univ t (t + h))‖
      ≤ ‖f (t + h) - taylorWithinEval f (m + 1) Set.univ t (t + h)‖ +
        ‖taylorWithinEval f (m + 1) Set.univ t (t + h) - taylorWithinEval f m Set.univ t (t + h)‖ :=
        norm_add_le _ _
    _ ≤ 1 * |h| ^ (m + 1) + ((m + 1)! : ℝ)⁻¹ * |h| ^ (m + 1) * ‖iteratedDeriv (m + 1) f t‖ := by
        rw [hstepnorm]; linarith
    _ = C * |h| ^ (m + 1) := by rw [hCdef]; ring

/-! ## N01, Euler conjunct: the one-step defect is `O(h^2)` -/

theorem n01_euler_part :
    ∀ (m : ℕ) (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ)) (z : ℝ → (Fin m → ℝ)),
      ContDiff ℝ ⊤ (fun q : ℝ × (Fin m → ℝ) => f q.1 q.2) → ContDiff ℝ ⊤ z →
      (∀ t, HasDerivAt z (f t (z t)) t) → ∀ t,
      PowBound 2 (fun h => ‖z (t + h) - euler f t h (z t)‖) := by
  intro m f z hf hz hz' t
  have hmain : PowBound 2
      (fun h => ‖z (t + h) - taylorWithinEval z 1 Set.univ t (t + h)‖) :=
    powBound_taylor_poly 1 z t (hz.of_le le_top)
  have hpoly : ∀ h : ℝ, taylorWithinEval z 1 Set.univ t (t + h) = euler f t h (z t) := by
    intro h
    rw [taylorWithinEval_eq_sum z 1 t h]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, iteratedDeriv_zero,
      iteratedDeriv_one, (hz' t).deriv, euler, Nat.factorial_zero, Nat.factorial_one,
      Nat.cast_one, inv_one, pow_zero, pow_one, mul_one, one_mul, one_smul]
  refine powBound_congr
    (e₁ := fun h => ‖z (t + h) - taylorWithinEval z 1 Set.univ t (t + h)‖) ?_ hmain
  intro h
  show ‖z (t + h) - taylorWithinEval z 1 Set.univ t (t + h)‖ = ‖z (t + h) - euler f t h (z t)‖
  rw [hpoly h]

/-! ## N01, trapezoid conjunct: the residual is `O(h^3)` -/

theorem n01_trapezoid_part :
    ∀ (m : ℕ) (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ)) (z : ℝ → (Fin m → ℝ)),
      ContDiff ℝ ⊤ (fun q : ℝ × (Fin m → ℝ) => f q.1 q.2) → ContDiff ℝ ⊤ z →
      (∀ t, HasDerivAt z (f t (z t)) t) → ∀ t,
      PowBound 3 (fun h => ‖trapResidual f t h (z t) (z (t + h))‖) := by
  intro m f z hf hz hz' t
  let G : ℝ → (Fin m → ℝ) := fun s => f s (z s)
  have hG : ContDiff ℝ ⊤ G := hf.comp (contDiff_id.prodMk hz)
  have hderivz : deriv z = G := funext fun s => (hz' s).deriv
  have h2z : iteratedDeriv 2 z t = deriv G t := by
    rw [iteratedDeriv_succ', hderivz, iteratedDeriv_one]
  -- the exact degree-2 Taylor polynomial of `z`
  have hTz : ∀ h : ℝ, taylorWithinEval z 2 Set.univ t (t + h)
      = z t + h • f t (z t) + (h ^ 2 / 2) • deriv G t := by
    intro h
    rw [taylorWithinEval_eq_sum z 2 t h]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, iteratedDeriv_zero,
      iteratedDeriv_one, (hz' t).deriv, h2z, Nat.factorial_zero, Nat.factorial_one,
      Nat.factorial_two, Nat.cast_one, inv_one, pow_zero, pow_one, mul_one, one_smul]
    first
      | (simp; module)
      | (norm_num; module)
      | simp
  -- the exact degree-1 Taylor polynomial of the velocity `G`
  have hTg : ∀ h : ℝ, taylorWithinEval G 1 Set.univ t (t + h) = f t (z t) + h • deriv G t := by
    intro h
    rw [taylorWithinEval_eq_sum G 1 t h]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, iteratedDeriv_zero,
      iteratedDeriv_one, Nat.factorial_zero, Nat.factorial_one, Nat.cast_one, inv_one,
      pow_zero, pow_one, mul_one, one_smul, G]
    first
      | (simp; module)
      | (norm_num; module)
      | simp
  have hA : PowBound 3 (fun h => ‖z (t + h) - taylorWithinEval z 2 Set.univ t (t + h)‖) :=
    powBound_taylor_poly 2 z t (hz.of_le le_top)
  have hB : PowBound 2 (fun h => ‖G (t + h) - taylorWithinEval G 1 Set.univ t (t + h)‖) :=
    powBound_taylor_poly 1 G t (hG.of_le le_top)
  refine powBound_combine_of_eq
    (A := fun h => z (t + h) - taylorWithinEval z 2 Set.univ t (t + h))
    (B := fun h => G (t + h) - taylorWithinEval G 1 Set.univ t (t + h))
    (Z := fun h => trapResidual f t h (z t) (z (t + h))) hA hB ?_
  intro h
  rw [hTz h, hTg h]
  dsimp only [G]
  simp only [trapResidual]
  module

/-! ## N01, RK4 conjunct: what is still missing -/

/-- The remaining obligation for the RK4 conjunct, isolated as a checked reduction.

If one RK4 step reproduces the degree-4 Taylor polynomial of the exact solution up to
`O(h^5)` — the classical RK4 order condition — then the RK4 conjunct of `N01` follows from
the Taylor remainder bound.  The hypothesis `hRK` is *not* proved anywhere in this
development; it is the precise gap. -/
theorem n01_rk4_of_taylor_poly (m : ℕ) (f : ℝ → (Fin m → ℝ) → (Fin m → ℝ))
    (z : ℝ → (Fin m → ℝ)) (t : ℝ) (hz : ContDiff ℝ ⊤ z)
    (hRK : PowBound 5
      (fun h => ‖rk4 f t h (z t) - taylorWithinEval z 4 Set.univ t (t + h)‖)) :
    PowBound 5 (fun h => ‖z (t + h) - rk4 f t h (z t)‖) := by
  have hT : PowBound 5 (fun h => ‖z (t + h) - taylorWithinEval z 4 Set.univ t (t + h)‖) :=
    powBound_taylor_poly 4 z t (hz.of_le le_top)
  have h2 : PowBound 5
      (fun h => ‖taylorWithinEval z 4 Set.univ t (t + h) - rk4 f t h (z t)‖) := by
    refine powBound_congr
      (e₁ := fun h => ‖rk4 f t h (z t) - taylorWithinEval z 4 Set.univ t (t + h)‖) ?_ hRK
    intro h
    show ‖rk4 f t h (z t) - taylorWithinEval z 4 Set.univ t (t + h)‖
      = ‖taylorWithinEval z 4 Set.univ t (t + h) - rk4 f t h (z t)‖
    rw [norm_sub_rev]
  refine powBound_add_of_eq
    (X := fun h => z (t + h) - taylorWithinEval z 4 Set.univ t (t + h))
    (Y := fun h => taylorWithinEval z 4 Set.univ t (t + h) - rk4 f t h (z t))
    (Z := fun h => z (t + h) - rk4 f t h (z t)) hT h2 ?_
  intro h
  abel

end DLWContract
