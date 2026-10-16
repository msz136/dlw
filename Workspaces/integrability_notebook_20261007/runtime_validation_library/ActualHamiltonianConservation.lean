import ActualPolynomialCurveDerivative
import ActualSpectralInvolution
import PhysicalEnergyEndpoint

/-!
Ordinary time conservation on the actual physical trajectory. The
charges here are the same finite differential-polynomial integrals as
in the static spectral and independence theorems. The proof uses the
proved Hamiltonian coordinate equations, ordinary differentiation of
the genuine smooth spacetime source, and the actual reduced bracket.
-/
namespace DLWLean
noncomputable section

theorem StartPoint.actualVelocity_eq_K_vector {par : FieldParameters}
    (start : StartPoint par) (t : ℝ) :
    start.actualVelocity t =
      reducedHamiltonianVector par (actualPhysicalKGradient par (start.closedCurve t)) := by
  unfold StartPoint.actualVelocity actualPhysicalKGradient StartPoint.closedCurve
  rw [FieldCoordinates.closedPairCoordinates_recover]

/-- Ordinary time derivative, rather than only an affine-line variation. -/
theorem StartPoint.fieldPolynomialIntegral_hamiltonian_derivative {par : FieldParameters}
    (start : StartPoint par)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) (t : ℝ) :
    HasDerivAt (fun τ => fieldPolynomialIntegral par p (start.closedCurve τ))
      (reducedBracketValue par (fieldEulerGradient par p (start.closedCurve t))
        (actualPhysicalKGradient par (start.closedCurve t))) t := by
  have h := start.fieldEulerGradient_time_pairing p t
  rw [start.actualVelocity_eq_K_vector] at h
  exact h

theorem StartPoint.actualConstructedCharge_hasDerivAt {par : FieldParameters}
    (start : StartPoint par) (n : ℕ) (t : ℝ) :
    HasDerivAt (fun τ => GlobalPDO.constructedCharge par n (start.closedCurve τ))
      (reducedBracketValue par (GlobalPDO.constructedChargeGradient par n (start.closedCurve t))
        (actualPhysicalKGradient par (start.closedCurve t))) t :=
  start.fieldPolynomialIntegral_hamiltonian_derivative
    (GlobalPDO.periodicDensityPolynomial par n) t

theorem constructedCharge_bracket_actualK_zero (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (n : ℕ) (hn : 0 < n)
    (z : ClosedPeriodicPair par) :
    reducedBracketValue par (GlobalPDO.constructedChargeGradient par n z)
      (actualPhysicalKGradient par z) = 0 := by
  rw [actualPhysicalKGradient_eq_first_charge,
    reducedBracketValue_add_right, reducedBracketValue_smul_right,
    reducedBracketValue_smul_right,
    actualSpectralBracket_zero par foundation n 1 z hn (by omega),
    GlobalPDO.constructedCharge_bracket_momentum_zero]
  ring

/-- Every positive spectral charge has zero ordinary time derivative
along the original physical Hamiltonian trajectory. -/
theorem StartPoint.actualConstructedCharge_conserved {par : FieldParameters}
    (start : StartPoint par) (foundation : ActualSpectralFoundation par)
    (n : ℕ) (hn : 0 < n) (t : ℝ) :
    HasDerivAt (fun τ => GlobalPDO.constructedCharge par n (start.closedCurve τ)) 0 t := by
  have h := start.actualConstructedCharge_hasDerivAt n t
  rw [constructedCharge_bracket_actualK_zero par foundation n hn] at h
  exact h

theorem StartPoint.actualPhysicalFamily_hasTimeDerivAt {par : FieldParameters}
    (start : StartPoint par) (n : ℕ) (t : ℝ) :
    HasDerivAt (fun τ => actualPhysicalFamily par n (start.closedCurve τ))
      (reducedBracketValue par (actualPhysicalFamilyGradient par n (start.closedCurve t))
        (actualPhysicalKGradient par (start.closedCurve t))) t := by
  let κ := if n = 0 then energyConstant par else 0
  have h := (start.fieldPolynomialIntegral_hasDerivAt
    (physicalFamilyDensityPolynomial par n) t).add_const κ
  have hf : (fun τ => actualPhysicalFamily par n (start.closedCurve τ)) =
      (fun τ => fieldPolynomialIntegral par (physicalFamilyDensityPolynomial par n)
        (start.closedCurve τ) + κ) := by
    funext τ
    exact actualPhysicalFamily_eq_density_plus_constant par (energyConstant par)
      (actualPhysicalK_eq_first_charge par) n (start.closedCurve τ)
  have hd := congrArg (fun f : ClosedPeriodicPair par →ₗ[ℝ] ℝ => f (start.actualVelocity t))
    (actualPhysicalFamily_covector_eq_density par n (start.closedCurve t))
  change coefficientGradientPairing par (actualPhysicalFamilyGradient par n (start.closedCurve t))
    (start.actualVelocity t) = _ at hd
  rw [← hd, start.actualVelocity_eq_K_vector] at h
  rw [hf]
  exact h

/-- K, P, C3, C5, ... are conserved as actual functions of the physical
fields, with the same definitions used for their reduced brackets. -/
theorem StartPoint.actualPhysicalFamily_conserved {par : FieldParameters}
    (start : StartPoint par) (foundation : ActualSpectralFoundation par)
    (n : ℕ) (t : ℝ) :
    HasDerivAt (fun τ => actualPhysicalFamily par n (start.closedCurve τ)) 0 t := by
  have h := start.actualPhysicalFamily_hasTimeDerivAt n t
  have hc := actualPhysicalFamily_commutes_of_spectral par
    (actualSpectralBracket_zero par foundation) n 0 (start.closedCurve t)
  change reducedBracketValue par (actualPhysicalFamilyGradient par n (start.closedCurve t))
    (actualPhysicalKGradient par (start.closedCurve t)) = 0 at hc
  rw [hc] at h
  exact h

#print axioms StartPoint.fieldPolynomialIntegral_hamiltonian_derivative
#print axioms StartPoint.actualConstructedCharge_conserved
#print axioms StartPoint.actualPhysicalFamily_conserved
end
end DLWLean
