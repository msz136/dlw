import FinalEndpoint

namespace NotebookDLWBracket
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

def J (par : FieldParameters) (g : ClosedPeriodicPair par) : ClosedPeriodicPair par :=
  (-(closedSpatialDerivative par g.2), -(closedSpatialDerivative par g.1))

def bracket (par : FieldParameters) (gF gH : ClosedPeriodicPair par) : ℝ :=
  coefficientGradientPairing par gF (J par gH)

example (par : FieldParameters) (gF gH : ClosedPeriodicPair par) :
    bracket par gF gH = reducedBracketValue par gF gH := rfl

theorem chargeDifferential (par : FieldParameters) (n : ℕ)
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun a : ℝ => GlobalPDO.constructedCharge par n (z + a • v))
      (gradientCovector par (GlobalPDO.constructedChargeGradient par n z) v) 0 :=
  GlobalPDO.constructedChargeGradient_hasDerivAt par n z v

#check chargeDifferential

end
end NotebookDLWBracket
