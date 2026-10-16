import AdlerFactorCoordinates

namespace DLWLean
noncomputable section
open scoped BigOperators

def staticFactorVariation {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A)
    (v : FactorPeriodicPair par) (j : Fin par.M) : A :=
  (↑(base.factors.denominator j)⁻¹ : A) * base.model.coefficient (v.2 j) *
      (1 + base.factors.site j) -
    (↑(base.factors.denominator j)⁻¹ : A) * base.model.coefficient (v.1 j)

def staticFactorVariationNat {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A)
    (v : FactorPeriodicPair par) (j : ℕ) : A :=
  if hj : j < par.M then staticFactorVariation base v ⟨j, hj⟩ else 0

def staticMonodromyVariation {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A)
    (v : FactorPeriodicPair par) : ℕ → A
  | 0 => 0
  | n + 1 => staticFactorVariationNat base v n * base.factors.monodromy n +
      (1 + base.factors.siteNat n) * staticMonodromyVariation base v n

/-- The actual source keeps the lattice mean of w fixed. Its free factor
variation is therefore the projection of the raw ambient variation. -/
def sourceFactorTangent (par : FieldParameters) (v : AmbientPeriodicPair par) :
    FactorPeriodicPair par :=
  ((1 / 2 : ℝ) • v.1 + (par.h / 8 : ℝ) • (projectedCoefficientGradient par v.2),
    (1 / 2 : ℝ) • v.1 - (par.h / 8 : ℝ) • (projectedCoefficientGradient par v.2))

theorem sourceFactorTangent_eq_projection (par : FieldParameters)
    (v : AmbientPeriodicPair par) :
    sourceFactorTangent par v = factorProjection par (ambientToFactorTangent par v) := by
  have hp : (fun j => (ambientToFactorTangent par v).1 j -
      (ambientToFactorTangent par v).2 j) = fun j => (par.h / 4 : ℝ) • v.2 j := by
    funext j
    dsimp [ambientToFactorTangent]
    module
  have hm : factorDifferenceMean par (ambientToFactorTangent par v) =
      (par.h / 4 : ℝ) • coefficientLatticeMean par v.2 := by
    rw [factorDifferenceMean, hp, coefficientLatticeMean_smul]
  unfold factorProjection
  rw [hm]
  apply Prod.ext <;> funext j <;>
    dsimp [sourceFactorTangent, ambientToFactorTangent, projectedCoefficientGradient] <;> module

theorem ambientAffine_g_time_slice (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (j : Fin par.M) :
    spacetimeSlice par.Lx 0 ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap
      (ambientAffinePolynomialEvaluation par z v (AmbientPDO.g par j))) =
      (par.h / 4 : ℝ) • (projectedCoefficientGradient par v.2 j) := by
  rw [ambientAffinePolynomialEvaluation_time_slice]
  simp [AmbientPDO.g, AmbientPDO.w, AmbientPDO.s, AmbientPDO.projectedJet,
    ambientPolynomialVariation, ambientPolynomialValue, ambientJet,
    ambientSpatialJet, ambientComponent, projectedCoefficientGradient,
    coefficientLatticeMean, Algebra.smul_def]

theorem ambientAffine_beta_time_slice (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (j : Fin par.M) :
    spacetimeSlice par.Lx 0 ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap
      (ambientAffinePolynomialEvaluation par z v (AmbientPDO.beta par j))) =
      (sourceFactorTangent par v).2 j := by
  rw [ambientAffinePolynomialEvaluation_time_slice]
  simp [AmbientPDO.beta, AmbientPDO.U, AmbientPDO.g, AmbientPDO.w,
    AmbientPDO.s, AmbientPDO.projectedJet, ambientPolynomialVariation,
    ambientPolynomialValue, ambientJet, ambientSpatialJet, ambientComponent,
    sourceFactorTangent, projectedCoefficientGradient, coefficientLatticeMean,
    Algebra.smul_def]
  apply Subtype.ext
  funext x
  simp only [Subalgebra.coe_mul, Subalgebra.coe_sub, Pi.mul_apply, Pi.sub_apply]
  have hconstant (r : ℝ) :
      (algebraMap ℝ (PeriodicCoefficient par.Lx) r : ℝ → ℝ) x = r :=
    (coefficientEvaluation par.Lx x).commutes r
  simp_rw [hconstant]
  ring

namespace AmbientSpectrumSpecialization
variable {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] {base : AmbientSpectrumBase par z A}
    {v : AmbientPeriodicPair par} (spec : AmbientSpectrumSpecialization base v)

theorem denominator_first_variation (j : Fin par.M) :
    spec.atZero (spec.source.model.evolution.toLinearMap
      (spec.source.factors.denominator j : spec.B)) =
      -base.model.coefficient ((sourceFactorTangent par v).2 j) := by
  rw [spec.source.factors.denominator_eq, map_sub, spec.source.model.evolution_D,
    spec.source.model.evolution_coeff, zero_sub, map_neg, spec.atZero_coefficient,
    ambientAffine_beta_time_slice]

theorem inverse_denominator_first_variation (j : Fin par.M) :
    spec.atZero (spec.source.model.evolution.toLinearMap
      (↑(spec.source.factors.denominator j)⁻¹ : spec.B)) =
      (↑(base.factors.denominator j)⁻¹ : A) *
        base.model.coefficient ((sourceFactorTangent par v).2 j) *
          (↑(base.factors.denominator j)⁻¹ : A) := by
  rw [unit_inverse_evolution, map_mul, map_mul, map_neg,
    spec.inverse_denominator_zero, spec.denominator_first_variation]
  noncomm_ring

theorem g_first_variation (j : Fin par.M) :
    spec.atZero (spec.source.model.evolution.toLinearMap
      (spec.source.model.normal.coefficient
        (ambientAffinePolynomialEvaluation par z v (AmbientPDO.g par j)))) =
      base.model.coefficient ((par.h / 4 : ℝ) • (projectedCoefficientGradient par v.2 j)) := by
  rw [spec.source.model.evolution_coeff, spec.atZero_coefficient,
    ambientAffine_g_time_slice]

theorem site_first_variation (j : Fin par.M) :
    spec.atZero (spec.source.model.evolution.toLinearMap (spec.source.factors.site j)) =
      staticFactorVariation base (sourceFactorTangent par v) j := by
  have hcoord : (sourceFactorTangent par v).1 j =
      (sourceFactorTangent par v).2 j +
        (par.h / 4 : ℝ) • (projectedCoefficientGradient par v.2 j) := by
    dsimp [sourceFactorTangent]
    module
  unfold AmbientPDO.FactorRealization.site
  rw [spec.source.model.evolution.leibniz, map_neg]
  simp only [map_add, map_mul, map_neg]
  rw [
    spec.inverse_denominator_first_variation, spec.inverse_denominator_zero,
    spec.atZero_coefficient, ambientAffinePolynomialEvaluation_slice_zero,
    spec.g_first_variation]
  unfold staticFactorVariation AmbientPDO.FactorRealization.site
  rw [hcoord, map_add]
  noncomm_ring

theorem siteNat_first_variation (j : ℕ) :
    spec.atZero (spec.source.model.evolution.toLinearMap (spec.source.factors.siteNat j)) =
      staticFactorVariationNat base (sourceFactorTangent par v) j := by
  unfold AmbientPDO.FactorRealization.siteNat staticFactorVariationNat
  split_ifs
  · exact spec.site_first_variation _
  · simp

theorem monodromy_first_variation (n : ℕ) :
    spec.atZero (spec.source.model.evolution.toLinearMap (spec.source.factors.monodromy n)) =
      staticMonodromyVariation base (sourceFactorTangent par v) n := by
  induction n with
  | zero => simp [AmbientPDO.FactorRealization.monodromy, staticMonodromyVariation,
      evolution_map_one]
  | succ n ih =>
    rw [AmbientPDO.FactorRealization.monodromy, spec.source.model.evolution.leibniz]
    simp only [map_add, evolution_map_one, zero_add, map_mul, map_one]
    rw [spec.siteNat_first_variation, spec.monodromy_zero, ih, spec.siteNat_zero]
    rfl

theorem monodromyFirstVariation_eq_source_static :
    spec.monodromyFirstVariation =
      staticMonodromyVariation base (sourceFactorTangent par v) par.M :=
  spec.monodromy_first_variation par.M

/-- The actual smooth affine source is exactly the projected free
factor variation, with no projection hidden in the external Adler
product/inverse theorem. -/
theorem monodromyFirstVariation_eq_static :
    spec.monodromyFirstVariation =
      staticMonodromyVariation base
        (factorProjection par (ambientToFactorTangent par v)) par.M := by
  rw [spec.monodromyFirstVariation_eq_source_static, sourceFactorTangent_eq_projection]

end AmbientSpectrumSpecialization

#print axioms AmbientSpectrumSpecialization.site_first_variation
#print axioms AmbientSpectrumSpecialization.monodromyFirstVariation_eq_source_static
#print axioms AmbientSpectrumSpecialization.monodromyFirstVariation_eq_static
end
end DLWLean
