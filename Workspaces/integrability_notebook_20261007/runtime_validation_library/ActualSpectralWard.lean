import CommonGaugeDensityVariation
import NormalScalarResidue
import PhysicalAmbientSpectrumIdentity

namespace DLWLean
noncomputable section
open scoped BigOperators

def smoothStaticCoefficientHom (Lx : ℝ) :
    PeriodicCoefficient Lx →ₐ[ℝ] SmoothSpacetimeCoefficient where
  toFun := smoothStaticCoefficient
  map_zero' := rfl
  map_one' := rfl
  map_add' _ _ := rfl
  map_mul' _ _ := rfl
  commutes' _ := rfl

def commonGaugeProjectedW (par : FieldParameters) (z : AmbientPeriodicPair par)
    (j : Fin par.M) : PeriodicCoefficient par.Lx :=
  algebraMap ℝ (PeriodicCoefficient par.Lx) par.c + z.2 j -
    algebraMap ℝ (PeriodicCoefficient par.Lx) (par.M : ℝ)⁻¹ * ∑ i, z.2 i

theorem commonGaugePolynomialEvaluation_U (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (j : Fin par.M) :
    commonGaugePolynomialEvaluation par z a (AmbientPDO.U par j) =
      smoothCommonUCoefficient (z.1 j) a := by
  simp [commonGaugePolynomialEvaluation, AmbientPDO.U, commonGaugeJetSource]

theorem commonGaugePolynomialEvaluation_w (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (j : Fin par.M) :
    commonGaugePolynomialEvaluation par z a (AmbientPDO.w par j) =
      smoothStaticCoefficient (commonGaugeProjectedW par z j) := by
  unfold AmbientPDO.w AmbientPDO.s AmbientPDO.projectedJet
  rw [map_add, map_sub, map_mul, map_sum, AmbientPDO.polynomialEvaluation_C,
    AmbientPDO.polynomialEvaluation_C]
  simp only [commonGaugePolynomialEvaluation, MvPolynomial.aeval_X, commonGaugeJetSource,
    Bool.false_eq_true, ↓reduceIte, Function.iterate_zero, id_eq]
  change _ = (smoothStaticCoefficientHom par.Lx)
    (algebraMap ℝ (PeriodicCoefficient par.Lx) par.c + z.2 j -
      algebraMap ℝ (PeriodicCoefficient par.Lx) (par.M : ℝ)⁻¹ * ∑ i, z.2 i)
  rw [map_sub, map_add, map_mul, map_sum]
  simp only [AlgHom.commutes]
  have hhom (f : PeriodicCoefficient par.Lx) :
      (smoothStaticCoefficientHom par.Lx) f = smoothStaticCoefficient f := rfl
  simp only [hhom]
  ring

theorem commonGaugePolynomialEvaluation_g (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (j : Fin par.M) :
    commonGaugePolynomialEvaluation par z a (AmbientPDO.g par j) =
      smoothStaticCoefficient (algebraMap ℝ (PeriodicCoefficient par.Lx) (par.h / 4) *
        commonGaugeProjectedW par z j) := by
  rw [AmbientPDO.g, map_mul, AmbientPDO.polynomialEvaluation_C,
    commonGaugePolynomialEvaluation_w]
  change _ = (smoothStaticCoefficientHom par.Lx) _
  rw [map_mul, AlgHom.commutes]
  rfl

theorem commonGaugePolynomialEvaluation_beta (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (j : Fin par.M) :
    commonGaugePolynomialEvaluation par z a (AmbientPDO.beta par j) =
      commonGaugeCoefficient par.h (smoothCommonUCoefficient (z.1 j) a)
        (smoothStaticCoefficient (commonGaugeProjectedW par z j)) (-1) := by
  rw [AmbientPDO.beta, map_mul, map_sub, AmbientPDO.polynomialEvaluation_C,
    commonGaugePolynomialEvaluation_U, AmbientPDO.g, map_mul,
    AmbientPDO.polynomialEvaluation_C, commonGaugePolynomialEvaluation_w]
  unfold commonGaugeCoefficient halfCoefficient latticeQuarter
  simp only [map_neg, map_one]
  ring

/-- Structural formal-PDO rules over actual smooth (epsilon,x) sources.
Every source derivative is fixed to the genuine calculus derivative. -/
structure SmoothTimePDOModel (A : Type*) [Ring A] [Algebra ℝ A] where
  normal : NormalPDOModel SmoothSpacetimeCoefficient A
  spatial : normal.d = smoothSpacetimeSpaceEvolution
  evolution : AlgebraEvolution A
  evolution_D : evolution.toLinearMap (normal.D : A) = 0
  evolution_coeff : ∀ r, evolution.toLinearMap (normal.coefficient r) =
    normal.coefficient (smoothSpacetimeTimeEvolution.toLinearMap r)
  evolution_coefficients : ∀ X e, normal.coefficients (evolution.toLinearMap X) e =
    smoothSpacetimeTimeEvolution.toLinearMap (normal.coefficients X e)

def SmoothTimePDOModel.operator {A : Type*} [Ring A] [Algebra ℝ A]
    (model : SmoothTimePDOModel A) : CoefficientOperatorModel SmoothSpacetimeCoefficient A where
  coeff := model.normal.coefficient
  space := smoothSpacetimeSpaceEvolution
  time := smoothSpacetimeTimeEvolution
  evolution := model.evolution
  D := model.normal.D
  space_commutation r := by
    rw [model.normal.D_coefficient_commutation, model.spatial]
    abel
  evolution_D := model.evolution_D
  evolution_coeff := model.evolution_coeff

/-- Formal first-order inverse units and the normalized monodromy inverse.
The constructed density, its gradient and Ward property are not inputs. -/
structure CommonGaugeRepresentation (par : FieldParameters) (z : AmbientPeriodicPair par)
    (a : PeriodicCoefficient par.Lx) (A : Type*) [Ring A] [Algebra ℝ A] where
  model : SmoothTimePDOModel A
  factors : AmbientPDO.FactorRealization par (commonGaugePolynomialEvaluation par z a) model.normal
  normalized : AmbientPDO.NormalizedRealization factors

namespace CommonGaugeRepresentation
variable {par : FieldParameters} {z : AmbientPeriodicPair par} {a : PeriodicCoefficient par.Lx}
    {A : Type*} [Ring A] [Algebra ℝ A]
    (rep : CommonGaugeRepresentation par z a A)
include rep

def Q : A := rep.model.normal.coefficient (actualGaugePrimitive a)

theorem denominator_inner (j : Fin par.M) :
    rep.model.evolution.toLinearMap (rep.factors.denominator j : A) =
      rep.Q * (rep.factors.denominator j : A) - (rep.factors.denominator j : A) * rep.Q := by
  rw [rep.factors.denominator_eq, commonGaugePolynomialEvaluation_beta]
  change rep.model.operator.evolution.toLinearMap (rep.model.operator.factor _) =
    rep.model.operator.coeff (actualGaugePrimitive a) * rep.model.operator.factor _ -
      rep.model.operator.factor _ * rep.model.operator.coeff (actualGaugePrimitive a)
  apply commonGauge_factor_inner
  · exact (smoothCommonUCoefficient_time _ _).trans (actualGaugePrimitive_space a).symm
  · exact smoothStaticCoefficient_time _

theorem site_inner (j : Fin par.M) :
    rep.model.evolution.toLinearMap (rep.factors.site j) =
      rep.Q * rep.factors.site j - rep.factors.site j * rep.Q := by
  have hi := unit_inverse_lax rep.model.evolution (rep.factors.denominator j) rep.Q
    (rep.denominator_inner j)
  have hg : rep.model.evolution.toLinearMap
      (rep.model.normal.coefficient (commonGaugePolynomialEvaluation par z a (AmbientPDO.g par j))) = 0 := by
    rw [rep.model.evolution_coeff, commonGaugePolynomialEvaluation_g,
      smoothStaticCoefficient_time, map_zero]
  have hc : rep.Q * rep.model.normal.coefficient
        (commonGaugePolynomialEvaluation par z a (AmbientPDO.g par j)) =
      rep.model.normal.coefficient
        (commonGaugePolynomialEvaluation par z a (AmbientPDO.g par j)) * rep.Q :=
    rep.model.operator.coeff_mul_comm _ _
  unfold AmbientPDO.FactorRealization.site
  rw [rep.model.evolution.leibniz, map_neg, hi, hg, mul_zero, add_zero]
  noncomm_ring [hc]

theorem siteNat_inner (j : ℕ) :
    rep.model.evolution.toLinearMap (rep.factors.siteNat j) =
      rep.Q * rep.factors.siteNat j - rep.factors.siteNat j * rep.Q := by
  unfold AmbientPDO.FactorRealization.siteNat
  split_ifs
  · exact rep.site_inner _
  · simp

theorem monodromyDifference_inner (n : ℕ) :
    rep.model.evolution.toLinearMap (rep.factors.monodromyDifference n) =
      rep.Q * rep.factors.monodromyDifference n - rep.factors.monodromyDifference n * rep.Q := by
  induction n with
  | zero => simp [AmbientPDO.FactorRealization.monodromyDifference]
  | succ n ih =>
    rw [AmbientPDO.FactorRealization.monodromyDifference, map_add, map_add,
      rep.model.evolution.leibniz, rep.siteNat_inner, ih]
    noncomm_ring

theorem normalized_inner :
    rep.model.evolution.toLinearMap rep.normalized.L =
      rep.Q * rep.normalized.L - rep.normalized.L * rep.Q := by
  have hu : rep.model.evolution.toLinearMap (rep.normalized.difference : A) =
      rep.Q * (rep.normalized.difference : A) - (rep.normalized.difference : A) * rep.Q := by
    rw [rep.normalized.difference_eq]
    exact rep.monodromyDifference_inner par.M
  have hi := unit_inverse_lax rep.model.evolution rep.normalized.difference rep.Q hu
  simp only [AmbientPDO.NormalizedRealization.L, map_add, map_smul, hi,
    evolution_map_one, smul_zero, add_zero, mul_add, add_mul, Algebra.mul_smul_comm,
    Algebra.smul_mul_assoc, mul_one, one_mul, smul_sub]
  abel

/-- Zero residue rate is derived from the source factor identities and
finite normal multiplication. No cyclicity is applied to the primitive. -/
theorem residue_rate_zero (n : ℕ) :
    rep.model.normal.coefficients (rep.model.evolution.toLinearMap (rep.normalized.L ^ n)) (-1) = 0 := by
  rw [lax_power_evolution rep.model.evolution rep.normalized.L rep.Q rep.normalized_inner n]
  exact rep.model.normal.scalar_commutator_residue_zero _ _

theorem density_time_zero (n : ℕ) :
    smoothSpacetimeTimeEvolution.toLinearMap
      (commonGaugePolynomialEvaluation par z a (AmbientPDO.spectralDensityPolynomial par n)) = 0 := by
  rw [rep.normalized.density_realization, map_smul,
    ← rep.model.evolution_coefficients, rep.residue_rate_zero, smul_zero]

theorem density_first_variation_zero (n : ℕ) :
    ambientPolynomialValue par
      (ambientPolynomialVariation par ((fun _ => a), 0)
        (AmbientPDO.periodicDensityPolynomial par n)) z = 0 := by
  apply Subtype.ext
  funext x
  have h := congrArg (fun f : SmoothSpacetimeCoefficient => (f : ℝ × ℝ → ℝ) (0, x))
    (rep.density_time_zero n)
  rw [commonGaugePolynomialEvaluation_time_value] at h
  exact h

end CommonGaugeRepresentation

/-- Every common direction has a formal PDO realization. Only normal
PDO definitions and inverse units are quantified over here. -/
def ActualSpectralWardFoundation (par : FieldParameters) (z : AmbientPeriodicPair par) : Prop :=
  ∀ a : PeriodicCoefficient par.Lx, ∃ (A : Type) (_ : Ring A) (_ : Algebra ℝ A),
    Nonempty (CommonGaugeRepresentation par z a A)

theorem actualSpectralCommonWard (par : FieldParameters) (z : AmbientPeriodicPair par)
    (foundation : ActualSpectralWardFoundation par z) (n : ℕ) :
    AmbientCommonWard par (AmbientPDO.periodicDensityPolynomial par n) z := by
  intro a
  obtain ⟨A, instRing, instAlgebra, ⟨rep⟩⟩ := foundation a
  unfold ambientPolynomialIntegral
  rw [rep.density_first_variation_zero, map_zero]

#print axioms CommonGaugeRepresentation.normalized_inner
#print axioms CommonGaugeRepresentation.density_first_variation_zero
#print axioms actualSpectralCommonWard
end
end DLWLean
