import GlobalSpectralRealization
import AmbientNormalizedRealization
import AmbientChartDerivative

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem coefficientLatticeMean_wCoordinate {par : FieldParameters} (z : FieldCoordinates par) :
    coefficientLatticeMean par z.wCoefficient = algebraMap ℝ (PeriodicCoefficient par.Lx) par.c := by
  apply Subtype.ext
  funext x
  rw [coefficientLatticeMean_eval]
  exact z.mean_w x

theorem AmbientPDO.evaluation_U_coordinate {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) :
    AmbientPDO.evaluation par (coordinateAmbient z) (AmbientPDO.U par j) = z.UCoefficient j := by
  rw [AmbientPDO.U, AmbientPDO.evaluation_X]
  rfl

theorem AmbientPDO.evaluation_w_coordinate {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) :
    AmbientPDO.evaluation par (coordinateAmbient z) (AmbientPDO.w par j) = z.wCoefficient j := by
  unfold AmbientPDO.w AmbientPDO.s AmbientPDO.projectedJet
  rw [map_add, map_sub, map_mul, map_sum, AmbientPDO.evaluation_C, AmbientPDO.evaluation_C]
  simp only [AmbientPDO.evaluation_X]
  change algebraMap ℝ (PeriodicCoefficient par.Lx) par.c +
    (z.wCoefficient j - algebraMap ℝ (PeriodicCoefficient par.Lx) (par.M : ℝ)⁻¹ *
      ∑ i : Fin par.M, z.wCoefficient i) = _
  have hm : algebraMap ℝ (PeriodicCoefficient par.Lx) (par.M : ℝ)⁻¹ *
      (∑ i : Fin par.M, z.wCoefficient i) = algebraMap ℝ (PeriodicCoefficient par.Lx) par.c := by
    simpa only [coefficientLatticeMean, Algebra.smul_def] using coefficientLatticeMean_wCoordinate z
  rw [hm]
  ring

namespace GlobalPDO
variable {par : FieldParameters} {A : Type*} [Ring A] [Algebra ℝ A]
    {z : ClosedPeriodicPair par} {model : NormalPDOModel (PeriodicCoefficient par.Lx) A}

theorem evaluation_U_coefficient (j : Fin par.M) :
    evaluation par z (U par j) = (closedPairCoordinates par z).UCoefficient j := by
  apply Subtype.ext
  funext x
  exact U_eval_value par z j x

theorem evaluation_w_coefficient (j : Fin par.M) :
    evaluation par z (w par j) = (closedPairCoordinates par z).wCoefficient j := by
  apply Subtype.ext
  funext x
  exact w_eval_value par z j x

theorem ambient_evaluation_g (j : Fin par.M) :
    AmbientPDO.evaluation par (coordinateAmbient (closedPairCoordinates par z))
      (AmbientPDO.g par j) = evaluation par z (g par j) := by
  rw [AmbientPDO.g, g, map_mul, map_mul, AmbientPDO.evaluation_C, evaluation_C,
    AmbientPDO.evaluation_w_coordinate, evaluation_w_coefficient]

theorem ambient_evaluation_beta (j : Fin par.M) :
    AmbientPDO.evaluation par (coordinateAmbient (closedPairCoordinates par z))
      (AmbientPDO.beta par j) = evaluation par z (beta par j) := by
  rw [AmbientPDO.beta, beta, map_mul, map_mul, map_sub, map_sub,
    AmbientPDO.evaluation_C, evaluation_C, AmbientPDO.evaluation_U_coordinate,
    evaluation_U_coefficient, ambient_evaluation_g]

def FactorRealization.ambient (factors : FactorRealization par z model) :
    AmbientPDO.FactorRealization par
      (AmbientPDO.evaluation par (coordinateAmbient (closedPairCoordinates par z))) model where
  derivative p := by
    rw [factors.spatial]
    exact AmbientPDO.evaluation_derivative par _ p
  denominator := factors.denominator
  denominator_eq j := by
    rw [ambient_evaluation_beta]
    exact factors.denominator_eq j

theorem FactorRealization.ambient_site_eq (factors : FactorRealization par z model)
    (j : Fin par.M) : factors.ambient.site j = factors.site j := by
  unfold AmbientPDO.FactorRealization.site FactorRealization.site FactorRealization.ambient
  rw [ambient_evaluation_g]

theorem FactorRealization.ambient_siteNat_eq (factors : FactorRealization par z model)
    (j : ℕ) : factors.ambient.siteNat j = factors.siteNat j := by
  unfold AmbientPDO.FactorRealization.siteNat FactorRealization.siteNat
  split_ifs
  · exact factors.ambient_site_eq _
  · rfl

theorem FactorRealization.ambient_monodromyDifference_eq (factors : FactorRealization par z model)
    (n : ℕ) : factors.ambient.monodromyDifference n = factors.monodromyDifference n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [AmbientPDO.FactorRealization.monodromyDifference, FactorRealization.monodromyDifference,
      factors.ambient_siteNat_eq, ih]

def NormalizedRealization.ambient {factors : FactorRealization par z model}
    (realization : NormalizedRealization factors) : AmbientPDO.NormalizedRealization factors.ambient where
  difference := realization.difference
  difference_eq := by rw [factors.ambient_monodromyDifference_eq]; exact realization.difference_eq

theorem ambient_periodicDensity_eval (n : ℕ) :
    ambientPolynomialValue par (AmbientPDO.periodicDensityPolynomial par n)
      (coordinateAmbient (closedPairCoordinates par z)) =
    AmbientPDO.evaluation par (coordinateAmbient (closedPairCoordinates par z))
      (AmbientPDO.spectralDensityPolynomial par n) := by
  unfold ambientPolynomialValue AmbientPDO.periodicDensityPolynomial AmbientPDO.evaluation
  rw [← MvPolynomial.eval₂_eq_eval_map]
  rfl

/-- The ambient hierarchy agrees with the global physical hierarchy by
realizing both recurrences in the same PDO factors. Chart identity is a
consequence, not an input. -/
theorem ambient_constructedCharge_eq {factors : FactorRealization par z model}
    (realization : NormalizedRealization factors) (n : ℕ) :
    AmbientPDO.constructedCharge par n (coordinateAmbient (closedPairCoordinates par z)) =
      constructedCharge par n z := by
  unfold AmbientPDO.constructedCharge ambientPolynomialIntegral constructedCharge fieldPolynomialIntegral
  rw [ambient_periodicDensity_eval, periodicDensityPolynomial_eval,
    realization.ambient.density_realization]
  rw [spectralDensityPolynomial, map_mul, evaluation_C]
  change periodicCoefficientIntegral par.Lx
      ((n : ℝ)⁻¹ • model.coefficients (realization.L ^ n) (-1)) =
    periodicCoefficientIntegral par.Lx
      ((n : ℝ)⁻¹ • evaluation par z (residuePolynomial par n))
  rw [realization.residue_realization]

#print axioms FactorRealization.ambient
#print axioms ambient_constructedCharge_eq
end GlobalPDO
end
end DLWLean
