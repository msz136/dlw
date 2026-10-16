import ActualHamiltonianDerivative
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Periodic

namespace DLWLean
noncomputable section
open scoped BigOperators

/-- Nondegeneracy of the actual period integral. Positivity on a shifted
period containing any chosen point upgrades the integral statement to a
global equality of periodic coefficient functions. -/
theorem periodicCoefficient_integral_square_zero (Lx : ℝ) (hLx : 0 < Lx)
    (q : PeriodicCoefficient Lx)
    (hzero : periodicCoefficientIntegral Lx (q * q) = 0) : q = 0 := by
  apply Subtype.ext
  funext x
  change (q : ℝ → ℝ) x = 0
  by_contra hqx
  have hperiodic : Function.Periodic (fun y => ((q : ℝ → ℝ) y) ^ 2) Lx := by
    intro y
    change ((q : ℝ → ℝ) (y + Lx)) ^ 2 = ((q : ℝ → ℝ) y) ^ 2
    rw [q.property.2 y]
  have hshift := hperiodic.intervalIntegral_add_eq x 0
  simp only [zero_add] at hshift
  have hint : (∫ y in (0 : ℝ)..Lx, ((q : ℝ → ℝ) y) ^ 2) = 0 := by
    change (∫ y in (0 : ℝ)..Lx, (q : ℝ → ℝ) y * (q : ℝ → ℝ) y) = 0 at hzero
    simpa only [pow_two] using hzero
  have hpos := intervalIntegral.integral_lt_integral_of_continuousOn_of_le_of_exists_lt
    (show x < x + Lx by linarith)
    (continuous_const.continuousOn : ContinuousOn (fun _ : ℝ => (0 : ℝ)) (Set.Icc x (x + Lx)))
    (q.property.1.continuous.pow 2).continuousOn
    (fun y _ => sq_nonneg ((q : ℝ → ℝ) y))
    ⟨x, ⟨le_rfl, by linarith⟩, sq_pos_of_ne_zero hqx⟩
  rw [intervalIntegral.integral_zero] at hpos
  change 0 < ∫ y in x..x + Lx, ((q : ℝ → ℝ) y) ^ 2 at hpos
  rw [hshift, hint] at hpos
  exact (lt_irrefl (0 : ℝ)) hpos

def ambientVariationPairing (par : FieldParameters)
    (fU fw δU δw : Fin par.M → PeriodicCoefficient par.Lx) : ℝ :=
  par.h * periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
    (fU j * δU j + fw j * δw j))

/-- Gauge Ward vanishing in every actual common-U direction forces the
ambient U gradient to have zero lattice sum. The test direction is the
gradient sum itself; no desired mean-zero conclusion is a hypothesis. -/
theorem ambient_U_gradient_sum_zero_of_common_Ward (par : FieldParameters)
    (fU fw : Fin par.M → PeriodicCoefficient par.Lx)
    (hWard : ∀ a : PeriodicCoefficient par.Lx,
      ambientVariationPairing par fU fw (fun _ => a) (fun _ => 0) = 0) :
    (∑ j : Fin par.M, fU j) = 0 := by
  let q := ∑ j : Fin par.M, fU j
  have h := hWard q
  have hvalue : ambientVariationPairing par fU fw (fun _ => q) (fun _ => 0) =
      par.h * periodicCoefficientIntegral par.Lx (q * q) := by
    simp only [ambientVariationPairing, mul_zero, add_zero, ← Finset.sum_mul]
    rfl
  rw [hvalue] at h
  have hint : periodicCoefficientIntegral par.Lx (q * q) = 0 :=
    (mul_eq_zero.mp h).resolve_left (ne_of_gt par.h_pos)
  exact periodicCoefficient_integral_square_zero par.Lx par.Lx_pos q hint

def projectedCoefficientGradient (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) : ClosedPeriodicField par :=
  ⟨fun j => f j - coefficientLatticeMean par f, by
    apply Subtype.ext
    funext x
    change coefficientEvaluation par.Lx x (∑ j : Fin par.M,
      (f j - coefficientLatticeMean par f)) = 0
    rw [map_sum]
    simp only [map_sub, coefficientEvaluation_apply, coefficientLatticeMean_eval]
    have h := sum_eq_card_mul_latticeMean par.M_ne_zero
      (latticeP0 (fun j => (f j : ℝ → ℝ) x))
    rw [latticeMean_P0 par.M_ne_zero, mul_zero] at h
    simpa only [latticeP0] using h⟩

def reduceAmbientGradient (par : FieldParameters)
    (fU fw : Fin par.M → PeriodicCoefficient par.Lx)
    (hU : (∑ j : Fin par.M, fU j) = 0) : ClosedPeriodicPair par :=
  (⟨fU, hU⟩, projectedCoefficientGradient par fw)

/-- Exact chart variation reduction for every ambient first-variation
gradient satisfying the Ward conclusion. The nonlinear chart shear and
the fw lattice-common part both cancel in the actual integral pairing. -/
theorem ambientVariationPairing_chart_reduction {par : FieldParameters}
    (z : FieldCoordinates par) (v : ClosedPeriodicPair par)
    (fU fw : Fin par.M → PeriodicCoefficient par.Lx)
    (hU : (∑ j : Fin par.M, fU j) = 0) :
    ambientVariationPairing par fU fw (coordinateUTangent z v) v.2 =
      coefficientGradientPairing par (reduceAmbientGradient par fU fw hU) v := by
  have hP : (∑ j : Fin par.M, fU j * coordinateUTangent z v j) =
      ∑ j : Fin par.M, fU j * v.1 j := by
    unfold coordinateUTangent
    simp only [mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul]
    rw [hU, zero_mul, sub_zero]
  have hS : (∑ j : Fin par.M, fw j * v.2 j) =
      ∑ j : Fin par.M, (projectedCoefficientGradient par fw j) * v.2 j := by
    change (∑ j : Fin par.M, fw j * v.2 j) =
      ∑ j : Fin par.M, (fw j - coefficientLatticeMean par fw) * v.2 j
    have hz : (∑ j : Fin par.M, v.2 j) = 0 := v.2.property
    simp only [sub_mul, Finset.sum_sub_distrib, ← Finset.mul_sum]
    rw [hz, mul_zero, sub_zero]
  unfold ambientVariationPairing
  rw [Finset.sum_add_distrib, hP, hS, map_add]
  unfold coefficientGradientPairing coefficientPairing reduceAmbientGradient
  ring

def ambientConstantBracket (par : FieldParameters)
    (fU fw gU gw : Fin par.M → PeriodicCoefficient par.Lx) : ℝ :=
  -(par.h * periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
    (fU j * (periodicSpatialEvolution par.Lx).toLinearMap (gw j) +
      fw j * (periodicSpatialEvolution par.Lx).toLinearMap (gU j))))

/-- The genuine reduced differential bracket equals the ambient constant
cross-derivative bracket on the actual Ward-invariant gradients. -/
theorem reducedBracketValue_eq_ambient_constant (par : FieldParameters)
    (fU fw gU gw : Fin par.M → PeriodicCoefficient par.Lx)
    (hf : (∑ j : Fin par.M, fU j) = 0)
    (hg : (∑ j : Fin par.M, gU j) = 0) :
    reducedBracketValue par (reduceAmbientGradient par fU fw hf)
      (reduceAmbientGradient par gU gw hg) = ambientConstantBracket par fU fw gU gw := by
  let Dx := (periodicSpatialEvolution par.Lx).toLinearMap
  have hgD : (∑ j : Fin par.M, Dx (gU j)) = 0 := by
    rw [← map_sum, hg, map_zero]
  have hP : (∑ j : Fin par.M,
      fU j * Dx (gw j - coefficientLatticeMean par gw)) =
      ∑ j : Fin par.M, fU j * Dx (gw j) := by
    simp only [map_sub, mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul]
    rw [hf, zero_mul, sub_zero]
  have hS : (∑ j : Fin par.M,
      (fw j - coefficientLatticeMean par fw) * Dx (gU j)) =
      ∑ j : Fin par.M, fw j * Dx (gU j) := by
    simp only [sub_mul, Finset.sum_sub_distrib, ← Finset.mul_sum]
    rw [hgD, mul_zero, sub_zero]
  simp only [reducedBracketValue, coefficientGradientPairing, reducedHamiltonianVector,
    coefficientPairing_neg_right]
  change -(par.h * periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      fU j * Dx (gw j - coefficientLatticeMean par gw))) +
    -(par.h * periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      (fw j - coefficientLatticeMean par fw) * Dx (gU j))) = _
  rw [hP, hS]
  simp only [ambientConstantBracket, Finset.sum_add_distrib, map_add]
  ring

#print axioms periodicCoefficient_integral_square_zero
#print axioms ambient_U_gradient_sum_zero_of_common_Ward
#print axioms ambientVariationPairing_chart_reduction
#print axioms reducedBracketValue_eq_ambient_constant
end
end DLWLean
