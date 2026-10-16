import FinalEndpoint

namespace NotebookDLWCoordinates
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

#print DLWLean.FieldCoordinates

def U {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : ℝ :=
  z.p.value j x +
    (par.gamma - latticeMean (fun i => z.p.value i x * z.s.value i x)) / par.c

def w {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : ℝ :=
  par.c + z.s.value j x

example {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : U z j x = z.U j x := rfl

example {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : w z j x = z.w j x := rfl

theorem reconstruction {par : FieldParameters}
    (f : PeriodicPhysicalState par) (j : Fin par.M) (x : ℝ) :
    f.toCoordinates.U j x = f.U.value j x ∧
    f.toCoordinates.w j x = f.w.value j x :=
  ⟨f.reconstruct_U j x, f.reconstruct_w j x⟩

#check reconstruction

end
end NotebookDLWCoordinates
