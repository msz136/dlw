import QuadraticFrequencyPolynomial

namespace DLWLean
noncomputable section

/-- A frequency polynomial is identified by the actual values on the
infinitely many positive periodic cosine frequencies. -/
theorem polynomial_eq_from_positive_fourier_values (period : ℝ) (hperiod : 0 < period)
    (p q : Polynomial ℝ)
    (hvalues : ∀ mode : ℕ, 0 < mode →
      p.eval (periodicFourierFrequency period mode ^ 2) =
        q.eval (periodicFourierFrequency period mode ^ 2)) : p = q := by
  apply Polynomial.eq_of_infinite_eval_eq
  have hinj : Function.Injective (fun mode : ℕ =>
      periodicFourierFrequency period (mode + 1) ^ 2) := by
    intro m n h
    have hm := periodicFourierFrequency_pos period hperiod (m + 1) (by omega)
    have hn := periodicFourierFrequency_pos period hperiod (n + 1) (by omega)
    have hfreq : periodicFourierFrequency period (m + 1) =
        periodicFourierFrequency period (n + 1) := by nlinarith
    have hmode := periodicFourierFrequency_injective period (ne_of_gt hperiod) hfreq
    omega
  apply (Set.infinite_range_of_injective hinj).mono
  rintro _ ⟨mode, rfl⟩
  exact hvalues (mode + 1) (by omega)

theorem polynomial_eq_monomial_from_positive_fourier_values
    (period : ℝ) (hperiod : 0 < period) (p : Polynomial ℝ) (top : ℝ) (k : ℕ)
    (hvalues : ∀ mode : ℕ, 0 < mode →
      p.eval (periodicFourierFrequency period mode ^ 2) =
        top * (periodicFourierFrequency period mode ^ 2) ^ k) :
    p = Polynomial.C top * Polynomial.X ^ k := by
  apply polynomial_eq_from_positive_fourier_values period hperiod
  intro mode hmode
  simpa only [Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_pow,
    Polynomial.eval_X] using hvalues mode hmode

#print axioms polynomial_eq_from_positive_fourier_values
#print axioms polynomial_eq_monomial_from_positive_fourier_values
end
end DLWLean
