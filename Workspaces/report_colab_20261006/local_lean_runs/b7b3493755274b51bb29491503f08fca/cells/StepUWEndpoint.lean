import StepUWStart

noncomputable section
open DLWContract DLWContract.ReportUW

-- 式（7）：u 与 ω 的两条演化方程。
example (a h : ℝ) (F G : Lattice) (hh : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : StartPoint a h F G) :
    reportN1 a h (physU F G) (omega G) = 0 ∧
      reportN2 a h (physU F G) (omega G) = 0 :=
  semiPair_implies_report7 a h F G hh hF hG hFp hGp hsp

-- 式（8）：重构后的物理场 (u, v)。
example (a h : ℝ) (F G : Lattice) (hh : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : StartPoint a h F G) :
    NonlinearPair a h (physU F G) (vFromOmega h (physU F G) (omega G)) :=
  semiPair_implies_report8 a h F G hh hF hG hFp hGp hsp

#print axioms DLWContract.ReportUW.semiPair_implies_report7
#print axioms DLWContract.ReportUW.semiPair_implies_report8
