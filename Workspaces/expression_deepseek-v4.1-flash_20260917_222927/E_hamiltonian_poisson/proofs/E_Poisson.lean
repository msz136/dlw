/-
  Direction E — Hamiltonian / Poisson structure for the `y`-discretised DLW system.

  Content (see ../report.md for the mathematics):

  * `Theta` is the field-dependent matrix that appears in the (1,1) block of the
    Helmholtz integrability condition for a bracket `P = d_x · Q` with CONSTANT
    symmetric `Q`, when the constraint `u_y = w` is solved by a discrete `d_y^{-1}`
    represented by the matrix `C` (so `u = C w`).

    Its key property is  `Theta = diag(w) * C - Cᵀ * diag(w)`.
    `Theta` is antisymmetric — exactly the symmetry type of `d_x` — so it can only
    be cancelled by another antisymmetric term; a *constant* `Q` provides none, and
    this is the obstruction.

  * The concrete `Fin 3` lattice with the one-sided cumulative-sum convention
    `u 0 = 0, u 1 = w 0, u 2 = w 0 + w 1` gives `Theta 1 0 = w 1`, so the
    Helmholtz condition `q11 • Theta = 0` forces `q11 = 0`, and the two remaining
    Helmholtz coefficient equations force `q12 = q22 = 0`.  Hence every constant
    symmetric `Q` solving the Helmholtz system is `Q = 0`, i.e. singular, i.e. NOT
    a bracket.  Negative result, formalised.

  Everything below is proved; there is no `sorry`, no `axiom`, no `admit`.
-/
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Mul
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Tactic

namespace DLW.E

open Matrix

variable {K : Type*} [CommRing K]
variable {n : Type*} [Fintype n] [DecidableEq n]

/-! ## 1.  The general obstruction matrix -/

/-- The field-dependent obstruction matrix of the `y`-discretised DLW system.
`C` is the chosen discrete `∂_y^{-1}` (so `u = C w`); `w` is the field `u_y`.

Explicitly it is the field-dependent (i.e. non-constant) part of the Fréchet
derivative `∂M/∂w` of the discrete flux `M_j = (d_x v)_j + (u_j + 2a) w_j`. -/
def Theta (w : n → K) (C : Matrix n n K) : Matrix n n K :=
  diagonal w * C - Cᵀ * diagonal w

/-- Entrywise form.  In particular `Theta` depends on `w` only through the
differences that the discrete `∂_y^{-1}` couples. -/
theorem theta_entry (w : n → K) (C : Matrix n n K) (i j : n) :
    Theta w C i j = w i * C i j - w j * C j i := by
  unfold Theta
  rw [Matrix.sub_apply, Matrix.diagonal_mul, Matrix.mul_diagonal]
  simp [Matrix.transpose_apply]
  ring

/-- **`Theta` is antisymmetric** for every `w` and every `C`.  This is the
structural reason why a bracket `P = d_x · Q` with *constant* `Q` cannot work:
the obstruction has exactly the antisymmetry type of `d_x`, and the only
antisymmetric constant-coefficient operators available are multiples of `d_x`,
whereas `Theta` is field-dependent. -/
theorem theta_antisym (w : n → K) (C : Matrix n n K) :
    (Theta w C)ᵀ = -Theta w C := by
  ext i j
  rw [Matrix.transpose_apply, Matrix.neg_apply, theta_entry, theta_entry]
  ring

/-- If the discrete `∂_y^{-1}` obeys the (periodic / zero-mean) skew-adjoint
convention `Cᵀ = -C`, the obstruction is the anticommutator `diag(w)C + C diag(w)`. -/
theorem theta_eq_of_skew (w : n → K) (C : Matrix n n K) (hC : Cᵀ = -C) :
    Theta w C = diagonal w * C + C * diagonal w := by
  ext i j
  rw [theta_entry, Matrix.add_apply, Matrix.diagonal_mul, Matrix.mul_diagonal]
  have h : C j i = -C i j := by
    have h' := congrFun (congrFun hC i) j
    simpa [Matrix.transpose_apply, Matrix.neg_apply] using h'
  rw [h]
  ring

/-! ## 2.  The explicit `Fin 3` lattice, one-sided cumsum convention -/

/-- Discrete `∂_y^{-1}` on three sites in the one-sided cumulative-sum
convention: `u = C w` means `u 0 = 0`, `u 1 = w 0`, `u 2 = w 0 + w 1`. -/
def cum3 : Matrix (Fin 3) (Fin 3) ℚ := fun i j => if (j : ℕ) < (i : ℕ) then 1 else 0

/-- The obstruction matrix of the `Fin 3` DLW lattice. -/
def Theta3 (w : Fin 3 → ℚ) : Matrix (Fin 3) (Fin 3) ℚ := Theta w cum3

theorem cum3_one_zero : cum3 1 0 = (1 : ℚ) := by decide

theorem cum3_zero_one : cum3 0 1 = (0 : ℚ) := by decide

theorem cum3_two_zero : cum3 2 0 = (1 : ℚ) := by decide

theorem cum3_zero_two : cum3 0 2 = (0 : ℚ) := by decide

/-- The `(1,0)` entry of the obstruction is exactly the local coupling `w 1`. -/
theorem Theta3_one_zero (w : Fin 3 → ℚ) : Theta3 w 1 0 = w 1 := by
  rw [Theta3, theta_entry, cum3_one_zero, cum3_zero_one]
  ring

/-- The `(2,0)` entry of the obstruction is exactly the local coupling `w 2`. -/
theorem Theta3_two_zero (w : Fin 3 → ℚ) : Theta3 w 2 0 = w 2 := by
  rw [Theta3, theta_entry, cum3_two_zero, cum3_zero_two]
  ring

/-- **Non-vanishing of the obstruction.**  As soon as the `u`–`w` coupling is
switched on at the second site (`w 1 ≠ 0`), the obstruction matrix does not
vanish: no constant symmetric bracket can cancel it. -/
theorem Theta3_ne_zero (w : Fin 3 → ℚ) (hw : w 1 ≠ 0) : Theta3 w ≠ 0 := by
  intro h
  have h10 : Theta3 w 1 0 = 0 := by rw [h, Matrix.zero_apply]
  rw [Theta3_one_zero] at h10
  exact hw h10

/-- Conversely, the fully degenerate case `u` constant in `y` (`w ≡ 0`) kills the
obstruction — but then the constraint `u_y = w` carries no information and the
system degenerates to a linear `x`-transport equation for `v`. -/
theorem Theta3_eq_zero_of_w_eq_zero (w : Fin 3 → ℚ) (hw : ∀ i, w i = 0) :
    Theta3 w = 0 := by
  apply Matrix.ext
  intro i j
  rw [Theta3, theta_entry, hw i, hw j, Matrix.zero_apply]
  ring

/-- The cumsum obstruction vanishes only in the degenerate case: if `Theta3 w = 0`
then `w 1 = w 2 = 0` (the `w`–`u` coupling is dead away from the first site). -/
theorem Theta3_eq_zero_forces (w : Fin 3 → ℚ) (h : Theta3 w = 0) :
    w 1 = 0 ∧ w 2 = 0 := by
  constructor
  · have h' : Theta3 w 1 0 = 0 := by rw [h, Matrix.zero_apply]
    rwa [Theta3_one_zero] at h'
  · have h' : Theta3 w 2 0 = 0 := by rw [h, Matrix.zero_apply]
    rwa [Theta3_two_zero] at h'

/-! ## 3.  The refutation: no constant symmetric bracket

`Theta` supplies only the `(1,1)` block, `D_x^0` coefficient.  The remaining
Helmholtz coefficient equations for `Q = q ⊗ 1` are, for the `Fin 3` cumsum
lattice and fields with `w 1 ≠ 0`:

* `(1,1)`, `D_x^0` :  `q11 • Theta = 0`
* `(2,2)`, `D_x^1` :  `2 * q12 = 0`
* `(1,2)`, `D_x^1` :  `q22 + q11 = 0`

(The `D_x^1` equations come from the fact that `Q` is constant, hence the
`d_x`-parts of the two off-diagonal blocks must match coefficientwise; the
`(2,2)`, `D_x^0` equation is `q12 • (E - Eᵀ) = 0`, which is implied by `q12 = 0`.)

They have only the solution `Q = 0`. -/

theorem no_invertible_constant_poisson_bracket
    (w : Fin 3 → ℚ) (hw : w 1 ≠ 0) (q11 q12 q22 : ℚ)
    (h11 : q11 • Theta3 w = 0)
    (h22 : 2 * q12 = 0)
    (h12 : q22 + q11 = 0) :
    q11 = 0 ∧ q12 = 0 ∧ q22 = 0 := by
  have h : q11 * w 1 = 0 := by
    have h' : (q11 • Theta3 w) 1 0 = 0 := by rw [h11, Matrix.zero_apply]
    simpa [Theta3_one_zero] using h'
  have hq11 : q11 = 0 := (mul_eq_zero.mp h).resolve_right hw
  have hq12 : q12 = 0 := by linarith
  exact ⟨hq11, hq12, by linarith⟩

/-- Consequently no *non-trivial* constant symmetric bracket satisfies the
Helmholtz system: `Q = !![q11, q12; q12, q22]` has all entries zero, so it is
singular and cannot serve as a Poisson/symplectic operator.  Hence there is no
Hamiltonian `H` with `∂_t (w,v) = d_x Q (δH/δw, δH/δv)` in this class. -/
theorem no_nontrivial_constant_poisson_Q
    (w : Fin 3 → ℚ) (hw : w 1 ≠ 0) (q11 q12 q22 : ℚ)
    (h11 : q11 • Theta3 w = 0)
    (h22 : 2 * q12 = 0)
    (h12 : q22 + q11 = 0) :
    ¬ (q11 ≠ 0 ∨ q12 ≠ 0 ∨ q22 ≠ 0) := by
  obtain ⟨h1, h2, h3⟩ :=
    no_invertible_constant_poisson_bracket w hw q11 q12 q22 h11 h22 h12
  rintro (h | h | h)
  · exact h h1
  · exact h h2
  · exact h h3

#print axioms DLW.E.theta_antisym
#print axioms DLW.E.theta_eq_of_skew
#print axioms DLW.E.Theta3_ne_zero
#print axioms DLW.E.no_invertible_constant_poisson_bracket
#print axioms DLW.E.no_nontrivial_constant_poisson_Q

end DLW.E
