import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic
open scoped BigOperators

example (N : ℕ) [NeZero N] (j : Fin N) : ((j + (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + 1) % N := by
  rw [Fin.val_add]; simp

example (N : ℕ) [NeZero N] (j : Fin N) : ((j - (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + N - 1) % N := by
  rw [Fin.val_sub]; simp

example (N : ℕ) [NeZero N] (j : Fin N) : ((j + (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + 1) % N := Fin.val_add_one j

example (N : ℕ) (hN : 2 ∣ N) (j : Fin N) :
    ((j + (1 : Fin N) : Fin N) : ℕ) % 2 = ((j - (1 : Fin N) : Fin N) : ℕ) % 2 := by
  haveI : NeZero N := ⟨fun h => by subst h; omega⟩
  have hNmod : N % 2 = 0 := Nat.mod_eq_zero_of_dvd hN
  have h1 : ((j + (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + 1) % N := by rw [Fin.val_add]; simp
  have h2 : ((j - (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + N - 1) % N := by rw [Fin.val_sub]; simp
  rw [h1, h2]
  have hp (x : ℕ) : (x % N) % 2 = x % 2 := by
    have h := Nat.mod_add_div x N
    have hpar : (x % N + N * (x / N)) % 2 = x % 2 := by omega
    rw [h] at hpar; exact hpar
  rw [hp, hp]
  have hj := j.isLt
  omega
