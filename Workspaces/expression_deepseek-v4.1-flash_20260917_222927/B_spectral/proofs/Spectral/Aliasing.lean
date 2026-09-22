/-
  Direction B — spectral / pseudo-spectral semidiscretisation of the DLW system.
  Module 3: aliasing, quantified, and the pseudo-spectral refutation.

  Setting.  A pseudo-spectral (collocation) scheme evaluates the quadratic
  nonlinearities of the DLW system by pointwise multiplication on a grid.  On an
  `M`-point uniform grid, a mode of frequency `l` and a mode of frequency
  `l + M t` have *identical samples* (`sample_alias`); that is the whole content
  of aliasing.  Consequently, whenever the product of two retained modes produces
  a frequency outside the retained band `-N..N` but congruent to a retained one
  modulo `M = 2N+1`, the pseudo-spectral evaluation contaminates a retained mode
  by an amount of the same order as the retained data — an O(1) relative error,
  not a small truncation error.

  What is formalised here:

  * `sample_alias` — the general aliasing identity on an `M`-point grid.
  * `out_of_band_folds_into_band` — the general arithmetic: every product
    frequency `f` with `N < f ≤ 2N` differs from an in-band frequency by exactly
    `M = 2N+1`, so the retained band *is* contaminated for every `N ≥ 1`.
  * the explicit `N = 1`, `M = 3` instance: the product `e^{iy} · e^{iy}` has
    frequency `2` (out of band) which is indistinguishable on the grid from the
    in-band mode `-1` (`three_point_collision`).
  * `aliasing_breaks_projected_identity` — **refutation**: the pseudo-spectral
    mode-`-1` projection of that product is non-zero (`3` before the `1/M`
    normalisation), while the dealiased / exact Galerkin value — reproduced
    exactly by the padded grid with `M = 3N+1 = 4` points — is `0`.  So the
    projected nonlinear identity is *destroyed* by aliasing, and any claim that
    an unpadded pseudo-spectral scheme preserves it is false.

  Scope.  The DLW nonlinearities `u u_xy`, `u_x u_y`, `(u v)_x` are all
  quadratic in the field variables (with `x`-derivatives that commute with the
  `y`-mode decomposition), so this quadratic analysis covers all of them.
-/
import Mathlib.Basic.Complex.Basic
import Mathlib.RingTheory.RootsOfUnity.Complex
import Mathlib.RingTheory.RootsOfUnity.PrimitiveRoots
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic

namespace DLW.Spectral

open scoped BigOperators

/-! ## General aliasing identity -/

/-- **Aliasing.**  Let `ζ` be a primitive `M`-th root of unity, i.e. the Fourier
    kernel of an `M`-point uniform grid.  Then for every grid index `j` the
    samples of the mode of frequency `l + M t` and of the mode of frequency `l`
    coincide.  Hence an `M`-point grid cannot distinguish them. -/
theorem sample_alias {M : ℕ} {ζ : ℂ} (hζ : IsPrimitiveRoot ζ M) (l t j : ℕ) :
    ζ ^ ((l + M * t) * j) = ζ ^ (l * j) := by
  have hzero : ζ ^ ((M * t) * j) = 1 := by
    rw [show (M * t) * j = M * (t * j) from by ring, pow_mul, hζ.pow_eq_one, one_pow]
  rw [add_mul, pow_add, hzero, mul_one]

/-! ## General arithmetic: out-of-band product frequencies fold into the band -/

/-- **Where the contamination lands.**  With `M = 2N+1` grid points and retained
    band `-N..N`, every frequency `f` with `N < f ≤ 2N` — exactly the range hit
    by the product of two retained modes — differs from an in-band frequency
    `i ∈ {-N,...,-1}` by precisely a multiple of `M`.  By `sample_alias` the grid
    cannot tell `f` from `i`, so mode `i` of the retained band is contaminated
    whenever the nonlinearity has frequency-`f` content. -/
theorem out_of_band_folds_into_band (N : ℕ) (f : ℤ)
    (h1 : (N : ℤ) + 1 ≤ f) (h2 : f ≤ 2 * N) :
    ∃ i : ℤ,
      i = f - (2 * (N : ℤ) + 1) ∧ f = i + (2 * (N : ℤ) + 1)
        ∧ -(N : ℤ) ≤ i ∧ i ≤ -1 :=
  ⟨f - (2 * (N : ℤ) + 1), rfl, by ring, by omega, by omega⟩

/-! ## The explicit `N = 1`, `M = 3` instance -/

/-- The cube root of unity generating the 3-point grid. -/
noncomputable def omega3 : ℂ := Complex.exp (2 * Real.pi * Complex.I / 3)

theorem omega3_primitive : IsPrimitiveRoot omega3 3 :=
  Complex.isPrimitiveRoot_exp 3 (by norm_num)

theorem omega3_cube : omega3 ^ 3 = 1 := omega3_primitive.pow_eq_one

/-- On the 3-point grid, the double frequency `2` and the mode `-1` are
    indistinguishable.  The mode `-1` is written with the positive exponent
    `3 - j`, which is its representative for `j ∈ {0,1,2}`. -/
theorem three_point_collision (j : ℕ) (hj : j < 3) :
    omega3 ^ (2 * j) = omega3 ^ (3 - j) := by
  interval_cases j
  · rw [show (3 - 0 : ℕ) = 3 from rfl, omega3_cube]
    simp
  · norm_num
  · rw [show (2 * 2 : ℕ) = 4 from rfl, show (3 - 2 : ℕ) = 1 from rfl,
      show omega3 ^ (4 : ℕ) = omega3 ^ 3 * omega3 from by ring,
      omega3_cube, one_mul, pow_one]

/-- The product of the two retained modes `+1` with itself carries the
    out-of-band frequency `2`, which differs from the retained mode `-1` by
    exactly the grid size `3`. -/
theorem alias_offset : ((3 : ℤ) ∣ (2 - (-1))) := by norm_num

/-! ## Powers of `I` on the padded 4-point grid -/

theorem I_pow_four : Complex.I ^ (4 : ℕ) = 1 := Complex.isPrimitiveRoot_I.pow_eq_one

theorem I_pow_three : Complex.I ^ (3 : ℕ) = -Complex.I := by
  rw [show (3 : ℕ) = 2 + 1 from rfl, pow_add, pow_two, pow_one, Complex.I_mul_I]
  ring

theorem I_pow_six : Complex.I ^ (6 : ℕ) = -1 := by
  rw [show (6 : ℕ) = 4 + 2 from rfl, pow_add, I_pow_four, pow_two, Complex.I_mul_I]
  ring

theorem I_pow_nine : Complex.I ^ (9 : ℕ) = Complex.I := by
  rw [show (9 : ℕ) = 8 + 1 from rfl, pow_add, pow_one,
    show (8 : ℕ) = 4 * 2 from rfl, pow_mul, I_pow_four]
  ring

/-! ## The projected coefficient of `e^{iy} · e^{iy}` at mode `-1` -/

/-- Pseudo-spectral evaluation on the 3-point grid, unnormalised: the mode-`-1`
    projection of the product `e^{iy} · e^{iy}` is `3`, i.e. coefficient `1`
    after the `1/M` normalisation.  The exact value is `0`. -/
theorem three_point_sum :
    (∑ j ∈ Finset.range 3, omega3 ^ (2 * j) * omega3 ^ j) = 3 := by
  have h0 : omega3 ^ (2 * 0) * omega3 ^ 0 = 1 := by simp
  have h1 : omega3 ^ (2 * 1) * omega3 ^ 1 = 1 := by
    rw [show (2 * 1 : ℕ) = 2 from rfl, ← pow_add, show (2 + 1 : ℕ) = 3 from rfl,
      omega3_cube]
  have h2 : omega3 ^ (2 * 2) * omega3 ^ 2 = 1 := by
    rw [show (2 * 2 : ℕ) = 4 from rfl, ← pow_add, show (4 + 2 : ℕ) = 6 from rfl,
      show (6 : ℕ) = 3 * 2 from rfl, pow_mul, omega3_cube]
    norm_num
  rw [Finset.sum_range_succ, Finset.sum_range_succ, Finset.sum_range_succ,
    Finset.sum_range_zero, h0, h1, h2]
  norm_num

/-- The same computation on the padded 4-point grid `M = 3N + 1 = 4`, which is
    alias-free for the quadratic nonlinearity at `N = 1`: the value is `0`, which
    is the exact Galerkin coefficient of the mode `-1` of `e^{2iy}`. -/
theorem four_point_sum :
    (∑ j ∈ Finset.range 4, Complex.I ^ (2 * j) * Complex.I ^ j) = 0 := by
  have h0 : Complex.I ^ (2 * 0) * Complex.I ^ 0 = 1 := by simp
  have h1 : Complex.I ^ (2 * 1) * Complex.I ^ 1 = -Complex.I := by
    rw [show (2 * 1 : ℕ) = 2 from rfl, ← pow_add, show (2 + 1 : ℕ) = 3 from rfl,
      I_pow_three]
  have h2 : Complex.I ^ (2 * 2) * Complex.I ^ 2 = -1 := by
    rw [show (2 * 2 : ℕ) = 4 from rfl, ← pow_add, show (4 + 2 : ℕ) = 6 from rfl,
      I_pow_six]
  have h3 : Complex.I ^ (2 * 3) * Complex.I ^ 3 = Complex.I := by
    rw [show (2 * 3 : ℕ) = 6 from rfl, ← pow_add, show (6 + 3 : ℕ) = 9 from rfl,
      I_pow_nine]
  rw [Finset.sum_range_succ, Finset.sum_range_succ, Finset.sum_range_succ,
    Finset.sum_range_succ, Finset.sum_range_zero, h0, h1, h2, h3]
  ring

/-- **REFUTATION — aliasing destroys the projected identity.**  For the same
    quadratic nonlinearity and the same retained mode `-1`, the un-dealiased
    3-point pseudo-spectral projection is non-zero while the alias-free padded
    projection (= the exact Galerkin coefficient) is zero.  Therefore an
    un-dealiased pseudo-spectral scheme does not solve the Fourier–Galerkin
    projection of the DLW system; it solves a different problem, and the
    difference is of the same order as the data. -/
theorem aliasing_breaks_projected_identity :
    (∑ j ∈ Finset.range 3, omega3 ^ (2 * j) * omega3 ^ j)
      ≠ (∑ j ∈ Finset.range 4, Complex.I ^ (2 * j) * Complex.I ^ j) := by
  rw [three_point_sum, four_point_sum]
  norm_num

end DLW.Spectral
