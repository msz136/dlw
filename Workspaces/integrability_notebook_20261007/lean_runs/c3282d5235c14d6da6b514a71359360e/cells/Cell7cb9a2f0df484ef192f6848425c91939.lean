import FinalEndpoint

namespace NotebookDLWCharges
noncomputable section
open DLWLean
open scoped BigOperators ContDiff DLWFieldTopology

def C (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) : ℝ :=
  fieldPolynomialIntegral par (GlobalPDO.periodicDensityPolynomial par n) z

def spectralL {par : FieldParameters} {z : ClosedPeriodicPair par}
    (rep : PhysicalSpectrumRepresentation par z) : rep.A :=
  (-par.G) • (↑rep.base.physicalNormalized.difference⁻¹ : rep.A) +
    (par.B - par.G / 2) • (1 : rep.A)

example (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) :
    C par n z = GlobalPDO.constructedCharge par n z := rfl

example {par : FieldParameters} {z : ClosedPeriodicPair par}
    (rep : PhysicalSpectrumRepresentation par z) : spectralL rep = rep.L := rfl

theorem traceIdentification {par : FieldParameters} {z : ClosedPeriodicPair par}
    (rep : PhysicalSpectrumRepresentation par z) (n : ℕ) :
    C par n z = (n : ℝ)⁻¹ * rep.base.tr.toLinearMap (spectralL rep ^ n) :=
  actualCharge_eq_trace rep n

#check traceIdentification
#print axioms traceIdentification

end
end NotebookDLWCharges
