import QuadraticPairings

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

/-- The frequency polynomial of an actual mixed quadratic derivative
term, after periodic integration by parts. Odd total orders vanish. -/
def derivativeFrequencyPolynomial (period : ℝ) (m n : ℕ) : Polynomial ℝ :=
  if Even (m + n) then
    Polynomial.C ((-1 : ℝ) ^ (m + (m + n) / 2) * (period / 2)) *
      Polynomial.X ^ ((m + n) / 2)
  else 0

theorem derivativePairing_cosine_frequencyPolynomial (period : ℝ)
    (hperiod : 0 < period) (mode : ℕ) (hmode : 0 < mode) (m n : ℕ) :
    derivativePairing period (periodicCosine period mode) m n =
      (derivativeFrequencyPolynomial period m n).eval
        (periodicFourierFrequency period mode ^ 2) := by
  by_cases heven : Even (m + n)
  · obtain ⟨k, hk⟩ := heven
    have htotal : m + n = 2 * k := by omega
    have hhalf : (m + n) / 2 = k := by omega
    rw [derivativePairing_even_total period (periodicCosine period mode)
      (periodicCosine_smooth period mode)
      (periodicCosine_periodic period (ne_of_gt hperiod) mode) m n k htotal,
      integral_periodicCosine_derivative_sq period hperiod mode hmode k]
    simp only [derivativeFrequencyPolynomial, show Even (m + n) from ⟨k, hk⟩,
      ite_true, hhalf, Polynomial.eval_mul, Polynomial.eval_C,
      Polynomial.eval_pow, Polynomial.eval_X]
    rw [← pow_mul]
    ring
  · have hodd : Odd (m + n) := by
      rcases Nat.even_or_odd (m + n) with h | h
      · exact (heven h).elim
      · exact h
    rw [derivativePairing_odd_total_zero period (periodicCosine period mode)
      (periodicCosine_smooth period mode)
      (periodicCosine_periodic period (ne_of_gt hperiod) mode) m n hodd]
    simp [derivativeFrequencyPolynomial, heven]

theorem derivativeFrequencyPolynomial_degree (period : ℝ) (m n k : ℕ)
    (hbound : m + n ≤ 2 * k) :
    (derivativeFrequencyPolynomial period m n).natDegree ≤ k := by
  unfold derivativeFrequencyPolynomial
  split_ifs with heven
  · have hhalf : (m + n) / 2 ≤ k := by omega
    calc
      _ ≤ (Polynomial.C ((-1 : ℝ) ^ (m + (m + n) / 2) * (period / 2))).natDegree +
          (Polynomial.X ^ ((m + n) / 2) : Polynomial ℝ).natDegree :=
        Polynomial.natDegree_mul_le
      _ = (m + n) / 2 := by
        rw [Polynomial.natDegree_C, Polynomial.natDegree_X_pow, zero_add]
      _ ≤ k := hhalf
  · simp

theorem derivativeFrequencyPolynomial_top_zero (period : ℝ) (m n k : ℕ)
    (hbound : m + n < 2 * k) :
    (derivativeFrequencyPolynomial period m n).coeff k = 0 := by
  unfold derivativeFrequencyPolynomial
  split_ifs with heven
  · have hhalf : (m + n) / 2 < k := by omega
    apply Polynomial.coeff_eq_zero_of_natDegree_lt
    calc
      _ ≤ (Polynomial.C ((-1 : ℝ) ^ (m + (m + n) / 2) * (period / 2))).natDegree +
          (Polynomial.X ^ ((m + n) / 2) : Polynomial ℝ).natDegree :=
        Polynomial.natDegree_mul_le
      _ = (m + n) / 2 := by
        rw [Polynomial.natDegree_C, Polynomial.natDegree_X_pow, zero_add]
      _ < k := hhalf
  · simp

def quadraticFrequencyPolynomial {ι : Type*} [Fintype ι]
    (period : ℝ) (coefficient : ι → ℝ) (left right : ι → ℕ) : Polynomial ℝ :=
  ∑ i, Polynomial.C (coefficient i) * derivativeFrequencyPolynomial period (left i) (right i)

theorem quadraticFrequencyPolynomial_eval {ι : Type*} [Fintype ι]
    (period : ℝ) (coefficient : ι → ℝ) (left right : ι → ℕ) (frequency : ℝ) :
    (quadraticFrequencyPolynomial period coefficient left right).eval frequency =
      ∑ i, coefficient i * (derivativeFrequencyPolynomial period (left i) (right i)).eval frequency := by
  unfold quadraticFrequencyPolynomial
  rw [Polynomial.eval_finsetSum]
  simp only [Polynomial.eval_mul, Polynomial.eval_C]

theorem quadraticFrequencyPolynomial_degree {ι : Type*} [Fintype ι]
    (period : ℝ) (coefficient : ι → ℝ) (left right : ι → ℕ)
    (k : ℕ) (hbound : ∀ i, left i + right i ≤ 2 * k) :
    (quadraticFrequencyPolynomial period coefficient left right).natDegree ≤ k := by
  apply Polynomial.natDegree_sum_le_of_forall_le
  intro i _
  calc
    _ ≤ (Polynomial.C (coefficient i)).natDegree +
        (derivativeFrequencyPolynomial period (left i) (right i)).natDegree :=
      Polynomial.natDegree_mul_le
    _ = (derivativeFrequencyPolynomial period (left i) (right i)).natDegree := by simp
    _ ≤ k := derivativeFrequencyPolynomial_degree period _ _ k (hbound i)

def quadraticDerivativeDensity {ι : Type*} [Fintype ι]
    (coefficient : ι → ℝ) (left right : ι → ℕ) (f : ℝ → ℝ) (x : ℝ) : ℝ :=
  ∑ i, coefficient i * (iteratedDeriv (left i) f x * iteratedDeriv (right i) f x)

/-- The finite mixed-derivative density has an actual Fourier integral
given by the constructed frequency polynomial. -/
theorem integral_quadraticDerivativeDensity_cosine {ι : Type*} [Fintype ι]
    (period : ℝ) (hperiod : 0 < period) (mode : ℕ) (hmode : 0 < mode)
    (coefficient : ι → ℝ) (left right : ι → ℕ) :
    (∫ x in (0 : ℝ)..period,
      quadraticDerivativeDensity coefficient left right (periodicCosine period mode) x) =
      (quadraticFrequencyPolynomial period coefficient left right).eval
        (periodicFourierFrequency period mode ^ 2) := by
  unfold quadraticDerivativeDensity
  rw [intervalIntegral.integral_finsetSum]
  · rw [quadraticFrequencyPolynomial_eval]
    apply Finset.sum_congr rfl
    intro i _
    rw [intervalIntegral.integral_const_mul]
    congr 1
    exact derivativePairing_cosine_frequencyPolynomial period hperiod mode hmode _ _
  · intro i _
    have hcont : Continuous (fun x : ℝ => coefficient i *
        (iteratedDeriv (left i) (periodicCosine period mode) x *
          iteratedDeriv (right i) (periodicCosine period mode) x)) :=
      continuous_const.mul
      (((periodicCosine_smooth period mode).continuous_iteratedDeriv (left i) (by simp)).mul
        ((periodicCosine_smooth period mode).continuous_iteratedDeriv (right i) (by simp)))
    exact hcont.intervalIntegrable 0 period

theorem derivativeFrequencyPolynomial_top_coefficient (period : ℝ) (m n k : ℕ)
    (htotal : m + n = 2 * k) :
    (derivativeFrequencyPolynomial period m n).coeff k =
      (-1 : ℝ) ^ (m + k) * (period / 2) := by
  have heven : Even (m + n) := ⟨k, by omega⟩
  have hhalf : (m + n) / 2 = k := by omega
  simp only [derivativeFrequencyPolynomial, heven, ite_true, hhalf]
  simp only [Polynomial.coeff_C_mul, Polynomial.coeff_X_pow_self, mul_one]

theorem quadraticFrequencyPolynomial_top_coefficient {ι : Type*} [Fintype ι]
    (period : ℝ) (coefficient : ι → ℝ) (left right : ι → ℕ)
    (k : ℕ) (hbound : ∀ i, left i + right i ≤ 2 * k) :
    (quadraticFrequencyPolynomial period coefficient left right).coeff k =
      ∑ i, if left i + right i = 2 * k then
        coefficient i * ((-1 : ℝ) ^ (left i + k) * (period / 2)) else 0 := by
  unfold quadraticFrequencyPolynomial
  rw [Polynomial.finsetSum_coeff]
  apply Finset.sum_congr rfl
  intro i _
  rw [Polynomial.coeff_C_mul]
  by_cases htotal : left i + right i = 2 * k
  · rw [if_pos htotal, derivativeFrequencyPolynomial_top_coefficient period _ _ k htotal]
  · have hlt : left i + right i < 2 * k := by have := hbound i; omega
    rw [if_neg htotal, derivativeFrequencyPolynomial_top_zero period _ _ k hlt, mul_zero]

/-- Mixed derivative terms on a genuine finite Fourier field give the
same scalar frequency polynomial, with the squared amplitude factors.
-/
theorem derivativePairing_cosineSum_frequencyPolynomial {N : ℕ}
    (period : ℝ) (hperiod : 0 < period) (mode : Fin N → ℕ)
    (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) (m n : ℕ) :
    derivativePairing period (periodicCosineSum period mode amplitude) m n =
      ∑ i, amplitude i ^ 2 * (derivativeFrequencyPolynomial period m n).eval
        (periodicFourierFrequency period (mode i) ^ 2) := by
  by_cases heven : Even (m + n)
  · obtain ⟨k, hk⟩ := heven
    have htotal : m + n = 2 * k := by omega
    have hhalf : (m + n) / 2 = k := by omega
    rw [derivativePairing_total_order period _
      (periodicCosineSum_smooth period mode amplitude)
      (periodicCosineSum_periodic period (ne_of_gt hperiod) mode amplitude) m n,
      htotal]
    unfold derivativePairing
    simp only [iteratedDeriv_zero]
    rw [periodicCosineSum_even_derivative,
      integral_periodicCosineSum_pair period hperiod mode hmode hinjective]
    simp only [derivativeFrequencyPolynomial, show Even (m + n) from ⟨k, hk⟩,
      ite_true, hhalf, Polynomial.eval_mul, Polynomial.eval_C,
      Polynomial.eval_pow, Polynomial.eval_X]
    simp_rw [← pow_mul]
    rw [Finset.mul_sum, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [pow_add]
    ring
  · have hodd : Odd (m + n) := by
      rcases Nat.even_or_odd (m + n) with h | h
      · exact (heven h).elim
      · exact h
    rw [derivativePairing_odd_total_zero period _
      (periodicCosineSum_smooth period mode amplitude)
      (periodicCosineSum_periodic period (ne_of_gt hperiod) mode amplitude) m n hodd]
    simp [derivativeFrequencyPolynomial, heven]

theorem integral_quadraticDerivativeDensity_cosineSum {ι : Type*} [Fintype ι] {N : ℕ}
    (period : ℝ) (hperiod : 0 < period) (mode : Fin N → ℕ)
    (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) (coefficient : ι → ℝ) (left right : ι → ℕ) :
    (∫ x in (0 : ℝ)..period, quadraticDerivativeDensity coefficient left right
      (periodicCosineSum period mode amplitude) x) =
      ∑ i, amplitude i ^ 2 * (quadraticFrequencyPolynomial period coefficient left right).eval
        (periodicFourierFrequency period (mode i) ^ 2) := by
  unfold quadraticDerivativeDensity
  rw [intervalIntegral.integral_finsetSum]
  · simp_rw [intervalIntegral.integral_const_mul]
    change (∑ a, coefficient a * derivativePairing period
        (periodicCosineSum period mode amplitude) (left a) (right a)) = _
    simp_rw [derivativePairing_cosineSum_frequencyPolynomial period hperiod mode
      hmode hinjective amplitude, Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro i _
    rw [quadraticFrequencyPolynomial_eval, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro a _
    ring
  · intro a _
    have hcont : Continuous (fun x : ℝ => coefficient a *
        (iteratedDeriv (left a) (periodicCosineSum period mode amplitude) x *
          iteratedDeriv (right a) (periodicCosineSum period mode amplitude) x)) :=
      continuous_const.mul
        (((periodicCosineSum_smooth period mode amplitude).continuous_iteratedDeriv (left a) (by simp)).mul
          ((periodicCosineSum_smooth period mode amplitude).continuous_iteratedDeriv (right a) (by simp)))
    exact hcont.intervalIntegrable 0 period

#print axioms derivativePairing_cosine_frequencyPolynomial
#print axioms quadraticFrequencyPolynomial_degree
#print axioms integral_quadraticDerivativeDensity_cosine
#print axioms quadraticFrequencyPolynomial_top_coefficient
#print axioms derivativePairing_cosineSum_frequencyPolynomial
#print axioms integral_quadraticDerivativeDensity_cosineSum
end
end DLWLean
