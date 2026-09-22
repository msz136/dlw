import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Complex.Basic

-- T1: does `ring` know Complex.I^2 = -1 ?
example (k : ℂ) : Complex.I * k * (Complex.I * k) = -k ^ 2 := by ring

-- T2: does `ring_nf` know it ?
example (k : ℂ) : Complex.I * k * (Complex.I * k) = -k ^ 2 := by ring_nf

-- T3: field_simp + ring in the presence of Complex.I
example (k : ℂ) (hk : k ≠ 0) (x : ℂ) :
    (Complex.I * k) ^ 2 * (x / k ^ 2) = -x := by
  field_simp
  ring

-- T4: is I_sq simp ?
example : (Complex.I : ℂ) ^ 2 = -1 := by simp

-- T5: mul_pow route
example (k : ℂ) : (Complex.I * k) ^ 2 = -k ^ 2 := by
  rw [mul_pow, Complex.I_sq]
  ring
