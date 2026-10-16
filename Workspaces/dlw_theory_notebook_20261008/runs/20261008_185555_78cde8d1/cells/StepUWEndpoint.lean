import StepUWStart

noncomputable section
open DLWContract DLWContract.ReportUW

-- 式（7）的两个通量与两个残差，定义与证明库一致。
namespace DLWContract.ReportUW.NotebookDisplay

def fluxUW (a h : ℝ) (u w : Lattice) : Lattice :=
  (u ^ 2 + w ^ 2) / 2 + (2 * a) • u - h • w

def fluxOmega (a h : ℝ) (u w : Lattice) : Lattice :=
  (u + CC a) * w - h • u

def reportN1 (a h : ℝ) (u w : Lattice) : Lattice :=
  dm h (lt u) + lx (dm h (fluxUW a h u w)) +
    lxx (dm h u + (4 / h) • mm w)

def reportN2 (a h : ℝ) (u w : Lattice) : Lattice :=
  lt w + lx (fluxOmega a h u w) - lxx w

theorem reportN1_matches (a h : ℝ) (u w : Lattice) :
    reportN1 a h u w = DLWContract.ReportUW.reportN1 a h u w := rfl

theorem reportN2_matches (a h : ℝ) (u w : Lattice) :
    reportN2 a h u w = DLWContract.ReportUW.reportN2 a h u w := rfl

#print reportN1
#print reportN2

end DLWContract.ReportUW.NotebookDisplay

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
