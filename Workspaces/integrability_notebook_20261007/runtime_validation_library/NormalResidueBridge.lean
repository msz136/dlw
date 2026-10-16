import QuadraticResolvent
import ResidueIntegral

/-!
The highest quadratic normal-form trace is derived from structural PDO
residue rules. These are representation obligations about differential
order and the coefficient embedding, not a prescribed spectral Hessian.
-/

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

structure PeriodicNormalResidueModel (A : Type*) [Ring A] [Algebra ℝ A] (Lx : ℝ) where
  coefficient : PeriodicCoefficient Lx →ₐ[ℝ] A
  D : Aˣ
  residue : A →ₗ[ℝ] PeriodicCoefficient Lx
  commutation : ∀ a, (D : A) * coefficient a =
    coefficient a * (D : A) + coefficient ((periodicSpatialEvolution Lx).toLinearMap a)
  left_coefficient : ∀ a X, residue (coefficient a * X) = a * residue X
  differential_zero : ∀ n a, residue ((D : A) ^ n * coefficient a) = 0
  inverse_leading : ∀ a, residue ((↑D⁻¹ : A) * coefficient a) = a

def periodicSpatialIterate {Lx : ℝ} (n : ℕ) (a : PeriodicCoefficient Lx) :
    PeriodicCoefficient Lx :=
  ((periodicSpatialEvolution Lx).toLinearMap)^[n] a

theorem periodicSpatialIterate_eval {Lx : ℝ} (n : ℕ)
    (a : PeriodicCoefficient Lx) (x : ℝ) :
    (periodicSpatialIterate n a : ℝ → ℝ) x = iteratedDeriv n (a : ℝ → ℝ) x := by
  induction n generalizing x with
  | zero => rfl
  | succ n ih =>
    unfold periodicSpatialIterate
    rw [Function.iterate_succ_apply', iteratedDeriv_succ]
    change deriv (periodicSpatialIterate n a : ℝ → ℝ) x =
      deriv (iteratedDeriv n (a : ℝ → ℝ)) x
    have hfun : (periodicSpatialIterate n a : ℝ → ℝ) = iteratedDeriv n (a : ℝ → ℝ) :=
      funext ih
    rw [hfun]

namespace PeriodicNormalResidueModel

variable {A : Type*} [Ring A] [Algebra ℝ A] {Lx : ℝ}
    (model : PeriodicNormalResidueModel A Lx)

/-- The literal residue of D^n a D^-1 b, derived by repeated commutation
and differential-order vanishing. The full binomial expansion is not
needed: all its nonnegative-order terms have zero residue. -/
theorem residue_quadratic (n : ℕ) (a b : PeriodicCoefficient Lx) :
    model.residue ((model.D : A) ^ n *
      (model.coefficient a * (↑model.D⁻¹ : A) * model.coefficient b)) =
        periodicSpatialIterate n a * b := by
  induction n generalizing a with
  | zero =>
    simp only [pow_zero, one_mul, periodicSpatialIterate, Function.iterate_zero_apply]
    rw [mul_assoc, model.left_coefficient, model.inverse_leading]
  | succ n ih =>
    let ax := (periodicSpatialEvolution Lx).toLinearMap a
    have hcancel : (model.D : A) * (↑model.D⁻¹ : A) = 1 := Units.mul_inv model.D
    have hexpand : (model.D : A) ^ (n + 1) *
        (model.coefficient a * (↑model.D⁻¹ : A) * model.coefficient b) =
        (model.D : A) ^ n * model.coefficient (a * b) +
          (model.D : A) ^ n *
            (model.coefficient ax * (↑model.D⁻¹ : A) * model.coefficient b) := by
      calc
        _ = (model.D : A) ^ n *
            (((model.D : A) * model.coefficient a) *
              (↑model.D⁻¹ : A) * model.coefficient b) := by
          rw [pow_succ]
          noncomm_ring
        _ = (model.D : A) ^ n *
            (model.coefficient a *
                ((model.D : A) * (↑model.D⁻¹ : A)) * model.coefficient b +
              model.coefficient ax * (↑model.D⁻¹ : A) * model.coefficient b) := by
          rw [model.commutation]
          change _ = (model.D : A) ^ n *
            (model.coefficient a *
                ((model.D : A) * (↑model.D⁻¹ : A)) * model.coefficient b +
              model.coefficient ((periodicSpatialEvolution Lx).toLinearMap a) *
                (↑model.D⁻¹ : A) * model.coefficient b)
          noncomm_ring
        _ = _ := by rw [hcancel, mul_one, ← map_mul, mul_add]
    rw [hexpand, map_add, model.differential_zero, zero_add, ih]
    change periodicSpatialIterate n ((periodicSpatialEvolution Lx).toLinearMap a) * b =
      periodicSpatialIterate (n + 1) a * b
    rw [periodicSpatialIterate, periodicSpatialIterate, Function.iterate_succ_apply]

theorem residue_quadratic_integral (n : ℕ) (a b : PeriodicCoefficient Lx) :
    periodicCoefficientIntegral Lx
      (model.residue ((model.D : A) ^ n *
        (model.coefficient a * (↑model.D⁻¹ : A) * model.coefficient b))) =
      ∫ x in (0 : ℝ)..Lx, iteratedDeriv n (a : ℝ → ℝ) x * (b : ℝ → ℝ) x := by
  rw [model.residue_quadratic]
  change (∫ x in (0 : ℝ)..Lx,
      (periodicSpatialIterate n a : ℝ → ℝ) x * (b : ℝ → ℝ) x) = _
  simp_rw [periodicSpatialIterate_eval]

end PeriodicNormalResidueModel

/-- The actual balanced operator jet yields the top spectral coefficient
with no target normal-trace or target-Hessian premise. Its remaining
model fields are listed in PeriodicNormalResidueModel. -/
theorem BalancedResolventStart.odd_spectral_second_from_normal_residue_model
    {A B : Type*} [Ring A] [Algebra ℝ A] [Ring B] [Algebra ℝ B]
    {j : AlgebraJet2 A B} (s : BalancedResolventStart j) (Lx : ℝ)
    (model : PeriodicNormalResidueModel B Lx)
    (hcyclic : ∀ X Y, periodicCoefficientIntegral Lx (model.residue (X * Y)) =
      periodicCoefficientIntegral Lx (model.residue (Y * X)))
    (g : PeriodicCoefficient Lx) (hbase : s.base = model.D)
    (hf : s.f = model.coefficient g) (k : ℕ) :
    spectralSecondCoefficient (periodicResidueTrace Lx model.residue hcyclic) j
      (zeroEtaNormalized s.latticeLength 0 s.sumUnit) (2 * k + 1) =
      (2 / s.latticeLength) * (-1 : ℝ) ^ (k + 1) *
        ∫ x in (0 : ℝ)..Lx, (iteratedDeriv k (g : ℝ → ℝ) x) ^ 2 := by
  apply s.odd_spectral_second_of_normal_form
    (periodicResidueTrace Lx model.residue hcyclic) Lx (g : ℝ → ℝ)
    g.property.1 g.property.2 k
  rw [hbase, hf]
  change periodicCoefficientIntegral Lx
    (model.residue ((model.D : B) ^ (2 * k) *
      (model.coefficient g * (↑model.D⁻¹ : B) * model.coefficient g))) = _
  rw [model.residue_quadratic_integral]
  congr 1
  funext x
  ring

#print axioms PeriodicNormalResidueModel.residue_quadratic
#print axioms BalancedResolventStart.odd_spectral_second_from_normal_residue_model

end
end DLWLean
