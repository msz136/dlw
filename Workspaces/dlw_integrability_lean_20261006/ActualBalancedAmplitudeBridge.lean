import ActualFourierEntries
import ActualOddFrequency
import BalancedAmplitudeEvaluationCore
import FourierDirectionJets

namespace DLWLean
noncomputable section
open scoped BigOperators

/-- The actual global charge on the physical amplitude line is the
literal balanced polynomial integral, for every epsilon coefficient. -/
theorem fieldAmplitudePolynomial_balanced_eq (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (n : ℕ) :
    fieldAmplitudePolynomial par (GlobalPDO.periodicDensityPolynomial par n)
      (balancedMomentumState par f) =
        integrateCoefficientPolynomial (periodicCoefficientIntegral par.Lx)
          (balancedPeriodicPerturbationEvaluation par f
            (BalancedPDO.balancedSpectralDensityPolynomial par.M n)) := by
  apply Polynomial.funext
  intro eps
  rw [fieldAmplitudePolynomial_eval, integrateCoefficientPolynomial_eval,
    balancedPeriodicPerturbationEvaluation_eval]
  change GlobalPDO.constructedCharge par n (eps • balancedMomentumState par f) = _
  rw [balancedMomentumState_smul_amplitude, constructedCharge_balanced_density]

theorem fieldAmplitudePolynomial_balanced_coefficient (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (n q : ℕ) :
    (fieldAmplitudePolynomial par (GlobalPDO.periodicDensityPolynomial par n)
      (balancedMomentumState par f)).coeff q =
        ∫ x in (0 : ℝ)..par.Lx,
          (BalancedPDO.perturbationPolynomial par.M
            (BalancedPDO.balancedSpectralDensityPolynomial par.M n) par.B (balancedEta par)
            (fun j k => balancedLatticeSign par j * iteratedDeriv k (f : ℝ → ℝ) x)).coeff q := by
  rw [fieldAmplitudePolynomial_balanced_eq, integrateCoefficientPolynomial_coeff]
  change (∫ x in (0 : ℝ)..par.Lx,
    ((balancedPeriodicPerturbationEvaluation par f
      (BalancedPDO.balancedSpectralDensityPolynomial par.M n)).coeff q : ℝ → ℝ) x) = _
  simp_rw [balancedPeriodicPerturbationEvaluation_pointwise]

/-- The quadratic coefficient of the literal physical amplitude
polynomial equals its computed finite Fourier functional. -/
theorem actualBalancedAmplitude_coeff_two (par : FieldParameters) (k : ℕ) {N : ℕ}
    (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) :
    (fieldAmplitudePolynomial par (GlobalPDO.periodicDensityPolynomial par (2 * k + 1))
      (balancedMomentumState par (periodicCosineSumCoefficient par mode amplitude))).coeff 2 =
        ∑ i, amplitude i ^ 2 * (actualOddFrequencyPolynomial par k).eval
          (periodicFourierFrequency par.Lx (mode i) ^ 2) := by
  rw [fieldAmplitudePolynomial_balanced_coefficient]
  exact actualOdd_quadraticAmplitude_cosineSum par k mode hmode hinjective amplitude

theorem periodicCosineSumCoefficient_amplitude_add (par : FieldParameters) {N : ℕ}
    (mode : Fin N → ℕ) (a b : Fin N → ℝ) :
    periodicCosineSumCoefficient par mode (fun i => a i + b i) =
      periodicCosineSumCoefficient par mode a + periodicCosineSumCoefficient par mode b := by
  apply Subtype.ext
  funext x
  simp [periodicCosineSumCoefficient, periodicCosineSum, add_mul, Finset.sum_add_distrib]

theorem periodicCosineSumCoefficient_amplitude_basis (par : FieldParameters) {N : ℕ}
    (mode : Fin N → ℕ) (j : Fin N) :
    periodicCosineSumCoefficient par mode (fun i => if i = j then 1 else 0) =
      periodicCosineCoefficient par (mode j) := by
  apply Subtype.ext
  funext x
  simp [periodicCosineSumCoefficient, periodicCosineCoefficient, periodicCosineSum]

/-- The literal differential polynomial has the computed linear
epsilon coefficient, including the indispensable amplitude column factor. -/
theorem actualBalancedAmplitudeDifferential_coeff_one (par : FieldParameters) (k : ℕ) {N : ℕ}
    (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) (j : Fin N) :
    (fieldAmplitudeDifferentialPolynomial par (GlobalPDO.periodicDensityPolynomial par (2 * k + 1))
      (balancedMomentumState par (periodicCosineSumCoefficient par mode amplitude))
      (balancedFourierDirection par mode j)).coeff 1 =
        2 * amplitude j * (actualOddFrequencyPolynomial par k).eval
          (periodicFourierFrequency par.Lx (mode j) ^ 2) := by
  classical
  have hsum : balancedMomentumState par (periodicCosineSumCoefficient par mode amplitude) +
      balancedFourierDirection par mode j =
        balancedMomentumState par (periodicCosineSumCoefficient par mode
          (fun i => amplitude i + if i = j then 1 else 0)) := by
    rw [periodicCosineSumCoefficient_amplitude_add, balancedMomentumState_add,
      periodicCosineSumCoefficient_amplitude_basis]
    rfl
  have hb : balancedFourierDirection par mode j = balancedMomentumState par
      (periodicCosineSumCoefficient par mode (fun i => if i = j then 1 else 0)) := by
    rw [periodicCosineSumCoefficient_amplitude_basis]
    rfl
  rw [fieldAmplitudeDifferentialPolynomial_coeff_one, hsum, hb,
    actualBalancedAmplitude_coeff_two par k mode hmode hinjective,
    actualBalancedAmplitude_coeff_two par k mode hmode hinjective,
    actualBalancedAmplitude_coeff_two par k mode hmode hinjective]
  rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib]
  calc
    _ = ∑ i : Fin N, if i = j then
        2 * amplitude j * (actualOddFrequencyPolynomial par k).eval
          (periodicFourierFrequency par.Lx (mode j) ^ 2) else 0 := by
      apply Finset.sum_congr rfl
      intro i _
      split_ifs with hij
      · subst i
        ring
      · ring
    _ = _ := by simp

#print axioms fieldAmplitudePolynomial_balanced_eq
#print axioms actualBalancedAmplitude_coeff_two
#print axioms actualBalancedAmplitudeDifferential_coeff_one
end
end DLWLean
