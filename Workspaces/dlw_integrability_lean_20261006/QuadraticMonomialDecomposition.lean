import BalancedAmplitudePolynomial
import Mathlib.Data.Finsupp.Multiset

namespace DLWLean.BalancedPDO
noncomputable section
open scoped BigOperators

def fieldMultiplicity {M : ℕ} (s : JetVariable M →₀ ℕ) : JetVariable M →₀ ℕ :=
  s.filter (fun i => fieldWeight M i = 1)

theorem fieldMultiplicity_total {M : ℕ} (s : JetVariable M →₀ ℕ) :
    (fieldMultiplicity s).sum (fun _ n => n) = fieldDegree s := by
  classical
  simp only [fieldMultiplicity, Finsupp.sum, Finsupp.support_filter,
    Finset.sum_filter, Finsupp.filter_apply, fieldDegree, Finsupp.weight_apply,
    Finsupp.sum, nsmul_eq_mul, Nat.cast_id]
  apply Finset.sum_congr rfl
  intro i _
  cases i <;> simp [fieldWeight]

theorem exponent_parameter_field_split {M : ℕ} (s : JetVariable M →₀ ℕ) :
    s = Finsupp.single .b (s .b) + Finsupp.single .eta (s .eta) + fieldMultiplicity s := by
  classical
  apply Finsupp.ext
  intro i
  simp only [Finsupp.add_apply, Finsupp.single_apply]
  rw [show fieldMultiplicity s i = if fieldWeight M i = 1 then s i else 0 from rfl]
  cases i <;> simp [fieldWeight]

/-- Every genuine quadratic field monomial is exactly two field jets,
with possible powers of the two constant background parameters. -/
theorem quadratic_exponent_decomposition {M : ℕ} (s : JetVariable M →₀ ℕ)
    (hq : fieldDegree s = 2) :
    ∃ (j l : Fin M) (m n : ℕ),
      s = Finsupp.single .b (s .b) + Finsupp.single .eta (s .eta) +
        Finsupp.single (.field j m) 1 + Finsupp.single (.field l n) 1 := by
  classical
  have hcard : (Finsupp.toMultiset (fieldMultiplicity s)).card = 2 := by
    rw [Finsupp.card_toMultiset]
    exact (fieldMultiplicity_total s).trans hq
  obtain ⟨i, a, hmultiset⟩ := Multiset.card_eq_two.mp hcard
  have hmult : fieldMultiplicity s = Finsupp.single i 1 + Finsupp.single a 1 := by
    have hsum : Finsupp.toMultiset (fieldMultiplicity s) = ({i} + {a} : Multiset (JetVariable M)) := by
      simpa only [Multiset.singleton_add, Multiset.insert_eq_cons] using hmultiset
    have h := congrArg Multiset.toFinsupp hsum
    simpa only [Finsupp.toMultiset_toFinsupp, Multiset.toFinsupp_add,
      Multiset.toFinsupp_singleton] using h
  have hparam (v : JetVariable M) (hv : fieldWeight M v = 0) : i ≠ v ∧ a ≠ v := by
    have h := congrArg (fun f : JetVariable M →₀ ℕ => f v) hmult
    simp only [fieldMultiplicity, Finsupp.filter_apply, hv, Nat.zero_ne_one,
      ite_false, Finsupp.add_apply, Finsupp.single_apply] at h
    by_cases hi : i = v <;> by_cases ha : a = v
    · simp [hi, ha] at h
    · simp [hi, ha] at h
    · simp [hi, ha] at h
    · exact ⟨hi, ha⟩
  have hib := (hparam .b rfl).1
  have hie := (hparam .eta rfl).1
  have hab := (hparam .b rfl).2
  have hae := (hparam .eta rfl).2
  cases i with
  | b => exact (hib rfl).elim
  | eta => exact (hie rfl).elim
  | field j m =>
    cases a with
    | b => exact (hab rfl).elim
    | eta => exact (hae rfl).elim
    | field l n =>
      refine ⟨j, l, m, n, ?_⟩
      calc
        s = Finsupp.single .b (s .b) + Finsupp.single .eta (s .eta) +
            fieldMultiplicity s := exponent_parameter_field_split s
        _ = _ := by rw [hmult, ← add_assoc]

theorem derivativeOrder_quadratic_split {M : ℕ} (s : JetVariable M →₀ ℕ)
    (j l : Fin M) (m n : ℕ)
    (hs : s = Finsupp.single .b (s .b) + Finsupp.single .eta (s .eta) +
      Finsupp.single (.field j m) 1 + Finsupp.single (.field l n) 1) :
    derivativeOrder s = m + n := by
  unfold derivativeOrder
  rw [hs]
  simp only [map_add]
  simp [Finsupp.weight_single, derivativeWeight]

theorem monomial_value_quadratic_split {M : ℕ} (s : JetVariable M →₀ ℕ)
    (j l : Fin M) (m n : ℕ)
    (hs : s = Finsupp.single .b (s .b) + Finsupp.single .eta (s .eta) +
      Finsupp.single (.field j m) 1 + Finsupp.single (.field l n) 1)
    (r B eta : ℝ) (field : Fin M → ℕ → ℝ) :
    MvPolynomial.eval (jetValue M B eta field) (MvPolynomial.monomial s r) =
      r * B ^ (s .b) * eta ^ (s .eta) * field j m * field l n := by
  classical
  have h := congrArg
    (fun t : JetVariable M →₀ ℕ =>
      MvPolynomial.eval (jetValue M B eta field) (MvPolynomial.monomial t r)) hs
  rw [h, MvPolynomial.eval_monomial]
  have hsingle (i : JetVariable M) (a : ℕ) :
      (Finsupp.single i a).prod (fun v k => jetValue M B eta field v ^ k) =
        jetValue M B eta field i ^ a :=
    Finsupp.prod_single_index (pow_zero _)
  simp only [Finsupp.prod_add_index' (fun _ => pow_zero _) (fun _ _ _ => pow_add _ _ _)]
  rw [hsingle .b (s .b), hsingle .eta (s .eta),
    hsingle (.field j m) 1, hsingle (.field l n) 1]
  simp only [jetValue, pow_one]
  ring

#print axioms quadratic_exponent_decomposition
#print axioms derivativeOrder_quadratic_split
#print axioms monomial_value_quadratic_split
end
end DLWLean.BalancedPDO
