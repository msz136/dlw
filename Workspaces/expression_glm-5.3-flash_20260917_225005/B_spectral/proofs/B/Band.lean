import Mathlib.Basic.Complex.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Data.Int.Cast.Basic
import Mathlib.Analysis.Complex.Norm

/-!
# B-direction: explicit finite-band stability bound (linearized, constant background)

Given the exact dispersion of the y-spectral modal system at a retained mode
(derived in `B.Dispersion` from the modal ODEs):

  (s + i c k)² = k⁴ − β k³/ℓ ,   c = u0 + 2a,  β = v0 + 2λ,  ℓ ≠ 0,

this module proves the **explicit band bound**

  ‖s + i c k‖² ≤ |k|⁴ + |β| · |k|³ / |ℓ|                       (B1)

and the corollary

  ‖s‖ ≤ √(|k|⁴ + |β| · |k|³ / |ℓ|) + |c| · |k|                 (B2)

and the diagonal specialization (k = ℓ = n ≥ 1)

  ‖s‖ ≤ √(n⁴ + |β| n²) + |c| n ~ n²                            (B3)

Quantitative meaning (see report §stability): on a retained band |ℓ| ≤ N with
x-wavenumbers |k| ≤ K, every modal growth rate obeys ‖s‖ ≤ √(K⁴+|β|K³) + |c|K —
finite-band stability. (B3) shows the order-N² growth that the top of the band
realizes, matching the continuous M4 obstruction at ℓ ~ N. Honest caveat: the
y-truncated system keeps x continuous, so the per-mode high-k growth ‖s‖ ~ k²
(M4) persists exactly; band-limited well-posedness does NOT imply convergence
for general data.

Pure algebra on ℂ/ℝ from the dispersion hypothesis; no smoothness assumptions.
-/

namespace DLWBSpec

/-- **(B1) Band bound on the shifted growth rate** ‖s + i c k‖². -/
theorem norm_sq_bound {s : ℂ} {k c β : ℝ} {ℓ : ℤ} (hℓ : ℓ ≠ 0)
    (h : (s + Complex.I * (c*k))^2 = ((k:ℂ)^4 - (β * (k:ℂ)^3 / (ℓ:ℂ)))) :
    ‖s + Complex.I * (c*k)‖ ^ 2 ≤ (|k|)^4 + |β| * (|k|)^3 / |((ℓ : ℤ) : ℝ)| := by
  have e0 : ‖s + Complex.I * (c*k)‖ ^ 2
      = ‖((k:ℂ)^4 - (β * (k:ℂ)^3 / (ℓ:ℂ)))‖ := by
    rw [← h, ← Complex.norm_pow]
  rw [e0]
  refine le_trans (norm_sub_le ((k:ℂ)^4) ((β * (k:ℂ)^3 / (ℓ:ℂ)))) ?_
  have h2 : ‖((k:ℂ)^4 : ℂ)‖ = (|k|)^4 := by
    rw [Complex.norm_pow, Complex.norm_real, Real.norm_eq_abs]
  have h3 : ‖((β * (k:ℂ)^3 / (ℓ:ℂ)) : ℂ)‖ = |β| * (|k|)^3 / |((ℓ:ℤ) : ℝ)| := by
    rw [Complex.norm_div, Complex.norm_mul, Complex.norm_pow, Complex.norm_real,
      Complex.norm_real, Complex.norm_real, Real.norm_eq_abs, Real.norm_eq_abs,
      Complex.norm_intCast]
  rw [h2, h3]

/-- **(B2) Explicit bound on ‖s‖.** -/
theorem s_bound {s : ℂ} {k c β : ℝ} {ℓ : ℤ} (hℓ : ℓ ≠ 0)
    (h : (s + Complex.I * (c*k))^2 = ((k:ℂ)^4 - (β * (k:ℂ)^3 / (ℓ:ℂ)))) :
    ‖s‖ ≤ Real.sqrt ((|k|)^4 + |β| * (|k|)^3 / |((ℓ : ℤ) : ℝ)|) + |c| * |k| := by
  have hb : ‖s + Complex.I * (c*k)‖ ^ 2 ≤ (|k|)^4 + |β| * (|k|)^3 / |((ℓ : ℤ) : ℝ)| :=
    norm_sq_bound hℓ h
  have hz : ‖s + Complex.I * (c*k)‖
      ≤ Real.sqrt ((|k|)^4 + |β| * (|k|)^3 / |((ℓ : ℤ) : ℝ)|) :=
    (Real.le_sqrt (by positivity) (by positivity)).mpr hb
  have t1 : ‖s‖ ≤ ‖s + Complex.I * (c*k)‖ + ‖Complex.I * (c*k)‖ := by
    have hsub := norm_sub_le (s + Complex.I * (c*k)) (Complex.I * (c*k))
    rwa [add_sub_cancel] at hsub
  have t2 : ‖Complex.I * (c*k)‖ = |c| * |k| := by
    rw [Complex.norm_mul, Complex.norm_I, Complex.norm_mul, Complex.norm_real,
      Complex.norm_real, Real.norm_eq_abs, Real.norm_eq_abs]
  linarith [t1, t2, hz]

/-- **(B3) Diagonal specialization k = ℓ = n ≥ 1: the explicit N²-type bound.**
For every root s of the diagonal dispersion (s + i c n)² = n⁴ − β n²:
‖s‖ ≤ √(n⁴ + |β| n²) + |c| n — of order n², quantifying the band-limited
obstruction on the retained band (top of band matches the M4 growth at ℓ ~ N). -/
theorem diagonal_bound {s : ℂ} {c β : ℝ} {n : ℕ} (hn : 0 < n)
    (h : (s + Complex.I * (c * (n:ℝ)))^2
        = (((n:ℝ):ℂ)^4 - (β * ((n:ℝ):ℂ)^3 / (((n : ℕ) : ℤ) : ℂ)))) :
    ‖s‖ ≤ Real.sqrt ((n:ℝ)^4 + |β| * (n:ℝ)^2) + |c| * (n:ℝ) := by
  have habsk : |(n:ℝ)| = (n:ℝ) := abs_of_nonneg (by positivity)
  have habsl : |(((n : ℕ) : ℤ) : ℝ)| = (n:ℝ) := by
    rw [Int.cast_natCast]
    exact abs_of_nonneg (by positivity)
  have hb := norm_sq_bound (ℓ := ((n : ℕ) : ℤ)) (k := (n:ℝ)) (c := c) (β := β)
    (by
      have h0 : (n : ℕ) ≠ 0 := ne_of_gt hn
      exact Nat.cast_ne_zero.mpr h0) h
  rw [habsk, habsl] at hb
  have h0' : (n:ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (ne_of_gt hn)
  have hdiv : (n:ℝ)^3 / (n:ℝ) = (n:ℝ)^2 := by
    field_simp [h0']
  rw [hdiv] at hb
  have hz : ‖s + Complex.I * (c * (n:ℝ))‖
      ≤ Real.sqrt ((n:ℝ)^4 + |β| * (n:ℝ)^2) :=
    (Real.le_sqrt (by positivity) (by positivity)).mpr hb
  have t1 : ‖s‖ ≤ ‖s + Complex.I * (c * (n:ℝ))‖ + ‖Complex.I * (c * (n:ℝ))‖ := by
    have hsub := norm_sub_le (s + Complex.I * (c * (n:ℝ))) (Complex.I * (c * (n:ℝ)))
    rwa [add_sub_cancel] at hsub
  have t2 : ‖Complex.I * (c * (n:ℝ))‖ = |c| * (n:ℝ) := by
    rw [Complex.norm_mul, Complex.norm_I, Complex.norm_mul, Complex.norm_real,
      Complex.norm_real, Real.norm_eq_abs, Real.norm_eq_abs, habsk]
  linarith [t1, t2, hz]

end DLWBSpec
