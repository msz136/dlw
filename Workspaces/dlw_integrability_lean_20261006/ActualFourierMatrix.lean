import ActualFourierEntries
import FourierDirectionJets

namespace DLWLean
noncomputable section

def actualFourierMatrix {N : ℕ} (par : FieldParameters) (mode : Fin N → ℕ)
    (amplitude : Fin N → ℝ) : Matrix (Fin N) (Fin N) (Polynomial ℝ) :=
  fun i j => fieldAmplitudeDifferentialPolynomial par
    (GlobalPDO.periodicDensityPolynomial par (2 * i.val + 1))
    (balancedMomentumState par (periodicCosineSumCoefficient par mode amplitude))
    (balancedFourierDirection par mode j)

theorem actualFourierMatrix_eval {N : ℕ} (par : FieldParameters) (mode : Fin N → ℕ)
    (amplitude : Fin N → ℝ) (eps : ℝ) (i j : Fin N) :
    fieldPolynomialDifferential par
      (GlobalPDO.periodicDensityPolynomial par (2 * i.val + 1))
      (balancedMomentumState par (eps • periodicCosineSumCoefficient par mode amplitude))
      (balancedFourierDirection par mode j) =
        (actualFourierMatrix par mode amplitude i j).eval eps := by
  rw [balancedMomentumState_smul]
  exact (fieldAmplitudeDifferentialPolynomial_eval par _ _ _ eps).symm

theorem actualFourierMatrix_coeff_zero {N : ℕ} (par : FieldParameters) (mode : Fin N → ℕ)
    (hmode : ∀ j, 0 < mode j) (amplitude : Fin N → ℝ) (i j : Fin N) :
    (actualFourierMatrix par mode amplitude i j).coeff 0 = 0 := by
  apply fieldAmplitudeDifferentialPolynomial_real_coeff_zero
  intro jet
  exact Fourier_direction_fieldJet_integral_zero par (mode j) (hmode j) jet

#print axioms actualFourierMatrix_eval
#print axioms actualFourierMatrix_coeff_zero
end
end DLWLean
