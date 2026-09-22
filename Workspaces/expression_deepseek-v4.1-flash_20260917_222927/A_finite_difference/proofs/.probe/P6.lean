import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

open scoped BigOperators
namespace DLW.Probe
variable {K : Type*} [Field K]

def altTwo : ℕ → K
  | 0 => 1
  | 1 => -1
  | n + 2 => altTwo n

@[simp] lemma altTwo_add_two (n : ℕ) : altTwo (K := K) (n + 2) = altTwo n := rfl

lemma altTwo_two_mul (a : ℕ) : altTwo (K := K) (2 * a) = 1 := by
  induction a with
  | zero => rfl
  | succ b ih =>
      have h : 2 * (b + 1) = 2 * b + 2 := by omega
      rw [h, altTwo_add_two]; exact ih

lemma altTwo_two_mul_add_one (a : ℕ) : altTwo (K := K) (2 * a + 1) = -1 := by
  induction a with
  | zero => rfl
  | succ b ih =>
      have h : 2 * (b + 1) + 1 = (2 * b + 1) + 2 := by omega
      rw [h, altTwo_add_two]; exact ih

lemma even_iff_mod (n : ℕ) : n % 2 = 0 ↔ 2 ∣ n := Nat.dvd_iff_mod_eq_zero.symm

lemma altTwo_eq_of_mod_two_eq {m n : ℕ} (h : m % 2 = n % 2) :
    altTwo (K := K) m = altTwo (K := K) n := by
  have hm' : m = 2 * (m / 2) + m % 2 := by have := Nat.div_add_mod m 2; omega
  have hn' : n = 2 * (n / 2) + n % 2 := by have := Nat.div_add_mod n 2; omega
  rw [hm', hn', h]
  by_cases h0 : n % 2 = 0
  · rw [h0]; simp [altTwo_two_mul]
  · have h1 : n % 2 = 1 := by omega
    rw [h1]; simp [altTwo_two_mul_add_one]

end DLW.Probe
