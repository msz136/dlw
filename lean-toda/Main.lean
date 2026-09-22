import Init.Grind.Ring.Field
import Init.GrindInstances.Ring.Rat

/-!
# A first formal Toda calculation

We use the pointwise form of the bilinear Toda equation

  τₙ τₙ'' - (τₙ')² = τₙ₊₁ τₙ₋₁ - τₙ².

For positive τ-functions, `qₙ = log τₙ` turns its left-hand side into
`τₙ² qₙ''`, while the quotient of neighbouring τ-functions becomes an
exponential.  The theorem below is the algebraic core of that conversion.
-/

open Lean.Grind

/- The exponential expression is kept as a quotient at this first stage.
   Analytically, it is `exp (log τnext + log τprev - 2 log τ)` for positive
   τ-values.  The quotient is the exact algebraic content needed here. -/
def todaGap (τprev τ τnext : Rat) : Rat :=
  (τnext * τprev) / τ ^ 2

theorem bilinear_to_log_toda
    (τprev τ τnext τt τtt : Rat)
    (hτ : τ ≠ 0)
    (hbilin : τ * τtt - τt ^ 2 = τnext * τprev - τ ^ 2) :
    τtt / τ - (τt / τ) ^ 2 = todaGap τprev τ τnext - 1 := by
  simp [todaGap, Field.div_eq_mul_inv]
  grind

/-!
The usual nonlinear semi-discrete Toda equation is obtained by taking the
difference of the preceding identity at two adjacent lattice sites.  This
small lemma records the corresponding cancellation independently of τ.
-/

theorem toda_difference
    (E : Rat → Rat) (qdd_prev qdd q_prev q qnext : Rat)
    (hprev : qdd_prev = E (q - q_prev) - 1)
    (h : qdd = E (qnext - q) - 1) :
    qdd - qdd_prev = E (qnext - q) - E (q - q_prev) := by
  rw [h, hprev]
  grind
