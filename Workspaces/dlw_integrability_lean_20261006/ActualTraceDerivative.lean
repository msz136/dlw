import PeriodicSpacetimeCoefficients
import ResidueIntegral
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.Analysis.Normed.Group.Bounded
import Mathlib.Topology.Order.Compact
import Mathlib.Tactic

namespace DLWLean
noncomputable section
open Set Filter MeasureTheory
open scoped Topology

/-- Ordinary differentiation under an actual integral on a finite period.
The derivative bound is derived on a compact rectangle, not postulated. -/
theorem integral_time_derivative_of_continuous
    (Lx : ℝ) (hLx : 0 < Lx) (F F' : ℝ → ℝ → ℝ)
    (hF : Continuous (Function.uncurry F))
    (hF' : Continuous (Function.uncurry F'))
    (hdiff : ∀ t x, HasDerivAt (fun τ => F τ x) (F' t x) t)
    (t : ℝ) :
    HasDerivAt (fun τ => ∫ x in (0 : ℝ)..Lx, F τ x)
      (∫ x in (0 : ℝ)..Lx, F' t x) t := by
  let K : Set (ℝ × ℝ) := Icc (t - 1) (t + 1) ×ˢ Icc 0 Lx
  have hcompact : IsCompact K := isCompact_Icc.prod isCompact_Icc
  obtain ⟨bound, hbound⟩ := hcompact.exists_bound_of_continuousOn hF'.continuousOn
  have hslice (τ : ℝ) : Continuous (F τ) :=
    hF.comp (continuous_const.prodMk continuous_id)
  have hslice' (τ : ℝ) : Continuous (F' τ) :=
    hF'.comp (continuous_const.prodMk continuous_id)
  have hnhds : Ioo (t - 1) (t + 1) ∈ 𝓝 t := Ioo_mem_nhds (by linarith) (by linarith)
  have h := intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (a := (0 : ℝ)) (b := Lx) (μ := volume) (F := F) (F' := F')
    (bound := fun _ => bound) hnhds
    (Filter.Eventually.of_forall (fun τ => (hslice τ).aestronglyMeasurable))
    ((hslice t).intervalIntegrable 0 Lx)
    (hslice' t).aestronglyMeasurable
    (Filter.Eventually.of_forall (fun x hx τ hτ => by
      have hx' : x ∈ Icc (0 : ℝ) Lx := by
        have hx0 : x ∈ Ioc (0 : ℝ) Lx := by
          simpa only [uIoc_of_le hLx.le] using hx
        exact ⟨hx0.1.le, hx0.2⟩
      exact hbound (τ, x) ⟨⟨hτ.1.le, hτ.2.le⟩, hx'⟩))
    (continuous_const.intervalIntegrable 0 Lx)
    (Filter.Eventually.of_forall (fun x _ τ _ => hdiff τ x))
  exact h.2

def spacetimeSlice (Lx t : ℝ) :
    PeriodicSpacetimeCoefficient Lx →ₗ[ℝ] PeriodicCoefficient Lx where
  toFun f := ⟨fun x => (f : ℝ × ℝ → ℝ) (t, x),
    PeriodicSpacetimeCoefficient.space_slice_smooth f t, f.property.2 t⟩
  map_add' f g := rfl
  map_smul' r f := rfl

def spacetimePeriodIntegral (Lx t : ℝ) :
    PeriodicSpacetimeCoefficient Lx →ₗ[ℝ] ℝ :=
  (periodicCoefficientIntegral Lx).comp (spacetimeSlice Lx t)

theorem spacetimePeriodIntegral_hasDerivAt
    (Lx : ℝ) (hLx : 0 < Lx) (f : PeriodicSpacetimeCoefficient Lx) (t : ℝ) :
    HasDerivAt (fun τ => spacetimePeriodIntegral Lx τ f)
      (spacetimePeriodIntegral Lx t
        ((periodicSpacetimeTimeEvolution Lx).toLinearMap f)) t := by
  apply integral_time_derivative_of_continuous Lx hLx
    (fun τ x => (f : ℝ × ℝ → ℝ) (τ, x))
    (fun τ x => spacetimeTimeDerivative (f : ℝ × ℝ → ℝ) (τ, x))
  · exact f.property.1.continuous
  · exact (spacetimeTimeDerivative_smooth _ f.property.1).continuous
  · intro τ x
    exact ((PeriodicSpacetimeCoefficient.time_slice_smooth f x).differentiable
      (by simp) τ).hasDerivAt

def spacetimeResidueTrace {A : Type*} [Ring A] [Algebra ℝ A]
    (Lx t : ℝ) (residue : A →ₗ[ℝ] PeriodicSpacetimeCoefficient Lx)
    (hcyclic : ∀ a b, spacetimePeriodIntegral Lx t (residue (a * b)) =
      spacetimePeriodIntegral Lx t (residue (b * a))) : CyclicTrace A where
  toLinearMap := (spacetimePeriodIntegral Lx t).comp residue
  cyclic := hcyclic

/-- The ordinary time derivative equals the algebraic spectral rate when
the PDO residue commutes with the actual time coefficient derivation. -/
theorem actualSpectralInvariant_hasDerivAt
    {A : Type*} [Ring A] [Algebra ℝ A]
    (Lx : ℝ) (hLx : 0 < Lx) (residue : A →ₗ[ℝ] PeriodicSpacetimeCoefficient Lx)
    (v : AlgebraEvolution A)
    (hresidueTime : ∀ a, residue (v.toLinearMap a) =
      (periodicSpacetimeTimeEvolution Lx).toLinearMap (residue a))
    (L : A) (n : ℕ) (t : ℝ) :
    HasDerivAt
      (fun τ => (n : ℝ)⁻¹ * spacetimePeriodIntegral Lx τ (residue (L ^ n)))
      ((n : ℝ)⁻¹ * spacetimePeriodIntegral Lx t (residue (v.toLinearMap (L ^ n)))) t := by
  rw [hresidueTime]
  exact (spacetimePeriodIntegral_hasDerivAt Lx hLx (residue (L ^ n)) t).const_mul _

#print axioms integral_time_derivative_of_continuous
#print axioms actualSpectralInvariant_hasDerivAt
end
end DLWLean
