import ReportNonlinearUW
import ReportNonlinearQRM
import ReportQRatio

/-!
One common entry point for the two forward nonlinearizations in Report.html.
Report (7) is the u/omega system. Report (21) is the Q/R/M system;
Report (22) reconstructs the same physical fields.
All derivatives are the actual real derivatives fixed by Contracts.
-/

noncomputable section
namespace DLWContract.ReportEndpoints

/-- The two equations displayed in Report (7). -/
def Report7 (a h : ℝ) (F G : Lattice) : Prop :=
  ReportUW.reportN1 a h (physU F G) (ReportUW.omega G) = 0 ∧
  ReportUW.reportN2 a h (physU F G) (ReportUW.omega G) = 0

/-- The two evolution equations and the lattice constraint of Report (21). -/
def Report21 (a h : ℝ) (F G : Lattice) : Prop :=
  ReportQRM.residualQ a h F G = 0 ∧ ReportQRM.residualR a h F G = 0 ∧
  ∀ j x t, (ReportQRM.M G (j+1) x t - ReportQRM.M G j x t) / h +
    ReportQRM.Q F G j x t * ReportQRM.R h F G j x t = 1

/-- Every physical reconstruction identity displayed in Report (22). -/
def Report22 (h : ℝ) (F G : Lattice) : Prop :=
  ∀ j x t,
    physU F G j x t = 2 * lx (ReportQRM.Q F G) j x t / ReportQRM.Q F G j x t ∧
    ReportQRM.omega G j x t =
      h * (1 - ReportQRM.Q F G j x t * ReportQRM.R h F G j x t) ∧
    ReportQRM.omega G j x t = ReportQRM.M G (j+1) x t - ReportQRM.M G j x t ∧
    physV h F G j x t = 4 * (1 - ReportQRM.Q F G j x t * ReportQRM.R h F G j x t) +
      (physU F G (j+1) x t - physU F G (j-1) x t) / (2*h)

/-- The actual exponential Q agrees with the centered positive square-root ratio. -/
theorem Q_is_centered_ratio (F G : Lattice) (hFp : PositiveL F) (hGp : PositiveL G) :
    ∀ j x t, ReportQRM.Q F G j x t =
      F j x t / Real.sqrt (G j x t * G (j+1) x t) := by
  intro j x t
  change Real.exp (Real.log (F j x t) - (1/2 : ℝ) *
    (Real.log (G j x t) + Real.log (G (j+1) x t))) = _
  rw [show (1/2 : ℝ) * (Real.log (G j x t) + Real.log (G (j+1) x t)) =
    (Real.log (G j x t) + Real.log (G (j+1) x t)) / 2 by ring]
  exact ReportQRatio.centered_exp_ratio _ _ _ (hFp j x t) (hGp j x t) (hGp (j+1) x t)

/-- First route: the original discrete bilinear pair implies Report (7). -/
theorem bilinear_to_report7 (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) : Report7 a h F G :=
  ReportUW.semiPair_implies_report7 a h F G hne hF hG hFp hGp hsp

/-- Second route: the same pair implies Report (21) together with Report (22). -/
theorem bilinear_to_report21_22 (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) : Report21 a h F G ∧ Report22 h F G :=
  ⟨ReportQRM.semiPair_implies_report21 a h F G hne hF hG hFp hGp hsp,
   ReportQRM.report22 h F G hne hF hG hFp hGp⟩

/-- Both routes and the original centered tau ratio, from one common starting pair. -/
theorem bilinear_to_both (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : SemiPair a h F G) :
    Report7 a h F G ∧ Report21 a h F G ∧ Report22 h F G ∧
      ∀ j x t, ReportQRM.Q F G j x t =
        F j x t / Real.sqrt (G j x t * G (j+1) x t) := by
  have hsecond := bilinear_to_report21_22 a h F G hne hF hG hFp hGp hsp
  exact ⟨bilinear_to_report7 a h F G hne hF hG hFp hGp hsp,
    hsecond.1, hsecond.2, Q_is_centered_ratio F G hFp hGp⟩

#print axioms Q_is_centered_ratio
#print axioms bilinear_to_report7
#print axioms bilinear_to_report21_22
#print axioms bilinear_to_both

end DLWContract.ReportEndpoints
