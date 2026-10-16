import GlobalCoefficientRecurrence

/-!
Realization of the finite global differential-polynomial recurrences in
a normal PDO model. The model supplies normal coefficients, their
multiplication law and formal inverses; no residue identity or field
polynomiality is assumed.
-/
namespace DLWLean.GlobalPDO
noncomputable section
open scoped BigOperators ContDiff

variable {par : FieldParameters} {A : Type*} [Ring A] [Algebra ℝ A]

structure FactorRealization (par : FieldParameters) (z : ClosedPeriodicPair par)
    (model : NormalPDOModel (PeriodicCoefficient par.Lx) A) where
  spatial : model.d = periodicSpatialEvolution par.Lx
  denominator : Fin par.M → Aˣ
  denominator_eq : ∀ j, (denominator j : A) = (model.D : A) -
    model.coefficient (evaluation par z (beta par j))

namespace FactorRealization
variable {z : ClosedPeriodicPair par}
    {model : NormalPDOModel (PeriodicCoefficient par.Lx) A}
    (factors : FactorRealization par z model)
include factors

theorem derivative_compatible (p : Poly par) :
    evaluation par z (spatialDerivative par p) = model.d.toLinearMap (evaluation par z p) := by
  rw [factors.spatial]
  exact evaluation_derivative par z p

theorem normalProduct_compatible (leftOrder : ℤ) (a b : ℕ → Poly par) (k : ℕ) :
    evaluation par z (normalProduct par leftOrder a b k) =
      normalProductCoefficient model.d leftOrder
        (fun r => evaluation par z (a r)) (fun r => evaluation par z (b r)) k := by
  rw [factors.spatial]
  exact normalProduct_eval par z leftOrder a b k

theorem denominator_bound (j : Fin par.M) :
    PDOOrderBound model.coefficients (factors.denominator j : A) 1 := by
  rw [factors.denominator_eq]
  apply model.sub_bound
  · simpa using model.D_power_bound 1
  · exact model.bound_mono (model.embedding_bound _) (by norm_num)

theorem denominator_coefficient (j : Fin par.M) (k : ℕ) :
    model.coefficientBelow (factors.denominator j : A) 1 k =
      if k = 0 then 1 else if k = 1 then -evaluation par z (beta par j) else 0 := by
  unfold NormalPDOModel.coefficientBelow
  rw [factors.denominator_eq, map_sub]
  simp only [Pi.sub_apply]
  have hD : model.coefficients (model.D : A) (1 - (k : ℤ)) =
      if 1 - (k : ℤ) = 1 then 1 else 0 := by
    simpa using model.coefficient_D_power 1 (1 - (k : ℤ))
  rw [hD, model.coefficient_embedding]
  have hk0 : 1 - (k : ℤ) = 1 ↔ k = 0 := by omega
  have hk1 : 1 - (k : ℤ) = 0 ↔ k = 1 := by omega
  simp only [hk0, hk1]
  split_ifs <;> simp_all

theorem inverse_bound (j : Fin par.M) :
    PDOOrderBound model.coefficients (↑(factors.denominator j)⁻¹ : A) (-1) := by
  apply model.inverse_bound (factors.denominator j) 1 (factors.denominator_bound j)
  have h := factors.denominator_coefficient j 0
  simp only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero, if_pos rfl] at h
  rw [h]
  exact isUnit_one

def inverseBelow (j : Fin par.M) (k : ℕ) : PeriodicCoefficient par.Lx :=
  model.coefficientBelow (↑(factors.denominator j)⁻¹ : A) (-1) k

theorem inverseBelow_zero (j : Fin par.M) : factors.inverseBelow j 0 = 1 := by
  have h := model.product_leading (factors.denominator j : A)
    (↑(factors.denominator j)⁻¹ : A) 1 (-1)
    (factors.denominator_bound j) (factors.inverse_bound j)
  rw [Units.mul_inv, model.coeff_one] at h
  have hlead := factors.denominator_coefficient j 0
  simp only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero, if_pos rfl] at hlead
  rw [hlead] at h
  simpa [inverseBelow, NormalPDOModel.coefficientBelow] using h.symm

theorem inverseBelow_succ (j : Fin par.M) (n : ℕ) :
    factors.inverseBelow j (n + 1) =
      evaluation par z (beta par j) * factors.inverseBelow j n -
        model.d.toLinearMap (factors.inverseBelow j n) := by
  have h := model.product_coefficient (factors.denominator j : A)
    (↑(factors.denominator j)⁻¹ : A) 1 (-1)
    (factors.denominator_bound j) (factors.inverse_bound j) (n + 1)
  rw [Units.mul_inv, model.coeff_one] at h
  have hseq : (fun r : ℕ => model.coefficients (factors.denominator j : A) (1 - (r : ℤ))) =
      (fun r => if r = 0 then 1 else if r = 1 then -evaluation par z (beta par j) else 0) := by
    funext r
    exact factors.denominator_coefficient j r
  rw [hseq, normalProductCoefficient_first_order] at h
  have hnonzero : 1 + (-1 : ℤ) - ((n + 1 : ℕ) : ℤ) ≠ 0 := by omega
  simp only [hnonzero, if_false] at h
  change 0 = factors.inverseBelow j (n + 1) +
    model.d.toLinearMap (factors.inverseBelow j n) -
      evaluation par z (beta par j) * factors.inverseBelow j n at h
  linear_combination -h

theorem inverse_coefficient_realization (j : Fin par.M) (k : ℕ) :
    factors.inverseBelow j k = evaluation par z (resolventCoefficient par j k) := by
  induction k with
  | zero => simpa [resolventCoefficient] using factors.inverseBelow_zero j
  | succ k ih =>
    rw [factors.inverseBelow_succ, resolventCoefficient, map_sub, map_mul,
      factors.derivative_compatible, ih]

/-- T_j=1+site_j=1-(D-beta_j)^-1 g_j. -/
def site (j : Fin par.M) : A :=
  -(↑(factors.denominator j)⁻¹ : A) * model.coefficient (evaluation par z (g par j))

theorem site_bound (j : Fin par.M) : PDOOrderBound model.coefficients (factors.site j) (-1) := by
  have hb : PDOOrderBound model.coefficients (-(↑(factors.denominator j)⁻¹ : A)) (-1) := by
    intro exponent he
    simp only [map_neg, Pi.neg_apply, factors.inverse_bound j exponent he, neg_zero]
  simpa only [site, add_zero] using model.product_bound
    (-(↑(factors.denominator j)⁻¹ : A))
    (model.coefficient (evaluation par z (g par j))) (-1) 0 hb (model.embedding_bound _)

theorem site_coefficient_realization (j : Fin par.M) (k : ℕ) :
    model.coefficientBelow (factors.site j) (-1) k =
      evaluation par z (siteCoefficient par j k) := by
  change model.coefficients (-(↑(factors.denominator j)⁻¹ : A) *
    model.coefficient (evaluation par z (g par j))) (-1 - (k : ℤ)) = _
  rw [neg_mul, map_neg]
  simp only [Pi.neg_apply]
  have hprod := model.product_coefficient (↑(factors.denominator j)⁻¹ : A)
    (model.coefficient (evaluation par z (g par j))) (-1) 0
      (factors.inverse_bound j) (model.embedding_bound _) k
  simp only [add_zero] at hprod
  rw [hprod]
  have hleft : (fun r : ℕ => model.coefficients (↑(factors.denominator j)⁻¹ : A) (-1 - (r : ℤ))) =
      (fun r => evaluation par z (resolventCoefficient par j r)) := by
    funext r
    exact factors.inverse_coefficient_realization j r
  have hright : (fun r : ℕ => model.coefficients (model.coefficient (evaluation par z (g par j)))
      (0 - (r : ℤ))) = (fun r => evaluation par z (if r = 0 then g par j else 0)) := by
    funext r
    rw [model.coefficient_embedding]
    split_ifs <;> simp_all
  rw [hleft, hright, siteCoefficient, map_neg, factors.normalProduct_compatible]

def siteNat (j : ℕ) : A := if hj : j < par.M then factors.site ⟨j, hj⟩ else 0

theorem siteNat_bound (j : ℕ) : PDOOrderBound model.coefficients (factors.siteNat j) (-1) := by
  unfold siteNat
  split_ifs
  · exact factors.site_bound _
  · intro exponent _
    simp

theorem siteNat_coefficient (j k : ℕ) :
    model.coefficientBelow (factors.siteNat j) (-1) k = evaluation par z (sites par j k) := by
  unfold siteNat sites
  split_ifs
  · exact factors.site_coefficient_realization _ k
  · simp [NormalPDOModel.coefficientBelow]

def monodromyDifference (factors : FactorRealization par z model) : ℕ → A
  | 0 => 0
  | n + 1 => factors.siteNat n + monodromyDifference factors n +
      factors.siteNat n * monodromyDifference factors n

theorem monodromyDifference_bound (n : ℕ) :
    PDOOrderBound model.coefficients (factors.monodromyDifference n) (-1) := by
  induction n with
  | zero => intro exponent _; simp [monodromyDifference]
  | succ n ih =>
    rw [monodromyDifference]
    apply model.add_bound (model.add_bound (factors.siteNat_bound n) ih)
    exact model.bound_mono
      (model.product_bound _ _ (-1) (-1) (factors.siteNat_bound n) ih) (by norm_num)

theorem monodromyDifference_coefficient (n k : ℕ) :
    model.coefficientBelow (factors.monodromyDifference n) (-1) k =
      evaluation par z (monodromyDifferenceCoefficient par n k) := by
  induction n generalizing k with
  | zero => simp [monodromyDifference, monodromyDifferenceCoefficient,
      NormalPDOModel.coefficientBelow]
  | succ n ih =>
    cases k with
    | zero =>
      have hp := model.product_bound (factors.siteNat n) (factors.monodromyDifference n)
        (-1) (-1) (factors.siteNat_bound n) (factors.monodromyDifference_bound n)
      have hzero := hp (-1) (by norm_num)
      simp only [monodromyDifference, NormalPDOModel.coefficientBelow, Nat.cast_zero,
        sub_zero, map_add, Pi.add_apply, hzero, add_zero, monodromyDifferenceCoefficient]
      change model.coefficientBelow (factors.siteNat n) (-1) 0 +
        model.coefficientBelow (factors.monodromyDifference n) (-1) 0 = _
      rw [factors.siteNat_coefficient, ih]
    | succ k =>
      have hp := model.product_coefficient (factors.siteNat n) (factors.monodromyDifference n)
        (-1) (-1) (factors.siteNat_bound n) (factors.monodromyDifference_bound n) k
      have hexp : (-1 : ℤ) - ((k + 1 : ℕ) : ℤ) = -1 + -1 - (k : ℤ) := by omega
      change model.coefficients (factors.siteNat n + factors.monodromyDifference n +
        factors.siteNat n * factors.monodromyDifference n) (-1 - ((k + 1 : ℕ) : ℤ)) = _
      simp only [map_add, Pi.add_apply]
      rw [hexp, hp]
      have hs : (fun r : ℕ => model.coefficients (factors.siteNat n) (-1 - (r : ℤ))) =
          (fun r => evaluation par z (sites par n r)) := by
        funext r
        exact factors.siteNat_coefficient n r
      have hm : (fun r : ℕ => model.coefficients (factors.monodromyDifference n) (-1 - (r : ℤ))) =
          (fun r => evaluation par z (monodromyDifferenceCoefficient par n r)) := by
        funext r
        exact ih r
      rw [hs, hm, ← factors.normalProduct_compatible]
      rw [← hexp]
      change model.coefficientBelow (factors.siteNat n) (-1) (k + 1) +
        model.coefficientBelow (factors.monodromyDifference n) (-1) (k + 1) + _ = _
      rw [factors.siteNat_coefficient, ih, monodromyDifferenceCoefficient, map_add, map_add]

def monodromy (factors : FactorRealization par z model) : ℕ → A
  | 0 => 1
  | n + 1 => (1 + factors.siteNat n) * monodromy factors n

theorem monodromyDifference_eq (n : ℕ) :
    factors.monodromyDifference n = factors.monodromy n - 1 := by
  induction n with
  | zero => simp [monodromyDifference, monodromy]
  | succ n ih =>
    rw [monodromyDifference, monodromy, ih]
    noncomm_ring

end FactorRealization

#print axioms FactorRealization.inverse_coefficient_realization
#print axioms FactorRealization.site_coefficient_realization
#print axioms FactorRealization.monodromyDifference_coefficient
end
end DLWLean.GlobalPDO
