import FinalEndpoint

namespace NotebookDLWGeneric
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

theorem oddGeneric (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) (N : ℕ) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z)) :=
  actualOdd_generically_independent par foundation.toActual N

theorem familyGeneric (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) (N : ℕ) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
        gradientCovector par (actualPhysicalFamilyGradient par i.val z)) :=
  actualPhysicalFamily_generically_independent par foundation.toActual N

#check oddGeneric
#check familyGeneric
#print axioms oddGeneric
#print axioms familyGeneric

end
end NotebookDLWGeneric
