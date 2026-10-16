import AmbientNormalizedRealization
import ActualTraceDerivative
import PolynomialReductionEndpoint
import SpectralVariation

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

/-- The actual affine periodic source f(x)+epsilon v(x). -/
def periodicAffineCoefficient {Lx : ℝ} (f v : PeriodicCoefficient Lx) :
    PeriodicSpacetimeCoefficient Lx :=
  ⟨fun tx => (f : ℝ → ℝ) tx.2 + tx.1 * (v : ℝ → ℝ) tx.2,
    (f.property.1.comp contDiff_snd).add (contDiff_fst.mul (v.property.1.comp contDiff_snd)), by
      intro t x
      exact congrArg₂ (fun a b : ℝ => a + t * b) (f.property.2 x) (v.property.2 x)⟩

theorem periodicAffineCoefficient_space {Lx : ℝ} (f v : PeriodicCoefficient Lx) :
    (periodicSpacetimeSpaceEvolution Lx).toLinearMap (periodicAffineCoefficient f v) =
      periodicAffineCoefficient ((periodicSpatialEvolution Lx).toLinearMap f)
        ((periodicSpatialEvolution Lx).toLinearMap v) := by
  apply Subtype.ext
  funext tx
  change deriv (fun x => (f : ℝ → ℝ) x + tx.1 * (v : ℝ → ℝ) x) tx.2 =
    deriv (f : ℝ → ℝ) tx.2 + tx.1 * deriv (v : ℝ → ℝ) tx.2
  exact (((f.property.1.differentiable (by simp) tx.2).hasDerivAt).add
    (((v.property.1.differentiable (by simp) tx.2).hasDerivAt).const_mul tx.1)).deriv

theorem periodicAffineCoefficient_iterate {Lx : ℝ} (f v : PeriodicCoefficient Lx) (k : ℕ) :
    ((periodicSpacetimeSpaceEvolution Lx).toLinearMap)^[k] (periodicAffineCoefficient f v) =
      periodicAffineCoefficient (periodicSpatialIterate k f) (periodicSpatialIterate k v) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', ih, periodicAffineCoefficient_space]
    simp only [periodicSpatialIterate, Function.iterate_succ_apply']

def ambientAffineJetSource (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (i : AmbientJetIndex par) : PeriodicSpacetimeCoefficient par.Lx :=
  ((periodicSpacetimeSpaceEvolution par.Lx).toLinearMap)^[i.2.2]
    (if i.1 then periodicAffineCoefficient (z.1 i.2.1) (v.1 i.2.1)
      else periodicAffineCoefficient (z.2 i.2.1) (v.2 i.2.1))

def ambientAffinePolynomialEvaluation (par : FieldParameters) (z v : AmbientPeriodicPair par) :
    AmbientPDO.Poly par →ₐ[ℝ] PeriodicSpacetimeCoefficient par.Lx :=
  MvPolynomial.aeval (ambientAffineJetSource par z v)

theorem ambientAffineJetSource_next (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (i : AmbientJetIndex par) :
    ambientAffineJetSource par z v (i.1, i.2.1, i.2.2 + 1) =
      (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (ambientAffineJetSource par z v i) :=
  Function.iterate_succ_apply' _ i.2.2 _

theorem ambientAffinePolynomialEvaluation_spatial (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (p : AmbientPDO.Poly par) :
    ambientAffinePolynomialEvaluation par z v (AmbientPDO.spatialDerivative par p) =
      (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap
        (ambientAffinePolynomialEvaluation par z v p) := by
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero, AmbientPDO.polynomialEvaluation_C]
    symm
    exact evolution_algebraMap_zero _ r
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p i hp =>
    rw [Derivation.leibniz]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      map_add, map_mul, ambientAffinePolynomialEvaluation, MvPolynomial.aeval_X,
      (periodicSpacetimeSpaceEvolution par.Lx).leibniz]
    have hXi : AmbientPDO.spatialDerivative par (MvPolynomial.X i) =
        AmbientPDO.generatorDerivative par i := MvPolynomial.mkDerivation_X _ _ _
    rw [hXi]
    simp only [AmbientPDO.generatorDerivative, MvPolynomial.aeval_X, ambientAffineJetSource_next]
    change _ = (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap
        (ambientAffinePolynomialEvaluation par z v p) * ambientAffineJetSource par z v i +
      ambientAffinePolynomialEvaluation par z v p *
        (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (ambientAffineJetSource par z v i)
    rw [← hp]
    dsimp only [ambientAffinePolynomialEvaluation]
    ring

theorem ambientAffineJetSource_value (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (i : AmbientJetIndex par) (t x : ℝ) :
    (ambientAffineJetSource par z v i : ℝ × ℝ → ℝ) (t, x) =
      (ambientJet par i (z + t • v) : ℝ → ℝ) x := by
  obtain ⟨b, j, k⟩ := i
  cases b <;>
    simp only [ambientAffineJetSource, Bool.false_eq_true, ↓reduceIte,
      periodicAffineCoefficient_iterate]
  · change (periodicSpatialIterate k (z.2 j) : ℝ → ℝ) x +
        t * (periodicSpatialIterate k (v.2 j) : ℝ → ℝ) x =
      (ambientSpatialJet par k (z.2 j + t • v.2 j) : ℝ → ℝ) x
    rw [map_add, map_smul, ambientSpatialJet_eq_iterate, ambientSpatialJet_eq_iterate]
    rfl
  · change (periodicSpatialIterate k (z.1 j) : ℝ → ℝ) x +
        t * (periodicSpatialIterate k (v.1 j) : ℝ → ℝ) x =
      (ambientSpatialJet par k (z.1 j + t • v.1 j) : ℝ → ℝ) x
    rw [map_add, map_smul, ambientSpatialJet_eq_iterate, ambientSpatialJet_eq_iterate]
    rfl

theorem ambientAffinePolynomialEvaluation_value (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (p : AmbientPDO.Poly par) (t x : ℝ) :
    (ambientAffinePolynomialEvaluation par z v p : ℝ × ℝ → ℝ) (t, x) =
      (ambientPolynomialValue par (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)
        (z + t • v) : ℝ → ℝ) x := by
  induction p using MvPolynomial.induction_on with
  | C r => simp [ambientAffinePolynomialEvaluation, ambientPolynomialValue]
  | add p q hp hq =>
    simp only [map_add, Subalgebra.coe_add, Pi.add_apply, ambientPolynomialValue] at *
    rw [hp, hq]
  | mul_X p i hp =>
    simp only [map_mul, MvPolynomial.map_X, ambientAffinePolynomialEvaluation,
      MvPolynomial.aeval_X, Subalgebra.coe_mul, Pi.mul_apply, ambientPolynomialValue,
      MvPolynomial.eval_mul, MvPolynomial.eval_X]
    rw [ambientAffineJetSource_value]
    exact congrArg (fun y : ℝ => y * (ambientJet par i (z + t • v) : ℝ → ℝ) x) hp

theorem ambientAffinePolynomialEvaluation_time_value (par : FieldParameters)
    (z v : AmbientPeriodicPair par) (p : AmbientPDO.Poly par) (x : ℝ) :
    ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap
      (ambientAffinePolynomialEvaluation par z v p) : ℝ × ℝ → ℝ) (0, x) =
      (ambientPolynomialValue par (ambientPolynomialVariation par v
        (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) z : ℝ → ℝ) x := by
  let q := MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p
  have h := linear_polynomial_evaluation_hasDerivAt_zero
    (coefficientEvaluation par.Lx x).toLinearMap (ambientPolynomialLine par q z v)
  rw [ambientPolynomialLine_coeff_one] at h
  change HasDerivAt
    (fun t : ℝ => (coefficientEvaluation par.Lx x)
      ((ambientPolynomialLine par q z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t)))
    ((coefficientEvaluation par.Lx x)
      (ambientPolynomialValue par (ambientPolynomialVariation par v q) z)) 0 at h
  have hf : (fun t : ℝ => (ambientAffinePolynomialEvaluation par z v p : ℝ × ℝ → ℝ) (t, x)) =
      (fun t : ℝ => (coefficientEvaluation par.Lx x)
        ((ambientPolynomialLine par q z v).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) t))) := by
    funext t
    rw [ambientPolynomialLine_eval]
    exact ambientAffinePolynomialEvaluation_value par z v p t x
  rw [← hf] at h
  exact h.deriv

theorem ambientAffinePolynomialEvaluation_time_slice (par : FieldParameters)
    (z v : AmbientPeriodicPair par) (p : AmbientPDO.Poly par) :
    spacetimeSlice par.Lx 0 ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap
      (ambientAffinePolynomialEvaluation par z v p)) =
    ambientPolynomialValue par (ambientPolynomialVariation par v
      (MvPolynomial.map (algebraMap ℝ (PeriodicCoefficient par.Lx)) p)) z := by
  apply Subtype.ext
  funext x
  exact ambientAffinePolynomialEvaluation_time_value par z v p x

structure PeriodicTimePDOModel (Lx : ℝ) (A : Type*) [Ring A] [Algebra ℝ A] where
  normal : NormalPDOModel (PeriodicSpacetimeCoefficient Lx) A
  spatial : normal.d = periodicSpacetimeSpaceEvolution Lx
  evolution : AlgebraEvolution A
  evolution_D : evolution.toLinearMap (normal.D : A) = 0
  evolution_coeff : ∀ r, evolution.toLinearMap (normal.coefficient r) =
    normal.coefficient ((periodicSpacetimeTimeEvolution Lx).toLinearMap r)
  evolution_coefficients : ∀ X e, normal.coefficients (evolution.toLinearMap X) e =
    (periodicSpacetimeTimeEvolution Lx).toLinearMap (normal.coefficients X e)

def PeriodicTimePDOModel.residue {Lx : ℝ} {A : Type*} [Ring A] [Algebra ℝ A]
    (model : PeriodicTimePDOModel Lx A) : A →ₗ[ℝ] PeriodicSpacetimeCoefficient Lx :=
  (LinearMap.proj (-1 : ℤ)).comp model.normal.coefficients

structure AmbientAffineSpectrum (par : FieldParameters) (z v : AmbientPeriodicPair par)
    (A : Type*) [Ring A] [Algebra ℝ A] where
  model : PeriodicTimePDOModel par.Lx A
  factors : AmbientPDO.FactorRealization par (ambientAffinePolynomialEvaluation par z v) model.normal
  normalized : AmbientPDO.NormalizedRealization factors

namespace AmbientAffineSpectrum
variable {par : FieldParameters} {z v : AmbientPeriodicPair par}
    {A : Type*} [Ring A] [Algebra ℝ A] (rep : AmbientAffineSpectrum par z v A)

/-- The actual Euler variation equals the actual time-source residue
rate, using the proved density realization and genuine derivatives. -/
theorem euler_variation_eq_residue_rate (n : ℕ) :
    ambientPairing par (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n) z) v =
      (n : ℝ)⁻¹ * spacetimePeriodIntegral par.Lx 0
        (rep.model.residue (rep.model.evolution.toLinearMap (rep.normalized.L ^ n))) := by
  rw [ambientEulerGradient_pairing]
  have hd := ambientAffinePolynomialEvaluation_time_slice par z v
    (AmbientPDO.spectralDensityPolynomial par n)
  change spacetimeSlice par.Lx 0 ((periodicSpacetimeTimeEvolution par.Lx).toLinearMap
    (ambientAffinePolynomialEvaluation par z v (AmbientPDO.spectralDensityPolynomial par n))) =
    ambientPolynomialValue par (ambientPolynomialVariation par v
      (AmbientPDO.periodicDensityPolynomial par n)) z at hd
  unfold ambientPolynomialIntegral
  rw [← hd, rep.normalized.density_realization, map_smul,
    ← rep.model.evolution_coefficients, map_smul, map_smul]
  rfl

/-- The rational monodromy gradient represents the constructed charge's
actual first variation, rather than being inserted as a gradient axiom. -/
theorem euler_variation_eq_rational_pairing (tr : CyclicTrace A)
    (htr : tr.toLinearMap = (spacetimePeriodIntegral par.Lx 0).comp rep.model.residue)
    (n : ℕ) (hn : 0 < n) :
    ambientPairing par (ambientEulerGradient par (AmbientPDO.periodicDensityPolynomial par n) z) v =
      tr.toLinearMap (rationalGradient par.G par.B rep.normalized.difference n *
        rep.model.evolution.toLinearMap (rep.factors.monodromy par.M)) := by
  have hu : (rep.normalized.difference : A) = rep.factors.monodromy par.M - 1 :=
    rep.normalized.difference_eq.trans (rep.factors.monodromyDifference_eq par.M)
  rw [rep.euler_variation_eq_residue_rate]
  have hr := rationalGradient_represents_spectral_variation tr rep.model.evolution
    (rep.factors.monodromy par.M) par.G par.B rep.normalized.difference hu n hn
  rw [← hr, spectralInvariantRate, htr]
  rfl

end AmbientAffineSpectrum

#print axioms ambientAffinePolynomialEvaluation_time_value
#print axioms AmbientAffineSpectrum.euler_variation_eq_rational_pairing
end
end DLWLean
