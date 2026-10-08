/-
Package: C02 — PROVED.  The target `C02` is established at the end of this file by

    theorem c02_proved : C02

No `sorry`, `admit` or new axiom is used: the proof is ordinary Mathlib calculus.

=============================================================================
THE THEOREM
=============================================================================

`C02` states: for smooth positive `f g : XYT` with `ContinuousPair a f g`, both
`c1 a (cu f g) (cv f g)` and `c2 a (cu f g) (cv f g)` vanish.

Put `A := log f + log g`, `B := log f - log g`.  Then, in `XYT` notation,

    cu f g = (2:ℝ) • sx B          (`c02_cu_eq`)
    cv f g = (2:ℝ) • sx (sy A)     (`c02_cv_eq`)

The proof runs through the certificate

    R  := c02R a A B = sx (sx A) + (sx B) * (sx B) + st B + (2a) • sx B
    S  := c02S a A B = sx (sx (sy A)) - sx (sx (sy B)) - st (sy A) + st (sy B)
                        - 2 • ((sx B) * (sx (sy A) - sx (sy B)))
                        - (2a) • (sx (sy A) - sx (sy B)) + 4 • sx B
    E2 := c02E2 a A B = (sy A - sy B) * R + S

(so, in jet notation and with the honest third-order quantity `e`,

    S = 2*e + 4*B_x,   E2 = 2*(q_y * R + e + 2*B_x),
    e = (1/2)*(A_xxy - B_xxy - A_yt + B_yt) - B_x*(A_xy - B_xy) - a*(A_xy - B_xy),
    q_y = (A_y - B_y)/2,

all verified exactly by `_c02_scratch/check_old_form.py` and formalised below),

together with the three bridges

    cbil a f g          = (f * g) * R                 (`c02_cbil_eq`)
    chx  f g            = (f * g) * sx B              (`c02_chx_eq`)
    2 • cbil a f (sy g) = (f * g) * (E2 - 4 • sx B)   (`c02_cbil_syg_eq`)

and the two *pure calculus* identities

    c1 a (2 • sx B) (2 • sx (sy A)) = 2 • sx (sy R)                 (`c02_c1_eq`)
    c2 a (2 • sx B) (2 • sx (sy A)) = 2 • sx (sy R) - 2 • sx S      (`c02_c2_eq`)

Vanishing then follows from positivity of `f * g`: the first hypothesis
`cbil a f g = 0` gives `R = 0`; the second hypothesis, in the equivalent form
`cbil a f (sy g) + 2 * chx f g = 0` produced by `c02_hyp_from_ContinuousPair`,
gives `E2 = 0`; hence `S = E2 - (sy A - sy B) * R = 0`, and both `c1` and `c2`
vanish.

=============================================================================
THE SCALAR HYPOTHESES (corrected, verbatim)
=============================================================================

For smooth positive `f`, `g`, `ContinuousPair a f g` — i.e.

    cbil a f g = 0  ∧  cdybil a f g - 4 * chx f g = 0

— is equivalent to the following pair of *scalar* equations on `A`, `B`:

    (I)  R  := c02R a A B
            = sx (sx A) + (sx B) * (sx B) + st B + (2a) • sx B = 0

    (II) E2 := c02E2 a A B = (sy A - sy B) * c02R a A B + c02S a A B = 0

with `c02S` exactly as displayed above (equivalently `S = 2*e + 4*B_x` with the
`e` above; equivalently `E2 = 2*(q_y * R + e + 2*B_x)` with `q_y = (A_y-B_y)/2`).

WARNING.  An earlier draft of this file recorded the second scalar as

    (II-wrong)  E2 = beta_y * (S_xx + (D_x)^2 + D_t + 2a * D_x) + 2 * B_x
                where  beta_y := (A_y - B_y)/2,  alpha := (A + B)/2,
                       S := alpha + beta_y,      D := alpha - beta_y.

THIS FORM IS WRONG.  `S := alpha + beta_y` is not a log coordinate at all (it
adds a function of `(x,t)` to a function of `(x,y,t)`), and the expression is not
equal to the correct `E2`: the difference `E2 - (II-wrong)` is a nonzero
polynomial on random smooth `A`, `B` (checked exactly with sympy in
`_c02_scratch/check_old_form.py`; it vanishes only for degenerate inputs such as
`a = 0` with `B` independent of `y`).  The correct statement is (II) above, whose
right-hand side is built from `R` and from the *third-order* quantity `c02S`.
Note also that the correction is not cosmetic: `2 • cbil a f (sy g)` is a
second-order expression in the jets, and matching it to `(f*g)*(E2 - 4 B_x)`
requires the `y`-derivatives `sx (sy A)`, `st (sy A)` appearing in `c02S`.

=============================================================================
WHAT IS PROVED IN THIS FILE
=============================================================================

* `c02_smooth_fixed_t`, `c02_smooth_fixed_x`, `c02_smooth_fixed_y` — slicing a
  `Smooth3` function in any one variable keeps it `C^∞`.
* `c02_log_sx`, `c02_log_sy`, `c02_log_st` — the log-jet lemmas
  `sx φ = φ * sx (log φ)` and its `sy`/`st` analogues for a positive smooth `φ`.
* `c02_log_sxx` — the second-order log-jet lemma
  `sx (sx φ) = φ * (sx (sx (log φ)) + (sx (log φ))^2)`.
* `c02_deriv_cbil_y` — the `y`-derivative of the bilinear form along `y`-slices,
  `deriv (fun y' => cbil a f g x y' t) y
     = cbil a (sy f) g x y t + cbil a f (sy g) x y t`
  (the copy of `PkgContinuous.lean`'s private `dc_deriv_cbil_y`).
* `c02_cdybil_eq` — the pointwise unfolding of `cdybil` used by `C01`.
* `c02_hyp_from_ContinuousPair` — the two scalar hypotheses (I) and (II) in the
  `A`/`B` normalisation, derived from `ContinuousPair` (I directly; II as
  `cbil a f (sy g) + 2 * chx f g = 0`, the form C01 shows is equivalent to
  `cdybil - 4 * chx = 0`).
* the `XYT` jet toolkit (`c02_sx_mul`, `c02_sy_st`, `c02_smooth_log`, ...), the
  three bridges `c02_cbil_eq` / `c02_chx_eq` / `c02_cbil_syg_eq`, the two
  calculus identities `c02_c1_eq` / `c02_c2_eq`, and finally
  `theorem c02_proved : C02`.
-/

import Contracts
import Mathlib.Analysis.Calculus.FDeriv.Symmetric
import Mathlib.Analysis.Calculus.FDeriv.CompCLM
import Mathlib.Analysis.Calculus.FDeriv.Prod
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## Smoothness of slices -/

lemma c02_top_ne_zero : (⊤ : WithTop ENat) ≠ 0 :=
  ENat.one_le_iff_ne_zero_withTop.mp le_top

lemma c02_smooth_fixed_t (f : XYT) (hf : Smooth3 f) (t : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f p.1 p.2 t) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (p.1, (p.2, t))) := by fun_prop
  exact hf.comp hg

lemma c02_smooth_fixed_x (f : XYT) (hf : Smooth3 f) (x : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f x p.1 p.2) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (x, (p.1, p.2))) := by fun_prop
  exact hf.comp hg

lemma c02_smooth_fixed_y (f : XYT) (hf : Smooth3 f) (y : ℝ) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => f p.1 y p.2) := by
  have hg : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => (p.1, (y, p.2))) := by fun_prop
  exact hf.comp hg

lemma c02_diffAt_of_contDiff {f : ℝ → ℝ} (h : ContDiff ℝ ⊤ f) (x : ℝ) :
    DifferentiableAt ℝ f x :=
  (h.differentiable c02_top_ne_zero).differentiableAt

/-! ## Log-jet lemmas for a positive smooth `φ : XYT`

`φ` positive and smooth on `XYT`; the log is taken pointwise.  These are the
`XYT` analogues of the first-order identities used inside `c13_proved`. -/

lemma c02_log_sx (φ : XYT) (hφ : Smooth3 φ) (hpos : ∀ x y t, 0 < φ x y t) :
    sx φ = φ * sx (fun x y t => Real.log (φ x y t)) := by
  funext x y t
  have hT : ContDiff ℝ ⊤ (fun z : ℝ => φ z y t) := by
    have hg : ContDiff ℝ ⊤ (fun z : ℝ => (z, (y, t))) := by fun_prop
    exact hφ.comp hg
  have hne : φ x y t ≠ 0 := ne_of_gt (hpos x y t)
  have h1 : HasDerivAt (fun z : ℝ => Real.log (φ z y t))
      (deriv (fun z : ℝ => φ z y t) x / φ x y t) x :=
    (c02_diffAt_of_contDiff hT x).hasDerivAt.log hne
  simp only [sx, Pi.mul_apply]
  rw [h1.deriv]
  field_simp

lemma c02_log_sy (φ : XYT) (hφ : Smooth3 φ) (hpos : ∀ x y t, 0 < φ x y t) :
    sy φ = φ * sy (fun x y t => Real.log (φ x y t)) := by
  funext x y t
  have hT : ContDiff ℝ ⊤ (fun z : ℝ => φ x z t) := by
    have hg : ContDiff ℝ ⊤ (fun z : ℝ => (x, (z, t))) := by fun_prop
    exact hφ.comp hg
  have hne : φ x y t ≠ 0 := ne_of_gt (hpos x y t)
  have h1 : HasDerivAt (fun z : ℝ => Real.log (φ x z t))
      (deriv (fun z : ℝ => φ x z t) y / φ x y t) y :=
    (c02_diffAt_of_contDiff hT y).hasDerivAt.log hne
  simp only [sy, Pi.mul_apply]
  rw [h1.deriv]
  field_simp

lemma c02_log_st (φ : XYT) (hφ : Smooth3 φ) (hpos : ∀ x y t, 0 < φ x y t) :
    st φ = φ * st (fun x y t => Real.log (φ x y t)) := by
  funext x y t
  have hT : ContDiff ℝ ⊤ (fun z : ℝ => φ x y z) := by
    have hg : ContDiff ℝ ⊤ (fun z : ℝ => (x, (y, z))) := by fun_prop
    exact hφ.comp hg
  have hne : φ x y t ≠ 0 := ne_of_gt (hpos x y t)
  have h1 : HasDerivAt (fun z : ℝ => Real.log (φ x y z))
      (deriv (φ x y) t / φ x y t) t :=
    (c02_diffAt_of_contDiff hT t).hasDerivAt.log hne
  simp only [st, Pi.mul_apply]
  rw [h1.deriv]
  field_simp

/-- Second-order log-jet lemma: `sx (sx φ) = φ * (sx (sx (log φ)) + (sx (log φ))^2)`. -/
lemma c02_log_sxx (φ : XYT) (hφ : Smooth3 φ) (hpos : ∀ x y t, 0 < φ x y t) :
    sx (sx φ) = φ * (sx (sx (fun x y t => Real.log (φ x y t)))
      + (sx (fun x y t => Real.log (φ x y t))) ^ 2) := by
  funext x y t
  set α : XYT := fun x y t => Real.log (φ x y t) with hα
  have hT : ∀ y t, ContDiff ℝ ⊤ (fun z : ℝ => φ z y t) := by
    intro y t
    have hg : ContDiff ℝ ⊤ (fun z : ℝ => (z, (y, t))) := by fun_prop
    exact hφ.comp hg
  have hA : ∀ y t, ContDiff ℝ ⊤ (fun z : ℝ => α z y t) := by
    intro y t
    have h : ContDiff ℝ ⊤ (fun z : ℝ => Real.log (φ z y t)) :=
      (hT y t).log (fun z => ne_of_gt (hpos z y t))
    simpa [hα] using h
  have hAd : ∀ y t, ContDiff ℝ ⊤ (deriv (fun z : ℝ => α z y t)) := by
    intro y t
    exact ContDiff.deriv' (n := ⊤) (show ContDiff ℝ (⊤ + 1) (fun z : ℝ => α z y t) from hA y t)
  have hdx : ∀ x y t, sx φ x y t = φ x y t * sx α x y t := by
    intro x y t
    have h := congrFun (congrFun (congrFun (c02_log_sx φ hφ hpos) x) y) t
    simpa [hα] using h
  have hfun : (fun z : ℝ => sx φ z y t) = ((fun z : ℝ => φ z y t) * (fun z : ℝ => sx α z y t)) := by
    funext z
    simpa [sx, Pi.mul_apply] using hdx z y t
  have hmul : deriv ((fun z : ℝ => φ z y t) * (fun z : ℝ => sx α z y t)) x
      = sx φ x y t * sx α x y t + φ x y t * sx (sx α) x y t := by
    have h := deriv_mul (c02_diffAt_of_contDiff (hT y t) x)
      (c02_diffAt_of_contDiff (hAd y t) x)
    simpa only [sx] using h
  show deriv (fun z : ℝ => sx φ z y t) x
      = (φ * (sx (sx α) + sx α ^ 2)) x y t
  rw [hfun, hmul, hdx x y t]
  simp only [Pi.mul_apply, Pi.add_apply, Pi.pow_apply]
  ring

/-! ## The `y`-derivative of the bilinear form along `y`-slices

This is the copy of the private lemma `dc_deriv_cbil_y` from `PkgContinuous.lean`
(helpers there are `private`, so it is reproduced here). -/

lemma c02_hasDerivAt_fst (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    HasDerivAt (fun x' => W (x', b)) (fderiv ℝ W (a, b) (1, 0)) a := by
  have hγ : HasFDerivAt (fun x' : ℝ => (x', b)) (ContinuousLinearMap.inl ℝ ℝ ℝ) a :=
    hasFDerivAt_prodMk_left a b
  exact (hW.comp a hγ).hasDerivAt

lemma c02_hasDerivAt_snd (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    HasDerivAt (fun y' => W (a, y')) (fderiv ℝ W (a, b) (0, 1)) b := by
  have hγ : HasFDerivAt (fun y' : ℝ => (a, y')) (ContinuousLinearMap.inr ℝ ℝ ℝ) b :=
    hasFDerivAt_prodMk_right a b
  exact (hW.comp b hγ).hasDerivAt

lemma c02_deriv_fst (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    deriv (fun x' => W (x', b)) a = fderiv ℝ W (a, b) (1, 0) :=
  (c02_hasDerivAt_fst W a b hW).deriv

lemma c02_deriv_snd (W : ℝ × ℝ → ℝ) (a b : ℝ)
    (hW : HasFDerivAt W (fderiv ℝ W (a, b)) (a, b)) :
    deriv (fun y' => W (a, y')) b = fderiv ℝ W (a, b) (0, 1) :=
  (c02_hasDerivAt_snd W a b hW).deriv

lemma c02_smooth_partial_fst (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) :
    ContDiff ℝ ⊤ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) :=
  (hW.fderiv_right (m := ⊤) le_top).clm_apply
    (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × ℝ => ((1 : ℝ), (0 : ℝ))))

lemma c02_diff_snd_family (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    DifferentiableAt ℝ (fun y' => deriv (fun x' => W (x', y')) x) y := by
  have hdW : Differentiable ℝ W := hW.differentiable c02_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable c02_top_ne_zero
  have hP : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have h : DifferentiableAt ℝ (fun y' => fderiv ℝ W (x, y') (1, 0)) y :=
    (c02_hasDerivAt_snd (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) x y hP.hasFDerivAt).differentiableAt
  have hfun : (fun y' : ℝ => fderiv ℝ W (x, y') (1, 0))
      = (fun y' => deriv (fun x' => W (x', y')) x) :=
    funext fun y' => (c02_deriv_fst W x y' (hdW (x, y')).hasFDerivAt).symm
  rwa [hfun] at h

lemma c02_diff_fst_family (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    DifferentiableAt ℝ (fun x' => deriv (fun y' => W (x', y')) y) x := by
  have hdW : Differentiable ℝ W := hW.differentiable c02_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable c02_top_ne_zero
  have hQ : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have h : DifferentiableAt ℝ (fun x' => fderiv ℝ W (x', y) (0, 1)) x :=
    (c02_hasDerivAt_fst (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) x y hQ.hasFDerivAt).differentiableAt
  have hfun : (fun x' : ℝ => fderiv ℝ W (x', y) (0, 1))
      = (fun x' => deriv (fun y' => W (x', y')) y) :=
    funext fun x' => (c02_deriv_snd W x' y (hdW (x', y)).hasFDerivAt).symm
  rwa [hfun] at h

/-- **Two-variable Clairaut**, `C^∞` form (copy of `PkgContinuous.lean`'s helper). -/
lemma c02_clairaut {W : ℝ × ℝ → ℝ} (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    deriv (fun y' => deriv (fun x' => W (x', y')) x) y
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x := by
  have hdW : Differentiable ℝ W := hW.differentiable c02_top_ne_zero
  have hdFW : Differentiable ℝ (fderiv ℝ W) :=
    (hW.fderiv_right (m := ⊤) le_top).differentiable c02_top_ne_zero
  have hP : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have hQ : DifferentiableAt ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) :=
    (hdFW (x, y)).clm_apply (differentiableAt_const _)
  have key : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0) := by
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
  have hPval : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) (x, y) (0, 1)
      = deriv (fun y' => deriv (fun x' => W (x', y')) x) y := by
    rw [← (c02_hasDerivAt_snd (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) x y hP.hasFDerivAt).deriv]
    congr 1
    funext y'
    exact (c02_deriv_fst W x y' (hdW (x, y')).hasFDerivAt).symm
  have hQval : fderiv ℝ (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) (x, y) (1, 0)
      = deriv (fun x' => deriv (fun y' => W (x', y')) y) x := by
    rw [← (c02_hasDerivAt_fst (fun p : ℝ × ℝ => fderiv ℝ W p (0, 1)) x y hQ.hasFDerivAt).deriv]
    congr 1
    funext x'
    exact (c02_deriv_snd W x' y (hdW (x', y)).hasFDerivAt).symm
  rw [← hPval, key, hQval]

lemma c02_jet1 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => W (x, y')) (deriv (fun b => W (x, b)) y) y := by
  have hdW : Differentiable ℝ W := hW.differentiable c02_top_ne_zero
  have h : HasDerivAt (fun y' => W (x, y')) (fderiv ℝ W (x, y) (0, 1)) y :=
    c02_hasDerivAt_snd W x y (hdW (x, y)).hasFDerivAt
  rwa [← c02_deriv_snd W x y (hdW (x, y)).hasFDerivAt] at h

lemma c02_jet2 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => deriv (fun a => W (a, y')) x)
      (deriv (fun a => deriv (fun b => W (a, b)) y) x) y := by
  have h := (c02_diff_snd_family W hW x y).hasDerivAt
  rwa [c02_clairaut hW x y] at h

lemma c02_jet3 (W : ℝ × ℝ → ℝ) (hW : ContDiff ℝ ⊤ W) (x y : ℝ) :
    HasDerivAt (fun y' => deriv (fun a => deriv (fun b => W (b, y')) a) x)
      (deriv (fun a => deriv (fun b => deriv (fun c => W (b, c)) y) a) x) y := by
  have hdW : Differentiable ℝ W := hW.differentiable c02_top_ne_zero
  have hP : ContDiff ℝ ⊤ (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) := c02_smooth_partial_fst W hW
  have hfun : (fun y' : ℝ => deriv (fun a => fderiv ℝ W (a, y') (1, 0)) x)
      = (fun y' => deriv (fun a => deriv (fun b => W (b, y')) a) x) := by
    funext y'
    congr 1
    funext a
    exact (c02_deriv_fst W a y' (hdW (a, y')).hasFDerivAt).symm
  rw [← hfun]
  have h := (c02_diff_snd_family (fun p : ℝ × ℝ => fderiv ℝ W p (1, 0)) hP x y).hasDerivAt
  rw [c02_clairaut hP x y] at h
  refine h.congr_deriv ?_
  apply congrArg (fun F : ℝ → ℝ => deriv F x)
  funext a
  rw [show (fun y' : ℝ => fderiv ℝ W (a, y') (1, 0)) = (fun y' => deriv (fun b => W (b, y')) a)
    from funext fun y' => (c02_deriv_fst W a y' (hdW (a, y')).hasFDerivAt).symm]
  exact c02_clairaut hW a y

lemma c02_jet4 (V : ℝ × ℝ → ℝ) (hV : ContDiff ℝ ⊤ V) (y t : ℝ) :
    HasDerivAt (fun y' => deriv (fun s => V (y', s)) t)
      (deriv (fun s => deriv (fun a => V (a, s)) y) t) y := by
  have h := (c02_diff_fst_family V hV y t).hasDerivAt
  rwa [← c02_clairaut hV y t] at h

/-- The four `y`-derivatives of the jets of `y' ↦ slice f y'`. -/
lemma c02_slice_jets (f : XYT) (hf : Smooth3 f) (x y t : ℝ) :
    HasDerivAt (fun y' => f x y' t) (sy f x y t) y ∧
    HasDerivAt (fun y' => dx (slice f y') x t) (dx (slice (sy f) y) x t) y ∧
    HasDerivAt (fun y' => xx (slice f y') x t) (xx (slice (sy f) y) x t) y ∧
    HasDerivAt (fun y' => dt (slice f y') x t) (dt (slice (sy f) y) x t) y :=
  ⟨c02_jet1 (fun p : ℝ × ℝ => f p.1 p.2 t) (c02_smooth_fixed_t f hf t) x y,
   c02_jet2 (fun p : ℝ × ℝ => f p.1 p.2 t) (c02_smooth_fixed_t f hf t) x y,
   c02_jet3 (fun p : ℝ × ℝ => f p.1 p.2 t) (c02_smooth_fixed_t f hf t) x y,
   c02_jet4 (fun p : ℝ × ℝ => f x p.1 p.2) (c02_smooth_fixed_x f hf x) y t⟩

lemma c02_two_apply (x t : ℝ) : (2 : XT) x t = (2 : ℝ) := rfl

/-- Product rule for `bil` along a `y`-family of `XT`s. -/
lemma c02_hasDerivAt_bil (a : ℝ) (F G : ℝ → XT) (F' G' : XT) (y x t : ℝ)
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
      c02_two_apply]
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
    c02_two_apply]
  ring

/-- The `y`-derivative of the bilinear form, split along the slices:
`∂_y (cbil a f g) = cbil a (sy f) g + cbil a f (sy g)`. -/
lemma c02_deriv_cbil_y (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (x y t : ℝ) :
    deriv (fun y' => cbil a f g x y' t) y
      = cbil a (sy f) g x y t + cbil a f (sy g) x y t := by
  have hF := c02_slice_jets f hf x y t
  have hG := c02_slice_jets g hg x y t
  exact (c02_hasDerivAt_bil a (slice f) (slice g) (slice (sy f) y) (slice (sy g) y) y x t
    hF.1 hF.2.1 hF.2.2.1 hF.2.2.2 hG.1 hG.2.1 hG.2.2.1 hG.2.2.2).deriv

/-! ## The two scalar hypotheses, extracted from `ContinuousPair` -/

/-- Pointwise unfolding of `cdybil`. -/
lemma c02_cdybil_eq (a : ℝ) (f g : XYT) (x y t : ℝ) :
    cdybil a f g x y t = cbil a (sy f) g x y t - cbil a f (sy g) x y t := by
  simp only [cdybil, Pi.sub_apply]

/-- The two hypotheses (I) and (II) in the form that C01 relates them to
`ContinuousPair`: `cbil a f g = 0` and `cbil a f (sy g) + 2 * chx f g = 0`. -/
lemma c02_hyp_from_ContinuousPair (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (h : ContinuousPair a f g) :
    cbil a f g = 0 ∧ cbil a f (sy g) + 2 * chx f g = 0 := by
  obtain ⟨hI, hII⟩ := h
  refine ⟨hI, ?_⟩
  -- ∂_y (cbil a f g) = 0 because cbil a f g = 0 as a function of y
  have hsum : cbil a (sy f) g + cbil a f (sy g) = 0 := by
    funext x y t
    have h1 : deriv (fun y' => cbil a f g x y' t) y = 0 := by
      rw [hI]
      simp
    rw [c02_deriv_cbil_y a f g hf hg x y t] at h1
    simpa using h1
  funext x y t
  show cbil a f (sy g) x y t + 2 * (chx f g x y t) = 0
  have hLp : cdybil a f g x y t - 4 * (chx f g x y t) = 0 := by
    have hh := congrFun (congrFun (congrFun hII x) y) t
    simpa using hh
  have h2 : cbil a (sy f) g x y t + cbil a f (sy g) x y t = 0 := by
    have hh := congrFun (congrFun (congrFun hsum x) y) t
    simpa using hh
  have h3 := c02_cdybil_eq a f g x y t
  linarith

/-- The same statement as `C02`, kept as a named `Prop`.  It is now *proved*:
`c02_gap_proved` at the end of this file inhabits this type, definitionally from
`c02_proved`. -/
def c02_gap : Prop := ∀ (a : ℝ) (f g : XYT), Smooth3 f → Smooth3 g →
  Positive3 f → Positive3 g → ContinuousPair a f g →
  c1 a (cu f g) (cv f g) = 0 ∧ c2 a (cu f g) (cv f g) = 0




/-! ## Toolkit: calculus lemmas for the three coordinate derivatives on `XYT`

Everything below is new material added by the final C02 closure. -/

abbrev c02lift (W : XYT) : ℝ × (ℝ × ℝ) → ℝ := fun z => W z.1 z.2.1 z.2.2

/-- The direction vectors, kept as `inl`/`inr` applications so no normalisation is needed. -/
abbrev c02vx : ℝ × (ℝ × ℝ) := ContinuousLinearMap.inl ℝ ℝ (ℝ × ℝ) 1

abbrev c02vy : ℝ × (ℝ × ℝ) :=
  (ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ) 1

abbrev c02vt : ℝ × (ℝ × ℝ) :=
  (ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ) 1

/-- `deriv` along the first coordinate is the Fréchet derivative at the lifted point. -/
lemma c02_deriv3_fst (W : XYT) (hW : Smooth3 W) (x y t : ℝ) :
    deriv (fun a : ℝ => W a y t) x = fderiv ℝ (c02lift W) (x, (y, t)) c02vx := by
  have hd : DifferentiableAt ℝ (c02lift W) (x, (y, t)) :=
    (hW.differentiable c02_top_ne_zero) (x, (y, t))
  have hγ : HasFDerivAt (fun a : ℝ => (a, (y, t)))
      (ContinuousLinearMap.inl ℝ ℝ (ℝ × ℝ)) x :=
    hasFDerivAt_prodMk_left x (y, t)
  have h := (hd.hasFDerivAt.comp x hγ).hasDerivAt
  simpa only [c02lift, c02vx, Function.comp_def, ContinuousLinearMap.comp_apply] using h.deriv

lemma c02_deriv3_snd (W : XYT) (hW : Smooth3 W) (x y t : ℝ) :
    deriv (fun b : ℝ => W x b t) y = fderiv ℝ (c02lift W) (x, (y, t)) c02vy := by
  have hd : DifferentiableAt ℝ (c02lift W) (x, (y, t)) :=
    (hW.differentiable c02_top_ne_zero) (x, (y, t))
  have hγ : HasFDerivAt (fun b : ℝ => (x, (b, t)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ)) y :=
    (hasFDerivAt_prodMk_right x (y, t)).comp y (hasFDerivAt_prodMk_left y t)
  have h := (hd.hasFDerivAt.comp y hγ).hasDerivAt
  simpa only [c02lift, c02vy, Function.comp_def, ContinuousLinearMap.comp_apply] using h.deriv

lemma c02_deriv3_trd (W : XYT) (hW : Smooth3 W) (x y t : ℝ) :
    deriv (W x y) t = fderiv ℝ (c02lift W) (x, (y, t)) c02vt := by
  have hd : DifferentiableAt ℝ (c02lift W) (x, (y, t)) :=
    (hW.differentiable c02_top_ne_zero) (x, (y, t))
  have hγ : HasFDerivAt (fun c : ℝ => (x, (y, c)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ)) t :=
    (hasFDerivAt_prodMk_right x (y, t)).comp t (hasFDerivAt_prodMk_right y t)
  have h := (hd.hasFDerivAt.comp t hγ).hasDerivAt
  simpa only [c02lift, c02vt, Function.comp_def, ContinuousLinearMap.comp_apply] using h.deriv

/-! ### Smoothness closure -/

@[simp] lemma c02_smooth_add {F G : XYT} (hF : Smooth3 F) (hG : Smooth3 G) :
    Smooth3 (F + G) := by
  have h := hF.add hG
  simpa only [Smooth3, c02lift, Pi.add_apply] using h

@[simp] lemma c02_smooth_sub {F G : XYT} (hF : Smooth3 F) (hG : Smooth3 G) :
    Smooth3 (F - G) := by
  have h := hF.sub hG
  simpa only [Smooth3, c02lift, Pi.sub_apply] using h

@[simp] lemma c02_smooth_neg {F : XYT} (hF : Smooth3 F) : Smooth3 (-F) := by
  have h := hF.neg
  simpa only [Smooth3, c02lift, Pi.neg_apply] using h

@[simp] lemma c02_smooth_mul {F G : XYT} (hF : Smooth3 F) (hG : Smooth3 G) :
    Smooth3 (F * G) := by
  have h := hF.mul hG
  simpa only [Smooth3, c02lift, Pi.mul_apply] using h

@[simp] lemma c02_smooth_smul (c : ℝ) {F : XYT} (hF : Smooth3 F) : Smooth3 (c • F) := by
  have h := hF.const_smul c
  simpa only [Smooth3, c02lift, Pi.smul_apply] using h

@[simp] lemma c02_smooth_sx {F : XYT} (hF : Smooth3 F) : Smooth3 (sx F) := by
  have hfd : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vx) :=
    (hF.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × (ℝ × ℝ) => c02vx))
  have hfun : (fun z : ℝ × (ℝ × ℝ) => sx F z.1 z.2.1 z.2.2)
      = fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vx := by
    funext z
    show deriv (fun a : ℝ => F a z.2.1 z.2.2) z.1 = fderiv ℝ (c02lift F) z c02vx
    exact c02_deriv3_fst F hF z.1 z.2.1 z.2.2
  show ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => sx F z.1 z.2.1 z.2.2)
  rw [hfun]
  exact hfd

@[simp] lemma c02_smooth_sy {F : XYT} (hF : Smooth3 F) : Smooth3 (sy F) := by
  have hfd : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vy) :=
    (hF.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × (ℝ × ℝ) => c02vy))
  have hfun : (fun z : ℝ × (ℝ × ℝ) => sy F z.1 z.2.1 z.2.2)
      = fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vy := by
    funext z
    show deriv (fun b : ℝ => F z.1 b z.2.2) z.2.1 = fderiv ℝ (c02lift F) z c02vy
    exact c02_deriv3_snd F hF z.1 z.2.1 z.2.2
  show ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => sy F z.1 z.2.1 z.2.2)
  rw [hfun]
  exact hfd

@[simp] lemma c02_smooth_st {F : XYT} (hF : Smooth3 F) : Smooth3 (st F) := by
  have hfd : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vt) :=
    (hF.fderiv_right (m := ⊤) le_top).clm_apply
      (contDiff_const : ContDiff ℝ ⊤ (fun _ : ℝ × (ℝ × ℝ) => c02vt))
  have hfun : (fun z : ℝ × (ℝ × ℝ) => st F z.1 z.2.1 z.2.2)
      = fun z : ℝ × (ℝ × ℝ) => fderiv ℝ (c02lift F) z c02vt := by
    funext z
    show deriv (F z.1 z.2.1) z.2.2 = fderiv ℝ (c02lift F) z c02vt
    exact c02_deriv3_trd F hF z.1 z.2.1 z.2.2
  show ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => st F z.1 z.2.1 z.2.2)
  rw [hfun]
  exact hfd

/-- `log` of a positive `XYT`, pointwise. -/
def c02log (f : XYT) : XYT := fun x y t => Real.log (f x y t)

/-- `c02log` unfolded to the raw `Real.log` lambda. -/
lemma c02log_eq (F : XYT) : c02log F = fun x y t => Real.log (F x y t) := rfl

@[simp] lemma c02_smooth_log {F : XYT} (hF : Smooth3 F) (hpos : Positive3 F) :
    Smooth3 (c02log F) := by
  have h : ContDiff ℝ ⊤ (fun z : ℝ × (ℝ × ℝ) => F z.1 z.2.1 z.2.2) := hF
  have h' := h.log (fun z => ne_of_gt (hpos z.1 z.2.1 z.2.2))
  simpa only [c02log, Smooth3, c02lift] using h'

/-! ### Differentiability of the coordinate slices -/

lemma c02_diff_x (F : XYT) (hF : Smooth3 F) (x y t : ℝ) :
    DifferentiableAt ℝ (fun a : ℝ => F a y t) x := by
  have hd : HasFDerivAt (c02lift F) (fderiv ℝ (c02lift F) (x, (y, t))) (x, (y, t)) :=
    ((hF.differentiable c02_top_ne_zero) (x, (y, t))).hasFDerivAt
  have hγ : HasFDerivAt (fun a : ℝ => (a, (y, t)))
      (ContinuousLinearMap.inl ℝ ℝ (ℝ × ℝ)) x := hasFDerivAt_prodMk_left x (y, t)
  have h3 := (hd.comp x hγ).differentiableAt
  simpa only [c02lift, Function.comp_def] using h3

lemma c02_diff_y (F : XYT) (hF : Smooth3 F) (x y t : ℝ) :
    DifferentiableAt ℝ (fun b : ℝ => F x b t) y := by
  have hd : HasFDerivAt (c02lift F) (fderiv ℝ (c02lift F) (x, (y, t))) (x, (y, t)) :=
    ((hF.differentiable c02_top_ne_zero) (x, (y, t))).hasFDerivAt
  have hγ : HasFDerivAt (fun b : ℝ => (x, (b, t)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inl ℝ ℝ ℝ)) y :=
    (hasFDerivAt_prodMk_right x (y, t)).comp y (hasFDerivAt_prodMk_left y t)
  have h3 := (hd.comp y hγ).differentiableAt
  simpa only [c02lift, Function.comp_def] using h3

lemma c02_diff_t (F : XYT) (hF : Smooth3 F) (x y t : ℝ) :
    DifferentiableAt ℝ (F x y) t := by
  have hd : HasFDerivAt (c02lift F) (fderiv ℝ (c02lift F) (x, (y, t))) (x, (y, t)) :=
    ((hF.differentiable c02_top_ne_zero) (x, (y, t))).hasFDerivAt
  have hγ : HasFDerivAt (fun c : ℝ => (x, (y, c)))
      ((ContinuousLinearMap.inr ℝ ℝ (ℝ × ℝ)).comp (ContinuousLinearMap.inr ℝ ℝ ℝ)) t :=
    (hasFDerivAt_prodMk_right x (y, t)).comp t (hasFDerivAt_prodMk_right y t)
  have h3 := (hd.comp t hγ).differentiableAt
  simpa only [c02lift, Function.comp_def] using h3

/-! ### Linearity over `+`, `-`, scalar multiples, and the product rule -/

lemma c02_sx_add (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sx (F + G) = sx F + sx G := by
  funext x y t
  simp only [sx, Pi.add_apply]
  exact deriv_add (c02_diff_x F hF x y t) (c02_diff_x G hG x y t)

lemma c02_sx_sub (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sx (F - G) = sx F - sx G := by
  funext x y t
  simp only [sx, Pi.sub_apply]
  exact deriv_sub (c02_diff_x F hF x y t) (c02_diff_x G hG x y t)

lemma c02_sx_smul (c : ℝ) (F : XYT) : sx (c • F) = c • sx F := by
  funext x y t
  simp only [sx, Pi.smul_apply, smul_eq_mul]
  exact deriv_const_mul_field c

lemma c02_sx_mul (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sx (F * G) = sx F * G + F * sx G := by
  funext x y t
  simp only [sx, Pi.mul_apply]
  exact deriv_mul (c02_diff_x F hF x y t) (c02_diff_x G hG x y t)

lemma c02_sy_add (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sy (F + G) = sy F + sy G := by
  funext x y t
  simp only [sy, Pi.add_apply]
  exact deriv_add (c02_diff_y F hF x y t) (c02_diff_y G hG x y t)

lemma c02_sy_sub (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sy (F - G) = sy F - sy G := by
  funext x y t
  simp only [sy, Pi.sub_apply]
  exact deriv_sub (c02_diff_y F hF x y t) (c02_diff_y G hG x y t)

lemma c02_sy_smul (c : ℝ) (F : XYT) : sy (c • F) = c • sy F := by
  funext x y t
  simp only [sy, Pi.smul_apply, smul_eq_mul]
  exact deriv_const_mul_field c

lemma c02_sy_mul (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    sy (F * G) = sy F * G + F * sy G := by
  funext x y t
  simp only [sy, Pi.mul_apply]
  exact deriv_mul (c02_diff_y F hF x y t) (c02_diff_y G hG x y t)

lemma c02_st_add (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    st (F + G) = st F + st G := by
  funext x y t
  simp only [st, Pi.add_apply]
  exact deriv_add (c02_diff_t F hF x y t) (c02_diff_t G hG x y t)

lemma c02_st_sub (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    st (F - G) = st F - st G := by
  funext x y t
  simp only [st, Pi.sub_apply]
  exact deriv_sub (c02_diff_t F hF x y t) (c02_diff_t G hG x y t)

lemma c02_st_smul (c : ℝ) (F : XYT) : st (c • F) = c • st F := by
  funext x y t
  simp only [st, Pi.smul_apply, smul_eq_mul]
  exact deriv_const_mul_field c

lemma c02_st_mul (F G : XYT) (hF : Smooth3 F) (hG : Smooth3 G) :
    st (F * G) = st F * G + F * st G := by
  funext x y t
  simp only [st, Pi.mul_apply]
  exact deriv_mul (c02_diff_t F hF x y t) (c02_diff_t G hG x y t)

/-! ### Clairaut swaps (normal form: `st` outermost, then `sx`, then `sy`) -/

lemma c02_sy_sx (W : XYT) (hW : Smooth3 W) : sy (sx W) = sx (sy W) := by
  funext x y t
  exact c02_clairaut (c02_smooth_fixed_t W hW t) x y

lemma c02_sy_st (W : XYT) (hW : Smooth3 W) : sy (st W) = st (sy W) := by
  funext x y t
  exact (c02_clairaut (c02_smooth_fixed_x W hW x) y t).symm

lemma c02_sx_st (W : XYT) (hW : Smooth3 W) : sx (st W) = st (sx W) := by
  funext x y t
  exact (c02_clairaut (c02_smooth_fixed_y W hW y) x t).symm

/-! ### Derivatives of the zero function -/

@[simp] lemma c02_sx_zero : sx (0 : XYT) = 0 := by
  funext x y t
  simp [sx]

@[simp] lemma c02_sy_zero : sy (0 : XYT) = 0 := by
  funext x y t
  simp [sy]

@[simp] lemma c02_st_zero : st (0 : XYT) = 0 := by
  funext x y t
  simp [st]

/-! ## The certificate -/

/-- Numerals in `XYT` are constant functions. -/
@[simp] lemma c02_ofNat_apply (n : ℕ) (x y t : ℝ) :
    ((OfNat.ofNat n : XYT) x y t) = (OfNat.ofNat n : ℝ) := rfl

/-- Numerals in `XT` are constant functions. -/
@[simp] lemma c02_ofNat_apply_XT (n : ℕ) (x t : ℝ) :
    ((OfNat.ofNat n : XT) x t) = (OfNat.ofNat n : ℝ) := rfl

/-- The `y`-slice at `x` is `F x y`. -/
lemma c02_slice_fun (F : XYT) (y x : ℝ) : slice F y x = F x y := rfl

/-! ## Unfolding `cbil` and `chx` on `XYT`

`cbil`/`chx` are defined through `y`-slices; these rewrites put them in `(x,t)`
derivative notation directly on `XYT`. -/

lemma c02_cbil_unfold (a : ℝ) (F G : XYT) :
    cbil a F G
      = sx (sx F) * G - ((2 : XYT) * sx F) * sx G + F * sx (sx G)
        + st F * G - F * st G + (2*a) • (sx F * G - F * sx G) := by
  funext x y t
  simp only [cbil, bil, slice, dx, dt, xx, hx, sx, st, Pi.mul_apply, Pi.sub_apply,
    Pi.add_apply, Pi.smul_apply, c02_ofNat_apply, c02_ofNat_apply_XT, c02_slice_fun]

lemma c02_chx_unfold (F G : XYT) : chx F G = sx F * G - F * sx G := by
  funext x y t
  simp only [chx, hx, slice, dx, sx, Pi.mul_apply, Pi.sub_apply]

/-! ## Log-jet rewrites for `XYT` -/

lemma c02_log_sx' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx F = F * sx (c02log F) := by
  have h := c02_log_sx F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

lemma c02_log_sy' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sy F = F * sy (c02log F) := by
  have h := c02_log_sy F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

lemma c02_log_st' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    st F = F * st (c02log F) := by
  have h := c02_log_st F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

lemma c02_log_sxx' (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx (sx F) = F * (sx (sx (c02log F)) + (sx (c02log F)) ^ 2) := by
  have h := c02_log_sxx F hF (fun x y t => hpos x y t)
  simpa only [c02log_eq] using h

/-- First `x`-derivative of `sy F`, in log coordinates. -/
lemma c02_sx_sy_log (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx (sy F) = sx F * sy (c02log F) + F * sx (sy (c02log F)) := by
  rw [c02_log_sy' F hF hpos]
  exact c02_sx_mul F (sy (c02log F)) hF (c02_smooth_sy (c02_smooth_log hF hpos))

/-- `t`-derivative of `sy F`, in log coordinates. -/
lemma c02_st_sy_log (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    st (sy F) = st F * sy (c02log F) + F * st (sy (c02log F)) := by
  rw [c02_log_sy' F hF hpos]
  exact c02_st_mul F (sy (c02log F)) hF (c02_smooth_sy (c02_smooth_log hF hpos))

/-- Second `x`-derivative of `sy F`, in log coordinates. -/
lemma c02_sxx_sy_log (F : XYT) (hF : Smooth3 F) (hpos : Positive3 F) :
    sx (sx (sy F)) = sx (sx F) * sy (c02log F)
      + (2 : XYT) * (sx F * sx (sy (c02log F))) + F * sx (sx (sy (c02log F))) := by
  have hQ : Smooth3 (c02log F) := c02_smooth_log hF hpos
  have hsyQ : Smooth3 (sy (c02log F)) := c02_smooth_sy hQ
  rw [c02_sx_sy_log F hF hpos,
    c02_sx_add (sx F * sy (c02log F)) (F * sx (sy (c02log F)))
      (c02_smooth_mul (c02_smooth_sx hF) hsyQ)
      (c02_smooth_mul hF (c02_smooth_sx hsyQ)),
    c02_sx_mul (sx F) (sy (c02log F)) (c02_smooth_sx hF) hsyQ,
    c02_sx_mul F (sx (sy (c02log F))) hF (c02_smooth_sx hsyQ)]
  ring

/-- `R = A_xx + (B_x)^2 + B_t + 2a B_x` (the C13 quotient in `A`,`B` coordinates). -/
def c02R (a : ℝ) (A B : XYT) : XYT :=
  sx (sx A) + (sx B) * (sx B) + st B + (2*a) • sx B

/-- `S = 2E + 4 B_x` with `E = q_xxy - 2 B_x q_xy - q_yt - 2a q_xy`, `q = (A-B)/2`. -/
def c02S (a : ℝ) (A B : XYT) : XYT :=
  sx (sx (sy A)) - sx (sx (sy B)) - st (sy A) + st (sy B)
    - (2:ℝ) • ((sx B) * (sx (sy A) - sx (sy B)))
    - (2*a) • (sx (sy A) - sx (sy B)) + (4:ℝ) • sx B

/-- `2 * (q_y R + E + 2 B_x)`: twice the honest third-order hypothesis. -/
def c02E2 (a : ℝ) (A B : XYT) : XYT := (sy A - sy B) * c02R a A B + c02S a A B

/-- All the rewriting used to compare `c1`/`c2` with the certificate. -/
macro "c02_simp" "[" es:Lean.Parser.Tactic.simpLemma,* "]" : tactic =>
  `(tactic|
    (simp (config := { maxDischargeDepth := 40 }) only [c1, c2, c02R, c02S, c02E2,
      c02_smooth_add, c02_smooth_sub, c02_smooth_neg, c02_smooth_mul, c02_smooth_smul,
      c02_smooth_sx, c02_smooth_sy, c02_smooth_st,
      c02_sx_add, c02_sx_sub, c02_sx_smul, c02_sx_mul,
      c02_sy_add, c02_sy_sub, c02_sy_smul, c02_sy_mul,
      c02_st_add, c02_st_sub, c02_st_smul, c02_st_mul,
      c02_sy_sx, c02_sy_st, c02_sx_st, $es,*]))

lemma c02_c1_eq (a : ℝ) (A B : XYT) (hA : Smooth3 A) (hB : Smooth3 B) :
    c1 a ((2:ℝ) • sx B) ((2:ℝ) • sx (sy A))
      = (2:ℝ) • sx (sy (c02R a A B)) := by
  c02_simp [hA, hB]
  funext x y t
  simp only [Pi.add_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-- The second residual identity: `c2 = 2 ∂x∂y R − 2 ∂x S`. -/
lemma c02_c2_eq (a : ℝ) (A B : XYT) (hA : Smooth3 A) (hB : Smooth3 B) :
    c2 a ((2:ℝ) • sx B) ((2:ℝ) • sx (sy A))
      = (2:ℝ) • sx (sy (c02R a A B)) - (2:ℝ) • sx (c02S a A B) := by
  c02_simp [hA, hB]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]
  ring

/-! ## The three bridge identities

With `A = log f + log g`, `B = log f - log g`:

* `cbil a f g = (f*g) * R` where `R = c02R a A B`,
* `chx f g = (f*g) * B_x`,
* `2 * cbil a f (sy g) = (f*g) * (c02E2 a A B - 4 B_x)`. -/

/-- All the rewriting used for the bridge identities. -/
macro "c02_bridge" "[" es:Lean.Parser.Tactic.simpLemma,* "]" : tactic =>
  `(tactic|
    (simp (config := { maxDischargeDepth := 60 }) only [c02R, c02S, c02E2,
      c02_cbil_unfold, c02_chx_unfold,
      c02_log_sx', c02_log_sy', c02_log_st', c02_log_sxx',
      c02_sx_sy_log, c02_st_sy_log, c02_sxx_sy_log,
      c02_smooth_add, c02_smooth_sub, c02_smooth_neg, c02_smooth_mul, c02_smooth_smul,
      c02_smooth_sx, c02_smooth_sy, c02_smooth_st, c02_smooth_log,
      c02_sx_add, c02_sx_sub, c02_sx_smul, c02_sx_mul,
      c02_sy_add, c02_sy_sub, c02_sy_smul, c02_sy_mul,
      c02_st_add, c02_st_sub, c02_st_smul, c02_st_mul,
      c02_sy_sx, c02_sy_st, c02_sx_st, $es,*]))

/-- Bridge 1: the C13 quotient identity in `A`,`B` coordinates. -/
lemma c02_cbil_eq (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g) :
    cbil a f g = (f * g) * c02R a (c02log f + c02log g) (c02log f - c02log g) := by
  c02_bridge [hf, hg, hfp, hgp]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    Pi.pow_apply, c02_ofNat_apply, c02_ofNat_apply_XT]
  ring

/-- Bridge 2: `chx f g = (f*g) * B_x`. -/
lemma c02_chx_eq (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g) :
    chx f g = (f * g) * sx (c02log f - c02log g) := by
  c02_bridge [hf, hg, hfp, hgp]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]
  ring

/-- Bridge 3: the `y`-derivative of `cbil` in `A`,`B` coordinates. -/
lemma c02_cbil_syg_eq (a : ℝ) (f g : XYT) (hf : Smooth3 f) (hg : Smooth3 g)
    (hfp : Positive3 f) (hgp : Positive3 g) :
    (2:ℝ) • cbil a f (sy g)
      = (f * g) * (c02E2 a (c02log f + c02log g) (c02log f - c02log g)
          - (4:ℝ) • sx (c02log f - c02log g)) := by
  c02_bridge [hf, hg, hfp, hgp]
  funext x y t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    Pi.pow_apply, c02_ofNat_apply, c02_ofNat_apply_XT]
  ring


/-! ## `cu`, `cv` in `A`,`B` coordinates -/

lemma c02_log_sub_eq (f g : XYT) :
    (fun x y t => Real.log (f x y t) - Real.log (g x y t)) = c02log f - c02log g := by
  funext x y t
  simp only [Pi.sub_apply, c02log_eq]

lemma c02_log_add_eq (f g : XYT) :
    (fun x y t => Real.log (f x y t) + Real.log (g x y t)) = c02log f + c02log g := by
  funext x y t
  simp only [Pi.add_apply, c02log_eq]

lemma c02_cu_eq (f g : XYT) :
    cu f g = (2:ℝ) • sx (c02log f - c02log g) := by
  funext x y t
  simp only [cu, c02_log_sub_eq, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]

lemma c02_cv_eq (f g : XYT) :
    cv f g = (2:ℝ) • sx (sy (c02log f + c02log g)) := by
  funext x y t
  simp only [cv, c02_log_add_eq, Pi.mul_apply, Pi.smul_apply, smul_eq_mul,
    c02_ofNat_apply]

/-! ## The target -/

/-- **C02 is proved.**

With `A = log f + log g`, `B = log f - log g`, `R := c02R a A B`, `S := c02S a A B`
and `E2 := (A_y - B_y) * R + S` the certificate is

* `cbil a f g = (f*g) * R` and `chx f g = (f*g) * B_x`,
* `2 * cbil a f (sy g) = (f*g) * (E2 - 4 B_x)`,
* `R = 0` and `E2 = 0` follow from `ContinuousPair`, hence `S = 0`,
* `c1 a (cu f g) (cv f g) = 2 ∂x∂y R` and `c2 a (cu f g) (cv f g) = 2 ∂x∂y R - 2 ∂x S`. -/
theorem c02_proved : C02 := by
  intro a f g hf hg hfp hgp hcont
  obtain ⟨hI, hII⟩ := c02_hyp_from_ContinuousPair a f g hf hg hcont
  set A : XYT := c02log f + c02log g with hAdef
  set B : XYT := c02log f - c02log g with hBdef
  have hA : Smooth3 A := by
    rw [hAdef]
    exact c02_smooth_add (c02_smooth_log hf hfp) (c02_smooth_log hg hgp)
  have hB : Smooth3 B := by
    rw [hBdef]
    exact c02_smooth_sub (c02_smooth_log hf hfp) (c02_smooth_log hg hgp)
  have hb1 : cbil a f g = (f * g) * c02R a A B := by
    rw [hAdef, hBdef]
    exact c02_cbil_eq a f g hf hg hfp hgp
  have hb2 : chx f g = (f * g) * sx B := by
    rw [hBdef]
    exact c02_chx_eq f g hf hg hfp hgp
  have hb3 : (2:ℝ) • cbil a f (sy g)
      = (f * g) * (c02E2 a A B - (4:ℝ) • sx B) := by
    rw [hAdef, hBdef]
    exact c02_cbil_syg_eq a f g hf hg hfp hgp
  have hR : c02R a A B = 0 := by
    funext x y t
    have hzero : (f * g) * c02R a A B = 0 := by rw [← hb1, hI]
    have hpt : (f x y t * g x y t) * c02R a A B x y t = 0 := by
      have hh := congrFun (congrFun (congrFun hzero x) y) t
      simpa [Pi.mul_apply] using hh
    rcases mul_eq_zero.mp hpt with h | h
    · exact absurd h (mul_ne_zero (ne_of_gt (hfp x y t)) (ne_of_gt (hgp x y t)))
    · exact h
  have hE2 : c02E2 a A B = 0 := by
    funext x y t
    have h1 : cbil a f (sy g) x y t + 2 * (chx f g x y t) = 0 := by
      have hh := congrFun (congrFun (congrFun hII x) y) t
      simpa using hh
    have h2 : chx f g x y t = (f x y t * g x y t) * sx B x y t := by
      have hh := congrFun (congrFun (congrFun hb2 x) y) t
      simpa [Pi.mul_apply] using hh
    have h3 : 2 * (cbil a f (sy g) x y t)
        = (f x y t * g x y t) * (c02E2 a A B x y t - 4 * (sx B x y t)) := by
      have hh := congrFun (congrFun (congrFun hb3 x) y) t
      simpa [Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul] using hh
    have hpt : (f x y t * g x y t) * c02E2 a A B x y t = 0 := by
      nlinarith [h1, h2, h3]
    rcases mul_eq_zero.mp hpt with h | h
    · exact absurd h (mul_ne_zero (ne_of_gt (hfp x y t)) (ne_of_gt (hgp x y t)))
    · exact h
  have hS : c02S a A B = 0 := by
    have h := hE2
    rw [c02E2, hR] at h
    simpa using h
  have hcu : cu f g = (2:ℝ) • sx B := by
    rw [c02_cu_eq f g, hBdef]
  have hcv : cv f g = (2:ℝ) • sx (sy A) := by
    rw [c02_cv_eq f g, hAdef]
  refine ⟨?_, ?_⟩
  · rw [hcu, hcv, c02_c1_eq a A B hA hB, hR]
    simp
  · rw [hcu, hcv, c02_c2_eq a A B hA hB, hR, hS]
    simp
/-- `c02_gap` and `C02` are the same statement; the placeholder `Prop` of the
earlier draft is therefore inhabited by the real proof. -/
theorem c02_gap_proved : c02_gap := c02_proved
end DLWContract
