import CoefficientJetRealization

namespace DLWLean
noncomputable section
open scoped BigOperators

namespace NormalPDOModel
variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

theorem D_mult_equation_coeff (Y Z : A)
    (hY : PDOOrderBound model.coefficients Y (-1))
    (hEq : (model.D : A) * Y = Z) (n : ℕ) :
    model.coefficientBelow Y (-1) (n + 1) +
      model.d.toLinearMap (model.coefficientBelow Y (-1) n) =
        model.coefficients Z (-((n + 1 : ℕ) : ℤ)) := by
  have h := model.product_coefficient (model.D : A) Y 1 (-1)
    (by simpa using model.D_power_bound 1) hY (n + 1)
  rw [hEq] at h
  have hD : (fun r : ℕ => model.coefficients (model.D : A) (1 - (r : ℤ))) =
      (fun r => if r = 0 then 1 else 0) := by
    funext r
    have h := model.coefficient_D_power 1 (1 - (r : ℤ))
    have hr : 1 - (r : ℤ) = 1 ↔ r = 0 := by omega
    simpa only [zpow_one, hr] using h
  rw [hD, normalProductCoefficient_first_order_delta] at h
  have he : (1 : ℤ) + (-1) - ((n + 1 : ℕ) : ℤ) = -((n + 1 : ℕ) : ℤ) := by omega
  simpa only [he, NormalPDOModel.coefficientBelow] using h.symm
end NormalPDOModel

namespace BalancedPDO
variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A) (e : DifferentialJetEvaluation M R model.d)

def firstResolventJet (f : R) : A :=
  (↑model.D⁻¹ : A) * model.coefficient f * (↑model.D⁻¹ : A)

def secondResolventJet (f : R) : A :=
  (2 : ℝ) • ((↑model.D⁻¹ : A) * model.coefficient f *
    (↑model.D⁻¹ : A) * model.coefficient f * (↑model.D⁻¹ : A))

theorem firstResolventJet_bound (f : R) :
    PDOOrderBound model.coefficients (firstResolventJet model f) (-2) := by
  unfold firstResolventJet
  have hDi : PDOOrderBound model.coefficients (↑model.D⁻¹ : A) (-1) := by
    simpa using model.D_power_bound (-1)
  have hleft := model.product_bound _ _ (-1) 0 hDi (model.embedding_bound f)
  simpa using model.product_bound _ _ (-1) (-1) hleft hDi

theorem secondResolventJet_bound (f : R) :
    PDOOrderBound model.coefficients (secondResolventJet model f) (-3) := by
  unfold secondResolventJet
  apply model.smul_bound
  have hDi : PDOOrderBound model.coefficients (↑model.D⁻¹ : A) (-1) := by
    simpa using model.D_power_bound (-1)
  have hleft := model.product_bound _ _ (-2) 0
    (firstResolventJet_bound model f) (model.embedding_bound f)
  simpa only [firstResolventJet, Int.reduceNeg, Int.reduceAdd] using
    model.product_bound _ _ (-2) (-1) hleft hDi

theorem firstResolventJet_D (f : R) :
    (model.D : A) * firstResolventJet model f = model.coefficient f * (↑model.D⁻¹ : A) := by
  simp [firstResolventJet, mul_assoc]

theorem secondResolventJet_D (f : R) :
    (model.D : A) * secondResolventJet model f =
      (2 : ℝ) • (model.coefficient f * firstResolventJet model f) := by
  simp [secondResolventJet, firstResolventJet, mul_assoc, Algebra.mul_smul_comm]

theorem resolventCoefficient_jet_realization (site : Fin M) (f : R)
    (hvalue : e.jet.value (balancedBeta M site) = 0)
    (hfirst : e.jet.first (balancedBeta M site) = f)
    (hsecond : e.jet.second (balancedBeta M site) = 0) :
    CoefficientJetRealization model e (resolventCoefficient M site) (-1)
      (↑model.D⁻¹ : A) (firstResolventJet model f) (secondResolventJet model f) := by
  have hR : PDOOrderBound model.coefficients (↑model.D⁻¹ : A) (-1) := by
    simpa using model.D_power_bound (-1)
  have h₁ := firstResolventJet_bound model f
  have h₂ := secondResolventJet_bound model f
  have h₁weak := model.bound_mono h₁ (by norm_num : (-2 : ℤ) ≤ -1)
  have h₂weak := model.bound_mono h₂ (by norm_num : (-3 : ℤ) ≤ -1)
  have hcR : model.coefficients (↑model.D⁻¹ : A) (-1) = 1 := by
    simpa using model.coefficient_D_power (-1) (-1)
  have hjet : ∀ k,
      e.jet.value (resolventCoefficient M site k) = model.coefficientBelow (↑model.D⁻¹ : A) (-1) k ∧
      e.jet.first (resolventCoefficient M site k) = model.coefficientBelow (firstResolventJet model f) (-1) k ∧
      e.jet.second (resolventCoefficient M site k) = model.coefficientBelow (secondResolventJet model f) (-1) k := by
    intro k
    induction k with
    | zero =>
      rw [resolventCoefficient, map_one, e.jet.first_one, e.jet.second_one]
      exact ⟨(by simpa [NormalPDOModel.coefficientBelow] using hcR.symm),
        (by simpa [NormalPDOModel.coefficientBelow] using (h₁ (-1) (by norm_num)).symm),
        (by simpa [NormalPDOModel.coefficientBelow] using (h₂ (-1) (by norm_num)).symm)⟩
    | succ k ih =>
      have hRrec := model.D_mult_equation_coeff (↑model.D⁻¹ : A) 1 hR (Units.mul_inv _) k
      have hRzero : model.coefficients (1 : A) (-((k + 1 : ℕ) : ℤ)) = 0 := by
        rw [model.coeff_one]
        simp only [show -((k + 1 : ℕ) : ℤ) ≠ 0 by omega, ite_false]
      rw [hRzero] at hRrec
      have h₁rec := model.D_mult_equation_coeff (firstResolventJet model f)
        (model.coefficient f * (↑model.D⁻¹ : A)) h₁weak (firstResolventJet_D model f) k
      rw [model.scalar_left_coefficient] at h₁rec
      have h₂rec := model.D_mult_equation_coeff (secondResolventJet model f)
        ((2 : ℝ) • (model.coefficient f * firstResolventJet model f))
          h₂weak (secondResolventJet_D model f) k
      rw [map_smul] at h₂rec
      simp only [Pi.smul_apply] at h₂rec
      rw [model.scalar_left_coefficient] at h₂rec
      have hexp : -((k + 1 : ℕ) : ℤ) = -1 - (k : ℤ) := by omega
      rw [hexp] at h₁rec h₂rec
      constructor
      · rw [resolventCoefficient, map_sub, map_mul, hvalue, zero_mul,
          e.value_spatial, ih.1]
        simpa only [zero_sub] using (eq_neg_of_add_eq_zero_left hRrec).symm
      constructor
      · rw [resolventCoefficient, map_sub, e.jet.first_mul, hvalue, hfirst,
          zero_mul, add_zero, e.first_spatial, ih.1, ih.2.1]
        change f * model.coefficientBelow (↑model.D⁻¹ : A) (-1) k -
          model.d.toLinearMap (model.coefficientBelow (firstResolventJet model f) (-1) k) = _
        dsimp [NormalPDOModel.coefficientBelow] at h₁rec ⊢
        linear_combination -h₁rec
      · rw [resolventCoefficient, map_sub, e.jet.second_mul, hvalue, hfirst, hsecond]
        simp only [zero_mul, zero_add, add_zero]
        rw [e.second_spatial, ih.2.1, ih.2.2]
        change f * model.coefficientBelow (firstResolventJet model f) (-1) k +
          f * model.coefficientBelow (firstResolventJet model f) (-1) k -
          model.d.toLinearMap (model.coefficientBelow (secondResolventJet model f) (-1) k) = _
        simp only [Algebra.smul_def, map_ofNat] at h₂rec
        dsimp [NormalPDOModel.coefficientBelow] at h₂rec ⊢
        linear_combination -h₂rec
  exact ⟨hR, h₁weak, h₂weak, fun k => (hjet k).1,
    fun k => (hjet k).2.1, fun k => (hjet k).2.2⟩

end BalancedPDO
#print axioms BalancedPDO.resolventCoefficient_jet_realization
end
end DLWLean
