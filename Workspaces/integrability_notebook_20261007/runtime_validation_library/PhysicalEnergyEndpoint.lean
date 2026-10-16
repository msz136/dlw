import GlobalFirstResidueBridge
import PhysicalFamilyGenericity

namespace DLWLean
noncomputable section
open scoped DLWFieldTopology

/-- The physical energy identity has no energy/residue identity premise.
It is supplied by the verified literal low-order coefficient calculation.
-/
theorem actualPhysicalK_eq_first_charge (par : FieldParameters) (z : ClosedPeriodicPair par) :
    actualPhysicalK par z = -8 * par.G * GlobalPDO.constructedCharge par 1 z +
      (par.gamma / par.c) * coefficientMomentum par z + energyConstant par :=
  GlobalPDO.physicalK_eq_constructed_C1 par z

theorem actualPhysicalKGradient_eq_first_charge (par : FieldParameters)
    (z : ClosedPeriodicPair par) :
    actualPhysicalKGradient par z =
      (-8 * par.G) • GlobalPDO.constructedChargeGradient par 1 z +
        (par.gamma / par.c) • momentumGradient z :=
  actualPhysicalKGradient_eq_of_energy par (energyConstant par)
    (actualPhysicalK_eq_first_charge par) z

theorem actualPhysicalFamily_covector_eq_density (par : FieldParameters) (n : ℕ)
    (z : ClosedPeriodicPair par) :
    gradientCovector par (actualPhysicalFamilyGradient par n z) =
      fieldPolynomialDifferential par (physicalFamilyDensityPolynomial par n) z :=
  actualPhysicalFamily_covector_eq_polynomial par (energyConstant par)
    (actualPhysicalK_eq_first_charge par) n z

theorem actualPhysicalFamily_commutes_of_spectral (par : FieldParameters)
    (hspectral : ∀ (m n : ℕ) (z : ClosedPeriodicPair par), 0 < m → 0 < n →
      reducedBracketValue par (GlobalPDO.constructedChargeGradient par m z)
        (GlobalPDO.constructedChargeGradient par n z) = 0) :
    ∀ (m n : ℕ) (z : ClosedPeriodicPair par),
      reducedBracketValue par (actualPhysicalFamilyGradient par m z)
        (actualPhysicalFamilyGradient par n z) = 0 :=
  actualPhysicalFamily_commutes_of_energy_and_spectral par (energyConstant par)
    (actualPhysicalK_eq_first_charge par) hspectral

theorem actualPhysicalFamily_independent_from_odd_minor (par : FieldParameters)
    {N : ℕ} (z : ClosedPeriodicPair par) (directions : Fin (N + 1) → ClosedPeriodicPair par)
    (extra : ClosedPeriodicPair par)
    (hminor : (covectorMinor
      (fun i : Fin (N + 1) => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z)) directions).det ≠ 0)
    (hannihilate : ∀ i, gradientCovector par (momentumGradient z) (directions i) = 0)
    (hextra : gradientCovector par (momentumGradient z) extra ≠ 0) :
    LinearIndependent ℝ (fun i : Fin (N + 2) =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val z)) :=
  actualPhysicalFamily_independent_of_odd_minor par (energyConstant par)
    (actualPhysicalK_eq_first_charge par) z directions extra hminor hannihilate hextra

theorem actualPhysicalFamily_generically_independent_from_witness (par : FieldParameters)
    {N : ℕ} (witness : ClosedPeriodicPair par)
    (hwitness : LinearIndependent ℝ (fun i : Fin N =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val witness))) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
        gradientCovector par (actualPhysicalFamilyGradient par i.val z)) :=
  actualPhysicalFamily_generically_independent_of_witness par (energyConstant par)
    (actualPhysicalK_eq_first_charge par) witness hwitness

#print axioms actualPhysicalK_eq_first_charge
#print axioms actualPhysicalKGradient_eq_first_charge
#print axioms actualPhysicalFamily_generically_independent_from_witness
end
end DLWLean
