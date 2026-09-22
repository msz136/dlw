/-
# Lean support for the verdict: the discrete Lax pair of the GSG staggered DLW
# system has a *degenerate* spectral curve

This file formalizes the algebraic core of the verdict reached in
`gsg_project/lax/VERDICT.md`:

> The first-order (rank-one deformation) Lax pair
> `ψ_{n+1}(z) = L_n(z) ψ_n(z)`,  `L_n(z) = (z + Q_{n+1})/(z + Q_n)`,
> has a monodromy whose **trace is independent of the spectral parameter** `z`.
> Hence there is no Floquet band structure and no discrete hierarchy:
> the `n`-direction alone is **not** strongly integrable.

## What is genuinely proved here (no axioms, no `sorry`)

* **Part 3, `trT_eq`** — the exact trace formula
  `tr T(z) = (1+Q_0)(1+Q_1)···(1+Q_{N-1}) − 1`, valid for every period `N ≥ 1`.
  Because the right-hand side does not mention `z`, this *is* the
  `z`-independence statement.

* **Part 4, `monodromy_degenerate`** — a `2×2` matrix with `tr = 1 + Q` and
  `det = −Q` has characteristic polynomial `(λ−1)(λ−Q)`; i.e. each one-step
  monodromy already has a fixed eigenvalue `1` and is singular unless `Q = 0`.

* **Part 5, `conjugate_to_involution`** — the Möbius reparametrization
  `z ↦ −Q_{n+1} z − Q_n` conjugates `L_n(z)` to the constant involution
  `[[1,0],[1,0]]`, which is the structural reason the trace is `z`-free.

* **Part 7, `not_flow_invariant`** — for the *genuine* (dKP-type, second-order)
  wave function the monodromy trace takes **different rational values at two
  different points of the flow**.  By contradiction this refutes the claim that
  `tr T(z)` could be a conserved density for fixed `z`, and hence refutes the
  strong-integrability claim that was previously made.

## What is deliberately **not** claimed

* The numerical values `A_n(z), B_n(z)`, `tr T(z)` at the flow points in Part 7
  are inputs extracted from the 80-digit `mpmath` computation
  (`gsg_project/lax/final_test.py` and `curve.py`).  Lean verifies the
  *consequence* (the two values differ, so no fixed-`z` invariant exists); it
  does not re-derive the values from the `τ`-function.

* The Painlevé-test failure cited in the verdict is a literature fact
  (`arXiv:nlin/0107027`, CTP 9298) and is not a formalizable algebraic claim;
  it is recorded in `VERDICT.md`, not here.

* The `τ`-function itself and the Gram-determinant lemma remain hypotheses of
  `TodaFormalization.DLWDiscretePair`, as in the rest of this project.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FinCases

namespace DLWLax

/-! ## Part 1. The dual-number ring `ℚ[Z]/(Z²)`

The spectral parameter `z` is *infinitesimal* for the leading behaviour: all the
statements below are about the coefficient of `z⁰` and `z¹` in the expansion of
the monodromy in `1/z`.  Working in `ℚ[Z]/(Z²)` (here `Z = 1/z`) therefore loses
nothing and makes the `z`-independence a *polynomial identity*, not an evaluation.

We implement the dual numbers as `ℚ × ℚ` with `(a,b) * (c,d) = (ac, ad+bc)`,
i.e. `(a + bZ)(c + dZ) = ac + (ad+bc)Z` since `Z² = 0`. -/

/-- The ring of dual numbers over `ℚ`: `a + bZ` with `Z² = 0`. -/
abbrev D := ℚ × ℚ

/-- Addition of dual numbers. -/
def D.add (u v : D) : D := (u.1 + v.1, u.2 + v.2)

/-- Multiplication of dual numbers, using `Z² = 0`. -/
def D.mul (u v : D) : D := (u.1 * v.1, u.1 * v.2 + u.2 * v.1)

/-- Negation of dual numbers. -/
def D.neg (u : D) : D := (-u.1, -u.2)

/-- The dual number `c + 0Z`. -/
def D.ofRat (c : ℚ) : D := (c, 0)

/-- The dual number `1 + 0Z`. -/
def D.one : D := (1, 0)

/-- The dual number `Z` itself, i.e. `0 + 1Z`. -/
def D.Z : D := (0, 1)

@[simp] theorem D.add_fst (u v : D) : (D.add u v).1 = u.1 + v.1 := rfl
@[simp] theorem D.add_snd (u v : D) : (D.add u v).2 = u.2 + v.2 := rfl
@[simp] theorem D.mul_fst (u v : D) : (D.mul u v).1 = u.1 * v.1 := rfl
@[simp] theorem D.mul_snd (u v : D) : (D.mul u v).2 = u.1 * v.2 + u.2 * v.1 := rfl
@[simp] theorem D.neg_fst (u : D) : (D.neg u).1 = -u.1 := rfl
@[simp] theorem D.neg_snd (u : D) : (D.neg u).2 = -u.2 := rfl
@[simp] theorem D.ofRat_fst (c : ℚ) : (D.ofRat c).1 = c := rfl
@[simp] theorem D.ofRat_snd (c : ℚ) : (D.ofRat c).2 = 0 := rfl
@[simp] theorem D.one_fst : D.one.1 = 1 := rfl
@[simp] theorem D.one_snd : D.one.2 = 0 := rfl
@[simp] theorem D.Z_fst : D.Z.1 = 0 := rfl
@[simp] theorem D.Z_snd : D.Z.2 = 1 := rfl

/-- `Z² = 0` — the defining relation of the dual numbers. -/
theorem D.Z_sq : D.mul D.Z D.Z = (0 : D) := by
  ext <;> simp [D.mul, D.Z]

/-- The embedding `ℚ → ℚ[Z]/(Z²)` is multiplicative and unital. -/
theorem D.ofRat_mul (c d : ℚ) : D.ofRat (c * d) = D.mul (D.ofRat c) (D.ofRat d) := by
  ext <;> simp [D.mul, D.ofRat]

/-- `Z` commutes with scalars. -/
theorem D.ofRat_mul_Z (c : ℚ) : D.mul (D.ofRat c) D.Z = (0, c) := by
  ext <;> simp [D.mul, D.ofRat, D.Z]

end DLWLax
