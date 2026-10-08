/-
Package: C01 — the continuous (Clairaut / product-rule) bridge.

Contents
* `dc_deriv_fst`, `dc_deriv_snd` — bridges between one-dimensional `deriv` and the
  Fréchet derivative on `ℝ × ℝ`;
* `deriv_deriv_comm` — the **two-variable Clairaut lemma** (mixed second partials of a
  smooth `u : ℝ → ℝ → ℝ` commute), obtained from symmetry of the second Fréchet
  derivative (`IsSymmSndFDerivAt`).  Stated with `ContDiff ℝ ⊤` (what `Smooth3`
  provides) and, as `deriv_deriv_comm_two`, with `ContDiff ℝ 2`;
* `dc_deriv_cbil_y` — for `Smooth3 f`, `Smooth3 g`:
  `∂_y (cbil a f g) = cbil a (sy f) g + cbil a f (sy g)`
  (product rule for `bil` along `y ↦ slice f y`, with the order-2 and order-3
  Clairaut applications);
* `c01_proved` — target `C01`.
-/
import Contracts
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## Smoothness indices -/

private lemma dc_top_ne_zero : (⊤ : WithTop ENat) ≠ 0 :=
  ENat.one_le_iff_ne_zero_withTop.mp le_top

private lemma dc_two_ne_zero : (2 : WithTop ENat) ≠ 0 := by
  rw [← ENat.one_le_iff_ne_zero_withTop]
  exact_mod_cast (by norm_num : (1 : ℕ) ≤ 2)

private lemma dc_one_ne_zero : (1 : WithTop ENat) ≠ 0 :=
  ENat.one_le_iff_ne_zero_withTop.mp le_rfl

/-! ## Bridges: `deriv` versus `fderiv` on `ℝ × ℝ` -/

private lemma dc_hasDerivAt_fst (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    HasDerivAt (fun x' => W (x', b)) (fderiv ℝ W (a, b) (1, 0)) a := by
  have hγ : HasFDerivAt (fun x' : ℝ => (x', b)) (ContinuousLinearMap.inl ℝ ℝ ℝ) a :=
    hasFDerivAt_prodMk_left a b
  have h : HasFDerivAt (fun x' : ℝ => W (x', b))
      ((fderiv ℝ W (a, b)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ)) a :=
    hW.comp a hγ
  exact h.hasDerivAt

private lemma dc_hasDerivAt_snd (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    HasDerivAt (fun y' => W (a, y')) (fderiv ℝ W (a, b) (0, 1)) b := by
  have hγ : HasFDerivAt (fun y' : ℝ => (a, y')) (ContinuousLinearMap.inr ℝ ℝ ℝ) b :=
    hasFDerivAt_prodMk_right a b
  have h : HasFDerivAt (fun y' : ℝ => W (a, y'))
      ((fderiv ℝ W (a, b)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ)) b :=
    hW.comp b hγ
  exact h.hasDerivAt

private lemma dc_deriv_fst (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    deriv (fun x' => W (x', b)) a = fderiv ℝ W (a, b) (1, 0) :=
  (dc_hasDerivAt_fst W a b hW).deriv

private lemma dc_deriv_snd (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    deriv (fun y' => W (a, y')) b = fderiv ℝ W (a, b) (0, 1) :=
  (dc_hasDerivAt_snd W a b hW).deriv

/-! ## The two-variable Clairaut lemma -/

private lemma dc_smooth_partial_fst (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) :=
  (hW.fderiv_right (m := ⊤) le_top).clm_apply
    (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ))))

private lemma dc_fderiv_partial_comm {W : ℝ × ℝ → ℝ} (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0) := by
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable dc_top_ne_zero
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

/-- Differentiability in the second variable of the partial `x`-derivative. -/
private lemma dc_diff_snd_family (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    DifferentiableAt ℝ (fun y' => deriv (fun x' => W (x', y')) x) y := by
  have hdW : Differentiable ℝ W := hW.differentiable dc_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable dc_top_ne_zero
  have hP : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have h : DifferentiableAt ℝ (fun y' => fderiv ℝ W (x, y') (1, 0)) y :=
    (dc_hasDerivAt_snd (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) x y hP.hasFDerivAt).differentiableAt
  have hfun : (fun y' : ℝ => fderiv ℝ W (x, y') (1, 0))
      = (fun y' => deriv (fun x' => W (x', y')) x) :=
    funext fun y' => (dc_deriv_fst W x y' (hdW (x, y')).hasFDerivAt).symm
  rwa [hfun] at h

/-- Differentiability in the first variable of the partial `y`-derivative. -/
private lemma dc_diff_fst_family (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    DifferentiableAt ℝ (fun x' => deriv (fun y' => W (x', y')) y) x := by
  have hdW : Differentiable ℝ W := hW.differentiable dc_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable dc_top_ne_zero
  have hQ : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have h : DifferentiableAt ℝ (fun x' => fderiv ℝ W (x', y) (0, 1)) x :=
    (dc_hasDerivAt_fst (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) x y hQ.hasFDerivAt).differentiableAt
  have hfun : (fun x' : ℝ => fderiv ℝ W (x', y) (0, 1))
      = (fun x' => deriv (fun y' => W (x', y')) y) :=
    funext fun x' => (dc_deriv_snd W x' y (hdW (x', y)).hasFDerivAt).symm
  rwa [hfun] at h

private lemma dc_clairaut_of {W : ℝ × ℝ → ℝ}
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
    rw [← (dc_hasDerivAt_snd (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) x y hP.hasFDerivAt).deriv]
    congr 1
    funext y'
    exact (dc_deriv_fst W x y' (hdW (x, y')).hasFDerivAt).symm
  have hQval : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0)
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x := by
    rw [← (dc_hasDerivAt_fst (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) x y hQ.hasFDerivAt).deriv]
    congr 1
    funext x'
    exact (dc_deriv_snd W x' y (hdW (x', y)).hasFDerivAt).symm
  rw [← hPval, key, hQval]

/-- **Two-variable Clairaut**, `C^∞` form. -/
private lemma dc_clairaut {W : ℝ × ℝ → ℝ} (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => W (x', y')) x) y
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x :=
  dc_clairaut_of (hW.differentiable dc_top_ne_zero)
    ((hW.fderiv_right (m := ⊤) le_top).differentiable dc_top_ne_zero)
    (fun p => hW.contDiffAt.isSymmSndFDerivAt (by simp)) x y

/-- **Two-variable Clairaut lemma**: mixed second partials of a smooth two-variable
function commute.  (`ContDiff ℝ ⊤` version; `Smooth3` supplies `⊤`.) -/
private lemma deriv_deriv_comm {u : ℝ → ℝ → ℝ}
    (hu : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => u p.1 p.2)) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => u x' y') x) y
      = deriv (fun x' => deriv (fun y' => u x' y') y) x :=
  dc_clairaut hu x y

/-- **Two-variable Clairaut**, `ContDiff ℝ 2` form. -/
private lemma dc_clairaut_two {W : ℝ × ℝ → ℝ} (hW : ContDiff ℝ 2 W) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => W (x', y')) x) y
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x :=
  dc_clairaut_of (hW.differentiable dc_two_ne_zero)
    ((hW.fderiv_right (m := 1) (by norm_num)).differentiable dc_one_ne_zero)
    (fun p => hW.contDiffAt.isSymmSndFDerivAt (by simp)) x y

/-- The `ContDiff ℝ 2` form of the Clairaut lemma, in the curried shape requested. -/
private lemma deriv_deriv_comm_two {u : ℝ → ℝ → ℝ}
    (hu : ContDiff ℝ 2 (fun p : ℝ × ℝ => u p.1 p.2)) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => u x' y') x) y
      = deriv (fun x' => deriv (fun y' => u x' y') y) x :=
  dc_clairaut_two hu x y

/-! ## (A2) the `y`-derivative of the bilinear form along slices -/

private lemma dc_smooth_fixed_t (f : XYT) (hf : Smooth3 f) (t : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f p.1 p.2 t) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (p.1, (p.2, t))) := by fun_prop
  exact hf.comp hg

private lemma dc_smooth_fixed_x (f : XYT) (hf : Smooth3 f) (x : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f x p.1 p.2) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (x, (p.1, p.2))) := by fun_prop
  exact hf.comp hg

private lemma dc_jet1 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => W (x, y')) (deriv (fun b => W (x, b)) y) y := by
  have hdW : Differentiable ℝ W := hW.differentiable dc_top_ne_zero
  have h : HasDerivAt (fun y' => W (x, y')) (fderiv ℝ W (x, y) (0, 1)) y :=
    dc_hasDerivAt_snd W x y (hdW (x, y)).hasFDerivAt
  rw [← dc_deriv_snd W x y (hdW (x, y)).hasFDerivAt] at h
  exact h

private lemma dc_jet2 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => deriv (fun a => W (a, y')) x)
      (deriv (fun a => deriv (fun b => W (a, b)) y) x) y := by
  have h := (dc_diff_snd_family W hW x y).hasDerivAt
  rw [dc_clairaut hW x y] at h
  exact h

private lemma dc_jet3 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => deriv (fun a => deriv (fun b => W (b, y')) a) x)
      (deriv (fun a => deriv (fun b => deriv (fun c => W (b, c)) y) a) x) y := by
  have hdW : Differentiable ℝ W := hW.differentiable dc_top_ne_zero
  have hP : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) := dc_smooth_partial_fst W hW
  have hfun : (fun y' : ℝ => deriv (fun a => fderiv ℝ W (a, y') (1, 0)) x)
      = (fun y' => deriv (fun a => deriv (fun b => W (b, y')) a) x) := by
    funext y'
    congr 1
    funext a
    exact (dc_deriv_fst W a y' (hdW (a, y')).hasFDerivAt).symm
  rw [← hfun]
  have h := (dc_diff_snd_family (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) hP x y).hasDerivAt
  rw [dc_clairaut hP x y] at h
  refine h.congr_deriv ?_
  apply congrArg (fun F : ℝ → ℝ => deriv F x)
  funext a
  rw [show (fun y' : ℝ => fderiv ℝ W (a, y') (1, 0)) = (fun y' => deriv (fun b => W (b, y')) a) from
    funext fun y' => (dc_deriv_fst W a y' (hdW (a, y')).hasFDerivAt).symm]
  exact dc_clairaut hW a y

private lemma dc_jet4 (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ ⊤ V) (y t : ℝ) :
    HasDerivAt (fun y' => deriv (fun s => V (y', s)) t)
      (deriv (fun s => deriv (fun a => V (a, s)) y) t) y := by
  have h := (dc_diff_fst_family V hV y t).hasDerivAt
  rw [← dc_clairaut hV y t] at h
  exact h

/-- The four `y`-derivatives of the jets of `y' ↦ slice f y'`. -/
private lemma dc_slice_jets (f : XYT) (hf : Smooth3 f) (x y t : ℝ) :
    HasDerivAt (fun y' => f x y' t) (sy f x y t) y ∧
    HasDerivAt (fun y' => dx (slice f y') x t) (dx (slice (sy f) y) x t) y ∧
    HasDerivAt (fun y' => xx (slice f y') x t) (xx (slice (sy f) y) x t) y ∧
    HasDerivAt (fun y' => dt (slice f y') x t) (dt (slice (sy f) y) x t) y :=
  ⟨dc_jet1 (fun p : ℝ × ℝ => f p.1 p.2 t) (dc_smooth_fixed_t f hf t) x y,
   dc_jet2 (fun p : ℝ × ℝ => f p.1 p.2 t) (dc_smooth_fixed_t f hf t) x y,
   dc_jet3 (fun p : ℝ × ℝ => f p.1 p.2 t) (dc_smooth_fixed_t f hf t) x y,
   dc_jet4 (fun p : ℝ × ℝ => f x p.1 p.2) (dc_smooth_fixed_x f hf x) y t⟩

/-- The function-level numeral `2 : XT` evaluated pointwise (definitional). -/
private lemma dc_two_apply (x t : ℝ) : (2 : XT) x t = (2 : ℝ) := rfl

/-- Product rule for `bil` along a `y`-family of `XT`s. -/
private lemma dc_hasDerivAt_bil (a : ℝ) (F G : ℝ → XT) (F' G' : XT) (y x t : ℝ)
    (hF : HasDerivAt (fun y' => F y' x t) (F' x t) y)
    (hFdx : HasDerivAt (fun y' => dx (F y') x t) (dx F' x t) y)
    (hFxx : HasDerivAt (fun y' => xx (F y') x t) (xx F' x t) y)
    (hFdt : HasDerivAt (fun y' => dt (F y') x t) (dt F' x t) y)
    (hG : HasDerivAt (fun y' => G y' x t) (G' x t) y)
    (hGdx : HasDerivAt (fun y' => dx (G y') x t) (dx G' x t) y)
    (hGxx : HasDerivAt (fun y' => xx (G y') x t) (xx G' x t) y)
    (hGdt : HasDerivAt (fun y' => dt (G y') x t) (dt G' x t) y) :
    HasDerivAt (fun y' => bil a (F y') (G y') x t)
      (bil a F' (G y) x t + bil a (F y) G' x t) y := by
  have hfun : (fun y' => bil a (F y') (G y') x t)
      = (fun y' => xx (F y') x t * (G y') x t - 2 * (dx (F y') x t * dx (G y') x t)
          + (F y') x t * xx (G y') x t + dt (F y') x t * (G y') x t
          - (F y') x t * dt (G y') x t
          + (2 * a) * (dx (F y') x t * (G y') x t - (F y') x t * dx (G y') x t)) := by
    funext y'
    simp only [bil, hx, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
      dc_two_apply]
    ring
  rw [hfun]
  have hA : HasDerivAt (fun y' => xx (F y') x t * (G y') x t)
      (xx F' x t * (G y) x t + xx (F y) x t * (G' x t)) y := hFxx.mul hG
  have hB : HasDerivAt (fun y' => 2 * (dx (F y') x t * dx (G y') x t))
      (2 * (dx F' x t * dx (G y) x t + dx (F y) x t * dx G' x t)) y :=
    (hFdx.mul hGdx).const_mul 2
  have hC : HasDerivAt (fun y' => (F y') x t * xx (G y') x t)
      ((F' x t) * xx (G y) x t + (F y) x t * xx G' x t) y := hF.mul hGxx
  have hD : HasDerivAt (fun y' => dt (F y') x t * (G y') x t)
      (dt F' x t * (G y) x t + dt (F y) x t * (G' x t)) y := hFdt.mul hG
  have hE : HasDerivAt (fun y' => (F y') x t * dt (G y') x t)
      ((F' x t) * dt (G y) x t + (F y) x t * dt G' x t) y := hF.mul hGdt
  have hF6 : HasDerivAt
      (fun y' => (2 * a) * (dx (F y') x t * (G y') x t - (F y') x t * dx (G y') x t))
      ((2 * a) * ((dx F' x t * (G y) x t + dx (F y) x t * (G' x t))
        - ((F' x t) * dx (G y) x t + (F y) x t * dx G' x t))) y :=
    ((hFdx.mul hG).sub (hF.mul hGdx)).const_mul (2 * a)
  have hchain : HasDerivAt (fun y' => xx (F y') x t * (G y') x t
      - 2 * (dx (F y') x t * dx (G y') x t) + (F y') x t * xx (G y') x t
      + dt (F y') x t * (G y') x t - (F y') x t * dt (G y') x t
      + (2 * a) * (dx (F y') x t * (G y') x t - (F y') x t * dx (G y') x t))
      (xx F' x t * (G y) x t + xx (F y) x t * (G' x t)
        - 2 * (dx F' x t * dx (G y) x t + dx (F y) x t * dx G' x t)
        + ((F' x t) * xx (G y) x t + (F y) x t * xx G' x t)
        + (dt F' x t * (G y) x t + dt (F y) x t * (G' x t))
        - ((F' x t) * dt (G y) x t + (F y) x t * dt G' x t)
        + (2 * a) * ((dx F' x t * (G y) x t + dx (F y) x t * (G' x t))
          - ((F' x t) * dx (G y) x t + (F y) x t * dx G' x t))) y :=
    ((((hA.sub hB).add hC).add hD).sub hE).add hF6
  refine HasDerivAt.congr_deriv hchain ?_
  simp only [bil, hx, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    dc_two_apply]
  ring

/-- **(A2)** the `y`-derivative of the bilinear form, split along the slices:
`∂_y (bil a (slice f y) (slice g y)) = bil a (slice (sy f) y) (slice g y)
+ bil a (slice f y) (slice (sy g) y)`. -/
private lemma dc_deriv_cbil_y (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (x y t : ℝ) :
    deriv (fun y' => cbil a f g x y' t) y
      = cbil a (sy f) g x y t + cbil a f (sy g) x y t := by
  have hF := dc_slice_jets f hf x y t
  have hG := dc_slice_jets g hg x y t
  exact (dc_hasDerivAt_bil a (slice f) (slice g) (slice (sy f) y) (slice (sy g) y) y x t
    hF.1 hF.2.1 hF.2.2.1 hF.2.2.2 hG.1 hG.2.1 hG.2.2.1 hG.2.2.2).deriv

/-! ## Target C01 -/

theorem c01_proved : C01 := by
  intro a f g hf hg h0
  -- differentiating the vanishing identity `cbil a f g = 0` in `y`
  have hsum : cbil a (sy f) g + cbil a f (sy g) = 0 := by
    funext x y t
    have h1 : deriv (fun y' => cbil a f g x y' t) y = 0 := by
      rw [h0]
      simp
    rw [dc_deriv_cbil_y a f g hf hg x y t] at h1
    simpa using h1
  have hsum_p : ∀ x y t, cbil a (sy f) g x y t + cbil a f (sy g) x y t = 0 := by
    intro x y t
    have h := congrFun (congrFun (congrFun hsum x) y) t
    simpa using h
  have hcd_p : ∀ x y t, cdybil a f g x y t
      = cbil a (sy f) g x y t - cbil a f (sy g) x y t := by
    intro x y t
    simp only [cdybil, Pi.sub_apply]
  constructor
  · intro hL
    funext x y t
    show cbil a f (sy g) x y t + 2 * (chx f g x y t) = 0
    have hLp : cdybil a f g x y t - 4 * (chx f g x y t) = 0 := by
      have h := congrFun (congrFun (congrFun hL x) y) t
      simpa using h
    have h2 := hsum_p x y t
    have h3 := hcd_p x y t
    linarith
  · intro hR
    funext x y t
    show cdybil a f g x y t - 4 * (chx f g x y t) = 0
    have hRp : cbil a f (sy g) x y t + 2 * (chx f g x y t) = 0 := by
      have h := congrFun (congrFun (congrFun hR x) y) t
      simpa using h
    have h2 := hsum_p x y t
    have h3 := hcd_p x y t
    linarith

end DLWContract
