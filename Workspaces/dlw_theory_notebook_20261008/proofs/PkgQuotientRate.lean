/-
Quotient / normalization-rate package.

Proves the three frozen targets `C13`, `C12`, `C24` declared in `Contracts.lean`.
No target statement is restated or altered here.
-/
import Contracts
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## Elementary calculus helpers -/

/-- `deriv` of a globally smooth real function is again globally smooth. -/
private lemma contDiff_deriv_top {f : ℝ → ℝ} (h : ContDiff ℝ ⊤ f) :
    ContDiff ℝ ⊤ (deriv f) :=
  ContDiff.deriv' (n := ⊤) (show ContDiff ℝ (⊤ + 1) f from h)

/-- A globally smooth real function is differentiable everywhere. -/
private lemma diffAt_of_contDiff {f : ℝ → ℝ} (h : ContDiff ℝ ⊤ f) (x : ℝ) :
    DifferentiableAt ℝ f x :=
  ((h.of_le le_top).differentiable_one).differentiableAt

/-- Slicing a smooth two-variable function in the second variable is smooth. -/
private lemma slice_cont {f : XT} (hf : SmoothXT f) (t : ℝ) :
    ContDiff ℝ ⊤ (fun x : ℝ => f x t) :=
  hf.comp (contDiff_prodMk_left t)

/-- Slicing a smooth two-variable function in the first variable is smooth. -/
private lemma slice_cont_t {f : XT} (hf : SmoothXT f) (x : ℝ) :
    ContDiff ℝ ⊤ (fun t : ℝ => f x t) :=
  hf.comp (contDiff_prodMk_right x)

/-! ## C13: normalized Hirota quotient identity -/

theorem c13_proved : C13 := by
  intro a f g hf hg hpos
  dsimp only
  set α : XT := fun x t => Real.log (f x t) with hα
  set β : XT := fun x t => Real.log (g x t) with hβ
  have hfT : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => f x t) := fun t => slice_cont hf t
  have hgT : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => g x t) := fun t => slice_cont hg t
  have hft : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => f x t) := fun x => slice_cont_t hf x
  have hgt : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => g x t) := fun x => slice_cont_t hg x
  have hαx : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => α x t) := by
    intro t
    have h : ContDiff ℝ ⊤ (fun x : ℝ => Real.log (f x t)) :=
      (hfT t).log (fun x => ne_of_gt (hpos x t).1)
    simpa [hα] using h
  have hβx : ∀ t, ContDiff ℝ ⊤ (fun x : ℝ => β x t) := by
    intro t
    have h : ContDiff ℝ ⊤ (fun x : ℝ => Real.log (g x t)) :=
      (hgT t).log (fun x => ne_of_gt (hpos x t).2)
    simpa [hβ] using h
  have hαt : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => α x t) := by
    intro x
    have h : ContDiff ℝ ⊤ (fun t : ℝ => Real.log (f x t)) :=
      (hft x).log (fun t => ne_of_gt (hpos x t).1)
    simpa [hα] using h
  have hβt : ∀ x, ContDiff ℝ ⊤ (fun t : ℝ => β x t) := by
    intro x
    have h : ContDiff ℝ ⊤ (fun t : ℝ => Real.log (g x t)) :=
      (hgt x).log (fun t => ne_of_gt (hpos x t).2)
    simpa [hβ] using h
  have hαxD : ∀ t, ContDiff ℝ ⊤ (deriv (fun x : ℝ => α x t)) := fun t =>
    contDiff_deriv_top (hαx t)
  have hβxD : ∀ t, ContDiff ℝ ⊤ (deriv (fun x : ℝ => β x t)) := fun t =>
    contDiff_deriv_top (hβx t)
  -- pointwise product identities for the logarithms
  have hdxf : ∀ x t, dx f x t = f x t * dx α x t := by
    intro x t
    have hfne : f x t ≠ 0 := ne_of_gt (hpos x t).1
    have h1 : HasDerivAt (fun z : ℝ => Real.log (f z t))
        (deriv (fun z : ℝ => f z t) x / f x t) x :=
      (diffAt_of_contDiff (hfT t) x).hasDerivAt.log hfne
    simp only [dx, hα]
    rw [h1.deriv]
    field_simp
  have hdxg : ∀ x t, dx g x t = g x t * dx β x t := by
    intro x t
    have hgne : g x t ≠ 0 := ne_of_gt (hpos x t).2
    have h1 : HasDerivAt (fun z : ℝ => Real.log (g z t))
        (deriv (fun z : ℝ => g z t) x / g x t) x :=
      (diffAt_of_contDiff (hgT t) x).hasDerivAt.log hgne
    simp only [dx, hβ]
    rw [h1.deriv]
    field_simp
  have hdtf : ∀ x t, dt f x t = f x t * dt α x t := by
    intro x t
    have hfne : f x t ≠ 0 := ne_of_gt (hpos x t).1
    have h1 : HasDerivAt (fun z : ℝ => Real.log (f x z))
        (deriv (f x) t / f x t) t :=
      (diffAt_of_contDiff (hft x) t).hasDerivAt.log hfne
    simp only [dt, hα]
    rw [h1.deriv]
    field_simp
  have hdtg : ∀ x t, dt g x t = g x t * dt β x t := by
    intro x t
    have hgne : g x t ≠ 0 := ne_of_gt (hpos x t).2
    have h1 : HasDerivAt (fun z : ℝ => Real.log (g x z))
        (deriv (g x) t / g x t) t :=
      (diffAt_of_contDiff (hgt x) t).hasDerivAt.log hgne
    simp only [dt, hβ]
    rw [h1.deriv]
    field_simp
  have hxxf : ∀ x t, xx f x t = f x t * (xx α x t + (dx α x t) ^ 2) := by
    intro x t
    have hfun : (fun z : ℝ => dx f z t) = ((fun z : ℝ => f z t) * (fun z : ℝ => dx α z t)) := by
      funext z
      simp only [Pi.mul_apply]
      exact hdxf z t
    have hd1 : DifferentiableAt ℝ (fun z : ℝ => f z t) x := diffAt_of_contDiff (hfT t) x
    have hd2 : DifferentiableAt ℝ (fun z : ℝ => dx α z t) x :=
      diffAt_of_contDiff (hαxD t) x
    have hmul : deriv ((fun z : ℝ => f z t) * (fun z : ℝ => dx α z t)) x
        = dx f x t * dx α x t + f x t * xx α x t := by
      have h := deriv_mul hd1 hd2
      simpa only [dx, xx] using h
    calc xx f x t = deriv (fun z : ℝ => dx f z t) x := rfl
      _ = deriv ((fun z : ℝ => f z t) * (fun z : ℝ => dx α z t)) x := by rw [hfun]
      _ = dx f x t * dx α x t + f x t * xx α x t := hmul
      _ = f x t * (xx α x t + (dx α x t) ^ 2) := by
            rw [hdxf x t]
            ring
  have hxxg : ∀ x t, xx g x t = g x t * (xx β x t + (dx β x t) ^ 2) := by
    intro x t
    have hfun : (fun z : ℝ => dx g z t) = ((fun z : ℝ => g z t) * (fun z : ℝ => dx β z t)) := by
      funext z
      simp only [Pi.mul_apply]
      exact hdxg z t
    have hd1 : DifferentiableAt ℝ (fun z : ℝ => g z t) x := diffAt_of_contDiff (hgT t) x
    have hd2 : DifferentiableAt ℝ (fun z : ℝ => dx β z t) x :=
      diffAt_of_contDiff (hβxD t) x
    have hmul : deriv ((fun z : ℝ => g z t) * (fun z : ℝ => dx β z t)) x
        = dx g x t * dx β x t + g x t * xx β x t := by
      have h := deriv_mul hd1 hd2
      simpa only [dx, xx] using h
    calc xx g x t = deriv (fun z : ℝ => dx g z t) x := rfl
      _ = deriv ((fun z : ℝ => g z t) * (fun z : ℝ => dx β z t)) x := by rw [hfun]
      _ = dx g x t * dx β x t + g x t * xx β x t := hmul
      _ = g x t * (xx β x t + (dx β x t) ^ 2) := by
            rw [hdxg x t]
            ring
  -- linearity of `dx`/`dt`/`xx`
  have hdxadd : dx (α + β) = dx α + dx β := by
    funext x t
    simp only [dx, Pi.add_apply]
    exact deriv_add (diffAt_of_contDiff (hαx t) x) (diffAt_of_contDiff (hβx t) x)
  have hdxsub : dx (α - β) = dx α - dx β := by
    funext x t
    simp only [dx, Pi.sub_apply]
    exact deriv_sub (diffAt_of_contDiff (hαx t) x) (diffAt_of_contDiff (hβx t) x)
  have hdtsub : dt (α - β) = dt α - dt β := by
    funext x t
    simp only [dt, Pi.sub_apply]
    exact deriv_sub (diffAt_of_contDiff (hαt x) t) (diffAt_of_contDiff (hβt x) t)
  have hxxadd : xx (α + β) = xx α + xx β := by
    funext x t
    have h1 : (fun z : ℝ => deriv (fun w : ℝ => α w t + β w t) z)
        = (fun z : ℝ => deriv (fun w : ℝ => α w t) z + deriv (fun w : ℝ => β w t) z) := by
      funext z
      exact deriv_add (diffAt_of_contDiff (hαx t) z) (diffAt_of_contDiff (hβx t) z)
    simp only [xx, dx, Pi.add_apply]
    rw [h1]
    exact deriv_add (diffAt_of_contDiff (hαxD t) x) (diffAt_of_contDiff (hβxD t) x)
  -- the pointwise algebraic identity
  funext x t
  have e1 : xx (α + β) x t = xx α x t + xx β x t := by simp only [hxxadd, Pi.add_apply]
  have e2 : dx (α - β) x t = dx α x t - dx β x t := by simp only [hdxsub, Pi.sub_apply]
  have e3 : dt (α - β) x t = dt α x t - dt β x t := by simp only [hdtsub, Pi.sub_apply]
  simp only [bil, hx, Pi.div_apply, Pi.mul_apply, Pi.sub_apply, Pi.add_apply, Pi.pow_apply,
    Pi.smul_apply, Pi.ofNat_apply, smul_eq_mul]
  rw [e1, e2, e3, hxxf x t, hxxg x t, hdxf x t, hdxg x t, hdtf x t, hdtg x t]
  rw [div_eq_iff (ne_of_gt (mul_pos (hpos x t).1 (hpos x t).2))]
  ring

/-! ## C12: second-order rate of the Lamé normalization -/

private lemma lam_den_ne (P : ℝ) (hP : P ≠ 0) {s : ℝ} (hs : |s| < |P|) : P - s / 2 ≠ 0 := by
  intro h0
  have hsp : s / 2 = P := by linarith
  have h1 : |s / 2| = |P| := by rw [hsp]
  have h2 : |s / 2| = |s| / 2 := by rw [abs_div]; norm_num
  rw [h2] at h1
  linarith [abs_pos.mpr hP]

private lemma lam_num_ne (P : ℝ) (hP : P ≠ 0) {s : ℝ} (hs : |s| < |P|) : P + s / 2 ≠ 0 := by
  intro h0
  have hsp : s / 2 = -P := by linarith
  have h1 : |s / 2| = |P| := by rw [hsp, abs_neg]
  have h2 : |s / 2| = |s| / 2 := by rw [abs_div]; norm_num
  rw [h2] at h1
  linarith [abs_pos.mpr hP]

private lemma lam_sq_ne (P : ℝ) (_hP : P ≠ 0) {s : ℝ} (hs : |s| < |P|) :
    P ^ 2 - s ^ 2 / 4 ≠ 0 := by
  have h1 : |s| ^ 2 < |P| ^ 2 := by nlinarith [abs_nonneg s, abs_nonneg P]
  rw [sq_abs, sq_abs] at h1
  exact ne_of_gt (by nlinarith [sq_nonneg s] : (0 : ℝ) < P ^ 2 - s ^ 2 / 4)

private lemma lam_hasDerivAt (P : ℝ) (hP : P ≠ 0) {s : ℝ} (hs : |s| < |P|) :
    HasDerivAt (fun u : ℝ => Real.log (lam u P)) (P / ((P + s / 2) * (P - s / 2))) s := by
  have hB : P - s / 2 ≠ 0 := lam_den_ne P hP hs
  have hA : P + s / 2 ≠ 0 := lam_num_ne P hP hs
  have h1 : HasDerivAt (fun u : ℝ => P + u / 2) (1 / 2) s := by
    have hi : HasDerivAt (fun u : ℝ => u / 2) (1 / 2) s :=
      (hasDerivAt_id' (x := s)).div_const 2
    have hc : HasDerivAt (fun _ : ℝ => P) (0 : ℝ) s := hasDerivAt_const (c := P) (x := s)
    refine (hc.add hi).congr_deriv ?_
    norm_num
  have h2 : HasDerivAt (fun u : ℝ => P - u / 2) (-(1 / 2)) s := by
    have hi : HasDerivAt (fun u : ℝ => u / 2) (1 / 2) s :=
      (hasDerivAt_id' (x := s)).div_const 2
    have hc : HasDerivAt (fun _ : ℝ => P) (0 : ℝ) s := hasDerivAt_const (c := P) (x := s)
    refine (hc.sub hi).congr_deriv ?_
    norm_num
  have h3 : HasDerivAt (fun u : ℝ => (P + u / 2) / (P - u / 2)) (P / (P - s / 2) ^ 2) s := by
    refine (h1.div h2 hB).congr_deriv ?_
    have hsq : (P - s / 2) ^ 2 ≠ 0 := pow_ne_zero 2 hB
    rw [div_eq_div_iff hsq hsq]
    ring
  have h4 : HasDerivAt (fun u : ℝ => Real.log ((P + u / 2) / (P - u / 2)))
      ((P / (P - s / 2) ^ 2) / ((P + s / 2) / (P - s / 2))) s :=
    h3.log (div_ne_zero hA hB)
  refine h4.congr_deriv ?_
  have hlam : (P + s / 2) / (P - s / 2) ≠ 0 := div_ne_zero hA hB
  have hsq : (P - s / 2) ^ 2 ≠ 0 := pow_ne_zero 2 hB
  have hprod : (P + s / 2) * (P - s / 2) ≠ 0 := mul_ne_zero hA hB
  field_simp [hB, hA, hlam, hsq, hprod]

theorem c12_proved : C12 := by
  intro P hP
  have hPpos : 0 < |P| := abs_pos.mpr hP
  refine ⟨1 / (2 * |P| ^ 3), by positivity, |P| / 2, by positivity, ?_⟩
  intro h hhpos hhlt
  dsimp only
  have hne : h ≠ 0 := abs_pos.mp hhpos
  set L : ℝ → ℝ := fun u => Real.log (lam u P) with hL
  have hL0 : L 0 = 0 := by
    rw [hL]
    dsimp only
    have h1 : lam 0 P = 1 := by
      simp only [lam, zero_div, add_zero, sub_zero]
      exact div_self hP
    rw [h1, Real.log_one]
  have hle : |h| < |P| := by linarith
  have hLh : Real.log (lam h P) = L h := by rw [hL]
  rw [hLh]
  rcases lt_or_gt_of_ne hne with hneg | hpos
  · have hsub : ∀ s ∈ Set.Icc h 0, |s| < |P| := by
      intro s hs
      have h1 : |s| = -s := abs_of_nonpos hs.2
      have h2 : |h| = -h := abs_of_neg hneg
      rw [h1]
      linarith [h2, hle, hs.1]
    have hcont : ContinuousOn L (Set.Icc h 0) := by
      apply DifferentiableOn.continuousOn (𝕜 := ℝ)
      intro s hs
      exact ((lam_hasDerivAt P hP (hsub s hs)).differentiableAt).differentiableWithinAt
    have hdiff : DifferentiableOn ℝ L (Set.Ioo h 0) := by
      intro s hs
      exact ((lam_hasDerivAt P hP (hsub s (Set.Ioo_subset_Icc_self hs))).differentiableAt).differentiableWithinAt
    obtain ⟨c, hc, hcd⟩ := exists_deriv_eq_slope L hneg hcont hdiff
    have hcabs : |c| < |h| := by
      rw [abs_of_neg hc.2, abs_of_neg hneg]
      linarith [hc.1]
    have hclt : |c| < |P| := lt_trans hcabs hle
    have hder : deriv L c = P / ((P + c / 2) * (P - c / 2)) := by
      rw [hL]
      exact (lam_hasDerivAt P hP hclt).deriv
    have h1 : deriv L c * h = L h - L 0 := by
      rw [hcd]
      have hz : (0 : ℝ) - h ≠ 0 := by linarith
      field_simp [hz]
      ring
    have hLh' : L h = deriv L c * h := by rw [h1, hL0, sub_zero]
    have heq : L h / h - 1 / P = deriv L c - 1 / P := by
      rw [hLh', mul_div_cancel_right₀ (deriv L c) hne]
    have hval : deriv L c - 1 / P = c ^ 2 / (4 * P * (P ^ 2 - c ^ 2 / 4)) := by
      have hA : P + c / 2 ≠ 0 := lam_num_ne P hP hclt
      have hB : P - c / 2 ≠ 0 := lam_den_ne P hP hclt
      have hC : P ^ 2 - c ^ 2 / 4 ≠ 0 := lam_sq_ne P hP hclt
      have hAB : (P + c / 2) * (P - c / 2) ≠ 0 := mul_ne_zero hA hB
      have hPC : 4 * P * (P ^ 2 - c ^ 2 / 4) ≠ 0 :=
        mul_ne_zero (mul_ne_zero (by norm_num) hP) hC
      rw [hder, div_sub_div P 1 hAB hP, div_eq_div_iff (mul_ne_zero hAB hP) hPC]
      ring
    have hch : c ^ 2 ≤ h ^ 2 := (sq_le_sq (a := c) (b := h)).mpr (le_of_lt hcabs)
    have hh2 : h ^ 2 < P ^ 2 / 4 := by
      have h2 : h ^ 2 < (P / 2) ^ 2 := by
        rw [sq_lt_sq, abs_div]
        norm_num
        exact hhlt
      nlinarith [h2]
    have hPsq : 0 < P ^ 2 := sq_pos_of_ne_zero hP
    have hA2 : P ^ 2 / 2 ≤ P ^ 2 - c ^ 2 / 4 := by nlinarith [hch, hh2, hPsq]
    have hApos : 0 < P ^ 2 - c ^ 2 / 4 := by linarith [hA2, hPsq]
    have hAbl : (0 : ℝ) < 4 * |P| * (P ^ 2 - c ^ 2 / 4) :=
      mul_pos (mul_pos (by norm_num) hPpos) hApos
    have hAb2 : (0 : ℝ) < 4 * |P| * (P ^ 2 / 2) :=
      mul_pos (mul_pos (by norm_num) hPpos) (by linarith [hPsq])
    have habs : |c ^ 2 / (4 * P * (P ^ 2 - c ^ 2 / 4))|
        = c ^ 2 / (4 * |P| * (P ^ 2 - c ^ 2 / 4)) := by
      rw [abs_div, abs_of_nonneg (sq_nonneg c), abs_mul, abs_mul,
        abs_of_pos (by norm_num : (0 : ℝ) < 4), abs_of_pos hApos]
    rw [heq, hval, habs]
    have hden : 4 * |P| * (P ^ 2 / 2) ≤ 4 * |P| * (P ^ 2 - c ^ 2 / 4) := by
      have h1 : (0 : ℝ) ≤ |P| := abs_nonneg P
      have h2 : 4 * (P ^ 2 / 2) ≤ 4 * (P ^ 2 - c ^ 2 / 4) := by linarith
      calc 4 * |P| * (P ^ 2 / 2) = |P| * (4 * (P ^ 2 / 2)) := by ring
        _ ≤ |P| * (4 * (P ^ 2 - c ^ 2 / 4)) := mul_le_mul_of_nonneg_left h2 h1
        _ = 4 * |P| * (P ^ 2 - c ^ 2 / 4) := by ring
    calc c ^ 2 / (4 * |P| * (P ^ 2 - c ^ 2 / 4))
        ≤ h ^ 2 / (4 * |P| * (P ^ 2 - c ^ 2 / 4)) :=
          div_le_div_of_nonneg_right hch (le_of_lt hAbl)
      _ ≤ h ^ 2 / (4 * |P| * (P ^ 2 / 2)) :=
          div_le_div_of_nonneg_left (sq_nonneg h) hAb2 hden
      _ = 1 / (2 * |P| ^ 3) * |h| ^ 2 := by
          have hsq : |P| ^ 2 = P ^ 2 := sq_abs P
          have he : 4 * |P| * (P ^ 2 / 2) = 2 * |P| ^ 3 := by
            rw [← hsq]
            ring
          rw [he, sq_abs h, one_div, div_eq_mul_inv,
            mul_comm (h ^ 2) ((2 * |P| ^ 3)⁻¹)]
  · have hsub : ∀ s ∈ Set.Icc 0 h, |s| < |P| := by
      intro s hs
      have h1 : |s| = s := abs_of_nonneg hs.1
      have h2 : |h| = h := abs_of_pos hpos
      rw [h1]
      linarith [h2, hle, hs.2]
    have hcont : ContinuousOn L (Set.Icc 0 h) := by
      apply DifferentiableOn.continuousOn (𝕜 := ℝ)
      intro s hs
      exact ((lam_hasDerivAt P hP (hsub s hs)).differentiableAt).differentiableWithinAt
    have hdiff : DifferentiableOn ℝ L (Set.Ioo 0 h) := by
      intro s hs
      exact ((lam_hasDerivAt P hP (hsub s (Set.Ioo_subset_Icc_self hs))).differentiableAt).differentiableWithinAt
    obtain ⟨c, hc, hcd⟩ := exists_deriv_eq_slope L hpos hcont hdiff
    have hcabs : |c| < |h| := by
      rw [abs_of_pos hc.1, abs_of_pos hpos]
      exact hc.2
    have hclt : |c| < |P| := lt_trans hcabs hle
    have hder : deriv L c = P / ((P + c / 2) * (P - c / 2)) := by
      rw [hL]
      exact (lam_hasDerivAt P hP hclt).deriv
    have h1 : deriv L c * h = L h - L 0 := by
      rw [hcd]
      have hz : h - 0 ≠ 0 := by linarith
      field_simp [hz]
      ring
    have hLh' : L h = deriv L c * h := by rw [h1, hL0, sub_zero]
    have heq : L h / h - 1 / P = deriv L c - 1 / P := by
      rw [hLh', mul_div_cancel_right₀ (deriv L c) hne]
    have hval : deriv L c - 1 / P = c ^ 2 / (4 * P * (P ^ 2 - c ^ 2 / 4)) := by
      have hA : P + c / 2 ≠ 0 := lam_num_ne P hP hclt
      have hB : P - c / 2 ≠ 0 := lam_den_ne P hP hclt
      have hC : P ^ 2 - c ^ 2 / 4 ≠ 0 := lam_sq_ne P hP hclt
      have hAB : (P + c / 2) * (P - c / 2) ≠ 0 := mul_ne_zero hA hB
      have hPC : 4 * P * (P ^ 2 - c ^ 2 / 4) ≠ 0 :=
        mul_ne_zero (mul_ne_zero (by norm_num) hP) hC
      rw [hder, div_sub_div P 1 hAB hP, div_eq_div_iff (mul_ne_zero hAB hP) hPC]
      ring
    have hch : c ^ 2 ≤ h ^ 2 := (sq_le_sq (a := c) (b := h)).mpr (le_of_lt hcabs)
    have hh2 : h ^ 2 < P ^ 2 / 4 := by
      have h2 : h ^ 2 < (P / 2) ^ 2 := by
        rw [sq_lt_sq, abs_div]
        norm_num
        exact hhlt
      nlinarith [h2]
    have hPsq : 0 < P ^ 2 := sq_pos_of_ne_zero hP
    have hA2 : P ^ 2 / 2 ≤ P ^ 2 - c ^ 2 / 4 := by nlinarith [hch, hh2, hPsq]
    have hApos : 0 < P ^ 2 - c ^ 2 / 4 := by linarith [hA2, hPsq]
    have hAbl : (0 : ℝ) < 4 * |P| * (P ^ 2 - c ^ 2 / 4) :=
      mul_pos (mul_pos (by norm_num) hPpos) hApos
    have hAb2 : (0 : ℝ) < 4 * |P| * (P ^ 2 / 2) :=
      mul_pos (mul_pos (by norm_num) hPpos) (by linarith [hPsq])
    have habs : |c ^ 2 / (4 * P * (P ^ 2 - c ^ 2 / 4))|
        = c ^ 2 / (4 * |P| * (P ^ 2 - c ^ 2 / 4)) := by
      rw [abs_div, abs_of_nonneg (sq_nonneg c), abs_mul, abs_mul,
        abs_of_pos (by norm_num : (0 : ℝ) < 4), abs_of_pos hApos]
    rw [heq, hval, habs]
    have hden : 4 * |P| * (P ^ 2 / 2) ≤ 4 * |P| * (P ^ 2 - c ^ 2 / 4) := by
      have h1 : (0 : ℝ) ≤ |P| := abs_nonneg P
      have h2 : 4 * (P ^ 2 / 2) ≤ 4 * (P ^ 2 - c ^ 2 / 4) := by linarith
      calc 4 * |P| * (P ^ 2 / 2) = |P| * (4 * (P ^ 2 / 2)) := by ring
        _ ≤ |P| * (4 * (P ^ 2 - c ^ 2 / 4)) := mul_le_mul_of_nonneg_left h2 h1
        _ = 4 * |P| * (P ^ 2 - c ^ 2 / 4) := by ring
    calc c ^ 2 / (4 * |P| * (P ^ 2 - c ^ 2 / 4))
        ≤ h ^ 2 / (4 * |P| * (P ^ 2 - c ^ 2 / 4)) :=
          div_le_div_of_nonneg_right hch (le_of_lt hAbl)
      _ ≤ h ^ 2 / (4 * |P| * (P ^ 2 / 2)) :=
          div_le_div_of_nonneg_left (sq_nonneg h) hAb2 hden
      _ = 1 / (2 * |P| ^ 3) * |h| ^ 2 := by
          have hsq : |P| ^ 2 = P ^ 2 := sq_abs P
          have he : 4 * |P| * (P ^ 2 / 2) = 2 * |P| ^ 3 := by
            rw [← hsq]
            ring
          rw [he, sq_abs h, one_div, div_eq_mul_inv,
            mul_comm (h ^ 2) ((2 * |P| ^ 3)⁻¹)]

/-! ## C24: the interpolated off-lattice family reproduces the lattice family -/

theorem c24_proved : C24 := by
  intro N D h hPD
  obtain ⟨hh, -, -, hpd⟩ := hPD
  have hne : h ≠ 0 := ne_of_gt hh
  have hchi : ∀ i k : Fin N, 0 < chi D h i k := by
    intro i k
    have hp : 0 < D.p i := (hpd i).1
    have hplt : D.p i < D.a - h / 2 := (hpd i).2.1
    have hA : 0 < D.a - h / 2 := lt_trans hp hplt
    have hq : 0 < D.q k := (hpd k).2.2.1
    have h1 : 0 < lam h (D.p i - D.a) := by
      simp only [lam]
      exact div_pos_of_neg_of_neg (by linarith) (by linarith)
    have h2 : 0 < lam h (D.q k + D.a) := by
      simp only [lam]
      exact div_pos (by linarith) (by linarith)
    simp only [chi]
    exact mul_pos h1 h2
  constructor
  · funext j x t
    simp only [sampleF, slice, F, tau, tauI, entry]
    congr 1
    funext i k
    have hy : (((j : ℝ) + 1 / 2) * h) / h - 1 / 2 = (j : ℝ) := by
      rw [mul_div_cancel_right₀ ((j : ℝ) + 1 / 2) hne]
      ring
    rw [hy, Real.exp_add, mul_comm ((j : ℝ)) (Real.log (chi D h i k)),
      ← Real.rpow_def_of_pos (hchi i k), Real.rpow_intCast]
    ring
  · funext j x t
    simp only [sampleG, slice, G, tau, tauI, entry]
    congr 1
    funext i k
    have hy : ((j : ℝ) * h) / h - 0 = (j : ℝ) := by
      rw [mul_div_cancel_right₀ (j : ℝ) hne, sub_zero]
    rw [hy, Real.exp_add, mul_comm ((j : ℝ)) (Real.log (chi D h i k)),
      ← Real.rpow_def_of_pos (hchi i k), Real.rpow_intCast]
    ring

end DLWContract
