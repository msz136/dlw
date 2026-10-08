import FourierAmplitudeWitness

namespace DLWLean
noncomputable section
open scoped BigOperators

def fieldAmplitudePolynomial (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) : Polynomial ℝ :=
  integrateCoefficientPolynomial (periodicCoefficientIntegral par.Lx)
    (fieldPolynomialLine par p 0 z)

def fieldAmplitudeDifferentialPolynomial (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) : Polynomial ℝ :=
  fieldAmplitudePolynomial par (fieldPolynomialVariation par v p) z

theorem fieldAmplitudePolynomial_eval (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) (eps : ℝ) :
    (fieldAmplitudePolynomial par p z).eval eps = fieldPolynomialIntegral par p (eps • z) := by
  rw [fieldAmplitudePolynomial, integrateCoefficientPolynomial_eval, fieldPolynomialLine_eval]
  simp only [zero_add]
  rfl

theorem fieldAmplitudeDifferentialPolynomial_eval (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) (eps : ℝ) :
    (fieldAmplitudeDifferentialPolynomial par p z v).eval eps =
      fieldPolynomialDifferential par p (eps • z) v :=
  fieldAmplitudePolynomial_eval par (fieldPolynomialVariation par v p) z eps

theorem fieldPolynomialLine_zero_mul_X (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) (i : FieldJetIndex par) :
    fieldPolynomialLine par (p * MvPolynomial.X i) 0 z =
      fieldPolynomialLine par p 0 z * (Polynomial.C (fieldJet par i z) * Polynomial.X) := by
  simp [fieldPolynomialLine]

theorem fieldPolynomialLine_zero_linear_add (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    (fieldPolynomialLine par p 0 (z + v)).coeff 1 =
      (fieldPolynomialLine par p 0 z).coeff 1 + (fieldPolynomialLine par p 0 v).coeff 1 := by
  rw [fieldPolynomialLine_coeff_one, fieldPolynomialLine_coeff_one, fieldPolynomialLine_coeff_one,
    fieldPolynomialVariation_add]
  simp [fieldDifferentialPolynomial]

theorem fieldPolynomialLine_variation_zero_quadratic_polarization (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    (fieldPolynomialLine par (fieldPolynomialVariation par v p) 0 z).coeff 1 =
      (fieldPolynomialLine par p 0 (z + v)).coeff 2 -
        (fieldPolynomialLine par p 0 z).coeff 2 - (fieldPolynomialLine par p 0 v).coeff 2 := by
  induction p using MvPolynomial.induction_on with
  | C r => simp [fieldPolynomialLine]
  | add p q hp hq =>
    simp only [map_add, fieldPolynomialLine, Polynomial.coeff_add] at *
    rw [hp, hq]
    ring
  | mul_X p i _ =>
    have hvariation : fieldPolynomialVariation par v (p * MvPolynomial.X i) =
        fieldPolynomialVariation par v p * MvPolynomial.X i +
          p * MvPolynomial.C (fieldJet par i v) := by
      simp only [Derivation.leibniz, Algebra.smul_def, Algebra.algebraMap_self,
        RingHom.id_apply, fieldPolynomialVariation, MvPolynomial.mkDerivation_X]
      ring
    have hline : fieldPolynomialLine par (fieldPolynomialVariation par v (p * MvPolynomial.X i)) 0 z =
        fieldPolynomialLine par (fieldPolynomialVariation par v p) 0 z *
          (Polynomial.C (fieldJet par i z) * Polynomial.X) +
        fieldPolynomialLine par p 0 z * Polynomial.C (fieldJet par i v) := by
      rw [hvariation]
      simp [fieldPolynomialLine]
    rw [hline]
    rw [Polynomial.coeff_add, ← mul_assoc, Polynomial.coeff_mul_X, Polynomial.coeff_mul_C,
      Polynomial.coeff_mul_C, fieldPolynomialLine_coeff_zero,
      ← fieldPolynomialLine_coeff_one par p 0 v]
    rw [fieldPolynomialLine_zero_mul_X, fieldPolynomialLine_zero_mul_X,
      fieldPolynomialLine_zero_mul_X]
    rw [← mul_assoc, Polynomial.coeff_mul_X, Polynomial.coeff_mul_C,
      ← mul_assoc, Polynomial.coeff_mul_X, Polynomial.coeff_mul_C,
      ← mul_assoc, Polynomial.coeff_mul_X, Polynomial.coeff_mul_C,
      fieldPolynomialLine_zero_linear_add, map_add]
    ring

theorem fieldAmplitudeDifferentialPolynomial_coeff_one (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    (fieldAmplitudeDifferentialPolynomial par p z v).coeff 1 =
      (fieldAmplitudePolynomial par p (z + v)).coeff 2 -
        (fieldAmplitudePolynomial par p z).coeff 2 - (fieldAmplitudePolynomial par p v).coeff 2 := by
  simp only [fieldAmplitudeDifferentialPolynomial, fieldAmplitudePolynomial,
    integrateCoefficientPolynomial_coeff]
  rw [fieldPolynomialLine_variation_zero_quadratic_polarization, map_sub, map_sub]

theorem fieldDifferentialPolynomial_real_zero (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) ℝ) :
    fieldDifferentialPolynomial par
      (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p) 0 =
      algebraMap ℝ (PeriodicCoefficient par.Lx) (MvPolynomial.eval (fun _ => 0) p) := by
  induction p using MvPolynomial.induction_on with
  | C r => simp [fieldDifferentialPolynomial]
  | add p q hp hq => simpa only [map_add, fieldDifferentialPolynomial, MvPolynomial.eval_add] using congrArg₂ (· + ·) hp hq
  | mul_X p i hp =>
    simp only [map_mul, MvPolynomial.map_X, fieldDifferentialPolynomial,
      MvPolynomial.eval_mul, MvPolynomial.eval_X, map_zero, mul_zero]

theorem fieldPolynomialDifferential_real_zero_of_zero_jet_integrals (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) ℝ) (v : ClosedPeriodicPair par)
    (hjets : ∀ i, periodicCoefficientIntegral par.Lx (fieldJet par i v) = 0) :
    fieldPolynomialDifferential par
      (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p) 0 v = 0 := by
  change periodicCoefficientIntegral par.Lx (fieldDifferentialPolynomial par
    (fieldPolynomialVariation par v (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) 0) = 0
  induction p using MvPolynomial.induction_on with
  | C r => simp [fieldDifferentialPolynomial]
  | add p q hp hq =>
    simp only [map_add, fieldDifferentialPolynomial, MvPolynomial.eval_add] at *
    rw [hp, hq, add_zero]
  | mul_X p i _ =>
    rw [map_mul, MvPolynomial.map_X, Derivation.leibniz]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      fieldDifferentialPolynomial, MvPolynomial.eval_add, MvPolynomial.eval_mul,
      MvPolynomial.eval_X, map_zero, mul_zero, zero_add]
    rw [show fieldPolynomialVariation par v (MvPolynomial.X i) =
        MvPolynomial.C (fieldJet par i v) from MvPolynomial.mkDerivation_X _ _ i,
      MvPolynomial.eval_C]
    simp only [zero_mul, add_zero]
    have heval := fieldDifferentialPolynomial_real_zero par p
    simp only [fieldDifferentialPolynomial, map_zero] at heval
    rw [heval]
    change periodicCoefficientIntegral par.Lx
      (MvPolynomial.eval (fun _ => 0) p • fieldJet par i v) = 0
    rw [map_smul, hjets, smul_zero]

theorem fieldAmplitudeDifferentialPolynomial_real_coeff_zero (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) ℝ) (z v : ClosedPeriodicPair par)
    (hjets : ∀ i, periodicCoefficientIntegral par.Lx (fieldJet par i v) = 0) :
    (fieldAmplitudeDifferentialPolynomial par
      (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p) z v).coeff 0 = 0 := by
  simp only [fieldAmplitudeDifferentialPolynomial, fieldAmplitudePolynomial,
    integrateCoefficientPolynomial_coeff, fieldPolynomialLine_coeff_zero]
  exact fieldPolynomialDifferential_real_zero_of_zero_jet_integrals par p v hjets

#print axioms fieldAmplitudeDifferentialPolynomial_eval
#print axioms fieldAmplitudeDifferentialPolynomial_coeff_one
#print axioms fieldAmplitudeDifferentialPolynomial_real_coeff_zero
end
end DLWLean
