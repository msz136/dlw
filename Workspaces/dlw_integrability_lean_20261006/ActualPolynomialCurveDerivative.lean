import PeriodicMixedDerivatives
import ActualHamiltonianFlow
import EulerVariationalGradient

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

def periodicStaticSpacetimeHom (Lx : ℝ) :
    PeriodicCoefficient Lx →ₐ[ℝ] PeriodicSpacetimeCoefficient Lx where
  toFun f := ⟨fun tx => (f : ℝ → ℝ) tx.2, f.property.1.comp contDiff_snd,
    fun _ => f.property.2⟩
  map_zero' := rfl
  map_one' := rfl
  map_add' _ _ := rfl
  map_mul' _ _ := rfl
  commutes' _ := rfl

theorem periodicStaticSpacetimeHom_time_zero {Lx : ℝ} (f : PeriodicCoefficient Lx) :
    (periodicSpacetimeTimeEvolution Lx).toLinearMap (periodicStaticSpacetimeHom Lx f) = 0 := by
  apply Subtype.ext
  funext tx
  change deriv (fun _ : ℝ => (f : ℝ → ℝ) tx.2) tx.1 = 0
  simp

theorem spacetimeSlice_spatial {Lx : ℝ} (f : PeriodicSpacetimeCoefficient Lx) (t : ℝ) :
    spacetimeSlice Lx t ((periodicSpacetimeSpaceEvolution Lx).toLinearMap f) =
      (periodicSpatialEvolution Lx).toLinearMap (spacetimeSlice Lx t f) := rfl

theorem spacetimeSlice_spatial_iterate (par : FieldParameters)
    (f : PeriodicSpacetimeCoefficient par.Lx) (t : ℝ) (k : ℕ) :
    spacetimeSlice par.Lx t (((periodicSpacetimeSpaceEvolution par.Lx).toLinearMap)^[k] f) =
      coefficientSpatialJet par k (spacetimeSlice par.Lx t f) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', spacetimeSlice_spatial, ih]
    rfl

def StartPoint.closedCurve {par : FieldParameters} (start : StartPoint par) (t : ℝ) :
    ClosedPeriodicPair par := ((start.trajectory t).closedP, (start.trajectory t).closedS)

def StartPoint.actualVelocity {par : FieldParameters} (start : StartPoint par) (t : ℝ) :
    ClosedPeriodicPair par := reducedHamiltonianVector par (physicalKGradient (start.trajectory t))

def StartPoint.coordinateSpacetimeSource {par : FieldParameters} (start : StartPoint par)
    (b : Bool) (j : Fin par.M) : PeriodicSpacetimeCoefficient par.Lx :=
  if b then
    ⟨fun tx => (start.trajectory tx.1).p.value j tx.2, start.joint_smooth_p j,
      fun t => (start.trajectory t).p.periodic j⟩
  else
    ⟨fun tx => (start.trajectory tx.1).s.value j tx.2, start.joint_smooth_s j,
      fun t => (start.trajectory t).s.periodic j⟩

def StartPoint.fieldJetSource {par : FieldParameters} (start : StartPoint par)
    (i : FieldJetIndex par) : PeriodicSpacetimeCoefficient par.Lx :=
  ((periodicSpacetimeSpaceEvolution par.Lx).toLinearMap)^[i.2.2]
    (start.coordinateSpacetimeSource i.1 i.2.1)

theorem StartPoint.coordinateSource_slice {par : FieldParameters} (start : StartPoint par)
    (b : Bool) (j : Fin par.M) (t : ℝ) :
    spacetimeSlice par.Lx t (start.coordinateSpacetimeSource b j) =
      closedPairComponent par b j (start.closedCurve t) := by
  cases b <;> rfl

theorem StartPoint.coordinateSource_time_slice {par : FieldParameters} (start : StartPoint par)
    (b : Bool) (j : Fin par.M) (t : ℝ) :
    spacetimeSlice par.Lx t ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap
      (start.coordinateSpacetimeSource b j)) =
      closedPairComponent par b j (start.actualVelocity t) := by
  apply Subtype.ext
  funext x
  cases b
  · exact (start.physicalK_generates_coordinates t x j).2.symm
  · exact (start.physicalK_generates_coordinates t x j).1.symm

theorem StartPoint.fieldJetSource_slice {par : FieldParameters} (start : StartPoint par)
    (i : FieldJetIndex par) (t : ℝ) :
    spacetimeSlice par.Lx t (start.fieldJetSource i) = fieldJet par i (start.closedCurve t) := by
  rw [StartPoint.fieldJetSource, spacetimeSlice_spatial_iterate, start.coordinateSource_slice]
  rfl

theorem StartPoint.fieldJetSource_time_slice {par : FieldParameters} (start : StartPoint par)
    (i : FieldJetIndex par) (t : ℝ) :
    spacetimeSlice par.Lx t ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap (start.fieldJetSource i)) =
      fieldJet par i (start.actualVelocity t) := by
  rw [StartPoint.fieldJetSource, periodicSpacetimeTimeSpace_iterate,
    spacetimeSlice_spatial_iterate, start.coordinateSource_time_slice]
  rfl

def StartPoint.fieldCurveEvaluation {par : FieldParameters} (start : StartPoint par) :
    MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx) →+*
      PeriodicSpacetimeCoefficient par.Lx :=
  MvPolynomial.eval₂Hom (periodicStaticSpacetimeHom par.Lx).toRingHom start.fieldJetSource

theorem StartPoint.fieldCurveEvaluation_C {par : FieldParameters} (start : StartPoint par)
    (r : PeriodicCoefficient par.Lx) :
    start.fieldCurveEvaluation (MvPolynomial.C r) = periodicStaticSpacetimeHom par.Lx r := by
  simp [StartPoint.fieldCurveEvaluation]

theorem StartPoint.fieldCurveEvaluation_X {par : FieldParameters} (start : StartPoint par)
    (i : FieldJetIndex par) : start.fieldCurveEvaluation (MvPolynomial.X i) = start.fieldJetSource i := by
  simp [StartPoint.fieldCurveEvaluation]

theorem StartPoint.fieldCurveEvaluation_value {par : FieldParameters} (start : StartPoint par)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) (t x : ℝ) :
    (start.fieldCurveEvaluation p : ℝ × ℝ → ℝ) (t, x) =
      (fieldDifferentialPolynomial par p (start.closedCurve t) : ℝ → ℝ) x := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [start.fieldCurveEvaluation_C]
    simp only [fieldDifferentialPolynomial, MvPolynomial.eval_C]
    rfl
  | add p q hp hq =>
    simp only [map_add, Subalgebra.coe_add, Pi.add_apply, fieldDifferentialPolynomial] at *
    rw [hp, hq]
  | mul_X p i hp =>
    rw [map_mul, start.fieldCurveEvaluation_X]
    simp only [Subalgebra.coe_mul, Pi.mul_apply, fieldDifferentialPolynomial, MvPolynomial.eval_mul,
      MvPolynomial.eval_X]
    rw [hp]
    have hi := congrArg (fun f : PeriodicCoefficient par.Lx => (f : ℝ → ℝ) x)
      (start.fieldJetSource_slice i t)
    exact congrArg (fun y : ℝ => (fieldDifferentialPolynomial par p (start.closedCurve t) : ℝ → ℝ) x * y) hi

theorem StartPoint.fieldCurveEvaluation_time_value {par : FieldParameters} (start : StartPoint par)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) (t x : ℝ) :
    ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap (start.fieldCurveEvaluation p) : ℝ × ℝ → ℝ) (t, x) =
      (fieldDifferentialPolynomial par (fieldPolynomialVariation par (start.actualVelocity t) p)
        (start.closedCurve t) : ℝ → ℝ) x := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [start.fieldCurveEvaluation_C, periodicStaticSpacetimeHom_time_zero, MvPolynomial.derivation_C]
    simp [fieldDifferentialPolynomial]
  | add p q hp hq =>
    simp only [map_add, Subalgebra.coe_add, Pi.add_apply, fieldDifferentialPolynomial] at *
    rw [hp, hq]
  | mul_X p i hp =>
    rw [map_mul, start.fieldCurveEvaluation_X, (periodicSpacetimeTimeEvolution par.Lx).leibniz,
      Derivation.leibniz]
    simp only [Subalgebra.coe_add, Subalgebra.coe_mul, Pi.add_apply, Pi.mul_apply,
      Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      fieldDifferentialPolynomial, MvPolynomial.eval_add, MvPolynomial.eval_mul,
      MvPolynomial.eval_X, fieldPolynomialVariation, MvPolynomial.mkDerivation_X,
      MvPolynomial.eval_C]
    rw [hp, start.fieldCurveEvaluation_value]
    have hi := congrArg (fun f : PeriodicCoefficient par.Lx => (f : ℝ → ℝ) x)
      (start.fieldJetSource_slice i t)
    have ht := congrArg (fun f : PeriodicCoefficient par.Lx => (f : ℝ → ℝ) x)
      (start.fieldJetSource_time_slice i t)
    change (start.fieldJetSource i : ℝ × ℝ → ℝ) (t, x) = _ at hi
    change ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap (start.fieldJetSource i) :
      ℝ × ℝ → ℝ) (t, x) = _ at ht
    rw [hi, ht]
    simp only [fieldDifferentialPolynomial, fieldPolynomialVariation]
    ring

/-- Genuine ordinary time derivative of every finite differential
polynomial integral along the actual physical trajectory. -/
theorem StartPoint.fieldPolynomialIntegral_hasDerivAt {par : FieldParameters} (start : StartPoint par)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) (t : ℝ) :
    HasDerivAt (fun τ : ℝ => fieldPolynomialIntegral par p (start.closedCurve τ))
      (fieldPolynomialDifferential par p (start.closedCurve t) (start.actualVelocity t)) t := by
  have h := spacetimePeriodIntegral_hasDerivAt par.Lx par.Lx_pos (start.fieldCurveEvaluation p) t
  have hfun : (fun τ : ℝ => spacetimePeriodIntegral par.Lx τ (start.fieldCurveEvaluation p)) =
      (fun τ : ℝ => fieldPolynomialIntegral par p (start.closedCurve τ)) := by
    funext τ
    unfold spacetimePeriodIntegral fieldPolynomialIntegral
    change periodicCoefficientIntegral par.Lx (spacetimeSlice par.Lx τ (start.fieldCurveEvaluation p)) = _
    congr 1
    apply Subtype.ext
    funext x
    exact start.fieldCurveEvaluation_value p τ x
  have hrate : spacetimePeriodIntegral par.Lx t
      ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap (start.fieldCurveEvaluation p)) =
      fieldPolynomialDifferential par p (start.closedCurve t) (start.actualVelocity t) := by
    change spacetimePeriodIntegral par.Lx t
      ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap (start.fieldCurveEvaluation p)) =
      fieldPolynomialIntegral par (fieldPolynomialVariation par (start.actualVelocity t) p)
        (start.closedCurve t)
    unfold spacetimePeriodIntegral fieldPolynomialIntegral
    change periodicCoefficientIntegral par.Lx (spacetimeSlice par.Lx t
      ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap (start.fieldCurveEvaluation p))) = _
    congr 1
    apply Subtype.ext
    funext x
    exact start.fieldCurveEvaluation_time_value p t x
  rw [hfun, hrate] at h
  exact h

theorem StartPoint.fieldEulerGradient_time_pairing {par : FieldParameters} (start : StartPoint par)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx)) (t : ℝ) :
    HasDerivAt (fun τ : ℝ => fieldPolynomialIntegral par p (start.closedCurve τ))
      (coefficientGradientPairing par (fieldEulerGradient par p (start.closedCurve t))
        (start.actualVelocity t)) t := by
  rw [fieldEulerGradient_pairing]
  exact start.fieldPolynomialIntegral_hasDerivAt p t

#print axioms StartPoint.fieldJetSource_time_slice
#print axioms StartPoint.fieldPolynomialIntegral_hasDerivAt
#print axioms StartPoint.fieldEulerGradient_time_pairing
end
end DLWLean
