import ActualTraceDerivative
import Mathlib.Analysis.Calculus.FDeriv.Symmetric

namespace DLWLean
noncomputable section
open scoped ContDiff

theorem fderiv_derivative_apply_const (F : ℝ × ℝ → ℝ) (hF : ContDiff ℝ ∞ F)
    (tx v w : ℝ × ℝ) :
    fderiv ℝ (fun y => fderiv ℝ F y w) tx v = fderiv ℝ (fderiv ℝ F) tx v w := by
  have hdf : DifferentiableAt ℝ (fderiv ℝ F) tx :=
    ((contDiff_infty_iff_fderiv.mp hF).2.differentiable (by simp)) tx
  rw [fderiv_clm_apply hdf (differentiableAt_const w)]
  simp

/-- Schwarz commutation for the actual two scalar partial derivatives. -/
theorem spacetimeTimeSpace_commute (F : ℝ × ℝ → ℝ) (hF : ContDiff ℝ ∞ F) (tx : ℝ × ℝ) :
    spacetimeTimeDerivative (spacetimeSpaceDerivative F) tx =
      spacetimeSpaceDerivative (spacetimeTimeDerivative F) tx := by
  have hs : spacetimeSpaceDerivative F = fun y => fderiv ℝ F y (0, 1) :=
    funext (spacetimeSpaceDerivative_eq_fderiv F hF)
  have ht : spacetimeTimeDerivative F = fun y => fderiv ℝ F y (1, 0) :=
    funext (spacetimeTimeDerivative_eq_fderiv F hF)
  rw [spacetimeTimeDerivative_eq_fderiv _ (spacetimeSpaceDerivative_smooth F hF),
    spacetimeSpaceDerivative_eq_fderiv _ (spacetimeTimeDerivative_smooth F hF), hs, ht,
    fderiv_derivative_apply_const F hF, fderiv_derivative_apply_const F hF]
  exact hF.contDiffAt.isSymmSndFDerivAt (by simp) (1, 0) (0, 1)

theorem periodicSpacetimeTimeSpace_commute {Lx : ℝ} (f : PeriodicSpacetimeCoefficient Lx) :
    (periodicSpacetimeTimeEvolution Lx).toLinearMap
      ((periodicSpacetimeSpaceEvolution Lx).toLinearMap f) =
    (periodicSpacetimeSpaceEvolution Lx).toLinearMap
      ((periodicSpacetimeTimeEvolution Lx).toLinearMap f) := by
  apply Subtype.ext
  funext tx
  exact spacetimeTimeSpace_commute _ f.property.1 tx

theorem periodicSpacetimeTimeSpace_iterate {Lx : ℝ} (f : PeriodicSpacetimeCoefficient Lx) (k : ℕ) :
    (periodicSpacetimeTimeEvolution Lx).toLinearMap
      (((periodicSpacetimeSpaceEvolution Lx).toLinearMap)^[k] f) =
    ((periodicSpacetimeSpaceEvolution Lx).toLinearMap)^[k]
      ((periodicSpacetimeTimeEvolution Lx).toLinearMap f) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', periodicSpacetimeTimeSpace_commute, ih,
      Function.iterate_succ_apply']

#print axioms periodicSpacetimeTimeSpace_commute
end
end DLWLean
