import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic
open scoped BigOperators
namespace DLW.Probe

section
variable {N : ℕ} [NeZero N]

example (j : Fin N) (h : ¬ (j : ℕ) + 1 < N) : ((j : ℕ) + 1) % N = 0 := by
  have h1 : (j : ℕ) + 1 ≤ N := by have := j.isLt; omega
  obtain ⟨k, hk⟩ : ∃ k, (j : ℕ) + 1 = k := ⟨_, rfl⟩
  omega

example (j : Fin N) (h : ¬ (j : ℕ) + 1 < N) : (j : ℕ) + 1 = N := by
  have h1 : (j : ℕ) + 1 ≤ N := by have := j.isLt; omega
  omega

example (j : Fin N) (h : ¬ (j : ℕ) + 1 < N) : ((j : ℕ) + 1) % N = 0 := by
  have h1 : (j : ℕ) + 1 = N := by have := j.isLt; omega
  rw [h1, Nat.mod_self]

end
end DLW.Probe
