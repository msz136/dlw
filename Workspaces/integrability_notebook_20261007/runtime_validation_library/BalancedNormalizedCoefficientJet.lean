import BalancedQuotientCoefficientJet
import BalancedCoefficientJet
import CoefficientJetPower

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A) (e : DifferentialJetEvaluation M R model.d)

def twoSiteField (plus minus : Fin M) (f : R) (j : Fin M) : R :=
  if j = plus then f else if j = minus then -f else 0

theorem sum_twoSite {B : Type*} [AddCommGroup B] (plus minus : Fin M)
    (hne : plus ≠ minus) (b₁ b₂ : B) :
    (∑ j : Fin M, if j = plus then b₁ else if j = minus then b₂ else 0) = b₁ + b₂ := by
  classical
  have hh (j : Fin M) : (if j = plus then b₁ else if j = minus then b₂ else 0) =
      (if j = plus then b₁ else 0) + (if j = minus then b₂ else 0) := by
    split_ifs <;> simp_all
  simp_rw [hh]
  rw [Finset.sum_add_distrib]
  simp

theorem twoSite_firstResolvent_sum (plus minus : Fin M) (hne : plus ≠ minus) (f : R) :
    (∑ j, firstResolventJet model (twoSiteField plus minus f j)) = 0 := by
  classical
  have hh (j : Fin M) : firstResolventJet model (twoSiteField plus minus f j) =
      if j = plus then firstResolventJet model f else
        if j = minus then -firstResolventJet model f else 0 := by
    unfold twoSiteField
    split_ifs <;> simp [firstResolventJet, map_neg, map_zero]
  simp_rw [hh]
  rw [sum_twoSite plus minus hne]
  simp

theorem twoSite_secondResolvent_sum (plus minus : Fin M) (hne : plus ≠ minus) (f : R) :
    (∑ j, secondResolventJet model (twoSiteField plus minus f j)) =
      (4 : ℝ) • ((↑model.D⁻¹ : A) * model.coefficient f * (↑model.D⁻¹ : A) *
        model.coefficient f * (↑model.D⁻¹ : A)) := by
  classical
  have hh (j : Fin M) : secondResolventJet model (twoSiteField plus minus f j) =
      if j = plus then secondResolventJet model f else
        if j = minus then secondResolventJet model f else 0 := by
    unfold twoSiteField
    split_ifs <;> simp [secondResolventJet, map_neg, map_zero]
  simp_rw [hh]
  rw [sum_twoSite plus minus hne]
  rw [secondResolventJet, ← add_smul]
  norm_num

def balancedBaseQuotientUnit (hM : M ≠ 0) : Aˣ :=
  (Units.map (algebraMap ℝ A).toMonoidHom
    (Units.mk0 (-2 * (M : ℝ)) (mul_ne_zero (by norm_num) (Nat.cast_ne_zero.mpr hM)))) *
      model.D⁻¹

theorem balancedBaseQuotientUnit_val (hM : M ≠ 0) :
    (balancedBaseQuotientUnit model hM : A) = (-2 * (M : ℝ)) • (↑model.D⁻¹ : A) := by
  simp [balancedBaseQuotientUnit, Algebra.smul_def]

theorem balancedBaseQuotientUnit_inv (hM : M ≠ 0) :
    (↑(balancedBaseQuotientUnit model hM)⁻¹ : A) = (-2 * (M : ℝ))⁻¹ • (model.D : A) := by
  have h0ne : (-2 * (M : ℝ)) ≠ 0 := mul_ne_zero (by norm_num) (Nat.cast_ne_zero.mpr hM)
  have hprod : (balancedBaseQuotientUnit model hM : A) *
      ((-2 * (M : ℝ))⁻¹ • (model.D : A)) = 1 := by
    rw [balancedBaseQuotientUnit_val]
    simp only [Algebra.smul_mul_assoc, Algebra.mul_smul_comm, smul_smul,
      Units.inv_mul, mul_inv_cancel₀ h0ne, inv_mul_cancel₀ h0ne, one_smul]
  calc
    (↑(balancedBaseQuotientUnit model hM)⁻¹ : A) =
        (↑(balancedBaseQuotientUnit model hM)⁻¹ : A) *
          ((balancedBaseQuotientUnit model hM : A) *
            ((-2 * (M : ℝ))⁻¹ • (model.D : A))) := by rw [hprod, mul_one]
    _ = _ := by rw [← mul_assoc, Units.inv_mul, one_mul]

def balancedLSecond (f : R) : A :=
  (-4 / (M : ℝ)) • (model.coefficient f * (↑model.D⁻¹ : A) * model.coefficient f)

theorem balancedNormalizedCoefficient_jet_of_quotient (hM : M ≠ 0) (f : R)
    (hH : CoefficientJetRealization model e (balancedQuotientCoefficient M) (-1)
      ((-2 * (M : ℝ)) • (↑model.D⁻¹ : A)) 0
      ((-8 : ℝ) • ((↑model.D⁻¹ : A) * model.coefficient f * (↑model.D⁻¹ : A) *
        model.coefficient f * (↑model.D⁻¹ : A))))
    (hb₀ : e.jet.value (MvPolynomial.X .b) = 0)
    (hb₁ : e.jet.first (MvPolynomial.X .b) = 0)
    (hb₂ : e.jet.second (MvPolynomial.X .b) = 0)
    (hη₀ : e.jet.value (MvPolynomial.X .eta) = 0)
    (hη₁ : e.jet.first (MvPolynomial.X .eta) = 0)
    (hη₂ : e.jet.second (MvPolynomial.X .eta) = 0) :
    CoefficientJetRealization model e (balancedNormalizedCoefficient M) 1
      (model.D : A) 0 (balancedLSecond (M := M) model f) := by
  let u := balancedBaseQuotientUnit model hM
  let T := (↑model.D⁻¹ : A) * model.coefficient f * (↑model.D⁻¹ : A) *
    model.coefficient f * (↑model.D⁻¹ : A)
  let H₂ := (-8 : ℝ) • T
  let V₂ := -(↑u⁻¹ : A) * H₂ * (↑u⁻¹ : A)
  have hu := balancedBaseQuotientUnit_val model hM
  have hui := balancedBaseQuotientUnit_inv model hM
  have hH' : CoefficientJetRealization model e (balancedQuotientCoefficient M) (-1)
      (u : A) 0 H₂ := by simpa only [u, hu, H₂, T] using hH
  have hUi : PDOOrderBound model.coefficients (↑u⁻¹ : A) 1 := by
    rw [hui]
    exact model.smul_bound _ (by simpa using model.D_power_bound 1)
  have hT : PDOOrderBound model.coefficients T (-3) := by
    have h := secondResolventJet_bound model f
    have hDi : PDOOrderBound model.coefficients (↑model.D⁻¹ : A) (-1) := by
      simpa using model.D_power_bound (-1)
    have hleft := model.product_bound _ _ (-2) 0 (firstResolventJet_bound model f)
      (model.embedding_bound f)
    simpa only [T, firstResolventJet, Int.reduceNeg, Int.reduceAdd] using
      model.product_bound _ _ (-2) (-1) hleft hDi
  have hH₂ : PDOOrderBound model.coefficients H₂ (-3) := model.smul_bound (-8) hT
  have hV₂strong : PDOOrderBound model.coefficients V₂ (-1) := by
    have hneg := model.smul_bound (-1) hUi
    have hh : PDOOrderBound model.coefficients (-(↑u⁻¹ : A)) 1 := by simpa using hneg
    have hleft : PDOOrderBound model.coefficients (-(↑u⁻¹ : A) * H₂) (-2) := by
      simpa only [Int.reduceNeg, Int.reduceAdd] using model.product_bound _ _ 1 (-3) hh hH₂
    simpa only [V₂, Int.reduceNeg, Int.reduceAdd] using
      model.product_bound _ _ (-2) 1 hleft hUi
  have hV₂ := model.bound_mono hV₂strong (by norm_num : (-1 : ℤ) ≤ 1)
  have hzero : PDOOrderBound model.coefficients (0 : A) 1 := by intro exponent _; simp
  have hp₁ : (u : A) * 0 + (0 : A) * (↑u⁻¹ : A) = 0 := by simp
  have hp₂ : (u : A) * V₂ + ((0 : A) * 0 + 0 * 0 + H₂ * (↑u⁻¹ : A)) = 0 := by
    simp [V₂, mul_assoc]
  have h0ne : (-2 * (M : ℝ)) ≠ 0 := mul_ne_zero (by norm_num) (Nat.cast_ne_zero.mpr hM)
  have hinverse := inverseCoefficient_jet_realization model e (balancedQuotientCoefficient M)
    (-2 * (M : ℝ)) h0ne u 0 H₂ 0 V₂ hH' (balancedQuotientCoefficient_leading M)
      hzero hV₂ (by simp) (hV₂strong 1 (by norm_num)) hp₁ hp₂
  have hs := CoefficientJetRealization.smul (-2 * (M : ℝ)) hinverse
  have hvalue : (-2 * (M : ℝ)) • (↑u⁻¹ : A) = (model.D : A) := by
    rw [hui, smul_smul, mul_inv_cancel₀ h0ne, one_smul]
  have hsecond : (-2 * (M : ℝ)) • V₂ = balancedLSecond (M := M) model f := by
    have hop : (model.D : A) * T * (model.D : A) =
        model.coefficient f * (↑model.D⁻¹ : A) * model.coefficient f := by
      simp [T, mul_assoc]
    dsimp [V₂, H₂]
    rw [hui]
    rw [← neg_smul]
    simp only [Algebra.smul_mul_assoc, Algebra.mul_smul_comm, smul_smul]
    rw [hop]
    unfold balancedLSecond
    congr 1
    have hMr : (M : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hM
    field_simp
    ring
  rw [hvalue, smul_zero, hsecond] at hs
  have hcor₀ (k : ℕ) : e.jet.value
      (if k = 1 then MvPolynomial.X .b - MvPolynomial.C (M : ℝ) * MvPolynomial.X .eta else 0) = 0 := by
    split_ifs <;> simp only [map_sub, map_mul, hb₀, hη₀, mul_zero, sub_zero, map_zero]
  have hcor₁ (k : ℕ) : e.jet.first
      (if k = 1 then MvPolynomial.X .b - MvPolynomial.C (M : ℝ) * MvPolynomial.X .eta else 0) = 0 := by
    split_ifs <;> simp only [map_sub, e.jet.first_mul, e.first_C,
      hb₁, hη₀, hη₁, zero_mul, mul_zero, zero_add, sub_zero, map_zero]
  have hcor₂ (k : ℕ) : e.jet.second
      (if k = 1 then MvPolynomial.X .b - MvPolynomial.C (M : ℝ) * MvPolynomial.X .eta else 0) = 0 := by
    split_ifs <;> simp only [map_sub, e.jet.second_mul, e.first_C, e.second_C,
      hb₂, hη₀, hη₁, hη₂, zero_mul, mul_zero, zero_add, sub_zero, map_zero]
  constructor
  · exact hs.bound_value
  · exact hs.bound_first
  · exact hs.bound_second
  · intro k
    unfold balancedNormalizedCoefficient normalizedCoefficient
    rw [map_add, hcor₀, add_zero]
    exact hs.value k
  · intro k
    unfold balancedNormalizedCoefficient normalizedCoefficient
    rw [map_add, hcor₁, add_zero]
    exact hs.first k
  · intro k
    unfold balancedNormalizedCoefficient normalizedCoefficient
    rw [map_add, hcor₂, add_zero]
    exact hs.second k

#print axioms balancedNormalizedCoefficient_jet_of_quotient
end
end DLWLean.BalancedPDO
