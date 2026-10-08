import AmbientEulerVariational

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem mvPolynomial_substitution_coeff_zero {R σ : Type*} [CommRing R]
    (p : MvPolynomial σ R) (P : σ → Polynomial R) :
    (MvPolynomial.eval₂Hom Polynomial.C P p).coeff 0 =
      MvPolynomial.eval (fun i => (P i).coeff 0) p := by
  have h := MvPolynomial.map_eval₂Hom Polynomial.C P Polynomial.constantCoeff p
  have hC : Polynomial.constantCoeff.comp (Polynomial.C : R →+* Polynomial R) = RingHom.id R := by
    ext r
    simp [Polynomial.constantCoeff]
  rw [hC] at h
  exact h

/-- The first coefficient of an arbitrary polynomial substitution depends
only on the zeroth and first coefficients of the substituted coordinates. -/
theorem mvPolynomial_substitution_coeff_one {R σ : Type*} [CommRing R]
    (p : MvPolynomial σ R) (P : σ → Polynomial R) :
    (MvPolynomial.eval₂Hom Polynomial.C P p).coeff 1 =
      MvPolynomial.eval (fun i => (P i).coeff 0)
        (MvPolynomial.mkDerivation R (fun i => MvPolynomial.C ((P i).coeff 1)) p) := by
  induction p using MvPolynomial.induction_on with
  | C r => simp
  | add p q hp hq =>
    simp only [map_add, Polynomial.coeff_add]
    rw [hp, hq]
  | mul_X p i hp =>
    rw [map_mul, MvPolynomial.eval₂Hom_X', Polynomial.mul_coeff_one,
      mvPolynomial_substitution_coeff_zero, hp]
    simp only [Derivation.leibniz, smul_eq_mul, MvPolynomial.mkDerivation_X,
      MvPolynomial.eval_add, MvPolynomial.eval_mul, MvPolynomial.eval_X, MvPolynomial.eval_C]
    ring

def coordinateAmbient {par : FieldParameters} (z : FieldCoordinates par) : AmbientPeriodicPair par :=
  (z.UCoefficient, z.wCoefficient)

def coordinateAmbientTangent {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) : AmbientPeriodicPair par := (coordinateUTangent z v, v.2)

def ambientChartJetPolynomial {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (i : AmbientJetIndex par) : Polynomial (PeriodicCoefficient par.Lx) :=
  if i.1 then
    quadraticCoefficientPolynomial
      (ambientSpatialJet par i.2.2 (z.UCoefficient i.2.1))
      (ambientSpatialJet par i.2.2 (coordinateUTangent z v i.2.1))
      (ambientSpatialJet par i.2.2 (coordinateUQuadratic par v))
  else
    linearCoefficientPolynomial
      (ambientSpatialJet par i.2.2 (z.wCoefficient i.2.1))
      (ambientSpatialJet par i.2.2 (v.2 i.2.1))

theorem ambientChartJetPolynomial_eval {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (i : AmbientJetIndex par) (t : ℝ) :
    (ambientChartJetPolynomial z v i).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t) =
      ambientJet par i (coordinateAmbient
        (closedPairCoordinates par ((z.closedP, z.closedS) + t • v))) := by
  obtain ⟨b, j, n⟩ := i
  cases b
  · change (linearCoefficientPolynomial _ _).eval _ =
      ambientSpatialJet par n
        ((closedPairCoordinates par ((z.closedP, z.closedS) + t • v)).wCoefficient j)
    rw [coordinateLine_w_polynomial, linearCoefficientPolynomial_eval,
      linearCoefficientPolynomial_eval, map_add, map_smul]
  · change (quadraticCoefficientPolynomial _ _ _).eval _ =
      ambientSpatialJet par n
        ((closedPairCoordinates par ((z.closedP, z.closedS) + t • v)).UCoefficient j)
    rw [coordinateLine_U_polynomial, quadraticCoefficientPolynomial_eval,
      quadraticCoefficientPolynomial_eval, map_add, map_add, map_smul, map_smul]

theorem ambientChartJetPolynomial_coeff_zero {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (i : AmbientJetIndex par) :
    (ambientChartJetPolynomial z v i).coeff 0 = ambientJet par i (coordinateAmbient z) := by
  obtain ⟨b, j, n⟩ := i
  cases b <;>
    simp [ambientChartJetPolynomial, quadraticCoefficientPolynomial, linearCoefficientPolynomial,
      ambientJet, ambientComponent, coordinateAmbient]

theorem ambientChartJetPolynomial_coeff_one {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (i : AmbientJetIndex par) :
    (ambientChartJetPolynomial z v i).coeff 1 =
      ambientJet par i (coordinateAmbientTangent z v) := by
  obtain ⟨b, j, n⟩ := i
  cases b <;>
    simp [ambientChartJetPolynomial, quadraticCoefficientPolynomial, linearCoefficientPolynomial,
      Polynomial.coeff_monomial, ambientJet, ambientComponent, coordinateAmbientTangent]

def ambientChartPolynomial {par : FieldParameters}
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : FieldCoordinates par) (v : ClosedPeriodicPair par) : Polynomial (PeriodicCoefficient par.Lx) :=
  MvPolynomial.eval₂Hom Polynomial.C (ambientChartJetPolynomial z v) p

theorem ambientChartPolynomial_eval {par : FieldParameters}
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : FieldCoordinates par) (v : ClosedPeriodicPair par) (t : ℝ) :
    (ambientChartPolynomial p z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t) =
      ambientPolynomialValue par p (coordinateAmbient
        (closedPairCoordinates par ((z.closedP, z.closedS) + t • v))) := by
  have h := MvPolynomial.map_eval₂Hom Polynomial.C (ambientChartJetPolynomial z v)
    (Polynomial.evalRingHom (algebraMap ℝ (PeriodicCoefficient par.Lx) t)) p
  have hC : (Polynomial.evalRingHom (algebraMap ℝ (PeriodicCoefficient par.Lx) t)).comp
      Polynomial.C = RingHom.id _ := by ext r; simp
  rw [hC] at h
  simpa only [ambientChartPolynomial, Polynomial.coe_evalRingHom,
    ambientChartJetPolynomial_eval, ambientPolynomialValue, MvPolynomial.eval] using h

theorem ambientChartPolynomial_coeff_one {par : FieldParameters}
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : FieldCoordinates par) (v : ClosedPeriodicPair par) :
    (ambientChartPolynomial p z v).coeff 1 =
      ambientPolynomialValue par
        (ambientPolynomialVariation par (coordinateAmbientTangent z v) p) (coordinateAmbient z) := by
  rw [ambientChartPolynomial, mvPolynomial_substitution_coeff_one]
  simp only [ambientChartJetPolynomial_coeff_zero, ambientChartJetPolynomial_coeff_one]
  rfl

/-- Actual first variation along the nonlinear physical coordinate chart,
including its quadratic U correction. -/
theorem ambientPolynomialIntegral_hasDerivAt_coordinateLine {par : FieldParameters}
    (p : MvPolynomial (AmbientJetIndex par) (PeriodicCoefficient par.Lx))
    (z : FieldCoordinates par) (v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => ambientPolynomialIntegral par p (coordinateAmbient
      (closedPairCoordinates par ((z.closedP, z.closedS) + t • v))))
      (ambientPairing par (ambientEulerGradient par p (coordinateAmbient z))
        (coordinateAmbientTangent z v)) 0 := by
  rw [ambientEulerGradient_pairing]
  have h := linear_polynomial_evaluation_hasDerivAt_zero
    (periodicCoefficientIntegral par.Lx) (ambientChartPolynomial p z v)
  rw [ambientChartPolynomial_coeff_one] at h
  have hf : (fun t : ℝ => ambientPolynomialIntegral par p (coordinateAmbient
      (closedPairCoordinates par ((z.closedP, z.closedS) + t • v)))) =
      (fun t : ℝ => periodicCoefficientIntegral par.Lx
        ((ambientChartPolynomial p z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t))) := by
    funext t
    rw [ambientChartPolynomial_eval]
    rfl
  rw [hf]
  exact h

#print axioms mvPolynomial_substitution_coeff_one
#print axioms ambientPolynomialIntegral_hasDerivAt_coordinateLine
end
end DLWLean
