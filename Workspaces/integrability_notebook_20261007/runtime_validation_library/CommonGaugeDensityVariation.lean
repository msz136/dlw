import ActualCommonGaugeSource
import AmbientNormalizedRealization
import PolynomialReductionEndpoint

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

theorem smoothStaticCoefficient_space {Lx : ℝ} (f : PeriodicCoefficient Lx) :
    smoothSpacetimeSpaceEvolution.toLinearMap (smoothStaticCoefficient f) =
      smoothStaticCoefficient ((periodicSpatialEvolution Lx).toLinearMap f) := by
  apply Subtype.ext
  funext tx
  rfl

theorem smoothCommonUCoefficient_space {Lx : ℝ} (f a : PeriodicCoefficient Lx) :
    smoothSpacetimeSpaceEvolution.toLinearMap (smoothCommonUCoefficient f a) =
      smoothCommonUCoefficient ((periodicSpatialEvolution Lx).toLinearMap f)
        ((periodicSpatialEvolution Lx).toLinearMap a) := by
  apply Subtype.ext
  funext tx
  change deriv (fun x => (f : ℝ → ℝ) x + tx.1 * (a : ℝ → ℝ) x) tx.2 =
    deriv (f : ℝ → ℝ) tx.2 + tx.1 * deriv (a : ℝ → ℝ) tx.2
  exact (((f.property.1.differentiable (by simp) tx.2).hasDerivAt).add
    (((a.property.1.differentiable (by simp) tx.2).hasDerivAt).const_mul tx.1)).deriv

theorem smoothCommonUCoefficient_iterate {Lx : ℝ} (f a : PeriodicCoefficient Lx) (n : ℕ) :
    (smoothSpacetimeSpaceEvolution.toLinearMap)^[n] (smoothCommonUCoefficient f a) =
      smoothCommonUCoefficient (periodicSpatialIterate n f) (periodicSpatialIterate n a) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih, smoothCommonUCoefficient_space]
    simp only [periodicSpatialIterate, Function.iterate_succ_apply']

theorem smoothStaticCoefficient_iterate {Lx : ℝ} (f : PeriodicCoefficient Lx) (n : ℕ) :
    (smoothSpacetimeSpaceEvolution.toLinearMap)^[n] (smoothStaticCoefficient f) =
      smoothStaticCoefficient (periodicSpatialIterate n f) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih, smoothStaticCoefficient_space]
    simp only [periodicSpatialIterate, Function.iterate_succ_apply']

def commonGaugeJetSource (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (i : AmbientJetIndex par) : SmoothSpacetimeCoefficient :=
  (smoothSpacetimeSpaceEvolution.toLinearMap)^[i.2.2]
    (if i.1 then smoothCommonUCoefficient (z.1 i.2.1) a
      else smoothStaticCoefficient (z.2 i.2.1))

def commonGaugePolynomialEvaluation (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) :
    AmbientPDO.Poly par →ₐ[ℝ] SmoothSpacetimeCoefficient :=
  MvPolynomial.aeval (commonGaugeJetSource par z a)

theorem commonGaugeJetSource_next (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (i : AmbientJetIndex par) :
    commonGaugeJetSource par z a (i.1, i.2.1, i.2.2 + 1) =
      smoothSpacetimeSpaceEvolution.toLinearMap (commonGaugeJetSource par z a i) := by
  exact Function.iterate_succ_apply' _ i.2.2 _

theorem commonGaugePolynomialEvaluation_spatial (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (p : AmbientPDO.Poly par) :
    commonGaugePolynomialEvaluation par z a (AmbientPDO.spatialDerivative par p) =
      smoothSpacetimeSpaceEvolution.toLinearMap (commonGaugePolynomialEvaluation par z a p) := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero, AmbientPDO.polynomialEvaluation_C]
    symm
    exact evolution_algebraMap_zero _ r
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p i hp =>
    rw [Derivation.leibniz]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply, map_add,
      map_mul, commonGaugePolynomialEvaluation, MvPolynomial.aeval_X,
      smoothSpacetimeSpaceEvolution.leibniz]
    have hXi : AmbientPDO.spatialDerivative par (MvPolynomial.X i) =
        AmbientPDO.generatorDerivative par i := MvPolynomial.mkDerivation_X _ _ _
    rw [hXi]
    simp only [AmbientPDO.generatorDerivative, MvPolynomial.aeval_X, commonGaugeJetSource_next]
    change _ = (smoothSpacetimeSpaceEvolution.toLinearMap
      (commonGaugePolynomialEvaluation par z a p)) * commonGaugeJetSource par z a i +
      (commonGaugePolynomialEvaluation par z a p) *
        smoothSpacetimeSpaceEvolution.toLinearMap (commonGaugeJetSource par z a i)
    rw [← hp]
    dsimp only [commonGaugePolynomialEvaluation]
    ring

theorem commonGaugeJetSource_value (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (i : AmbientJetIndex par) (t x : ℝ) :
    (commonGaugeJetSource par z a i : ℝ × ℝ → ℝ) (t, x) =
      (ambientJet par i (z + t • ((fun _ => a), 0)) : ℝ → ℝ) x := by
  obtain ⟨b, j, n⟩ := i
  cases b
  · simp only [commonGaugeJetSource, Bool.false_eq_true, ↓reduceIte, smoothStaticCoefficient_iterate]
    change (periodicSpatialIterate n (z.2 j) : ℝ → ℝ) x =
      (ambientSpatialJet par n (z.2 j + t • (0 : PeriodicCoefficient par.Lx)) : ℝ → ℝ) x
    rw [smul_zero, add_zero, ambientSpatialJet_eq_iterate]
  · simp only [commonGaugeJetSource, ↓reduceIte, smoothCommonUCoefficient_iterate]
    change (periodicSpatialIterate n (z.1 j) : ℝ → ℝ) x +
        t * (periodicSpatialIterate n a : ℝ → ℝ) x =
      (ambientSpatialJet par n (z.1 j + t • a) : ℝ → ℝ) x
    rw [map_add, map_smul, ambientSpatialJet_eq_iterate, ambientSpatialJet_eq_iterate]
    rfl

theorem commonGaugePolynomialEvaluation_value (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (p : AmbientPDO.Poly par) (t x : ℝ) :
    (commonGaugePolynomialEvaluation par z a p : ℝ × ℝ → ℝ) (t, x) =
      (ambientPolynomialValue par (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)
        (z + t • ((fun _ => a), 0)) : ℝ → ℝ) x := by
  induction p using MvPolynomial.induction_on with
  | C r => simp [commonGaugePolynomialEvaluation, ambientPolynomialValue]
  | add p q hp hq =>
    simp only [map_add, Subalgebra.coe_add, Pi.add_apply, ambientPolynomialValue] at *
    rw [hp, hq]
  | mul_X p i hp =>
    simp only [map_mul, MvPolynomial.map_X, commonGaugePolynomialEvaluation,
      MvPolynomial.aeval_X, Subalgebra.coe_mul, Pi.mul_apply, ambientPolynomialValue,
      MvPolynomial.eval_mul, MvPolynomial.eval_X]
    rw [commonGaugeJetSource_value]
    exact congrArg (fun y : ℝ => y *
      (ambientJet par i (z + t • ((fun _ => a), 0)) : ℝ → ℝ) x) hp

/-- The actual time derivative of the smooth common-U source density
is exactly the genuine ambient polynomial first variation at epsilon=0. -/
theorem commonGaugePolynomialEvaluation_time_value (par : FieldParameters)
    (z : AmbientPeriodicPair par) (a : PeriodicCoefficient par.Lx) (p : AmbientPDO.Poly par)
    (x : ℝ) :
    (smoothSpacetimeTimeEvolution.toLinearMap (commonGaugePolynomialEvaluation par z a p) :
      ℝ × ℝ → ℝ) (0, x) =
      (ambientPolynomialValue par
        (ambientPolynomialVariation par ((fun _ => a), 0)
          (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) z : ℝ → ℝ) x := by
  let q := MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p
  have h := linear_polynomial_evaluation_hasDerivAt_zero
    (coefficientEvaluation par.Lx x).toLinearMap
    (ambientPolynomialLine par q z ((fun _ => a), 0))
  rw [ambientPolynomialLine_coeff_one] at h
  change HasDerivAt
    (fun t : ℝ => (coefficientEvaluation par.Lx x)
      ((ambientPolynomialLine par q z ((fun _ => a), 0)).eval
        (algebraMap ℝ (PeriodicCoefficient par.Lx) t)))
    ((coefficientEvaluation par.Lx x)
      (ambientPolynomialValue par (ambientPolynomialVariation par ((fun _ => a), 0) q) z)) 0 at h
  have hf : (fun t : ℝ => (commonGaugePolynomialEvaluation par z a p : ℝ × ℝ → ℝ) (t, x)) =
      (fun t : ℝ => (coefficientEvaluation par.Lx x)
        ((ambientPolynomialLine par q z ((fun _ => a), 0)).eval
          (algebraMap ℝ (PeriodicCoefficient par.Lx) t))) := by
    funext t
    rw [ambientPolynomialLine_eval]
    exact commonGaugePolynomialEvaluation_value par z a p t x
  rw [← hf] at h
  exact h.deriv

#print axioms commonGaugePolynomialEvaluation_spatial
#print axioms commonGaugePolynomialEvaluation_time_value
end
end DLWLean
