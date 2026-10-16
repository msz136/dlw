import FinalEndpoint

namespace NotebookDLWConditions
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

#print DLWLean.FieldParameters
#print DLWLean.SmoothPeriodicField
#print DLWLean.PeriodicPhysicalState

theorem fixedMeans (par : FieldParameters)
    (f : PeriodicPhysicalState par) (x : ℝ) :
    latticeMean (fun j => f.w.value j x) = par.c ∧
    latticeMean (fun j => f.U.value j x * f.w.value j x) = par.gamma :=
  ⟨f.mean_w x, f.mean_Uw x⟩

#check fixedMeans

end
end NotebookDLWConditions
