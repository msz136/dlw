import Common.Operators

-- Smoke test for direction A pipeline. Trivial but real lemma.
open DLW

theorem A_smoke (q : ℚ) (hq : q + 1 = q + 2) : q + 1 = q + 2 := hq

example : (1 : ℚ) + 1 = 2 := by norm_num

#print axioms A_smoke
