/-
Report.html equations (1), (4), (7), (8): real differential proofs.

The omega below is the UNSCALED logarithmic derivative in Report (4).
Only the original bilinear equations are assumed by the final endpoint.
The frozen Contracts and the historical Main module are unchanged.
-/
import PkgNonlinear
import PkgLattice

noncomputable section
namespace DLWContract.ReportUW

/-- Report (4): omega = (log G[j+1] - log G[j])_x, without 4/h. -/
def omega (G : Lattice) : Lattice := lx (Sh (logL G) - logL G)

/-- Report (7), first nonlinear flux. -/
def fluxUW (a h : ℝ) (u w : Lattice) : Lattice :=
  (u ^ 2 + w ^ 2) / 2 + (2 * a) • u - h • w

/-- Report (7), second nonlinear flux. -/
def fluxOmega (a h : ℝ) (u w : Lattice) : Lattice :=
  (u + CC a) * w - h • u

/-- Report (7), first residual, with the displayed derivative order. -/
def reportN1 (a h : ℝ) (u w : Lattice) : Lattice :=
  dm h (lt u) + lx (dm h (fluxUW a h u w)) +
    lxx (dm h u + (4 / h) • mm w)

/-- Report (7), second residual. -/
def reportN2 (a h : ℝ) (u w : Lattice) : Lattice :=
  lt w + lx (fluxOmega a h u w) - lxx w

/-- Report (8)'s physical field reconstructed from unscaled omega. -/
def vFromOmega (h : ℝ) (u w : Lattice) : Lattice := (4 / h) • w + d0 h u

lemma smooth_logL (F : Lattice) (hF : SmoothL F) (hp : PositiveL F) :
    SmoothL (logL F) := by
  intro j
  exact (hF j).log (fun p => ne_of_gt (hp j p.1 p.2))

lemma smooth_omega (G : Lattice) (hG : SmoothL G) (hp : PositiveL G) :
    SmoothL (omega G) :=
  smL_lx (smL_sub (smL_Sh (smooth_logL G hG hp)) (smooth_logL G hG hp))

lemma smooth_physU (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) : SmoothL (physU F G) := by
  exact smL_lx (smL_sub
    (smL_sub (smL_mul (smL_const 2) (smooth_logL F hF hFp))
      (smooth_logL G hG hGp))
    (smL_Sh (smooth_logL G hG hGp)))

lemma smooth_fluxUW (a h : ℝ) {u w : Lattice} (hu : SmoothL u) (hw : SmoothL w) :
    SmoothL (fluxUW a h u w) :=
  smL_sub (smL_add (smL_div (smL_add (smL_pow hu 2) (smL_pow hw 2)) 2)
    (smL_smul (2 * a) hu)) (smL_smul h hw)

lemma smooth_fluxOmega (a h : ℝ) {u w : Lattice} (hu : SmoothL u) (hw : SmoothL w) :
    SmoothL (fluxOmega a h u w) :=
  smL_sub (smL_mul (smL_add hu (smL_const (2 * a))) hw) (smL_smul h hu)

lemma smooth_vFromOmega (h : ℝ) {u w : Lattice} (hu : SmoothL u) (hw : SmoothL w) :
    SmoothL (vFromOmega h u w) :=
  smL_add (smL_smul (4 / h) hw) (smL_d0 h hu)

/-- The physical reconstruction agrees exactly with Contracts.physV. -/
theorem physical_v (h : ℝ) (F G : Lattice) :
    physV h F G = vFromOmega h (physU F G) (omega G) := rfl

lemma W_vFromOmega (h : ℝ) (u w : Lattice) :
    W h u (vFromOmega h u w) = (4 / h) • w := by
  unfold W vFromOmega
  abel

lemma H_vFromOmega (a h : ℝ) (hh : h ≠ 0) (u w : Lattice) :
    H a h u (vFromOmega h u w) = fluxUW a h u w := by
  rw [H, W_vFromOmega]
  funext j x t
  simp only [fluxUW, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply,
    Pi.div_apply, Pi.ofNat_apply, Pi.smul_apply, smul_eq_mul]
  field_simp
  ring

lemma lx_dm_commute (h : ℝ) {z : Lattice} (hz : SmoothL z) :
    lx (dm h z) = dm h (lx z) := by
  have he : dm h z = (1 / h) • (z - Shb z) := rfl
  rw [he, lx_smul (1 / h) (smL_sub hz (smL_Shb hz)),
    lx_sub hz (smL_Shb hz), ← Shb_lx]
  rfl

/-- Exact finite-difference identity responsible for eliminating Z in Report (7). -/
lemma first_spatial_bridge (h : ℝ) (hh : h ≠ 0) (u w : Lattice) :
    mm (vFromOmega h u w) - (h ^ 2 / 4) • lap h (dm h u) =
      dm h u + (4 / h) • mm w := by
  funext j x t
  simp only [mm, vFromOmega, d0, dm, lap, Pi.add_apply, Pi.sub_apply,
    Pi.mul_apply, Pi.div_apply, Pi.smul_apply, Pi.ofNat_apply, smul_eq_mul]
  simp only [Int.add_sub_cancel, Int.sub_add_cancel]
  field_simp
  ring

/-- Report (7)'s first residual is precisely Report (8)'s first residual. -/
theorem reportN1_eq_n1 (a h : ℝ) (hh : h ≠ 0) {u w : Lattice}
    (hu : SmoothL u) (hw : SmoothL w) :
    reportN1 a h u w = n1 a h u (vFromOmega h u w) := by
  rw [reportN1, n1, H_vFromOmega a h hh u w,
    first_spatial_bridge h hh u w, dm_add, lx_dm_commute h (smooth_fluxUW a h hu hw)]

/-- The local W conservation law becomes the unscaled omega equation. -/
lemma omega_conservation_bridge (a h : ℝ) (hh : h ≠ 0) {u w : Lattice}
    (hu : SmoothL u) (hw : SmoothL w) :
    lt (W h u (vFromOmega h u w)) + lx (JW a h u (vFromOmega h u w)) =
      (4 / h) • reportN2 a h u w := by
  have hJW : JW a h u (vFromOmega h u w) =
      (4 / h) • (fluxOmega a h u w - lx w) := by
    rw [JW, W_vFromOmega, lx_smul (4 / h) hw]
    funext j x t
    simp only [fluxOmega, CC, Pi.add_apply, Pi.sub_apply, Pi.mul_apply,
      Pi.smul_apply, Pi.ofNat_apply, smul_eq_mul]
    field_simp
  rw [W_vFromOmega, hJW, lt_smul (4 / h) hw,
    lx_smul (4 / h) (smL_sub (smooth_fluxOmega a h hu hw) (smL_lx hw)),
    lx_sub (smooth_fluxOmega a h hu hw) (smL_lx hw)]
  funext j x t
  simp only [reportN2, lxx, Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
  ring

/-- Equation (1) implies BOTH displayed residual equations (7), with real derivatives. -/
theorem semiPair_implies_report7 (a h : ℝ) (F G : Lattice) (hh : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) :
    reportN1 a h (physU F G) (omega G) = 0 ∧
      reportN2 a h (physU F G) (omega G) = 0 := by
  have hu := smooth_physU F G hF hG hFp hGp
  have hw := smooth_omega G hG hGp
  have hv := smooth_vFromOmega h hu hw
  have hnp := c15_proved a h F G hh hF hG hFp hGp hsp
  rw [physical_v] at hnp
  constructor
  · rw [reportN1_eq_n1 a h hh hu hw]
    exact hnp.1
  · have hcons := (c19_proved a h (physU F G)
      (vFromOmega h (physU F G) (omega G)) hh hu hv hnp).1
    rw [omega_conservation_bridge a h hh hu hw] at hcons
    funext j x t
    have hp := congrFun (congrFun (congrFun hcons j) x) t
    simp only [Pi.smul_apply, Pi.zero_apply, smul_eq_mul] at hp
    exact (mul_eq_zero.mp hp).resolve_left (div_ne_zero (by norm_num) hh)

/-- Equation (1) also gives the physical u/v equations displayed as (8). -/
theorem semiPair_implies_report8 (a h : ℝ) (F G : Lattice) (hh : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) :
    NonlinearPair a h (physU F G) (vFromOmega h (physU F G) (omega G)) := by
  rw [← physical_v]
  exact c15_proved a h F G hh hF hG hFp hGp hsp

#print axioms physical_v
#print axioms first_spatial_bridge
#print axioms reportN1_eq_n1
#print axioms omega_conservation_bridge
#print axioms semiPair_implies_report7
#print axioms semiPair_implies_report8

end DLWContract.ReportUW
