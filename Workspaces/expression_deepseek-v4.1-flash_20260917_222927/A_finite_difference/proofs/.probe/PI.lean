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
  | succ b ih => have h : 2 * (b + 1) = 2 * b + 2 := by omega; rw [h, altTwo_add_two]; exact ih

lemma altTwo_two_mul_add_one (a : ℕ) : altTwo (K := K) (2 * a + 1) = -1 := by
  induction a with
  | zero => rfl
  | succ b ih => have h : 2 * (b + 1) + 1 = (2 * b + 1) + 2 := by omega; rw [h, altTwo_add_two]; exact ih

example (n : ℕ) : altTwo (K := K) n = 1 ∨ altTwo (K := K) n = -1 := by
  have h : n = 2 * (n / 2) + n % 2 := by have := Nat.div_add_mod n 2; omega
  have hlt : n % 2 < 2 := Nat.mod_lt _ (by omega)
  interval_cases h2 : n % 2
  · left; rw [h, h2, altTwo_two_mul]
  · right; rw [h, h2, altTwo_two_mul_add_one]

example (n : ℕ) : altTwo (K := K) (n + 1) = -altTwo n := by
  have h : n = 2 * (n / 2) + n % 2 := by have := Nat.div_add_mod n 2; omega
  have hlt : n % 2 < 2 := Nat.mod_lt _ (by omega)
  interval_cases h2 : n % 2
  · have hn : n + 1 = 2 * (n / 2) + 1 := by omega
    rw [hn, altTwo_two_mul_add_one, h, h2, altTwo_two_mul]; simp
  · have hn : n + 1 = 2 * (n / 2 + 1) := by omega
    rw [hn, altTwo_two_mul, h, h2, altTwo_two_mul_add_one]; simp

end DLW.Probe
