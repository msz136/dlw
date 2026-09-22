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
  have hm' : m = 2 * (m / 2) + m % 2 := by have := Nat.div_add_mod m 2; omega
  have hn' : n = 2 * (n / 2) + n % 2 := by have := Nat.div_add_mod n 2; omega
  rw [hm', hn', h]
  by_cases h0 : n % 2 = 0
  · rw [h0]; simp [altTwo_two_mul]
  · have h1 : n % 2 = 1 := by omega
    rw [h1]; simp [altTwo_two_mul_add_one]

section Grid
variable {N : ℕ} (hN : 2 ∣ N)
include hN

lemma neZero_of_two_dvd : NeZero N := ⟨fun h => by subst h; omega⟩

def altOf (j : Fin N) : K := altTwo ((j : ℕ) % 2)

def ctr (f : Fin N → K) (j : Fin N) : K := f (j + 1) - f (j - 1)

lemma ctr_const (c : K) : ctr (N := N) (fun _ : Fin N => c) = 0 := by
  funext j; simp [ctr]

lemma sameClass_succ_pred (j : Fin N) :
    ((j + 1 : Fin N) : ℕ) % 2 = ((j - 1 : Fin N) : ℕ) % 2 := by
  have hNmod : N % 2 = 0 := Nat.mod_eq_zero_of_dvd hN
  have h1 : ((j + 1 : Fin N) : ℕ) = ((j : ℕ) + 1) % N := by simp [Fin.val_add]
  have h2 : ((j - 1 : Fin N) : ℕ) = ((j : ℕ) + N - 1) % N := by
    rw [Fin.val_sub]; simp
  rw [h1, h2, mod_even_parity _ _ hNmod, mod_even_parity _ _ hNmod]
  have hj := j.isLt
  omega

end Grid
end DLW.Probe
