import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic
open scoped BigOperators

-- can we use the numeral 1 on Fin N with a local NeZero instance?
example (N : ℕ) (hN : 2 ∣ N) (f : Fin N → ℕ) (j : Fin N) :
    f (j + (1 : Fin N)) = f j := by
  haveI : NeZero N := ⟨fun h => by subst h; omega⟩
  sorry

-- explicit step functions, no OfNat needed
def fwd {N : ℕ} (i : Fin N) : ℕ := (i : ℕ) + 1

example (N : ℕ) (i : Fin N) (h : (i : ℕ) + 1 < N) :
    fwd i = (i : ℕ) + 1 := rfl

-- Fin.mk with a proof
example (N : ℕ) (x : ℕ) (h : x < N) : (Fin.mk x h : ℕ) = x := rfl
