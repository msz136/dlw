import StaticFactorTraceCotangent
import FactorProjectionAlgebra

/-!
The external Adler product/inverse theorem is stated only for the static
free variations of independent first-order factors. The actual DLW
projected source, pairing normalization and Ward reduction are bridged
by proved finite algebra, not inserted as an external bracket identity.
-/
namespace DLWLean
noncomputable section
open scoped BigOperators

structure FactorAdlerFoundation {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A) where
  sources : ∀ v : AmbientPeriodicPair par, AmbientSpectrumSpecialization base v
  plus : A →ₗ[ℝ] A
  plus_coefficient : ∀ X e, base.model.coefficients (plus X) e =
    if 0 ≤ e then base.model.coefficients X e else 0
  product_inverse_transport : ∀ (f g : FactorPeriodicPair par) (X Y : A),
    (∀ v, factorPairing par f v = base.tr.toLinearMap
      (X * staticMonodromyVariation base v par.M)) →
    (∀ v, factorPairing par g v = base.tr.toLinearMap
      (Y * staticMonodromyVariation base v par.M)) →
    standardFactorBracket par f g =
      base.tr.toLinearMap (X * adler plus (base.factors.monodromy par.M) Y)

theorem FactorAdlerFoundation.actual_covector_eq_projected
    {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] {base : AmbientSpectrumBase par z A}
    (foundation : FactorAdlerFoundation base) (f : AmbientPeriodicPair par) (X : A)
    (hf : ∀ v, ambientPairing par f v =
      base.tr.toLinearMap (X * (foundation.sources v).monodromyFirstVariation)) :
    ambientToFactorCotangent par f = factorProjection par (staticFactorTraceCotangent base X) := by
  apply factorPairing_ext par
  intro v
  rw [factorPairing_actual_coordinate_change, hf,
    AmbientSpectrumSpecialization.monodromyFirstVariation_eq_static,
    ambientToFactorTangent_inverse, ← staticFactorTraceCotangent_pairing,
    factorPairing_projection_self_adjoint]

def FactorAdlerFoundation.toAmbient {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] {base : AmbientSpectrumBase par z A}
    (foundation : FactorAdlerFoundation base) : AmbientAdlerFoundation base where
  sources := foundation.sources
  plus := foundation.plus
  plus_coefficient := foundation.plus_coefficient
  factor_transport := by
    intro f g X Y hfWard hgWard hf hg
    have hfProj := foundation.actual_covector_eq_projected f X hf
    have hgProj := foundation.actual_covector_eq_projected g Y hg
    have hXWard : (∑ j : Fin par.M, ((staticFactorTraceCotangent base X).1 j +
        (staticFactorTraceCotangent base X).2 j)) = 0 := by
      rw [← factorProjection_sum_add par (staticFactorTraceCotangent base X),
        ← hfProj, ambientToFactorCotangent_sum_add, hfWard, smul_zero]
    have hYWard : (∑ j : Fin par.M, ((staticFactorTraceCotangent base Y).1 j +
        (staticFactorTraceCotangent base Y).2 j)) = 0 := by
      rw [← factorProjection_sum_add par (staticFactorTraceCotangent base Y),
        ← hgProj, ambientToFactorCotangent_sum_add, hgWard, smul_zero]
    rw [← independentFactorBracket_actual_coordinate_change par f g,
      independentFactorBracket, hfProj, hgProj,
      standardFactorBracket_projection_Ward par _ _ hXWard hYWard,
      foundation.product_inverse_transport _ _ X Y
        (staticFactorTraceCotangent_pairing base X) (staticFactorTraceCotangent_pairing base Y)]

structure PhysicalFactorSpectrumRepresentation (par : FieldParameters) (z : ClosedPeriodicPair par) where
  A : Type
  ringA : Ring A
  algebraA : Algebra ℝ A
  base : @AmbientSpectrumBase par (coordinateAmbient (closedPairCoordinates par z)) A ringA algebraA
  adlerFoundation : @FactorAdlerFoundation par (coordinateAmbient (closedPairCoordinates par z)) A
    ringA algebraA base
  wardFoundation : ActualSpectralWardFoundation par (coordinateAmbient (closedPairCoordinates par z))

attribute [instance] PhysicalFactorSpectrumRepresentation.ringA PhysicalFactorSpectrumRepresentation.algebraA

def PhysicalFactorSpectrumRepresentation.toActual {par : FieldParameters}
    {z : ClosedPeriodicPair par} (rep : PhysicalFactorSpectrumRepresentation par z) :
    PhysicalSpectrumRepresentation par z where
  A := rep.A
  ringA := rep.ringA
  algebraA := rep.algebraA
  base := rep.base
  adlerFoundation := rep.adlerFoundation.toAmbient
  wardFoundation := rep.wardFoundation

def FactorSpectralFoundation (par : FieldParameters) : Prop :=
  ∀ z : ClosedPeriodicPair par, Nonempty (PhysicalFactorSpectrumRepresentation par z)

theorem FactorSpectralFoundation.toActual {par : FieldParameters}
    (foundation : FactorSpectralFoundation par) : ActualSpectralFoundation par := by
  intro z
  obtain ⟨rep⟩ := foundation z
  exact ⟨rep.toActual⟩

#print axioms FactorAdlerFoundation.actual_covector_eq_projected
#print axioms FactorAdlerFoundation.toAmbient
#print axioms FactorSpectralFoundation.toActual
end
end DLWLean
