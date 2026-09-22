/-
Package: C11 — the semi-discrete `O(h^2)` wall-average / wall-difference identities.

Contents
* `c11_powBound_*` — `ℝ`-valued `PowBound` tools (addition, a pure quadratic term,
  symmetrised second differences of a remainder, difference quotients of a remainder,
  a norm-to-`abs` bridge and an "away from `h = 0`" congruence);
* a locally re-derived copy of the calculus machinery of `PkgContinuous` (bridges between
  `deriv` and `fderiv` on `ℝ × ℝ`, the two-variable Clairaut lemma, the `y`-jets of a
  slice), plus smoothness of the slice families;
* `c11_proved` — target `C11`, by one degree-2 Taylor expansion of
  `Φ s = bil (a + s) (slice f y) (slice g (y + s)) x t`
  around `s = 0`, using `wallPlus = Φ (h/2)`, `wallMinus = Φ (-(h/2))`,
  `cbil a f g x y t = Φ 0` and `Φ'(0) = cbil a f (sy g) x y t + 2 * chx f g x y t`.

Everything uses the frozen statements of `Contracts.lean` verbatim; no hypothesis is added
to any target and no target is restated.
-/
import Contracts
import PkgNumeric
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Tactic

set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## `PowBound` tools for `ℝ`-valued errors -/

/-- The function-level numeral `2 : XT` evaluated pointwise (definitional). -/
private lemma c11_two_apply (x t : ℝ) : (2 : XT) x t = (2 : ℝ) := rfl

/-- Triangle inequality for `PowBound` at a fixed order (`ℝ`-valued). -/
theorem c11_powBound_add {p : ℕ} {X Y Z : ℝ → ℝ} (hX : PowBound p X) (hY : PowBound p Y)
    (hXYZ : ∀ h, X h + Y h = Z h) : PowBound p Z := by
  obtain ⟨CX, hCX, εX, hεX, hXb⟩ := hX
  obtain ⟨CY, hCY, εY, hεY, hYb⟩ := hY
  refine ⟨CX + CY, add_nonneg hCX hCY, min εX εY, lt_min hεX hεY, fun h hh hlt => ?_⟩
  have h1 : |h| < εX := lt_of_lt_of_le hlt (min_le_left _ _)
  have h2 : |h| < εY := lt_of_lt_of_le hlt (min_le_right _ _)
  rw [← hXYZ h]
  calc |X h + Y h| ≤ |X h| + |Y h| := abs_add_le _ _
    _ ≤ CX * |h| ^ p + CY * |h| ^ p := add_le_add (hXb h hh h1) (hYb h hh h2)
    _ = (CX + CY) * |h| ^ p := by ring

/-- A pure quadratic error term is `O(h^2)` with the exact constant `|c| / 8`. -/
theorem c11_powBound_quad (c : ℝ) : PowBound 2 (fun h : ℝ => (h ^ 2 / 8) * c) := by
  refine ⟨|c| / 8, by positivity, 1, one_pos, fun h _ _ => ?_⟩
  have hval : |(h ^ 2 / 8) * c| = |c| / 8 * |h| ^ 2 := by
    rw [abs_mul, abs_div, abs_pow, abs_of_pos (by norm_num : (0 : ℝ) < 8)]
    ring
  rw [hval]

/-- The `abs`-of-norm bridge: `PowBound` for `h ↦ ‖X h‖` gives `PowBound` for `X`. -/
theorem c11_powBound_norm_abs {p : ℕ} {X : ℝ → ℝ} (h : PowBound p (fun h => ‖X h‖)) :
    PowBound p X := by
  obtain ⟨C, hC, ε, hε, hb⟩ := h
  exact ⟨C, hC, ε, hε, fun h hh hlt => by
    simpa only [Real.norm_eq_abs, abs_abs] using hb h hh hlt⟩

/-- Transfer of `PowBound` along a pointwise equality that is only required for `h ≠ 0`. -/
theorem c11_powBound_congr_ne {p : ℕ} {e₁ e₂ : ℝ → ℝ}
    (hEq : ∀ h, h ≠ 0 → e₁ h = e₂ h) (h₁ : PowBound p e₁) : PowBound p e₂ := by
  obtain ⟨C, hC, ε, hε, hb⟩ := h₁
  exact ⟨C, hC, ε, hε, fun h hh hlt => by
    rw [← hEq h (abs_pos.mp hh)]
    exact hb h hh hlt⟩

/-- The symmetrised second difference of an `O(|u|^{p+1})` remainder is `O(|h|^p)`. -/
theorem c11_powBound_symm_avg {p : ℕ} {R : ℝ → ℝ} (hR : PowBound (p + 1) R) :
    PowBound p (fun h : ℝ => (R (h / 2) + R (-(h / 2))) / 2) := by
  obtain ⟨C, hC, ε, hε, hb⟩ := hR
  refine ⟨C, hC, min (2 * ε) 1, lt_min (by linarith) one_pos, fun h hh hlt => ?_⟩
  have hε2 : |h| < 2 * ε := lt_of_lt_of_le hlt (min_le_left _ _)
  have h1 : |h| ≤ 1 := le_of_lt (lt_of_lt_of_le hlt (min_le_right _ _))
  have hhalf : |h / 2| = |h| / 2 := by
    rw [abs_div, abs_of_pos (by norm_num : (0 : ℝ) < 2)]
  have hpos2 : (0 : ℝ) < |h| / 2 := by linarith [hh]
  have hlt2 : |h / 2| < ε := by rw [hhalf]; linarith
  have b1 : |R (h / 2)| ≤ C * |h / 2| ^ (p + 1) :=
    hb (h / 2) (by rw [hhalf]; exact hpos2) hlt2
  have b2 : |R (-(h / 2))| ≤ C * |h / 2| ^ (p + 1) := by
    have h := hb (-(h / 2)) (by rw [abs_neg, hhalf]; exact hpos2) (by rw [abs_neg]; exact hlt2)
    simpa only [abs_neg] using h
  rw [abs_div, abs_of_pos (by norm_num : (0 : ℝ) < 2)]
  calc |R (h / 2) + R (-(h / 2))| / 2
      ≤ (|R (h / 2)| + |R (-(h / 2))|) / 2 := by
        have := abs_add_le (R (h / 2)) (R (-(h / 2))); linarith
    _ ≤ (C * |h / 2| ^ (p + 1) + C * |h / 2| ^ (p + 1)) / 2 := by linarith
    _ = C * (|h| / 2) ^ (p + 1) := by rw [hhalf]; ring
    _ ≤ C * |h| ^ p := by
        have h3 : (|h| / 2) ^ (p + 1) ≤ |h| ^ p := by
          calc (|h| / 2) ^ (p + 1) ≤ |h| ^ (p + 1) :=
                pow_le_pow_left₀ (by positivity) (by linarith [abs_nonneg h]) (p + 1)
            _ ≤ |h| ^ p := by
                rw [pow_succ]
                exact mul_le_of_le_one_right (pow_nonneg (abs_nonneg h) p) h1
        exact mul_le_mul_of_nonneg_left h3 hC

/-- The symmetrised difference quotient of an `O(|u|^{p+1})` remainder is `O(|h|^p)`. -/
theorem c11_powBound_symm_diff {p : ℕ} {R : ℝ → ℝ} (hR : PowBound (p + 1) R) :
    PowBound p (fun h : ℝ => (R (h / 2) - R (-(h / 2))) / h) := by
  obtain ⟨C, hC, ε, hε, hb⟩ := hR
  refine ⟨2 * C, by positivity, min (2 * ε) 1, lt_min (by linarith) one_pos, fun h hh hlt => ?_⟩
  have hε2 : |h| < 2 * ε := lt_of_lt_of_le hlt (min_le_left _ _)
  have hpos : (0 : ℝ) < |h| := hh
  have hhalf : |h / 2| = |h| / 2 := by
    rw [abs_div, abs_of_pos (by norm_num : (0 : ℝ) < 2)]
  have hpos2 : (0 : ℝ) < |h| / 2 := by linarith [hh]
  have hlt2 : |h / 2| < ε := by rw [hhalf]; linarith
  have b1 : |R (h / 2)| ≤ C * |h / 2| ^ (p + 1) :=
    hb (h / 2) (by rw [hhalf]; exact hpos2) hlt2
  have b2 : |R (-(h / 2))| ≤ C * |h / 2| ^ (p + 1) := by
    have h := hb (-(h / 2)) (by rw [abs_neg, hhalf]; exact hpos2) (by rw [abs_neg]; exact hlt2)
    simpa only [abs_neg] using h
  rw [abs_div, div_le_iff₀ hpos]
  calc |R (h / 2) - R (-(h / 2))|
      ≤ |R (h / 2)| + |R (-(h / 2))| := by
        calc |R (h / 2) - R (-(h / 2))| = |R (h / 2) + -R (-(h / 2))| := by rw [sub_eq_add_neg]
          _ ≤ |R (h / 2)| + |-R (-(h / 2))| := abs_add_le _ _
          _ = |R (h / 2)| + |R (-(h / 2))| := by rw [abs_neg]
    _ ≤ C * |h / 2| ^ (p + 1) + C * |h / 2| ^ (p + 1) := add_le_add b1 b2
    _ = 2 * C * (|h| / 2) ^ (p + 1) := by rw [hhalf]; ring
    _ ≤ 2 * C * |h| ^ (p + 1) := by
        have h3 : (|h| / 2) ^ (p + 1) ≤ |h| ^ (p + 1) :=
          pow_le_pow_left₀ (by positivity) (by linarith [abs_nonneg h]) (p + 1)
        exact mul_le_mul_of_nonneg_left h3 (by positivity)
    _ = 2 * C * |h| ^ p * |h| := by rw [pow_succ]; ring

/-! ## Calculus infrastructure (locally re-derived; the same chain as in `PkgContinuous`) -/

private lemma c11_top_ne_zero : (⊤ : WithTop ENat) ≠ 0 :=
  ENat.one_le_iff_ne_zero_withTop.mp le_top

private lemma c11_hasDerivAt_fst (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    HasDerivAt (fun x' => W (x', b)) (fderiv ℝ W (a, b) (1, 0)) a := by
  have hγ : HasFDerivAt (fun x' : ℝ => (x', b)) (ContinuousLinearMap.inl ℝ ℝ ℝ) a :=
    hasFDerivAt_prodMk_left a b
  have h : HasFDerivAt (fun x' : ℝ => W (x', b))
      ((fderiv ℝ W (a, b)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ)) a :=
    hW.comp a hγ
  exact h.hasDerivAt

private lemma c11_hasDerivAt_snd (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    HasDerivAt (fun y' => W (a, y')) (fderiv ℝ W (a, b) (0, 1)) b := by
  have hγ : HasFDerivAt (fun y' : ℝ => (a, y')) (ContinuousLinearMap.inr ℝ ℝ ℝ) b :=
    hasFDerivAt_prodMk_right a b
  have h : HasFDerivAt (fun y' : ℝ => W (a, y'))
      ((fderiv ℝ W (a, b)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ)) b :=
    hW.comp b hγ
  exact h.hasDerivAt

private lemma c11_deriv_fst (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    deriv (fun x' => W (x', b)) a = fderiv ℝ W (a, b) (1, 0) :=
  (c11_hasDerivAt_fst W a b hW).deriv

private lemma c11_deriv_snd (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    deriv (fun y' => W (a, y')) b = fderiv ℝ W (a, b) (0, 1) :=
  (c11_hasDerivAt_snd W a b hW).deriv

private lemma c11_smooth_partial_fst (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) :=
  (hW.fderiv_right (m := ⊤) le_top).clm_apply
    (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ))))

private lemma c11_fderiv_partial_comm {W : ℝ × ℝ → ℝ} (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0) := by
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable c11_top_ne_zero
  have hsymm : IsSymmSndFDerivAt ℝ W (x, y) :=
    hW.contDiffAt.isSymmSndFDerivAt (by simp)
  have e1 : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = fderiv ℝ (fderiv ℝ W) (x, y) ((0 : ℝ), (1 : ℝ)) ((1 : ℝ), (0 : ℝ)) := by
    rw [fderiv_clm_apply (c := fderiv ℝ W) (u := fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ)))
      (hdFW (x, y)) (differentiableAt_const _)]
    simp [fderiv_const_apply, ContinuousLinearMap.flip_apply]
  have e2 : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0)
      = fderiv ℝ (fderiv ℝ W) (x, y) ((1 : ℝ), (0 : ℝ)) ((0 : ℝ), (1 : ℝ)) := by
    rw [fderiv_clm_apply (c := fderiv ℝ W) (u := fun _ : ℝ × ℝ => ((0 : ℝ), (1 : ℝ)))
      (hdFW (x, y)) (differentiableAt_const _)]
    simp [fderiv_const_apply, ContinuousLinearMap.flip_apply]
  rw [e1, e2]
  exact hsymm.eq ((0 : ℝ), (1 : ℝ)) ((1 : ℝ), (0 : ℝ))

private lemma c11_diff_snd_family (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    DifferentiableAt ℝ (fun y' => deriv (fun x' => W (x', y')) x) y := by
  have hdW : Differentiable ℝ W := hW.differentiable c11_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable c11_top_ne_zero
  have hP : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have h : DifferentiableAt ℝ (fun y' => fderiv ℝ W (x, y') (1, 0)) y :=
    (c11_hasDerivAt_snd (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) x y hP.hasFDerivAt).differentiableAt
  have hfun : (fun y' : ℝ => fderiv ℝ W (x, y') (1, 0))
      = (fun y' => deriv (fun x' => W (x', y')) x) :=
    funext fun y' => (c11_deriv_fst W x y' (hdW (x, y')).hasFDerivAt).symm
  rwa [hfun] at h

private lemma c11_diff_fst_family (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    DifferentiableAt ℝ (fun x' => deriv (fun y' => W (x', y')) y) x := by
  have hdW : Differentiable ℝ W := hW.differentiable c11_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable c11_top_ne_zero
  have hQ : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have h : DifferentiableAt ℝ (fun x' => fderiv ℝ W (x', y) (0, 1)) x :=
    (c11_hasDerivAt_fst (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) x y hQ.hasFDerivAt).differentiableAt
  have hfun : (fun x' : ℝ => fderiv ℝ W (x', y) (0, 1))
      = (fun x' => deriv (fun y' => W (x', y')) y) :=
    funext fun x' => (c11_deriv_snd W x' y (hdW (x', y)).hasFDerivAt).symm
  rwa [hfun] at h

private lemma c11_clairaut_of {W : ℝ × ℝ → ℝ}
    (hdW : Differentiable ℝ W) (hdFW : Differentiable ℝ (fderiv ℝ W))
    (hsymm : ∀ p, IsSymmSndFDerivAt ℝ W p) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => W (x', y')) x) y
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x := by
  have hP : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have hQ : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have key : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0) := by
    have e1 : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
        = fderiv ℝ (fderiv ℝ W) (x, y) ((0 : ℝ), (1 : ℝ)) ((1 : ℝ), (0 : ℝ)) := by
      rw [fderiv_clm_apply (c := fderiv ℝ W) (u := fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ)))
        (hdFW (x, y)) (differentiableAt_const _)]
      simp [fderiv_const_apply, ContinuousLinearMap.flip_apply]
    have e2 : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0)
        = fderiv ℝ (fderiv ℝ W) (x, y) ((1 : ℝ), (0 : ℝ)) ((0 : ℝ), (1 : ℝ)) := by
      rw [fderiv_clm_apply (c := fderiv ℝ W) (u := fun _ : ℝ × ℝ => ((0 : ℝ), (1 : ℝ)))
        (hdFW (x, y)) (differentiableAt_const _)]
      simp [fderiv_const_apply, ContinuousLinearMap.flip_apply]
    rw [e1, e2]
    exact (hsymm (x, y)).eq ((0 : ℝ), (1 : ℝ)) ((1 : ℝ), (0 : ℝ))
  have hPval : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = deriv (fun y' => deriv (fun x' => W (x', y')) x) y := by
    rw [← (c11_hasDerivAt_snd (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) x y hP.hasFDerivAt).deriv]
    congr 1
    funext y'
    exact (c11_deriv_fst W x y' (hdW (x, y')).hasFDerivAt).symm
  have hQval : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0)
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x := by
    rw [← (c11_hasDerivAt_fst (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) x y hQ.hasFDerivAt).deriv]
    congr 1
    funext x'
    exact (c11_deriv_snd W x' y (hdW (x', y)).hasFDerivAt).symm
  rw [← hPval, key, hQval]

/-- **Two-variable Clairaut**, `C^∞` form. -/
private lemma c11_clairaut {W : ℝ × ℝ → ℝ} (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => W (x', y')) x) y
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x :=
  c11_clairaut_of (hW.differentiable c11_top_ne_zero)
    ((hW.fderiv_right (m := ⊤) le_top).differentiable c11_top_ne_zero)
    (fun p => hW.contDiffAt.isSymmSndFDerivAt (by simp)) x y

/-! ## Slices of a smooth `XYT` -/

private lemma c11_smooth_fixed_t (f : XYT) (hf : Smooth3 f) (t : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f p.1 p.2 t) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (p.1, (p.2, t))) := by fun_prop
  exact hf.comp hg

private lemma c11_smooth_fixed_x (f : XYT) (hf : Smooth3 f) (x : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f x p.1 p.2) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (x, (p.1, p.2))) := by fun_prop
  exact hf.comp hg

private lemma c11_jet1 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => W (x, y')) (deriv (fun b => W (x, b)) y) y := by
  have hdW : Differentiable ℝ W := hW.differentiable c11_top_ne_zero
  have h : HasDerivAt (fun y' => W (x, y')) (fderiv ℝ W (x, y) (0, 1)) y :=
    c11_hasDerivAt_snd W x y (hdW (x, y)).hasFDerivAt
  rw [← c11_deriv_snd W x y (hdW (x, y)).hasFDerivAt] at h
  exact h

private lemma c11_jet2 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => deriv (fun a => W (a, y')) x)
      (deriv (fun a => deriv (fun b => W (a, b)) y) x) y := by
  have h := (c11_diff_snd_family W hW x y).hasDerivAt
  rw [c11_clairaut hW x y] at h
  exact h

private lemma c11_jet3 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => deriv (fun a => deriv (fun b => W (b, y')) a) x)
      (deriv (fun a => deriv (fun b => deriv (fun c => W (b, c)) y) a) x) y := by
  have hdW : Differentiable ℝ W := hW.differentiable c11_top_ne_zero
  have hP : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) := c11_smooth_partial_fst W hW
  have hfun : (fun y' : ℝ => deriv (fun a => fderiv ℝ W (a, y') (1, 0)) x)
      = (fun y' => deriv (fun a => deriv (fun b => W (b, y')) a) x) := by
    funext y'
    congr 1
    funext a
    exact (c11_deriv_fst W a y' (hdW (a, y')).hasFDerivAt).symm
  rw [← hfun]
  have h := (c11_diff_snd_family (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) hP x y).hasDerivAt
  rw [c11_clairaut hP x y] at h
  refine h.congr_deriv ?_
  apply congrArg (fun F : ℝ → ℝ => deriv F x)
  funext a
  rw [show (fun y' : ℝ => fderiv ℝ W (a, y') (1, 0))
      = (fun y' => deriv (fun b => W (b, y')) a) from
    funext fun y' => (c11_deriv_fst W a y' (hdW (a, y')).hasFDerivAt).symm]
  exact c11_clairaut hW a y

private lemma c11_jet4 (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ ⊤ V) (y t : ℝ) :
    HasDerivAt (fun y' => deriv (fun s => V (y', s)) t)
      (deriv (fun s => deriv (fun a => V (a, s)) y) t) y := by
  have h := (c11_diff_fst_family V hV y t).hasDerivAt
  rw [← c11_clairaut hV y t] at h
  exact h

/-- The four `y`-derivatives of the jets of `y' ↦ slice f y'`. -/
private lemma c11_slice_jets (f : XYT) (hf : Smooth3 f) (x y t : ℝ) :
    HasDerivAt (fun y' => f x y' t) (sy f x y t) y ∧
    HasDerivAt (fun y' => dx (slice f y') x t) (dx (slice (sy f) y) x t) y ∧
    HasDerivAt (fun y' => xx (slice f y') x t) (xx (slice (sy f) y) x t) y ∧
    HasDerivAt (fun y' => dt (slice f y') x t) (dt (slice (sy f) y) x t) y :=
  ⟨c11_jet1 (fun p : ℝ × ℝ => f p.1 p.2 t) (c11_smooth_fixed_t f hf t) x y,
   c11_jet2 (fun p : ℝ × ℝ => f p.1 p.2 t) (c11_smooth_fixed_t f hf t) x y,
   c11_jet3 (fun p : ℝ × ℝ => f p.1 p.2 t) (c11_smooth_fixed_t f hf t) x y,
   c11_jet4 (fun p : ℝ × ℝ => f x p.1 p.2) (c11_smooth_fixed_x f hf x) y t⟩

/-- The slice family `y' ↦ slice g y' x t` is smooth. -/
private lemma c11_smooth_slice (g : XYT) (hg : Smooth3 g) (x t : ℝ) :
    ContDiff ℝ ⊤ (fun y' : ℝ => slice g y' x t) := by
  have hW : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => g p.1 p.2 t) := c11_smooth_fixed_t g hg t
  exact hW.comp (contDiff_prodMk_right (e₀ := x))

/-- The slice family of `∂_x` is smooth. -/
private lemma c11_smooth_dx_slice (g : XYT) (hg : Smooth3 g) (x t : ℝ) :
    ContDiff ℝ ⊤ (fun y' : ℝ => dx (slice g y') x t) := by
  have hW : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => g p.1 p.2 t) := c11_smooth_fixed_t g hg t
  have hV : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) p) (1, 0)) :=
    c11_smooth_partial_fst _ hW
  have hfun : (fun y' : ℝ => dx (slice g y') x t)
      = fun y' => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) (x, y')) (1, 0) := by
    funext y'
    show deriv (fun z : ℝ => g z y' t) x = _
    exact c11_deriv_fst (fun q : ℝ × ℝ => g q.1 q.2 t) x y'
      ((c11_smooth_fixed_t g hg t).differentiable c11_top_ne_zero (x, y')).hasFDerivAt
  rw [hfun]
  exact hV.comp (contDiff_prodMk_right (e₀ := x))

/-- The slice family of `∂_x²` is smooth. -/
private lemma c11_smooth_xx_slice (g : XYT) (hg : Smooth3 g) (x t : ℝ) :
    ContDiff ℝ ⊤ (fun y' : ℝ => xx (slice g y') x t) := by
  have hW : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => g p.1 p.2 t) := c11_smooth_fixed_t g hg t
  have hdW : Differentiable ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) :=
    hW.differentiable c11_top_ne_zero
  have hV : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) p) (1, 0)) :=
    c11_smooth_partial_fst _ hW
  have hV2 : ContDiff ℝ ⊤
      (fun p : ℝ × ℝ =>
        (fderiv ℝ (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) p) (1, 0)) p)
          (1, 0)) :=
    c11_smooth_partial_fst _ hV
  have hfun : (fun y' : ℝ => xx (slice g y') x t)
      = fun y' => (fderiv ℝ
          (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) p) (1, 0)) (x, y'))
          (1, 0) := by
    funext y'
    show deriv (fun z : ℝ => deriv (fun w : ℝ => g w y' t) z) x = _
    rw [show (fun z : ℝ => deriv (fun w : ℝ => g w y' t) z)
        = (fun z : ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) (z, y')) (1, 0)) from
      funext fun z => c11_deriv_fst (fun q : ℝ × ℝ => g q.1 q.2 t) z y'
        (hdW (z, y')).hasFDerivAt]
    exact c11_deriv_fst (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g q.1 q.2 t) p) (1, 0))
      x y' ((hV.differentiable c11_top_ne_zero) (x, y')).hasFDerivAt
  rw [hfun]
  exact hV2.comp (contDiff_prodMk_right (e₀ := x))

/-- The slice family of `∂_t` is smooth. -/
private lemma c11_smooth_dt_slice (g : XYT) (hg : Smooth3 g) (x t : ℝ) :
    ContDiff ℝ ⊤ (fun y' : ℝ => dt (slice g y') x t) := by
  have hU : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => g x p.1 p.2) := c11_smooth_fixed_x g hg x
  have hdU : Differentiable ℝ (fun q : ℝ × ℝ => g x q.1 q.2) :=
    hU.differentiable c11_top_ne_zero
  have hV : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (fderiv ℝ (fun q : ℝ × ℝ => g x q.1 q.2) p) (0, 1)) :=
    (hU.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × ℝ => ((0 : ℝ), (1 : ℝ))))
  have hfun : (fun y' : ℝ => dt (slice g y') x t)
      = fun y' => (fderiv ℝ (fun q : ℝ × ℝ => g x q.1 q.2) (y', t)) (0, 1) := by
    funext y'
    show deriv (fun s : ℝ => g x y' s) t = _
    exact c11_deriv_snd (fun q : ℝ × ℝ => g x q.1 q.2) y' t
      (hdU (y', t)).hasFDerivAt
  rw [hfun]
  exact hV.comp (contDiff_prodMk_left (f₀ := t))

/-! ## Target C11 -/

theorem c11_proved : C11 := by
  intro a f g hf hg x y t
  -- the one-parameter family whose Taylor expansion at `0` gives both conjuncts
  let Φ : ℝ → ℝ := fun s => bil (a + s) (slice f y) (slice g (y + s)) x t
  let F0 : ℝ → ℝ := fun y' => slice g y' x t
  let F1 : ℝ → ℝ := fun y' => dx (slice g y') x t
  let F2 : ℝ → ℝ := fun y' => xx (slice g y') x t
  let F3 : ℝ → ℝ := fun y' => dt (slice g y') x t
  let pxx : ℝ := xx (slice f y) x t
  let pdx : ℝ := dx (slice f y) x t
  let pp : ℝ := slice f y x t
  let pdt : ℝ := dt (slice f y) x t
  have hΦdef : Φ = fun s : ℝ => bil (a + s) (slice f y) (slice g (y + s)) x t := rfl
  -- `Φ` written out with the `s`-dependent and constant pieces separated
  have hΦexp : Φ = fun s : ℝ =>
      pxx * F0 (y + s) - 2 * (pdx * F1 (y + s)) + pp * F2 (y + s) + pdt * F0 (y + s)
        - pp * F3 (y + s) + (2 * (a + s)) * (pdx * F0 (y + s) - pp * F1 (y + s)) := by
    funext s
    rw [hΦdef]
    dsimp only [F0, F1, F2, F3, pxx, pdx, pp, pdt]
    simp only [bil, hx, Pi.mul_apply, Pi.sub_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul,
      c11_two_apply]
    ring
  -- `Φ` is `C^3`
  have hΦ3 : ContDiff ℝ 3 Φ := by
    have hF0c : ContDiff ℝ 3 F0 := (c11_smooth_slice g hg x t).of_le le_top
    have hF1c : ContDiff ℝ 3 F1 := (c11_smooth_dx_slice g hg x t).of_le le_top
    have hF2c : ContDiff ℝ 3 F2 := (c11_smooth_xx_slice g hg x t).of_le le_top
    have hF3c : ContDiff ℝ 3 F3 := (c11_smooth_dt_slice g hg x t).of_le le_top
    rw [hΦexp]
    fun_prop
  -- the `y`-jets of the slice family of `g`, shifted to the base point `0`
  have hF0' : HasDerivAt (fun s : ℝ => F0 (y + s)) ((slice (sy g) y) x t) 0 := by
    have hjet : HasDerivAt (fun y' : ℝ => g x y' t) (sy g x y t) (y + 0) := by
      simpa only [add_zero] using (c11_slice_jets g hg x y t).1
    show HasDerivAt (fun s : ℝ => g x (y + s) t) (sy g x y t) 0
    exact hjet.comp_const_add y 0
  have hF1' : HasDerivAt (fun s : ℝ => F1 (y + s)) ((dx (slice (sy g) y)) x t) 0 := by
    have hjet : HasDerivAt (fun y' : ℝ => dx (slice g y') x t) (dx (slice (sy g) y) x t) (y + 0) := by
      simpa only [add_zero] using (c11_slice_jets g hg x y t).2.1
    show HasDerivAt (fun s : ℝ => dx (slice g (y + s)) x t) (dx (slice (sy g) y) x t) 0
    exact hjet.comp_const_add y 0
  have hF2' : HasDerivAt (fun s : ℝ => F2 (y + s)) ((xx (slice (sy g) y)) x t) 0 := by
    have hjet : HasDerivAt (fun y' : ℝ => xx (slice g y') x t) (xx (slice (sy g) y) x t) (y + 0) := by
      simpa only [add_zero] using (c11_slice_jets g hg x y t).2.2.1
    show HasDerivAt (fun s : ℝ => xx (slice g (y + s)) x t) (xx (slice (sy g) y) x t) 0
    exact hjet.comp_const_add y 0
  have hF3' : HasDerivAt (fun s : ℝ => F3 (y + s)) ((dt (slice (sy g) y)) x t) 0 := by
    have hjet : HasDerivAt (fun y' : ℝ => dt (slice g y') x t) (dt (slice (sy g) y) x t) (y + 0) := by
      simpa only [add_zero] using (c11_slice_jets g hg x y t).2.2.2
    show HasDerivAt (fun s : ℝ => dt (slice g (y + s)) x t) (dt (slice (sy g) y) x t) 0
    exact hjet.comp_const_add y 0
  -- `Φ'(0)`, split as `bil` + the explicit `s`-dependence
  let Dexp : ℝ := pxx * ((slice (sy g) y) x t) - 2 * (pdx * ((dx (slice (sy g) y)) x t))
      + pp * ((xx (slice (sy g) y)) x t) + pdt * ((slice (sy g) y) x t)
      - pp * ((dt (slice (sy g) y)) x t)
      + (2 * (pdx * F0 (y + 0) - pp * F1 (y + 0))
         + (2 * (a + 0)) * (pdx * ((slice (sy g) y) x t) - pp * ((dx (slice (sy g) y)) x t)))
  have hDval : cbil a f (sy g) x y t + 2 * chx f g x y t = Dexp := by
    dsimp only [Dexp, pxx, pdx, pp, pdt, F0, F1]
    simp only [cbil, chx, bil, hx, Pi.mul_apply, Pi.sub_apply, Pi.add_apply, Pi.smul_apply,
      smul_eq_mul, c11_two_apply, add_zero]
    ring
  have hΦd : HasDerivAt Φ (cbil a f (sy g) x y t + 2 * chx f g x y t) 0 := by
    have hA : HasDerivAt (fun s : ℝ => pxx * F0 (y + s)) (pxx * ((slice (sy g) y) x t)) 0 :=
      hF0'.const_mul pxx
    have hB : HasDerivAt (fun s : ℝ => 2 * (pdx * F1 (y + s)))
        (2 * (pdx * ((dx (slice (sy g) y)) x t))) 0 :=
      (hF1'.const_mul pdx).const_mul 2
    have hC : HasDerivAt (fun s : ℝ => pp * F2 (y + s)) (pp * ((xx (slice (sy g) y)) x t)) 0 :=
      hF2'.const_mul pp
    have hD : HasDerivAt (fun s : ℝ => pdt * F0 (y + s)) (pdt * ((slice (sy g) y) x t)) 0 :=
      hF0'.const_mul pdt
    have hE : HasDerivAt (fun s : ℝ => pp * F3 (y + s)) (pp * ((dt (slice (sy g) y)) x t)) 0 :=
      hF3'.const_mul pp
    have hshift2 : HasDerivAt (fun s : ℝ => 2 * (a + s)) 2 0 := by
      have h1 : HasDerivAt (fun s : ℝ => a + s) 1 0 := (hasDerivAt_id (0 : ℝ)).const_add a
      simpa using h1.const_mul (2 : ℝ)
    have hlin : HasDerivAt (fun s : ℝ => pdx * F0 (y + s) - pp * F1 (y + s))
        (pdx * ((slice (sy g) y) x t) - pp * ((dx (slice (sy g) y)) x t)) 0 :=
      (hF0'.const_mul pdx).sub (hF1'.const_mul pp)
    have hF6 : HasDerivAt
        (fun s : ℝ => (2 * (a + s)) * (pdx * F0 (y + s) - pp * F1 (y + s)))
        (2 * (pdx * F0 (y + 0) - pp * F1 (y + 0))
          + (2 * (a + 0)) * (pdx * ((slice (sy g) y) x t) - pp * ((dx (slice (sy g) y)) x t))) 0 :=
      hshift2.mul hlin
    have hchain : HasDerivAt (fun s : ℝ =>
        pxx * F0 (y + s) - 2 * (pdx * F1 (y + s)) + pp * F2 (y + s) + pdt * F0 (y + s)
          - pp * F3 (y + s) + (2 * (a + s)) * (pdx * F0 (y + s) - pp * F1 (y + s))) Dexp 0 :=
      ((((hA.sub hB).add hC).add hD).sub hE).add hF6
    rw [hΦexp]
    exact hchain.congr_deriv hDval.symm
  have hderiv : deriv Φ 0 = cbil a f (sy g) x y t + 2 * chx f g x y t := hΦd.deriv
  -- the degree-2 Taylor remainder of `Φ` at `0`
  let R : ℝ → ℝ := fun u => Φ u - (Φ 0 + u * deriv Φ 0 + (u ^ 2 / 2) * deriv (deriv Φ) 0)
  have hT : ∀ u : ℝ, taylorWithinEval Φ 2 Set.univ 0 u
      = Φ 0 + u * deriv Φ 0 + (u ^ 2 / 2) * deriv (deriv Φ) 0 := by
    intro u
    rw [show taylorWithinEval Φ 2 Set.univ 0 u = taylorWithinEval Φ 2 Set.univ 0 (0 + u) by
      rw [zero_add]]
    rw [taylorWithinEval_eq_sum Φ 2 0 u]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, iteratedDeriv_zero,
      iteratedDeriv_one, iteratedDeriv_succ, Nat.factorial_zero, Nat.factorial_one,
      Nat.factorial_two, Nat.cast_one, Nat.cast_ofNat, inv_one, pow_zero, pow_one,
      one_mul, mul_one, one_smul, smul_eq_mul]
    ring
  have hRt : PowBound 3
      (fun u : ℝ => Φ (0 + u) - taylorWithinEval Φ 2 Set.univ 0 (0 + u)) :=
    c11_powBound_norm_abs (powBound_taylor_poly 2 Φ 0 hΦ3)
  have hR : PowBound 3 R := by
    refine powBound_congr (fun u => ?_) hRt
    dsimp only [R]
    rw [zero_add, hT u]
  -- the walls in terms of `Φ`
  have hwallP : ∀ h : ℝ, wallPlus a h y f g x t = Φ (h / 2) := fun h => rfl
  have hwallM : ∀ h : ℝ, wallMinus a h y f g x t = Φ (-(h / 2)) := by
    intro h
    have h1 : a - h / 2 = a + -(h / 2) := by rw [sub_eq_add_neg]
    have h2 : y - h / 2 = y + -(h / 2) := by rw [sub_eq_add_neg]
    dsimp only [wallMinus, Φ]
    simp only [h1, h2]
  have hcbil : cbil a f g x y t = Φ 0 := by
    dsimp only [cbil, Φ]
    simp only [add_zero]
  have hcbilSy : cbil a f (sy g) x y t + 2 * chx f g x y t = deriv Φ 0 := hderiv.symm
  constructor
  · -- first conjunct: the symmetrised average
    let P : ℝ → ℝ := fun h => (h ^ 2 / 8) * deriv (deriv Φ) 0
    let Q : ℝ → ℝ := fun h => (R (h / 2) + R (-(h / 2))) / 2
    have hP : PowBound 2 P := by
      dsimp only [P]
      exact c11_powBound_quad (deriv (deriv Φ) 0)
    have hQ : PowBound 2 Q := by
      dsimp only [Q]
      exact c11_powBound_symm_avg (p := 2) hR
    have hsum : PowBound 2 (fun h => P h + Q h) := c11_powBound_add hP hQ (fun h => rfl)
    refine c11_powBound_congr_ne ?_ hsum
    intro h _
    dsimp only [P, Q, R]
    rw [hwallP h, hwallM h, hcbil]
    ring
  · -- second conjunct: the symmetrised difference quotient
    let S : ℝ → ℝ := fun h => (R (h / 2) - R (-(h / 2))) / h
    have hS : PowBound 2 S := by
      dsimp only [S]
      exact c11_powBound_symm_diff (p := 2) hR
    refine c11_powBound_congr_ne ?_ hS
    intro h hh
    dsimp only [S, R]
    rw [hwallP h, hwallM h, hcbilSy]
    field_simp
    ring

end DLWContract
