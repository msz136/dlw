/-
Copyright: formal companion to the GSG/DLW semi-discretization project.

# The `y`-rate of the staggered lattice (the `P`-direction of T1)

The staggered construction replaces the continuum plane-wave factor `e^{P y}` by the
two-sided geometric sequence with multiplier

`χ = mobiusRate P (h/2) = (P + h/2) / (P - h/2)`,

whose **logarithmic rate** is `(1/h)·log χ`.  The continuum rate is `P`, i.e. the
logarithmic derivative of `e^{P y}`.

This file formalises two statements:

* `lattice_rate_tendsto` : `(1/h)·log χ → 1/P` as `h → 0`.  This is the `y`-direction
  half of T1: the discrete rate converges to the continuum rate.
* `lattice_rate_centred_exact` : the *centred* (Cayley / logarithmic-derivative) form of
  the discrete rate is `1/P` **exactly**, for every `h` — the discrete `y`-rate carries no
  error at all once written in centred form.  Equivalently, the `[1/1]` Padé multiplier is
  the unique rational approximation whose centred rate is exact.

Both build on the Möbius multiplier `DLW.mobiusRate` of `TodaFormalization/DLWDiscretePair.lean`.
-/
import TodaFormalization.DLWDiscretePair
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.Calculus.Deriv.Slope

open Topology Filter Asymptotics

namespace DLW

/-! ## 1. The logarithmic lattice rate converges to the continuum rate -/

/-- **T1, `y`-direction.**  The logarithmic rate `(1/h)·log χ` of the lattice multiplier
`χ = (P + h/2)/(P - h/2)` tends to the continuum rate `1/P`.

The proof is a single derivative: the function `h ↦ log χ(h)` vanishes at `h = 0` and has
derivative `1/P` there, so its slope through the origin converges to `1/P`. -/
theorem lattice_rate_tendsto (P : ℝ) (hP : P ≠ 0) :
    Tendsto (fun h : ℝ => (1 / h) * Real.log ((P + h / 2) / (P - h / 2)))
      (𝓝[≠] (0 : ℝ)) (𝓝 (1 / P)) := by
  have hnum : HasDerivAt (fun h : ℝ => P + h / 2) (1 / 2) (0 : ℝ) := by
    have h1 : HasDerivAt (fun h : ℝ => h / 2) (1 / 2) (0 : ℝ) :=
      (hasDerivAt_id (0 : ℝ)).div_const 2
    simpa [add_comm] using h1.add_const P
  have hden : HasDerivAt (fun h : ℝ => P - h / 2) (-(1 / 2)) (0 : ℝ) := by
    have h1 : HasDerivAt (fun h : ℝ => h / 2) (1 / 2) (0 : ℝ) :=
      (hasDerivAt_id (0 : ℝ)).div_const 2
    simpa using h1.const_sub P
  have hquot : HasDerivAt (fun h : ℝ => (P + h / 2) / (P - h / 2))
      (((1 / 2) * (P - 0 / 2) - (P + 0 / 2) * (-(1 / 2))) / (P - 0 / 2) ^ 2) (0 : ℝ) :=
    hnum.div hden (by simpa using hP)
  have hlog : HasDerivAt (fun h : ℝ => Real.log ((P + h / 2) / (P - h / 2)))
      ((((1 / 2) * (P - 0 / 2) - (P + 0 / 2) * (-(1 / 2))) / (P - 0 / 2) ^ 2)
        / ((P + 0 / 2) / (P - 0 / 2))) (0 : ℝ) :=
    hquot.log (by
      simp only [zero_div, add_zero, sub_zero]
      exact div_ne_zero hP hP)
  have hderiv : HasDerivAt (fun h : ℝ => Real.log ((P + h / 2) / (P - h / 2)))
      (1 / P) (0 : ℝ) := by
    convert hlog using 1
    field_simp
    try ring
  have hH0 : Real.log ((P + 0 / 2) / (P - 0 / 2)) = 0 := by
    simp [hP]
  refine Tendsto.congr' ?_ hderiv.tendsto_slope_zero
  filter_upwards with h
  simp only [zero_add, hH0, sub_zero, smul_eq_mul, one_div]

/-! ## 2. The centred rate is exact at finite `h` -/

/-- **The centred lattice rate equals the continuum rate exactly.**

Writing the lattice multiplier as `χ = mobiusRate P d = (P + d)/(P - d)` with half-step
`d = h/2`, its centred (Cayley / logarithmic-derivative) rate `(χ - 1)/(d(χ + 1))` is
*identically* `1/P`, for every `d` — no error term at all.  This is the exact form of
"the discrete `y`-rate agrees with the continuum rate". -/
theorem lattice_rate_centred_exact (P d : ℝ) (hP : P ≠ 0) (hd : P - d ≠ 0) (hd0 : d ≠ 0) :
    (mobiusRate P d - 1) / (d * (mobiusRate P d + 1)) = 1 / P := by
  have hnum : mobiusRate P d - 1 = 2 * d / (P - d) := by
    unfold mobiusRate
    field_simp
    ring
  have hden : mobiusRate P d + 1 = 2 * P / (P - d) := by
    unfold mobiusRate
    field_simp
    ring
  rw [hnum, hden]
  field_simp
  try ring

/-- The same exactness statement in the `h`-variable used by the staggered scheme:
the two walls sit at `a ± h/2`, so the half-step is `d = h/2` and the centred rate is
`2(χ - 1) / (h(χ + 1)) = 1/P`. -/
theorem lattice_rate_centred_exact_h (P h : ℝ) (hP : P ≠ 0) (hh : h ≠ 0)
    (hd : P - h / 2 ≠ 0) :
    2 * (mobiusRate P (h / 2) - 1) / (h * (mobiusRate P (h / 2) + 1)) = 1 / P := by
  have hd2 : P * 2 - h ≠ 0 := by
    intro hcon
    exact hd (by linarith)
  have hkey : P - h / 2 = (P * 2 - h) / 2 := by ring
  have hnum : mobiusRate P (h / 2) - 1 = h / (P - h / 2) := by
    unfold mobiusRate
    rw [hkey]
    field_simp
    ring
  have hden : mobiusRate P (h / 2) + 1 = 2 * P / (P - h / 2) := by
    unfold mobiusRate
    rw [hkey]
    field_simp
    ring
  -- the half-step `h/2` is nonzero, and `χ + 1 = 2P/(P - h/2)` is nonzero too, so the
  -- denominator `(h/2)·(χ + 1)` of the centred form is nonzero
  have hhalf : h / 2 ≠ 0 := by
    intro hcon
    exact hh (by linarith)
  have hY : mobiusRate P (h / 2) + 1 ≠ 0 := by
    rw [hden]
    exact div_ne_zero (mul_ne_zero (by norm_num) hP) hd
  have hX : h / 2 * (mobiusRate P (h / 2) + 1) ≠ 0 := mul_ne_zero hhalf hY
  -- doubling numerator and denominator changes nothing
  have hscale : 2 * (mobiusRate P (h / 2) - 1) / (2 * (h / 2 * (mobiusRate P (h / 2) + 1)))
      = (mobiusRate P (h / 2) - 1) / (h / 2 * (mobiusRate P (h / 2) + 1)) := by
    field_simp
    try ring
  have hargs : h * (mobiusRate P (h / 2) + 1)
      = 2 * (h / 2 * (mobiusRate P (h / 2) + 1)) := by ring
  rw [hargs, hscale]
  exact lattice_rate_centred_exact P (h / 2) hP hd hhalf

end DLW
