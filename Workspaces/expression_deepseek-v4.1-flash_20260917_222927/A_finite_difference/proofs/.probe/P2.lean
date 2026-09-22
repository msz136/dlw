import Mathlib.Data.Nat.Parity
import Mathlib.Tactic

lemma even_mul (q N : ℕ) (hN : N % 2 = 0) : (q * N) % 2 = 0 := by
  omega

lemma parity_add_even (x q N : ℕ) (hN : N % 2 = 0) : (x + q * N) % 2 = x % 2 := by
  omega

/-- the modulo by an even number does not change parity -/
lemma mod_even_parity (x N : ℕ) (hN : N % 2 = 0) : (x % N) % 2 = x % 2 := by
  have h := Nat.mod_add_div x N
  have hpar : (x % N + N * (x / N)) % 2 = x % 2 := by omega
  rw [Nat.add_comm] at hpar
  rw [h] at hpar
  exact hpar

example (x N : ℕ) (hN : N % 2 = 0) : (x + 2) % N % 2 = x % 2 := by
  rw [mod_even_parity _ _ hN]
  omega
