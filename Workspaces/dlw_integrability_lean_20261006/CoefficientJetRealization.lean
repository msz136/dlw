import DifferentialJetEvaluation

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem normalInverseRemainder_congr {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (H H' V V' : ℕ → R) (n : ℕ)
    (hH : ∀ r, H r = H' r) (hV : ∀ s ≤ n, V s = V' s) :
    normalInverseRemainder d H V n = normalInverseRemainder d H' V' n := by
  classical
  unfold normalInverseRemainder
  apply Finset.sum_congr rfl
  intro s _
  apply Finset.sum_congr rfl
  intro r _
  rw [hH, hV s.val (by have := s.isLt; omega)]

namespace NormalPDOModel
variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

theorem bound_pred_of_leading_zero (X : A) (order : ℤ)
    (hX : PDOOrderBound model.coefficients X order)
    (hzero : model.coefficients X order = 0) :
    PDOOrderBound model.coefficients X (order - 1) := by
  intro exponent he
  by_cases hexp : exponent = order
  · simpa [hexp] using hzero
  · exact hX exponent (by omega)

theorem sum_bound {ι : Type*} (s : Finset ι) (X : ι → A) (order : ℤ)
    (hX : ∀ i ∈ s, PDOOrderBound model.coefficients (X i) order) :
    PDOOrderBound model.coefficients (∑ i ∈ s, X i) order := by
  intro exponent he
  rw [map_sum]
  rw [Finset.sum_apply]
  exact Finset.sum_eq_zero (fun i hi => hX i hi exponent he)

theorem linear_inverse_equation_succ (u : Aˣ) (h0 : ℝ) (h0ne : h0 ≠ 0)
    (hu : PDOOrderBound model.coefficients (u : A) (-1))
    (hlead : model.coefficients (u : A) (-1) = algebraMap ℝ R h0)
    (Y Z : A) (hY : PDOOrderBound model.coefficients Y 1)
    (hlinear : (u : A) * Y + Z = 0) (n : ℕ) :
    model.coefficientBelow Y 1 (n + 1) = algebraMap ℝ R (-h0⁻¹) *
      (normalInverseRemainder model.d
        (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow Y 1) n +
        model.coefficients Z (-((n + 1 : ℕ) : ℤ))) := by
  have h := congrArg (fun X : A => model.coefficients X (-((n + 1 : ℕ) : ℤ))) hlinear
  simp only [map_add, map_zero, Pi.add_apply, Pi.zero_apply] at h
  have hexp : -((n + 1 : ℕ) : ℤ) = (-1 : ℤ) + 1 - ((n + 1 : ℕ) : ℤ) := by omega
  rw [hexp, model.product_coefficient _ _ (-1) 1 hu hY,
    normalProductCoefficient_isolate_inverse] at h
  simp only [Nat.cast_zero, sub_zero, hlead] at h
  change algebraMap ℝ R h0 * model.coefficientBelow Y 1 (n + 1) +
    normalInverseRemainder model.d (model.coefficientBelow (u : A) (-1))
      (model.coefficientBelow Y 1) n + model.coefficients Z
      ((-1 : ℤ) + 1 - ((n + 1 : ℕ) : ℤ)) = 0 at h
  have hi : algebraMap ℝ R h0⁻¹ * algebraMap ℝ R h0 = 1 := by
    rw [← map_mul, inv_mul_cancel₀ h0ne, map_one]
  have hsol := congrArg (fun x : R => algebraMap ℝ R h0⁻¹ * x) h
  simp only [mul_add, ← mul_assoc, hi, one_mul, mul_zero] at hsol
  rw [map_neg, neg_mul]
  have hz : (-1 : ℤ) + 1 - ((n + 1 : ℕ) : ℤ) = -((n + 1 : ℕ) : ℤ) := by omega
  rw [hz] at hsol
  linear_combination hsol

theorem product_coefficient_without_leading (X Y : A)
    (hX : PDOOrderBound model.coefficients X (-1))
    (hY : PDOOrderBound model.coefficients Y 1)
    (hlead : model.coefficients X (-1) = 0) (n : ℕ) :
    model.coefficients (X * Y) (-((n + 1 : ℕ) : ℤ)) =
      normalInverseRemainder model.d
        (model.coefficientBelow X (-1)) (model.coefficientBelow Y 1) n := by
  have hexp : -((n + 1 : ℕ) : ℤ) = (-1 : ℤ) + 1 - ((n + 1 : ℕ) : ℤ) := by omega
  rw [hexp, model.product_coefficient _ _ (-1) 1 hX hY,
    normalProductCoefficient_isolate_inverse]
  simp only [Nat.cast_zero, sub_zero, hlead, zero_mul, zero_add]
  rfl

end NormalPDOModel

namespace BalancedPDO
variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A) (e : DifferentialJetEvaluation M R model.d)

/-- A coefficient-wise two-jet of one finite normal-form recurrence.
No parameter differentiation is postulated on the PDO ring itself. -/
structure CoefficientJetRealization (a : ℕ → Poly M) (order : ℤ) (X₀ X₁ X₂ : A) : Prop where
  bound_value : PDOOrderBound model.coefficients X₀ order
  bound_first : PDOOrderBound model.coefficients X₁ order
  bound_second : PDOOrderBound model.coefficients X₂ order
  value : ∀ k, e.jet.value (a k) = model.coefficientBelow X₀ order k
  first : ∀ k, e.jet.first (a k) = model.coefficientBelow X₁ order k
  second : ∀ k, e.jet.second (a k) = model.coefficientBelow X₂ order k

namespace CoefficientJetRealization
variable {model e}

theorem smul (c : ℝ) {a : ℕ → Poly M} {order : ℤ} {X₀ X₁ X₂ : A}
    (ha : CoefficientJetRealization model e a order X₀ X₁ X₂) :
    CoefficientJetRealization model e (fun k => MvPolynomial.C c * a k) order
      (c • X₀) (c • X₁) (c • X₂) := by
  constructor
  · exact model.smul_bound c ha.bound_value
  · exact model.smul_bound c ha.bound_first
  · exact model.smul_bound c ha.bound_second
  · intro k
    rw [map_mul, e.value_C, ha.value]
    unfold NormalPDOModel.coefficientBelow
    rw [map_smul]
    simp only [Pi.smul_apply, Algebra.smul_def]
  · intro k
    rw [e.jet.first_mul, e.first_C, zero_mul, zero_add, e.value_C, ha.first]
    unfold NormalPDOModel.coefficientBelow
    rw [map_smul]
    simp only [Pi.smul_apply, Algebra.smul_def]
  · intro k
    rw [e.jet.second_mul, e.first_C, e.second_C]
    simp only [zero_mul, zero_add]
    rw [e.value_C, ha.second]
    unfold NormalPDOModel.coefficientBelow
    rw [map_smul]
    simp only [Pi.smul_apply, Algebra.smul_def]

theorem sum {ι : Type*} (s : Finset ι) (a : ι → ℕ → Poly M) (order : ℤ)
    (X₀ X₁ X₂ : ι → A)
    (h : ∀ i ∈ s, CoefficientJetRealization model e (a i) order (X₀ i) (X₁ i) (X₂ i)) :
    CoefficientJetRealization model e (fun k => ∑ i ∈ s, a i k) order
      (∑ i ∈ s, X₀ i) (∑ i ∈ s, X₁ i) (∑ i ∈ s, X₂ i) := by
  constructor
  · exact model.sum_bound s X₀ order (fun i hi => (h i hi).bound_value)
  · exact model.sum_bound s X₁ order (fun i hi => (h i hi).bound_first)
  · exact model.sum_bound s X₂ order (fun i hi => (h i hi).bound_second)
  · intro k
    simp only [map_sum, NormalPDOModel.coefficientBelow, Finset.sum_apply]
    apply Finset.sum_congr rfl
    intro i hi
    exact (h i hi).value k
  · intro k
    simp only [map_sum, NormalPDOModel.coefficientBelow, Finset.sum_apply]
    apply Finset.sum_congr rfl
    intro i hi
    exact (h i hi).first k
  · intro k
    simp only [map_sum, NormalPDOModel.coefficientBelow, Finset.sum_apply]
    apply Finset.sum_congr rfl
    intro i hi
    exact (h i hi).second k

theorem mul {a b : ℕ → Poly M} {orderA orderB : ℤ} {X₀ X₁ X₂ Y₀ Y₁ Y₂ : A}
    (ha : CoefficientJetRealization model e a orderA X₀ X₁ X₂)
    (hb : CoefficientJetRealization model e b orderB Y₀ Y₁ Y₂) :
    CoefficientJetRealization model e (normalProduct M orderA a b)
      (orderA + orderB) (X₀ * Y₀) (X₁ * Y₀ + X₀ * Y₁)
      (X₂ * Y₀ + X₁ * Y₁ + X₁ * Y₁ + X₀ * Y₂) := by
  constructor
  · exact model.product_bound _ _ _ _ ha.bound_value hb.bound_value
  · exact model.add_bound
      (model.product_bound _ _ _ _ ha.bound_first hb.bound_value)
      (model.product_bound _ _ _ _ ha.bound_value hb.bound_first)
  · exact model.add_bound (model.add_bound (model.add_bound
      (model.product_bound _ _ _ _ ha.bound_second hb.bound_value)
      (model.product_bound _ _ _ _ ha.bound_first hb.bound_first))
      (model.product_bound _ _ _ _ ha.bound_first hb.bound_first))
      (model.product_bound _ _ _ _ ha.bound_value hb.bound_second)
  · intro k
    rw [e.normalProduct_value]
    simp only [ha.value, hb.value, NormalPDOModel.coefficientBelow]
    exact (model.product_coefficient _ _ _ _ ha.bound_value hb.bound_value k).symm
  · intro k
    rw [e.normalProduct_first]
    simp only [ha.value, ha.first, hb.value, hb.first, NormalPDOModel.coefficientBelow,
      map_add, Pi.add_apply]
    rw [model.product_coefficient _ _ _ _ ha.bound_first hb.bound_value,
      model.product_coefficient _ _ _ _ ha.bound_value hb.bound_first]
  · intro k
    rw [e.normalProduct_second]
    simp only [ha.value, ha.first, ha.second, hb.value, hb.first, hb.second,
      NormalPDOModel.coefficientBelow, map_add, Pi.add_apply]
    rw [model.product_coefficient _ _ _ _ ha.bound_second hb.bound_value,
      model.product_coefficient _ _ _ _ ha.bound_first hb.bound_first,
      model.product_coefficient _ _ _ _ ha.bound_value hb.bound_second]

end CoefficientJetRealization

theorem inverseCoefficient_jet_realization (H : ℕ → Poly M) (h0 : ℝ) (h0ne : h0 ≠ 0)
    (u : Aˣ) (H₁ H₂ V₁ V₂ : A)
    (hH : CoefficientJetRealization model e H (-1) (u : A) H₁ H₂)
    (hH0 : H 0 = MvPolynomial.C h0)
    (hV₁ : PDOOrderBound model.coefficients V₁ 1)
    (hV₂ : PDOOrderBound model.coefficients V₂ 1)
    (hV₁0 : model.coefficients V₁ 1 = 0)
    (hV₂0 : model.coefficients V₂ 1 = 0)
    (hprod₁ : (u : A) * V₁ + H₁ * (↑u⁻¹ : A) = 0)
    (hprod₂ : (u : A) * V₂ +
      (H₁ * V₁ + H₁ * V₁ + H₂ * (↑u⁻¹ : A)) = 0) :
    CoefficientJetRealization model e (inverseCoefficient M H h0⁻¹) 1
      (↑u⁻¹ : A) V₁ V₂ := by
  classical
  have hlead : model.coefficients (u : A) (-1) = algebraMap ℝ R h0 := by
    have h := hH.value 0
    rw [hH0, e.value_C] at h
    simpa only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero] using h.symm
  have hH₁0 : model.coefficients H₁ (-1) = 0 := by
    have h := hH.first 0
    rw [hH0, e.first_C] at h
    simpa only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero] using h.symm
  have hH₂0 : model.coefficients H₂ (-1) = 0 := by
    have h := hH.second 0
    rw [hH0, e.second_C] at h
    simpa only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero] using h.symm
  have hinv := model.constantLeading_inverse_bound u h0 h0ne hH.bound_value hlead
  have hjet : ∀ k,
      e.jet.value (inverseCoefficient M H h0⁻¹ k) = model.coefficientBelow (↑u⁻¹ : A) 1 k ∧
      e.jet.first (inverseCoefficient M H h0⁻¹ k) = model.coefficientBelow V₁ 1 k ∧
      e.jet.second (inverseCoefficient M H h0⁻¹ k) = model.coefficientBelow V₂ 1 k := by
    intro k
    induction k using Nat.strong_induction_on with
    | h k ih =>
      cases k with
      | zero =>
        rw [inverseCoefficient, e.value_C, e.first_C, e.second_C]
        exact ⟨(model.constantLeading_inverse_zero u h0 h0ne hH.bound_value hlead).symm,
          (by simpa [NormalPDOModel.coefficientBelow] using hV₁0.symm),
          (by simpa [NormalPDOModel.coefficientBelow] using hV₂0.symm)⟩
      | succ n =>
        let V := inverseCoefficient M H h0⁻¹
        have hR₀₀ : normalInverseRemainder model.d (fun r => e.jet.value (H r))
            (fun s => e.jet.value (V s)) n = normalInverseRemainder model.d
              (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow (↑u⁻¹ : A) 1) n :=
          normalInverseRemainder_congr model.d _ _ _ _ n hH.value
            (fun s hs => (ih s (by omega)).1)
        have hR₁₀ : normalInverseRemainder model.d (fun r => e.jet.first (H r))
            (fun s => e.jet.value (V s)) n = normalInverseRemainder model.d
              (model.coefficientBelow H₁ (-1)) (model.coefficientBelow (↑u⁻¹ : A) 1) n :=
          normalInverseRemainder_congr model.d _ _ _ _ n hH.first
            (fun s hs => (ih s (by omega)).1)
        have hR₀₁ : normalInverseRemainder model.d (fun r => e.jet.value (H r))
            (fun s => e.jet.first (V s)) n = normalInverseRemainder model.d
              (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow V₁ 1) n :=
          normalInverseRemainder_congr model.d _ _ _ _ n hH.value
            (fun s hs => (ih s (by omega)).2.1)
        have hR₂₀ : normalInverseRemainder model.d (fun r => e.jet.second (H r))
            (fun s => e.jet.value (V s)) n = normalInverseRemainder model.d
              (model.coefficientBelow H₂ (-1)) (model.coefficientBelow (↑u⁻¹ : A) 1) n :=
          normalInverseRemainder_congr model.d _ _ _ _ n hH.second
            (fun s hs => (ih s (by omega)).1)
        have hR₁₁ : normalInverseRemainder model.d (fun r => e.jet.first (H r))
            (fun s => e.jet.first (V s)) n = normalInverseRemainder model.d
              (model.coefficientBelow H₁ (-1)) (model.coefficientBelow V₁ 1) n :=
          normalInverseRemainder_congr model.d _ _ _ _ n hH.first
            (fun s hs => (ih s (by omega)).2.1)
        have hR₀₂ : normalInverseRemainder model.d (fun r => e.jet.value (H r))
            (fun s => e.jet.second (V s)) n = normalInverseRemainder model.d
              (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow V₂ 1) n :=
          normalInverseRemainder_congr model.d _ _ _ _ n hH.value
            (fun s hs => (ih s (by omega)).2.2)
        constructor
        · rw [inverseCoefficient_succ, map_mul, e.value_C, e.inverseRemainder_value]
          rw [show normalInverseRemainder model.d (fun r => e.jet.value (H r))
            (fun s => e.jet.value (inverseCoefficient M H h0⁻¹ s)) n = _ from hR₀₀]
          exact (model.constantLeading_inverse_succ u h0 h0ne hH.bound_value hlead n).symm
        constructor
        · rw [inverseCoefficient_succ, e.jet.first_mul, e.first_C, zero_mul, zero_add,
            e.value_C, e.inverseRemainder_first]
          rw [show normalInverseRemainder model.d (fun r => e.jet.first (H r))
            (fun s => e.jet.value (inverseCoefficient M H h0⁻¹ s)) n = _ from hR₁₀,
            show normalInverseRemainder model.d (fun r => e.jet.value (H r))
            (fun s => e.jet.first (inverseCoefficient M H h0⁻¹ s)) n = _ from hR₀₁]
          rw [model.linear_inverse_equation_succ u h0 h0ne hH.bound_value hlead V₁
            (H₁ * (↑u⁻¹ : A)) hV₁ hprod₁,
            model.product_coefficient_without_leading _ _ hH.bound_first hinv hH₁0]
          ring
        · rw [inverseCoefficient_succ, e.jet.second_mul, e.first_C, e.second_C,
            zero_mul, zero_add, e.value_C, e.inverseRemainder_second]
          rw [show normalInverseRemainder model.d (fun r => e.jet.second (H r))
            (fun s => e.jet.value (inverseCoefficient M H h0⁻¹ s)) n = _ from hR₂₀,
            show normalInverseRemainder model.d (fun r => e.jet.first (H r))
            (fun s => e.jet.first (inverseCoefficient M H h0⁻¹ s)) n = _ from hR₁₁,
            show normalInverseRemainder model.d (fun r => e.jet.value (H r))
            (fun s => e.jet.second (inverseCoefficient M H h0⁻¹ s)) n = _ from hR₀₂]
          rw [model.linear_inverse_equation_succ u h0 h0ne hH.bound_value hlead V₂
            (H₁ * V₁ + H₁ * V₁ + H₂ * (↑u⁻¹ : A)) hV₂ hprod₂,
            map_add, map_add]
          simp only [Pi.add_apply]
          rw [model.product_coefficient_without_leading _ _ hH.bound_first hV₁ hH₁0,
            model.product_coefficient_without_leading _ _ hH.bound_second hinv hH₂0]
          ring
  exact ⟨hinv, hV₁, hV₂, fun k => (hjet k).1,
    fun k => (hjet k).2.1, fun k => (hjet k).2.2⟩
end BalancedPDO

#print axioms BalancedPDO.CoefficientJetRealization.mul
#print axioms BalancedPDO.inverseCoefficient_jet_realization
end
end DLWLean
