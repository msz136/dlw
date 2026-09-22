/-
  Direction B — spectral / pseudo-spectral semidiscretisation of the DLW system.
  Module 2: linearised dispersion relation and the growth bound.

  Continuum linearisation.  About the constant background `(u0, v0)` the
  linearisation of

      (1)  u_yt + v_xx + u u_xy + u_x u_y + 2 a u_xy = 0
      (2)  v_t + (u v)_x + u_xxy + 2 a v_x + 2 lam u_x = 0

  is, for a mode `exp (s t + i (k x + l y))` with amplitudes `(U, V)`,

      (1L)  (i l s) U - k^2 V - (u0 + 2 a) k l U = 0
      (2L)  (s + i (u0 + 2 a) k) V + i (v0 + 2 lam) k U - i k^2 l U = 0

  `dispersion_relation` eliminates `V` and proves, machine-checked,

      (s + i (u0 + 2 a) k)^2 = k^4 - (v0 + 2 lam) k^3 / l .

  This is a statement about the *continuous* symbol: it is unchanged by any
  `y`-discretisation, because discretising `y` can only restrict `l` to a finite
  set, never restrict `k`.  `band_contains_growing_mode` makes that precise: the
  growth bound contains no truncation parameter.

  `sqrt_growth_lower_bound` / `growth_lower_bound` give the quantitative form:
  for `c = v0 + 2 lam >= 0` and a retained mode `l >= 1`,

      Re s  >=  k^2 - (c / l) k      for every  k >= c / l .
-/
import Mathlib.Basic.Complex.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic
import Spectral.Multiplier

namespace DLW.Spectral

/-! ## The linearised dispersion relation (pure field algebra) -/

/-- The substitution that drives the elimination of `V`, and the only place where
    `i^2 = -1` enters:
    `i l s - A k l = i l (s + i A k)`. -/
theorem I_factor (A l s k : ℂ) :
    Complex.I * l * s - A * k * l = Complex.I * l * (s + Complex.I * A * k) := by
  have hI2 : (1 : ℂ) + Complex.I ^ 2 = 0 := by
    rw [pow_two, Complex.I_mul_I]
    ring
  linear_combination (norm := ring_nf) (-(l * A * k)) * hI2

/-- Eliminating the amplitude `V` from the linearised DLW mode system yields the
    dispersion relation.  Stated with division-free hypotheses so that no
    bookkeeping about invertibility is smuggled in. -/
theorem dispersion_relation (u0 v0 a lam k l s U V : ℂ)
    (hk : k ≠ 0) (hl : l ≠ 0) (hU : U ≠ 0)
    (h1 : (Complex.I * l * s) * U - k ^ 2 * V - (u0 + 2 * a) * k * l * U = 0)
    (h2 : (s + Complex.I * (u0 + 2 * a) * k) * V
            + Complex.I * (v0 + 2 * lam) * k * U - Complex.I * k ^ 2 * l * U = 0) :
    (s + Complex.I * (u0 + 2 * a) * k) ^ 2 = k ^ 4 - (v0 + 2 * lam) * k ^ 3 / l := by
  -- Multiply (2L) by `k^2` and use (1L) to eliminate `k^2 V`.
  have hkey : Complex.I * U *
      (l * (s + Complex.I * (u0 + 2 * a) * k) ^ 2 + (v0 + 2 * lam) * k ^ 3
        - k ^ 4 * l) = 0 := by
    linear_combination (norm := ring_nf)
      (s + Complex.I * (u0 + 2 * a) * k) * h1 + k ^ 2 * h2
        - (U * (s + Complex.I * (u0 + 2 * a) * k)) * I_factor (u0 + 2 * a) l s k
  have hIU : Complex.I * U ≠ 0 := mul_ne_zero Complex.I_ne_zero hU
  have hz : l * (s + Complex.I * (u0 + 2 * a) * k) ^ 2 + (v0 + 2 * lam) * k ^ 3
      - k ^ 4 * l = 0 := (mul_eq_zero.mp hkey).resolve_left hIU
  have hX : (s + Complex.I * (u0 + 2 * a) * k) ^ 2
      = (k ^ 4 * l - (v0 + 2 * lam) * k ^ 3) / l := by
    rw [eq_div_iff hl]
    linear_combination (norm := ring_nf) hz
  rw [hX]
  field_simp

/-- Every *non-trivial* linearised mode satisfies the dispersion relation.
    (`U = 0` forces `V = 0` by (1L) when `k ≠ 0`, so the hypothesis `U ≠ 0` is
    not a restriction on non-trivial modes.) -/
theorem nontrivial_dispersion_relation (u0 v0 a lam k l s U V : ℂ)
    (hk : k ≠ 0) (hl : l ≠ 0) (hn : U ≠ 0 ∨ V ≠ 0)
    (h1 : (Complex.I * l * s) * U - k ^ 2 * V - (u0 + 2 * a) * k * l * U = 0)
    (h2 : (s + Complex.I * (u0 + 2 * a) * k) * V
            + Complex.I * (v0 + 2 * lam) * k * U - Complex.I * k ^ 2 * l * U = 0) :
    (s + Complex.I * (u0 + 2 * a) * k) ^ 2 = k ^ 4 - (v0 + 2 * lam) * k ^ 3 / l := by
  by_cases hU : U = 0
  · exfalso
    have hV0 : V = 0 := by
      have hz : k ^ 2 * V = 0 := by
        have h1' := h1
        rw [hU] at h1'
        linear_combination (norm := ring_nf) -h1'
      exact (mul_eq_zero.mp hz).resolve_left (pow_ne_zero 2 hk)
    rcases hn with hn | hn
    · exact hn hU
    · exact hn hV0
  · exact dispersion_relation u0 v0 a lam k l s U V hk hl hU h1 h2

/-- Converse: the dispersion relation is sufficient.  With `U = 1` and
    `V = (i l s - (u0+2a) k l)/k^2` the linearised mode system holds, so the
    relation really characterises the (non-trivial) linearised modes. -/
theorem mode_of_dispersion_relation (u0 v0 a lam k l s : ℂ)
    (hk : k ≠ 0) (hl : l ≠ 0) (h : (s + Complex.I * (u0 + 2 * a) * k) ^ 2
        = k ^ 4 - (v0 + 2 * lam) * k ^ 3 / l) :
    ((Complex.I * l * s) * 1
          - k ^ 2 * ((Complex.I * l * s - (u0 + 2 * a) * k * l) / k ^ 2)
          - (u0 + 2 * a) * k * l * 1 = 0)
      ∧ ((s + Complex.I * (u0 + 2 * a) * k)
            * ((Complex.I * l * s - (u0 + 2 * a) * k * l) / k ^ 2)
          + Complex.I * (v0 + 2 * lam) * k * 1 - Complex.I * k ^ 2 * l * 1 = 0) := by
  have hz : l * (s + Complex.I * (u0 + 2 * a) * k) ^ 2
      + (v0 + 2 * lam) * k ^ 3 - k ^ 4 * l = 0 := by
    rw [h]
    field_simp
    ring
  constructor
  · field_simp
    ring
  · field_simp
    linear_combination (norm := ring_nf)
      Complex.I * hz
        + (s + Complex.I * (u0 + 2 * a) * k) * I_factor (u0 + 2 * a) l s k

/-! ## The real growth bound

    `c := v0 + 2 lam` is the single parameter that enters.  Everything below is
    real analysis; no complex arithmetic is left. -/

/-- The discriminant is non-negative on the unstable side. -/
theorem discriminant_nonneg {c l k : ℝ} (hc : 0 ≤ c) (hl : 0 < l) (hk : c / l ≤ k) :
    0 ≤ k ^ 4 - c * k ^ 3 / l := by
  have hd : 0 ≤ c / l := div_nonneg hc (le_of_lt hl)
  have hk0 : 0 ≤ k := le_trans hd hk
  have hfac : k ^ 4 - c * k ^ 3 / l = k ^ 3 * (k - c / l) := by ring_nf
  rw [hfac]
  exact mul_nonneg (by positivity) (by linarith)

/-- Core real lemma: for `0 ≤ d ≤ k`, `k^2 - d k ≤ sqrt (k^4 - d k^3)`.
    This is the square root of the discriminant dominating a linear-in-`k`
    deficit. -/
theorem sqrt_growth_lower_bound {d k : ℝ} (hd : 0 ≤ d) (hk : d ≤ k) :
    k ^ 2 - d * k ≤ Real.sqrt (k ^ 4 - d * k ^ 3) := by
  have hk0 : 0 ≤ k := le_trans hd hk
  have hX : 0 ≤ k ^ 2 - d * k := by nlinarith
  have hprod : 0 ≤ d * k ^ 2 * (k - d) :=
    mul_nonneg (mul_nonneg hd (sq_nonneg k)) (by linarith)
  have hsq : (k ^ 2 - d * k) ^ 2 ≤ k ^ 4 - d * k ^ 3 := by nlinarith [hprod]
  have hR : 0 ≤ k ^ 4 - d * k ^ 3 := le_trans (sq_nonneg _) hsq
  exact (Real.le_sqrt hX hR).mpr hsq

/-- Growth bound in the DLW parameters.  For `c = v0 + 2 lam ≥ 0`, any retained
    non-zero mode `l ≥ 1` and any `k ≥ c/l`, the discriminant is non-negative and
    its square root — the real part of one branch of `s` — is at least
    `k^2 - (c/l) k`.

    Note what is absent: the truncation index `N`.  The bound is the same for
    every finite band that contains the mode `l`. -/
theorem growth_lower_bound {c l k : ℝ} (hc : 0 ≤ c) (hl : 0 < l) (hk : c / l ≤ k) :
    k ^ 2 - (c / l) * k ≤ Real.sqrt (k ^ 4 - c * k ^ 3 / l) := by
  have h := sqrt_growth_lower_bound (d := c / l) (k := k)
    (div_nonneg hc (le_of_lt hl)) hk
  have heq : k ^ 4 - c * k ^ 3 / l = k ^ 4 - (c / l) * k ^ 3 := by ring_nf
  rwa [heq]

/-- **Positive discriminant:** an actual root with positive real part, equal to
    `sqrt R`.  The shift `B` is the purely imaginary part `i (u0 + 2a) k`. -/
theorem mode_of_nonneg_discriminant {B R : ℝ} (hR : 0 ≤ R) :
    ∃ s : ℂ, (s + Complex.I * (B : ℂ)) ^ 2 = ((R : ℝ) : ℂ) ∧ s.re = Real.sqrt R := by
  refine ⟨-(Complex.I * (B : ℂ)) + ((Real.sqrt R : ℝ) : ℂ), ?_, ?_⟩
  · have h1 : (-(Complex.I * (B : ℂ)) + ((Real.sqrt R : ℝ) : ℂ)) + Complex.I * (B : ℂ)
        = ((Real.sqrt R : ℝ) : ℂ) := by ring
    rw [h1, ← Complex.ofReal_pow, Real.sq_sqrt hR]
  · simp [Complex.mul_re]

/-- There is an actual complex root `s` of the dispersion relation realising the
    bound: a linearised mode growing like `exp ((k^2 - (c/l) k) t)`. -/
theorem exists_growing_mode {c l k A : ℝ} (hc : 0 ≤ c) (hl : 0 < l) (hk : c / l ≤ k) :
    ∃ s : ℂ,
      (s + Complex.I * ((A * k : ℝ) : ℂ)) ^ 2
          = ((k : ℂ)) ^ 4 - ((c : ℂ)) * ((k : ℂ)) ^ 3 / ((l : ℂ))
        ∧ k ^ 2 - (c / l) * k ≤ s.re := by
  have hR : 0 ≤ k ^ 4 - c * k ^ 3 / l := discriminant_nonneg hc hl hk
  obtain ⟨s, hs, hre⟩ :=
    mode_of_nonneg_discriminant (B := A * k) (R := k ^ 4 - c * k ^ 3 / l) hR
  refine ⟨s, ?_, ?_⟩
  · rw [hs]
    push_cast
    ring
  · rw [hre]
    exact growth_lower_bound hc hl hk

/-! ## The neutrality branch and the finite-band stability bound -/

/-- `(i x)^2 = -x^2`, the only complex identity needed for the neutral branch. -/
theorem I_mul_sq (x : ℂ) : (Complex.I * x) ^ 2 = -(x ^ 2) := by
  have hI2 : (1 : ℂ) + Complex.I ^ 2 = 0 := by
    rw [pow_two, Complex.I_mul_I]
    ring
  linear_combination (norm := ring_nf) (x ^ 2) * hI2

/-- **Neutral branch.**  If the discriminant `R` is negative, both branches of `s`
    are purely imaginary: the mode neither grows nor decays.  Together with
    `mode_of_nonneg_discriminant` this is the exact dichotomy — positive
    discriminant gives growth `sqrt R`, negative discriminant gives neutrality. -/
theorem neutral_mode_of_negative_discriminant {B R : ℝ} (hR : R < 0) :
    ∃ s : ℂ,
      (s + Complex.I * (B : ℂ)) ^ 2 = ((R : ℝ) : ℂ) ∧ s.re = 0 := by
  refine ⟨-(Complex.I * (B : ℂ))
      + Complex.I * ((Real.sqrt (-R) : ℝ) : ℂ), ?_, ?_⟩
  · have hstep : (-(Complex.I * (B : ℂ))
          + Complex.I * ((Real.sqrt (-R) : ℝ) : ℂ)) + Complex.I * (B : ℂ)
        = Complex.I * ((Real.sqrt (-R) : ℝ) : ℂ) := by ring
    rw [hstep, I_mul_sq]
    have hsq : ((Real.sqrt (-R) : ℝ) : ℂ) ^ 2 = ((-R : ℝ) : ℂ) := by
      rw [← Complex.ofReal_pow, Real.sq_sqrt (by linarith)]
    rw [hsq]
    push_cast
    ring
  · simp [Complex.mul_re]

/-- **One-sided finite-band stability bound.**  On the *one-sided* sector `l ≥ 1`
    (the sector `k l > 0`, i.e. `k > 0` here) the discriminant is non-positive for
    every retained mode as soon as `k ≤ c/N`: that sector is neutral, with
    threshold `k = c/N` shrinking like `1/N`.

    This is deliberately only one-sided.  The opposite-sign modes `l < 0` are
    unstable for *every* `k > 0` (discriminant `k^4 + c k^3/|l|`), which is why the
    full band is never stable — see `band_unstable_uniform_in_N`. -/
theorem band_stability_threshold {c k : ℝ} (hc : 0 < c) {N l : ℕ} (hN : 1 ≤ N)
    (hl1 : 1 ≤ l) (hlN : l ≤ N) (hk : 0 < k) (hkN : k ≤ c / N) :
    k ^ 4 - c * k ^ 3 / (l : ℝ) ≤ 0 := by
  have hl : (0 : ℝ) < (l : ℝ) := by exact_mod_cast hl1
  have hNr : (0 : ℝ) < (N : ℝ) := by exact_mod_cast hN
  have hle : c / (N : ℝ) ≤ c / (l : ℝ) :=
    (div_le_div_iff_of_pos_left hc hNr hl).mpr (by exact_mod_cast hlN)
  have hkN' : k ≤ c / (l : ℝ) := le_trans hkN hle
  have hfac : k ^ 4 - c * k ^ 3 / (l : ℝ) = k ^ 3 * (k - c / (l : ℝ)) := by ring_nf
  rw [hfac]
  exact mul_nonpos_of_nonneg_of_nonpos (by positivity) (by linarith)

/-- The edge of the one-sided stability region is sharp: `k > c/N` makes the
    extreme retained mode `l = N` unstable. -/
theorem band_instability_threshold {c k : ℝ} (hc : 0 < c) {N : ℕ} (hN : 1 ≤ N)
    (hk : c / N < k) : 0 < k ^ 4 - c * k ^ 3 / (N : ℝ) := by
  have hNr : (0 : ℝ) < (N : ℝ) := by exact_mod_cast hN
  have hk0 : 0 < k := lt_of_le_of_lt (div_nonneg (le_of_lt hc) (le_of_lt hNr)) hk
  have hfac : k ^ 4 - c * k ^ 3 / (N : ℝ) = k ^ 3 * (k - c / (N : ℝ)) := by ring_nf
  rw [hfac]
  exact mul_pos (by positivity) (by linarith)

/-! ## Tie to the retained band of `Spectral/Multiplier.lean` -/

/-- For every truncation `N ≥ 1` the retained band `-N..N` contains the mode
    `l = 1`. -/
theorem mode_one_mem_band (N : ℕ) (hN : 1 ≤ N) : ∃ i : Fin (2 * N + 1), modeIdx N i = 1 := by
  refine ⟨⟨N + 1, by omega⟩, ?_⟩
  simp only [modeIdx]
  push_cast
  omega

/-- For every truncation `N ≥ 1` the retained band `-N..N` contains the mode
    `l = -1` as well. -/
theorem mode_neg_one_mem_band (N : ℕ) (hN : 1 ≤ N) :
    ∃ i : Fin (2 * N + 1), modeIdx N i = -(1 : ℤ) := by
  refine ⟨⟨N - 1, by omega⟩, ?_⟩
  simp only [modeIdx]
  omega

/-- **No truncation in `y` is stable at any non-zero `x`-wavenumber.**  For every
    band `-N..N` with `N ≥ 1` the mode `l = -1` is retained, and for every `k > 0`
    that mode has discriminant `k^4 + c k^3 > 0`, hence a root with
    `Re s = sqrt (k^4 + c k^3) ≥ k^2`.  Nothing in the conclusion depends on `N`:
    refining the `y`-resolution never restores stability and never reduces the
    `x`-frequency growth rate. -/
theorem band_unstable_uniform_in_N (N : ℕ) (hN : 1 ≤ N) {c k A : ℝ}
    (hc : 0 < c) (hk : 0 < k) :
    (∃ i : Fin (2 * N + 1), modeIdx N i = -(1 : ℤ))
      ∧ ∃ s : ℂ,
          (s + Complex.I * ((A * k : ℝ) : ℂ)) ^ 2 = (((k ^ 4 + c * k ^ 3 : ℝ)) : ℂ)
            ∧ s.re = Real.sqrt (k ^ 4 + c * k ^ 3) ∧ k ^ 2 ≤ s.re := by
  have hR : 0 ≤ k ^ 4 + c * k ^ 3 := by positivity
  obtain ⟨s, hs, hre⟩ :=
    mode_of_nonneg_discriminant (B := A * k) (R := k ^ 4 + c * k ^ 3) hR
  refine ⟨mode_neg_one_mem_band N hN, s, hs, hre, ?_⟩
  rw [hre]
  refine (Real.le_sqrt (sq_nonneg k) hR).mpr ?_
  have h3 : 0 < c * k ^ 3 := by positivity
  nlinarith

/-- **A stable fixed truncation is not grid-uniform stability.**  For *every*
    `N ≥ 1` the retained band contains the mode `l = 1`, and for every `k ≥ c`
    there is a linearised mode in that band with `Re s ≥ k^2 - c k`.  Since `k` is
    the *continuous* `x`-wavenumber, letting `k → ∞` at fixed `N` gives unbounded
    growth. -/
theorem band_contains_growing_mode (N : ℕ) (hN : 1 ≤ N) {c k A : ℝ}
    (hc : 0 ≤ c) (hk : c ≤ k) :
    (∃ i : Fin (2 * N + 1), modeIdx N i = 1)
      ∧ ∃ s : ℂ,
          (s + Complex.I * ((A * k : ℝ) : ℂ)) ^ 2
              = ((k : ℂ)) ^ 4 - ((c : ℂ)) * ((k : ℂ)) ^ 3 / ((1 : ℝ) : ℂ)
            ∧ k ^ 2 - (c / 1) * k ≤ s.re :=
  ⟨mode_one_mem_band N hN,
    exists_growing_mode (c := c) (l := 1) (k := k) (A := A) hc (by norm_num) (by simpa using hk)⟩

end DLW.Spectral
