import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

open scoped BigOperators

namespace DLW.Probe

variable {K : Type*} [Field K]

lemma mod_even_parity (x N : ℕ) (hN : N % 2 = 0) : (x % N) % 2 = x % 2 := by
  have h := Nat.mod_add_div x N
  have hpar : (x % N + N * (x / N)) % 2 = x % 2 := by omega
  rw [h] at hpar
  exact hpar

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

lemma altTwo_eq_of_mod_two_eq {m n : ℕ} (h : m % 2 = n % 2) :
    altTwo (K := K) m = altTwo (K := K) n := by
  have hm' : m = 2 * (m / 2) + m % 2 := by
    have := Nat.div_add_mod m 2; omega
  have hn' : n = 2 * (n / 2) + n % 2 := by
    have := Nat.div_add_mod n 2; omega
  rw [hm', hn', h]
  rcases Nat.mod_two_eq_zero_or_one (n % 2) with h0 | h1
  · rw [h0]; simp [altTwo_two_mul]
  · rw [h1]; simp [altTwo_two_mul_add_one]

example (a b : ℕ) : 2 * (b + 1) = 2 * b + 2 := by omega
example (a b : ℕ) : 2 * (b + 1) + 1 = (2 * b + 1) + 2 := by omega

end DLW.Probe
