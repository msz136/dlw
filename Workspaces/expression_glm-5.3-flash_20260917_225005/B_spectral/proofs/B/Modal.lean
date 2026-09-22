import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp

/-!
# B-direction: Fourier-in-y modal infrastructure (spectral along y)

Setting (direction B): the DLW system (W1)(W2) with **only y discretized**;
y is periodic on [0, 2π), so the exact discretization along y is Fourier.
A y-periodic function is represented by its Fourier coefficient sequence
`u : ℤ → ℂ`. The exact identity ∂_y e^{iℓy} = iℓ e^{iℓy} means the modal
y-derivative is multiplication by iℓ — no discretization error per mode.

This module records the structural facts about the zero mode:
* mode 0 is the kernel of the modal ∂_y (the y-mean of u is NOT determined
  by u_y; w = u_y leaves the y-mean of u free);
* on every mode ℓ ≠ 0 the multiplier is invertible, with the explicit
  constructive inverse û_ℓ = ĝ_ℓ / (iℓ);
* equality of two ∂_y-images determines all modes except mode 0.

These are exact statements about the modal (spectral) representation;
no smoothness or convergence assumptions are needed at this level.
-/

namespace DLWBSpec

/-- The exact y-derivative multiplier on Fourier mode ℓ: ∂_y e^{iℓy} = iℓ e^{iℓy}. -/
def dyMul (ℓ : ℤ) : ℂ := Complex.I * (ℓ : ℂ)

theorem dyMul_apply (ℓ : ℤ) : dyMul ℓ = Complex.I * (ℓ : ℂ) := rfl

@[simp] theorem dyMul_zero : dyMul 0 = 0 := by simp [dyMul]

theorem dyMul_ne_zero {ℓ : ℤ} (h : ℓ ≠ 0) : dyMul ℓ ≠ 0 := by
  have hz : Complex.I * (ℓ : ℂ) = 0 → ℓ = 0 := by
    intro hne
    rw [mul_eq_zero, or_iff_right Complex.I_ne_zero, Int.cast_eq_zero] at hne
    exact hne
  intro hne
  exact absurd (hz hne) h

/-- Constructive inversion of the multiplier on mode ℓ ≠ 0:
    the recovered modal coefficient is û_ℓ = ĝ_ℓ / (iℓ). -/
theorem mul_div_cancel' {ℓ : ℤ} (h : ℓ ≠ 0) (g : ℂ) :
    dyMul ℓ * (g / dyMul ℓ) = g := by
  have h0 : dyMul ℓ ≠ 0 := dyMul_ne_zero h
  field_simp [h0]

/-- A y-periodic function represented by its Fourier coefficient sequence. -/
abbrev ModalFun := ℤ → ℂ

/-- Exact modal y-derivative: (D_y u)_ℓ = iℓ · û_ℓ. -/
def dySeq (u : ModalFun) : ModalFun := fun ℓ => dyMul ℓ * u ℓ

@[simp] theorem dySeq_apply (u : ModalFun) (ℓ : ℤ) : dySeq u ℓ = dyMul ℓ * u ℓ := rfl

/-- Multiplication by the nonzero multiplier kills exactly the zero factor. -/
theorem dyMul_mul_eq_zero {ℓ : ℤ} (h : ℓ ≠ 0) (x : ℂ) :
    dyMul ℓ * x = 0 ↔ x = 0 := by
  rw [mul_eq_zero, or_iff_right (dyMul_ne_zero h)]

/-- **Zero-mode kernel**: the modal ∂_y vanishes exactly on the pure-mean
component. Mode 0 of u is killed by ∂_y and nothing else is. -/
theorem dySeq_eq_zero_iff (u : ModalFun) :
    dySeq u = 0 ↔ ∀ ℓ : ℤ, ℓ ≠ 0 → u ℓ = 0 := by
  constructor
  · intro h ℓ hℓ
    have h0 : dySeq u ℓ = 0 := by simpa using congrFun h ℓ
    rwa [dySeq_apply, dyMul_mul_eq_zero hℓ] at h0
  · intro h
    funext ℓ
    rcases eq_or_ne ℓ 0 with rfl | hℓ
    · simp
    · simp only [dySeq_apply, Pi.zero_apply, dyMul_mul_eq_zero hℓ]
      exact h ℓ hℓ

/-- **Mean-mode freedom**: two coefficient sequences have the same ∂_y
iff they agree on every mode ℓ ≠ 0. In particular the value of û_0 (the
y-mean of u) is not determined by ĝ = u_y. -/
theorem dySeq_eq_iff (u v : ModalFun) :
    dySeq u = dySeq v ↔ ∀ ℓ : ℤ, ℓ ≠ 0 → u ℓ = v ℓ := by
  constructor
  · intro h ℓ hℓ
    exact mul_left_cancel₀ (dyMul_ne_zero hℓ) (congrFun h ℓ)
  · intro h
    funext ℓ
    rcases eq_or_ne ℓ 0 with rfl | hℓ
    · simp
    · simp only [dySeq_apply, h ℓ hℓ]

/-- **Constructive inverse**: given ĝ, the canonical zero-mean preimage
û with (D_y û)_ℓ = ĝ_ℓ for every ℓ ≠ 0 (and û_0 = 0). -/
noncomputable def dyInverse (g : ModalFun) : ModalFun :=
  fun ℓ => if ℓ = 0 then 0 else g ℓ / dyMul ℓ

theorem dyInverse_apply {g : ModalFun} {ℓ : ℤ} (h : ℓ ≠ 0) :
    dySeq (dyInverse g) ℓ = g ℓ := by
  simp only [dySeq_apply, dyInverse, if_neg h, mul_div_cancel' h]

/-- Uniqueness within the zero-mean class: if û has zero mode 0 and
(D_y û)_ℓ = ĝ_ℓ for all ℓ ≠ 0, then û = dyInverse ĝ. -/
theorem dyInverse_unique {g û : ModalFun} (h0 : û 0 = 0)
    (h : ∀ ℓ : ℤ, ℓ ≠ 0 → dySeq û ℓ = g ℓ) : û = dyInverse g := by
  funext ℓ
  rcases eq_or_ne ℓ 0 with rfl | hℓ
  · simp [dyInverse, h0]
  · simp only [dyInverse, if_neg hℓ]
    have h1 : dyMul ℓ * û ℓ = g ℓ := by rw [← dySeq_apply]; exact h ℓ hℓ
    rw [eq_div_iff (dyMul_ne_zero hℓ), mul_comm]
    exact h1

end DLWBSpec
