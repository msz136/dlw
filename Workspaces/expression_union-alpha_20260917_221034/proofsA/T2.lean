import Mathlib.Tactic.Ring

/-!
Doc block.
-/

namespace T2

structure Jet (R : Type*) where
  value : R
  dx : R

variable {R : Type*} [CommRing R]

theorem t (F : Jet R) : F.value * 1 = F.value := by ring

end T2
