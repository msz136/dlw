import StepQRMStart

noncomputable section
open DLWContract DLWContract.ReportQRM

-- (21): equations for Q and R, and the lattice constraint.
example (a h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G)
    (hsp : StartPoint a h F G) :
    residualQ a h F G = 0 ∧ residualR a h F G = 0 ∧
      ∀ j x t, (M G (j+1) x t-M G j x t)/h + Q F G j x t*R h F G j x t = 1 :=
  semiPair_implies_report21 a h F G hne hF hG hFp hGp hsp

-- (22): reconstruction of u, ω and v.
example (h : ℝ) (F G : Lattice) (hne : h ≠ 0)
    (hF : SmoothL F) (hG : SmoothL G) (hFp : PositiveL F) (hGp : PositiveL G) :
    ∀ j x t,
      physU F G j x t = 2 * lx (Q F G) j x t / Q F G j x t ∧
      omega G j x t = h*(1-Q F G j x t*R h F G j x t) ∧
      omega G j x t = M G (j+1) x t-M G j x t ∧
      physV h F G j x t = 4*(1-Q F G j x t*R h F G j x t) +
        (physU F G (j+1) x t-physU F G (j-1) x t)/(2*h) :=
  report22 h F G hne hF hG hFp hGp

#print axioms DLWContract.ReportQRM.semiPair_implies_report21
#print axioms DLWContract.ReportQRM.report22
