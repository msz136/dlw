import FinalEndpoint

namespace NotebookDLWEndpoint
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

#print DLWLean.PeriodicIntegrabilityConclusion

theorem periodicIntegrability (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) :
    PeriodicIntegrabilityConclusion par :=
  general_periodic_dlw_integrability par foundation

#check periodicIntegrability
#print axioms periodicIntegrability

end
end NotebookDLWEndpoint
