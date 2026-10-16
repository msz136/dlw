import ActualOddFrequency
import BalancedOddCoefficientIntegral
import ActualSpectralInvolution
import FourierMomentum

namespace DLWLean
noncomputable section

theorem twoSiteField_eq_balancedLatticeSign (par : FieldParameters) (f : ℝ) (j : Fin par.M) :
    BalancedPDO.twoSiteField (firstLatticeSite par) (secondLatticeSite par) f j =
      balancedLatticeSign par j * f := by
  classical
  unfold BalancedPDO.twoSiteField balancedLatticeSign
  by_cases hfirst : j = firstLatticeSite par
  · have hsecond : j ≠ secondLatticeSite par := by
      simpa only [hfirst] using first_ne_second par
    simp [hfirst, first_ne_second par]
  · by_cases hsecond : j = secondLatticeSite par <;>
      simp [hfirst, hsecond, first_ne_second par, Ne.symm (first_ne_second par)]

theorem actualOddFrequencyPolynomial_top_from_normal_model (par : FieldParameters) (k : ℕ)
    {A : Type*} [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel (PeriodicCoefficient par.Lx) A)
    (spatial : model.d = periodicSpatialEvolution par.Lx) (tr : CyclicTrace A)
    (trace_eq : ∀ X : A, tr.toLinearMap X =
      periodicCoefficientIntegral par.Lx (model.coefficients X (-1))) :
    (actualOddFrequencyPolynomial par k).coeff k =
      (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) := by
  apply actualOddFrequencyPolynomial_top_of_computed_values
  intro mode hmode
  have h := BalancedPDO.balancedOddDensity_actual_quadratic_integral model spatial tr trace_eq
    (firstLatticeSite par) (secondLatticeSite par) (first_ne_second par) par.M_ne_zero
      (periodicCosineCoefficient par mode) k
  simp_rw [twoSiteField_eq_balancedLatticeSign] at h
  change (∫ x in (0 : ℝ)..par.Lx,
    (BalancedPDO.perturbationPolynomial par.M
      (BalancedPDO.balancedSpectralDensityPolynomial par.M (2 * k + 1)) 0 0
        (fun j r => balancedLatticeSign par j *
          iteratedDeriv r (periodicCosine par.Lx mode) x)).coeff 2) =
      (2 / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) *
        ∫ x in (0 : ℝ)..par.Lx, (iteratedDeriv k (periodicCosine par.Lx mode) x) ^ 2 at h
  rw [integral_periodicCosine_derivative_sq par.Lx par.Lx_pos mode hmode k] at h
  rw [h]
  rw [← pow_mul]
  ring

theorem actualOddFrequencyPolynomial_top (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).coeff k =
      (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) := by
  obtain ⟨rep⟩ := foundation 0
  exact actualOddFrequencyPolynomial_top_from_normal_model par k
    rep.base.model rep.base.spatial rep.base.tr rep.base.trace_eq

theorem actualOddFrequencyPolynomial_leading_ne_zero (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).coeff k ≠ 0 := by
  rw [actualOddFrequencyPolynomial_top par foundation k]
  exact actualOddFrequency_top_ne_zero par k

#print axioms actualOddFrequencyPolynomial_top
#print axioms actualOddFrequencyPolynomial_leading_ne_zero
end
end DLWLean
