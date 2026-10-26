import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

example : (2 : ℕ) + 2 = 4 := by norm_num
example (x y : ℝ) : (x + y)^2 = x^2 + 2*x*y + y^2 := by ring
example (x : ℝ) (h : x > 1) : x > 0 := by linarith
