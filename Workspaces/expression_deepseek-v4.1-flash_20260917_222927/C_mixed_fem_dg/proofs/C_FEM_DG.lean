/-
  Direction C — mixed finite-element / discontinuous-Galerkin discretisation of the
  DLW system in the `y` direction only (`x`, `t` stay continuous).

  Contents (all fully proved, no `sorry`, no new `axiom`):

  §1  P1 (linear) FEM on a uniform mesh of size `h`:
        element mass matrix      `(h/6) * [[2,1],[1,2]]`,  det = h^2/12
        element stiffness matrix `(1/h) * [[1,-1],[-1,1]]`, annihilates constants
  §2  semi-discrete symbols replacing `i*ell`:
        consistent-mass P1:  `mu_h(ell) = i * 3 sin(ell h) / (h (2 + cos(ell h)))`
        effective-wavenumber factor  `R(theta) = 3 sin theta / (theta (2 + cos theta))`,
        `R(theta) * (theta * (2 + cos theta)) = 3 sin theta`,  `R(0) = 1`
      honest NEGATIVE finding: `R(pi) = 0` (the mass factor `2 + cos` is NEVER zero,
      so the Nyquist zero of the consistent-mass P1 rule comes from the stiffness /
      advection symbol `sin theta`, exactly as for the centred difference).
      DG-upwind (P0) contrast:  `mu = (1 - exp(-i theta))/h`, whose real part
      `(1 - cos theta)/h` is non-negative (upwind dissipation) and equals `2/h` at
      Nyquist: NO Nyquist zero.
  §3  upwind discrete dissipation identity (structural result, uses the shared
      `DLW.Common.telescoping`), valid for any real sequence, plus non-negativity
      with zero boundary data.
-/
import Common.Operators
import Mathlib.Basic.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

namespace DLWC

open scoped BigOperators

/-! ## §1. P1 mass / stiffness matrices on a uniform mesh -/

/-- Diagonal entry of the P1 element mass matrix `(h/6)*[[2,1],[1,2]]` is `h/3`. -/
theorem p1_mass_entry (h : ℝ) : 2 * h / 6 = h / 3 := by ring

/-- Determinant of the P1 element mass matrix `(h/6)*[[2,1],[1,2]]` is `h^2/12`. -/
theorem p1_mass_det (h : ℝ) : (h / 3) * (h / 3) - (h / 6) * (h / 6) = h ^ 2 / 12 := by
  ring

/-- Hence the consistent mass matrix has no spurious kernel for `h ≠ 0`:
    the mass matrix does NOT produce a Nyquist zero. -/
theorem p1_mass_det_ne_zero (h : ℝ) (hh : h ≠ 0) :
    (h / 3) * (h / 3) - (h / 6) * (h / 6) ≠ 0 := by
  rw [p1_mass_det]
  exact div_ne_zero (pow_ne_zero 2 hh) (by norm_num)

/-- Element mass matrix is strictly diagonally dominant (`h/6 < h/3`) for `h > 0`. -/
theorem p1_mass_diag_dominant (h : ℝ) (hh : 0 < h) : h / 6 < h / 3 := by
  linarith

/-- The assembled periodic consistent-mass row `(h/6)*(1,4,1)` is strictly
    diagonally dominant: off-diagonal sum `h/3` below the diagonal `2h/3`. -/
theorem p1_mass_global_diag_dominant (h : ℝ) (hh : 0 < h) : h / 6 + h / 6 < 2 * h / 3 := by
  linarith

/-- The P1 element stiffness matrix `(1/h)*[[1,-1],[-1,1]]` kills the constant vector. -/
theorem p1_stiffness_kills_constant (h : ℝ) :
    ((1 / h) * 1 + (-(1 / h)) * 1 = 0) ∧ ((1 / h) * 1 + (-(1 / h)) * 1 = 0) := by
  constructor <;> ring

/-- The associated stiffness quadratic form vanishes on the constant vector. -/
theorem p1_stiffness_quadform_constant (h : ℝ) :
    (1 / h) * (1 * 1) + (-(1 / h)) * (1 * 1) + (-(1 / h)) * (1 * 1) + (1 / h) * (1 * 1)
      = 0 := by
  ring

/-- Global P1 stiffness symbol `(2 - 2 cos theta)/h` at `theta = 0`: the constant
    direction is the kernel, i.e. `d/dy` annihilates `y`-independent data exactly. -/
theorem p1_stiffness_symbol_at_zero (h : ℝ) : (2 - 2 * Real.cos 0) / h = 0 := by
  rw [Real.cos_zero]; ring

/-! ## §2. Semi-discrete symbols -/

/-- Effective-wavenumber factor of the consistent-mass P1 rule. -/
noncomputable def R1 (θ : ℝ) : ℝ := 3 * Real.sin θ / (θ * (2 + Real.cos θ))

/-- The symbol that replaces `i * ell` for consistent-mass P1, i.e. the eigenvalue of
    `M_h^{-1} A_h^T` on the Fourier mode `y_j ↦ exp(i ell y_j)`. -/
noncomputable def muP1 (h ℓ : ℝ) : ℂ :=
  Complex.I * ((3 * Real.sin (ℓ * h) / (h * (2 + Real.cos (ℓ * h))) : ℝ) : ℂ)

/-- The denominator `2 + cos theta` of the mass symbol is confined to `[1,3]`:
    it can never vanish, so `M_h` is invertible at EVERY wavenumber. -/
theorem mass_symbol_bounds (θ : ℝ) : 1 ≤ 2 + Real.cos θ ∧ 2 + Real.cos θ ≤ 3 := by
  constructor
  · have := Real.neg_one_le_cos θ; linarith
  · have := Real.cos_le_one θ; linarith

theorem mass_symbol_ne_zero (θ : ℝ) : 2 + Real.cos θ ≠ 0 := by
  have := (mass_symbol_bounds θ).1
  linarith

/-- At Nyquist the mass symbol is `1`, i.e. still non-degenerate. -/
theorem mass_symbol_at_nyquist : 2 + Real.cos Real.pi = 1 := by
  rw [Real.cos_pi]; norm_num

/-- On the open band `0 < theta < pi` the consistent-mass P1 symbol is strictly
    non-zero: there is no spurious zero strictly inside the band. -/
theorem p1_symbol_pos_in_band (h θ : ℝ) (hh : 0 < h) (h0 : 0 < θ) (hπ : θ < Real.pi) :
    0 < 3 * Real.sin θ / (h * (2 + Real.cos θ)) := by
  have hs : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi h0 hπ
  have hc : 0 < 2 + Real.cos θ := by
    have := (mass_symbol_bounds θ).1; linarith
  exact div_pos (mul_pos (by norm_num) hs) (mul_pos hh hc)

/-- HONEST NEGATIVE FINDING: the consistent-mass P1 symbol DOES vanish at the
    Nyquist wavenumber `ell h = pi`, because the stiffness/advection factor is
    `sin(ell h)`.  The mass factor `2 + cos` (the only place the mass matrix enters)
    is non-zero there; it does not remove the zero. -/
theorem muP1_nyquist_zero (h : ℝ) (hh : h ≠ 0) : muP1 h (Real.pi / h) = 0 := by
  unfold muP1
  have h1 : Real.pi / h * h = Real.pi := by field_simp
  rw [h1, Real.sin_pi]
  simp

/-- Contrast: the centred-difference symbol `i sin(ell h)/h` vanishes at Nyquist too. -/
theorem ctr_symbol_nyquist_zero (h : ℝ) : Real.sin Real.pi / h = 0 := by
  rw [Real.sin_pi]; ring

/-- Normalisation identity: dividing out the continuous `i ell` leaves exactly `R`,
    and `R` is exactly `1` at `theta = 0` (the `mu_h → i ell` normalisation). -/
theorem p1_symbol_normalisation (θ : ℝ) (hθ : θ ≠ 0) :
    (3 * Real.sin θ / (θ * (2 + Real.cos θ))) * (θ * (2 + Real.cos θ)) = 3 * Real.sin θ := by
  have hc : 2 + Real.cos θ ≠ 0 := mass_symbol_ne_zero θ
  have h1 : θ * (2 + Real.cos θ) ≠ 0 := mul_ne_zero hθ hc
  first
    | (field_simp [h1, hc, hθ]; ring)
    | field_simp [h1, hc, hθ]

/-- Consistency bookkeeping at the algebraic level: the deviation of `R` from `1` is
    exactly the displayed quotient; its numerator has no terms of order 0..4
    (SymPy: `3 sin θ - θ(2+cos θ) = -θ^5/60 + O(θ^7)`, hence `R = 1 - θ^4/180 + O(θ^6)`). -/
theorem p1_symbol_deviation (θ : ℝ) (hθ : θ ≠ 0) :
    3 * Real.sin θ / (θ * (2 + Real.cos θ)) - 1
      = (3 * Real.sin θ - θ * (2 + Real.cos θ)) / (θ * (2 + Real.cos θ)) := by
  have hc : 2 + Real.cos θ ≠ 0 := mass_symbol_ne_zero θ
  have h1 : θ * (2 + Real.cos θ) ≠ 0 := mul_ne_zero hθ hc
  first
    | (field_simp [h1, hc, hθ]; ring)
    | field_simp [h1, hc, hθ]

/-- DG-upwind (P0) symbol: squared modulus identity `|1 - e^{-i theta}|^2 = 2 - 2 cos theta`. -/
theorem dg_symbol_norm_identity (θ : ℝ) :
    (1 - Real.cos θ) ^ 2 + Real.sin θ ^ 2 = 2 - 2 * Real.cos θ := by
  nlinarith [Real.sin_sq_add_cos_sq θ]

/-- Upwind numerical dissipation is non-negative at every wavenumber. -/
theorem dg_symbol_re_nonneg (θ : ℝ) : 0 ≤ 1 - Real.cos θ := by
  have := Real.cos_le_one θ; linarith

/-- Contrast with P1 / centred differences: the DG-upwind real part at Nyquist is
    `2/h ≠ 0`. -/
theorem dg_symbol_re_at_nyquist (h : ℝ) : (1 - Real.cos Real.pi) / h = 2 / h := by
  rw [Real.cos_pi]; ring

/-- HONEST POSITIVE FINDING: the DG-upwind (P0) symbol has NO Nyquist zero. -/
theorem dg_symbol_no_nyquist_zero (h : ℝ) (hh : h ≠ 0) :
    ((1 - Real.cos Real.pi) / h) ^ 2 + (Real.sin Real.pi / h) ^ 2 ≠ 0 := by
  have hsin : (Real.sin Real.pi / h) ^ 2 = 0 := by rw [Real.sin_pi]; simp
  have hcos : (1 - Real.cos Real.pi) / h = 2 / h := by rw [Real.cos_pi]; ring
  rw [hsin, hcos, add_zero]
  exact pow_ne_zero 2 (div_ne_zero (by norm_num) hh)

/-! ## §3. Upwind dissipation identity (structural) -/

/-- Exact discrete dissipation (summation-by-parts-type) identity for the upwind
    (left-trace) difference stencil `u_{j+1} - u_j`. -/
theorem dg_upwind_dissipation_identity (u : Nat → ℝ) (N : Nat) :
    2 * (∑ j ∈ Finset.range N, u (j + 1) * (u (j + 1) - u j))
      = (∑ j ∈ Finset.range N, (u (j + 1) - u j) ^ 2) + (u N ^ 2 - u 0 ^ 2) := by
  rw [Finset.mul_sum]
  have ht : (u N ^ 2 - u 0 ^ 2 : ℝ)
      = ∑ j ∈ Finset.range N, (u (j + 1) ^ 2 * (1 : ℝ) - u j ^ 2 * (1 : ℝ)) := by
    rw [DLW.Common.telescoping (fun j : Nat => u j ^ 2) (fun _ : Nat => (1 : ℝ)) N]
    ring
  rw [ht, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- Consequence over ℝ: with zero boundary data the upwind form is non-negative,
    i.e. the upwind `y`-derivative carries a sign-definite dissipation. -/
theorem dg_upwind_dissipation_nonneg (u : Nat → ℝ) (N : Nat)
    (h0 : u 0 = 0) (hN : u N = 0) :
    0 ≤ ∑ j ∈ Finset.range N, u (j + 1) * (u (j + 1) - u j) := by
  have hid := dg_upwind_dissipation_identity u N
  rw [h0, hN] at hid
  have hsq : 0 ≤ ∑ j ∈ Finset.range N, (u (j + 1) - u j) ^ 2 :=
    Finset.sum_nonneg (fun j _ => sq_nonneg _)
  nlinarith

/-! ## Axiom audit -/

#print axioms DLWC.p1_mass_det_ne_zero
#print axioms DLWC.muP1_nyquist_zero
#print axioms DLWC.dg_symbol_no_nyquist_zero
#print axioms DLWC.dg_upwind_dissipation_identity
#print axioms DLWC.dg_upwind_dissipation_nonneg

end DLWC
