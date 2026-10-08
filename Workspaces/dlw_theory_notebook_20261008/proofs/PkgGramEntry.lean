/-
Package: Gram-matrix entry targets.

Targets C04, C05, C06, C10 of `Contracts.lean`.

All four concern the explicit Gram entry
`entry D h s n j i k = δ_{ik} + ρ_i/(p_i+q_k) · γ_{ik}(s)^n · χ_{ik}(h)^j · exp(…)`
of the contract file; nothing beyond `Contracts.lean` is assumed.
-/
import Contracts
import Mathlib.Analysis.SpecialFunctions.Exponential
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

/-! ## Auxiliary definitions -/

/-- The `δ`-free part of a Gram entry. -/
private def corr {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (i k : Fin N) : XT :=
  fun x t => D.rho i/(D.p i+D.q k)*(gamma D s i k)^n*(chi D h i k)^j*
    Real.exp ((D.p i+D.q k)*x+((D.q k)^2-(D.p i)^2)*t)

/-! ## Auxiliary calculus lemmas -/

private lemma hasDerivAt_exp_affine (A B x : ℝ) :
    HasDerivAt (fun z : ℝ => Real.exp (A * z + B)) (Real.exp (A * x + B) * A) x := by
  have h1 : HasDerivAt (fun z : ℝ => A * z + B) A x := by
    simpa using ((hasDerivAt_id x).const_mul A).add_const B
  simpa using h1.exp

/-- Derivative at `x` of `z ↦ c + K · exp (A z + B)`. -/
private lemma deriv_const_add_mul_exp (c K A B x : ℝ) :
    deriv (fun z : ℝ => c + K * Real.exp (A * z + B)) x =
      K * (A * Real.exp (A * x + B)) := by
  have h1 : HasDerivAt (fun z : ℝ => K * Real.exp (A * z + B))
      (K * (Real.exp (A * x + B) * A)) x :=
    (hasDerivAt_exp_affine A B x).const_mul K
  have h2 : HasDerivAt (fun z : ℝ => c + K * Real.exp (A * z + B))
      (0 + K * (Real.exp (A * x + B) * A)) x :=
    (hasDerivAt_const x c).add h1
  rw [h2.deriv]
  ring

/-- Same, with the affine argument written the other way round. -/
private lemma deriv_const_add_mul_exp_comm (c K A B x : ℝ) :
    deriv (fun z : ℝ => c + K * Real.exp (B + A * z)) x =
      K * (A * Real.exp (B + A * x)) := by
  have hfun : (fun z : ℝ => c + K * Real.exp (B + A * z)) =
      (fun z : ℝ => c + K * Real.exp (A * z + B)) := by
    funext z
    rw [add_comm B (A * z)]
  rw [hfun, deriv_const_add_mul_exp c K A B x, add_comm (A * x) B]

/-! ## C04 — the exact `gamma`/`chi` shift identity -/

private lemma gamma_shift {N : ℕ} (D : Data N) (h : ℝ) (i k : Fin N)
    (hAdm : Admissible D h) :
    gamma D (D.a - h/2) i k = gamma D (D.a + h/2) i k * chi D h i k := by
  have h1 : D.p i - D.a - h/2 ≠ 0 := (hAdm.2.2.1 i).1
  have h3 : D.q k + D.a - h/2 ≠ 0 := (hAdm.2.2.2 k).1
  have h5 : D.q k + (D.a - h/2) ≠ 0 := by
    intro hh
    exact (hAdm.2.2.2 k).1 (by linarith)
  have h6 : D.q k + (D.a + h/2) ≠ 0 := by
    intro hh
    exact (hAdm.2.2.2 k).2 (by linarith)
  simp only [gamma, chi, lam]
  rw [div_mul_div_comm, div_mul_div_comm]
  rw [div_eq_div_iff h5 (mul_ne_zero h6 (mul_ne_zero h1 h3))]
  ring

theorem c04_proved : C04 := by
  intro N D h hAdm n j i k
  have hkey : gamma D (D.a - h/2) i k = gamma D (D.a + h/2) i k * chi D h i k :=
    gamma_shift D h i k hAdm
  have hchi : chi D h i k ≠ 0 := by
    simp only [chi, lam]
    refine mul_ne_zero (div_ne_zero ?_ ?_) (div_ne_zero ?_ ?_)
    · exact (hAdm.2.2.1 i).2
    · exact (hAdm.2.2.1 i).1
    · exact (hAdm.2.2.2 k).2
    · exact (hAdm.2.2.2 k).1
  have hstep : (gamma D (D.a - h/2) i k)^n * (chi D h i k)^j
      = (gamma D (D.a + h/2) i k)^n * (chi D h i k)^(j+n) := by
    rw [hkey, mul_zpow, mul_assoc, ← zpow_add₀ hchi n j, add_comm n j]
  funext x t
  simp only [entry]
  have htwo : (D.rho i/(D.p i + D.q k) * (gamma D (D.a - h/2) i k)^n) * (chi D h i k)^j
      = (D.rho i/(D.p i + D.q k) * (gamma D (D.a + h/2) i k)^n) * (chi D h i k)^(j+n) := by
    simp only [mul_assoc]
    rw [hstep]
  rw [htwo]

/-! ## C05 — the determinant inherits the shift -/

theorem c05_proved : C05 := by
  intro N D h hAdm n j
  funext x t
  simp only [tau]
  have hmat : (fun i k : Fin N => entry D h (D.a - h/2) n j i k x t)
      = (fun i k : Fin N => entry D h (D.a + h/2) n (j+n) i k x t) := by
    funext i k
    exact congrFun (congrFun (c04_proved N D h hAdm n j i k) x) t
  rw [hmat]

/-! ## C06 — derivatives and the layer recursion -/

theorem c06_proved : C06 := by
  intro N D h s hAdm hLayer n j i k
  dsimp only
  refine ⟨?_, ?_, ?_⟩
  · funext x t
    by_cases hik : i = k
    · simp only [dx, entry, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, if_pos hik]
      rw [deriv_const_add_mul_exp]
      ring
    · simp only [dx, entry, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, if_neg hik]
      rw [deriv_const_add_mul_exp]
      ring
  · funext x t
    show deriv (fun z : ℝ => (if i = k then (1 : ℝ) else 0) +
        D.rho i / (D.p i + D.q k) * (gamma D s i k) ^ n * (chi D h i k) ^ j *
          Real.exp ((D.p i + D.q k) * x + ((D.q k) ^ 2 - (D.p i) ^ 2) * z)) t =
      ((D.q k) ^ 2 - (D.p i) ^ 2) * ((if i = k then (1 : ℝ) else 0) +
        D.rho i / (D.p i + D.q k) * (gamma D s i k) ^ n * (chi D h i k) ^ j *
          Real.exp ((D.p i + D.q k) * x + ((D.q k) ^ 2 - (D.p i) ^ 2) * t) -
        (if i = k then (1 : ℝ) else 0))
    rw [deriv_const_add_mul_exp_comm]
    ring
  · have hq : D.q k + s ≠ 0 := hLayer.2 k
    have hγne : gamma D s i k ≠ 0 := by
      simp only [gamma]
      exact div_ne_zero (fun hh => hLayer.1 i (neg_eq_zero.mp hh)) hq
    have hγ : gamma D s i k = 1 - (D.p i + D.q k)/(D.q k + s) := by
      simp only [gamma]
      field_simp
      ring
    have hpow : (gamma D s i k)^(n+1) = (gamma D s i k)^n * gamma D s i k :=
      zpow_add_one₀ hγne n
    funext x t
    by_cases hik : i = k
    · simp only [entry, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, if_pos hik]
      rw [hpow, hγ]
      ring
    · simp only [entry, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, if_neg hik]
      rw [hpow, hγ]
      ring

/-! ## C10 — the `N = 2` determinant expansion -/

/-- Generic two-by-two cancellation behind C10. -/
private lemma cross_identity
    (ρ01 ρ10 ρ00 ρ11 g01 g10 g00 g11 x01 x10 x00 x11 E01 E10 E00 E11 κ : ℝ)
    (hE : E01 * E10 = E00 * E11) (n j : ℤ)
    (hG : g01 * g10 = g00 * g11) (hX : x01 * x10 = x00 * x11)
    (hκ : ρ01 * ρ10 = (1 - κ) * ρ00 * ρ11) :
    (ρ01 * g01 ^ n * x01 ^ j * E01) * (ρ10 * g10 ^ n * x10 ^ j * E10) =
      ((1 - κ) * (ρ00 * g00 ^ n * x00 ^ j * E00)) * (ρ11 * g11 ^ n * x11 ^ j * E11) := by
  have hgn : g01 ^ n * g10 ^ n = g00 ^ n * g11 ^ n := by
    rw [← Commute.mul_zpow (Commute.all g01 g10) n, hG,
      Commute.mul_zpow (Commute.all g00 g11) n]
  have hxn : x01 ^ j * x10 ^ j = x00 ^ j * x11 ^ j := by
    rw [← Commute.mul_zpow (Commute.all x01 x10) j, hX,
      Commute.mul_zpow (Commute.all x00 x11) j]
  calc (ρ01 * g01 ^ n * x01 ^ j * E01) * (ρ10 * g10 ^ n * x10 ^ j * E10)
      = ρ01 * ρ10 * (g01 ^ n * g10 ^ n) * (x01 ^ j * x10 ^ j) * (E01 * E10) := by
        ac_rfl
    _ = ρ01 * ρ10 * (g00 ^ n * g11 ^ n) * (x00 ^ j * x11 ^ j) * (E00 * E11) := by
        rw [hgn, hxn, hE]
    _ = (1 - κ) * ρ00 * ρ11 * (g00 ^ n * g11 ^ n) * (x00 ^ j * x11 ^ j) * (E00 * E11) := by
        rw [hκ]
    _ = ((1 - κ) * (ρ00 * g00 ^ n * x00 ^ j * E00)) * (ρ11 * g11 ^ n * x11 ^ j * E11) := by
        ac_rfl

/-- The `N = 2` determinant written out entrywise. -/
private lemma tau_two (D : Data 2) (h s : ℝ) (n j : ℤ) (x t : ℝ) :
    tau D h s n j x t = entry D h s n j 0 0 x t * entry D h s n j 1 1 x t
      - entry D h s n j 0 1 x t * entry D h s n j 1 0 x t := by
  have hdet := Matrix.det_fin_two (fun i k : Fin 2 => entry D h s n j i k x t)
  have h1 : tau D h s n j x t =
      Matrix.det (fun i k : Fin 2 => entry D h s n j i k x t) := rfl
  rw [h1]
  exact hdet.trans (by rfl)

theorem c10_proved : C10 := by
  intro D h s hAdm hLayer n j x t
  dsimp only
  rw [tau_two]
  have e00 : entry D h s n j 0 0 x t = 1 + corr D h s n j 0 0 x t := by
    simp [entry, corr]
  have e01 : entry D h s n j 0 1 x t = corr D h s n j 0 1 x t := by
    simp [entry, corr]
  have e10 : entry D h s n j 1 0 x t = corr D h s n j 1 0 x t := by
    simp [entry, corr]
  have e11 : entry D h s n j 1 1 x t = 1 + corr D h s n j 1 1 x t := by
    simp [entry, corr]
  simp only [e00, e01, e10, e11]
  set c00 := corr D h s n j 0 0 x t with hc00
  set c01 := corr D h s n j 0 1 x t with hc01
  set c10 := corr D h s n j 1 0 x t with hc10
  set c11 := corr D h s n j 1 1 x t with hc11
  set κ := interaction (D.p 0) (D.p 1) (D.q 0) (D.q 1) with hκdef
  have hp01 : D.p 0 + D.q 1 ≠ 0 := hAdm.2.1 0 1
  have hp10 : D.p 1 + D.q 0 ≠ 0 := hAdm.2.1 1 0
  have hp00 : D.p 0 + D.q 0 ≠ 0 := hAdm.2.1 0 0
  have hp11 : D.p 1 + D.q 1 ≠ 0 := hAdm.2.1 1 1
  have hG : gamma D s 0 1 * gamma D s 1 0 = gamma D s 0 0 * gamma D s 1 1 := by
    simp only [gamma]
    ring
  have hX : chi D h 0 1 * chi D h 1 0 = chi D h 0 0 * chi D h 1 1 := by
    simp only [chi]
    ring
  have hE :
      Real.exp ((D.p 0 + D.q 1)*x + ((D.q 1)^2 - (D.p 0)^2)*t) *
        Real.exp ((D.p 1 + D.q 0)*x + ((D.q 0)^2 - (D.p 1)^2)*t) =
      Real.exp ((D.p 0 + D.q 0)*x + ((D.q 0)^2 - (D.p 0)^2)*t) *
        Real.exp ((D.p 1 + D.q 1)*x + ((D.q 1)^2 - (D.p 1)^2)*t) := by
    simp only [← Real.exp_add]
    congr 1
    ring
  have hκrel : D.rho 0/(D.p 0 + D.q 1) * (D.rho 1/(D.p 1 + D.q 0)) =
      (1 - interaction (D.p 0) (D.p 1) (D.q 0) (D.q 1)) *
        (D.rho 0/(D.p 0 + D.q 0)) * (D.rho 1/(D.p 1 + D.q 1)) := by
    simp only [interaction]
    field_simp
    ring
  have hkey : c01 * c10 = (1 - κ) * c00 * c11 := by
    rw [hc01, hc10, hc00, hc11, hκdef]
    simp only [corr]
    exact (cross_identity
      (D.rho 0/(D.p 0 + D.q 1)) (D.rho 1/(D.p 1 + D.q 0))
      (D.rho 0/(D.p 0 + D.q 0)) (D.rho 1/(D.p 1 + D.q 1))
      (gamma D s 0 1) (gamma D s 1 0) (gamma D s 0 0) (gamma D s 1 1)
      (chi D h 0 1) (chi D h 1 0) (chi D h 0 0) (chi D h 1 1)
      (Real.exp ((D.p 0 + D.q 1)*x + ((D.q 1)^2 - (D.p 0)^2)*t))
      (Real.exp ((D.p 1 + D.q 0)*x + ((D.q 0)^2 - (D.p 1)^2)*t))
      (Real.exp ((D.p 0 + D.q 0)*x + ((D.q 0)^2 - (D.p 0)^2)*t))
      (Real.exp ((D.p 1 + D.q 1)*x + ((D.q 1)^2 - (D.p 1)^2)*t))
      (interaction (D.p 0) (D.p 1) (D.q 0) (D.q 1))
      hE n j hG hX hκrel).trans (by ring)
  rw [hkey]
  ring

end DLWContract
