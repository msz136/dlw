import QuadraticMonomialDecomposition
import QuadraticFrequencyPolynomial

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators ContDiff

structure QuadraticDescription {M : ℕ} (s : JetVariable M →₀ ℕ) where
  j : Fin M
  l : Fin M
  m : ℕ
  n : ℕ
  split : s = Finsupp.single .b (s .b) + Finsupp.single .eta (s .eta) +
    Finsupp.single (.field j m) 1 + Finsupp.single (.field l n) 1

def quadraticDescription {M : ℕ} (s : JetVariable M →₀ ℕ)
    (hq : fieldDegree s = 2) : QuadraticDescription s :=
  Classical.choice (by
    obtain ⟨j, l, m, n, hs⟩ := quadratic_exponent_decomposition s hq
    exact ⟨⟨j, l, m, n, hs⟩⟩)

def quadraticSupport {M : ℕ} (p : Poly M) : Finset (JetVariable M →₀ ℕ) :=
  p.support.filter (fun s => fieldDegree s = 2)

def quadraticTermDescription {M : ℕ} (p : Poly M) (i : ↥(quadraticSupport p)) :
    QuadraticDescription i.val :=
  quadraticDescription i.val (Finset.mem_filter.mp i.property).2

def quadraticLeft {M : ℕ} (p : Poly M) (i : ↥(quadraticSupport p)) : ℕ :=
  (quadraticTermDescription p i).m

def quadraticRight {M : ℕ} (p : Poly M) (i : ↥(quadraticSupport p)) : ℕ :=
  (quadraticTermDescription p i).n

def quadraticScalar {M : ℕ} (p : Poly M) (B eta : ℝ) (sign : Fin M → ℝ)
    (i : ↥(quadraticSupport p)) : ℝ :=
  p.coeff i.val * B ^ (i.val .b) * eta ^ (i.val .eta) *
    sign (quadraticTermDescription p i).j * sign (quadraticTermDescription p i).l

def balancedQuadraticFrequencyPolynomial {M : ℕ} (p : Poly M) (period B eta : ℝ)
    (sign : Fin M → ℝ) : Polynomial ℝ :=
  quadraticFrequencyPolynomial period (quadraticScalar p B eta sign)
    (quadraticLeft p) (quadraticRight p)

theorem fieldDegreePart_eval_quadratic {M : ℕ} (p : Poly M) (B eta : ℝ)
    (field : Fin M → ℕ → ℝ) :
    MvPolynomial.eval (jetValue M B eta field) (fieldDegreePart M p 2) =
      ∑ i : ↥(quadraticSupport p),
        MvPolynomial.eval (jetValue M B eta field) (MvPolynomial.monomial i.val (p.coeff i.val)) := by
  classical
  unfold fieldDegreePart
  rw [map_sum]
  simp only [apply_ite, map_zero]
  rw [← Finset.sum_filter]
  exact (Finset.sum_coe_sort (quadraticSupport p) _).symm

theorem quadraticAmplitude_density {M : ℕ} (p : Poly M) (B eta : ℝ)
    (sign : Fin M → ℝ) (f : ℝ → ℝ) (x : ℝ) :
    (perturbationPolynomial M p B eta
      (fun j k => sign j * iteratedDeriv k f x)).coeff 2 =
      quadraticDerivativeDensity (quadraticScalar p B eta sign)
        (quadraticLeft p) (quadraticRight p) f x := by
  classical
  rw [perturbationPolynomial_coefficient, fieldDegreePart_eval_quadratic]
  unfold quadraticDerivativeDensity
  apply Finset.sum_congr rfl
  intro i _
  rw [monomial_value_quadratic_split i.val _ _ _ _
    (quadraticTermDescription p i).split]
  unfold quadraticScalar quadraticLeft quadraticRight
  ring

theorem balancedQuadraticFrequencyPolynomial_degree {M : ℕ} (p : Poly M)
    (period B eta : ℝ) (sign : Fin M → ℝ) (k : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) ((2 * k : ℤ) + 2)) :
    (balancedQuadraticFrequencyPolynomial p period B eta sign).natDegree ≤ k := by
  apply quadraticFrequencyPolynomial_degree
  intro i
  have hs := Finset.mem_filter.mp i.property
  have horder := quadratic_support_derivative_bound p (2 * k) hp i.val hs.1 hs.2
  rw [derivativeOrder_quadratic_split i.val _ _ _ _
    (quadraticTermDescription p i).split] at horder
  exact horder

theorem quadraticScalar_top_parameter_independent {M : ℕ} (p : Poly M)
    (B eta : ℝ) (sign : Fin M → ℝ) (k : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) ((2 * k : ℤ) + 2))
    (i : ↥(quadraticSupport p))
    (htop : quadraticLeft p i + quadraticRight p i = 2 * k) :
    quadraticScalar p B eta sign i = quadraticScalar p 0 0 sign i := by
  have hs := Finset.mem_filter.mp i.property
  have horder : derivativeOrder i.val = 2 * k :=
    (derivativeOrder_quadratic_split i.val _ _ _ _
      (quadraticTermDescription p i).split).trans htop
  obtain ⟨hb, he⟩ := top_quadratic_parameters_absent p (2 * k) hp i.val hs.1 hs.2 horder
  simp only [quadraticScalar, hb, he, pow_zero]

theorem balancedQuadraticFrequencyPolynomial_top_parameter_independent {M : ℕ} (p : Poly M)
    (period B eta : ℝ) (sign : Fin M → ℝ) (k : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) ((2 * k : ℤ) + 2)) :
    (balancedQuadraticFrequencyPolynomial p period B eta sign).coeff k =
      (balancedQuadraticFrequencyPolynomial p period 0 0 sign).coeff k := by
  have hbound (i : ↥(quadraticSupport p)) : quadraticLeft p i + quadraticRight p i ≤ 2 * k := by
    have hs := Finset.mem_filter.mp i.property
    have horder := quadratic_support_derivative_bound p (2 * k) hp i.val hs.1 hs.2
    rw [derivativeOrder_quadratic_split i.val _ _ _ _
      (quadraticTermDescription p i).split] at horder
    exact horder
  unfold balancedQuadraticFrequencyPolynomial
  rw [quadraticFrequencyPolynomial_top_coefficient _ _ _ _ _ hbound,
    quadraticFrequencyPolynomial_top_coefficient _ _ _ _ _ hbound]
  apply Finset.sum_congr rfl
  intro i _
  split_ifs with htop
  · rw [quadraticScalar_top_parameter_independent p B eta sign k hp i htop]
  · rfl

theorem integral_quadraticAmplitude_cosineSum {M N : ℕ} (p : Poly M)
    (period : ℝ) (hperiod : 0 < period) (B eta : ℝ) (sign : Fin M → ℝ)
    (mode : Fin N → ℕ) (hmode : ∀ i, 0 < mode i) (hinjective : Function.Injective mode)
    (amplitude : Fin N → ℝ) :
    (∫ x in (0 : ℝ)..period,
      (perturbationPolynomial M p B eta (fun j k => sign j *
        iteratedDeriv k (periodicCosineSum period mode amplitude) x)).coeff 2) =
      ∑ i, amplitude i ^ 2 *
        (balancedQuadraticFrequencyPolynomial p period B eta sign).eval
          (periodicFourierFrequency period (mode i) ^ 2) := by
  simp_rw [quadraticAmplitude_density]
  exact integral_quadraticDerivativeDensity_cosineSum period hperiod mode hmode hinjective
    amplitude (quadraticScalar p B eta sign) (quadraticLeft p) (quadraticRight p)

theorem integral_quadraticAmplitude_cosine {M : ℕ} (p : Poly M)
    (period : ℝ) (hperiod : 0 < period) (B eta : ℝ) (sign : Fin M → ℝ)
    (mode : ℕ) (hmode : 0 < mode) :
    (∫ x in (0 : ℝ)..period,
      (perturbationPolynomial M p B eta (fun j k => sign j *
        iteratedDeriv k (periodicCosine period mode) x)).coeff 2) =
      (balancedQuadraticFrequencyPolynomial p period B eta sign).eval
        (periodicFourierFrequency period mode ^ 2) := by
  simp_rw [quadraticAmplitude_density]
  exact integral_quadraticDerivativeDensity_cosine period hperiod mode hmode
    (quadraticScalar p B eta sign) (quadraticLeft p) (quadraticRight p)

#print axioms quadraticAmplitude_density
#print axioms balancedQuadraticFrequencyPolynomial_degree
#print axioms balancedQuadraticFrequencyPolynomial_top_parameter_independent
#print axioms integral_quadraticAmplitude_cosineSum
end
end DLWLean.BalancedPDO
