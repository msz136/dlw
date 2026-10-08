import Mathlib.Algebra.MvPolynomial.Derivation
import Mathlib.RingTheory.MvPolynomial.WeightedHomogeneous
import Mathlib.RingTheory.Binomial
import Mathlib.Algebra.MvPolynomial.Polynomial
import Mathlib.Tactic

/-!
All-order balanced-slice normal coefficients in the genuine polynomial
algebra of B, eta and the spatial jets of every f_j. Coefficients are
constructed by finite normal-form recurrences; no target Hessian formula
or homogeneity of that formula is supplied as a premise.
-/

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

inductive JetVariable (M : ℕ) where
  | b : JetVariable M
  | eta : JetVariable M
  | field : Fin M → ℕ → JetVariable M
  deriving DecidableEq

abbrev Poly (M : ℕ) := MvPolynomial (JetVariable M) ℝ

def jetWeight (M : ℕ) : JetVariable M → ℤ
  | .b => 1
  | .eta => 1
  | .field _ k => (k : ℤ) + 1

def generatorDerivative (M : ℕ) : JetVariable M → Poly M
  | .b => 0
  | .eta => 0
  | .field j k => MvPolynomial.X (.field j (k + 1))

def spatialDerivative (M : ℕ) : Derivation ℝ (Poly M) (Poly M) :=
  MvPolynomial.mkDerivation ℝ (generatorDerivative M)

theorem generatorDerivative_homogeneous (M : ℕ) (i : JetVariable M) :
    (generatorDerivative M i).IsWeightedHomogeneous (jetWeight M) (jetWeight M i + 1) := by
  cases i with
  | b => exact MvPolynomial.isWeightedHomogeneous_zero _ _ _
  | eta => exact MvPolynomial.isWeightedHomogeneous_zero _ _ _
  | field j k =>
    convert MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M)
      (.field j (k + 1)) using 1 <;> simp [generatorDerivative, jetWeight]

theorem spatialDerivative_homogeneous (M : ℕ) (p : Poly M) (n : ℤ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) n) :
    (spatialDerivative M p).IsWeightedHomogeneous (jetWeight M) (n + 1) := by
  classical
  refine MvPolynomial.IsWeightedHomogeneous.induction_on
    (motive := fun p _ => (spatialDerivative M p).IsWeightedHomogeneous (jetWeight M) (n + 1))
    ?_ ?_ ?_ hp
  · rw [map_zero]
    exact MvPolynomial.isWeightedHomogeneous_zero _ _ _
  · intro p q _ _ hp hq
    rw [map_add]
    exact hp.add hq
  · intro s r hs
    rw [spatialDerivative, MvPolynomial.mkDerivation_monomial]
    simp only [Algebra.smul_def, MvPolynomial.algebraMap_eq, smul_eq_mul]
    apply MvPolynomial.IsWeightedHomogeneous.C_mul
    unfold Finsupp.sum
    apply MvPolynomial.IsWeightedHomogeneous.sum
    intro i hi
    have hsi : s i ≠ 0 := Finsupp.mem_support_iff.mp hi
    have hsub : Finsupp.weight (jetWeight M) (s - Finsupp.single i 1) = n - jetWeight M i := by
      have h := Finsupp.weight_sub_single_add (w := jetWeight M) hsi
      rw [hs] at h
      omega
    have hm := MvPolynomial.isWeightedHomogeneous_monomial (jetWeight M)
      (s - Finsupp.single i 1) (s i : ℝ) hsub
    convert hm.mul (generatorDerivative_homogeneous M i) using 1 <;> omega

def spatialIterate (M : ℕ) (k : ℕ) (p : Poly M) : Poly M :=
  (spatialDerivative M)^[k] p

theorem spatialIterate_homogeneous (M : ℕ) (p : Poly M) (n : ℤ) (k : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) n) :
    (spatialIterate M k p).IsWeightedHomogeneous (jetWeight M) (n + (k : ℤ)) := by
  induction k with
  | zero => simpa [spatialIterate] using hp
  | succ k ih =>
    simpa [spatialIterate, Function.iterate_succ_apply', Nat.cast_add, add_assoc] using
      spatialDerivative_homogeneous M _ _ ih

def balancedBeta (M : ℕ) (j : Fin M) : Poly M :=
  MvPolynomial.X .b + MvPolynomial.X (.field j 0) - MvPolynomial.X .eta

theorem balancedBeta_homogeneous (M : ℕ) (j : Fin M) :
    (balancedBeta M j).IsWeightedHomogeneous (jetWeight M) 1 := by
  unfold balancedBeta
  apply MvPolynomial.IsWeightedHomogeneous.sub
  · apply MvPolynomial.IsWeightedHomogeneous.add
    · exact MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M) .b
    · exact MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M) (.field j 0)
  · exact MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M) .eta

/-- The coefficients of (D-B-f_j+eta)^-1, determined by its left inverse
equation. This recurrence is finite and polynomial at every order. -/
def resolventCoefficient (M : ℕ) (j : Fin M) : ℕ → Poly M
  | 0 => 1
  | k + 1 => balancedBeta M j * resolventCoefficient M j k -
      spatialDerivative M (resolventCoefficient M j k)

theorem resolventCoefficient_homogeneous (M : ℕ) (j : Fin M) (k : ℕ) :
    (resolventCoefficient M j k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  induction k with
  | zero => exact MvPolynomial.isWeightedHomogeneous_one _ _
  | succ k ih =>
    rw [resolventCoefficient]
    apply MvPolynomial.IsWeightedHomogeneous.sub
    · convert (balancedBeta_homogeneous M j).mul ih using 1 <;> push_cast <;> ring
    · convert spatialDerivative_homogeneous M _ _ ih using 1 <;> push_cast <;> ring

/-- Coefficients of V_j=-2(D-B-f_j+eta)^-1; T_j=1+eta V_j. -/
def siteQuotientCoefficient (M : ℕ) (j : Fin M) (k : ℕ) : Poly M :=
  MvPolynomial.C (-2) * resolventCoefficient M j k

theorem siteQuotientCoefficient_homogeneous (M : ℕ) (j : Fin M) (k : ℕ) :
    (siteQuotientCoefficient M j k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) :=
  (resolventCoefficient_homogeneous M j k).C_mul _

/-- Literal normal-form product coefficient. The inputs have arbitrary
leading orders; only the left order enters the generalized binomial.
The output index k counts distance below the sum of the two orders. -/
def normalProduct (M : ℕ) (leftOrder : ℤ)
    (a b : ℕ → Poly M) (k : ℕ) : Poly M :=
  ∑ r : Fin (k + 1), ∑ s : Fin (k + 1),
    if r.val + s.val ≤ k then
      MvPolynomial.C ((Ring.choose (leftOrder - (r.val : ℤ))
        (k - (r.val + s.val)) : ℤ) : ℝ) * a r.val *
          spatialIterate M (k - (r.val + s.val)) (b s.val)
    else 0

theorem normalProduct_homogeneous (M : ℕ) (leftOrder : ℤ)
    (a b : ℕ → Poly M) (k : ℕ)
    (ha : ∀ r, (a r).IsWeightedHomogeneous (jetWeight M) (r : ℤ))
    (hb : ∀ s, (b s).IsWeightedHomogeneous (jetWeight M) (s : ℤ)) :
    (normalProduct M leftOrder a b k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  classical
  unfold normalProduct
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro r _
  apply MvPolynomial.IsWeightedHomogeneous.sum
  intro s _
  split_ifs with hrs
  · have hd := spatialIterate_homogeneous M (b s.val) (s.val : ℤ)
      (k - (r.val + s.val)) (hb s.val)
    convert ((ha r.val).C_mul _).mul hd using 1
    rw [Nat.cast_sub hrs]
    push_cast
    ring
  · exact MvPolynomial.isWeightedHomogeneous_zero _ _ _

/-- The regular quotient H=(monodromy-1)/eta constructed without eta
division. All terms of its product recurrence are polynomials. -/
def regularQuotientCoefficient (M : ℕ) (V : ℕ → ℕ → Poly M) : ℕ → ℕ → Poly M
  | 0, _ => 0
  | n + 1, 0 => V n 0 + regularQuotientCoefficient M V n 0
  | n + 1, k + 1 => V n (k + 1) + regularQuotientCoefficient M V n (k + 1) +
      MvPolynomial.X .eta *
        normalProduct M (-1) (V n) (regularQuotientCoefficient M V n) k

theorem regularQuotientCoefficient_homogeneous (M : ℕ) (V : ℕ → ℕ → Poly M)
    (hV : ∀ j k, (V j k).IsWeightedHomogeneous (jetWeight M) (k : ℤ))
    (n k : ℕ) :
    (regularQuotientCoefficient M V n k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  induction n generalizing k with
  | zero => exact MvPolynomial.isWeightedHomogeneous_zero _ _ _
  | succ n ih =>
    cases k with
    | zero => exact (hV n 0).add (ih 0)
    | succ k =>
      rw [regularQuotientCoefficient]
      apply MvPolynomial.IsWeightedHomogeneous.add
      · exact (hV n (k + 1)).add (ih (k + 1))
      · convert (MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M) .eta).mul
          (normalProduct_homogeneous M (-1) (V n)
            (regularQuotientCoefficient M V n) k (hV n) ih) using 1 <;>
          simp [jetWeight, Nat.cast_add, add_comm]

def balancedSites (M : ℕ) (n k : ℕ) : Poly M :=
  if hn : n < M then siteQuotientCoefficient M ⟨n, hn⟩ k else 0

theorem balancedSites_homogeneous (M n k : ℕ) :
    (balancedSites M n k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  unfold balancedSites
  split_ifs
  · exact siteQuotientCoefficient_homogeneous M _ k
  · exact MvPolynomial.isWeightedHomogeneous_zero _ _ _

def balancedQuotientCoefficient (M k : ℕ) : Poly M :=
  regularQuotientCoefficient M (balancedSites M) M k

theorem balancedQuotientCoefficient_homogeneous (M k : ℕ) :
    (balancedQuotientCoefficient M k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) :=
  regularQuotientCoefficient_homogeneous M (balancedSites M) (balancedSites_homogeneous M) M k

theorem regular_balanced_leading (M n : ℕ) (hn : n ≤ M) :
    regularQuotientCoefficient M (balancedSites M) n 0 = MvPolynomial.C (-2 * (n : ℝ)) := by
  induction n with
  | zero => simp [regularQuotientCoefficient]
  | succ n ih =>
    have hlt : n < M := by omega
    rw [regularQuotientCoefficient, ih (by omega)]
    simp [balancedSites, hlt, siteQuotientCoefficient, resolventCoefficient, ← map_add]
    congr 1
    push_cast
    ring

theorem balancedQuotientCoefficient_leading (M : ℕ) :
    balancedQuotientCoefficient M 0 = MvPolynomial.C (-2 * (M : ℝ)) :=
  regular_balanced_leading M M le_rfl

/-- Inverse of an order-minus-one series with fixed leading coefficient.
`a0` is its scalar reciprocal. The next coefficient is obtained by
removing the already isolated leading times new-coefficient term from
the literal normal product. Only finite earlier coefficients occur. -/
def inverseCoefficient (M : ℕ) (H : ℕ → Poly M) (a0 : ℝ) : ℕ → Poly M
  | 0 => MvPolynomial.C a0
  | n + 1 =>
      MvPolynomial.C (-a0) *
        ∑ s : Fin (n + 1), ∑ r : Fin (n + 2),
          if r.val + s.val ≤ n + 1 then
            MvPolynomial.C ((Ring.choose (-1 - (r.val : ℤ))
              (n + 1 - (r.val + s.val)) : ℤ) : ℝ) * H r.val *
                spatialIterate M (n + 1 - (r.val + s.val))
                  (inverseCoefficient M H a0 s.val)
          else 0
termination_by k => k
decreasing_by exact s.isLt

theorem inverseCoefficient_homogeneous (M : ℕ) (H : ℕ → Poly M) (a0 : ℝ)
    (hH : ∀ r, (H r).IsWeightedHomogeneous (jetWeight M) (r : ℤ)) (k : ℕ) :
    (inverseCoefficient M H a0 k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  classical
  induction k using Nat.strong_induction_on with
  | h k ih =>
    cases k with
    | zero =>
      rw [inverseCoefficient]
      exact MvPolynomial.isWeightedHomogeneous_C (jetWeight M) a0
    | succ n =>
      rw [inverseCoefficient]
      apply MvPolynomial.IsWeightedHomogeneous.C_mul
      apply MvPolynomial.IsWeightedHomogeneous.sum
      intro s _
      apply MvPolynomial.IsWeightedHomogeneous.sum
      intro r _
      split_ifs with hrs
      · have hd := spatialIterate_homogeneous M (inverseCoefficient M H a0 s.val)
          (s.val : ℤ) (n + 1 - (r.val + s.val)) (ih s.val s.isLt)
        convert ((hH r.val).C_mul _).mul hd using 1
        rw [Nat.cast_sub hrs]
        push_cast
        ring
      · exact MvPolynomial.isWeightedHomogeneous_zero _ _ _

/-- Every coefficient of the actual regular eta-normalization is a
polynomial: the inverse divides by -2N, never by eta. The index k is the
distance below order one, so ell_j is coefficient j+1. -/
def normalizedCoefficient (M : ℕ) (N : ℝ) (H : ℕ → Poly M) (k : ℕ) : Poly M :=
  MvPolynomial.C (-2 * N) * inverseCoefficient M H (-2 * N)⁻¹ k +
    if k = 1 then MvPolynomial.X .b - MvPolynomial.C N * MvPolynomial.X .eta else 0

theorem normalizedCoefficient_homogeneous (M : ℕ) (N : ℝ) (H : ℕ → Poly M)
    (hH : ∀ r, (H r).IsWeightedHomogeneous (jetWeight M) (r : ℤ)) (k : ℕ) :
    (normalizedCoefficient M N H k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  classical
  unfold normalizedCoefficient
  apply MvPolynomial.IsWeightedHomogeneous.add
  · exact (inverseCoefficient_homogeneous M H _ hH k).C_mul _
  · split_ifs with hk
    · subst k
      exact (MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M) .b).sub
        ((MvPolynomial.isWeightedHomogeneous_X (R := ℝ) (jetWeight M) .eta).C_mul N)
    · exact MvPolynomial.isWeightedHomogeneous_zero _ _ _

def balancedNormalizedCoefficient (M k : ℕ) : Poly M :=
  normalizedCoefficient M (M : ℝ) (balancedQuotientCoefficient M) k

theorem balancedNormalizedCoefficient_homogeneous (M k : ℕ) :
    (balancedNormalizedCoefficient M k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) :=
  normalizedCoefficient_homogeneous M (M : ℝ) (balancedQuotientCoefficient M)
    (balancedQuotientCoefficient_homogeneous M) k

theorem balancedNormalizedCoefficient_leading (M : ℕ) (hM : M ≠ 0) :
    balancedNormalizedCoefficient M 0 = 1 := by
  have hMr : (M : ℝ) ≠ 0 := by exact_mod_cast hM
  unfold balancedNormalizedCoefficient normalizedCoefficient
  rw [inverseCoefficient]
  simp only [Nat.zero_ne_one, ite_false, add_zero, ← map_mul]
  rw [mul_inv_cancel₀ (mul_ne_zero (by norm_num : (-2 : ℝ) ≠ 0) hMr)]
  exact map_one _

/-- Finite normal-form recurrence for every coefficient of the n-th
power of an order-one polynomial symbol. -/
def powerCoefficient (M : ℕ) (L : ℕ → Poly M) : ℕ → ℕ → Poly M
  | 0, k => if k = 0 then 1 else 0
  | n + 1, k => normalProduct M (n : ℤ) (powerCoefficient M L n) L k

theorem powerCoefficient_homogeneous (M : ℕ) (L : ℕ → Poly M)
    (hL : ∀ r, (L r).IsWeightedHomogeneous (jetWeight M) (r : ℤ)) (n k : ℕ) :
    (powerCoefficient M L n k).IsWeightedHomogeneous (jetWeight M) (k : ℤ) := by
  induction n generalizing k with
  | zero =>
    unfold powerCoefficient
    split_ifs with hk
    · subst k
      exact MvPolynomial.isWeightedHomogeneous_one _ _
    · exact MvPolynomial.isWeightedHomogeneous_zero _ _ _
  | succ n ih =>
    exact normalProduct_homogeneous M (n : ℤ) (powerCoefficient M L n) L k ih hL

def balancedResiduePolynomial (M n : ℕ) : Poly M :=
  powerCoefficient M (balancedNormalizedCoefficient M) n (n + 1)

/-- All-order polynomial homogeneity of the actual balanced recurrence
residue. In particular n=2k+1 has total weight 2k+2. -/
theorem balancedResiduePolynomial_homogeneous (M n : ℕ) :
    (balancedResiduePolynomial M n).IsWeightedHomogeneous (jetWeight M) ((n : ℤ) + 1) := by
  simpa [balancedResiduePolynomial] using
    powerCoefficient_homogeneous M (balancedNormalizedCoefficient M)
      (balancedNormalizedCoefficient_homogeneous M) n (n + 1)

def parameterWeight (M : ℕ) : JetVariable M → ℕ
  | .b => 1
  | .eta => 1
  | .field _ _ => 0

def fieldWeight (M : ℕ) : JetVariable M → ℕ
  | .b => 0
  | .eta => 0
  | .field _ _ => 1

def derivativeWeight (M : ℕ) : JetVariable M → ℕ
  | .b => 0
  | .eta => 0
  | .field _ k => k

def parameterDegree {M : ℕ} (s : JetVariable M →₀ ℕ) : ℕ :=
  Finsupp.weight (parameterWeight M) s

def fieldDegree {M : ℕ} (s : JetVariable M →₀ ℕ) : ℕ :=
  Finsupp.weight (fieldWeight M) s

def derivativeOrder {M : ℕ} (s : JetVariable M →₀ ℕ) : ℕ :=
  Finsupp.weight (derivativeWeight M) s

theorem monomial_weight_decomposition {M : ℕ} (s : JetVariable M →₀ ℕ) :
    Finsupp.weight (jetWeight M) s =
      (parameterDegree s : ℤ) + (fieldDegree s : ℤ) + (derivativeOrder s : ℤ) := by
  classical
  simp only [parameterDegree, fieldDegree, derivativeOrder,
    Finsupp.weight_apply, Finsupp.sum, nsmul_eq_mul]
  push_cast
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro i _
  cases i <;> simp [jetWeight, parameterWeight, fieldWeight, derivativeWeight] <;> ring

/-- The parameter exponents are absent from maximal-order quadratic
monomials in a homogeneous density. The field support may involve any
sites; a later balanced f,-f restriction preserves this fact. -/
theorem top_quadratic_parameters_absent {M : ℕ} (p : Poly M) (K : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) ((K : ℤ) + 2))
    (s : JetVariable M →₀ ℕ) (hs : s ∈ p.support)
    (hfield : fieldDegree s = 2) (hderivative : derivativeOrder s = K) :
    s .b = 0 ∧ s .eta = 0 := by
  have hw := hp (MvPolynomial.mem_support_iff.mp hs)
  rw [monomial_weight_decomposition, hfield, hderivative] at hw
  have hparam : parameterDegree s = 0 := by omega
  have hb := Finsupp.le_weight (parameterWeight M) (s := JetVariable.b)
    (by simp [parameterWeight] : parameterWeight M .b ≠ 0) s
  have he := Finsupp.le_weight (parameterWeight M) (s := JetVariable.eta)
    (by simp [parameterWeight] : parameterWeight M .eta ≠ 0) s
  change s .b ≤ parameterDegree s at hb
  change s .eta ≤ parameterDegree s at he
  omega

theorem balancedOddResidue_top_parameters_absent (M k : ℕ)
    (s : JetVariable M →₀ ℕ) (hs : s ∈ (balancedResiduePolynomial M (2 * k + 1)).support)
    (hfield : fieldDegree s = 2) (hderivative : derivativeOrder s = 2 * k) :
    s .b = 0 ∧ s .eta = 0 := by
  apply top_quadratic_parameters_absent _ (2 * k) _ s hs hfield hderivative
  convert balancedResiduePolynomial_homogeneous M (2 * k + 1) using 1 <;> push_cast <;> ring

def jetValue (M : ℕ) (B eta : ℝ) (field : Fin M → ℕ → ℝ) : JetVariable M → ℝ
  | .b => B
  | .eta => eta
  | .field j k => field j k

def topQuadraticPart (M : ℕ) (p : Poly M) (K : ℕ) : Poly M :=
  ∑ s ∈ p.support,
    if fieldDegree s = 2 ∧ derivativeOrder s = K then MvPolynomial.monomial s (p.coeff s) else 0

theorem monomial_eval_parameter_independent (M : ℕ) (s : JetVariable M →₀ ℕ) (r : ℝ)
    (hB : s .b = 0) (heta : s .eta = 0)
    (B eta : ℝ) (field : Fin M → ℕ → ℝ) :
    MvPolynomial.eval (jetValue M B eta field) (MvPolynomial.monomial s r) =
      MvPolynomial.eval (jetValue M 0 0 field) (MvPolynomial.monomial s r) := by
  classical
  simp only [MvPolynomial.eval_monomial, Finsupp.prod]
  congr 1
  apply Finset.prod_congr rfl
  intro i _
  cases i with
  | b => simp [jetValue, hB]
  | eta => simp [jetValue, heta]
  | field j k => rfl

/-- Parameter independence of the actual finite maximal-derivative
quadratic projection, derived from recurrence homogeneity. -/
theorem topQuadraticPart_parameter_independent {M : ℕ} (p : Poly M) (K : ℕ)
    (hp : p.IsWeightedHomogeneous (jetWeight M) ((K : ℤ) + 2))
    (B eta : ℝ) (field : Fin M → ℕ → ℝ) :
    MvPolynomial.eval (jetValue M B eta field) (topQuadraticPart M p K) =
      MvPolynomial.eval (jetValue M 0 0 field) (topQuadraticPart M p K) := by
  classical
  unfold topQuadraticPart
  rw [map_sum, map_sum]
  apply Finset.sum_congr rfl
  intro s hs
  split_ifs with h
  · obtain ⟨hB, heta⟩ := top_quadratic_parameters_absent p K hp s hs h.1 h.2
    exact monomial_eval_parameter_independent M s (p.coeff s) hB heta B eta field
  · rw [map_zero, map_zero]

theorem balancedOddResidue_top_parameter_independent (M k : ℕ)
    (B eta : ℝ) (field : Fin M → ℕ → ℝ) :
    MvPolynomial.eval (jetValue M B eta field)
        (topQuadraticPart M (balancedResiduePolynomial M (2 * k + 1)) (2 * k)) =
      MvPolynomial.eval (jetValue M 0 0 field)
        (topQuadraticPart M (balancedResiduePolynomial M (2 * k + 1)) (2 * k)) := by
  apply topQuadraticPart_parameter_independent _ (2 * k) _ B eta field
  convert balancedResiduePolynomial_homogeneous M (2 * k + 1) using 1 <;> push_cast <;> ring

def balancedSpectralDensityPolynomial (M n : ℕ) : Poly M :=
  MvPolynomial.C (n : ℝ)⁻¹ * balancedResiduePolynomial M n

theorem balancedSpectralDensityPolynomial_homogeneous (M n : ℕ) :
    (balancedSpectralDensityPolynomial M n).IsWeightedHomogeneous (jetWeight M) ((n : ℤ) + 1) :=
  (balancedResiduePolynomial_homogeneous M n).C_mul _

def perturbationVariable (M : ℕ) (B eta : ℝ) (field : Fin M → ℕ → ℝ) :
    JetVariable M → Polynomial ℝ
  | .b => Polynomial.C B
  | .eta => Polynomial.C eta
  | .field j k => Polynomial.C (field j k) * Polynomial.X

/-- A real polynomial in the actual perturbation amplitude is
constructed from any normal-form coefficient polynomial. -/
def perturbationPolynomial (M : ℕ) (p : Poly M) (B eta : ℝ)
    (field : Fin M → ℕ → ℝ) : Polynomial ℝ :=
  MvPolynomial.eval₂ Polynomial.C (perturbationVariable M B eta field) p

theorem perturbationPolynomial_eval (M : ℕ) (p : Poly M) (B eta eps : ℝ)
    (field : Fin M → ℕ → ℝ) :
    (perturbationPolynomial M p B eta field).eval eps =
      MvPolynomial.eval (jetValue M B eta (fun j k => eps * field j k)) p := by
  unfold perturbationPolynomial
  rw [MvPolynomial.polynomial_eval_eval₂]
  have hc : (Polynomial.evalRingHom eps).comp Polynomial.C = RingHom.id ℝ := by
    ext r
    simp
  have hv : (fun i => Polynomial.eval eps (perturbationVariable M B eta field i)) =
      jetValue M B eta (fun j k => eps * field j k) := by
    funext i
    cases i <;> simp only [perturbationVariable, jetValue,
      Polynomial.eval_mul, Polynomial.eval_C, Polynomial.eval_X] <;> ring
  rw [hc, hv]
  rfl

#print axioms spatialDerivative_homogeneous
#print axioms resolventCoefficient_homogeneous
#print axioms balancedQuotientCoefficient_homogeneous
#print axioms balancedQuotientCoefficient_leading
#print axioms inverseCoefficient_homogeneous
#print axioms balancedNormalizedCoefficient_homogeneous
#print axioms balancedResiduePolynomial_homogeneous
#print axioms balancedOddResidue_top_parameters_absent
#print axioms balancedOddResidue_top_parameter_independent
#print axioms perturbationPolynomial_eval

end
end DLWLean.BalancedPDO
