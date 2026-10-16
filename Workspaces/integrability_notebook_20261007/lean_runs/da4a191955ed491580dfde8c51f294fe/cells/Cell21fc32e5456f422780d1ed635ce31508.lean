import FinalEndpoint

namespace NotebookDLWStart
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

#print DLWLean.previousSite

def physicalDLW (par : FieldParameters)
    (z : ℝ → FieldCoordinates par) : Prop :=
  ∀ t x j,
    deltaMinus par (fun i =>
      deriv (fun τ => (z τ).U i x) t +
        deriv (fun y => ((z t).U i y) ^ 2 / 2 +
          (par.h ^ 2 / 32) * ((z t).w i y) ^ 2) x) j +
      deriv (deriv (fun y =>
        deltaMinus par (fun i => (z t).U i y) j +
          averageMinus par (fun i => (z t).w i y) j)) x = 0 ∧
    deriv (fun τ => (z τ).w j x) t +
      deriv (fun y => (z t).U j y * (z t).w j y) x -
        deriv (deriv ((z t).w j)) x = 0

example (par : FieldParameters) (z : ℝ → FieldCoordinates par) :
    physicalDLW par z = PhysicalDLW par z := rfl

#print DLWLean.StartPoint

theorem originalEquations {par : FieldParameters} (start : StartPoint par) :
    physicalDLW par start.trajectory := start.physical_equations

#check originalEquations

end
end NotebookDLWStart
