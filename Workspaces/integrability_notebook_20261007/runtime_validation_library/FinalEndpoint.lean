import ActualGenericIndependence
import ActualHamiltonianConservation
import FactorAdlerFoundation

namespace DLWLean
noncomputable section
open scoped DLWFieldTopology

def PhysicalSpectrumRepresentation.L {par : FieldParameters} {z : ClosedPeriodicPair par}
    (rep : PhysicalSpectrumRepresentation par z) : rep.A := rep.base.physicalNormalized.L

theorem actualCharge_eq_trace {par : FieldParameters} {z : ClosedPeriodicPair par}
    (rep : PhysicalSpectrumRepresentation par z) (n : ℕ) :
    GlobalPDO.constructedCharge par n z =
      (n : ℝ)⁻¹ * rep.base.tr.toLinearMap (rep.L ^ n) :=
  rep.base.physicalNormalized.constructedCharge_eq_spectralInvariant
    rep.base.tr rep.base.trace_eq n

theorem actualPhysicalFamily_commutes (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (m n : ℕ) (z : ClosedPeriodicPair par) :
    reducedBracketValue par (actualPhysicalFamilyGradient par m z)
      (actualPhysicalFamilyGradient par n z) = 0 :=
  actualPhysicalFamily_commutes_of_spectral par (actualSpectralBracket_zero par foundation) m n z

/-- The requested field conclusion, separated from the explicit PDO
foundation. All regularity and mean closure are carried by StartPoint
and ClosedPeriodicPair; no target property is a foundation field. -/
structure PeriodicIntegrabilityConclusion (par : FieldParameters) : Prop where
  traceIdentification : ∀ z : ClosedPeriodicPair par,
    ∃ rep : PhysicalSpectrumRepresentation par z, ∀ n : ℕ,
      GlobalPDO.constructedCharge par n z =
        (n : ℝ)⁻¹ * rep.base.tr.toLinearMap (rep.L ^ n)
  energy : ∀ z : ClosedPeriodicPair par,
    actualPhysicalK par z = -8 * par.G * GlobalPDO.constructedCharge par 1 z +
      (par.gamma / par.c) * coefficientMomentum par z + energyConstant par
  physicalHamiltonianEvolution : ∀ (start : StartPoint par) (t x : ℝ) (j : Fin par.M),
    (((reducedHamiltonianVector par
        (actualPhysicalKGradient par (start.closedCurve t))).1 j : ℝ → ℝ) x =
      deriv (fun τ => (start.trajectory τ).p.value j x) t) ∧
    (((reducedHamiltonianVector par
        (actualPhysicalKGradient par (start.closedCurve t))).2 j : ℝ → ℝ) x =
      deriv (fun τ => (start.trajectory τ).s.value j x) t)
  spectralInvolution : ∀ (m n : ℕ) (z : ClosedPeriodicPair par), 0 < m → 0 < n →
    reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
      (GlobalPDO.constructedChargeGradient par n z) = 0
  oddGeneric : ∀ N : ℕ, ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
    ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N => gradientCovector par
      (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z))
  familyInvolution : ∀ (m n : ℕ) (z : ClosedPeriodicPair par),
    reducedBracketValue par (actualPhysicalFamilyGradient par m z)
      (actualPhysicalFamilyGradient par n z) = 0
  familyGeneric : ∀ N : ℕ, ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
    ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val z))
  spectralConservation : ∀ (start : StartPoint par) (n : ℕ), 0 < n → ∀ t : ℝ,
    HasDerivAt (fun τ => GlobalPDO.constructedCharge par n (start.closedCurve τ)) 0 t
  familyConservation : ∀ (start : StartPoint par) (n : ℕ) (t : ℝ),
    HasDerivAt (fun τ => actualPhysicalFamily par n (start.closedCurve τ)) 0 t

theorem periodic_integrability_of_actual_foundation (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) : PeriodicIntegrabilityConclusion par where
  traceIdentification z := by
    obtain ⟨rep⟩ := foundation z
    exact ⟨rep, actualCharge_eq_trace rep⟩
  energy := actualPhysicalK_eq_first_charge par
  physicalHamiltonianEvolution start t x j := by
    unfold actualPhysicalKGradient StartPoint.closedCurve
    rw [FieldCoordinates.closedPairCoordinates_recover]
    exact start.physicalK_generates_coordinates t x j
  spectralInvolution := actualSpectralBracket_zero par foundation
  oddGeneric := actualOdd_generically_independent par foundation
  familyInvolution := actualPhysicalFamily_commutes par foundation
  familyGeneric := actualPhysicalFamily_generically_independent par foundation
  spectralConservation start n hn t := start.actualConstructedCharge_conserved foundation n hn t
  familyConservation start n t := start.actualPhysicalFamily_conserved foundation n t

/-- Main field theorem with the standard static free-factor Adler
foundation. All DLW coordinate, source-projection, energy, spectral,
Fourier and generic-independence bridges are proved in this project. -/
theorem general_periodic_dlw_integrability (par : FieldParameters)
    (foundation : FactorSpectralFoundation par) :
    PeriodicIntegrabilityConclusion par :=
  periodic_integrability_of_actual_foundation par foundation.toActual

#print axioms actualCharge_eq_trace
#print axioms periodic_integrability_of_actual_foundation
#print axioms general_periodic_dlw_integrability

end
end DLWLean
