import Common.DirA

/-! Root of the Union Alpha proof tree for direction A.
Main agent integrates; Dir A subagent owns Common\DirA.lean. -/

/-!
NOTE (main agent): the final integrated tree will import Common.DirA..DirH
once each direction's module exists in this root. Per-direction roots keep
only their own module so concurrent verification stays independent.
-/