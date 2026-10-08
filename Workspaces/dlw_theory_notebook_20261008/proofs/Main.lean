/-
DLW endpoint contracts — integration module.

Imports every package file and audits the axiom footprint of each exported target.
Run through the standard entry:

  & 'C:\Users\msz\aca\_lean_shared\Check-Lean.ps1' `
    -Root 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs' `
    -File 'C:\Users\msz\aca\Workspaces\lean_contracts\proofs\Main.lean'

Every `#print axioms` line below must report only Lean's three standard axioms
(`propext`, `Classical.choice`, `Quot.sound`) — in particular no `sorryAx`.
-/
import Contracts
import PkgTrivial
import PkgGramEntry
import PkgQuotientRate
import PkgContinuous
import PkgLattice
import PkgNumeric
import PkgC11
import PkgNonlinear
import PkgC02
import PkgC17
import PkgC09Complete
import PkgGramBridges
import PkgRK4
import PkgRK4Complete
import PkgC18Complete
import PkgGramComplete
import PkgC23Complete
import PkgC22Complete

namespace DLWContract

/-- With positivity now proved, the exact Gram nonlinear endpoint has only
the arbitrary-N bilinear chain as its remaining premise. This is a conditional
bridge, not an unconditional proof of C16. -/
theorem c16_of_c07 (h07 : C07) : C16 :=
  c16_of_c08_c09 (c08_of_c07 h07) c09_proved

#print axioms c09_proved
#print axioms c07_proved
#print axioms c08_proved
#print axioms c16_proved
#print axioms c08_of_c07
#print axioms c16_of_c08_c09
#print axioms c16_of_c07
#print axioms RK4Proof.autoStep_linear

/-! ## Package A — semantic / continuous layer -/
#print axioms c01_proved
#print axioms c03_proved

/-! ## Package B — Gram exactness (entry algebra) -/
#print axioms c04_proved
#print axioms c05_proved
#print axioms c06_proved
#print axioms c10_proved

/-! ## Package C — analysis and limits (rate, quotient) -/
#print axioms c12_proved
#print axioms c13_proved
#print axioms c24_proved
#print axioms c23_proved
#print axioms c22_proved

/-! ## Package D — nonlinear bridge and nonlinear-system properties -/
#print axioms c21_proved
#print axioms c19_proved
#print axioms c20_proved
#print axioms c25_proved

/-! ## Package F — continuous sampling consistency
`C11` is the fixed-physical-`y` two-wall consistency: the half-sum of the
`a ± h/2` walls converges to `cbil a f g` at `O(h²)`, and the half-difference
divided by `h` converges to `cbil a f (sy g) + 2 · chx f g` at `O(h²)`.
Both conjuncts fall out of one second-order Taylor expansion of
`s ↦ bil (a+s) (slice f y) (slice g (y+s))`. -/
#print axioms c11_proved

/-! ## Package G — bilinear→nonlinear residual bridge
`C14` is the exact residual identity (no equation assumed): `n1`/`n2` of the
physical fields equal lattice differences of the normalized bilinear residuals.
`C15` is the corollary for the semi-discrete system: `SemiPair` forces
`normA = normC = 0`, hence `NonlinearPair`. -/
#print axioms c14_proved
#print axioms c15_proved

/-! ## Package H — continuous bilinear → physical DLW
`C02` is the `λ = -2` continuous physical system.  Conjunct 1 is `c1 = 2·∂ₓ∂ᵧR`,
conjunct 2 is `c2 = 2·∂ₓ∂ᵧR - 2·∂ₓS`, both with multiplier ±1; `R = 0` and `S = 0`
follow from `ContinuousPair`, which yields `cbil a f g = 0` and
`cbil a f (sy g) + 2·chx f g = 0`. -/
#print axioms c02_proved

/-! ## Package I — lattice sampling consistency
`C17` has two conjuncts.  The first is an EXACT identity for every `h` (including
`h = 0`): the physical fields of the sampled Gram data equal the sampled
interpolated fields, `physU ∘ sample = sample ∘ interpU` and likewise for `physV`
— pure lattice index arithmetic, no analysis.  The second is the `O(h²)`
consistency `interpU → cu` and `interpV → cv`, both reduced to centred-difference
truncation of one-variable Taylor remainders. -/
#print axioms c17_proved
#print axioms c18_proved

/-! ## Package E — numerical-method foundations
`N01` is proved, including nonlinear RK4 and time-dependent RHS. The augmented
autonomous trajectory and the actual RK4 stages have equal jets through order
four; two Taylor remainders give the fifth-order local defect. This does not
claim a global error bound for the implemented DLW solver. -/
#print axioms n01_proved
#print axioms n02_proved
#print axioms n03_proved
#print axioms n04_proved
#print axioms n05_proved
#print axioms n06_proved
#print axioms n07_proved
#print axioms n01_euler_part
#print axioms n01_trapezoid_part
#print axioms n01_rk4_of_taylor_poly

end DLWContract
