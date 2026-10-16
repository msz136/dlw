import PeriodicCoefficients
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

namespace DLWLean
noncomputable section

/-- The concrete scalar coefficient integral over one spatial period. -/
def periodicCoefficientIntegral (Lx : ℝ) : PeriodicCoefficient Lx →ₗ[ℝ] ℝ where
  toFun f := ∫ x in (0 : ℝ)..Lx, (f : ℝ → ℝ) x
  map_add' f g := by
    exact intervalIntegral.integral_add
      (f.property.1.continuous.intervalIntegrable 0 Lx)
      (g.property.1.continuous.intervalIntegrable 0 Lx)
  map_smul' r f := by
    change (∫ x in (0 : ℝ)..Lx, r • (f : ℝ → ℝ) x) =
      r • (∫ x in (0 : ℝ)..Lx, (f : ℝ → ℝ) x)
    exact intervalIntegral.integral_smul r _

/-- Total spatial derivatives have zero actual period integral. -/
theorem periodicCoefficientIntegral_space_zero (Lx : ℝ)
    (f : PeriodicCoefficient Lx) :
    periodicCoefficientIntegral Lx ((periodicSpatialEvolution Lx).toLinearMap f) = 0 := by
  change (∫ x in (0 : ℝ)..Lx, deriv (f : ℝ → ℝ) x) = 0
  rw [intervalIntegral.integral_deriv_eq_sub
    (fun x _ => f.property.1.differentiable (by simp) x)
    ((PeriodicCoefficient.spatialDerivative f).property.1.continuous.intervalIntegrable 0 Lx)]
  have hp := f.property.2 0
  simpa using sub_eq_zero.mpr (by simpa using hp)

/-- Integration by parts in the genuine coefficient algebra. -/
theorem periodicCoefficientIntegral_parts (Lx : ℝ)
    (f g : PeriodicCoefficient Lx) :
    periodicCoefficientIntegral Lx
        (f * (periodicSpatialEvolution Lx).toLinearMap g) =
      -periodicCoefficientIntegral Lx
        ((periodicSpatialEvolution Lx).toLinearMap f * g) := by
  have h := periodicCoefficientIntegral_space_zero Lx (f * g)
  rw [(periodicSpatialEvolution Lx).leibniz, map_add] at h
  exact eq_neg_of_add_eq_zero_right h

/-- Trace is the actual period integral of the supplied PDO residue map.
Its cyclic law is exactly the external theoretical premise authorized
by the user; the trace is not an unrelated matrix trace. -/
def periodicResidueTrace {A : Type*} [Ring A] [Algebra ℝ A]
    (Lx : ℝ) (residue : A →ₗ[ℝ] PeriodicCoefficient Lx)
    (hcyclic : ∀ a b, periodicCoefficientIntegral Lx (residue (a * b)) =
      periodicCoefficientIntegral Lx (residue (b * a))) : CyclicTrace A where
  toLinearMap := (periodicCoefficientIntegral Lx).comp residue
  cyclic := hcyclic

theorem spectralInvariant_eq_residueIntegral
    {A : Type*} [Ring A] [Algebra ℝ A]
    (Lx : ℝ) (residue : A →ₗ[ℝ] PeriodicCoefficient Lx)
    (hcyclic : ∀ a b, periodicCoefficientIntegral Lx (residue (a * b)) =
      periodicCoefficientIntegral Lx (residue (b * a)))
    (L : A) (n : ℕ) :
    spectralInvariant (periodicResidueTrace Lx residue hcyclic) L n =
      (n : ℝ)⁻¹ * ∫ x in (0 : ℝ)..Lx, (residue (L ^ n) : ℝ → ℝ) x := rfl

#print axioms spectralInvariant_eq_residueIntegral
end
end DLWLean
