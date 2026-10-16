import PeriodicCoefficients
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

namespace DLWLean
noncomputable section
open scoped ContDiff

/-- The actual primitive exists for every smooth periodic test function.
It need not be periodic, and is used only for scalar gauge commutators. -/
def smoothSpatialPrimitive {Lx : ℝ} (f : PeriodicCoefficient Lx) (x : ℝ) : ℝ :=
  ∫ y in (0 : ℝ)..x, (f : ℝ → ℝ) y

theorem smoothSpatialPrimitive_hasDerivAt {Lx : ℝ}
    (f : PeriodicCoefficient Lx) (x : ℝ) :
    HasDerivAt (smoothSpatialPrimitive f) ((f : ℝ → ℝ) x) x := by
  apply intervalIntegral.integral_hasDerivAt_right
  · exact f.property.1.continuous.intervalIntegrable 0 x
  · exact f.property.1.continuous.aestronglyMeasurable.stronglyMeasurableAtFilter
  · exact f.property.1.continuous.continuousAt

theorem smoothSpatialPrimitive_deriv {Lx : ℝ} (f : PeriodicCoefficient Lx) :
    deriv (smoothSpatialPrimitive f) = (f : ℝ → ℝ) :=
  funext fun x => (smoothSpatialPrimitive_hasDerivAt f x).deriv

theorem smoothSpatialPrimitive_smooth {Lx : ℝ} (f : PeriodicCoefficient Lx) :
    ContDiff ℝ ∞ (smoothSpatialPrimitive f) := by
  apply contDiff_infty_iff_deriv.mpr
  refine ⟨fun x => (smoothSpatialPrimitive_hasDerivAt f x).differentiableAt, ?_⟩
  rw [smoothSpatialPrimitive_deriv]
  exact f.property.1

#print axioms smoothSpatialPrimitive_smooth
end
end DLWLean
