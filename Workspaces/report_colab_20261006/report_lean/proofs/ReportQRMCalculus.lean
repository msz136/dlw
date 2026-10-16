/- Real derivative helpers for the Report (21) proof; no frozen target is changed. -/
import PkgLattice
import PkgQuotientRate
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic

noncomputable section
namespace DLWContract.ReportQRM
open DLWContract

def expL (p : Lattice) : Lattice := fun j x t => Real.exp (p j x t)

lemma smooth_log (F : Lattice) (hF : SmoothL F) (hFp : PositiveL F) :
    SmoothL (logL F) := by
  intro j
  exact (hF j).log (fun p => ne_of_gt (hFp j p.1 p.2))

lemma smooth_exp {p : Lattice} (hp : SmoothL p) : SmoothL (expL p) := by
  intro j
  exact (hp j).exp

lemma exp_ne (p : Lattice) (j : ℤ) (x t : ℝ) : expL p j x t ≠ 0 :=
  Real.exp_ne_zero _

lemma lx_exp {p : Lattice} (hp : SmoothL p) : lx (expL p) = expL p * lx p := by
  funext j x t
  exact ((sm_diffAt_x (hp j) x t).hasDerivAt.exp).deriv

lemma lt_exp {p : Lattice} (hp : SmoothL p) : lt (expL p) = expL p * lt p := by
  funext j x t
  exact ((sm_diffAt_t (hp j) x t).hasDerivAt.exp).deriv

lemma lx_mul {z w : Lattice} (hz : SmoothL z) (hw : SmoothL w) :
    lx (z * w) = lx z * w + z * lx w := by
  funext j x t
  exact ((sm_diffAt_x (hz j) x t).hasDerivAt.mul
    (sm_diffAt_x (hw j) x t).hasDerivAt).deriv

lemma lt_mul {z w : Lattice} (hz : SmoothL z) (hw : SmoothL w) :
    lt (z * w) = lt z * w + z * lt w := by
  funext j x t
  exact ((sm_diffAt_t (hz j) x t).hasDerivAt.mul
    (sm_diffAt_t (hw j) x t).hasDerivAt).deriv

lemma lxx_mul {z w : Lattice} (hz : SmoothL z) (hw : SmoothL w) :
    lxx (z * w) = lxx z * w + (2 : ℝ) • (lx z * lx w) + z * lxx w := by
  change lx (lx (z * w)) = _
  rw [lx_mul hz hw, DLWContract.lx_add
    (smL_mul (smL_lx hz) hw) (smL_mul hz (smL_lx hw)),
    lx_mul (smL_lx hz) hw, lx_mul hz (smL_lx hw)]
  funext j x t
  simp only [Pi.add_apply, Pi.mul_apply, Pi.smul_apply, smul_eq_mul, lxx]
  ring

lemma lxx_exp {p : Lattice} (hp : SmoothL p) :
    lxx (expL p) = expL p * ((lx p)^2 + lxx p) := by
  change lx (lx (expL p)) = _
  rw [lx_exp hp, lx_mul (smooth_exp hp) (smL_lx hp), lx_exp hp]
  funext j x t
  simp only [Pi.add_apply, Pi.mul_apply, Pi.pow_apply, lxx]
  ring

lemma lx_zero : lx (0 : Lattice) = 0 := by
  funext j x t
  simp [lx, dx]

lemma lt_zero : lt (0 : Lattice) = 0 := by
  funext j x t
  simp [lt, dt]

lemma lx_const (c : ℝ) : lx (fun _ _ _ => c) = 0 := by
  funext j x t
  simp [lx, dx]

lemma lt_const (c : ℝ) : lt (fun _ _ _ => c) = 0 := by
  funext j x t
  simp [lt, dt]

lemma normA_log (a h : ℝ) (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) (j : ℤ) :
    normA a h F G j = xx (logL F j + logL G j) +
      (dx (logL F j - logL G j))^2 + dt (logL F j - logL G j) +
      (2*(a-h/2)) • dx (logL F j-logL G j) :=
  c13_proved (a-h/2) (F j) (G j) (hF j) (hG j)
    (fun x t => ⟨hFp j x t, hGp j x t⟩)

lemma normC_log (a h : ℝ) (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) (j : ℤ) :
    normC a h F G j = xx (logL F j + logL G (j+1)) +
      (dx (logL F j - logL G (j+1)))^2 + dt (logL F j - logL G (j+1)) +
      (2*(a+h/2)) • dx (logL F j-logL G (j+1)) :=
  c13_proved (a+h/2) (F j) (G (j+1)) (hF j) (hG (j+1))
    (fun x t => ⟨hFp j x t, hGp (j+1) x t⟩)

lemma normA_zero (a h : ℝ) (F G : Lattice) (hsp : SemiPair a h F G) :
    normA a h F G = 0 := by
  funext j x t
  change (bil (a-h/2) (F j) (G j) / (F j * G j)) x t = 0
  rw [(hsp j).1]
  simp

lemma normC_zero (a h : ℝ) (F G : Lattice) (hsp : SemiPair a h F G) :
    normC a h F G = 0 := by
  funext j x t
  change (bil (a+h/2) (F j) (G (j+1)) / (F j * G (j+1))) x t = 0
  rw [(hsp j).2]
  simp

end DLWContract.ReportQRM
