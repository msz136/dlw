import AmbientSpectralVariation
import ActualSpectralWard

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem AmbientPDO.periodicPolynomialValue_eq_evaluation (par : FieldParameters)
    (z : AmbientPeriodicPair par) (p : AmbientPDO.Poly par) :
    ambientPolynomialValue par (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p) z =
      AmbientPDO.evaluation par z p := by
  unfold ambientPolynomialValue AmbientPDO.evaluation
  rw [← MvPolynomial.eval₂_eq_eval_map]
  rfl

theorem ambientAffinePolynomialEvaluation_slice_zero (par : FieldParameters)
    (z v : AmbientPeriodicPair par) (p : AmbientPDO.Poly par) :
    spacetimeSlice par.Lx 0 (ambientAffinePolynomialEvaluation par z v p) =
      AmbientPDO.evaluation par z p := by
  rw [← AmbientPDO.periodicPolynomialValue_eq_evaluation]
  apply Subtype.ext
  funext x
  change (ambientAffinePolynomialEvaluation par z v p : ℝ × ℝ → ℝ) (0, x) = _
  have h := ambientAffinePolynomialEvaluation_value par z v p 0 x
  simpa only [zero_smul, add_zero] using h

theorem algHom_unit_inverse {A B : Type*} [Ring A] [Ring B] [Algebra ℝ A] [Algebra ℝ B]
    (f : A →ₐ[ℝ] B) (u : Aˣ) (v : Bˣ) (hu : f (u : A) = (v : B)) :
    f (↑u⁻¹ : A) = (↑v⁻¹ : B) := by
  calc
    f (↑u⁻¹ : A) = (↑v⁻¹ : B) * ((v : B) * f (↑u⁻¹ : A)) := by
      rw [← mul_assoc, Units.inv_mul, one_mul]
    _ = _ := by rw [← hu, ← map_mul, Units.mul_inv, map_one, mul_one]

structure AmbientSpectrumBase (par : FieldParameters) (z : AmbientPeriodicPair par)
    (A : Type*) [Ring A] [Algebra ℝ A] where
  model : NormalPDOModel (PeriodicCoefficient par.Lx) A
  spatial : model.d = periodicSpatialEvolution par.Lx
  factors : AmbientPDO.FactorRealization par (AmbientPDO.evaluation par z) model
  normalized : AmbientPDO.NormalizedRealization factors
  tr : CyclicTrace A
  trace_eq : ∀ X, tr.toLinearMap X = periodicCoefficientIntegral par.Lx (model.coefficients X (-1))

/-- Epsilon=0 is a coefficientwise algebra specialization of formal
PDOs. Only coefficient, D and multiplication semantics are supplied. -/
structure AmbientSpectrumSpecialization {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A)
    (v : AmbientPeriodicPair par) where
  B : Type
  ringB : Ring B
  algebraB : Algebra ℝ B
  source : @AmbientAffineSpectrum par z v B ringB algebraB
  atZero : @AlgHom ℝ B A _ ringB.toSemiring _ algebraB _
  atZero_coefficient : ∀ r, atZero (source.model.normal.coefficient r) =
    base.model.coefficient (spacetimeSlice par.Lx 0 r)
  atZero_D : atZero (source.model.normal.D : B) = (base.model.D : A)
  atZero_coefficients : ∀ X e, base.model.coefficients (atZero X) e =
    spacetimeSlice par.Lx 0 (source.model.normal.coefficients X e)

attribute [instance] AmbientSpectrumSpecialization.ringB AmbientSpectrumSpecialization.algebraB

namespace AmbientSpectrumSpecialization
variable {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] {base : AmbientSpectrumBase par z A}
    {v : AmbientPeriodicPair par} (spec : AmbientSpectrumSpecialization base v)

theorem denominator_zero (j : Fin par.M) :
    spec.atZero (spec.source.factors.denominator j : spec.B) = (base.factors.denominator j : A) := by
  rw [spec.source.factors.denominator_eq, map_sub, spec.atZero_D,
    spec.atZero_coefficient, ambientAffinePolynomialEvaluation_slice_zero,
    base.factors.denominator_eq]

theorem inverse_denominator_zero (j : Fin par.M) :
    spec.atZero (↑(spec.source.factors.denominator j)⁻¹ : spec.B) =
      (↑(base.factors.denominator j)⁻¹ : A) :=
  algHom_unit_inverse spec.atZero _ _ (spec.denominator_zero j)

theorem site_zero (j : Fin par.M) :
    spec.atZero (spec.source.factors.site j) = base.factors.site j := by
  unfold AmbientPDO.FactorRealization.site
  rw [map_mul, map_neg, spec.inverse_denominator_zero, spec.atZero_coefficient,
    ambientAffinePolynomialEvaluation_slice_zero]

theorem siteNat_zero (j : ℕ) :
    spec.atZero (spec.source.factors.siteNat j) = base.factors.siteNat j := by
  unfold AmbientPDO.FactorRealization.siteNat
  split_ifs
  · exact spec.site_zero _
  · exact map_zero _

theorem monodromyDifference_zero (n : ℕ) :
    spec.atZero (spec.source.factors.monodromyDifference n) = base.factors.monodromyDifference n := by
  induction n with
  | zero => exact map_zero _
  | succ n ih =>
    rw [AmbientPDO.FactorRealization.monodromyDifference, map_add, map_add, map_mul,
      spec.siteNat_zero, ih]
    rfl

theorem monodromy_zero (n : ℕ) :
    spec.atZero (spec.source.factors.monodromy n) = base.factors.monodromy n := by
  have hs : spec.source.factors.monodromy n = spec.source.factors.monodromyDifference n + 1 := by
    rw [spec.source.factors.monodromyDifference_eq, sub_add_cancel]
  rw [hs, map_add, map_one, spec.monodromyDifference_zero,
    base.factors.monodromyDifference_eq, sub_add_cancel]

theorem difference_zero :
    spec.atZero (spec.source.normalized.difference : spec.B) = (base.normalized.difference : A) := by
  rw [spec.source.normalized.difference_eq, spec.monodromyDifference_zero,
    base.normalized.difference_eq]

theorem inverse_difference_zero :
    spec.atZero (↑spec.source.normalized.difference⁻¹ : spec.B) =
      (↑base.normalized.difference⁻¹ : A) :=
  algHom_unit_inverse spec.atZero _ _ spec.difference_zero

theorem normalizedL_zero :
    spec.atZero (normalizedL par.G par.B spec.source.normalized.difference) =
      normalizedL par.G par.B base.normalized.difference := by
  simp only [normalizedL, map_add, map_smul, map_one, spec.inverse_difference_zero]

theorem rationalGradient_zero (n : ℕ) :
    spec.atZero (rationalGradient par.G par.B spec.source.normalized.difference n) =
      rationalGradient par.G par.B base.normalized.difference n := by
  simp only [rationalGradient, map_smul, map_mul, map_pow,
    spec.inverse_difference_zero, spec.normalizedL_zero]

def sourceTrace : CyclicTrace spec.B where
  toLinearMap := base.tr.toLinearMap.comp spec.atZero.toLinearMap
  cyclic X Y := by
    change base.tr.toLinearMap (spec.atZero (X * Y)) = base.tr.toLinearMap (spec.atZero (Y * X))
    calc
      base.tr.toLinearMap (spec.atZero (X * Y)) =
          base.tr.toLinearMap (spec.atZero X * spec.atZero Y) :=
        congrArg base.tr.toLinearMap (map_mul spec.atZero X Y)
      _ = base.tr.toLinearMap (spec.atZero Y * spec.atZero X) := base.tr.cyclic _ _
      _ = base.tr.toLinearMap (spec.atZero (Y * X)) :=
        congrArg base.tr.toLinearMap (map_mul spec.atZero Y X).symm

theorem sourceTrace_eq : spec.sourceTrace.toLinearMap =
    (spacetimePeriodIntegral par.Lx 0).comp spec.source.model.residue := by
  apply LinearMap.ext
  intro X
  change base.tr.toLinearMap (spec.atZero X) =
    periodicCoefficientIntegral par.Lx (spacetimeSlice par.Lx 0
      (spec.source.model.normal.coefficients X (-1)))
  rw [base.trace_eq, spec.atZero_coefficients]

/-- This is a genuine source derivative, evaluated only after the
epsilon derivative. It is not a proposed spectral Hamiltonian vector. -/
def monodromyFirstVariation : A :=
  spec.atZero (spec.source.model.evolution.toLinearMap (spec.source.factors.monodromy par.M))

theorem euler_pairing (n : ℕ) (hn : 0 < n) :
    ambientPairing par (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n) z) v =
      base.tr.toLinearMap (rationalGradient par.G par.B base.normalized.difference n *
        spec.monodromyFirstVariation) := by
  have h := spec.source.euler_variation_eq_rational_pairing spec.sourceTrace spec.sourceTrace_eq n hn
  change _ = base.tr.toLinearMap (spec.atZero
    (rationalGradient par.G par.B spec.source.normalized.difference n *
      spec.source.model.evolution.toLinearMap (spec.source.factors.monodromy par.M))) at h
  rw [map_mul, spec.rationalGradient_zero] at h
  exact h

end AmbientSpectrumSpecialization

/-- Intermediate transport interface in DLW coordinates. The final
entry point derives it from the static free-factor Adler theorem in
FactorAdlerFoundation, including the 1/8 normalization and projection.
It contains no spectral charge, zero bracket or gradient conclusion. -/
structure AmbientAdlerFoundation {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A) where
  sources : ∀ v : AmbientPeriodicPair par, AmbientSpectrumSpecialization base v
  plus : A →ₗ[ℝ] A
  plus_coefficient : ∀ X e, base.model.coefficients (plus X) e =
    if 0 ≤ e then base.model.coefficients X e else 0
  factor_transport : ∀ (f g : AmbientPeriodicPair par) (X Y : A),
    (∑ j : Fin par.M, f.1 j) = 0 → (∑ j : Fin par.M, g.1 j) = 0 →
    (∀ v, ambientPairing par f v = base.tr.toLinearMap (X * (sources v).monodromyFirstVariation)) →
    (∀ v, ambientPairing par g v = base.tr.toLinearMap (Y * (sources v).monodromyFirstVariation)) →
    ambientConstantBracket par f.1 f.2 g.1 g.2 =
      (1 / 8 : ℝ) * base.tr.toLinearMap (X * adler plus (base.factors.monodromy par.M) Y)

theorem actualAmbientSpectralBracket_zero {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A)
    (foundation : AmbientAdlerFoundation base)
    (ward : ActualSpectralWardFoundation par z) (m n : ℕ) (hm : 0 < m) (hn : 0 < n) :
    ambientConstantBracket par
      (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par m) z).1
      (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par m) z).2
      (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n) z).1
      (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n) z).2 = 0 := by
  rw [foundation.factor_transport _ _
    (rationalGradient par.G par.B base.normalized.difference m)
    (rationalGradient par.G par.B base.normalized.difference n)
    (ambientEulerGradient_U_sum_zero par _ z (actualSpectralCommonWard par z ward m))
    (ambientEulerGradient_U_sum_zero par _ z (actualSpectralCommonWard par z ward n))
    (fun v => (foundation.sources v).euler_pairing m hm)
    (fun v => (foundation.sources v).euler_pairing n hn)]
  have hu : (base.normalized.difference : A) = base.factors.monodromy par.M - 1 :=
    base.normalized.difference_eq.trans (base.factors.monodromyDifference_eq par.M)
  rw [rationalGradients_adler_involution base.tr foundation.plus (base.factors.monodromy par.M)
    par.G par.B base.normalized.difference hu m n, mul_zero]

theorem actualReducedAmbientSpectralBracket_zero {par : FieldParameters} {z : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (base : AmbientSpectrumBase par z A)
    (foundation : AmbientAdlerFoundation base)
    (ward : ActualSpectralWardFoundation par z) (m n : ℕ) (hm : 0 < m) (hn : 0 < n) :
    reducedBracketValue par
      (reducedAmbientEulerGradient par (AmbientPDO.periodicDensityPolynomial par m) z
        (actualSpectralCommonWard par z ward m))
      (reducedAmbientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n) z
        (actualSpectralCommonWard par z ward n)) = 0 := by
  rw [reducedAmbientEulerGradient_bracket_eq]
  exact actualAmbientSpectralBracket_zero base foundation ward m n hm hn

#print axioms AmbientSpectrumSpecialization.euler_pairing
#print axioms actualAmbientSpectralBracket_zero
#print axioms actualReducedAmbientSpectralBracket_zero
end
end DLWLean
