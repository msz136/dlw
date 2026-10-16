import FieldCoordinates
import CyclicTrace
import Mathlib.Algebra.Algebra.Subalgebra.Basic
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Shift
import Mathlib.Analysis.Calculus.Deriv.Mul

namespace DLWLean
noncomputable section
open scoped ContDiff

/-- The actual coefficient algebra of smooth periodic real functions. -/
def periodicCoefficientAlgebra (Lx : ℝ) : Subalgebra ℝ (ℝ → ℝ) where
  carrier := {f | ContDiff ℝ ∞ f ∧ Function.Periodic f Lx}
  algebraMap_mem' r := by
    change ContDiff ℝ ∞ (fun _ : ℝ => r) ∧ Function.Periodic (fun _ : ℝ => r) Lx
    exact ⟨contDiff_const, fun _ => rfl⟩
  add_mem' := by
    intro f g hf hg
    refine ⟨hf.1.add hg.1, ?_⟩
    intro x
    change f (x + Lx) + g (x + Lx) = f x + g x
    rw [hf.2 x, hg.2 x]
  mul_mem' := by
    intro f g hf hg
    refine ⟨hf.1.mul hg.1, ?_⟩
    intro x
    change f (x + Lx) * g (x + Lx) = f x * g x
    rw [hf.2 x, hg.2 x]

abbrev PeriodicCoefficient (Lx : ℝ) := periodicCoefficientAlgebra Lx

theorem periodic_derivative_of_periodic (f : ℝ → ℝ) (Lx : ℝ)
    (hperiodic : Function.Periodic f Lx) : Function.Periodic (deriv f) Lx := by
  intro x
  have hshift : (fun y => f (y + Lx)) = f := funext hperiodic
  rw [← deriv_comp_add_const, hshift]

def PeriodicCoefficient.spatialDerivative {Lx : ℝ} (f : PeriodicCoefficient Lx) :
    PeriodicCoefficient Lx :=
  ⟨deriv (f : ℝ → ℝ), ⟨f.property.1.iterate_deriv 1,
    periodic_derivative_of_periodic _ Lx f.property.2⟩⟩

/-- Real differentiation is constructed, not supplied as a coefficient
derivation premise. Smoothness supplies the needed Leibniz hypotheses. -/
def periodicSpatialEvolution (Lx : ℝ) : AlgebraEvolution (PeriodicCoefficient Lx) where
  toLinearMap :=
    { toFun := PeriodicCoefficient.spatialDerivative
      map_add' := by
        intro f g
        apply Subtype.ext
        funext x
        exact ((f.property.1.differentiable (by simp) x).hasDerivAt.add
          (g.property.1.differentiable (by simp) x).hasDerivAt).deriv
      map_smul' := by
        intro r f
        apply Subtype.ext
        funext x
        change deriv (fun y => r * (f : ℝ → ℝ) y) x = r * deriv (f : ℝ → ℝ) x
        exact ((f.property.1.differentiable (by simp) x).hasDerivAt.const_mul r).deriv }
  leibniz := by
    intro f g
    apply Subtype.ext
    funext x
    exact ((f.property.1.differentiable (by simp) x).hasDerivAt.mul
      (g.property.1.differentiable (by simp) x).hasDerivAt).deriv

def SmoothPeriodicField.coefficient {M : ℕ} {Lx : ℝ}
    (f : SmoothPeriodicField M Lx) (j : Fin M) : PeriodicCoefficient Lx :=
  ⟨f.value j, f.smooth j, f.periodic j⟩

#print axioms periodicSpatialEvolution
end
end DLWLean
