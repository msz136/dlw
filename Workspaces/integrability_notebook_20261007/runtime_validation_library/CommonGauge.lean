import HeatIntertwiner
import QuadraticSymbol

namespace DLWLean
noncomputable section
open scoped BigOperators

variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]

/-- Only those normal coefficients which can contribute to a scalar
product's residue are needed. The displayed formulas are the finite
normal-form multiplication rules, rather than a spectral-invariance
premise. The coefficient ring may include a nonperiodic primitive. -/
structure ScalarNormalResidueModel (model : CoefficientOperatorModel R A) where
  residue : A →ₗ[ℝ] R
  upper : A → ℕ
  negativeOne : A → R
  nonnegative : A → ℕ → R
  left_scalar : ∀ ψ X, residue (model.coeff ψ * X) = ψ * negativeOne X
  right_scalar : ∀ X ψ, residue (X * model.coeff ψ) =
    negativeOne X * ψ + ∑ k ∈ Finset.range (upper X + 1),
      (((Ring.choose (k : ℤ) (k + 1) : ℤ) : R)) * nonnegative X k *
        ((model.space.toLinearMap)^[k + 1] ψ)

theorem ScalarNormalResidueModel.scalar_commutator_zero
    {model : CoefficientOperatorModel R A} (normal : ScalarNormalResidueModel model)
    (ψ : R) (X : A) :
    normal.residue (model.coeff ψ * X - X * model.coeff ψ) = 0 := by
  have hchoose (k : ℕ) : Ring.choose (k : ℤ) (k + 1) = 0 := by
    rw [Ring.choose_natCast, Nat.choose_eq_zero_of_lt (Nat.lt_succ_self k)]
    simp
  rw [map_sub, normal.left_scalar, normal.right_scalar]
  simp only [hchoose, Int.cast_zero, zero_mul, Finset.sum_const_zero, add_zero]
  rw [mul_comm ψ, sub_self]

def commonGaugeCoefficient (h : ℝ) (U w : R) (sign : ℝ) : R :=
  halfCoefficient * (U + algebraMap ℝ R sign * latticeQuarter h * w)

/-- A common-U variation with rate 2 psi_x induces an inner variation
of each literal first-order factor. No gauge-invariance conclusion is
included in the source derivative assumptions. -/
theorem commonGauge_factor_inner
    (model : CoefficientOperatorModel R A) (h : ℝ) (U w ψ : R) (sign : ℝ)
    (hU : model.time.toLinearMap U = 2 * model.space.toLinearMap ψ)
    (hw : model.time.toLinearMap w = 0) :
    model.evolution.toLinearMap (model.factor (commonGaugeCoefficient h U w sign)) =
      model.coeff ψ * model.factor (commonGaugeCoefficient h U w sign) -
        model.factor (commonGaugeCoefficient h U w sign) * model.coeff ψ := by
  have htime : model.time.toLinearMap (commonGaugeCoefficient h U w sign) =
      model.space.toLinearMap ψ := by
    unfold commonGaugeCoefficient
    simp only [model.time.leibniz, halfCoefficient, latticeQuarter, map_add,
      evolution_algebraMap_zero, zero_mul, zero_add, hU, hw, mul_zero, add_zero]
    have hhalf := two_mul_halfCoefficient (R := R)
    calc
      algebraMap ℝ R (1 / 2) * (2 * model.space.toLinearMap ψ) =
          (2 * halfCoefficient) * model.space.toLinearMap ψ := by
        unfold halfCoefficient
        ring
      _ = _ := by rw [hhalf, one_mul]
  simp only [CoefficientOperatorModel.factor, map_sub, model.evolution_D,
    model.evolution_coeff, htime, zero_sub]
  simp only [mul_sub, sub_mul]
  rw [model.D_mul_coeff ψ]
  rw [model.coeff_mul_comm ψ (commonGaugeCoefficient h U w sign)]
  noncomm_ring

theorem commonGauge_transfer_inner
    (model : CoefficientOperatorModel R A) (h : ℝ) (U w ψ : R)
    (hU : model.time.toLinearMap U = 2 * model.space.toLinearMap ψ)
    (hw : model.time.toLinearMap w = 0) (denominator : Aˣ)
    (hdenominator : (denominator : A) = model.factor (commonGaugeCoefficient h U w (-1))) :
    model.evolution.toLinearMap
      ((↑denominator⁻¹ : A) * model.factor (commonGaugeCoefficient h U w 1)) =
      model.coeff ψ * ((↑denominator⁻¹ : A) * model.factor (commonGaugeCoefficient h U w 1)) -
        ((↑denominator⁻¹ : A) * model.factor (commonGaugeCoefficient h U w 1)) * model.coeff ψ := by
  apply transfer_from_two_factor_links
  · exact commonGauge_factor_inner model h U w ψ 1 hU hw
  · rw [hdenominator]
    exact commonGauge_factor_inner model h U w ψ (-1) hU hw

/-- The common gauge direction has zero residue rate of every power.
This uses scalar normal-form residue cancellation, so it also works
when psi is nonperiodic; no cyclic-trace assertion is made for it. -/
theorem commonGauge_spectral_residue_rate_zero
    (model : CoefficientOperatorModel R A) (normal : ScalarNormalResidueModel model)
    (ψ : R) (L : A)
    (hinner : model.evolution.toLinearMap L = model.coeff ψ * L - L * model.coeff ψ)
    (n : ℕ) : normal.residue (model.evolution.toLinearMap (L ^ n)) = 0 := by
  rw [lax_power_evolution model.evolution L (model.coeff ψ) hinner n]
  exact normal.scalar_commutator_zero ψ (L ^ n)

/-- All common-U factor variations propagate to the normalized finite
monodromy and annihilate each spectral residue. Only actual source
derivatives and formal units are input; a Lax identity for L is derived. -/
theorem commonGauge_normalized_spectral_residue_rate_zero
    (model : CoefficientOperatorModel R A) (normal : ScalarNormalResidueModel model)
    (h G B : ℝ) (U w : ℕ → R) (ψ : R) (M : ℕ)
    (hU : ∀ j < M, model.time.toLinearMap (U j) = 2 * model.space.toLinearMap ψ)
    (hw : ∀ j < M, model.time.toLinearMap (w j) = 0)
    (denominator : ℕ → Aˣ)
    (hdenominator : ∀ j < M, (denominator j : A) =
      model.factor (commonGaugeCoefficient h (U j) (w j) (-1)))
    (monodromyMinusOne : Aˣ)
    (hmonodromy : (monodromyMinusOne : A) =
      transferProduct (fun j => (↑(denominator j)⁻¹ : A) *
        model.factor (commonGaugeCoefficient h (U j) (w j) 1)) M - 1)
    (n : ℕ) :
    normal.residue (model.evolution.toLinearMap
      (normalizedL G B monodromyMinusOne ^ n)) = 0 := by
  let T : ℕ → A := fun j => (↑(denominator j)⁻¹ : A) *
    model.factor (commonGaugeCoefficient h (U j) (w j) 1)
  have hlinks : ∀ j < M, model.evolution.toLinearMap (T j) =
      model.coeff ψ * T j - T j * model.coeff ψ := by
    intro j hj
    exact commonGauge_transfer_inner model h (U j) (w j) ψ
      (hU j hj) (hw j hj) (denominator j) (hdenominator j hj)
  have hmono := periodic_monodromy_lax model.evolution T
    (fun _ => model.coeff ψ) M hlinks rfl
  have hinner := normalizedL_lax model.evolution (transferProduct T M)
    (model.coeff ψ) G B monodromyMinusOne hmonodromy hmono
  exact commonGauge_spectral_residue_rate_zero model normal ψ _ hinner n

#print axioms ScalarNormalResidueModel.scalar_commutator_zero
#print axioms commonGauge_factor_inner
#print axioms commonGauge_spectral_residue_rate_zero
#print axioms commonGauge_normalized_spectral_residue_rate_zero
end
end DLWLean
