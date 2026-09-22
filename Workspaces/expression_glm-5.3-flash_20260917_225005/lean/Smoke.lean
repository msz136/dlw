import Common.Operators

namespace SmokeTest

open DLW

theorem hirotaX_zero_self (K : Type) [Field K] (F : Jet K) :
    hirotaX F F = 0 := by
  simp [hirotaX]; ring

theorem shift_dplus_smoke (u : LatticeFun ℝ) : shift (dplus u) = dplus (shift u) :=
  shift_dplus u

#print axioms SmokeTest.hirotaX_zero_self
#print axioms SmokeTest.shift_dplus_smoke

end SmokeTest
