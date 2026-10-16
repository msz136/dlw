import FinalEndpoint

namespace NotebookDLWEnergy
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

def H0 (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
  let q := closedPairCoordinates par z
  par.h * ∑ j, ∫ x in (0 : ℝ)..par.Lx,
    (q.U j x) ^ 2 * q.w j x / 2 + beta par * (q.w j x) ^ 3 / 3 +
      q.w j x * deriv (q.U j) x +
        q.w j x * latticeResolvent par (fun i => deriv (q.w i) x) j / 2

def K (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
  H0 par z - par.gamma * (closedPairCoordinates par z).physicalUIntegral

def P (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
  coefficientPairing par z.1 z.2

def F (par : FieldParameters) : ℕ → ClosedPeriodicPair par → ℝ
  | 0 => actualPhysicalK par
  | 1 => coefficientMomentum par
  | n + 2 => GlobalPDO.constructedCharge par (2 * n + 3)

example (par : FieldParameters) (z : ClosedPeriodicPair par) :
    K par z = actualPhysicalK par z := rfl

example (par : FieldParameters) (z : ClosedPeriodicPair par) :
    P par z = coefficientMomentum par z := rfl

example (par : FieldParameters) : F par = actualPhysicalFamily par := rfl

theorem energyIdentity (par : FieldParameters) (z : ClosedPeriodicPair par) :
    actualPhysicalK par z = -8 * par.G * GlobalPDO.constructedCharge par 1 z +
      (par.gamma / par.c) * coefficientMomentum par z + energyConstant par :=
  actualPhysicalK_eq_first_charge par z

#check energyIdentity
#print axioms energyIdentity

end
end NotebookDLWEnergy
