import Mathlib.Tactic.Ring

namespace T1

variable {R : Type*} [CommRing R]

theorem t (a b : R) : a*b = b*a := by ring

end T1
