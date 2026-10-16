import GlobalCoefficientRecurrence
import EulerVariationalGradient

namespace DLWLean
noncomputable section
open scoped BigOperators

def closedTranslationDirection (par : FieldParameters) (z : ClosedPeriodicPair par) :
    ClosedPeriodicPair par := (closedSpatialDerivative par z.1, closedSpatialDerivative par z.2)

theorem fieldJet_translation (par : FieldParameters) (z : ClosedPeriodicPair par)
    (i : FieldJetIndex par) :
    fieldJet par i (closedTranslationDirection par z) =
      fieldJet par (i.1, i.2.1, i.2.2 + 1) z := by
  obtain ⟨b, j, n⟩ := i
  cases b <;>
    change coefficientSpatialJet par n
      ((periodicSpatialEvolution par.Lx).toLinearMap _) = coefficientSpatialJet par (n + 1) _
  all_goals
    rw [coefficientSpatialJet_eq_iterate, coefficientSpatialJet_eq_iterate]
    exact (Function.iterate_succ_apply _ n _).symm

theorem coefficientGradientPairing_neg_right (par : FieldParameters)
    (f v : ClosedPeriodicPair par) :
    coefficientGradientPairing par f (-v) = -coefficientGradientPairing par f v := by
  simp only [coefficientGradientPairing, Prod.fst_neg, Prod.snd_neg, coefficientPairing_neg_right]
  ring

namespace GlobalPDO

theorem evaluation_eq_mapped_fieldPolynomial (par : FieldParameters) (z : ClosedPeriodicPair par)
    (p : Poly par) :
    fieldDifferentialPolynomial par (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p) z =
      evaluation par z p := by
  unfold fieldDifferentialPolynomial evaluation
  rw [← MvPolynomial.eval₂_eq_eval_map]
  rfl

/-- The actual direction derivative of a constant-coefficient local
polynomial under spatial translation is its spatial total derivative. -/
theorem translation_variation_evaluation (par : FieldParameters) (z : ClosedPeriodicPair par)
    (p : Poly par) :
    fieldDifferentialPolynomial par
      (fieldPolynomialVariation par (closedTranslationDirection par z)
        (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) z =
      evaluation par z (spatialDerivative par p) := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    simp [fieldDifferentialPolynomial, spatialDerivative]
  | add p q hp hq =>
    simp only [map_add, fieldDifferentialPolynomial] at *
    rw [hp, hq]
  | mul_X p i hp =>
    rw [map_mul, MvPolynomial.map_X, Derivation.leibniz]
    simp only [fieldDifferentialPolynomial, Algebra.smul_def, Algebra.algebraMap_self,
      RingHom.id_apply, map_add, map_mul, MvPolynomial.eval_X, fieldPolynomialVariation,
      MvPolynomial.mkDerivation_X, MvPolynomial.eval_C]
    have hmap : MvPolynomial.eval (fun i => fieldJet par i z)
        (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p) =
          evaluation par z p := evaluation_eq_mapped_fieldPolynomial par z p
    rw [hmap]
    change (evaluation par z p) * fieldJet par i (closedTranslationDirection par z) +
      fieldJet par i z *
        fieldDifferentialPolynomial par
          (fieldPolynomialVariation par (closedTranslationDirection par z)
            (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) z = _
    rw [hp, fieldJet_translation]
    rw [Derivation.leibniz]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply, map_add,
      map_mul, evaluation_X, spatialDerivative, MvPolynomial.mkDerivation_X,
      generatorDerivative, evaluation_X]

theorem translation_variation_integral_zero (par : FieldParameters) (z : ClosedPeriodicPair par)
    (p : Poly par) :
    fieldPolynomialIntegral par
      (fieldPolynomialVariation par (closedTranslationDirection par z)
        (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) z = 0 := by
  unfold fieldPolynomialIntegral
  rw [translation_variation_evaluation, evaluation_derivative,
    periodicCoefficientIntegral_space_zero]

def constructedChargeGradient (par : FieldParameters) (n : ℕ) (z : ClosedPeriodicPair par) :
    ClosedPeriodicPair par := fieldEulerGradient par (periodicDensityPolynomial par n) z

theorem constructedChargeGradient_hasDerivAt (par : FieldParameters) (n : ℕ)
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => constructedCharge par n (z + t • v))
      (coefficientGradientPairing par (constructedChargeGradient par n z) v) 0 :=
  fieldEulerGradient_hasDerivAt par (periodicDensityPolynomial par n) z v

/-- The actual reduced bracket with the physical translation momentum
vanishes for every constructed charge and every closed periodic field. -/
theorem constructedCharge_bracket_momentum_zero (par : FieldParameters) (n : ℕ)
    (z : ClosedPeriodicPair par) :
    reducedBracketValue par (constructedChargeGradient par n z) (momentumGradient z) = 0 := by
  change coefficientGradientPairing par (constructedChargeGradient par n z)
      (-closedTranslationDirection par z) = 0
  rw [coefficientGradientPairing_neg_right]
  unfold constructedChargeGradient
  rw [fieldEulerGradient_pairing]
  change -fieldPolynomialIntegral par
      (fieldPolynomialVariation par (closedTranslationDirection par z)
        (periodicDensityPolynomial par n)) z = 0
  rw [periodicDensityPolynomial, translation_variation_integral_zero, neg_zero]

#print axioms translation_variation_evaluation
#print axioms constructedChargeGradient_hasDerivAt
#print axioms constructedCharge_bracket_momentum_zero
end GlobalPDO
end
end DLWLean
