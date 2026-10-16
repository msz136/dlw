import FinalEndpoint

namespace NotebookDLWInvolution
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

theorem spectralCommutes (par : FieldParameters)
    (foundation : FactorSpectralFoundation par)
    (m n : ℕ) (z : ClosedPeriodicPair par) (hm : 0 < m) (hn : 0 < n) :
    reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
      (GlobalPDO.constructedChargeGradient par n z) = 0 :=
  actualSpectralBracket_zero par foundation.toActual m n z hm hn

theorem withMomentum (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) :
    reducedBracketValue par (GlobalPDO.constructedChargeGradient par n z)
      (momentumGradient z) = 0 :=
  GlobalPDO.constructedCharge_bracket_momentum_zero par n z

theorem familyCommutes (par : FieldParameters)
    (foundation : FactorSpectralFoundation par)
    (m n : ℕ) (z : ClosedPeriodicPair par) :
    reducedBracketValue par (actualPhysicalFamilyGradient par m z)
      (actualPhysicalFamilyGradient par n z) = 0 :=
  actualPhysicalFamily_commutes par foundation.toActual m n z

#check spectralCommutes
#check withMomentum
#check familyCommutes
#print axioms familyCommutes

end
end NotebookDLWInvolution
