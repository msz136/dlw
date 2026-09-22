import Mathlib.Tactic

lemma mod_even_parity (x N : ℕ) (hN : N % 2 = 0) : (x % N) % 2 = x % 2 := by
  have h := Nat.mod_add_div x N
  have hpar : (x % N + N * (x / N)) % 2 = x % 2 := by omega
  rw [Nat.add_comm] at hpar
  rw [h] at hpar
  exact hpar

example (N : ℕ) (hN : 2 ≤ N) (j : Fin N) : ((j + (2 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + 2) % N := by
  simp [Fin.val_add]

example (N : ℕ) (hN : 2 ≤ N) (hN2 : N % 2 = 0) (j : Fin N) :
    ((j + (2 : Fin N) : Fin N) : ℕ) % 2 = (j : ℕ) % 2 := by
  rw [show ((j + (2 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + 2) % N by simp [Fin.val_add]]
  rw [mod_even_parity _ _ hN2]
  omega
