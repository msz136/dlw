import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic
open scoped BigOperators
namespace DLW.Probe

section
variable {N : ℕ} [NeZero N]

#check (1 : Fin N)
#check (fun (j : Fin N) => j + (1 : Fin N))

def fwdN (j : Fin N) : Fin N :=
  if h : (j : ℕ) + 1 < N then ⟨(j : ℕ) + 1, h⟩ else ⟨0, Nat.pos_of_ne_zero (NeZero.ne N)⟩

lemma fwdN_val (j : Fin N) : (fwdN j : ℕ) = ((j : ℕ) + 1) % N := by
  unfold fwdN
  split_ifs with h
  · rw [Nat.mod_eq_of_lt h]
  · rw [Nat.mod_eq_of_lt (Nat.pos_of_ne_zero (NeZero.ne N))]

lemma fwdN_eq_add (j : Fin N) : fwdN j = j + (1 : Fin N) := by
  apply Fin.ext
  rw [fwdN_val, Fin.val_add]
  simp

end
end DLW.Probe
