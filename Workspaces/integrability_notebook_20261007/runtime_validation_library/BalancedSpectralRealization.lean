import BalancedRealization
import NormalInverseRecurrence

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    {model : NormalPDOModel R A} {e : DifferentialEvaluation M R model.d}

namespace FactorRealization
variable (factors : FactorRealization model e)

def sites (n : ℕ) : A :=
  if hn : n < M then (-2 : ℝ) • (↑(factors.denominator ⟨n, hn⟩)⁻¹ : A) else 0

theorem sites_bound (n : ℕ) : PDOOrderBound model.coefficients (factors.sites n) (-1) := by
  unfold sites
  split_ifs
  · exact model.smul_bound _ (factors.inverse_bound _)
  · intro exponent _
    simp

theorem sites_coefficient (n k : ℕ) :
    model.coefficientBelow (factors.sites n) (-1) k = e.evaluation (balancedSites M n k) := by
  unfold sites balancedSites
  split_ifs with hn
  · change model.coefficients ((-2 : ℝ) • (↑(factors.denominator ⟨n, hn⟩)⁻¹ : A))
      (-1 - (k : ℤ)) = e.evaluation (MvPolynomial.C (-2) * resolventCoefficient M ⟨n, hn⟩ k)
    rw [map_smul, map_mul, e.C_eval]
    simp only [Pi.smul_apply]
    rw [show model.coefficients (↑(factors.denominator ⟨n, hn⟩)⁻¹ : A)
        (-1 - (k : ℤ)) = e.evaluation (resolventCoefficient M ⟨n, hn⟩ k) from
      factors.inverse_coefficient_realization ⟨n, hn⟩ k]
    exact Algebra.smul_def _ _
  · simp [NormalPDOModel.coefficientBelow]

def regularQuotient (n : ℕ) : A := affineParameterQuotient factors.sites
  (model.coefficient (e.evaluation (MvPolynomial.X .eta))) n

theorem regularQuotient_bound (n : ℕ) :
    PDOOrderBound model.coefficients (factors.regularQuotient n) (-1) := by
  induction n with
  | zero => intro exponent _; simp [regularQuotient, affineParameterQuotient]
  | succ n ih =>
    change PDOOrderBound model.coefficients
      (factors.sites n + factors.regularQuotient n +
        model.coefficient (e.evaluation (MvPolynomial.X .eta)) *
          factors.sites n * factors.regularQuotient n) (-1)
    apply model.add_bound (model.add_bound (factors.sites_bound n) ih)
    apply model.bound_mono
    · exact model.product_bound _ _ (-1) (-1)
        (by simpa using model.product_bound _ _ 0 (-1) (model.embedding_bound _) (factors.sites_bound n)) ih
    · norm_num

theorem regularQuotient_coefficient (n k : ℕ) :
    model.coefficientBelow (factors.regularQuotient n) (-1) k =
      e.evaluation (regularQuotientCoefficient M (balancedSites M) n k) := by
  induction n generalizing k with
  | zero => simp [regularQuotient, affineParameterQuotient,
      regularQuotientCoefficient, NormalPDOModel.coefficientBelow]
  | succ n ih =>
    change model.coefficients
      (factors.sites n + factors.regularQuotient n +
        model.coefficient (e.evaluation (MvPolynomial.X .eta)) *
          factors.sites n * factors.regularQuotient n) (-1 - (k : ℤ)) = _
    rw [map_add, map_add]
    simp only [Pi.add_apply]
    rw [mul_assoc, model.scalar_left_coefficient]
    cases k with
    | zero =>
      have hp := model.product_bound (factors.sites n) (factors.regularQuotient n)
        (-1) (-1) (factors.sites_bound n) (factors.regularQuotient_bound n)
      have hz : model.coefficients (factors.sites n * factors.regularQuotient n) (-1) = 0 :=
        hp (-1) (by norm_num)
      simp only [Nat.cast_zero, sub_zero, hz, mul_zero, add_zero, regularQuotientCoefficient, map_add]
      rw [show model.coefficients (factors.sites n) (-1) =
        e.evaluation (balancedSites M n 0) from factors.sites_coefficient n 0,
        show model.coefficients (factors.regularQuotient n) (-1) =
        e.evaluation (regularQuotientCoefficient M (balancedSites M) n 0) from ih 0]
    | succ k =>
      have hexp : -1 - ((k + 1 : ℕ) : ℤ) = (-1 : ℤ) + (-1) - (k : ℤ) := by omega
      rw [regularQuotientCoefficient, map_add, map_add,
        map_mul e.evaluation, e.normalProduct_eval]
      have hsites : (fun r : ℕ => model.coefficients (factors.sites n) (-1 - (r : ℤ))) =
          (fun r => e.evaluation (balancedSites M n r)) := by
        funext r
        exact factors.sites_coefficient n r
      have hquot : (fun r : ℕ => model.coefficients (factors.regularQuotient n) (-1 - (r : ℤ))) =
          (fun r => e.evaluation (regularQuotientCoefficient M (balancedSites M) n r)) := by
        funext r
        exact ih r
      rw [hexp, model.product_coefficient _ _ (-1) (-1)
        (factors.sites_bound n) (factors.regularQuotient_bound n) k, hsites, hquot]
      rw [← hexp]
      rw [show model.coefficients (factors.sites n) (-1 - ((k + 1 : ℕ) : ℤ)) =
        e.evaluation (balancedSites M n (k + 1)) from factors.sites_coefficient n (k + 1),
        show model.coefficients (factors.regularQuotient n) (-1 - ((k + 1 : ℕ) : ℤ)) =
        e.evaluation (regularQuotientCoefficient M (balancedSites M) n (k + 1)) from ih (k + 1)]

end FactorRealization

structure NormalizedRealization (factors : FactorRealization model e) where
  quotient : Aˣ
  quotient_eq : (quotient : A) = factors.regularQuotient M

namespace NormalizedRealization
variable {factors : FactorRealization model e} (realization : NormalizedRealization factors)

theorem quotient_bound : PDOOrderBound model.coefficients (realization.quotient : A) (-1) := by
  rw [realization.quotient_eq]
  exact factors.regularQuotient_bound M

theorem quotient_coefficient (k : ℕ) :
    model.coefficientBelow (realization.quotient : A) (-1) k =
      e.evaluation (balancedQuotientCoefficient M k) := by
  rw [realization.quotient_eq]
  exact factors.regularQuotient_coefficient M k

theorem quotient_leading : model.coefficients (realization.quotient : A) (-1) =
    algebraMap ℝ R (-2 * (M : ℝ)) := by
  have h := realization.quotient_coefficient 0
  simpa only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero,
    balancedQuotientCoefficient_leading, e.C_eval] using h

theorem inverse_bound (hM : M ≠ 0) :
    PDOOrderBound model.coefficients (↑realization.quotient⁻¹ : A) 1 :=
  model.constantLeading_inverse_bound realization.quotient (-2 * (M : ℝ))
    (mul_ne_zero (by norm_num) (Nat.cast_ne_zero.mpr hM))
    realization.quotient_bound realization.quotient_leading

theorem inverse_coefficient_realization (hM : M ≠ 0) (k : ℕ) :
    model.coefficientBelow (↑realization.quotient⁻¹ : A) 1 k =
      e.evaluation (inverseCoefficient M (balancedQuotientCoefficient M) (-2 * (M : ℝ))⁻¹ k) := by
  classical
  have hleadne : (-2 * (M : ℝ)) ≠ 0 :=
    mul_ne_zero (by norm_num) (Nat.cast_ne_zero.mpr hM)
  induction k using Nat.strong_induction_on with
  | h k ih =>
    cases k with
    | zero =>
      rw [inverseCoefficient, e.C_eval]
      exact model.constantLeading_inverse_zero realization.quotient _ hleadne
        realization.quotient_bound realization.quotient_leading
    | succ n =>
      rw [model.constantLeading_inverse_succ realization.quotient _ hleadne
        realization.quotient_bound realization.quotient_leading]
      rw [inverseCoefficient, map_mul, e.C_eval]
      congr 1
      unfold normalInverseRemainder
      rw [map_sum]
      apply Finset.sum_congr rfl
      intro t _
      rw [map_sum]
      apply Finset.sum_congr rfl
      intro r _
      split_ifs
      · rw [map_mul, map_mul, e.C_eval, ← realization.quotient_coefficient,
          e.spatialIterate_eval, ← ih t.val t.isLt]
      · rw [map_zero]

def L : A := (-2 * (M : ℝ)) • (↑realization.quotient⁻¹ : A) +
  model.coefficient (e.evaluation (MvPolynomial.X .b)) -
    (M : ℝ) • model.coefficient (e.evaluation (MvPolynomial.X .eta))

theorem L_bound (hM : M ≠ 0) : PDOOrderBound model.coefficients realization.L 1 := by
  exact model.sub_bound
    (model.add_bound (model.smul_bound _ (realization.inverse_bound hM))
      (model.bound_mono (model.embedding_bound _) (by norm_num)))
    (model.bound_mono (model.smul_bound _ (model.embedding_bound _)) (by norm_num))

theorem L_coefficient_realization (hM : M ≠ 0) (k : ℕ) :
    model.coefficientBelow realization.L 1 k = e.evaluation (balancedNormalizedCoefficient M k) := by
  simp only [L, NormalPDOModel.coefficientBelow, map_sub, map_add, map_smul,
    Pi.sub_apply, Pi.add_apply, Pi.smul_apply, model.coefficient_embedding]
  simp only [balancedNormalizedCoefficient, normalizedCoefficient, map_add, map_mul, e.C_eval]
  have hk : (1 : ℤ) - (k : ℤ) = 0 ↔ k = 1 := by omega
  simp only [hk]
  have hi := realization.inverse_coefficient_realization hM k
  unfold NormalPDOModel.coefficientBelow at hi
  rw [hi]
  split_ifs <;> simp [Algebra.smul_def, map_sub, map_mul, e.C_eval] <;> ring

theorem power_bound (hM : M ≠ 0) (n : ℕ) :
    PDOOrderBound model.coefficients (realization.L ^ n) (n : ℤ) := by
  induction n with
  | zero =>
    simpa only [pow_zero, Nat.cast_zero, map_one] using model.embedding_bound (1 : R)
  | succ n ih =>
    simpa only [pow_succ, Nat.cast_add, Nat.cast_one] using
      model.product_bound _ _ (n : ℤ) 1 ih (realization.L_bound hM)

theorem power_coefficient_realization (hM : M ≠ 0) (n k : ℕ) :
    model.coefficientBelow (realization.L ^ n) (n : ℤ) k =
      e.evaluation (powerCoefficient M (balancedNormalizedCoefficient M) n k) := by
  induction n generalizing k with
  | zero =>
    simp only [pow_zero, NormalPDOModel.coefficientBelow, Nat.cast_zero, zero_sub,
      model.coeff_one, powerCoefficient]
    have hk : -(k : ℤ) = 0 ↔ k = 0 := by omega
    simp only [hk]
    split_ifs <;> simp
  | succ n ih =>
    rw [pow_succ]
    have hexp : ((n + 1 : ℕ) : ℤ) - (k : ℤ) = (n : ℤ) + 1 - (k : ℤ) := by omega
    change model.coefficients (realization.L ^ n * realization.L) (((n + 1 : ℕ) : ℤ) - (k : ℤ)) = _
    rw [hexp, model.product_coefficient _ _ (n : ℤ) 1
      (realization.power_bound hM n) (realization.L_bound hM) k]
    have hpower : (fun r : ℕ => model.coefficients (realization.L ^ n) ((n : ℤ) - (r : ℤ))) =
        (fun r => e.evaluation (powerCoefficient M (balancedNormalizedCoefficient M) n r)) := by
      funext r
      exact ih r
    have hL : (fun r : ℕ => model.coefficients realization.L (1 - (r : ℤ))) =
        (fun r => e.evaluation (balancedNormalizedCoefficient M r)) := by
      funext r
      exact realization.L_coefficient_realization hM r
    rw [hpower, hL, ← e.normalProduct_eval]
    rfl

theorem residue_realization (hM : M ≠ 0) (n : ℕ) :
    model.coefficients (realization.L ^ n) (-1) = e.evaluation (balancedResiduePolynomial M n) := by
  have h := realization.power_coefficient_realization hM n (n + 1)
  have hexp : (n : ℤ) - ((n + 1 : ℕ) : ℤ) = -1 := by omega
  simpa only [NormalPDOModel.coefficientBelow, hexp, balancedResiduePolynomial] using h

end NormalizedRealization

#print axioms FactorRealization.regularQuotient_coefficient
#print axioms NormalizedRealization.residue_realization
end
end DLWLean.BalancedPDO
