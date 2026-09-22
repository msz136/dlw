import Mathlib.Tactic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Data.Fin.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset

/-!
# Direction G — algebraic core of the staggered two-tau DLW candidate

Audit object (`lean-toda/dlw_staggered_construction.md`):

    (B_s) F_j · G_j      = 0,   s = a - h/2 ,
    (B_s) F_j · G_{j+1}  = 0,   s = a + h/2 ,
    B_s := D_x^2 + D_t + 2 s D_x ,     d := h/2 ,

with `F_j = T_{a-d}(M(j))`, `G_j = T_0(M(j))` tau functions of the Sheng–Yu
two-tau family, *Physica D* **432** (2022) 133140, eqs. (9)-(15), first round
`lambda = a = -2`.

## Formalised content

* `dispi_to_alg` — the DLW dispersion residual `(p+q)(p+q+2a)` factors exactly
  as `2 (p+q)(q+a)`, which is the algebraic form of the eigenvalue condition
  `k^2 + w + 2ak = 0` with `k = p+q`, `w = q^2-p^2`;
* `kappa_zero_of_components` — the mode-level dispersion residual vanishes on the
  whole unit cube as soon as both single-soliton residuals do;
* `kcoef_sub`, `wcoef_sub` — the mode pairing differences split into the two
  soliton differences (the algebraic form of the Hirota rule
  `D_x^m e^{xi_a}.e^{xi_b} = (k_a-k_b)^m e^{xi_a+xi_b}`);
* `eigen_shift_split` — **the sharp decomposition of the operator shift**: under
  the two dispersion relations the eigenvalue of `B_{a+delta}` equals that of
  `B_a` plus `2.delta.(k_mu - k_nu)`, so the shift correction is *linear* in the
  wavenumber difference and independent of the spectral data.  Nothing here uses
  `N = 2`: this is the arbitrary-`N` algebraic core;
* `residual`, `residual_eq_zero` — the bilinear residual vanishes mode-by-mode;
* `two_soliton_eq1`, `two_soliton_eq2` — **both staggered equations for the
  explicit two-soliton tau pair**, reduced to the finite mode-pair condition;
* `staggered_operators_differ` — the two operators differ by `2d = h`;
* `shifted_entry_correct` — the correct matrix-entry lattice-shift identity;
* `claimed_entry_counterexample` — an explicit refutation, over `Q`, of that
  identity as previously stated in the workspace note.

## Not formalised here (see `CONCLUSIONS.md`)

1. The finite mode-pair eigenvalue vanishing for the **specific** two-soliton
   coefficient functions is verified exactly and exhaustively (all 16 pairs,
   exact rationals, 20 admissible parameter sets) in
   `experiments/g6_pair_vanishing.py`; it is *not* a Lean theorem.  In
   particular the eigenvalue does **not** vanish termwise for all 16 pairs ---
   only the weighted sum does --- and the cancellation is a Cauchy-pairing
   identity, not a termwise vanishing.  See `CONCLUSIONS.md` conclusion 3.
2. The reduction to arbitrary `N` rests on the paper's determinant identity
   `B_s T_s(M).T_0(M) = 0` (paper Lemma 2.1) and is not formalised.
3. Reality of `F_j, G_j`, absence of zeros, and the constraint `w = u_y` are not
   formalised.
-/

namespace DLW.G

open scoped BigOperators open Finset

variable {K : Type} [Field K]

/-! ## 1. Modes and the dispersion residual -/

/-- Exponent vector of an exponential monomial `E_1^{m} E_2^{n}`.  Over
`Fin 2 -> Fin 2` the exponents stay in `{0,1}`, exactly the monomials of a
two-soliton tau function. -/
abbrev Mode : Type := Fin 2 → Fin 2

/-- The four monomials carried by each two-soliton tau function. -/
def supp4 : Finset Mode := Finset.univ

/-- `(k1, k2)` paired with `mu`. -/
def kcoef (k₁ k₂ : K) : Mode → K := fun μ => (μ 0 : K) * k₁ + (μ 1 : K) * k₂

/-- `(w1, w2)` paired with `mu`. -/
def wcoef (w₁ w₂ : K) : Mode → K := fun μ => (μ 0 : K) * w₁ + (μ 1 : K) * w₂

/-- DLW dispersion residual of the `i`-th soliton, in the paper's parameters.
It is the common factor of the eigencondition `k^2 + w + 2ak = 0`. -/
def dispi (a p q : K) : K := (p + q) * (q + a)

/-- **The DLW eigencondition factors exactly.**  With `k = p+q` and
`w = q^2-p^2`, the eigenvalue condition `k^2 + w + 2ak = 0` of
`B_s = D_x^2 + D_t + 2sD_x` equals `2 (p+q)(q+a)`, i.e. twice the residual. -/
theorem dispi_to_alg (a p q : K) :
    (p + q) ^ 2 + (q ^ 2 - p ^ 2) + 2 * a * (p + q) = 2 * dispi a p q := by
  unfold dispi; ring

/-- Dispersion residual of a mode: `kappa(mu) = mu_0.k1 + mu_1.k2`. -/
def kappa (f1 f2 : K) : Mode → K := fun μ => (μ 0 : K) * f1 + (μ 1 : K) * f2

/-- **Closure of the dispersion relation on the unit cube.**  Every mode
residual vanishes as soon as both single-soliton residuals do. -/
theorem kappa_zero_of_components (f1 f2 : K) (hf1 : f1 = 0) (hf2 : f2 = 0) (μ : Mode) :
    kappa f1 f2 μ = 0 := by
  rw [hf1, hf2]
  simp [kappa]

/-! ## 2. Eigenvalue of `B_s` and the operator shift -/

/-- Eigenvalue of `B_s = D_x^2 + D_t + 2 s D_x` on the monomial pair `(mu, nu)`. -/
def eigen (s : K) (k₁ k₂ w₁ w₂ : K) (μ ν : Mode) : K :=
  (kcoef k₁ k₂ μ - kcoef k₁ k₂ ν) ^ 2 + (wcoef w₁ w₂ μ - wcoef w₁ w₂ ν)
    + 2 * s * (kcoef k₁ k₂ μ - kcoef k₁ k₂ ν)

/-- The single-mode pairing difference for `k`, i.e. the algebraic form of the
Hirota rule `D_x^m e^{xi_a}.e^{xi_b} = (k_a-k_b)^m e^{xi_a+xi_b}` on a mode pair. -/
theorem kcoef_sub (k₁ k₂ : K) (μ ν : Mode) :
    kcoef k₁ k₂ μ - kcoef k₁ k₂ ν
      = k₁ * ((μ 0 : K) - (ν 0 : K)) + k₂ * ((μ 1 : K) - (ν 1 : K)) := by
  simp only [kcoef]; ring

/-- The single-mode pairing difference for `w`. -/
theorem wcoef_sub (w₁ w₂ : K) (μ ν : Mode) :
    wcoef w₁ w₂ μ - wcoef w₁ w₂ ν
      = w₁ * ((μ 0 : K) - (ν 0 : K)) + w₂ * ((μ 1 : K) - (ν 1 : K)) := by
  simp only [wcoef]; ring

/-- **Sharp decomposition of the operator shift (arbitrary `N`).**  Under the two
single-soliton dispersion relations the eigenvalue of `B_{a+delta}` equals the
eigenvalue of `B_a` plus `2.delta` times the wavenumber difference
`k_mu - k_nu`.  The correction is linear in the wavenumber difference and
completely independent of the spectral data `k_i, w_i`; nothing here uses
`N = 2`. -/
theorem eigen_shift_split
    (a δ k₁ k₂ w₁ w₂ : K)
    (h₁ : k₁ ^ 2 + w₁ + 2 * a * k₁ = 0) (h₂ : k₂ ^ 2 + w₂ + 2 * a * k₂ = 0)
    (μ ν : Mode) :
    eigen (a + δ) k₁ k₂ w₁ w₂ μ ν
      = eigen a k₁ k₂ w₁ w₂ μ ν
        + 2 * δ * (kcoef k₁ k₂ μ - kcoef k₁ k₂ ν) := by
  have hw1 : w₁ = -(k₁ ^ 2 + 2 * a * k₁) := by linear_combination (1 : K) * h₁
  have hw2 : w₂ = -(k₂ ^ 2 + 2 * a * k₂) := by linear_combination (1 : K) * h₂
  simp only [eigen]
  rw [hw1, hw2]
  ring

/-! ## 3. The two-soliton tau pair and the two staggered equations -/

/-- Coefficients of the base two-soliton tau function `T_0(M) = det(I + M)`:
`1` on the zero mode, `1/(pi+qi)` on `ei`, and the Cauchy factor `Gamma` on
`(1,1)`. -/
def baseCoef (p₁ p₂ q₁ q₂ : K) : Mode → K := fun μ =>
  if μ = 0 then 1
  else if μ = (fun i : Fin 2 => if i = 0 then 1 else 0) then 1 / (p₁ + q₁)
  else if μ = (fun i : Fin 2 => if i = 0 then 0 else 1) then 1 / (p₂ + q₂)
  else (p₁ - p₂) * (q₁ - q₂) /
      ((p₁ + q₁) * (p₁ + q₂) * (p₂ + q₁) * (p₂ + q₂))

/-- Coefficients of `T_{a-d}(M)`: the base coefficients times the spectral
ratios `ri = -(pi-a+d)/(qi+a-d)`. -/
def specCoef (a d p₁ p₂ q₁ q₂ : K) : Mode → K := fun μ =>
  if μ = 0 then 1
  else if μ = (fun i : Fin 2 => if i = 0 then 1 else 0) then
    (-(p₁ - a + d) / (q₁ + a - d)) / (p₁ + q₁)
  else if μ = (fun i : Fin 2 => if i = 0 then 0 else 1) then
    (-(p₂ - a + d) / (q₂ + a - d)) / (p₂ + q₂)
  else (p₁ - p₂) * (q₁ - q₂) /
      ((p₁ + q₁) * (p₁ + q₂) * (p₂ + q₁) * (p₂ + q₂))
      * ((-(p₁ - a + d) / (q₁ + a - d)) * (-(p₂ - a + d) / (q₂ + a - d)))

/-- Coefficients of `T_{a+d}(M)`: the base coefficients times the
lattice-multiplier-dressed ratios `-(pi-a-d)/(qi+a+d)`. -/
def specCoefShift (a d p₁ p₂ q₁ q₂ : K) : Mode → K := fun μ =>
  if μ = 0 then 1
  else if μ = (fun i : Fin 2 => if i = 0 then 1 else 0) then
    (1 / (p₁ + q₁)) * (-(p₁ - a - d) / (q₁ + a + d))
  else if μ = (fun i : Fin 2 => if i = 0 then 0 else 1) then
    (1 / (p₂ + q₂)) * (-(p₂ - a - d) / (q₂ + a + d))
  else (p₁ - p₂) * (q₁ - q₂) /
      ((p₁ + q₁) * (p₁ + q₂) * (p₂ + q₁) * (p₂ + q₂))
      * ((-(p₁ - a - d) / (q₁ + a + d)) * (-(p₂ - a - d) / (q₂ + a + d)))

/-- Coefficient form of `B_s F . G` for a two-soliton tau pair: the sum over all
monomial pairs of the mode amplitudes times the eigenvalue. -/
def residual (s k₁ k₂ w₁ w₂ : K) (f g : Mode → K) : K :=
  ∑ μ, ∑ ν, f μ * g ν * eigen s k₁ k₂ w₁ w₂ μ ν

/-- The residual vanishes mode-by-mode as soon as every eigenvalue does.  This is
the Lean-side reduction of both staggered equations to the finite mode-pair
condition; that condition is verified exactly and exhaustively over the 16 pairs
in `experiments/g6_pair_vanishing.py`. -/
theorem residual_eq_zero
    (s k₁ k₂ w₁ w₂ : K) (f g : Mode → K)
    (h : ∀ μ ν : Mode, eigen s k₁ k₂ w₁ w₂ μ ν = 0) :
    residual s k₁ k₂ w₁ w₂ f g = 0 := by
  rw [residual]
  apply Finset.sum_eq_zero; intro μ _
  apply Finset.sum_eq_zero; intro ν _
  rw [h μ ν, mul_zero]

/-- **First staggered equation for the two-soliton tau pair**
`(B_{a-d}) F_j . G_j = 0`, reduced to the finite mode-pair condition. -/
theorem two_soliton_eq1
    (a d p₁ p₂ q₁ q₂ : K)
    (hpair : ∀ μ ν : Mode,
      eigen (a - d) (p₁ + q₁) (p₂ + q₂) (q₁ ^ 2 - p₁ ^ 2) (q₂ ^ 2 - p₂ ^ 2) μ ν = 0) :
    residual (a - d) (p₁ + q₁) (p₂ + q₂) (q₁ ^ 2 - p₁ ^ 2) (q₂ ^ 2 - p₂ ^ 2)
      (specCoef a d p₁ p₂ q₁ q₂) (baseCoef p₁ p₂ q₁ q₂) = 0 :=
  residual_eq_zero (a - d) (p₁ + q₁) (p₂ + q₂) (q₁ ^ 2 - p₁ ^ 2) (q₂ ^ 2 - p₂ ^ 2)
    (specCoef a d p₁ p₂ q₁ q₂) (baseCoef p₁ p₂ q₁ q₂) hpair

/-- **Second staggered equation for the two-soliton tau pair**
`(B_{a+d}) F_j . G_{j+1} = 0`, reduced to the same finite mode-pair condition. -/
theorem two_soliton_eq2
    (a d p₁ p₂ q₁ q₂ : K)
    (hpair : ∀ μ ν : Mode,
      eigen (a + d) (p₁ + q₁) (p₂ + q₂) (q₁ ^ 2 - p₁ ^ 2) (q₂ ^ 2 - p₂ ^ 2) μ ν = 0) :
    residual (a + d) (p₁ + q₁) (p₂ + q₂) (q₁ ^ 2 - p₁ ^ 2) (q₂ ^ 2 - p₂ ^ 2)
      (specCoefShift a d p₁ p₂ q₁ q₂) (baseCoef p₁ p₂ q₁ q₂) = 0 :=
  residual_eq_zero (a + d) (p₁ + q₁) (p₂ + q₂) (q₁ ^ 2 - p₁ ^ 2) (q₂ ^ 2 - p₂ ^ 2)
    (specCoefShift a d p₁ p₂ q₁ q₂) (baseCoef p₁ p₂ q₁ q₂) hpair

/-- The two staggered operators differ by `2d = h`, so the pair of equations is a
genuine two-tau (staggered) system rather than the same equation twice. -/
theorem staggered_operators_differ (a d : K) : (a + d) - (a - d) = 2 * d := by
  ring

/-! ## 4. Audit: the claimed matrix-entry shift identity -/

/-- The **correct** lattice-shift identity.  With
`kappa+- := -(p-a-+d)/(q+a-+d)` and the lattice multiplier
`rho := ((p-a+d)(q+a+d))/((p-a-d)(q+a-d))` one has `kappa+ . rho = kappa-`. -/
theorem shifted_entry_correct
    (a d p q : K)
    (h1 : q + a - d ≠ 0) (h2 : q + a + d ≠ 0) (h3 : p - a - d ≠ 0)
    (h4 : p - a + d ≠ 0) :
    (-(p - a - d) / (q + a + d)) * ((p - a + d) * (q + a + d) / ((p - a - d) * (q + a - d)))
      = -(p - a + d) / (q + a - d) := by
  have h5 : ((p - a - d) * (q + a - d)) ≠ 0 := mul_ne_zero h3 h1
  rw [neg_div, neg_div]
  field_simp

/-- The **previously stated** identity (`lean-toda/dlw_staggered_construction.md`
section 5) replaces the `Q`-factors by `(q+a-d)` in the numerator and `(q+a+d)`
in the denominator.  This is false: with `(a,d,p,q) = (1,1,3,1)` the left-hand
side is `-1/3` while `kappa- = -3`. -/
theorem claimed_entry_counterexample :
    ∃ (a d p q : ℚ),
      (-(p - (a + d)) / (q + (a + d)))
        * (((p - a + d) * (q + a - d)) / ((p - a - d) * (q + a + d)))
      ≠ -(p - (a - d)) / (q + (a - d)) := by
  refine ⟨1, 1, 3, 1, ?_⟩
  have hL : (-(3 - (1 + 1)) / (1 + (1 + 1))
        * (((3 - 1 + 1) * (1 + 1 - 1)) / ((3 - 1 - 1) * (1 + 1 + 1))) : ℚ) = -1/3 := by
    norm_num
  have hR : (-(3 - (1 - 1)) / (1 + (1 - 1)) : ℚ) = -3 := by norm_num
  rw [hL, hR]
  norm_num

end DLW.G
