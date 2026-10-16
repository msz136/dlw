import FinalEndpoint

namespace NotebookDLWFoundation
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

def foundation (par : FieldParameters) : Prop :=
  ∀ z : ClosedPeriodicPair par,
    Nonempty (PhysicalFactorSpectrumRepresentation par z)

example (par : FieldParameters) :
    foundation par = FactorSpectralFoundation par := rfl

#print DLWLean.PhysicalFactorSpectrumRepresentation
#print DLWLean.FactorAdlerFoundation
#check DLWLean.FactorSpectralFoundation.toActual

end
end NotebookDLWFoundation
