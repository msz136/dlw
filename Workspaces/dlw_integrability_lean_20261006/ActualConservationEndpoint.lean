import Endpoint
import ActualCoefficientSource
import ActualTraceDerivative

namespace DLWLean
noncomputable section

/-- A precise formal PDO representation interface over the actual smooth
spacetime coefficient algebra. Its inputs specify multiplication,
residue and formal inverses; the physical Lax/conservation conclusions
are absent. Constructing its canonical PDO instance remains separate. -/
structure PhysicalFormalModel (par : FieldParameters) (start : StartPoint par)
    (A : Type*) [Ring A] [Algebra ℝ A] where
  model : CoefficientOperatorModel (PeriodicSpacetimeCoefficient par.Lx) A
  space_is_actual : model.space = periodicSpacetimeSpaceEvolution par.Lx
  time_is_actual : model.time = periodicSpacetimeTimeEvolution par.Lx
  v0 : ℝ
  residue : A →ₗ[ℝ] PeriodicSpacetimeCoefficient par.Lx
  residue_time : ∀ a, residue (model.evolution.toLinearMap a) =
    (periodicSpacetimeTimeEvolution par.Lx).toLinearMap (residue a)
  cyclic : ∀ t a b, spacetimePeriodIntegral par.Lx t (residue (a * b)) =
    spacetimePeriodIntegral par.Lx t (residue (b * a))
  denominator : Fin par.M → Aˣ
  denominator_value : ∀ j, (denominator j : A) = model.factor
    (start.coefficientSource model space_is_actual time_is_actual v0 j).beta
  monodromyMinusOne : Aˣ
  monodromy_value : (monodromyMinusOne : A) =
    transferProduct (fun j => (↑(denominator (periodicSite par j))⁻¹ : A) *
      model.factor
        (start.coefficientSource model space_is_actual time_is_actual v0
          (periodicSite par j)).alpha) par.M - 1

variable {par : FieldParameters} {start : StartPoint par}
variable {A : Type*} [Ring A] [Algebra ℝ A]

def PhysicalFormalModel.L (pdo : PhysicalFormalModel par start A) : A :=
  normalizedL par.G par.B pdo.monodromyMinusOne

def PhysicalFormalModel.C (pdo : PhysicalFormalModel par start A) (n : ℕ) (t : ℝ) : ℝ :=
  (n : ℝ)⁻¹ * spacetimePeriodIntegral par.Lx t (pdo.residue (pdo.L ^ n))

def PhysicalFormalModel.operatorStart (pdo : PhysicalFormalModel par start A) (t : ℝ) :
    OperatorStart par A :=
  operatorStartFromPhysicalSources par pdo.model
    (spacetimeResidueTrace par.Lx t pdo.residue (pdo.cyclic t)) 0
    (start.coefficientSource pdo.model pdo.space_is_actual pdo.time_is_actual pdo.v0)
    (start.coefficientSource_potential_next pdo.model pdo.space_is_actual
      pdo.time_is_actual pdo.v0)
    pdo.denominator pdo.denominator_value pdo.monodromyMinusOne pdo.monodromy_value

/-- From the actual original PDE, every supplied formal PDO realization
has zero ordinary time derivatives of all positive-order residue charges.
This replaces the earlier merely algebraic-rate endpoint. -/
theorem physical_spectral_conservation
    (pdo : PhysicalFormalModel par start A) :
    ∀ n : ℕ, 0 < n → ∀ t : ℝ, HasDerivAt (pdo.C n) 0 t := by
  intro n hn t
  have hderiv := actualSpectralInvariant_hasDerivAt par.Lx par.Lx_pos
    pdo.residue pdo.model.evolution pdo.residue_time pdo.L n t
  have hzero := (operator_endpoint par (pdo.operatorStart t)).1 n hn
  have hrate : (n : ℝ)⁻¹ * spacetimePeriodIntegral par.Lx t
      (pdo.residue (pdo.model.evolution.toLinearMap (pdo.L ^ n))) = 0 := hzero
  rw [hrate] at hderiv
  exact hderiv

#print axioms physical_spectral_conservation
end
end DLWLean
