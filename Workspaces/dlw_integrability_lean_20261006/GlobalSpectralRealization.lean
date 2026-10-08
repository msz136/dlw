import GlobalRealization
import NormalInverseRecurrence

namespace DLWLean.GlobalPDO
noncomputable section
open scoped BigOperators ContDiff

variable {par : FieldParameters} {A : Type*} [Ring A] [Algebra ℝ A]
    {z : ClosedPeriodicPair par}
    {model : NormalPDOModel (PeriodicCoefficient par.Lx) A}

/-- The only additional datum is the formal inverse of M-1. Its
coefficients and every trace-power density are proved below. -/
structure NormalizedRealization (factors : FactorRealization par z model) where
  difference : Aˣ
  difference_eq : (difference : A) = factors.monodromyDifference par.M

namespace NormalizedRealization
variable {factors : FactorRealization par z model}
    (realization : NormalizedRealization factors)

theorem difference_bound : PDOOrderBound model.coefficients (realization.difference : A) (-1) := by
  rw [realization.difference_eq]
  exact factors.monodromyDifference_bound par.M

theorem difference_coefficient (k : ℕ) :
    model.coefficientBelow (realization.difference : A) (-1) k =
      evaluation par z (monodromyCoefficient par k) := by
  rw [realization.difference_eq]
  exact factors.monodromyDifference_coefficient par.M k

theorem difference_leading : model.coefficients (realization.difference : A) (-1) =
    algebraMap ℝ (PeriodicCoefficient par.Lx) (-par.G) := by
  have h := realization.difference_coefficient 0
  simpa only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero,
    monodromyCoefficient_leading, evaluation_C] using h

theorem inverse_bound : PDOOrderBound model.coefficients (↑realization.difference⁻¹ : A) 1 :=
  model.constantLeading_inverse_bound realization.difference (-par.G)
    (neg_ne_zero.mpr par.G_ne_zero) realization.difference_bound realization.difference_leading

theorem inverse_coefficient_realization (k : ℕ) :
    model.coefficientBelow (↑realization.difference⁻¹ : A) 1 k =
      evaluation par z (inverseCoefficient par k) := by
  classical
  induction k using Nat.strong_induction_on with
  | h k ih =>
    cases k with
    | zero =>
      rw [inverseCoefficient, evaluation_C]
      exact model.constantLeading_inverse_zero realization.difference (-par.G)
        (neg_ne_zero.mpr par.G_ne_zero) realization.difference_bound realization.difference_leading
    | succ n =>
      rw [model.constantLeading_inverse_succ realization.difference (-par.G)
        (neg_ne_zero.mpr par.G_ne_zero) realization.difference_bound realization.difference_leading]
      rw [inverseCoefficient, map_mul, evaluation_C]
      congr 1
      unfold normalInverseRemainder
      rw [map_sum]
      apply Finset.sum_congr rfl
      intro t _
      rw [map_sum]
      apply Finset.sum_congr rfl
      intro r _
      split_ifs
      · rw [map_mul, map_mul, evaluation_C, ← realization.difference_coefficient,
          evaluation_iterate, ← factors.spatial, ← ih t.val t.isLt]
      · rw [map_zero]

def L : A := (-par.G) • (↑realization.difference⁻¹ : A) +
  (par.B - par.G / 2) • (1 : A)

theorem L_eq_normalized_monodromy : realization.L =
    (-par.G) • (↑realization.difference⁻¹ : A) + (par.B - par.G / 2) • (1 : A) := rfl

theorem L_bound : PDOOrderBound model.coefficients realization.L 1 := by
  apply model.add_bound (model.smul_bound _ realization.inverse_bound)
  have hone : PDOOrderBound model.coefficients (1 : A) 0 := by
    simpa only [map_one] using model.embedding_bound (1 : PeriodicCoefficient par.Lx)
  exact model.bound_mono (model.smul_bound _ hone) (by norm_num)

theorem L_coefficient_realization (k : ℕ) :
    model.coefficientBelow realization.L 1 k =
      evaluation par z (normalizedCoefficient par k) := by
  simp only [L, NormalPDOModel.coefficientBelow, map_add, map_smul, Pi.add_apply,
    Pi.smul_apply, model.coeff_one]
  simp only [Algebra.smul_def, normalizedCoefficient, map_add, map_mul, evaluation_C]
  have hk : (1 : ℤ) - (k : ℤ) = 0 ↔ k = 1 := by omega
  simp only [hk]
  have hi := realization.inverse_coefficient_realization k
  unfold NormalPDOModel.coefficientBelow at hi
  rw [hi]
  split_ifs <;> simp

theorem power_bound (n : ℕ) :
    PDOOrderBound model.coefficients (realization.L ^ n) (n : ℤ) := by
  induction n with
  | zero =>
    simpa only [pow_zero, Nat.cast_zero, map_one] using model.embedding_bound (1 : PeriodicCoefficient par.Lx)
  | succ n ih =>
    simpa only [pow_succ, Nat.cast_add, Nat.cast_one] using
      model.product_bound (realization.L ^ n) realization.L (n : ℤ) 1 ih realization.L_bound

theorem power_coefficient_realization (n k : ℕ) :
    model.coefficientBelow (realization.L ^ n) (n : ℤ) k =
      evaluation par z (powerCoefficient par n k) := by
  induction n generalizing k with
  | zero =>
    simp only [pow_zero, NormalPDOModel.coefficientBelow, Nat.cast_zero, zero_sub,
      model.coeff_one, powerCoefficient]
    have hk : -(k : ℤ) = 0 ↔ k = 0 := by omega
    simp only [hk]
    split_ifs <;> simp
  | succ n ih =>
    rw [pow_succ]
    have hp := model.product_coefficient (realization.L ^ n) realization.L (n : ℤ) 1
      (realization.power_bound n) realization.L_bound k
    have hexp : ((n + 1 : ℕ) : ℤ) - (k : ℤ) = (n : ℤ) + 1 - (k : ℤ) := by omega
    change model.coefficients (realization.L ^ n * realization.L) (((n + 1 : ℕ) : ℤ) - (k : ℤ)) = _
    rw [hexp, hp]
    have hpower : (fun r : ℕ => model.coefficients (realization.L ^ n) ((n : ℤ) - (r : ℤ))) =
        (fun r => evaluation par z (powerCoefficient par n r)) := by
      funext r
      exact ih r
    have hL : (fun r : ℕ => model.coefficients realization.L (1 - (r : ℤ))) =
        (fun r => evaluation par z (normalizedCoefficient par r)) := by
      funext r
      exact realization.L_coefficient_realization r
    rw [hpower, hL, ← factors.normalProduct_compatible]
    rfl

/-- The actual coefficient of D^-1 in L^n is the constructed globally
restricted finite differential polynomial, for every natural n. -/
theorem residue_realization (n : ℕ) :
    model.coefficients (realization.L ^ n) (-1) =
      evaluation par z (residuePolynomial par n) := by
  have h := realization.power_coefficient_realization n (n + 1)
  have hexp : (n : ℤ) - ((n + 1 : ℕ) : ℤ) = -1 := by omega
  simpa only [NormalPDOModel.coefficientBelow, hexp, residuePolynomial] using h

/-- A periodic residue trace is identified with its defining actual
integral. No polynomial density or spectral-charge equality is a premise. -/
theorem constructedCharge_eq_spectralInvariant (tr : CyclicTrace A)
    (trace_eq : ∀ X, tr.toLinearMap X =
      periodicCoefficientIntegral par.Lx (model.coefficients X (-1))) (n : ℕ) :
    constructedCharge par n z = spectralInvariant tr realization.L n := by
  rw [spectralInvariant, trace_eq, realization.residue_realization]
  change periodicCoefficientIntegral par.Lx
    (fieldDifferentialPolynomial par (periodicDensityPolynomial par n) z) = _
  rw [periodicDensityPolynomial_eval, spectralDensityPolynomial, map_mul, evaluation_C]
  change periodicCoefficientIntegral par.Lx
    ((n : ℝ)⁻¹ • evaluation par z (residuePolynomial par n)) = _
  exact map_smul (periodicCoefficientIntegral par.Lx) (n : ℝ)⁻¹ _

end NormalizedRealization

#print axioms NormalizedRealization.inverse_coefficient_realization
#print axioms NormalizedRealization.residue_realization
#print axioms NormalizedRealization.constructedCharge_eq_spectralInvariant
end
end DLWLean.GlobalPDO
