import QuadraticResolvent
import Mathlib.Algebra.BigOperators.GroupWithZero.Action

/-!
The finite transfer product at eta=0. Differentiating the regular quotient
identity determines its value; no monodromy derivative formula is assumed.
Existence of that quotient as a unit is kept explicit.
-/
namespace DLWLean
noncomputable section

variable {A B : Type*} [Ring A] [Algebra ℝ A] [Ring B] [Algebra ℝ B]

/-- `(a+eta)^(-1)(a-eta)` written without a second factor inverse. -/
def etaTransfer (denominator : Aˣ) (eta : A) : A :=
  (↑denominator⁻¹ : A) * ((denominator : A) - (2 : ℝ) • eta)

theorem etaTransfer_value (j : AlgebraJet2 A B) (denominator : Aˣ)
    (eta : A) (heta : j.value eta = 0) :
    j.value (etaTransfer denominator eta) = 1 := by
  simp only [etaTransfer, map_mul, map_sub, map_smul, heta, smul_zero, sub_zero]
  rw [← map_mul, Units.inv_mul, map_one]

theorem etaTransfer_first (j : AlgebraJet2 A B) (denominator : Aˣ)
    (eta : A) (heta : j.value eta = 0) (hfirsteta : j.first eta = 1) :
    j.first (etaTransfer denominator eta) =
      (-2 : ℝ) • j.value (↑denominator⁻¹ : A) := by
  simp only [etaTransfer, j.first_mul, map_sub, map_smul, heta,
    smul_zero, sub_zero, hfirsteta]
  rw [j.first_inverse]
  have hinverse : j.value (↑denominator⁻¹ : A) * j.value (denominator : A) = 1 := by
    rw [← map_mul, Units.inv_mul, map_one]
  simp only [mul_sub, neg_mul, mul_assoc, hinverse, mul_one,
    Algebra.mul_smul_comm, mul_one]
  simp only [neg_smul]
  abel

theorem transferProduct_value_one (j : AlgebraJet2 A B) (T : ℕ → A)
    (N : ℕ) (hvalue : ∀ i < N, j.value (T i) = 1) :
    j.value (transferProduct T N) = 1 := by
  induction N with
  | zero => simp [transferProduct]
  | succ N ih =>
    rw [transferProduct, map_mul, hvalue N (Nat.lt_succ_self N)]
    simp only [one_mul]
    exact ih (fun i hi => hvalue i (Nat.lt_succ_of_lt hi))

/-- At identity-valued factors, order drops out of the first variation. -/
theorem transferProduct_first_at_identity (j : AlgebraJet2 A B) (T : ℕ → A)
    (N : ℕ) (hvalue : ∀ i < N, j.value (T i) = 1) :
    j.first (transferProduct T N) = ∑ i ∈ Finset.range N, j.first (T i) := by
  induction N with
  | zero => simp [transferProduct, j.first_one]
  | succ N ih =>
    have hprefix : ∀ i < N, j.value (T i) = 1 :=
      fun i hi => hvalue i (Nat.lt_succ_of_lt hi)
    rw [transferProduct, j.first_mul,
      transferProduct_value_one j T N hprefix, hvalue N (Nat.lt_succ_self N),
      mul_one, one_mul, ih hprefix, Finset.sum_range_succ]
    abel

theorem etaMonodromy_first (j : AlgebraJet2 A B) (denominator : ℕ → Aˣ)
    (eta : A) (heta : j.value eta = 0) (hfirsteta : j.first eta = 1) (N : ℕ) :
    j.first (transferProduct (fun i => etaTransfer (denominator i) eta) N) =
      (-2 : ℝ) • (∑ i ∈ Finset.range N, j.value (↑(denominator i)⁻¹ : A)) := by
  rw [transferProduct_first_at_identity j _ N
    (fun i _ => etaTransfer_value j (denominator i) eta heta)]
  simp only [etaTransfer_first j _ eta heta hfirsteta, Finset.smul_sum]

/-- A finite, polynomial expression for the quotient of an ordered product
of `1 + eta * V_j` by eta. This avoids division at eta=0. -/
def affineParameterQuotient (V : ℕ → A) (eta : A) : ℕ → A
  | 0 => 0
  | n + 1 => V n + affineParameterQuotient V eta n +
      eta * V n * affineParameterQuotient V eta n

theorem affineParameterProduct_factor (V : ℕ → A) (eta : A) (N : ℕ)
    (hcentral : ∀ i < N, Commute eta (V i)) :
    transferProduct (fun i => 1 + eta * V i) N =
      1 + eta * affineParameterQuotient V eta N := by
  induction N with
  | zero => simp [transferProduct, affineParameterQuotient]
  | succ N ih =>
    rw [transferProduct, ih (fun i hi => hcentral i (Nat.lt_succ_of_lt hi)),
      affineParameterQuotient]
    have hc := (hcentral N (Nat.lt_succ_self N)).eq
    have hcross : eta * V N * (eta * affineParameterQuotient V eta N) =
        eta * (eta * V N * affineParameterQuotient V eta N) := by
      rw [mul_assoc eta (V N), ← mul_assoc (V N), ← hc]
    simp only [mul_add, add_mul, one_mul, mul_one]
    rw [hcross]
    abel

theorem etaTransfer_eq_affine (denominator : Aˣ) (eta : A)
    (hcentral : Commute eta (↑denominator⁻¹ : A)) :
    etaTransfer denominator eta =
      1 + eta * ((-2 : ℝ) • (↑denominator⁻¹ : A)) := by
  have hc := hcentral.eq
  rw [etaTransfer, mul_sub, Units.inv_mul]
  simp only [Algebra.mul_smul_comm, ← hc, neg_smul, mul_neg]
  abel

/-- Explicit regular quotient for the actual eta transfer factors. -/
def etaMonodromyQuotient (denominator : ℕ → Aˣ) (eta : A) (N : ℕ) : A :=
  affineParameterQuotient (fun i => (-2 : ℝ) • (↑(denominator i)⁻¹ : A)) eta N

theorem etaMonodromyQuotient_factor (denominator : ℕ → Aˣ)
    (eta : A) (N : ℕ)
    (hcentral : ∀ i < N, Commute eta (↑(denominator i)⁻¹ : A)) :
    transferProduct (fun i => etaTransfer (denominator i) eta) N - 1 =
      eta * etaMonodromyQuotient denominator eta N := by
  have hfactor : transferProduct (fun i => etaTransfer (denominator i) eta) N =
      transferProduct (fun i => 1 +
        eta * ((-2 : ℝ) • (↑(denominator i)⁻¹ : A))) N := by
    induction N with
    | zero => rfl
    | succ N ih =>
      rw [transferProduct, transferProduct,
        etaTransfer_eq_affine (denominator N) eta (hcentral N (Nat.lt_succ_self N)),
        ih (fun i hi => hcentral i (Nat.lt_succ_of_lt hi))]
  have hcommute : ∀ i < N,
      Commute eta ((-2 : ℝ) • (↑(denominator i)⁻¹ : A)) := by
    intro i hi
    show eta * ((-2 : ℝ) • (↑(denominator i)⁻¹ : A)) =
      ((-2 : ℝ) • (↑(denominator i)⁻¹ : A)) * eta
    simp only [Algebra.mul_smul_comm, Algebra.smul_mul_assoc]
    rw [(hcentral i hi).eq]
  rw [hfactor, affineParameterProduct_factor _ eta N hcommute]
  simp only [etaMonodromyQuotient, add_sub_cancel_left]

/-- A regular quotient Q=(monodromy-1)/eta has the forced value
`-2 sum a_j^(-1)`; the quotient existence itself is not assumed away. -/
theorem regularEtaQuotient_value (j : AlgebraJet2 A B)
    (denominator : ℕ → Aˣ) (eta : A) (N : ℕ) (Q : A)
    (heta : j.value eta = 0) (hfirsteta : j.first eta = 1)
    (hquotient : transferProduct (fun i => etaTransfer (denominator i) eta) N - 1 =
      eta * Q) :
    j.value Q =
      (-2 : ℝ) • (∑ i ∈ Finset.range N, j.value (↑(denominator i)⁻¹ : A)) := by
  have h := congrArg j.first hquotient
  rw [map_sub, j.first_one, sub_zero, j.first_mul,
    heta, hfirsteta, one_mul, zero_mul, add_zero,
    etaMonodromy_first j denominator eta heta hfirsteta N] at h
  exact h.symm

/-- Algebraic expression after cancelling eta from numerator and resolvent. -/
def regularEtaNormalized (N B₀ : ℝ) (Q : Aˣ) (eta : A) : A :=
  (-2 * N) • (↑Q⁻¹ : A) + B₀ • (1 : A) - N • eta

/-- The manuscript's eta=0 expression is derived from the transfer factors
and a regular invertible quotient, not supplied as the evaluated value. -/
theorem regularEtaNormalized_value (j : AlgebraJet2 A B)
    (denominator : ℕ → Aˣ) (eta : A) (N : ℕ) (B₀ : ℝ)
    (Q : Aˣ) (sumUnit : Bˣ)
    (heta : j.value eta = 0) (hfirsteta : j.first eta = 1)
    (hquotient : transferProduct (fun i => etaTransfer (denominator i) eta) N - 1 =
      eta * (Q : A))
    (hsum : (sumUnit : B) =
      ∑ i ∈ Finset.range N, j.value (↑(denominator i)⁻¹ : A)) :
    j.value (regularEtaNormalized (N : ℝ) B₀ Q eta) =
      (N : ℝ) • (↑sumUnit⁻¹ : B) + B₀ • (1 : B) := by
  have hQ : j.value (Q : A) = (-2 : ℝ) • (sumUnit : B) := by
    rw [regularEtaQuotient_value j denominator eta N (Q : A) heta hfirsteta hquotient,
      ← hsum]
  have hinv : j.value (↑Q⁻¹ : A) = (-2 : ℝ)⁻¹ • (↑sumUnit⁻¹ : B) := by
    apply j.scaled_value_inverse Q sumUnit⁻¹ (-2) (by norm_num)
    simpa only [inv_inv] using hQ
  simp only [regularEtaNormalized, map_sub, map_add, map_smul, map_one,
    heta, smul_zero, sub_zero, hinv, smul_smul]
  congr 1
  congr 1
  norm_num
  ring

/-- Use the explicitly constructed finite quotient. Only its formal
invertibility remains an operator-realization input. -/
theorem constructedEtaNormalized_value (j : AlgebraJet2 A B)
    (denominator : ℕ → Aˣ) (eta : A) (N : ℕ) (B₀ : ℝ)
    (Q : Aˣ) (sumUnit : Bˣ)
    (heta : j.value eta = 0) (hfirsteta : j.first eta = 1)
    (hcentral : ∀ i < N, Commute eta (↑(denominator i)⁻¹ : A))
    (hQ : (Q : A) = etaMonodromyQuotient denominator eta N)
    (hsum : (sumUnit : B) =
      ∑ i ∈ Finset.range N, j.value (↑(denominator i)⁻¹ : A)) :
    j.value (regularEtaNormalized (N : ℝ) B₀ Q eta) =
      (N : ℝ) • (↑sumUnit⁻¹ : B) + B₀ • (1 : B) := by
  apply regularEtaNormalized_value j denominator eta N B₀ Q sumUnit
    heta hfirsteta _ hsum
  rw [hQ]
  exact etaMonodromyQuotient_factor denominator eta N hcentral

/-!
The weight-isolation step below is a finite polynomial statement, rather
than a hypothesis equating a physical Hessian to its desired value.
To apply it to the physical PDO residue, the normal-form coefficient
recurrences must still supply a homogeneous quadratic polynomial.
-/

structure QuadraticJetMonomial where
  bPower : ℕ
  etaPower : ℕ
  leftDeriv : ℕ
  rightDeriv : ℕ

namespace QuadraticJetMonomial

/-- B, eta, and f have weight one; each spatial derivative adds one. -/
def weight (term : QuadraticJetMonomial) : ℕ :=
  term.bPower + term.etaPower + term.leftDeriv + term.rightDeriv + 2

def derivativeOrder (term : QuadraticJetMonomial) : ℕ :=
  term.leftDeriv + term.rightDeriv

def evaluate (term : QuadraticJetMonomial) (B₀ eta : ℝ) (jet : ℕ → ℝ) : ℝ :=
  B₀ ^ term.bPower * eta ^ term.etaPower *
    jet term.leftDeriv * jet term.rightDeriv

theorem derivativeOrder_le (term : QuadraticJetMonomial) (N : ℕ)
    (hweight : term.weight = N + 2) : term.derivativeOrder ≤ N := by
  unfold weight at hweight
  unfold derivativeOrder
  omega

theorem parameters_vanish_at_top (term : QuadraticJetMonomial) (N : ℕ)
    (hweight : term.weight = N + 2) (htop : term.derivativeOrder = N) :
    term.bPower = 0 ∧ term.etaPower = 0 := by
  unfold weight at hweight
  unfold derivativeOrder at htop
  omega

theorem evaluate_top_independent (term : QuadraticJetMonomial) (N : ℕ)
    (hweight : term.weight = N + 2) (htop : term.derivativeOrder = N)
    (B₀ eta : ℝ) (jet : ℕ → ℝ) :
    term.evaluate B₀ eta jet = term.evaluate 0 0 jet := by
  obtain ⟨hB, heta⟩ := term.parameters_vanish_at_top N hweight htop
  simp only [evaluate, hB, heta, pow_zero, one_mul]

theorem parameter_terms_have_lower_order (term : QuadraticJetMonomial) (N : ℕ)
    (hweight : term.weight = N + 2)
    (hparameter : 0 < term.bPower + term.etaPower) :
    term.derivativeOrder < N := by
  unfold weight at hweight
  unfold derivativeOrder
  omega

end QuadraticJetMonomial

/-- The part of an actual finite polynomial density having maximal total
derivative count, prior to integration by parts. -/
def weightedQuadraticTop {I : Type*} (terms : Finset I)
    (coefficient : I → ℝ) (monomial : I → QuadraticJetMonomial)
    (N : ℕ) (B₀ eta : ℝ) (jet : ℕ → ℝ) : ℝ :=
  ∑ i ∈ terms, if (monomial i).derivativeOrder = N then
    coefficient i * (monomial i).evaluate B₀ eta jet else 0

/-- The manuscript's 'no remaining weight' argument, proved termwise.
The homogeneity premise is exposed and must come from the PDO recurrences. -/
theorem weightedQuadraticTop_independent {I : Type*} (terms : Finset I)
    (coefficient : I → ℝ) (monomial : I → QuadraticJetMonomial)
    (N : ℕ) (hweight : ∀ i ∈ terms, (monomial i).weight = N + 2)
    (B₀ eta : ℝ) (jet : ℕ → ℝ) :
    weightedQuadraticTop terms coefficient monomial N B₀ eta jet =
      weightedQuadraticTop terms coefficient monomial N 0 0 jet := by
  apply Finset.sum_congr rfl
  intro i hi
  by_cases htop : (monomial i).derivativeOrder = N
  · simp only [htop, ite_true]
    rw [(monomial i).evaluate_top_independent N (hweight i hi) htop]
  · simp only [htop, ite_false]

#print axioms etaTransfer_first
#print axioms etaMonodromy_first
#print axioms regularEtaNormalized_value
#print axioms etaMonodromyQuotient_factor
#print axioms constructedEtaNormalized_value
#print axioms weightedQuadraticTop_independent

end
end DLWLean
