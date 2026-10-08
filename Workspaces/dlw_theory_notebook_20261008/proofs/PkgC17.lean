/-
Package: C17 — the F-lattice sampling identities and the `O(h^2)` consistency errors.

Verified in this file:

* `c17_sample_physU`, `c17_sample_physV` — the *exact* identities
  `physU (sampleF h f) (sampleG h g) = sampleF h (interpU h f g)` (and the `V` analogue),
  valid for every `h` including `0`; index arithmetic only.
* `c17_proved` — target `C17`: the two identities plus `PowBound 2` for
  `interpU - cu` and `interpV - cv`, at an arbitrary point `(x, y, t)`.

The estimates are obtained by writing the exact errors as combinations of centred
differences of the Taylor remainders of the one-variable functions
`u ↦ ∂_x log f (x,u,t)` and `u ↦ ∂_x log g (x,u,t)`, which are `C^3` because they are
partial derivatives of a `C^∞` two-variable function.

Everything below uses the frozen statements of `Contracts.lean` verbatim (through the
definitions `interpU`, `interpV`, `physU`, `physV`, `sampleF`, `sampleG`, `cu`, `cv`, `C17`);
no hypothesis is added to any of them and no target is restated.
-/
import Contracts
import PkgNumeric
import PkgC11
import PkgC02
import Mathlib.Analysis.Calculus.Taylor
import Mathlib.Tactic

set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false
set_option linter.unreachableTactic false
set_option maxHeartbeats 1600000

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## Numeral reduction on the lattice level -/

/-- Numerals in `Lattice` are constant functions. -/
@[simp] private lemma c17_ofNat_lattice (n : ℕ) (j : ℤ) (x t : ℝ) :
    (((OfNat.ofNat n : Lattice) j) x t) = (OfNat.ofNat n : ℝ) := rfl

/-! ## Part 1 — the exact sampling identities -/

private theorem c17_sample_physU (f g : XYT) (h : ℝ) :
    physU (sampleF h f) (sampleG h g) = sampleF h (interpU h f g) := by
  funext j x t
  simp only [physU, lx, dx, logL, sampleF, sampleG, slice, interpU, sx,
    Pi.sub_apply, Pi.add_apply, Pi.mul_apply, c02_ofNat_apply, c02_ofNat_apply_XT,
    c17_ofNat_lattice]
  refine congrArg (fun F : ℝ → ℝ => deriv F x) ?_
  funext z
  have hB : (j : ℝ) * h = (((j : ℝ) + 1/2) * h - h/2) := by ring
  have hC : (((j + 1 : ℤ) : ℝ)) * h = (((j : ℝ) + 1/2) * h + h/2) := by
    rw [Int.cast_add, Int.cast_one]; ring
  simp only [hB, hC]

private theorem c17_sample_physV (f g : XYT) (h : ℝ) :
    physV h (sampleF h f) (sampleG h g) = sampleF h (interpV h f g) := by
  funext j x t
  -- unfold `physV` but *not* `physU`/`sampleF`, so that the sampling identity applies
  simp only [physV, d0, Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul]
  have hPU : ∀ k : ℤ, physU (sampleF h f) (sampleG h g) k
      = sampleF h (interpU h f g) k := fun k => congrFun (c17_sample_physU f g h) k
  rw [hPU (j+1), hPU (j-1)]
  -- unfold everything down to `deriv (fun z => ...) x`
  simp only [lx, dx, logL, sampleF, sampleG, slice, interpV, interpU, sx, Pi.add_apply,
    Pi.smul_apply, Pi.sub_apply, Pi.mul_apply, smul_eq_mul, c02_ofNat_apply,
    c02_ofNat_apply_XT, c17_ofNat_lattice]
  -- canonical sample abscissa `Y = (j + 1/2) h`
  set Y : ℝ := ((j : ℝ) + 1/2) * h with hY
  have e1 : (((j + 1 : ℤ) : ℝ)) * h = Y + h/2 := by rw [hY]; push_cast; ring
  have e2 : (j : ℝ) * h = Y - h/2 := by rw [hY]; ring
  have e3 : (((j + 1 + 1 : ℤ) : ℝ)) * h = Y + 3*h/2 := by rw [hY]; push_cast; ring
  have e4 : (((j - 1 : ℤ) : ℝ)) * h = Y - 3*h/2 := by rw [hY]; push_cast; ring
  have e5 : ((((j + 1 : ℤ) : ℝ)) + 1/2) * h = Y + h := by rw [hY]; push_cast; ring
  have e6 : ((((j - 1 : ℤ) : ℝ)) + 1/2) * h = Y - h := by rw [hY]; push_cast; ring
  have f1 : (Y + h) - h/2 = Y + h/2 := by ring
  have f2 : (Y + h) + h/2 = Y + 3*h/2 := by ring
  have f3 : (Y - h) - h/2 = Y - 3*h/2 := by ring
  have f4 : (Y - h) + h/2 = Y - h/2 := by ring
  simp only [e1, e2, e3, e4, e5, e6, f1, f2, f3, f4]
  ring

/-! ## `PowBound` tools -/

/-- Multiplication by a constant preserves `PowBound`. -/
private theorem c17_powBound_const_mul {p : ℕ} {X : ℝ → ℝ} (c : ℝ) (hX : PowBound p X) :
    PowBound p (fun h => c * X h) := by
  obtain ⟨C, hC, ε, hε, hb⟩ := hX
  refine ⟨|c| * C, by positivity, ε, hε, fun h hh hlt => ?_⟩
  rw [abs_mul]
  calc |c| * |X h| ≤ |c| * (C * |h| ^ p) := mul_le_mul_of_nonneg_left (hb h hh hlt) (abs_nonneg c)
    _ = |c| * C * |h| ^ p := by ring

/-- Negation preserves `PowBound`. -/
private theorem c17_powBound_neg {p : ℕ} {X : ℝ → ℝ} (hX : PowBound p X) :
    PowBound p (fun h => -X h) := by
  obtain ⟨C, hC, ε, hε, hb⟩ := hX
  exact ⟨C, hC, ε, hε, fun h hh hlt => by simpa only [abs_neg] using hb h hh hlt⟩

/-- Difference of two `PowBound`s at the same order. -/
private theorem c17_powBound_sub {p : ℕ} {X Y : ℝ → ℝ} (hX : PowBound p X)
    (hY : PowBound p Y) : PowBound p (fun h => X h - Y h) :=
  c11_powBound_add hX (c17_powBound_neg hY) (fun h => by ring)

/-- The scaled symmetrised difference quotient of an `O(|u|^{p+1})` remainder. -/
private theorem c17_powBound_symm_scaled {p : ℕ} {R : ℝ → ℝ} (c : ℝ) (hc : 0 < c)
    (hR : PowBound (p + 1) R) :
    PowBound p (fun h : ℝ => (R (c*h) - R (-(c*h)))/(2*c*h)) := by
  obtain ⟨C, hC, ε, hε, hb⟩ := hR
  refine ⟨C * c ^ p, by positivity, ε / c, by positivity, fun h hh hlt => ?_⟩
  have hch : |c * h| = c * |h| := by rw [abs_mul, abs_of_pos hc]
  have hhpos : 0 < |c*h| := by rw [hch]; exact mul_pos hc hh
  have hltc : |c*h| < ε := by
    rw [hch]
    have h1 : |h| * c < ε := (lt_div_iff₀ hc).mp hlt
    calc c * |h| = |h| * c := by ring
      _ < ε := h1
  have b1 : |R (c*h)| ≤ C * |c*h| ^ (p + 1) := hb (c*h) hhpos hltc
  have b2 : |R (-(c*h))| ≤ C * |c*h| ^ (p + 1) := by
    have h := hb (-(c*h)) (by rwa [abs_neg]) (by rwa [abs_neg])
    rwa [abs_neg] at h
  simp only [abs_div, abs_mul, abs_of_pos (by norm_num : (0:ℝ) < 2), abs_of_pos hc]
  rw [div_le_iff₀ (by positivity : (0:ℝ) < 2 * c * |h|)]
  calc |R (c*h) - R (-(c*h))| ≤ |R (c*h)| + |R (-(c*h))| := by
        calc |R (c*h) - R (-(c*h))| = |R (c*h) + -R (-(c*h))| := by rw [sub_eq_add_neg]
          _ ≤ |R (c*h)| + |-R (-(c*h))| := abs_add_le _ _
          _ = |R (c*h)| + |R (-(c*h))| := by rw [abs_neg]
    _ ≤ C * |c*h| ^ (p+1) + C * |c*h| ^ (p+1) := add_le_add b1 b2
    _ = 2 * C * |c*h| ^ (p+1) := by ring
    _ = C * c^p * |h|^p * (2 * c * |h|) := by
        rw [hch, mul_pow, pow_succ, pow_succ]; ring

/-- `c = 1`: the centred difference quotient `(R h - R (-h))/(2h)` is `O(|h|^p)`. -/
private theorem c17_powBound_symm_dbl {p : ℕ} {R : ℝ → ℝ} (hR : PowBound (p + 1) R) :
    PowBound p (fun h : ℝ => (R h - R (-h))/(2*h)) := by
  have hgen := c17_powBound_symm_scaled (p := p) (R := R) (c := 1) one_pos hR
  refine powBound_congr
    (e₁ := fun h : ℝ => (R ((1:ℝ)*h) - R (-((1:ℝ)*h)))/(2*(1:ℝ)*h)) ?_ hgen
  intro h
  simp only [one_mul, mul_one]

/-- `c = 3/2`: the centred difference quotient `(R (3h/2) - R (-(3h/2)))/(3h)` is `O(|h|^p)`. -/
private theorem c17_powBound_symm_3half {p : ℕ} {R : ℝ → ℝ} (hR : PowBound (p + 1) R) :
    PowBound p (fun h : ℝ => (R (3*h/2) - R (-(3*h/2)))/(3*h)) := by
  have hgen := c17_powBound_symm_scaled (p := p) (R := R) (c := (3:ℝ)/2) (by norm_num) hR
  refine powBound_congr
    (e₁ := fun h : ℝ => (R (((3:ℝ)/2)*h) - R (-(((3:ℝ)/2)*h)))/(2*((3:ℝ)/2)*h)) ?_ hgen
  intro h
  have h1 : ((3:ℝ)/2)*h = 3*h/2 := by ring
  have h2 : (2*((3:ℝ)/2))*h = 3*h := by ring
  rw [h1, h2]

/-! ## The Taylor-remainder bridge -/

/-- The degree-2 Taylor polynomial of `φ` at `y`, evaluated at `y + u`. -/
private lemma c17_taylor_two (φ : ℝ → ℝ) (y u : ℝ) :
    taylorWithinEval φ 2 Set.univ y (y + u)
      = φ y + u * deriv φ y + (u^2/2) * deriv (deriv φ) y := by
  rw [taylorWithinEval_eq_sum φ 2 y u]
  simp only [Finset.sum_range_succ, Finset.sum_range_zero, zero_add, iteratedDeriv_zero,
    iteratedDeriv_one, iteratedDeriv_succ, Nat.factorial_zero, Nat.factorial_one,
    Nat.factorial_two, Nat.cast_one, Nat.cast_ofNat, inv_one, pow_zero, pow_one,
    one_mul, mul_one, one_smul, smul_eq_mul]
  ring

/-- The degree-2 Taylor remainder of a `C^3` function is `O(|u|^3)`. -/
private theorem c17_powBound_taylor_rem (φ : ℝ → ℝ) (y : ℝ) (hφ : ContDiff ℝ 3 φ) :
    PowBound 3 (fun u : ℝ =>
      φ (y+u) - (φ y + u * deriv φ y + (u^2/2) * deriv (deriv φ) y)) := by
  have hbase : PowBound 3 (fun u : ℝ => φ (y+u) - taylorWithinEval φ 2 Set.univ y (y+u)) :=
    c11_powBound_norm_abs (powBound_taylor_poly 2 φ y hφ)
  refine powBound_congr
    (e₁ := fun u : ℝ => φ (y+u) - taylorWithinEval φ 2 Set.univ y (y+u)) ?_ hbase
  intro u
  rw [c17_taylor_two φ y u]

/-! ## Target C17 -/

theorem c17_proved : C17 := by
  intro f g hf hg hpf hpg
  refine ⟨fun h => ⟨c17_sample_physU f g h, c17_sample_physV f g h⟩, ?_⟩
  intro x y t
  have hLf : Smooth3 (c02log f) := c02_smooth_log hf hpf
  have hLg : Smooth3 (c02log g) := c02_smooth_log hg hpg
  let Wf : ℝ × ℝ → ℝ := fun p => c02log f p.1 p.2 t
  let Wg : ℝ × ℝ → ℝ := fun p => c02log g p.1 p.2 t
  have hWf : ContDiff ℝ ⊤ Wf := c02_smooth_fixed_t (c02log f) hLf t
  have hWg : ContDiff ℝ ⊤ Wg := c02_smooth_fixed_t (c02log g) hLg t
  have hWfd : Differentiable ℝ Wf := hWf.differentiable c02_top_ne_zero
  have hWgd : Differentiable ℝ Wg := hWg.differentiable c02_top_ne_zero
  let A : ℝ → ℝ := fun u => sx (c02log f) x u t
  let B : ℝ → ℝ := fun u => sx (c02log g) x u t
  have hA3 : ContDiff ℝ 3 A := by
    have hfun : A = fun u => fderiv ℝ Wf (x,u) (1,0) := by
      funext u
      exact c02_deriv_fst Wf x u ((hWfd (x,u)).hasFDerivAt)
    rw [hfun]
    exact ((c02_smooth_partial_fst Wf hWf).comp (contDiff_prodMk_right (e₀ := x))).of_le le_top
  have hB3 : ContDiff ℝ 3 B := by
    have hfun : B = fun u => fderiv ℝ Wg (x,u) (1,0) := by
      funext u
      exact c02_deriv_fst Wg x u ((hWgd (x,u)).hasFDerivAt)
    rw [hfun]
    exact ((c02_smooth_partial_fst Wg hWg).comp (contDiff_prodMk_right (e₀ := x))).of_le le_top
  have hA_deriv : ∀ u : ℝ, HasDerivAt (fun z => c02log f z u t) (A u) x := by
    intro u
    have hd : HasFDerivAt Wf (fderiv ℝ Wf (x, u)) (x, u) := (hWfd (x,u)).hasFDerivAt
    have h := c02_hasDerivAt_fst Wf x u hd
    rw [← c02_deriv_fst Wf x u hd] at h
    exact h
  have hB_deriv : ∀ u : ℝ, HasDerivAt (fun z => c02log g z u t) (B u) x := by
    intro u
    have hd : HasFDerivAt Wg (fderiv ℝ Wg (x, u)) (x, u) := (hWgd (x,u)).hasFDerivAt
    have h := c02_hasDerivAt_fst Wg x u hd
    rw [← c02_deriv_fst Wg x u hd] at h
    exact h
  -- the exact `interpU` and `cu` values
  have hIU : ∀ (h y' : ℝ), interpU h f g x y' t = 2 * A y' - B (y' - h/2) - B (y' + h/2) := by
    intro h y'
    have hc := (((hA_deriv y').const_mul (2:ℝ)).sub (hB_deriv (y' - h/2))).sub
      (hB_deriv (y' + h/2))
    exact hc.deriv
  have hcu : cu f g x y t = 2 * (A y - B y) := by
    rw [c02_cu_eq f g, c02_sx_sub (c02log f) (c02log g) hLf hLg]
    rfl
  have hcv : cv f g x y t = 2 * (deriv A y + deriv B y) := by
    rw [c02_cv_eq f g, c02_sy_add (c02log f) (c02log g) hLf hLg,
      c02_sx_add (sy (c02log f)) (sy (c02log g)) (c02_smooth_sy hLf) (c02_smooth_sy hLg),
      ← c02_sy_sx (c02log f) hLf, ← c02_sy_sx (c02log g) hLg]
    rfl
  -- the Taylor remainders
  let RA : ℝ → ℝ := fun u => A (y+u) - (A y + u * deriv A y + (u^2/2) * deriv (deriv A) y)
  let RB : ℝ → ℝ := fun u => B (y+u) - (B y + u * deriv B y + (u^2/2) * deriv (deriv B) y)
  have hRA : PowBound 3 RA := by
    have h := c17_powBound_taylor_rem A y hA3
    refine powBound_congr (e₁ := fun u : ℝ =>
      A (y+u) - (A y + u * deriv A y + (u^2/2) * deriv (deriv A) y)) ?_ h
    intro u
    rfl
  have hRB : PowBound 3 RB := by
    have h := c17_powBound_taylor_rem B y hB3
    refine powBound_congr (e₁ := fun u : ℝ =>
      B (y+u) - (B y + u * deriv B y + (u^2/2) * deriv (deriv B) y)) ?_ h
    intro u
    rfl
  constructor
  · -- `interpU - cu` is `O(h^2)`
    have hUerr : ∀ h : ℝ, interpU h f g x y t - cu f g x y t
        = -2 * ((RB (h/2) + RB (-(h/2)))/2) - (h^2/4) * deriv (deriv B) y := by
      intro h
      rw [hIU h y, hcu]
      dsimp only [RB]
      simp only [sub_eq_add_neg]
      ring
    have hQ : PowBound 2 (fun h : ℝ => (RB (h/2) + RB (-(h/2)))/2) :=
      c11_powBound_symm_avg (p := 2) hRB
    have hX : PowBound 2 (fun h : ℝ => -2 * ((RB (h/2) + RB (-(h/2)))/2)) :=
      c17_powBound_const_mul (-2) hQ
    have hY : PowBound 2 (fun h : ℝ => -((h^2/4) * deriv (deriv B) y)) := by
      have h := c11_powBound_quad (-(2 * deriv (deriv B) y))
      refine powBound_congr
        (e₁ := fun h : ℝ => (h^2/8) * (-(2 * deriv (deriv B) y))) ?_ h
      intro h
      ring
    have hZ : PowBound 2 (fun h : ℝ =>
        -2 * ((RB (h/2) + RB (-(h/2)))/2) - (h^2/4) * deriv (deriv B) y) :=
      c11_powBound_add hX hY (fun h => by ring)
    exact powBound_congr (fun h => (hUerr h).symm) hZ
  · -- `interpV - cv` is `O(h^2)`
    have hBsy : ∀ (h y' : ℝ),
        (sx (fun x y t => Real.log (g x (y + h/2) t) - Real.log (g x (y - h/2) t))) x y' t
          = B (y' + h/2) - B (y' - h/2) := by
      intro h y'
      have h2 : HasDerivAt (fun z => c02log g z (y' + h/2) t) (B (y' + h/2)) x :=
        hB_deriv (y' + h/2)
      have h3 : HasDerivAt (fun z => c02log g z (y' - h/2) t) (B (y' - h/2)) x :=
        hB_deriv (y' - h/2)
      exact (h2.sub h3).deriv
    have hIV : ∀ h : ℝ, interpV h f g x y t
        = (4/h) * (B (y+h/2) - B (y-h/2))
          + ((2*A (y+h) - B (y+h/2) - B (y+3*h/2))
             - (2*A (y-h) - B (y-3*h/2) - B (y-h/2)))/(2*h) := by
      intro h
      simp only [interpV, Pi.add_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul]
      rw [hBsy h y, hIU h (y+h), hIU h (y-h)]
      simp only [show (y+h) - h/2 = y+h/2 by ring,
        show (y+h) + h/2 = y+3*h/2 by ring,
        show (y-h) - h/2 = y-3*h/2 by ring,
        show (y-h) + h/2 = y-h/2 by ring]
    have hVerr : ∀ h : ℝ, h ≠ 0 → interpV h f g x y t - cv f g x y t
        = (7/2) * ((RB (h/2) - RB (-(h/2)))/h)
          - (3/2) * ((RB (3*h/2) - RB (-(3*h/2)))/(3*h))
          + 2 * ((RA h - RA (-h))/(2*h)) := by
      intro h hh
      rw [hIV h, hcv]
      dsimp only [RA, RB]
      simp only [sub_eq_add_neg]
      field_simp
      ring
    have hB1 : PowBound 2 (fun h : ℝ => (RB (h/2) - RB (-(h/2)))/h) :=
      c11_powBound_symm_diff (p := 2) hRB
    have hB3 : PowBound 2 (fun h : ℝ => (RB (3*h/2) - RB (-(3*h/2)))/(3*h)) :=
      c17_powBound_symm_3half (p := 2) hRB
    have hA1 : PowBound 2 (fun h : ℝ => (RA h - RA (-h))/(2*h)) :=
      c17_powBound_symm_dbl (p := 2) hRA
    have hT1 : PowBound 2 (fun h : ℝ =>
        (7/2) * ((RB (h/2) - RB (-(h/2)))/h)
          - (3/2) * ((RB (3*h/2) - RB (-(3*h/2)))/(3*h))) := by
      refine c11_powBound_add (c17_powBound_const_mul (7/2) hB1)
        (c17_powBound_neg (c17_powBound_const_mul (3/2) hB3)) (fun h => by ring)
    have hT2 : PowBound 2 (fun h : ℝ =>
        (7/2) * ((RB (h/2) - RB (-(h/2)))/h)
          - (3/2) * ((RB (3*h/2) - RB (-(3*h/2)))/(3*h))
          + 2 * ((RA h - RA (-h))/(2*h))) :=
      c11_powBound_add hT1 (c17_powBound_const_mul 2 hA1) (fun h => by ring)
    exact c11_powBound_congr_ne (fun h hh => (hVerr h hh).symm) hT2

end DLWContract
