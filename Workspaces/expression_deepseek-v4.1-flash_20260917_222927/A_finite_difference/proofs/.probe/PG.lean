import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic
open scoped BigOperators
namespace DLW.Probe

lemma mod_even_parity (x N : ℕ) (hN : N % 2 = 0) : (x % N) % 2 = x % 2 := by
  have h := Nat.mod_add_div x N
  have hpar : (x % N + N * (x / N)) % 2 = x % 2 := by omega
  rw [h] at hpar
  exact hpar

section
variable {N : ℕ} [NeZero N]

example (hN : 2 ≤ N) (j : Fin N) :
    ((j - (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + N - 1) % N := by
  rw [Fin.val_sub]
  have h1 : ((1 : Fin N) : ℕ) = 1 := by
    simp only [Fin.val_one']
    exact Nat.mod_eq_of_lt (by omega)
  rw [h1]
  congr 1
  omega

example (hN : 2 ≤ N) (j : Fin N) :
    ((j + (1 : Fin N) : Fin N) : ℕ) % 2 = ((j - (1 : Fin N) : Fin N) : ℕ) % 2 := by
  have hNmod : N % 2 = 0 := by omega
  have h1 : ((j + (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + 1) % N := by
    rw [Fin.val_add]; simp
  have h2 : ((j - (1 : Fin N) : Fin N) : ℕ) = ((j : ℕ) + N - 1) % N := by
    rw [Fin.val_sub]
    have hh : ((1 : Fin N) : ℕ) = 1 := by
      simp only [Fin.val_one']
      exact Nat.mod_eq_of_lt (by omega)
    rw [hh]
    congr 1
    omega
  rw [h1, h2, mod_even_parity _ _ hNmod, mod_even_parity _ _ hNmod]
  have hj := j.isLt
  omega

end
end DLW.Probe
