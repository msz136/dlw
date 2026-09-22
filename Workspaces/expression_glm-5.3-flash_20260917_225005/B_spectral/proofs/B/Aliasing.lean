import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Data.Int.Interval
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Order.Interval.Finset.Defs
import B.Modal

/-!
# B-direction: products of y-modes — exact Leibniz, band doubling, truncation loss

Physical picture: x and t stay continuous; only y is truncated, on the
periodic cell [0, 2π). A y-periodic function is a trigonometric polynomial
when its coefficient sequence is finitely supported; pointwise products of
trigonometric polynomials are exact (coefficient = discrete convolution).
This module proves, at the level of Fourier coefficients:

1. **Exact Leibniz rule in modal space** (no aliasing at this level):
   (D_y (u·v))_m = Σ_j (i j) u_j v_{m−j} + Σ_j u_j (i (m−j)) v_{m−j}.

2. **Band doubling**: the product of two band-M factors is band-2M.

3. **Truncation loss**: the Galerkin projection Π_N discards exactly the
   modes N < |ℓ| ≤ 2M of a product of band-M factors; concretely, the
   single mode e^{iNy} squared has coefficient 1 at mode 2N ∉ band N.

LEVEL-2 REMARK (documented, not formalized): classical aliasing (folding
mode 2N ↦ 2N − (2N+1) = −1 on a (2N+1)-point y-grid) arises only if one
*additionally* computes the nonlinear products on a physical y-grid
(pseudo-spectral collocation). With x continuous and y truncated by
Galerkin projection there is no y-grid and hence no aliasing artifact;
x-products are never aliased because x is continuous.
-/

namespace DLWBSpec

/-- Band-limited (finite modal truncation) coefficient sequence. -/
def BandLim (N : ℕ) (u : ModalFun) : Prop :=
  ∀ ℓ : ℤ, (N : ℤ) < ℓ ∨ ℓ < -(N : ℤ) → u ℓ = 0

/-- Discrete convolution over the window [−M, M] (exact for sequences
supported in [−M, M]). -/
def conv (M : ℕ) (u v : ModalFun) : ModalFun :=
  fun m => ∑ j ∈ Finset.Ico (-(M : ℤ)) ((M : ℤ) + 1), u j * v (m - j)

theorem conv_apply (M : ℕ) (u v : ModalFun) (m : ℤ) :
    conv M u v m = ∑ j ∈ Finset.Ico (-(M : ℤ)) ((M : ℤ) + 1), u j * v (m - j) := rfl

/-- **Exact product rule in modal space** (no aliasing at this level). -/
theorem conv_Leibniz (M : ℕ) (u v : ModalFun) (m : ℤ) :
    dyMul m * conv M u v m = conv M (dySeq u) v m + conv M u (dySeq v) m := by
  have hstep : ∀ j ∈ Finset.Ico (-(M : ℤ)) ((M : ℤ) + 1),
      dyMul m * (u j * v (m - j)) =
        (dyMul j * u j) * v (m - j) + u j * (dyMul (m - j) * v (m - j)) := by
    intro j _
    have hm : dyMul m = dyMul j + dyMul (m - j) := by
      simp only [dyMul, Int.cast_sub]
      ring
    rw [hm]
    ring
  simp only [conv, Finset.mul_sum]
  rw [← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun j hj => hstep j hj

/-- **Band doubling**: product of band-M factors is band-2M. -/
theorem conv_band_double {M : ℕ} {u v : ModalFun}
    (hu : BandLim M u) (hv : BandLim M v) :
    BandLim (2 * M) (conv M u v) := by
  intro m hm
  rw [conv_apply]
  refine Finset.sum_eq_zero fun j hj => ?_
  obtain ⟨hj1, hj2⟩ := Finset.mem_Ico.mp hj
  rcases hm with hbig | hsmall
  · have hvz : v (m - j) = 0 := by
      refine hv (m - j) ?_
      left
      push_cast at hbig hj2 ⊢
      linarith
    rw [hvz, mul_zero]
  · have hvz : v (m - j) = 0 := by
      refine hv (m - j) ?_
      right
      push_cast at hsmall hj1 ⊢
      linarith
    rw [hvz, mul_zero]

/-- Galerkin projection onto the retained band |ℓ| ≤ N. -/
def proj (N : ℕ) (u : ModalFun) : ModalFun :=
  fun ℓ => if (N : ℤ) < ℓ ∨ ℓ < -(N : ℤ) then 0 else u ℓ

/-- y-truncation commutes with the exact y-derivative: the multiplier is
diagonal in modes, so no aliasing can enter through ∂_y itself. -/
theorem proj_dySeq (N : ℕ) (u : ModalFun) :
    dySeq (proj N u) = proj N (dySeq u) := by
  funext ℓ
  by_cases h : (N : ℤ) < ℓ ∨ ℓ < -(N : ℤ)
  · simp [proj, h, dySeq_apply]
  · simp [proj, h, dySeq_apply]

/-- **Explicit truncation loss**: the single mode e^{iNy} squared has modal
coefficient 1 at mode 2N, outside the retained band |ℓ| ≤ N (N ≥ 1).
This is the precise content a Galerkin projection discards — and the mode
that a level-2 y-grid computation would fold back to mode 2N − (2N+1) = −1
(classical aliasing). -/
theorem mode_doubling_example {N : ℕ} (hN : 0 < N) :
    conv N (fun ℓ => if ℓ = (N : ℤ) then 1 else 0)
          (fun ℓ => if ℓ = (N : ℤ) then 1 else 0) (2 * (N : ℤ)) = 1 := by
  have hmem : (N : ℤ) ∈ Finset.Ico (-(N : ℤ)) ((N : ℤ) + 1) := by
    rw [Finset.mem_Ico]
    constructor <;> push_cast <;> omega
  have hne : ∀ j ∈ Finset.Ico (-(N : ℤ)) ((N : ℤ) + 1), j ≠ (N : ℤ) →
      ((if j = (N : ℤ) then (1 : ℂ) else 0) *
        (if 2 * (N : ℤ) - j = (N : ℤ) then 1 else 0)) = 0 := by
    intro j _ hj
    rw [if_neg hj, zero_mul]
  rw [conv_apply, Finset.sum_eq_single (N : ℤ) hne
    (fun hnot => by exfalso; exact absurd hmem hnot)]
  have h2N : 2 * (N : ℤ) - (N : ℤ) = (N : ℤ) := by push_cast; omega
  simp [h2N]

end DLWBSpec
