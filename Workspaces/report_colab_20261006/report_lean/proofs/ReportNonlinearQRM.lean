/- Forward formalization of Report (1) -> (21), (22).
The exponential Q and quotient R below are actual smooth functions.
-/
import ReportQRMCalculus
import ReportNonlinearUW

noncomputable section
namespace DLWContract.ReportQRM
open DLWContract

def potential (F G : Lattice) : Lattice :=
  logL F - (1/2 : ℝ) • (logL G + Sh (logL G))
def Q (F G : Lattice) : Lattice := expL (potential F G)
def M (G : Lattice) : Lattice := lx (logL G)
def omega (G : Lattice) : Lattice := lx (Sh (logL G) - logL G)
def R (h : ℝ) (F G : Lattice) : Lattice :=
  fun j x t => (1 - omega G j x t / h) / Q F G j x t
def coefficient (a h : ℝ) (F G : Lattice) : Lattice :=
  lx (M G + Sh (M G)) + (h^2/4) • ((Q F G)^2 * (R h F G)^2 - 1)
def residualQ (a h : ℝ) (F G : Lattice) : Lattice :=
  lt (Q F G) + lxx (Q F G) + (2*a) • lx (Q F G) + coefficient a h F G * Q F G
def residualR (a h : ℝ) (F G : Lattice) : Lattice :=
  lt (R h F G) - lxx (R h F G) + (2*a) • lx (R h F G) - coefficient a h F G * R h F G

lemma smooth_potential (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) : SmoothL (potential F G) :=
  smL_sub (smooth_log F hF hFp) (smL_smul (1/2)
    (smL_add (smooth_log G hG hGp) (smL_Sh (smooth_log G hG hGp))))

lemma smooth_Q (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) : SmoothL (Q F G) :=
  smooth_exp (smooth_potential F G hF hG hFp hGp)

lemma Q_positive (F G : Lattice) : PositiveL (Q F G) := fun j x t => Real.exp_pos _

lemma Q_ne (F G : Lattice) (j : ℤ) (x t : ℝ) : Q F G j x t ≠ 0 := Real.exp_ne_zero _

lemma smooth_omega (G : Lattice) (hG : SmoothL G) (hGp : PositiveL G) :
    SmoothL (omega G) :=
  smL_lx (smL_sub (smL_Sh (smooth_log G hG hGp)) (smooth_log G hG hGp))

lemma smooth_R (h : ℝ) (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) : SmoothL (R h F G) := by
  intro j
  exact (contDiff_const.sub ((smooth_omega G hG hGp j).div_const h)).div
    (smooth_Q F G hF hG hFp hGp j) (fun p => Q_ne F G j p.1 p.2)

lemma QR_identity (h : ℝ) (F G : Lattice) :
    Q F G * R h F G = 1 - (1/h) • omega G := by
  funext j x t
  simp only [Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, Pi.one_apply, smul_eq_mul, R]
  field_simp [Q_ne F G j x t]

lemma omega_M (G : Lattice) (hG : SmoothL G) (hGp : PositiveL G) :
    omega G = Sh (M G) - M G := by
  rw [omega, DLWContract.lx_sub (smL_Sh (smooth_log G hG hGp)) (smooth_log G hG hGp)]
  rfl

lemma physical_u (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) :
    physU F G = (2 : ℝ) • lx (potential F G) := by
  have hf := smooth_log F hF hFp
  have hg := smooth_log G hG hGp
  have hs := smL_Sh hg
  have hu : 2 * logL F - logL G - Sh (logL G) = (2 : ℝ) • potential F G := by
    funext j x t
    simp only [potential, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.smul_apply,
      Pi.ofNat_apply, smul_eq_mul]
    ring
  change lx (2 * logL F - logL G - Sh (logL G)) = _
  rw [hu, DLWContract.lx_smul 2 (smooth_potential F G hF hG hFp hGp)]

lemma coefficient_omega (a h : ℝ) (F G : Lattice) (hne : h ≠ 0) :
    coefficient a h F G = lx (M G + Sh (M G)) +
      (1/4 : ℝ) • (omega G)^2 - (h/2) • omega G := by
  have hp := QR_identity h F G
  funext j x t
  have hprod := congrFun (congrFun (congrFun hp j) x) t
  simp only [Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, Pi.one_apply, smul_eq_mul] at hprod
  simp only [coefficient, Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply,
    Pi.smul_apply, Pi.one_apply, smul_eq_mul]
  rw [show (Q F G j x t)^2 * (R h F G j x t)^2 =
    (Q F G j x t * R h F G j x t)^2 by ring, hprod]
  field_simp
  <;> ring

lemma Q_residual_identity (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G) :
    residualQ a h F G = (1/2 : ℝ) • (Q F G * (normA a h F G + normC a h F G)) := by
  have hf := smooth_log F hF hFp
  have hg := smooth_log G hG hGp
  have hs := smL_Sh hg
  have hp := smooth_potential F G hF hG hFp hGp
  have hd : lx (potential F G) = lx (logL F) - (1/2 : ℝ) •
      (lx (logL G) + lx (Sh (logL G))) := by
    rw [potential, DLWContract.lx_sub hf (smL_smul (1/2) (smL_add hg hs)),
      DLWContract.lx_smul (1/2) (smL_add hg hs), DLWContract.lx_add hg hs]
  have ht : lt (potential F G) = lt (logL F) - (1/2 : ℝ) •
      (lt (logL G) + lt (Sh (logL G))) := by
    rw [potential, DLWContract.lt_sub hf (smL_smul (1/2) (smL_add hg hs)),
      DLWContract.lt_smul (1/2) (smL_add hg hs), DLWContract.lt_add hg hs]
  have hxx : lxx (potential F G) = lxx (logL F) - (1/2 : ℝ) •
      (lxx (logL G) + lxx (Sh (logL G))) := by
    rw [potential, DLWContract.lxx_sub hf (smL_smul (1/2) (smL_add hg hs)),
      DLWContract.lxx_smul (1/2) (smL_add hg hs), DLWContract.lxx_add hg hs]
  have hw : omega G = lx (Sh (logL G)) - lx (logL G) :=
    DLWContract.lx_sub hs hg
  have hm : lx (M G + Sh (M G)) = lxx (logL G) + lxx (Sh (logL G)) := by
    change lx (lx (logL G) + Sh (lx (logL G))) = _
    rw [DLWContract.lx_add (smL_lx hg) (smL_Sh (smL_lx hg))]
    rfl
  rw [residualQ, coefficient_omega a h F G hne]
  change lt (expL (potential F G)) + lxx (expL (potential F G)) +
    (2*a) • lx (expL (potential F G)) +
    (lx (M G + Sh (M G)) + (1/4 : ℝ) • (omega G)^2 - (h/2) • omega G) * Q F G = _
  rw [lt_exp hp, lxx_exp hp, lx_exp hp, hd, ht, hxx, hw, hm]
  funext j x t
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply, Pi.smul_apply, smul_eq_mul]
  rw [normA_log a h F G hF hG hFp hGp j, normC_log a h F G hF hG hFp hGp j]
  rw [show xx (logL F j + logL G j) = xx (logL F j) + xx (logL G j) by
    exact congrFun (DLWContract.lxx_add hf hg) j,
    show xx (logL F j + logL G (j+1)) = xx (logL F j) + xx (logL G (j+1)) by
    exact congrFun (DLWContract.lxx_add hf hs) j,
    dx_sub (hf j) (hg j), dx_sub (hf j) (hg (j+1)),
    dt_sub (hf j) (hg j), dt_sub (hf j) (hg (j+1))]
  simp only [Pi.add_apply, Pi.sub_apply, Pi.mul_apply, Pi.pow_apply, Pi.smul_apply,
    smul_eq_mul, Sh, lx, lt, lxx, xx, Q]
  ring

theorem report_Q_equation (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) : residualQ a h F G = 0 := by
  rw [Q_residual_identity a h F G hne hF hG hFp hGp,
    normA_zero a h F G hsp, normC_zero a h F G hsp, add_zero, mul_zero, smul_zero]

lemma u_reconstruction (F G : Lattice) (hF : SmoothL F) (hG : SmoothL G)
    (hFp : PositiveL F) (hGp : PositiveL G) (j : ℤ) (x t : ℝ) :
    physU F G j x t = 2 * lx (Q F G) j x t / Q F G j x t := by
  rw [physical_u F G hF hG hFp hGp]
  have hd := congrFun (congrFun (congrFun
    (lx_exp (smooth_potential F G hF hG hFp hGp)) j) x) t
  change lx (Q F G) j x t = Q F G j x t * lx (potential F G) j x t at hd
  simp only [Pi.smul_apply, smul_eq_mul]
  rw [hd]
  field_simp [Q_ne F G j x t]

lemma lattice_constraint (h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hG : SmoothL G) (hGp : PositiveL G) (j : ℤ) (x t : ℝ) :
    (M G (j+1) x t - M G j x t)/h + Q F G j x t * R h F G j x t = 1 := by
  have hp := congrFun (congrFun (congrFun (QR_identity h F G) j) x) t
  have hw := congrFun (congrFun (congrFun (omega_M G hG hGp) j) x) t
  simp only [Sh, Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, Pi.one_apply, smul_eq_mul] at hp hw
  rw [hp, hw]
  field_simp
  <;> ring

lemma omega_reconstruction (h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (j : ℤ) (x t : ℝ) :
    omega G j x t = h * (1 - Q F G j x t * R h F G j x t) := by
  have hp := congrFun (congrFun (congrFun (QR_identity h F G) j) x) t
  simp only [Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, Pi.one_apply, smul_eq_mul] at hp
  rw [hp]
  field_simp
  <;> ring

lemma v_reconstruction (h : ℝ) (F G : Lattice) (hne : h ≠ 0) (j : ℤ) (x t : ℝ) :
    physV h F G j x t = 4 * (1-Q F G j x t*R h F G j x t) +
      (physU F G (j+1) x t-physU F G (j-1) x t)/(2*h) := by
  change (4/h)*omega G j x t + (1/(2*h))*
    (physU F G (j+1) x t-physU F G (j-1) x t) = _
  rw [omega_reconstruction h F G hne]
  field_simp
  <;> ring

def residualProduct (a h : ℝ) (F G : Lattice) : Lattice :=
  lt (Q F G * R h F G) - lxx (Q F G * R h F G) +
    (2*a) • lx (Q F G * R h F G) + (2 : ℝ) • lx (lx (Q F G) * R h F G)

lemma product_residual_split (a h : ℝ) (F G : Lattice)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G) :
    residualProduct a h F G = R h F G * residualQ a h F G + Q F G * residualR a h F G := by
  have hq := smooth_Q F G hF hG hFp hGp
  have hr := smooth_R h F G hF hG hFp hGp
  rw [residualProduct, lt_mul hq hr, lxx_mul hq hr, lx_mul hq hr,
    lx_mul (smL_lx hq) hr]
  funext j x t
  simp only [residualQ, residualR, Pi.add_apply, Pi.sub_apply, Pi.mul_apply,
    Pi.smul_apply, smul_eq_mul, lxx]
  ring

lemma product_residual_omega (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G) :
    residualProduct a h F G = (-1/h) •
      ReportUW.reportN2 a h (physU F G) (ReportUW.omega G) := by
  have hu := ReportUW.smooth_physU F G hF hG hFp hGp
  have hw := smooth_omega G hG hGp
  have hf := smL_mul hu hw
  have hqr : Q F G * R h F G = (fun _ _ _ => 1) - (1/h) • omega G := QR_identity h F G
  have hux : (2 : ℝ) • (lx (Q F G) * R h F G) =
      physU F G * (Q F G * R h F G) := by
    rw [physical_u F G hF hG hFp hGp]
    change (2 : ℝ) • (lx (expL (potential F G)) * R h F G) = _
    rw [lx_exp (smooth_potential F G hF hG hFp hGp)]
    funext j x t
    simp only [Q, Pi.mul_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have hux' : (2 : ℝ) • lx (lx (Q F G) * R h F G) =
      lx (physU F G - (1/h) • (physU F G * omega G)) := by
    have hq := smooth_Q F G hF hG hFp hGp
    have hr := smooth_R h F G hF hG hFp hGp
    rw [← DLWContract.lx_smul 2 (smL_mul (smL_lx hq) hr), hux, hqr]
    congr 1
    funext j x t
    simp only [Pi.mul_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have hflux : ReportUW.fluxOmega a h (physU F G) (ReportUW.omega G) =
      physU F G * omega G + (2*a) • omega G - h • physU F G := by
    funext j x t
    simp only [ReportUW.fluxOmega, ReportUW.omega, omega, CC, Pi.mul_apply,
      Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]
    ring
  have hlxxc : lxx (fun _ _ _ => (1 : ℝ)) = 0 := by
    change lx (lx (fun _ _ _ => (1 : ℝ))) = 0
    rw [lx_const, lx_zero]
  rw [residualProduct, hux', hqr,
    DLWContract.lt_sub (smL_const 1) (smL_smul (1/h) hw),
    DLWContract.lt_smul (1/h) hw, lt_const,
    DLWContract.lxx_sub (smL_const 1) (smL_smul (1/h) hw),
    DLWContract.lxx_smul (1/h) hw, hlxxc,
    DLWContract.lx_sub (smL_const 1) (smL_smul (1/h) hw),
    DLWContract.lx_smul (1/h) hw, lx_const,
    DLWContract.lx_sub hu (smL_smul (1/h) hf), DLWContract.lx_smul (1/h) hf]
  rw [ReportUW.reportN2, hflux,
    DLWContract.lx_sub (smL_add hf (smL_smul (2*a) hw)) (smL_smul h hu),
    DLWContract.lx_add hf (smL_smul (2*a) hw),
    DLWContract.lx_smul (2*a) hw, DLWContract.lx_smul h hu]
  funext j x t
  simp only [ReportUW.omega, omega, Pi.add_apply, Pi.sub_apply, Pi.mul_apply,
    Pi.zero_apply, Pi.smul_apply, smul_eq_mul]
  field_simp
  ring

theorem report_R_equation (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) : residualR a h F G = 0 := by
  have hp : residualProduct a h F G = 0 := by
    rw [product_residual_omega a h F G hne hF hG hFp hGp,
      (ReportUW.semiPair_implies_report7 a h F G hne hF hG hFp hGp hsp).2, smul_zero]
  rw [product_residual_split a h F G hF hG hFp hGp,
    report_Q_equation a h F G hne hF hG hFp hGp hsp, mul_zero, zero_add] at hp
  funext j x t
  have hv := congrFun (congrFun (congrFun hp j) x) t
  simp only [Pi.mul_apply, Pi.zero_apply] at hv
  exact (mul_eq_zero.mp hv).resolve_left (Q_ne F G j x t)

/-- Both heat-type equations and the lattice constraint of Report (21). -/
theorem semiPair_implies_report21 (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) :
    residualQ a h F G = 0 ∧ residualR a h F G = 0 ∧
      ∀ j x t, (M G (j+1) x t-M G j x t)/h + Q F G j x t*R h F G j x t = 1 :=
  ⟨report_Q_equation a h F G hne hF hG hFp hGp hsp,
    report_R_equation a h F G hne hF hG hFp hGp hsp,
    lattice_constraint h F G hne hG hGp⟩

/-- All physical reconstruction identities displayed in Report (22). -/
theorem report22 (h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G) :
    ∀ j x t,
      physU F G j x t = 2 * lx (Q F G) j x t / Q F G j x t ∧
      omega G j x t = h*(1-Q F G j x t*R h F G j x t) ∧
      omega G j x t = M G (j+1) x t-M G j x t ∧
      physV h F G j x t = 4*(1-Q F G j x t*R h F G j x t) +
        (physU F G (j+1) x t-physU F G (j-1) x t)/(2*h) := by
  intro j x t
  refine ⟨u_reconstruction F G hF hG hFp hGp j x t,
    omega_reconstruction h F G hne j x t, ?_, v_reconstruction h F G hne j x t⟩
  exact congrFun (congrFun (congrFun (omega_M G hG hGp) j) x) t

#print axioms Q_residual_identity
#print axioms product_residual_split
#print axioms semiPair_implies_report21
#print axioms report22

end DLWContract.ReportQRM
