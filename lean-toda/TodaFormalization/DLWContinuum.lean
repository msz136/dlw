/-
Copyright: formal companion to the GSG/DLW semi-discretization project.

# The analytic (T1) layer for the staggered DLW bilinear pair

`TodaFormalization/DLWDiscretePair.lean` proves the *exact, finite-`h`* content of the
staggered construction: the discrete bilinear pair `(6)_h`, `(7)_h` and the algebraic
identities that make the two equations share one `τ`-matrix.  That file is pure algebra.

This file adds the **continuum limit** layer, i.e. the statement that as `h → 0` the
discrete pair really does collapse onto the original continuum pair.  Two things are
formalised.

## 1. The analytic bridge

Everything analytic reduces to one one-variable fact: a `C⁴` function agrees with its
third-order Taylor jet at `Y` to `O(u⁴)`:

* `taylor_jet3_isBigO`, and its two shifted forms `jet3_half_isBigO`, `jet3_negHalf_isBigO`
  (offsets `+h/2`, `-h/2`, i.e. the two cell walls `a ± h/2`).

Two elementary order lemmas drive all the bookkeeping:

* `pow_isBigO_pow` : higher powers are `O` of lower powers near `0`;
* `div_id_of_isBigO_cube` : an `O(h³)` remainder divided by `h` is an `O(h²)` remainder.

## 2. The two template reductions (T1)

With `P` (the `B_a f·g` slot) and `Q` (the `D_x f·g` slot) both `C⁴` at the cell centre `Y`:

* `symmetric_remainder_isBigO` :
  `½[(6)_h + (7)_h] - (P Y + (h²/8)(P'' Y + 4 Q' Y)) = O(h⁴)`,
  and `M₀ = P Y`, so to leading order `½[(6)_h + (7)_h] → M₀`;
* `antisymmetric_remainder_isBigO` :
  `[(6)_h - (7)_h]/h - (P' Y + 2 Q Y) = O(h²)`,
  and `M₁ = P' Y + 2 Q Y`, so `[(6)_h - (7)_h]/h → M₁`.

These are exactly the two reductions that the discrete pair must satisfy for T1.
-/
import TodaFormalization.DLWDiscretePair
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Analysis.Asymptotics.Ring
import Mathlib.Analysis.Calculus.Deriv.Slope

open Topology Filter Asymptotics

namespace DLW

/-! ## 1. The analytic bridge -/

/-- The third-order Taylor jet of `f` at `Y`, as a function of the offset `u`. -/
noncomputable def jet3 (f : ℝ → ℝ) (Y u : ℝ) : ℝ :=
  f Y + u * deriv f Y + u ^ 2 / 2 * iteratedDeriv 2 f Y
    + u ^ 3 / 6 * iteratedDeriv 3 f Y

/-- **The analytic bridge.**  A `C⁴` function agrees with its third-order Taylor jet to
`O(u⁴)`.  This is the only analytic input used by the template reductions below. -/
theorem taylor_jet3_isBigO (f : ℝ → ℝ) (hf : ContDiff ℝ 4 f) (Y : ℝ) :
    (fun u : ℝ => f (Y + u) - jet3 f Y u) =O[𝓝 (0 : ℝ)] fun u : ℝ => u ^ 4 := by
  have hφ : Tendsto (fun u : ℝ => Y + u) (𝓝 (0 : ℝ)) (𝓝 Y) := by
    have hc : Continuous fun u : ℝ => Y + u := continuous_const.add continuous_id
    simpa [ContinuousAt] using hc.continuousAt (x := (0 : ℝ))
  have hlo : (fun u : ℝ => f (Y + u) - taylorWithinEval f 4 Set.univ Y (Y + u))
      =o[𝓝 (0 : ℝ)] fun u : ℝ => u ^ 4 := by
    have h1 := (taylor_isLittleO_univ (x₀ := Y) (n := 4) hf).comp_tendsto hφ
    have h2 : (fun u : ℝ => f (Y + u) - taylorWithinEval f 4 Set.univ Y (Y + u))
        = ((fun x : ℝ => f x - taylorWithinEval f 4 Set.univ Y x) ∘ fun u : ℝ => Y + u) := rfl
    have h3 : (fun u : ℝ => u ^ 4) = ((fun x : ℝ => (x - Y) ^ 4) ∘ fun u : ℝ => Y + u) := by
      funext u
      simp
    rw [h2, h3]
    exact h1
  have hjet : (fun u : ℝ => f (Y + u) - jet3 f Y u)
      = fun u : ℝ => (f (Y + u) - taylorWithinEval f 4 Set.univ Y (Y + u))
          + u ^ 4 / 24 * iteratedDeriv 4 f Y := by
    funext u
    rw [taylor_within_apply]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add,
      iteratedDerivWithin_univ, smul_eq_mul, add_sub_cancel_left]
    norm_num
    unfold jet3
    ring
  rw [hjet]
  have h2 : (fun u : ℝ => u ^ 4 / 24 * iteratedDeriv 4 f Y)
      =O[𝓝 (0 : ℝ)] fun u : ℝ => u ^ 4 := by
    refine ((isBigO_refl (fun u : ℝ => u ^ 4) (𝓝 (0 : ℝ))).const_mul_left
      (iteratedDeriv 4 f Y / 24)).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with u
    ring
  exact hlo.isBigO.add h2

/-- The bridge at the wall `Y + h/2`. -/
theorem jet3_half_isBigO (f : ℝ → ℝ) (hf : ContDiff ℝ 4 f) (Y : ℝ) :
    (fun h : ℝ => f (Y + h / 2) - jet3 f Y (h / 2)) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
  have hφ : Tendsto (fun h : ℝ => h / 2) (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    have hc : Continuous fun h : ℝ => h / 2 := continuous_id.div_const 2
    simpa [ContinuousAt] using hc.continuousAt (x := (0 : ℝ))
  have h1 : (fun h : ℝ => f (Y + h / 2) - jet3 f Y (h / 2))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => (h / 2) ^ 4 :=
    (taylor_jet3_isBigO f hf Y).comp_tendsto hφ
  have h2 : (fun h : ℝ => (h / 2) ^ 4) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
    refine ((isBigO_refl (fun h : ℝ => h ^ 4) (𝓝 (0 : ℝ))).const_mul_left
      ((1 / 2 : ℝ) ^ 4)).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    ring
  exact h1.trans h2

/-- The bridge at the wall `Y - h/2` (auxiliary form, with the offset written additively so
that it matches the composition produced by `IsBigO.comp_tendsto`). -/
private theorem jet3_negHalf_aux (f : ℝ → ℝ) (hf : ContDiff ℝ 4 f) (Y : ℝ) :
    (fun h : ℝ => f (Y + (-h) / 2) - jet3 f Y ((-h) / 2))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
  have hφ : Tendsto (fun h : ℝ => (-h) / 2) (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    have hc : Continuous fun h : ℝ => (-h) / 2 := continuous_id.neg.div_const 2
    simpa [ContinuousAt] using hc.continuousAt (x := (0 : ℝ))
  have h2 : ((fun u : ℝ => u ^ 4) ∘ fun h : ℝ => (-h) / 2)
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
    refine ((isBigO_refl (fun h : ℝ => h ^ 4) (𝓝 (0 : ℝ))).const_mul_left
      ((1 / 2 : ℝ) ^ 4)).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    simp only [Function.comp_apply]
    ring
  exact ((taylor_jet3_isBigO f hf Y).comp_tendsto hφ).trans h2

/-- The bridge at the wall `Y - h/2`. -/
theorem jet3_negHalf_isBigO (f : ℝ → ℝ) (hf : ContDiff ℝ 4 f) (Y : ℝ) :
    (fun h : ℝ => f (Y - h / 2) - jet3 f Y (-h / 2)) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
  refine (jet3_negHalf_aux f hf Y).congr' ?_ (EventuallyEq.refl _ _)
  filter_upwards with h
  rw [show Y + (-h) / 2 = Y - h / 2 by ring]

/-! ## 2. Order bookkeeping -/

/-- Near the origin, a higher power is `O` of a lower one. -/
theorem pow_isBigO_pow {k m : ℕ} (hm : m ≤ k) :
    (fun h : ℝ => h ^ k) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ m := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hm
  refine IsBigO.of_bound 1 ?_
  filter_upwards [Metric.ball_mem_nhds (0 : ℝ) one_pos] with h hh
  have habs : |h| ≤ 1 := by
    rw [Metric.mem_ball, dist_eq_norm, Real.norm_eq_abs, sub_zero] at hh
    exact le_of_lt hh
  have h1 : |h| ^ d ≤ 1 := by
    simpa using pow_le_pow_left₀ (abs_nonneg h) habs d
  have h2 : (0 : ℝ) ≤ |h| ^ m := pow_nonneg (abs_nonneg h) m
  rw [pow_add]
  simp only [norm_mul, norm_pow, Real.norm_eq_abs, one_mul]
  calc |h| ^ m * |h| ^ d ≤ |h| ^ m * 1 := mul_le_mul_of_nonneg_left h1 h2
    _ = |h| ^ m := mul_one _

/-- An `O(h³)` remainder divided by `h` is an `O(h²)` remainder (on `h ≠ 0`). -/
theorem div_id_of_isBigO_cube {f : ℝ → ℝ}
    (hf : f =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ 3) :
    (fun h : ℝ => f h / h) =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ 2 := by
  obtain ⟨C, hb⟩ := hf.bound
  refine IsBigO.of_bound (max C 0) ?_
  filter_upwards [hb, self_mem_nhdsWithin] with h hb' hh
  have hh' : h ≠ 0 := by simpa using hh
  have hb'' : |f h| ≤ C * |h| ^ 3 := by
    simpa only [norm_pow, Real.norm_eq_abs] using hb'
  have habs : 0 < |h| := abs_pos.mpr hh'
  rw [show ‖f h / h‖ = |f h| / |h| by simp only [norm_div, Real.norm_eq_abs],
    show ‖h ^ 2‖ = |h| ^ 2 by simp only [norm_pow, Real.norm_eq_abs],
    div_le_iff₀ habs]
  calc |f h| ≤ C * |h| ^ 3 := hb''
    _ ≤ max C 0 * |h| ^ 3 := mul_le_mul_of_nonneg_right (le_max_left C 0) (by positivity)
    _ = max C 0 * |h| ^ 2 * |h| := by ring

/-! ## 3. The symmetric template reduction -/

/-- **T1, symmetric half.**  With both slots `C⁴` at the centre `Y`, the symmetric
recombination of the two walls differs from `M₀ = P Y` by `O(h⁴)` — the `h²` term
`(h²/8)(P'' Y + 4 Q' Y)` is retained explicitly, matching the exact jet expansion. -/
theorem symmetric_remainder_isBigO (P Q : ℝ → ℝ) (hP : ContDiff ℝ 4 P) (hQ : ContDiff ℝ 4 Q)
    (Y : ℝ) :
    (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2)) + (P (Y - h / 2) - h * Q (Y - h / 2))) / 2
        - (P Y + h ^ 2 / 8 * (iteratedDeriv 2 P Y + 4 * deriv Q Y)))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
  have key : (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2))
        + (P (Y - h / 2) - h * Q (Y - h / 2))) - 2 * P Y
        - h ^ 2 / 4 * (iteratedDeriv 2 P Y + 4 * deriv Q Y))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
    have hPp := jet3_half_isBigO P hP Y
    have hPm := jet3_negHalf_isBigO P hP Y
    have hQp := jet3_half_isBigO Q hQ Y
    have hQm := jet3_negHalf_isBigO Q hQ Y
    have hA : (fun h : ℝ => (P (Y + h / 2) - jet3 P Y (h / 2))
          + (P (Y - h / 2) - jet3 P Y (-h / 2))) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 :=
      hPp.add hPm
    have hB : (fun h : ℝ => (Q (Y + h / 2) - jet3 Q Y (h / 2))
          - (Q (Y - h / 2) - jet3 Q Y (-h / 2))) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 :=
      hQp.sub hQm
    have hC : (fun h : ℝ => h * ((Q (Y + h / 2) - jet3 Q Y (h / 2))
          - (Q (Y - h / 2) - jet3 Q Y (-h / 2))))
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
      refine (hB.mul (isBigO_refl (fun h : ℝ => h) (𝓝 (0 : ℝ)))).congr' ?_ ?_
      · filter_upwards with h; ring
      · filter_upwards with h; ring
    have hC' : (fun h : ℝ => h * ((Q (Y + h / 2) - jet3 Q Y (h / 2))
          - (Q (Y - h / 2) - jet3 Q Y (-h / 2))))
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 :=
      hC.trans (pow_isBigO_pow (k := 5) (m := 4) (by norm_num))
    have hG : (fun h : ℝ => h ^ 4 / 24 * iteratedDeriv 3 Q Y)
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 := by
      refine ((isBigO_refl (fun h : ℝ => h ^ 4) (𝓝 (0 : ℝ))).const_mul_left
        (iteratedDeriv 3 Q Y / 24)).congr' ?_ (EventuallyEq.refl _ _)
      filter_upwards with h
      ring
    refine ((hA.add hC').add hG).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    unfold jet3
    ring
  refine (key.const_mul_left (1 / 2)).congr' ?_ (EventuallyEq.refl _ _)
  filter_upwards with h
  ring

/-! ## 4. The antisymmetric template reduction -/

/-- **T1, antisymmetric half.**  The divided difference of the two walls differs from
`M₁ = P' Y + 2 Q Y` by `O(h²)`. -/
theorem antisymmetric_remainder_isBigO (P Q : ℝ → ℝ) (hP : ContDiff ℝ 4 P) (hQ : ContDiff ℝ 4 Q)
    (Y : ℝ) :
    (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2)) - (P (Y - h / 2) - h * Q (Y - h / 2))) / h
        - (deriv P Y + 2 * Q Y))
      =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ 2 := by
  have key0 : (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2))
        - (P (Y - h / 2) - h * Q (Y - h / 2))) - h * (deriv P Y + 2 * Q Y))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 3 := by
    have hPp := jet3_half_isBigO P hP Y
    have hPm := jet3_negHalf_isBigO P hP Y
    have hQp := jet3_half_isBigO Q hQ Y
    have hQm := jet3_negHalf_isBigO Q hQ Y
    have hA : (fun h : ℝ => (P (Y + h / 2) - jet3 P Y (h / 2))
          - (P (Y - h / 2) - jet3 P Y (-h / 2))) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 3 :=
      (hPp.sub hPm).trans (pow_isBigO_pow (k := 4) (m := 3) (by norm_num))
    have hB : (fun h : ℝ => (Q (Y + h / 2) - jet3 Q Y (h / 2))
          + (Q (Y - h / 2) - jet3 Q Y (-h / 2))) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 :=
      hQp.add hQm
    have hC : (fun h : ℝ => h * ((Q (Y + h / 2) - jet3 Q Y (h / 2))
          + (Q (Y - h / 2) - jet3 Q Y (-h / 2))))
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
      refine (hB.mul (isBigO_refl (fun h : ℝ => h) (𝓝 (0 : ℝ)))).congr' ?_ ?_
      · filter_upwards with h; ring
      · filter_upwards with h; ring
    have hC' : (fun h : ℝ => h * ((Q (Y + h / 2) - jet3 Q Y (h / 2))
          + (Q (Y - h / 2) - jet3 Q Y (-h / 2))))
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 3 :=
      hC.trans (pow_isBigO_pow (k := 5) (m := 3) (by norm_num))
    have hF : (fun h : ℝ => h ^ 3 / 24 * (iteratedDeriv 3 P Y + 6 * iteratedDeriv 2 Q Y))
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 3 := by
      refine ((isBigO_refl (fun h : ℝ => h ^ 3) (𝓝 (0 : ℝ))).const_mul_left
        ((iteratedDeriv 3 P Y + 6 * iteratedDeriv 2 Q Y) / 24)).congr' ?_
        (EventuallyEq.refl _ _)
      filter_upwards with h
      ring
    refine ((hF.add hA).add hC').congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    unfold jet3
    ring
  have key : (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2))
        - (P (Y - h / 2) - h * Q (Y - h / 2))) - h * (deriv P Y + 2 * Q Y))
      =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ 3 := key0.mono nhdsWithin_le_nhds
  refine (div_id_of_isBigO_cube key).congr' ?_ (EventuallyEq.refl _ _)
  filter_upwards [self_mem_nhdsWithin] with h hh
  have hh' : h ≠ 0 := by simpa using hh
  field_simp

/-! ## 5. Strengthening the antisymmetric remainder to `O(h⁴)`

`antisymmetric_remainder_isBigO` proves only `[(6)_h - (7)_h]/h - M₁ = O(h²)`.  The template
reduction behind it uses the *third*-order jet of `P` (remainder `O(u⁴)`); the difference of the
two walls cancels one order, but the subsequent division by `h` hands it back.

The *exact* jet expansion `antisymmetric_expansion` exhibits the `h²` coefficient
`(1/24)(b₃ + 6d₂)`, so the sharp statement is

  `[(6)_h - (7)_h]/h = M₁ + (h²/24)(P''' Y + 6 Q'' Y) + O(h⁴)`,

and that is exactly what costs one more derivative of `P`: the fourth-order jet (class `C⁵`)
instead of the third-order jet (class `C⁴`).  This section supplies it, together with the
general division lemma `O(h^{k+1}) / h = O(h^k)`.

Note that no such strengthening is needed on the symmetric side: there the third-order jet
already suffices, because the `P`-remainder enters *undivided* as `R(h/2) + R(-h/2)`. -/

/-- An `O(h^{k+1})` remainder divided by `h` is an `O(h^k)` remainder (on `h ≠ 0`). -/
theorem div_id_of_isBigO_pow {k : ℕ} {f : ℝ → ℝ}
    (hf : f =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ (k + 1)) :
    (fun h : ℝ => f h / h) =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ k := by
  obtain ⟨C, hb⟩ := hf.bound
  refine IsBigO.of_bound (max C 0) ?_
  filter_upwards [hb, self_mem_nhdsWithin] with h hb' hh
  have hh' : h ≠ 0 := by simpa using hh
  have hb'' : |f h| ≤ C * |h| ^ (k + 1) := by
    simpa only [norm_pow, Real.norm_eq_abs] using hb'
  have habs : 0 < |h| := abs_pos.mpr hh'
  rw [show ‖f h / h‖ = |f h| / |h| by simp only [norm_div, Real.norm_eq_abs],
    show ‖h ^ k‖ = |h| ^ k by simp only [norm_pow, Real.norm_eq_abs],
    div_le_iff₀ habs]
  calc |f h| ≤ C * |h| ^ (k + 1) := hb''
    _ ≤ max C 0 * |h| ^ (k + 1) := mul_le_mul_of_nonneg_right (le_max_left C 0) (by positivity)
    _ = max C 0 * |h| ^ k * |h| := by rw [pow_succ]; ring

/-- The fourth-order Taylor jet of `f` at `Y`, as a function of the offset `u`. -/
noncomputable def jet4 (f : ℝ → ℝ) (Y u : ℝ) : ℝ :=
  jet3 f Y u + u ^ 4 / 24 * iteratedDeriv 4 f Y

/-- **The analytic bridge, one order higher.**  A `C⁵` function agrees with its fourth-order
Taylor jet to `O(u⁵)`. -/
theorem taylor_jet4_isBigO (f : ℝ → ℝ) (hf : ContDiff ℝ 5 f) (Y : ℝ) :
    (fun u : ℝ => f (Y + u) - jet4 f Y u) =O[𝓝 (0 : ℝ)] fun u : ℝ => u ^ 5 := by
  have hφ : Tendsto (fun u : ℝ => Y + u) (𝓝 (0 : ℝ)) (𝓝 Y) := by
    have hc : Continuous fun u : ℝ => Y + u := continuous_const.add continuous_id
    simpa [ContinuousAt] using hc.continuousAt (x := (0 : ℝ))
  have hlo : (fun u : ℝ => f (Y + u) - taylorWithinEval f 5 Set.univ Y (Y + u))
      =o[𝓝 (0 : ℝ)] fun u : ℝ => u ^ 5 := by
    have h1 := (taylor_isLittleO_univ (x₀ := Y) (n := 5) hf).comp_tendsto hφ
    have h2 : (fun u : ℝ => f (Y + u) - taylorWithinEval f 5 Set.univ Y (Y + u))
        = ((fun x : ℝ => f x - taylorWithinEval f 5 Set.univ Y x) ∘ fun u : ℝ => Y + u) := rfl
    have h3 : (fun u : ℝ => u ^ 5) = ((fun x : ℝ => (x - Y) ^ 5) ∘ fun u : ℝ => Y + u) := by
      funext u
      simp
    rw [h2, h3]
    exact h1
  have hjet : (fun u : ℝ => f (Y + u) - jet4 f Y u)
      = fun u : ℝ => (f (Y + u) - taylorWithinEval f 5 Set.univ Y (Y + u))
          + u ^ 5 / 120 * iteratedDeriv 5 f Y := by
    funext u
    rw [taylor_within_apply]
    simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add,
      iteratedDerivWithin_univ, smul_eq_mul, add_sub_cancel_left]
    norm_num
    unfold jet4 jet3
    ring
  rw [hjet]
  have h2 : (fun u : ℝ => u ^ 5 / 120 * iteratedDeriv 5 f Y)
      =O[𝓝 (0 : ℝ)] fun u : ℝ => u ^ 5 := by
    refine ((isBigO_refl (fun u : ℝ => u ^ 5) (𝓝 (0 : ℝ))).const_mul_left
      (iteratedDeriv 5 f Y / 120)).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with u
    ring
  exact hlo.isBigO.add h2

/-- The fourth-order bridge at the wall `Y + h/2`. -/
theorem jet4_half_isBigO (f : ℝ → ℝ) (hf : ContDiff ℝ 5 f) (Y : ℝ) :
    (fun h : ℝ => f (Y + h / 2) - jet4 f Y (h / 2)) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
  have hφ : Tendsto (fun h : ℝ => h / 2) (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    have hc : Continuous fun h : ℝ => h / 2 := continuous_id.div_const 2
    simpa [ContinuousAt] using hc.continuousAt (x := (0 : ℝ))
  have h1 : (fun h : ℝ => f (Y + h / 2) - jet4 f Y (h / 2))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => (h / 2) ^ 5 :=
    (taylor_jet4_isBigO f hf Y).comp_tendsto hφ
  have h2 : (fun h : ℝ => (h / 2) ^ 5) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
    refine ((isBigO_refl (fun h : ℝ => h ^ 5) (𝓝 (0 : ℝ))).const_mul_left
      ((1 / 2 : ℝ) ^ 5)).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    ring
  exact h1.trans h2

/-- The fourth-order bridge at `Y - h/2` (auxiliary additive form). -/
private theorem jet4_negHalf_aux (f : ℝ → ℝ) (hf : ContDiff ℝ 5 f) (Y : ℝ) :
    (fun h : ℝ => f (Y + (-h) / 2) - jet4 f Y ((-h) / 2))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
  have hφ : Tendsto (fun h : ℝ => (-h) / 2) (𝓝 (0 : ℝ)) (𝓝 (0 : ℝ)) := by
    have hc : Continuous fun h : ℝ => (-h) / 2 := continuous_id.neg.div_const 2
    simpa [ContinuousAt] using hc.continuousAt (x := (0 : ℝ))
  have h2 : ((fun u : ℝ => u ^ 5) ∘ fun h : ℝ => (-h) / 2)
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
    refine ((isBigO_refl (fun h : ℝ => h ^ 5) (𝓝 (0 : ℝ))).const_mul_left
      ((-1 / 2 : ℝ) ^ 5)).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    simp only [Function.comp_apply]
    ring
  exact ((taylor_jet4_isBigO f hf Y).comp_tendsto hφ).trans h2

/-- The fourth-order bridge at the wall `Y - h/2`. -/
theorem jet4_negHalf_isBigO (f : ℝ → ℝ) (hf : ContDiff ℝ 5 f) (Y : ℝ) :
    (fun h : ℝ => f (Y - h / 2) - jet4 f Y (-h / 2)) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
  refine (jet4_negHalf_aux f hf Y).congr' ?_ (EventuallyEq.refl _ _)
  filter_upwards with h
  rw [show Y + (-h) / 2 = Y - h / 2 by ring]

/-- **T1, antisymmetric half — sharp version.**  With `P` of class `C⁵` and `Q` of class `C⁴`,
the divided difference of the two walls differs from

  `M₁ + (h²/24)(P''' Y + 6 Q'' Y)`

by `O(h⁴)`.  The explicit `h²` coefficient is the one already exhibited by the *exact*
expansion `antisymmetric_expansion`; the improvement from `O(h²)` to `O(h⁴)` is precisely
what the fourth-order jet of `P` buys.

The `P`-remainder was `O(u⁴)` and its difference over the two walls therefore only `O(h⁴)`;
upgrading it to `O(u⁵)` is what makes the difference `O(h⁵)`, and hence the divided
difference `O(h⁴)`.  The `Q`-remainder is already `O(u⁴)` and enters multiplied by `h`. -/
theorem antisymmetric_remainder_isBigO4 (P Q : ℝ → ℝ) (hP : ContDiff ℝ 5 P)
    (hQ : ContDiff ℝ 4 Q) (Y : ℝ) :
    (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2)) - (P (Y - h / 2) - h * Q (Y - h / 2))) / h
        - (deriv P Y + 2 * Q Y
            + h ^ 2 / 24 * (iteratedDeriv 3 P Y + 6 * iteratedDeriv 2 Q Y)))
      =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ 4 := by
  have key0 : (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2))
        - (P (Y - h / 2) - h * Q (Y - h / 2)))
        - h * (deriv P Y + 2 * Q Y
            + h ^ 2 / 24 * (iteratedDeriv 3 P Y + 6 * iteratedDeriv 2 Q Y)))
      =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
    have hPp := jet4_half_isBigO P hP Y
    have hPm := jet4_negHalf_isBigO P hP Y
    have hQp := jet3_half_isBigO Q hQ Y
    have hQm := jet3_negHalf_isBigO Q hQ Y
    have hA : (fun h : ℝ => (P (Y + h / 2) - jet4 P Y (h / 2))
          - (P (Y - h / 2) - jet4 P Y (-h / 2))) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 :=
      hPp.sub hPm
    have hB : (fun h : ℝ => (Q (Y + h / 2) - jet3 Q Y (h / 2))
          + (Q (Y - h / 2) - jet3 Q Y (-h / 2))) =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 4 :=
      hQp.add hQm
    have hC : (fun h : ℝ => h * ((Q (Y + h / 2) - jet3 Q Y (h / 2))
          + (Q (Y - h / 2) - jet3 Q Y (-h / 2))))
        =O[𝓝 (0 : ℝ)] fun h : ℝ => h ^ 5 := by
      refine (hB.mul (isBigO_refl (fun h : ℝ => h) (𝓝 (0 : ℝ)))).congr' ?_ ?_
      · filter_upwards with h; ring
      · filter_upwards with h; ring
    refine (hA.add hC).congr' ?_ (EventuallyEq.refl _ _)
    filter_upwards with h
    unfold jet4 jet3
    ring
  have key : (fun h : ℝ => ((P (Y + h / 2) + h * Q (Y + h / 2))
        - (P (Y - h / 2) - h * Q (Y - h / 2)))
        - h * (deriv P Y + 2 * Q Y
            + h ^ 2 / 24 * (iteratedDeriv 3 P Y + 6 * iteratedDeriv 2 Q Y)))
      =O[𝓝[≠] (0 : ℝ)] fun h : ℝ => h ^ 5 := key0.mono nhdsWithin_le_nhds
  refine (div_id_of_isBigO_pow (k := 4) key).congr' ?_ (EventuallyEq.refl _ _)
  filter_upwards [self_mem_nhdsWithin] with h hh
  have hh' : h ≠ 0 := by simpa using hh
  field_simp

end DLW
