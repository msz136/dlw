import PhysicalBracket
import ActualPhysicalSource
import PhysicalFirstResidue
import PolynomialIntegralVariation

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

def coefficientEvaluation (Lx x : ℝ) : PeriodicCoefficient Lx →ₐ[ℝ] ℝ where
  toFun f := (f : ℝ → ℝ) x
  map_zero' := rfl
  map_one' := rfl
  map_add' _ _ := rfl
  map_mul' _ _ := rfl
  commutes' _ := rfl

@[simp] theorem coefficientEvaluation_apply (Lx x : ℝ) (f : PeriodicCoefficient Lx) :
    coefficientEvaluation Lx x f = (f : ℝ → ℝ) x := rfl

def coefficientLatticeMean (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) : PeriodicCoefficient par.Lx :=
  (par.M : ℝ)⁻¹ • ∑ j : Fin par.M, f j

theorem coefficientLatticeMean_eval (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) (x : ℝ) :
    (coefficientLatticeMean par f : ℝ → ℝ) x = latticeMean (fun j => (f j : ℝ → ℝ) x) := by
  change coefficientEvaluation par.Lx x ((par.M : ℝ)⁻¹ • ∑ j : Fin par.M, f j) = _
  rw [map_smul, map_sum]
  simp only [coefficientEvaluation_apply, smul_eq_mul, latticeMean, div_eq_mul_inv]
  ring

def periodicHamiltonianResolvent (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) :
    PeriodicCoefficient par.Lx :=
  ⟨fun x => latticeResolvent par (fun i => (f i : ℝ → ℝ) x) j,
    smooth_finite_linear_map (latticeResolvent par) _ (fun i => (f i).property.1) j,
    periodic_finite_linear_map par.Lx (latticeResolvent par) _ (fun i => (f i).property.2) j⟩

theorem periodicHamiltonianResolvent_skew (par : FieldParameters)
    (f g : Fin par.M → PeriodicCoefficient par.Lx) :
    (∑ j : Fin par.M, f j * periodicHamiltonianResolvent par g j) =
      -(∑ j : Fin par.M, periodicHamiltonianResolvent par f j * g j) := by
  apply Subtype.ext
  funext x
  have h := latticeResolvent_skew par (fun i => (f i : ℝ → ℝ) x)
    (fun i => (g i : ℝ → ℝ) x)
  change coefficientEvaluation par.Lx x (∑ j : Fin par.M, f j * periodicHamiltonianResolvent par g j) =
    coefficientEvaluation par.Lx x (-(∑ j : Fin par.M, periodicHamiltonianResolvent par f j * g j))
  simpa only [map_sum, map_neg, map_mul, coefficientEvaluation_apply, periodicHamiltonianResolvent] using h

theorem periodicHamiltonianResolvent_space (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) :
    (periodicSpatialEvolution par.Lx).toLinearMap (periodicHamiltonianResolvent par f j) =
      periodicHamiltonianResolvent par (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (f i)) j := by
  apply Subtype.ext
  funext x
  exact derivative_finite_linear_map (latticeResolvent par) _
    (fun i => (f i).property.1.differentiable (by simp)) x j

def physicalKGradientP {par : FieldParameters} (z : FieldCoordinates par) :
    ClosedPeriodicField par :=
  ⟨fun j => z.UCoefficient j * z.wCoefficient j -
    algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma -
      (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient j), by
    apply Subtype.ext
    funext x
    change coefficientEvaluation par.Lx x (∑ j : Fin par.M,
      (z.UCoefficient j * z.wCoefficient j -
      algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma -
      (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient j))) = 0
    rw [map_sum]
    change (∑ j : Fin par.M, (z.U j x * z.w j x - par.gamma - deriv (z.w j) x)) = 0
    have hm := z.mean_Uw x
    have hw := derivative_latticeMean_of_constant z.w
      (fun i => (z.w_smooth i).differentiable (by simp)) par.c z.mean_w x
    have hsum : (∑ j : Fin par.M, z.U j x * z.w j x) = (par.M : ℝ) * par.gamma := by
      rw [sum_eq_card_mul_latticeMean par.M_ne_zero, hm]
    have hsumw : (∑ j : Fin par.M, deriv (z.w j) x) = 0 := by
      rw [sum_eq_card_mul_latticeMean par.M_ne_zero, hw, mul_zero]
    simpa only [Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, nsmul_eq_mul, hsum, hsumw, sub_self, sub_zero]⟩

def physicalKUnprojectedS {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) : PeriodicCoefficient par.Lx :=
  (1 / 2 : ℝ) • (z.UCoefficient j ^ 2) +
    beta par • (z.wCoefficient j ^ 2) +
    (periodicSpatialEvolution par.Lx).toLinearMap (z.UCoefficient j) +
    periodicHamiltonianResolvent par (fun i =>
      (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient i)) j

def physicalKGradientS {par : FieldParameters} (z : FieldCoordinates par) :
    ClosedPeriodicField par :=
  ⟨fun j => physicalKUnprojectedS z j - coefficientLatticeMean par (physicalKUnprojectedS z), by
    apply Subtype.ext
    funext x
    change coefficientEvaluation par.Lx x (∑ j : Fin par.M,
      (physicalKUnprojectedS z j - coefficientLatticeMean par (physicalKUnprojectedS z))) = 0
    rw [map_sum]
    simp only [map_sub, coefficientEvaluation_apply, coefficientLatticeMean_eval]
    have h := sum_eq_card_mul_latticeMean par.M_ne_zero
      (latticeP0 (fun j => (physicalKUnprojectedS z j : ℝ → ℝ) x))
    rw [latticeMean_P0 par.M_ne_zero, mul_zero] at h
    simpa only [latticeP0] using h⟩

def physicalKGradient {par : FieldParameters} (z : FieldCoordinates par) :
    ClosedPeriodicPair par := (physicalKGradientP z, physicalKGradientS z)

theorem periodicHamiltonianResolvent_gradient_pairing (par : FieldParameters)
    (w q : Fin par.M → PeriodicCoefficient par.Lx) :
    periodicCoefficientIntegral par.Lx (∑ j : Fin par.M, w j * periodicHamiltonianResolvent par
      (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (q i)) j) =
    periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      periodicHamiltonianResolvent par (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j * q j) := by
  rw [periodicHamiltonianResolvent_skew, map_neg, map_sum, map_sum]
  simp_rw [periodicCoefficientIntegral_parts, periodicHamiltonianResolvent_space]
  rw [Finset.sum_neg_distrib, neg_neg]

/-- The actual integrated energy first-variation expression is reduced by
periodic integration by parts and the constructed R skewness. This lemma
does not assert that an arbitrary nonlinear functional has this variation. -/
theorem physicalK_raw_variation_reduction (par : FieldParameters)
    (U w V q : Fin par.M → PeriodicCoefficient par.Lx) :
    periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      (U j * V j * w j + (1 / 2 : ℝ) • (U j ^ 2 * q j) +
        beta par • (w j ^ 2 * q j) +
        q j * (periodicSpatialEvolution par.Lx).toLinearMap (U j) +
        w j * (periodicSpatialEvolution par.Lx).toLinearMap (V j) +
        (1 / 2 : ℝ) • (q j * periodicHamiltonianResolvent par
          (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j) +
        (1 / 2 : ℝ) • (w j * periodicHamiltonianResolvent par
          (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (q i)) j) -
        par.gamma • (V j))) =
    periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      ((U j * w j - (periodicSpatialEvolution par.Lx).toLinearMap (w j) -
        algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma) * V j +
      ((1 / 2 : ℝ) • (U j ^ 2) + beta par • (w j ^ 2) +
        (periodicSpatialEvolution par.Lx).toLinearMap (U j) +
        periodicHamiltonianResolvent par (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j) * q j)) := by
  let I := periodicCoefficientIntegral par.Lx
  have hR := periodicHamiltonianResolvent_gradient_pairing par w q
  have hparts : I (∑ j : Fin par.M, w j * (periodicSpatialEvolution par.Lx).toLinearMap (V j)) =
      -I (∑ j : Fin par.M, (periodicSpatialEvolution par.Lx).toLinearMap (w j) * V j) := by
    simp only [I, map_sum]
    simp_rw [periodicCoefficientIntegral_parts]
    rw [Finset.sum_neg_distrib]
  have hcomm : I (∑ j : Fin par.M, q j * periodicHamiltonianResolvent par
      (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j) =
      I (∑ j : Fin par.M, periodicHamiltonianResolvent par
        (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j * q j) := by
    congr 1
    apply Finset.sum_congr rfl
    intro j _
    exact mul_comm _ _
  have hexpand : (∑ j : Fin par.M,
      ((U j * w j - (periodicSpatialEvolution par.Lx).toLinearMap (w j) -
        algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma) * V j +
      ((1 / 2 : ℝ) • (U j ^ 2) + beta par • (w j ^ 2) +
        (periodicSpatialEvolution par.Lx).toLinearMap (U j) +
        periodicHamiltonianResolvent par (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j) * q j)) =
      (∑ j : Fin par.M, U j * V j * w j) -
      (∑ j : Fin par.M, (periodicSpatialEvolution par.Lx).toLinearMap (w j) * V j) -
      par.gamma • (∑ j : Fin par.M, V j) + (1 / 2 : ℝ) • (∑ j : Fin par.M, U j ^ 2 * q j) +
      beta par • (∑ j : Fin par.M, w j ^ 2 * q j) +
      (∑ j : Fin par.M, q j * (periodicSpatialEvolution par.Lx).toLinearMap (U j)) +
      (∑ j : Fin par.M, periodicHamiltonianResolvent par (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j * q j) := by
    simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, Finset.smul_sum]
    rw [← Finset.sum_sub_distrib, ← Finset.sum_sub_distrib,
      ← Finset.sum_add_distrib, ← Finset.sum_add_distrib,
      ← Finset.sum_add_distrib, ← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    simp only [Algebra.smul_def]
    ring
  rw [hexpand]
  simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.smul_sum,
    map_add, map_sub, map_smul, smul_eq_mul] at *
  rw [hparts, hR, hcomm]
  dsimp [I]
  ring

def coordinateUTangent {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (j : Fin par.M) : PeriodicCoefficient par.Lx :=
  v.1 j - par.c⁻¹ • coefficientLatticeMean par
    (fun i => z.s.coefficient i * v.1 i + z.p.coefficient i * v.2 i)

theorem physicalK_coordinate_variation_reduction {par : FieldParameters}
    (z : FieldCoordinates par) (v : ClosedPeriodicPair par) :
    par.h * periodicCoefficientIntegral par.Lx (∑ j : Fin par.M,
      ((physicalKGradientP z j) * coordinateUTangent z v j +
        physicalKUnprojectedS z j * v.2 j)) =
      coefficientGradientPairing par (physicalKGradient z) v := by
  have hP : (∑ j : Fin par.M, (physicalKGradientP z j) * coordinateUTangent z v j) =
      ∑ j : Fin par.M, (physicalKGradientP z j) * v.1 j := by
    unfold coordinateUTangent
    have hz : (∑ j : Fin par.M, physicalKGradientP z j) = 0 := (physicalKGradientP z).property
    simp only [mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul]
    rw [hz, zero_mul, sub_zero]
  have hS : (∑ j : Fin par.M, physicalKUnprojectedS z j * v.2 j) =
      ∑ j : Fin par.M, (physicalKGradientS z j) * v.2 j := by
    change (∑ j : Fin par.M, physicalKUnprojectedS z j * v.2 j) =
      ∑ j : Fin par.M, (physicalKUnprojectedS z j -
        coefficientLatticeMean par (physicalKUnprojectedS z)) * v.2 j
    have hz : (∑ j : Fin par.M, v.2 j) = 0 := v.2.property
    simp only [sub_mul, Finset.sum_sub_distrib, ← Finset.mul_sum]
    rw [hz, mul_zero, sub_zero]
  rw [Finset.sum_add_distrib, hP, hS, map_add]
  unfold coefficientGradientPairing coefficientPairing physicalKGradient
  ring

def physicalKRawCoefficient (par : FieldParameters)
    (U w V q : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) :
    PeriodicCoefficient par.Lx :=
  U j * V j * w j + (1 / 2 : ℝ) • (U j ^ 2 * q j) +
    beta par • (w j ^ 2 * q j) +
    q j * (periodicSpatialEvolution par.Lx).toLinearMap (U j) +
    w j * (periodicSpatialEvolution par.Lx).toLinearMap (V j) +
    (1 / 2 : ℝ) • (q j * periodicHamiltonianResolvent par
      (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j) +
    (1 / 2 : ℝ) • (w j * periodicHamiltonianResolvent par
      (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (q i)) j) -
    par.gamma • (V j)

def quadraticCoefficientPolynomial {Lx : ℝ} (a b c : PeriodicCoefficient Lx) :
    Polynomial (PeriodicCoefficient Lx) :=
  Polynomial.C a + Polynomial.monomial 1 b + Polynomial.monomial 2 c

def linearCoefficientPolynomial {Lx : ℝ} (a b : PeriodicCoefficient Lx) :
    Polynomial (PeriodicCoefficient Lx) := Polynomial.C a + Polynomial.monomial 1 b

def physicalKDensityPolynomial (par : FieldParameters)
    (U V W w q : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) :
    Polynomial (PeriodicCoefficient par.Lx) :=
  let Dx := (periodicSpatialEvolution par.Lx).toLinearMap
  let u := quadraticCoefficientPolynomial (U j) (V j) (W j)
  let wpoly := linearCoefficientPolynomial (w j) (q j)
  let ux := quadraticCoefficientPolynomial (Dx (U j)) (Dx (V j)) (Dx (W j))
  let rwx := linearCoefficientPolynomial
    (periodicHamiltonianResolvent par (fun i => Dx (w i)) j)
    (periodicHamiltonianResolvent par (fun i => Dx (q i)) j)
  Polynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) (1 / 2)) * u ^ 2 * wpoly +
    Polynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) (beta par / 3)) * wpoly ^ 3 +
    wpoly * ux + Polynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) (1 / 2)) * wpoly * rwx -
    Polynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma) * u

theorem physicalKDensityPolynomial_coeff_one (par : FieldParameters)
    (U V W w q : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) :
    (physicalKDensityPolynomial par U V W w q j).coeff 1 =
      physicalKRawCoefficient par U w V q j := by
  simp only [physicalKDensityPolynomial, quadraticCoefficientPolynomial,
    linearCoefficientPolynomial, pow_succ, pow_zero, mul_one,
    Polynomial.coeff_add, Polynomial.coeff_sub, Polynomial.mul_coeff_one,
    Polynomial.mul_coeff_zero, Polynomial.coeff_C, Polynomial.coeff_monomial,
    Polynomial.coeff_one]
  norm_num
  apply Subtype.ext
  funext x
  simp only [physicalKRawCoefficient, Subalgebra.coe_add, Pi.add_apply,
    Subalgebra.coe_sub, Pi.sub_apply, Subalgebra.coe_mul, Pi.mul_apply,
    Subalgebra.coe_pow, Pi.pow_apply, Subalgebra.coe_algebraMap, Pi.algebraMap_apply,
    Subalgebra.coe_smul, Pi.smul_apply, smul_eq_mul]
  simp
  ring

/-- Ordinary derivative of the actual coefficient-integral polynomial,
including quadratic U chart terms. Only the linear U term survives. -/
theorem physicalKPolynomialIntegral_hasDerivAt (par : FieldParameters)
    (U V W w q : Fin par.M → PeriodicCoefficient par.Lx) :
    HasDerivAt (fun ε : ℝ => par.h * periodicCoefficientIntegral par.Lx
      ((∑ j : Fin par.M, physicalKDensityPolynomial par U V W w q j).eval
        (algebraMap ℝ (PeriodicCoefficient par.Lx) ε)))
      (par.h * periodicCoefficientIntegral par.Lx
        (∑ j : Fin par.M, physicalKRawCoefficient par U w V q j)) 0 := by
  have h := linear_polynomial_evaluation_hasDerivAt_zero (periodicCoefficientIntegral par.Lx)
    (∑ j : Fin par.M, physicalKDensityPolynomial par U V W w q j)
  simp only [Polynomial.finset_sum_coeff, physicalKDensityPolynomial_coeff_one] at h
  exact h.const_mul par.h

#print axioms physicalKPolynomialIntegral_hasDerivAt
#print axioms physicalK_coordinate_variation_reduction
#print axioms periodicHamiltonianResolvent_gradient_pairing
#print axioms physicalK_raw_variation_reduction
end
end DLWLean




