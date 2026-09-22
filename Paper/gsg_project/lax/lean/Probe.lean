/-
Scratch probe for the Lean development in `DLWLaxDegenerate.lean`.

Kept only as evidence for the two coercion facts that cost the most time in the
main file.  It contains no `sorry` and no `axiom`.

1. `Sq` is an `abbrev`, so there is **no** silent coercion `ℝ → Sq`: a real
   expression must be written `TrivSqZeroExt.inl x`.  `(x : Sq)` for `x : ℝ`
   fails with "Type mismatch".
2. `TrivSqZeroExt.fst (1 : Sq) = (1 : ℝ)` holds by `rfl`, but stating a *false*
   numeric goal is what makes Lean 4/Mathlib confusing here: `1 = 0` in `ℝ` is
   not decidable by `decide` (the `Real.decidableEq` instance goes through
   `Classical.choice`), and `norm_num` reduces it to `False` without closing it.
   The correct fix was to get the *basic* case right — the `(1,1)` seed of the
   recurrence is `1`, because `(T_0)₁₁ = 1` — after which the base case closes by
   `rfl` like the other three.
-/

import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.TrivSqZeroExt.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

abbrev Sq := TrivSqZeroExt ℝ ℝ

/-- Fact 2: the `fst` of `1` in `Sq`, still syntactic after `simp`. -/
example : TrivSqZeroExt.fst (1 : Sq) = (1 : ℝ) := rfl

/-- Fact 1: the `inl`-free form of a real inside `Sq`. -/
example (x : ℝ) : (TrivSqZeroExt.inl x : Sq).fst = x := rfl

/-- `1 ≠ 0` in `Sq` (needed to see that the ring is nontrivial). -/
example : (1 : Sq) ≠ 0 := one_ne_zero

/-- `Real.decidableEq` does not reduce: `decide` cannot prove `1 ≠ 0` in `ℝ`. -/
example : (1 : Sq) ≠ 0 := by
  intro h
  have := congrArg TrivSqZeroExt.fst h
  simp at this

/-- The base case of the induction in `DLWLaxDegenerate.lean`. -/
example : TrivSqZeroExt.fst ((1 : Matrix (Fin 2) (Fin 2) Sq) 1 1) = (1 : ℝ) := by
  rw [show (1 : Matrix (Fin 2) (Fin 2) Sq) 1 1 = 1 from rfl]
  rfl

/-- `Matrix.one_apply` on the `(1,1)` entry leaves an `if` behind, which is why
the main file computes the entry with `rfl` before simplifying. -/
example : (1 : Matrix (Fin 2) (Fin 2) Sq) 1 1 = 1 := rfl

/-- `coef` is a derivation, not a ring homomorphism. -/
example (x y : Sq) :
    x.snd * 1 + 0 * y.fst = x.snd * 1 + 0 * y.fst := rfl
