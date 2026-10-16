import BalancedCoefficientRecurrence

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

theorem perturbationVariable_factor (M : ℕ) (B eta : ℝ)
    (field : Fin M → ℕ → ℝ) (i : JetVariable M) :
    perturbationVariable M B eta field i =
      Polynomial.C (jetValue M B eta field i) * Polynomial.X ^ (fieldWeight M i) := by
  cases i <;> simp [perturbationVariable, jetValue, fieldWeight]

/-- Literal epsilon substitution on one monomial records exactly its
field degree as its epsilon exponent, with actual parameter/jet value.
-/
theorem perturbationPolynomial_monomial (M : ℕ) (s : JetVariable M →₀ ℕ) (r B eta : ℝ)
    (field : Fin M → ℕ → ℝ) :
    perturbationPolynomial M (MvPolynomial.monomial s r) B eta field =
      Polynomial.C (MvPolynomial.eval (jetValue M B eta field) (MvPolynomial.monomial s r)) *
        Polynomial.X ^ fieldDegree s := by
  classical
  unfold perturbationPolynomial
  rw [MvPolynomial.eval₂_monomial, MvPolynomial.eval_monomial]
  simp only [Finsupp.prod, perturbationVariable_factor, mul_pow, ← Polynomial.C_pow,
    Finset.prod_mul_distrib, ← map_prod, ← pow_mul,
    Finset.prod_pow_eq_pow_sum, ← Polynomial.C_mul, ← mul_assoc]
  congr 1
  congr 1
  simp only [fieldDegree, Finsupp.weight_apply, Finsupp.sum, nsmul_eq_mul, Nat.mul_comm, Nat.cast_id]

theorem perturbationPolynomial_monomial_coefficient (M : ℕ)
    (s : JetVariable M →₀ ℕ) (r B eta : ℝ) (field : Fin M → ℕ → ℝ) (q : ℕ) :
    (perturbationPolynomial M (MvPolynomial.monomial s r) B eta field).coeff q =
      if fieldDegree s = q then
        MvPolynomial.eval (jetValue M B eta field) (MvPolynomial.monomial s r) else 0 := by
  rw [perturbationPolynomial_monomial, Polynomial.coeff_C_mul, Polynomial.coeff_X_pow]
  split_ifs <;> simp_all

def fieldDegreePart (M : ℕ) (p : Poly M) (q : ℕ) : Poly M :=
  ∑ s ∈ p.support, if fieldDegree s = q then MvPolynomial.monomial s (p.coeff s) else 0

/-- The actual epsilon coefficient is the evaluated finite field-degree
projection. In particular q=2 is the true quadratic amplitude density.
-/
theorem perturbationPolynomial_coefficient (M : ℕ) (p : Poly M) (B eta : ℝ)
    (field : Fin M → ℕ → ℝ) (q : ℕ) :
    (perturbationPolynomial M p B eta field).coeff q =
      MvPolynomial.eval (jetValue M B eta field) (fieldDegreePart M p q) := by
  classical
  conv_lhs => rw [MvPolynomial.as_sum p]
  unfold perturbationPolynomial fieldDegreePart
  rw [MvPolynomial.eval₂_sum, Polynomial.finsetSum_coeff, map_sum]
  apply Finset.sum_congr rfl
  intro s _
  change (perturbationPolynomial M (MvPolynomial.monomial s (p.coeff s)) B eta field).coeff q = _
  rw [perturbationPolynomial_monomial_coefficient]
  split_ifs <;> simp only [map_zero]

theorem quadratic_support_derivative_bound {M : ℕ} (p : Poly M) (K : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) ((K : ℤ) + 2))
    (s : JetVariable M →₀ ℕ) (hs : s ∈ p.support) (hq : fieldDegree s = 2) :
    derivativeOrder s ≤ K := by
  have hw := hp (MvPolynomial.mem_support_iff.mp hs)
  rw [monomial_weight_decomposition, hq] at hw
  omega

theorem odd_quadratic_support_derivative_bound (M k : ℕ)
    (s : JetVariable M →₀ ℕ) (hs : s ∈ (balancedSpectralDensityPolynomial M (2 * k + 1)).support)
    (hq : fieldDegree s = 2) : derivativeOrder s ≤ 2 * k := by
  apply quadratic_support_derivative_bound _ (2 * k) _ s hs hq
  convert balancedSpectralDensityPolynomial_homogeneous M (2 * k + 1) using 1 <;>
    push_cast <;> ring

#print axioms perturbationPolynomial_monomial
#print axioms perturbationPolynomial_coefficient
#print axioms odd_quadratic_support_derivative_bound
end
end DLWLean.BalancedPDO
