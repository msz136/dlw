import ActualPhysicalFamily
import CovectorWitness

namespace DLWLean
noncomputable section
open scoped BigOperators
open scoped DLWFieldTopology
set_option maxHeartbeats 800000

abbrev FieldDensity (par : FieldParameters) :=
  MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)

def momentumDensityPolynomial (par : FieldParameters) : FieldDensity par :=
  MvPolynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) par.h) *
    ∑ j : Fin par.M, MvPolynomial.X (true, j, 0) * MvPolynomial.X (false, j, 0)

theorem momentumDensityPolynomial_integral (par : FieldParameters) (z : ClosedPeriodicPair par) :
    fieldPolynomialIntegral par (momentumDensityPolynomial par) z = coefficientMomentum par z := by
  unfold fieldPolynomialIntegral fieldDifferentialPolynomial momentumDensityPolynomial
  simp only [MvPolynomial.eval_mul, MvPolynomial.eval_C, MvPolynomial.eval_sum,
    MvPolynomial.eval_X]
  change periodicCoefficientIntegral par.Lx
    (par.h • ∑ j : Fin par.M, z.1 j * z.2 j) = _
  rw [map_smul]
  rfl

theorem fieldPolynomialIntegral_add (par : FieldParameters) (p q : FieldDensity par)
    (z : ClosedPeriodicPair par) :
    fieldPolynomialIntegral par (p + q) z =
      fieldPolynomialIntegral par p z + fieldPolynomialIntegral par q z := by
  simp only [fieldPolynomialIntegral, fieldDifferentialPolynomial, MvPolynomial.eval_add, map_add]

theorem fieldPolynomialIntegral_smul (par : FieldParameters) (r : ℝ) (p : FieldDensity par)
    (z : ClosedPeriodicPair par) :
    fieldPolynomialIntegral par (r • p) z = r * fieldPolynomialIntegral par p z := by
  unfold fieldPolynomialIntegral fieldDifferentialPolynomial
  simp only [Algebra.smul_def]
  rw [IsScalarTower.algebraMap_apply ℝ (PeriodicCoefficient par.Lx) (FieldDensity par) r,
    MvPolynomial.algebraMap_eq, MvPolynomial.eval_mul, MvPolynomial.eval_C]
  change periodicCoefficientIntegral par.Lx
    (r • MvPolynomial.eval (fun i => fieldJet par i z) p) = _
  exact map_smul (periodicCoefficientIntegral par.Lx) r _

def physicalFamilyDensityPolynomial (par : FieldParameters) : ℕ → FieldDensity par
  | 0 => (-8 * par.G) • GlobalPDO.periodicDensityPolynomial par 1 +
      (par.gamma / par.c) • momentumDensityPolynomial par
  | 1 => momentumDensityPolynomial par
  | n + 2 => GlobalPDO.periodicDensityPolynomial par (2 * n + 3)

theorem actualPhysicalFamily_eq_density_plus_constant (par : FieldParameters) (κ : ℝ)
    (henergy : ∀ z : ClosedPeriodicPair par,
      actualPhysicalK par z = (-8 * par.G) * GlobalPDO.constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + κ)
    (n : ℕ) (z : ClosedPeriodicPair par) :
    actualPhysicalFamily par n z =
      fieldPolynomialIntegral par (physicalFamilyDensityPolynomial par n) z +
        (if n = 0 then κ else 0) := by
  rcases n with _ | _ | n
  · simp only [actualPhysicalFamily, physicalFamilyDensityPolynomial,
      fieldPolynomialIntegral_add, fieldPolynomialIntegral_smul,
      momentumDensityPolynomial_integral, ite_true, henergy]
    rfl
  · simp only [actualPhysicalFamily, physicalFamilyDensityPolynomial,
      momentumDensityPolynomial_integral, Nat.zero_add, Nat.one_ne_zero, ite_false, add_zero]
  · simp only [actualPhysicalFamily, physicalFamilyDensityPolynomial,
      show n + 2 ≠ 0 by omega, ite_false, add_zero]
    rfl

/-- The final family's actual directional covectors are identified with
the polynomial covectors by uniqueness of ordinary derivatives. -/
theorem actualPhysicalFamily_covector_eq_polynomial (par : FieldParameters) (κ : ℝ)
    (henergy : ∀ z : ClosedPeriodicPair par,
      actualPhysicalK par z = (-8 * par.G) * GlobalPDO.constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + κ)
    (n : ℕ) (z : ClosedPeriodicPair par) :
    gradientCovector par (actualPhysicalFamilyGradient par n z) =
      fieldPolynomialDifferential par (physicalFamilyDensityPolynomial par n) z := by
  apply LinearMap.ext
  intro v
  have hA := actualPhysicalFamily_hasDerivAt par n z v
  have hE := (fieldPolynomialDifferential_hasDerivAt par
    (physicalFamilyDensityPolynomial par n) z v).add_const (if n = 0 then κ else 0)
  have hfun : (fun t : ℝ => actualPhysicalFamily par n (z + t • v)) =
      fun t => fieldPolynomialIntegral par (physicalFamilyDensityPolynomial par n)
        (z + t • v) + (if n = 0 then κ else 0) :=
    funext fun t => actualPhysicalFamily_eq_density_plus_constant par κ henergy n (z + t • v)
  rw [hfun] at hA
  exact hA.unique hE

theorem derivativeMinor_eq_covectorMinor (par : FieldParameters) {N : ℕ}
    (charges : Fin N → FieldDensity par) (directions : Fin N → ClosedPeriodicPair par)
    (z : ClosedPeriodicPair par) :
    fieldPolynomialDerivativeMinor par charges directions z =
      (covectorMinor (fun i => fieldPolynomialDifferential par (charges i) z) directions).det := rfl

/-- A single independent actual field witness gives an open dense set
for the final finite block in the actual compact-jet field topology. -/
theorem actualPhysicalFamily_generically_independent_of_witness (par : FieldParameters)
    (κ : ℝ)
    (henergy : ∀ z : ClosedPeriodicPair par,
      actualPhysicalK par z = (-8 * par.G) * GlobalPDO.constructedCharge par 1 z +
        (par.gamma / par.c) * coefficientMomentum par z + κ)
    {N : ℕ} (witness : ClosedPeriodicPair par)
    (hwitness : LinearIndependent ℝ (fun i : Fin N =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val witness))) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
        gradientCovector par (actualPhysicalFamilyGradient par i.val z)) := by
  let charges : Fin N → FieldDensity par := fun i => physicalFamilyDensityPolynomial par i.val
  have heq (z : ClosedPeriodicPair par) :
      (fun i : Fin N => gradientCovector par (actualPhysicalFamilyGradient par i.val z)) =
        (fun i : Fin N => fieldPolynomialDifferential par (charges i) z) := by
    funext i
    exact actualPhysicalFamily_covector_eq_polynomial par κ henergy i.val z
  have hfield : LinearIndependent ℝ
      (fun i : Fin N => fieldPolynomialDifferential par (charges i) witness) := by
    rw [← heq witness]
    exact hwitness
  obtain ⟨directions, hminor⟩ := covectors_independent_exists_nonzero_minor
    (V := ClosedPeriodicPair par) (N := N)
    (fun i : Fin N => fieldPolynomialDifferential par (charges i) witness) hfield
  have hw : fieldPolynomialDerivativeMinor par
      charges directions witness ≠ 0 := by
    rw [derivativeMinor_eq_covectorMinor]
    exact hminor
  obtain ⟨S, ho, hd, hS⟩ := fieldPolynomialDifferentials_generically_independent par
    charges directions witness hw
  refine ⟨S, ho, hd, ?_⟩
  intro z hz
  rw [heq z]
  exact hS z hz

#print axioms momentumDensityPolynomial_integral
#print axioms actualPhysicalFamily_covector_eq_polynomial
#print axioms actualPhysicalFamily_generically_independent_of_witness
end
end DLWLean
