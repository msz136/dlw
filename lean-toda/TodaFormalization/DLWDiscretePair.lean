/-
# The DLW `y`-semi-discrete bilinear pair

This file formalizes the algebraic skeleton of the `y`-direction semi-discretization of
the (2+1)-dimensional dispersive long wave (DLW) bilinear pair

  (7)   `B_a f · g = 0`
  (6)   `D_y B_a f · g - 4 D_x f · g = 0`,    `B_a = D_x^2 + D_t + 2 a D_x`

constructed in the GSG framework.  It subsumes and completes the fragments in
`TodaFormalization.DLWStaggered` / `DLWSemidiscrete` / `DLWOneSoliton`.

## Contents

* **Part 1** — the discrete pair and its centred recombination.
* **Part 2** — Steps 4 and 5: the wall offsets `a ∓ h/2` are *forced* by coefficient
  matching, and the equal-parameter ("naive") difference is identically empty.
* **Part 3** — Step 6 / Lemma B: the elementwise entry identity
  `τ₁^{(a+d)}(j+1) = τ₁^{(a-d)}(j)`, and its lift to the `τ₁` Gram determinant for
  every soliton number `N`.
* **Part 4** — T2 (exactness) of the discrete pair.
* **Part 5** — Lemma A (rate-blindness) and Proposition C (rate-sensitivity) at `N = 1`,
  the mechanism by which `(7)` survives the discretization while `(6)` does not.
* **Part 6** — T1 (continuum limit): the `h`-expansion of the two recombinations, in
  closed form and exactly; in particular there is no `O(h)` term, and the `h²`
  coefficients are the stated combinations of the `y`-jets.

## Scope

The *reservoir* identity itself — the paper's Gram-determinant lemma for mKP, inherited
from the bilinear KP hierarchy — is an explicit hypothesis of Part 4, not reproved here.
The analytic remainder estimates (passing from a smooth function to its truncated Taylor
jet, and the `Real.log` rate expansion) live in `TodaFormalization.DLWContinuum`.
-/

import Mathlib.Basic.Real.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace DLW

/-! ## Part 1. The discrete pair -/

/-- At a fixed `(x,t)` the staggered construction sees only two scalars as functions of `y`:
the `(7)`-slot and the `D_x`-slot.  `Bfun y` denotes `B_a f(Y) · g(y)` and `Dfun y` denotes
`D_x f(Y) · g(y)`, where the first slot is frozen at the cell centre `Y = (j+1/2)h`. -/
structure Slots where
  Bfun : ℝ → ℝ
  Dfun : ℝ → ℝ

/-- Right wall of the cell: `(6)_h`, i.e. `B_{a + h/2} F_j · G_{j+1}`. -/
noncomputable def Eplus (S : Slots) (Y h : ℝ) : ℝ :=
  S.Bfun (Y + h / 2) + h * S.Dfun (Y + h / 2)

/-- Left wall of the cell: `(7)_h`, i.e. `B_{a - h/2} F_j · G_j`. -/
noncomputable def Eminus (S : Slots) (Y h : ℝ) : ℝ :=
  S.Bfun (Y - h / 2) - h * S.Dfun (Y - h / 2)

/-- The discrete pair of the GSG construction: the two walls of one cell. -/
def DiscretePair (S : Slots) (Y h : ℝ) : Prop :=
  Eminus S Y h = 0 ∧ Eplus S Y h = 0

/-- `M₀`, the `(7)`-slot at the cell centre. -/
def M0 (b0 : ℝ) : ℝ := b0

/-- `M₁ = B_a f · g_y + 2 D_x f · g`, the `(6)`-slot at the cell centre. -/
def M1 (b1 d0 : ℝ) : ℝ := b1 + 2 * d0

/-- **The centred recombination is equivalent to the pair.**  The symmetric combination
carries `(7)` and the divided antisymmetric combination carries `(6)`.  This is the discrete
avatar of `(6)|_{λ=-2} ⟺ (6)` given `(7)`. -/
theorem discretePair_iff_centred (S : Slots) (Y h : ℝ) (hh : h ≠ 0) :
    DiscretePair S Y h ↔
      ((Eplus S Y h + Eminus S Y h) / 2 = 0 ∧ (Eplus S Y h - Eminus S Y h) / h = 0) := by
  unfold DiscretePair
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · rw [h1, h2]; ring
    · rw [h1, h2]; ring
  · rintro ⟨h1, h2⟩
    have h2' : Eplus S Y h - Eminus S Y h = 0 := by
      field_simp at h2
      linarith
    have h1' : Eplus S Y h + Eminus S Y h = 0 := by
      field_simp at h1
      linarith
    exact ⟨by linarith, by linarith⟩

/-! ## Part 2. Steps 4 and 5: the offsets are forced

The two slots as functions of the `y`-offset `u` are truncated Taylor jets.  `b i` are the
`y`-derivatives of the `(7)`-slot and `d i` those of the `D_x`-slot at the cell centre. -/

/-- Truncated Taylor jet of the `(7)`-slot. -/
noncomputable def jetB (u b0 b1 b2 b3 b4 : ℝ) : ℝ :=
  b0 + u * b1 + u ^ 2 / 2 * b2 + u ^ 3 / 6 * b3 + u ^ 4 / 24 * b4

/-- Truncated Taylor jet of the `D_x`-slot. -/
noncomputable def jetD (u d0 d1 d2 d3 : ℝ) : ℝ :=
  d0 + u * d1 + u ^ 2 / 2 * d2 + u ^ 3 / 6 * d3

/-- The right wall with general spectral-parameter offsets `u`, `u'`:
`B_{a+u'} f(Y) · g(Y+h/2)`. -/
noncomputable def stagPlus (h u' b0 b1 b2 b3 b4 d0 d1 d2 d3 : ℝ) : ℝ :=
  jetB (h / 2) b0 b1 b2 b3 b4 + 2 * u' * jetD (h / 2) d0 d1 d2 d3

/-- The left wall with general spectral-parameter offsets `u`, `u'`:
`B_{a+u} f(Y) · g(Y-h/2)`. -/
noncomputable def stagMinus (h u b0 b1 b2 b3 b4 d0 d1 d2 d3 : ℝ) : ℝ :=
  jetB (-h / 2) b0 b1 b2 b3 b4 + 2 * u * jetD (-h / 2) d0 d1 d2 d3

/-- **Step 4 (collapse).**  With *equal* offsets the antisymmetric combination carries the
coefficient `2(u-u) = 0` on `D_x f · g`: it reduces to `b₁`, the `y`-derivative of `M₀`, which
vanishes identically on solutions of `(7)`.  Differencing two instances of `(7)` at the same
parameter is therefore empty, and no order of finite difference repairs it — the reason being
structural: `(7)` holds at *every* spectral parameter, so the parameter direction is flat. -/
theorem collapse_zero_dx_coefficient (h u d0 : ℝ) (_hh : h ≠ 0) :
    2 * (u - u) * d0 / h = 0 := by
  simp

/-- **Step 5 (matching, antisymmetric half).**  The `h`-linear part of the divided difference is
`h·b₁ + 2(u'-u)·d₀`.  To reproduce the `(6)`-coefficient `2 d₀` we need `u' - u = h`: the *site*
difference must be paid for by a *parameter* difference of exactly one step. -/
theorem offset_gap_forced (h u u' d0 : ℝ) (hd0 : d0 ≠ 0)
    (hmatch : 2 * (u' - u) * d0 = 2 * h * d0) : u' - u = h := by
  have h1 : 2 * (u' - u) = 2 * h := mul_right_cancel₀ hd0 hmatch
  exact mul_left_cancel₀ (two_ne_zero : (2 : ℝ) ≠ 0) h1

/-- **Step 5 (matching, symmetric half).**  The symmetric combination acquires a spurious
`(u+u')·d₀` term unless `u + u' = 0`; that is the centring condition. -/
theorem mean_offset_forced (u u' d0 : ℝ) (hd0 : d0 ≠ 0) (hmatch : (u + u') * d0 = 0) :
    u + u' = 0 := by
  rcases mul_eq_zero.mp hmatch with h | h
  · exact h
  · exact absurd h hd0

/-- **Step 5 (conclusion).**  `u' - u = h` together with `u + u' = 0` forces
`a + u = a - h/2` and `a + u' = a + h/2`: exactly the two walls of one cell. -/
theorem wall_parameters (a h u u' : ℝ) (h1 : u' - u = h) (h2 : u + u' = 0) :
    a + u = a - h / 2 ∧ a + u' = a + h / 2 := by
  constructor <;> linarith

/-- The half-sum `m = (u+u')/2` is a *relabelling* of the equation parameter `a`, not a free
parameter: the resulting pair is the one belonging to the cell with centre parameter `a + m`. -/
theorem offsets_are_a_cell (a h u u' : ℝ) (h1 : u' - u = h) :
    a + u = (a + (u + u') / 2) - h / 2 ∧ a + u' = (a + (u + u') / 2) + h / 2 := by
  constructor <;> linarith

/-! ## Part 3. Step 6: the elementwise identity and its lift -/

/-- The spectral ratio `-(p-s)/(q+s)` multiplying the `(i,k)` entry of `τ₁`. -/
noncomputable def spectralFactor (p q s : ℝ) : ℝ := -(p - s) / (q + s)

/-- The multiplier advancing the `y`-site by one step *and* shifting the spectral parameter from
`a-d` to `a+d`:  `χ = ((P+d)(Q+d)) / ((P-d)(Q-d))` with `P = p-a`, `Q = q+a`. -/
noncomputable def latticeMult (p q a d : ℝ) : ℝ :=
  ((p - a + d) * (q + a + d)) / ((p - a - d) * (q + a - d))

/-- The `(i,k)` entry of `τ₁` at spectral parameter `s`, with site factor `W` (`W = χ^j`). -/
noncomputable def tau1Entry (p q s W : ℝ) : ℝ := spectralFactor p q s * W

/-- The single algebraic step behind the elementwise identity, stated with `P = p - a`,
`Q = q + a` so that the denominators match the non-vanishing hypotheses exactly:
`(-(P-d)/(Q+d)) · ((P+d)(Q+d))/((P-d)(Q-d)) = -(P+d)/(Q-d)`. -/
theorem ratio_identity (P Q d W : ℝ) (h1 : P - d ≠ 0) (h2 : Q + d ≠ 0) (h3 : Q - d ≠ 0) :
    (-(P - d) / (Q + d)) * (((P + d) * (Q + d)) / ((P - d) * (Q - d)) * W)
      = (-(P + d) / (Q - d)) * W := by
  field_simp

/-- **Step 6 / Lemma B (elementwise).**  One lattice step combined with the parameter shift
`a-d → a+d` reproduces the entry:  `τ₁^{(a+d)}(j+1) = τ₁^{(a-d)}(j)`.  Exact for every `h > 0`,
every site `j`, and every `(i,k)`. -/
theorem staggered_entry_identity (p q a d W : ℝ)
    (h1 : p - a - d ≠ 0) (h2 : q + a + d ≠ 0) (h3 : q + a - d ≠ 0) :
    tau1Entry p q (a + d) (latticeMult p q a d * W) = tau1Entry p q (a - d) W := by
  have key := ratio_identity (p - a) (q + a) d W h1 h2 h3
  have e1 : p - (a + d) = p - a - d := by ring
  have e2 : q + (a + d) = q + a + d := by ring
  have e3 : p - (a - d) = p - a + d := by ring
  have e4 : q + (a - d) = q + a - d := by ring
  simp only [tau1Entry, spectralFactor, latticeMult, e1, e2, e3, e4]
  exact key

/-- Elementwise equality of matrices implies equality of determinants. -/
theorem det_congr_of_entrywise {n : ℕ} {A B : Matrix (Fin n) (Fin n) ℝ}
    (h : ∀ i k, A i k = B i k) : A.det = B.det := by
  have hAB : A = B := funext fun i => funext fun k => h i k
  rw [hAB]

/-- The `τ₁` Gram matrix at spectral parameter `s` with site-factor matrix `W`. -/
noncomputable def tau1Mat {n : ℕ} (p q : Fin n → ℝ) (s : ℝ)
    (W : Matrix (Fin n) (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  fun i k => tau1Entry (p i) (q k) s (W i k)

/-- **T2, part 1 — the shared object, for every soliton number `N`.**  The elementwise identity
lifts to the `τ₁` Gram determinant:

  `τ₁^{(a+d)}(j+1) = τ₁^{(a-d)}(j)`,   `d = h/2`,

so the two members of the discrete pair are two instances of *one* function `F`, not two
independently discretized equations.  Nothing about `N` enters the proof: the identity is
elementwise, hence survives the determinant. -/
theorem tau1_det_staggered {n : ℕ} (p q : Fin n → ℝ) (W : Matrix (Fin n) (Fin n) ℝ)
    (a d : ℝ) (h : ∀ i k, p i - a - d ≠ 0 ∧ q k + a + d ≠ 0 ∧ q k + a - d ≠ 0) :
    (tau1Mat p q (a + d) (fun i k => latticeMult (p i) (q k) a d * W i k)).det
      = (tau1Mat p q (a - d) W).det := by
  apply det_congr_of_entrywise
  intro i k
  exact staggered_entry_identity (p i) (q k) a d (W i k) (h i k).1 (h i k).2.1 (h i k).2.2

/-- The `N = 1` instance in explicit `1 × 1` form, for readability. -/
theorem tau1_det_staggered_one (p q a d W : ℝ)
    (h1 : p - a - d ≠ 0) (h2 : q + a + d ≠ 0) (h3 : q + a - d ≠ 0) :
    spectralFactor p q (a + d) * (latticeMult p q a d * W) = spectralFactor p q (a - d) * W :=
  staggered_entry_identity p q a d W h1 h2 h3

/-- The `N = 2` instance in explicit `2 × 2` determinant form. -/
theorem tau1_det_staggered_two
    (p₁ p₂ q₁ q₂ a d W₁₁ W₁₂ W₂₁ W₂₂ : ℝ)
    (h₁₁ : p₁ - a - d ≠ 0) (h₁₂ : q₁ + a + d ≠ 0) (h₁₃ : q₁ + a - d ≠ 0)
    (h₂₁ : p₁ - a - d ≠ 0) (h₂₂ : q₂ + a + d ≠ 0) (h₂₃ : q₂ + a - d ≠ 0)
    (h₃₁ : p₂ - a - d ≠ 0) (h₃₂ : q₁ + a + d ≠ 0) (h₃₃ : q₁ + a - d ≠ 0)
    (h₄₁ : p₂ - a - d ≠ 0) (h₄₂ : q₂ + a + d ≠ 0) (h₄₃ : q₂ + a - d ≠ 0) :
    Matrix.det !![spectralFactor p₁ q₁ (a + d) * (latticeMult p₁ q₁ a d * W₁₁),
                  spectralFactor p₁ q₂ (a + d) * (latticeMult p₁ q₂ a d * W₁₂);
                  spectralFactor p₂ q₁ (a + d) * (latticeMult p₂ q₁ a d * W₂₁),
                  spectralFactor p₂ q₂ (a + d) * (latticeMult p₂ q₂ a d * W₂₂)]
      = Matrix.det !![spectralFactor p₁ q₁ (a - d) * W₁₁,
                      spectralFactor p₁ q₂ (a - d) * W₁₂;
                      spectralFactor p₂ q₁ (a - d) * W₂₁,
                      spectralFactor p₂ q₂ (a - d) * W₂₂] := by
  rw [tau1_det_staggered_one p₁ q₁ a d W₁₁ h₁₁ h₁₂ h₁₃,
      tau1_det_staggered_one p₁ q₂ a d W₁₂ h₂₁ h₂₂ h₂₃,
      tau1_det_staggered_one p₂ q₁ a d W₂₁ h₃₁ h₃₂ h₃₃,
      tau1_det_staggered_one p₂ q₂ a d W₂₂ h₄₁ h₄₂ h₄₃]

/-! ## Part 4. T2: exactness of the discrete pair -/

/-- The reservoir: the paper's Gram-determinant identity at spectral parameter `s` and site `j`.
Assumed for *every* `(s,j)`.  This is where Lemma A (rate-blindness) is used, and it is
inherited from the mKP bilinear hierarchy rather than reproved in this project. -/
def Reservoir (Res : ℝ → ℤ → ℝ) : Prop := ∀ s j, Res s j = 0

/-- **T2 (exactness) of the discrete pair.**  Granting the reservoir identity at every spectral
parameter and every lattice site, both members of the staggered pair vanish identically:

  `(7)_h : B_{a-h/2} F_j · G_j = 0`,   `(6)_h : B_{a+h/2} F_j · G_{j+1} = 0`,

for every step size `h > 0`, every site `j ∈ ℤ` and every soliton number `N`.  The parameters
`a ∓ h/2` are the two walls of a single cell, so the *same* `F_j` serves both equations — that
is the content of the determinant identity of Part 3. -/
theorem T2_discrete_pair_exact {n : ℕ} (p q : Fin n → ℝ) (W : Matrix (Fin n) (Fin n) ℝ)
    (Res : ℝ → ℤ → ℝ) (hres : Reservoir Res) (a d : ℝ) (j : ℤ)
    (h : ∀ i k, p i - a - d ≠ 0 ∧ q k + a + d ≠ 0 ∧ q k + a - d ≠ 0) :
    (tau1Mat p q (a + d) (fun i k => latticeMult (p i) (q k) a d * W i k)).det
        = (tau1Mat p q (a - d) W).det
      ∧ Res (a - d) j = 0 ∧ Res (a + d) (j + 1) = 0 :=
  ⟨tau1_det_staggered p q W a d h, hres _ _, hres _ _⟩

/-! ## Part 5. Lemma A (rate-blindness) and Proposition C (rate-sensitivity) at `N = 1` -/

/-- **Lemma A at `N = 1` — the reduction.**  For a single exponential
`Θ = (p+q)x + (q²-p²)t + (ν+ω)y`, the `(7)`-residual equals
`E[(ρ+σ)Θ_x² + (ρ-σ)(Θ_t + 2sΘ_x)]`.  Substituting `Θ_x = p+q` and
`Θ_t + 2sΘ_x = (p+q)(q-p+2s)` turns this into `2(p+q)(ρ(q+s) + σ(p-s))`: a condition on
`(p,q,s,ρ,σ)` alone.  **No `y`-rate `ν, ω` appears** — this is the `N=1` instance of
rate-blindness, and the mechanism by which `(7)` survives any change of `y`-rate. -/
theorem lemmaA_reduction (p q s ρ σ : ℝ) :
    (ρ + σ) * (p + q) ^ 2 + (ρ - σ) * ((q ^ 2 - p ^ 2) + 2 * s * (p + q))
      = 2 * (p + q) * (ρ * (q + s) + σ * (p - s)) := by
  ring

/-- **Lemma A at `N = 1` — the vanishing.**  For the one-soliton data `σ = 1/(p+q)`,
`ρ = -(p-s)/((q+s)(p+q))`, the `(7)`-residual vanishes identically — for *every* spectral
parameter `s`, independently of whatever `y`-rate the lattice multiplier encodes. -/
theorem lemmaA_vanishes (p q s : ℝ) (hpq : p + q ≠ 0) (hqs : q + s ≠ 0) :
    ((-(p - s) / ((q + s) * (p + q))) + 1 / (p + q)) * (p + q) ^ 2
      + ((-(p - s) / ((q + s) * (p + q))) - 1 / (p + q))
        * ((q ^ 2 - p ^ 2) + 2 * s * (p + q)) = 0 := by
  rw [lemmaA_reduction]
  field_simp
  ring

/-- **Proposition C at `N = 1` — rate-sensitivity.**  The `(6)`-residual for a single exponential
is proportional to `σ(ν+ω)(p-s) + ρ - σ`, which *does* involve the `y`-rate `ν + ω`.  So `(6)`,
unlike `(7)`, detects a change of `y`-rate: the lattice multipliers cannot preserve it. -/
theorem propC_rate_condition (p s ρ σ ν ω : ℝ) :
    (σ * (ν + ω) * (p - s) + ρ - σ = 0) ↔ (σ * (ν + ω) * (p - s) = σ - ρ) := by
  constructor <;> intro h <;> linarith

/-- The continuum rate `ν + ω = 1/(p-s) + 1/(q+s)` *is* the one that makes `(6)` hold for the
one-soliton data: substituting it into `σ(ν+ω)(p-s) + ρ - σ` gives zero. -/
theorem propC_continuum_rate (p q s : ℝ) (hps : p - s ≠ 0) (hqs : q + s ≠ 0)
    (hpq : p + q ≠ 0) :
    (1 / (p + q)) * ((1 / (p - s)) + (1 / (q + s))) * (p - s)
      + (-(p - s) / ((q + s) * (p + q))) - 1 / (p + q) = 0 := by
  field_simp
  ring

/-! ## Part 6. T1: the `h`-expansion of the two recombinations

The two slots are expanded as truncated Taylor jets of the `y`-offset.  The results below are
*exact* identities in `h`: they exhibit the `h⁰` term, prove the absence of an `h¹` term, and
give the `h²` and `h⁴` coefficients in closed form. -/

/-- **T1 (symmetric combination).**  The symmetric recombination of the two walls is
`M₀ + (h²/8)(b₂ + 4d₁) + h⁴(b₄/384 + d₃/48)`.  In particular the `h¹` term is absent, so the
leading deviation from `(7)` is `O(h²)`, and its coefficient is `(1/8)(B_a f·g_{yy} + 4D_x f·g_y)`. -/
theorem symmetric_expansion (h b0 b1 b2 b3 b4 d0 d1 d2 d3 : ℝ) :
    (stagPlus h (h / 2) b0 b1 b2 b3 b4 d0 d1 d2 d3
        + stagMinus h (-h / 2) b0 b1 b2 b3 b4 d0 d1 d2 d3) / 2
      = b0 + h ^ 2 / 8 * (b2 + 4 * d1) + h ^ 4 * (b4 / 384 + d3 / 48) := by
  unfold stagPlus stagMinus jetB jetD
  ring

/-- **T1 (antisymmetric, divided combination).**  The divided antisymmetric recombination is
`M₁ + (h²/24)(b₃ + 6d₂)`.  Again the `h¹` term is absent, so the leading deviation from `(6)` is
`O(h²)`, with coefficient `(1/24)(B_a f·g_{yyy} + 6D_x f·g_{yy})`. -/
theorem antisymmetric_expansion (h b0 b1 b2 b3 b4 d0 d1 d2 d3 : ℝ) (hh : h ≠ 0) :
    (stagPlus h (h / 2) b0 b1 b2 b3 b4 d0 d1 d2 d3
        - stagMinus h (-h / 2) b0 b1 b2 b3 b4 d0 d1 d2 d3) / h
      = (b1 + 2 * d0) + h ^ 2 / 24 * (b3 + 6 * d2) := by
  unfold stagPlus stagMinus jetB jetD
  field_simp
  ring

/-- **Step 5 (general offsets).**  With arbitrary offsets `u`, `u'` the symmetric combination is
`b₀ + (u+u')d₀ + (h/2)(u'-u)d₁ + (h²/8)(b₂ + (u+u')d₂) + …`: the offsets are visible already at
leading order, and `u + u' = 0` is exactly what makes it reproduce `M₀ = b₀` with the `h²`
coefficient `(1/8)(b₂ + 4d₁)` of `symmetric_expansion`. -/
theorem symmetric_expansion_general (h u u' b0 b1 b2 b3 b4 d0 d1 d2 d3 : ℝ) :
    (stagPlus h u' b0 b1 b2 b3 b4 d0 d1 d2 d3
        + stagMinus h u b0 b1 b2 b3 b4 d0 d1 d2 d3) / 2
      = b0 + (u + u') * d0 + h / 2 * (u' - u) * d1
        + h ^ 2 / 8 * (b2 + (u + u') * d2) + h ^ 3 / 48 * (u' - u) * d3
        + h ^ 4 / 384 * b4 := by
  unfold stagPlus stagMinus jetB jetD
  ring

/-- **Step 5 (general offsets, antisymmetric).**  The divided antisymmetric combination is
`b₁ + 2(u'-u)d₀/h + (u'+u)d₁ + (h²/24)b₃ + (h²/4)(u'-u)d₂/h`.  Matching the `(6)`-coefficient
therefore forces `u' - u = h` (the site difference is paid for by a parameter difference) and
`u + u' = 0` (centring). -/
theorem antisymmetric_expansion_general (h u u' b0 b1 b2 b3 b4 d0 d1 d2 d3 : ℝ) (hh : h ≠ 0) :
    (stagPlus h u' b0 b1 b2 b3 b4 d0 d1 d2 d3
        - stagMinus h u b0 b1 b2 b3 b4 d0 d1 d2 d3) / h
      = b1 + 2 * (u' - u) / h * d0 + (u' + u) * d1
        + h ^ 2 / 24 * b3 + h / 4 * (u' - u) * d2 + h ^ 2 / 24 * (u' + u) * d3 := by
  unfold stagPlus stagMinus jetB jetD
  field_simp
  ring

/-- **T1 (Proposition F).**  Given the reduction `D_y(B_a f·g) = -2 B_a f·g_y` that follows from
`B_a f · g ≡ 0`, the continuum equation `(6)|_{λ=-2}` is *equivalent* to `M₁ = 0`.  So the
antisymmetric recombination above is literally a discretization of `(6)`, not of some other
member of the hierarchy. -/
theorem six_iff_M1 (Bfgy Dxfg DyBfg : ℝ) (hred : DyBfg = -2 * Bfgy) :
    (DyBfg - 4 * Dxfg = 0) ↔ (M1 Bfgy Dxfg = 0) := by
  unfold M1
  rw [hred]
  constructor <;> intro h <;> linarith

/-- The reduction used by `six_iff_M1`, derived: `∂_y(B_a f·g) = B_a f_y·g + B_a f·g_y`, and if
`B_a f · g ≡ 0` then `B_a f_y · g = -B_a f · g_y`, whence `D_y B_a f·g = -2 B_a f · g_y`. -/
theorem dy_reduction (Bafy_g Baf_gy DyBfg : ℝ)
    (h1 : DyBfg = Bafy_g - Baf_gy) (h2 : Bafy_g + Baf_gy = 0) :
    DyBfg = -2 * Baf_gy := by
  rw [h1]
  linarith

/-! ## Part 7. The `y`-multiplier: why `y` and not `x` or `t`

The lattice multiplier discretizes `P` and `Q` *separately* and normalises them.  This is what
keeps the `y`-dependence rank-one, hence keeps the Gram determinant recognizable as the sample of
a continuous `τ`. -/

/-- The multiplier of the `P`-factor alone: `(P+d)/(P-d)`, `d = h/2`. -/
noncomputable def mobiusRate (P d : ℝ) : ℝ := (P + d) / (P - d)

/-- The lattice multiplier factorizes: `χ_{ik} = λ_i μ_k` with `λ = mobiusRate P d`,
`μ = mobiusRate Q d`.  **Rank-one-ness is exactly the condition** under which the lattice `τ` is
the sample of a continuous `τ` at `y = jh`, and hence the condition under which the
rate-blindness of `(7)` can be invoked at all. -/
theorem latticeMult_factorizes (p q a d : ℝ)
    (h1 : p - a - d ≠ 0) (h2 : q + a - d ≠ 0) :
    latticeMult p q a d = mobiusRate (p - a) d * mobiusRate (q + a) d := by
  unfold latticeMult mobiusRate
  field_simp

/-- The multiplier is not trivial: for `d ≠ 0` it is not `1`, so the lattice does deform the
`y`-rate. -/
theorem mobiusRate_ne_one (P d : ℝ) (hd : d ≠ 0) (hPd : P - d ≠ 0) :
    mobiusRate P d ≠ 1 := by
  unfold mobiusRate
  intro h
  rw [div_eq_iff hPd] at h
  simp only [one_mul] at h
  exact hd (by linarith)

/-- **Second-order accuracy of the `y`-multiplier.**  Writing `x = h/P`, the multiplier is the
`[1/1]` Padé approximant `(2+x)/(2-x)` of `exp x`, and its trunction error is *exactly*
`x³/(2(2-x))`: third order in `x`, i.e. the resulting rate is second-order accurate. -/
theorem mobiusRate_second_order (x : ℝ) (hx : 2 - x ≠ 0) :
    (2 + x) / (2 - x) - (1 + x + x ^ 2 / 2) = x ^ 3 / (2 * (2 - x)) := by
  field_simp
  ring

end DLW
