import AmbientAdlerInvolution
import ConstructedChargeMomentum
import GradientNondegeneracy

namespace DLWLean
noncomputable section
open scoped BigOperators

namespace AmbientSpectrumBase
variable {par : FieldParameters} {z : ClosedPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A]
    (base : AmbientSpectrumBase par (coordinateAmbient (closedPairCoordinates par z)) A)
include base

def physicalFactors : GlobalPDO.FactorRealization par z base.model where
  spatial := base.spatial
  denominator := base.factors.denominator
  denominator_eq j := by
    rw [← GlobalPDO.ambient_evaluation_beta]
    exact base.factors.denominator_eq j

theorem physical_site_eq (j : Fin par.M) : base.physicalFactors.site j = base.factors.site j := by
  unfold GlobalPDO.FactorRealization.site AmbientPDO.FactorRealization.site physicalFactors
  rw [GlobalPDO.ambient_evaluation_g]

theorem physical_siteNat_eq (j : ℕ) : base.physicalFactors.siteNat j = base.factors.siteNat j := by
  unfold GlobalPDO.FactorRealization.siteNat AmbientPDO.FactorRealization.siteNat
  split_ifs
  · exact base.physical_site_eq _
  · rfl

theorem physical_monodromyDifference_eq (n : ℕ) :
    base.physicalFactors.monodromyDifference n = base.factors.monodromyDifference n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [GlobalPDO.FactorRealization.monodromyDifference,
      AmbientPDO.FactorRealization.monodromyDifference, base.physical_siteNat_eq, ih]

def physicalNormalized : GlobalPDO.NormalizedRealization base.physicalFactors where
  difference := base.normalized.difference
  difference_eq := by rw [base.physical_monodromyDifference_eq]; exact base.normalized.difference_eq

theorem physical_charge_identity (n : ℕ) :
    AmbientPDO.constructedCharge par n (coordinateAmbient (closedPairCoordinates par z)) =
      GlobalPDO.constructedCharge par n z :=
  GlobalPDO.ambient_constructedCharge_eq base.physicalNormalized n

end AmbientSpectrumBase

/-- Intermediate physical representation. The final entry point builds
this structure from PhysicalFactorSpectrumRepresentation using the
proved free-factor coordinate and projection bridge. -/
structure PhysicalSpectrumRepresentation (par : FieldParameters) (z : ClosedPeriodicPair par) where
  A : Type
  ringA : Ring A
  algebraA : Algebra ℝ A
  base : @AmbientSpectrumBase par (coordinateAmbient (closedPairCoordinates par z)) A ringA algebraA
  adlerFoundation : @AmbientAdlerFoundation par (coordinateAmbient (closedPairCoordinates par z)) A
    ringA algebraA base
  wardFoundation : ActualSpectralWardFoundation par (coordinateAmbient (closedPairCoordinates par z))

attribute [instance] PhysicalSpectrumRepresentation.ringA PhysicalSpectrumRepresentation.algebraA

def ActualSpectralFoundation (par : FieldParameters) : Prop :=
  ∀ z : ClosedPeriodicPair par, Nonempty (PhysicalSpectrumRepresentation par z)

theorem actualSpectral_charge_identity (par : FieldParameters) (foundation : ActualSpectralFoundation par)
    (n : ℕ) (z : ClosedPeriodicPair par) :
    AmbientPDO.constructedCharge par n (coordinateAmbient (closedPairCoordinates par z)) =
      GlobalPDO.constructedCharge par n z := by
  obtain ⟨rep⟩ := foundation z
  exact rep.base.physical_charge_identity n

/-- The global physical Euler gradient equals the actual Ward-reduced
ambient Euler gradient. Equality follows from actual derivatives and
nondegeneracy; a target gradient formula is never an input. -/
theorem actualSpectral_gradient_eq_reduced (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (n : ℕ) (z : ClosedPeriodicPair par)
    (ward : ActualSpectralWardFoundation par (coordinateAmbient (closedPairCoordinates par z))) :
    GlobalPDO.constructedChargeGradient par n z =
      reducedAmbientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n)
        (coordinateAmbient (closedPairCoordinates par z))
        (actualSpectralCommonWard par _ ward n) := by
  apply coefficientGradientPairing_ext par
  intro v
  have hambient := reducedAmbientEulerGradient_hasDerivAt
    (AmbientPDO.periodicDensityPolynomial par n) (closedPairCoordinates par z)
      (actualSpectralCommonWard par _ ward n) v
  change HasDerivAt (fun t : ℝ => AmbientPDO.constructedCharge par n
      (coordinateAmbient (closedPairCoordinates par (z + t • v))))
    (coefficientGradientPairing par
      (reducedAmbientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n)
        (coordinateAmbient (closedPairCoordinates par z))
        (actualSpectralCommonWard par _ ward n)) v) 0 at hambient
  have hfun : (fun t : ℝ => AmbientPDO.constructedCharge par n
      (coordinateAmbient (closedPairCoordinates par (z + t • v)))) =
      (fun t : ℝ => GlobalPDO.constructedCharge par n (z + t • v)) :=
    funext (fun t => actualSpectral_charge_identity par foundation n (z + t • v))
  rw [hfun] at hambient
  exact (GlobalPDO.constructedChargeGradient_hasDerivAt par n z v).unique hambient

/-- The actual reduced brackets of all constructed positive spectral
charges vanish under the intermediate representation interface above.
FactorAdlerFoundation supplies its transport from the free-factor theory. -/
theorem actualSpectralBracket_zero (par : FieldParameters) (foundation : ActualSpectralFoundation par)
    (m n : ℕ) (z : ClosedPeriodicPair par) (hm : 0 < m) (hn : 0 < n) :
    reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
      (GlobalPDO.constructedChargeGradient par n z) = 0 := by
  obtain ⟨rep⟩ := foundation z
  rw [actualSpectral_gradient_eq_reduced par foundation m z rep.wardFoundation,
    actualSpectral_gradient_eq_reduced par foundation n z rep.wardFoundation]
  exact actualReducedAmbientSpectralBracket_zero rep.base rep.adlerFoundation rep.wardFoundation m n hm hn

#print axioms AmbientSpectrumBase.physical_charge_identity
#print axioms actualSpectral_gradient_eq_reduced
#print axioms actualSpectralBracket_zero
end
end DLWLean
