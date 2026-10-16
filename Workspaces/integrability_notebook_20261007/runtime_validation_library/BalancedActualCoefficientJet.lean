import BalancedNormalizedCoefficientJet
import CoefficientJetPointwise
import NormalModelResidue

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

def twoSiteSpatialField (d : AlgebraEvolution R) (plus minus : Fin M) (f : R)
    (j : Fin M) (k : ℕ) : R := twoSiteField plus minus (d.toLinearMap^[k] f) j

theorem twoSiteSpatialField_derivative (d : AlgebraEvolution R)
    (plus minus : Fin M) (f : R) (j : Fin M) (k : ℕ) :
    d.toLinearMap (twoSiteSpatialField d plus minus f j k) =
      twoSiteSpatialField d plus minus f j (k + 1) := by
  classical
  unfold twoSiteSpatialField twoSiteField
  split_ifs <;> simp [Function.iterate_succ_apply', map_neg, map_zero]

def twoSiteDifferentialJetEvaluation (plus minus : Fin M) (f : R) :
    DifferentialJetEvaluation M R model.d :=
  actualDifferentialJetEvaluation M (twoSiteSpatialField model.d plus minus f) model.d
    (twoSiteSpatialField_derivative model.d plus minus f)

theorem balancedNormalizedCoefficient_actual_twoSite_jet (plus minus : Fin M)
    (hne : plus ≠ minus) (hM : M ≠ 0) (f : R) :
    CoefficientJetRealization model (twoSiteDifferentialJetEvaluation model plus minus f)
      (balancedNormalizedCoefficient M) 1 (model.D : A) 0 (balancedLSecond (M := M) model f) := by
  let e := twoSiteDifferentialJetEvaluation model plus minus f
  have he : e.jet = actualCoefficientJet M (twoSiteSpatialField model.d plus minus f) := rfl
  have hη₀ : e.jet.value (MvPolynomial.X .eta) = 0 := by rw [he]; simp
  have hη₁ : e.jet.first (MvPolynomial.X .eta) = 0 := by rw [he]; simp
  have hη₂ : e.jet.second (MvPolynomial.X .eta) = 0 := by rw [he]; simp
  have hβ₀ (j : Fin M) : e.jet.value (balancedBeta M j) = 0 := by
    rw [he]
    simp [balancedBeta]
  have hβ₁ (j : Fin M) : e.jet.first (balancedBeta M j) = twoSiteField plus minus f j := by
    rw [he]
    simp [balancedBeta, twoSiteSpatialField]
  have hβ₂ (j : Fin M) : e.jet.second (balancedBeta M j) = 0 := by
    rw [he]
    simp [balancedBeta]
  have hH := balancedQuotient_jet_realization model e (twoSiteField plus minus f)
    hη₀ hη₁ hη₂ hβ₀ hβ₁ hβ₂
  rw [twoSite_firstResolvent_sum model plus minus hne f,
    twoSite_secondResolvent_sum model plus minus hne f, smul_zero, smul_smul] at hH
  norm_num only at hH
  exact balancedNormalizedCoefficient_jet_of_quotient model e hM f hH
    (by rw [he]; simp) (by rw [he]; simp) (by rw [he]; simp) hη₀ hη₁ hη₂

/-- The literal coefficient jet, normalized by n and by Taylor's 1/2,
has its all-order trace coefficient computed from the finite recurrences. -/
theorem balancedOddDensity_actual_second_trace (tr : CyclicTrace A)
    (residueTrace : R →ₗ[ℝ] ℝ)
    (htrace : ∀ X : A, tr.toLinearMap X = residueTrace (model.coefficients X (-1)))
    (plus minus : Fin M) (hne : plus ≠ minus) (hM : M ≠ 0) (f : R) (k : ℕ) :
    (1 / 2 : ℝ) * residueTrace
      ((twoSiteDifferentialJetEvaluation model plus minus f).jet.second
        (balancedSpectralDensityPolynomial M (2 * k + 1))) =
      (-2 / (M : ℝ)) * tr.toLinearMap ((model.D : A) ^ (2 * k) *
        (model.coefficient f * (↑model.D⁻¹ : A) * model.coefficient f)) := by
  let e := twoSiteDifferentialJetEvaluation model plus minus f
  have hL := balancedNormalizedCoefficient_actual_twoSite_jet model plus minus hne hM f
  have hpower := powerCoefficient_spectral_second_trace model e tr residueTrace htrace
    (balancedNormalizedCoefficient M) (balancedLSecond (M := M) model f) hL
      (2 * k + 1) (by omega)
  have hDensity : e.jet.second (balancedSpectralDensityPolynomial M (2 * k + 1)) =
      ((2 * k + 1 : ℕ) : ℝ)⁻¹ • e.jet.second (balancedResiduePolynomial M (2 * k + 1)) := by
    unfold balancedSpectralDensityPolynomial
    rw [e.jet.second_mul, e.first_C, e.second_C]
    simp only [zero_mul, zero_add]
    rw [e.value_C, Algebra.smul_def]
  rw [hDensity, map_smul]
  simp only [smul_eq_mul]
  change (1 / 2 : ℝ) * (((2 * k + 1 : ℕ) : ℝ)⁻¹ * residueTrace
    (e.jet.second (powerCoefficient M (balancedNormalizedCoefficient M) (2 * k + 1) (2 * k + 1 + 1)))) = _
  rw [hpower]
  simp only [Nat.add_sub_cancel, balancedLSecond, Algebra.mul_smul_comm, map_smul, smul_eq_mul]
  ring

#print axioms balancedNormalizedCoefficient_actual_twoSite_jet
#print axioms balancedOddDensity_actual_second_trace
end
end DLWLean.BalancedPDO
