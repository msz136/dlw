import Contracts
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Tactic

noncomputable section
open Set
namespace DLWContract.UniformTaylor

/-- A uniform second-order estimate from an actual pair of derivatives. -/
theorem second_order_of_bound {Z : Type*} (K : Set Z) (d C : ℝ) (hC : 0≤C)
    (f f1 f2 : ℝ → Z → ℝ)
    (hf : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f s z) (f1 h z) h)
    (hf1 : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f1 s z) (f2 h z) h)
    (hzero : ∀ z ∈ K, f1 0 z=0)
    (hbound : ∀ z ∈ K, ∀ h ∈ Icc 0 d, |f2 h z|≤C) :
    ∀ z ∈ K, ∀ h ∈ Icc 0 d, |f h z-f 0 z|≤C*h^2 := by
  intro z hz h hh
  have hfirst (s : ℝ) (hs : s ∈ Icc 0 h) : |f1 s z|≤C*s := by
    have hb : ∀ r ∈ Ico 0 h, ‖f2 r z‖≤C := by
      intro r hr
      rw [Real.norm_eq_abs]
      exact hbound z hz r ⟨hr.1,hr.2.le.trans hh.2⟩
    have H := norm_image_sub_le_of_norm_deriv_le_segment'
      (a := (0 : ℝ)) (b := h) (C := C) (f := fun s => f1 s z) (f' := fun s => f2 s z)
      (fun r hr => (hf1 z hz r ⟨hr.1,hr.2.trans hh.2⟩).hasDerivWithinAt)
      hb s hs
    simpa only [hzero z hz,sub_zero,Real.norm_eq_abs] using H
  have H := norm_image_sub_le_of_norm_deriv_le_segment'
    (a := (0 : ℝ)) (b := h) (C := C*h) (f := fun s => f s z) (f' := fun s => f1 s z)
    (fun r hr => (hf z hz r ⟨hr.1,hr.2.trans hh.2⟩).hasDerivWithinAt)
    (fun r hr => by
      rw [Real.norm_eq_abs]
      exact (hfirst r ⟨hr.1,hr.2.le⟩).trans (mul_le_mul_of_nonneg_left hr.2.le hC))
    h ⟨hh.1,le_rfl⟩
  simpa only [Real.norm_eq_abs,sub_zero,pow_two,mul_assoc] using H

/-- Compactness turns a continuous second derivative into a single constant
valid for every spatial parameter in the compact set. -/
theorem second_order_on_compact {Z : Type*} [TopologicalSpace Z]
    (K : Set Z) (hK : IsCompact K) (d : ℝ)
    (f f1 f2 : ℝ → Z → ℝ)
    (hf : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f s z) (f1 h z) h)
    (hf1 : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f1 s z) (f2 h z) h)
    (hzero : ∀ z ∈ K, f1 0 z=0)
    (hcont : ContinuousOn (fun p : ℝ × Z => f2 p.1 p.2) (Icc 0 d ×ˢ K)) :
    ∃ C : ℝ, 0≤C ∧ ∀ z ∈ K, ∀ h ∈ Icc 0 d, |f h z-f 0 z|≤C*h^2 := by
  obtain ⟨C,hC⟩ := (isCompact_Icc.prod hK).exists_bound_of_continuousOn hcont
  refine ⟨max C 0,le_max_right _ _,second_order_of_bound K d (max C 0)
    (le_max_right _ _) f f1 f2 hf hf1 hzero ?_⟩
  intro z hz h hh
  have H : |f2 h z|≤C := by simpa only [Real.norm_eq_abs] using hC (h,z) ⟨hh,hz⟩
  exact H.trans (le_max_left _ _)

theorem third_order_of_bound {Z : Type*} (K : Set Z) (d C : ℝ) (hC : 0≤C)
    (f f1 f2 f3 : ℝ → Z → ℝ)
    (hf : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f s z) (f1 h z) h)
    (hf1 : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f1 s z) (f2 h z) h)
    (hf2 : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f2 s z) (f3 h z) h)
    (hz1 : ∀ z ∈ K, f1 0 z=0) (hz2 : ∀ z ∈ K, f2 0 z=0)
    (hbound : ∀ z ∈ K, ∀ h ∈ Icc 0 d, |f3 h z|≤C) :
    ∀ z ∈ K, ∀ h ∈ Icc 0 d, |f h z-f 0 z|≤C*h^3 := by
  have H2 := second_order_of_bound K d C hC f1 f2 f3 hf1 hf2 hz2 hbound
  intro z hz h hh
  have hb : ∀ r ∈ Ico 0 h, ‖f1 r z‖≤C*h^2 := by
    intro r hr
    have H := H2 z hz r ⟨hr.1,hr.2.le.trans hh.2⟩
    simp only [hz1 z hz,sub_zero] at H
    rw [Real.norm_eq_abs]
    exact H.trans (mul_le_mul_of_nonneg_left (pow_le_pow_left₀ hr.1 hr.2.le 2) hC)
  have H := norm_image_sub_le_of_norm_deriv_le_segment'
    (a := (0 : ℝ)) (b := h) (C := C*h^2) (f := fun s => f s z) (f' := fun s => f1 s z)
    (fun r hr => (hf z hz r ⟨hr.1,hr.2.trans hh.2⟩).hasDerivWithinAt) hb h ⟨hh.1,le_rfl⟩
  simpa only [Real.norm_eq_abs,sub_zero,pow_succ,mul_assoc] using H

theorem third_order_on_compact {Z : Type*} [TopologicalSpace Z]
    (K : Set Z) (hK : IsCompact K) (d : ℝ)
    (f f1 f2 f3 : ℝ → Z → ℝ)
    (hf : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f s z) (f1 h z) h)
    (hf1 : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f1 s z) (f2 h z) h)
    (hf2 : ∀ z ∈ K, ∀ h ∈ Icc 0 d, HasDerivAt (fun s => f2 s z) (f3 h z) h)
    (hz1 : ∀ z ∈ K, f1 0 z=0) (hz2 : ∀ z ∈ K, f2 0 z=0)
    (hcont : ContinuousOn (fun p : ℝ × Z => f3 p.1 p.2) (Icc 0 d ×ˢ K)) :
    ∃ C : ℝ, 0≤C ∧ ∀ z ∈ K, ∀ h ∈ Icc 0 d, |f h z-f 0 z|≤C*h^3 := by
  obtain ⟨C,hC⟩ := (isCompact_Icc.prod hK).exists_bound_of_continuousOn hcont
  refine ⟨max C 0,le_max_right _ _,third_order_of_bound K d (max C 0)
    (le_max_right _ _) f f1 f2 f3 hf hf1 hf2 hz1 hz2 ?_⟩
  intro z hz h hh
  have H : |f3 h z|≤C := by simpa only [Real.norm_eq_abs] using hC (h,z) ⟨hh,hz⟩
  exact H.trans (le_max_left _ _)

#print axioms second_order_on_compact
#print axioms third_order_on_compact
end DLWContract.UniformTaylor
