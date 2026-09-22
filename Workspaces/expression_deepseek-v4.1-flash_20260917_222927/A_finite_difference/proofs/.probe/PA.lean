import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic
open scoped BigOperators
namespace DLW.Probe

/-- forward neighbour, wrapping around -/
def fwdN (N : ℕ) (j : Fin N) : Fin N :=
  if h : (j : ℕ) + 1 < N then ⟨(j : ℕ) + 1, h⟩ else ⟨0, Nat.pos_of_ne_zero (by
    intro hz; rw [hz] at h; simp at h; omega)⟩

lemma fwdN_val (N : ℕ) [NeZero N] (j : Fin N) : (fwdN N j : ℕ) = ((j : ℕ) + 1) % N := by
  unfold fwdN
  split_ifs with h
  · rw [Nat.mod_eq_of_lt h]
  · rw [Nat.mod_eq_of_lt (by omega : 0 < N)]

lemma fwdN_eq_add (N : ℕ) (hN : 2 ∣ N) (j : Fin N) : fwdN N j = j + (1 : Fin N) := by
  haveI : NeZero N := ⟨fun h => by subst h; omega⟩
  apply Fin.ext
  rw [fwdN_val]
  rw [Fin.val_add]
  simp

end DLW.Probe
