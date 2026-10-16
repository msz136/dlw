import FinalEndpoint

namespace NotebookDLWConservation
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

theorem chargeConserved (par : FieldParameters)
    (foundation : FactorSpectralFoundation par)
    (start : StartPoint par) (n : ℕ) (hn : 0 < n) (t : ℝ) :
    HasDerivAt (fun τ => GlobalPDO.constructedCharge par n (start.closedCurve τ)) 0 t :=
  start.actualConstructedCharge_conserved foundation.toActual n hn t

theorem familyConserved (par : FieldParameters)
    (foundation : FactorSpectralFoundation par)
    (start : StartPoint par) (n : ℕ) (t : ℝ) :
    HasDerivAt (fun τ => actualPhysicalFamily par n (start.closedCurve τ)) 0 t :=
  start.actualPhysicalFamily_conserved foundation.toActual n t

#check chargeConserved
#check familyConserved
#print axioms chargeConserved
#print axioms familyConserved

end
end NotebookDLWConservation
