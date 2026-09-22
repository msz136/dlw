/-
Package: elementary core targets.

Targets C03, C21, N02, N03, N04, N05, N06, N07 of `Contracts.lean`.

None of these depends on the Gram/determinant layer; they are pure order/algebra or
elementary calculus facts about the *definitions* in the contract file.  The contract
statements are used verbatim through the frozen `C01..C25`/`N01..N07` definitions.
-/
import Contracts
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## C03 — the staggered offsets are forced inside the two-wall template -/

theorem c03_proved : C03 := by
  intro a h left right hh h1 h2
  have h1' : left + right = 0 := by
    have := h1 1
    simpa using this
  have h2' : 2 * (right - left) = 2 * h := by
    have := h2 1
    simpa using this
  constructor <;> linarith

/-! ## C21 — the mean mode is a genuine free degree of freedom -/

theorem c21_proved : C21 := by
  intro a h c hc hh
  refine ⟨?_, ?_⟩
  · funext j x t
    simp only [n1, Pi.zero_apply, Pi.add_apply]
    have hW : W h (fun _ _ t => c t) 0 = 0 := by
      funext j x t
      simp [W, d0]
    have hH : H a h (fun _ _ t => c t) 0 = fun _ _ t => c t ^ 2 / 2 + (2 * a) * c t := by
      funext j x t
      simp [H, hW]
    have hdm : dm h (lt (fun _ _ t => c t) + lx (H a h (fun _ _ t => c t) 0)) = 0 := by
      funext j x t
      simp [dm, hH, lt, lx]
    have hlap : lap h (dm h (fun _ _ t => c t)) = 0 := by
      funext j x t
      simp [lap, dm]
    simp [hdm, hlap, mm, lxx, lx, dx]
  · funext j x t
    simp only [n2, Pi.zero_apply, Pi.add_apply]
    have hW : W h (fun _ _ t => c t) 0 = 0 := by
      funext j x t
      simp [W, d0]
    have hH : H a h (fun _ _ t => c t) 0 = fun _ _ t => c t ^ 2 / 2 + (2 * a) * c t := by
      funext j x t
      simp [H, hW]
    have hd0H : d0 h (H a h (fun _ _ t => c t) 0) = 0 := by
      funext j x t
      simp [d0, hH]
    have hd0u : d0 h (fun _ _ t => c t) = 0 := by
      funext j x t
      simp [d0]
    have hlapW : lap h (W h (fun _ _ t => c t) 0) = 0 := by
      funext j x t
      simp [lap, hW]
    simp [hd0H, hd0u, hW, lt, lx, lxx, dx, dt, lap]

/-! ## N02 — the finite-step error recurrence -/

theorem n02_proved : N02 := by
  intro e q η hq hη hrec n
  have hgeom : ∀ n : ℕ, (1 : ℝ) + q * (∑ i ∈ Finset.range n, q ^ i)
      = (∑ i ∈ Finset.range n, q ^ i) + q ^ n := by
    intro n
    have := geom_sum_mul q n
    linarith
  induction n with
  | zero => simp
  | succ n ih =>
    have hmul : q * e n ≤ q * (q ^ n * e 0 + η * ∑ i ∈ Finset.range n, q ^ i) :=
      mul_le_mul_of_nonneg_left ih hq
    calc e (n + 1) ≤ q * e n + η := hrec n
      _ ≤ q * (q ^ n * e 0 + η * ∑ i ∈ Finset.range n, q ^ i) + η := by linarith
      _ = q ^ (n + 1) * e 0 + η * ∑ i ∈ Finset.range (n + 1), q ^ i := by
            rw [Finset.sum_range_succ, pow_succ]
            have hg := hgeom n
            linear_combination (η : ℝ) * hg

/-! ## N03 — splitting a total error into its two references -/

theorem n03_proved : N03 := by
  intro m computed exactH exact0
  have h : computed - exact0 = (computed - exactH) + (exactH - exact0) := by abel
  calc ‖computed - exact0‖ = ‖(computed - exactH) + (exactH - exact0)‖ := by rw [h]
    _ ≤ ‖computed - exactH‖ + ‖exactH - exact0‖ := norm_add_le _ _

/-! ## N04 — the finite-sample numerical certificate -/

theorem n04_proved : N04 := by
  intro m computed lo hi reference tol htol hlo hcomp i
  have hlo1 : (lo i : ℝ) ≤ reference i := (hlo i).1
  have hlo2 : reference i ≤ (hi i : ℝ) := (hlo i).2
  have hc1 : ((computed i : ℚ) : ℝ) - (lo i : ℝ) ≤ (tol : ℝ) := by
    have := (abs_le.mp (hcomp i).1).2
    exact_mod_cast this
  have hc2 : -((tol : ℚ) : ℝ) ≤ ((computed i : ℚ) : ℝ) - (hi i : ℝ) := by
    have := (abs_le.mp (hcomp i).2).1
    exact_mod_cast this
  rw [abs_le]
  constructor <;> linarith

/-! ## N05 — the open-chain base-value reconstruction -/

theorem n05_proved : N05 := by
  intro h b p hh
  refine ⟨?_, ?_⟩
  · simp [reconstruct]
  · intro j
    simp only [reconstruct]
    rw [Finset.sum_range_succ]
    field_simp
    ring

/-! ## N06 — a positive growth rate is not removed by exact integration -/

theorem n06_proved : N06 := by
  intro g Δt hg hΔt
  have hpos : 0 < Δt * g := mul_pos hΔt hg
  constructor
  · linarith
  · exact Real.one_lt_exp_iff.mpr hpos

/-! ## N07 — the linear error budget -/

theorem n07_proved : N07 := by
  intro seed tolerance g T hseed hle hg hT hmain
  have hseedpos : 0 < seed := hseed
  have htolpos : 0 < tolerance := lt_of_lt_of_le hseedpos hle
  have hratio : 0 < tolerance / seed := div_pos htolpos hseedpos
  have hexp : Real.exp (g * T) ≤ tolerance / seed := by
    rw [← Real.exp_log hratio]
    exact Real.exp_le_exp.mpr hmain
  calc seed * Real.exp (g * T) ≤ seed * (tolerance / seed) :=
        mul_le_mul_of_nonneg_left hexp (le_of_lt hseedpos)
    _ = tolerance := by field_simp

end DLWContract
