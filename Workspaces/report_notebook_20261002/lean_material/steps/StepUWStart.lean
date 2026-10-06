import StepUWImport

namespace DLWContract.ReportUW

def StartPoint (a h : ℝ) (F G : Lattice) : Prop :=
  ∀ j, bil (a-h/2) (F j) (G j) = 0 ∧
    bil (a+h/2) (F j) (G (j+1)) = 0

#print StartPoint

end DLWContract.ReportUW
