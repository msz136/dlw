import StepUWStart

noncomputable section
open DLWContract DLWContract.ReportUW

-- (7): equations for u and ω.
example (a h : ℝ) (F G : Lattice) (hh : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : StartPoint a h F G) :
    reportN1 a h (physU F G) (omega G) = 0 ∧
      reportN2 a h (physU F G) (omega G) = 0 :=
  semiPair_implies_report7 a h F G hh hF hG hFp hGp hsp

-- (8): the reconstructed pair (u, v).
example (a h : ℝ) (F G : Lattice) (hh : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : StartPoint a h F G) :
    NonlinearPair a h (physU F G) (vFromOmega h (physU F G) (omega G)) :=
  semiPair_implies_report8 a h F G hh hF hG hFp hGp hsp

#print axioms DLWContract.ReportUW.semiPair_implies_report7
#print axioms DLWContract.ReportUW.semiPair_implies_report8
