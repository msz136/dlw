import BalancedQuadraticFrequency
import GlobalBalancedSliceBridge
import FrequencyPolynomialIdentification

namespace DLWLean
noncomputable section
open scoped BigOperators

/-- The actual frequency polynomial of the quadratic amplitude
coefficient of the odd charge on the physical balanced slice. -/
def actualOddFrequencyPolynomial (par : FieldParameters) (k : ℕ) : Polynomial ℝ :=
  BalancedPDO.balancedQuadraticFrequencyPolynomial
    (BalancedPDO.balancedSpectralDensityPolynomial par.M (2 * k + 1))
      par.Lx par.B (balancedEta par) (balancedLatticeSign par)

theorem actualOddFrequencyPolynomial_degree (par : FieldParameters) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).natDegree ≤ k := by
  apply BalancedPDO.balancedQuadraticFrequencyPolynomial_degree
  convert BalancedPDO.balancedSpectralDensityPolynomial_homogeneous par.M (2 * k + 1)
    using 1 <;> push_cast <;> ring

theorem actualOddFrequencyPolynomial_top_eq_zero_background (par : FieldParameters) (k : ℕ) :
    (actualOddFrequencyPolynomial par k).coeff k =
      (BalancedPDO.balancedQuadraticFrequencyPolynomial
        (BalancedPDO.balancedSpectralDensityPolynomial par.M (2 * k + 1))
          par.Lx 0 0 (balancedLatticeSign par)).coeff k := by
  apply BalancedPDO.balancedQuadraticFrequencyPolynomial_top_parameter_independent
  convert BalancedPDO.balancedSpectralDensityPolynomial_homogeneous par.M (2 * k + 1)
    using 1 <;> push_cast <;> ring

theorem actualOdd_quadraticAmplitude_cosineSum (par : FieldParameters) (k : ℕ) {N : ℕ}
    (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) :
    (∫ x in (0 : ℝ)..par.Lx,
      (BalancedPDO.perturbationPolynomial par.M
        (BalancedPDO.balancedSpectralDensityPolynomial par.M (2 * k + 1))
        par.B (balancedEta par) (fun j r => balancedLatticeSign par j *
          iteratedDeriv r (periodicCosineSum par.Lx mode amplitude) x)).coeff 2) =
      ∑ i, amplitude i ^ 2 * (actualOddFrequencyPolynomial par k).eval
        (periodicFourierFrequency par.Lx (mode i) ^ 2) :=
  BalancedPDO.integral_quadraticAmplitude_cosineSum _ par.Lx par.Lx_pos _ _ _
    mode hmode hinjective amplitude

/-- This bridge identifies the finite polynomial using computed
zero-background cosine values. The concrete coefficient computation
will supply hcomputed in the next module. -/
theorem actualOddFrequencyPolynomial_top_of_computed_values (par : FieldParameters) (k : ℕ)
    (hcomputed : ∀ mode : ℕ, 0 < mode →
      (∫ x in (0 : ℝ)..par.Lx,
        (BalancedPDO.perturbationPolynomial par.M
          (BalancedPDO.balancedSpectralDensityPolynomial par.M (2 * k + 1))
          0 0 (fun j r => balancedLatticeSign par j *
            iteratedDeriv r (periodicCosine par.Lx mode) x)).coeff 2) =
        (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) *
          (periodicFourierFrequency par.Lx mode ^ 2) ^ k) :
    (actualOddFrequencyPolynomial par k).coeff k =
      (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) := by
  rw [actualOddFrequencyPolynomial_top_eq_zero_background]
  let p := BalancedPDO.balancedQuadraticFrequencyPolynomial
    (BalancedPDO.balancedSpectralDensityPolynomial par.M (2 * k + 1))
      par.Lx 0 0 (balancedLatticeSign par)
  have heq : p = Polynomial.C ((par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1)) *
      Polynomial.X ^ k := by
    apply polynomial_eq_monomial_from_positive_fourier_values par.Lx par.Lx_pos
    intro mode hmode
    rw [← BalancedPDO.integral_quadraticAmplitude_cosine _ par.Lx par.Lx_pos 0 0
      (balancedLatticeSign par) mode hmode]
    exact hcomputed mode hmode
  change p.coeff k = _
  rw [heq, Polynomial.coeff_C_mul, Polynomial.coeff_X_pow_self, mul_one]

theorem actualOddFrequency_top_ne_zero (par : FieldParameters) (k : ℕ) :
    (par.Lx / (par.M : ℝ)) * (-1 : ℝ) ^ (k + 1) ≠ 0 :=
  mul_ne_zero (div_ne_zero (ne_of_gt par.Lx_pos) (Nat.cast_ne_zero.mpr par.M_ne_zero))
    (pow_ne_zero _ (by norm_num))

#print axioms actualOddFrequencyPolynomial_degree
#print axioms actualOddFrequencyPolynomial_top_of_computed_values
end
end DLWLean
