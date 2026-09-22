import Mathlib.Tactic.Ring

namespace SmokeTest

variable {Q : Type*} [CommRing Q]

theorem smoke (x : Q) : x*1 = x := by ring

end SmokeTest