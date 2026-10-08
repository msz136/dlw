import PhysicalHamiltonianVariation

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem coefficientLatticeMean_add (par : FieldParameters)
    (f g : Fin par.M → PeriodicCoefficient par.Lx) :
    coefficientLatticeMean par (fun i => f i + g i) =
      coefficientLatticeMean par f + coefficientLatticeMean par g := by
  simp [coefficientLatticeMean, Finset.sum_add_distrib, smul_add]

theorem coefficientLatticeMean_smul (par : FieldParameters)
    (r : ℝ) (f : Fin par.M → PeriodicCoefficient par.Lx) :
    coefficientLatticeMean par (fun i => r • f i) = r • coefficientLatticeMean par f := by
  simp only [coefficientLatticeMean, ← Finset.smul_sum, smul_smul]
  congr 1
  ring

theorem quadraticCoefficientPolynomial_eval {Lx : ℝ}
    (a b c : PeriodicCoefficient Lx) (ε : ℝ) :
    (quadraticCoefficientPolynomial a b c).eval (algebraMap ℝ (PeriodicCoefficient Lx) ε) =
      a + ε • b + ε ^ 2 • c := by
  simp only [quadraticCoefficientPolynomial, Polynomial.eval_add, Polynomial.eval_C,
    Polynomial.eval_monomial]
  simp only [Algebra.smul_def, map_pow]
  ring

theorem linearCoefficientPolynomial_eval {Lx : ℝ}
    (a b : PeriodicCoefficient Lx) (ε : ℝ) :
    (linearCoefficientPolynomial a b).eval (algebraMap ℝ (PeriodicCoefficient Lx) ε) =
      a + ε • b := by
  simp only [linearCoefficientPolynomial, Polynomial.eval_add, Polynomial.eval_C,
    Polynomial.eval_monomial, pow_one, Algebra.smul_def]
  ring

theorem closedPairCoordinates_UCoefficient_eq (par : FieldParameters)
    (z : ClosedPeriodicPair par) (j : Fin par.M) :
    (closedPairCoordinates par z).UCoefficient j =
      z.1 j + algebraMap ℝ (PeriodicCoefficient par.Lx) (par.gamma / par.c) -
        par.c⁻¹ • coefficientLatticeMean par (fun i => z.1 i * z.2 i) := by
  apply Subtype.ext
  funext x
  change (closedPairCoordinates par z).U j x =
    (z.1 j : ℝ → ℝ) x + par.gamma / par.c -
      par.c⁻¹ * (coefficientLatticeMean par (fun i => z.1 i * z.2 i) : ℝ → ℝ) x
  rw [coefficientLatticeMean_eval]
  change (z.1 j : ℝ → ℝ) x +
      (par.gamma - latticeMean (fun i => (z.1 i : ℝ → ℝ) x * (z.2 i : ℝ → ℝ) x)) / par.c = _
  simp only [Subalgebra.coe_mul, Pi.mul_apply]
  ring

theorem coefficientMean_affine_product (par : FieldParameters)
    (z v : ClosedPeriodicPair par) (ε : ℝ) :
    coefficientLatticeMean par (fun i => (z.1 i + ε • v.1 i) * (z.2 i + ε • v.2 i)) =
      coefficientLatticeMean par (fun i => z.1 i * z.2 i) +
        ε • coefficientLatticeMean par (fun i => z.2 i * v.1 i + z.1 i * v.2 i) +
        ε ^ 2 • coefficientLatticeMean par (fun i => v.1 i * v.2 i) := by
  have hfun : (fun i => (z.1 i + ε • v.1 i) * (z.2 i + ε • v.2 i)) =
      fun i => z.1 i * z.2 i + ε • (z.2 i * v.1 i + z.1 i * v.2 i) +
        ε ^ 2 • (v.1 i * v.2 i) := by
    funext i
    simp only [Algebra.smul_def, map_pow]
    ring
  rw [hfun, coefficientLatticeMean_add, coefficientLatticeMean_add,
    coefficientLatticeMean_smul, coefficientLatticeMean_smul]

def coordinateUQuadratic (par : FieldParameters) (v : ClosedPeriodicPair par) :
    PeriodicCoefficient par.Lx :=
  -(par.c⁻¹ • coefficientLatticeMean par (fun i => v.1 i * v.2 i))

theorem coordinateLine_U_polynomial {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (ε : ℝ) (j : Fin par.M) :
    (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)).UCoefficient j =
      (quadraticCoefficientPolynomial (z.UCoefficient j) (coordinateUTangent z v j)
        (coordinateUQuadratic par v)).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) ε) := by
  rw [quadraticCoefficientPolynomial_eval, closedPairCoordinates_UCoefficient_eq]
  have hz := closedPairCoordinates_UCoefficient_eq par (z.closedP, z.closedS) j
  rw [z.closedPairCoordinates_recover] at hz
  rw [hz]
  change z.closedP j + ε • v.1 j +
    algebraMap ℝ (PeriodicCoefficient par.Lx) (par.gamma / par.c) -
      par.c⁻¹ • coefficientLatticeMean par
        (fun i => (z.closedP i + ε • v.1 i) * (z.closedS i + ε • v.2 i)) = _
  have hm := coefficientMean_affine_product par (z.closedP, z.closedS) v ε
  dsimp only at hm
  rw [hm]
  change _ = z.closedP j + algebraMap ℝ (PeriodicCoefficient par.Lx) (par.gamma / par.c) -
    par.c⁻¹ • coefficientLatticeMean par (fun i => z.closedP i * z.closedS i) +
    ε • (v.1 j - par.c⁻¹ • coefficientLatticeMean par
      (fun i => z.closedS i * v.1 i + z.closedP i * v.2 i)) +
      ε ^ 2 • (-(par.c⁻¹ • coefficientLatticeMean par (fun i => v.1 i * v.2 i)))
  simp only [smul_add, smul_sub, smul_neg, smul_smul]
  module

theorem coordinateLine_w_polynomial {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (ε : ℝ) (j : Fin par.M) :
    (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)).wCoefficient j =
      (linearCoefficientPolynomial (z.wCoefficient j) (v.2 j)).eval
        (algebraMap ℝ (PeriodicCoefficient par.Lx) ε) := by
  rw [linearCoefficientPolynomial_eval]
  apply Subtype.ext
  funext x
  change par.c + ((z.s.value j x) + ε * (v.2 j : ℝ → ℝ) x) =
    (par.c + z.s.value j x) + ε * (v.2 j : ℝ → ℝ) x
  ring

theorem periodicHamiltonianResolvent_affine (par : FieldParameters)
    (f g : Fin par.M → PeriodicCoefficient par.Lx) (ε : ℝ) (j : Fin par.M) :
    periodicHamiltonianResolvent par (fun i => f i + ε • g i) j =
      periodicHamiltonianResolvent par f j + ε • periodicHamiltonianResolvent par g j := by
  apply Subtype.ext
  funext x
  change latticeResolvent par
      ((fun i => (f i : ℝ → ℝ) x) + ε • (fun i => (g i : ℝ → ℝ) x)) j =
    latticeResolvent par (fun i => (f i : ℝ → ℝ) x) j +
      ε * latticeResolvent par (fun i => (g i : ℝ → ℝ) x) j
  rw [map_add, map_smul]
  rfl

theorem coefficient_space_quadratic_polynomial {Lx : ℝ}
    (a b c : PeriodicCoefficient Lx) (ε : ℝ) :
    (periodicSpatialEvolution Lx).toLinearMap
        ((quadraticCoefficientPolynomial a b c).eval (algebraMap ℝ (PeriodicCoefficient Lx) ε)) =
      (quadraticCoefficientPolynomial
        ((periodicSpatialEvolution Lx).toLinearMap a)
        ((periodicSpatialEvolution Lx).toLinearMap b)
        ((periodicSpatialEvolution Lx).toLinearMap c)).eval
          (algebraMap ℝ (PeriodicCoefficient Lx) ε) := by
  simp only [quadraticCoefficientPolynomial_eval, map_add, map_smul]

theorem coefficient_space_linear_polynomial {Lx : ℝ}
    (a b : PeriodicCoefficient Lx) (ε : ℝ) :
    (periodicSpatialEvolution Lx).toLinearMap
        ((linearCoefficientPolynomial a b).eval (algebraMap ℝ (PeriodicCoefficient Lx) ε)) =
      (linearCoefficientPolynomial
        ((periodicSpatialEvolution Lx).toLinearMap a)
        ((periodicSpatialEvolution Lx).toLinearMap b)).eval
          (algebraMap ℝ (PeriodicCoefficient Lx) ε) := by
  simp only [linearCoefficientPolynomial_eval, map_add, map_smul]

def periodicPhysicalKDensity (par : FieldParameters)
    (U w : Fin par.M → PeriodicCoefficient par.Lx) (j : Fin par.M) :
    PeriodicCoefficient par.Lx :=
  (1 / 2 : ℝ) • (U j ^ 2 * w j) + (beta par / 3) • (w j ^ 3) +
    w j * (periodicSpatialEvolution par.Lx).toLinearMap (U j) +
    (1 / 2 : ℝ) • (w j * periodicHamiltonianResolvent par
      (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (w i)) j) -
    par.gamma • (U j)

theorem physicalKDensityPolynomial_eval (par : FieldParameters)
    (U V W w q : Fin par.M → PeriodicCoefficient par.Lx) (ε : ℝ) (j : Fin par.M) :
    (physicalKDensityPolynomial par U V W w q j).eval
      (algebraMap ℝ (PeriodicCoefficient par.Lx) ε) =
    periodicPhysicalKDensity par
      (fun i => (quadraticCoefficientPolynomial (U i) (V i) (W i)).eval
        (algebraMap ℝ (PeriodicCoefficient par.Lx) ε))
      (fun i => (linearCoefficientPolynomial (w i) (q i)).eval
        (algebraMap ℝ (PeriodicCoefficient par.Lx) ε)) j := by
  simp only [physicalKDensityPolynomial, periodicPhysicalKDensity,
    Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_mul,
    Polynomial.eval_pow, Polynomial.eval_C,
    coefficient_space_quadratic_polynomial, coefficient_space_linear_polynomial]
  simp only [linearCoefficientPolynomial_eval, periodicHamiltonianResolvent_affine]
  simp only [Algebra.smul_def]
  ring

theorem periodicPhysicalKDensity_eval {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) :
    (periodicPhysicalKDensity par z.UCoefficient z.wCoefficient j : ℝ → ℝ) x =
      localPhysicalEnergy z j x - par.gamma * z.U j x := by
  change (1 / 2 : ℝ) * (z.U j x ^ 2 * z.w j x) +
    (beta par / 3) * z.w j x ^ 3 + z.w j x * deriv (z.U j) x +
    (1 / 2 : ℝ) * (z.w j x * latticeResolvent par (fun i => deriv (z.w i) x) j) -
    par.gamma * z.U j x = _
  unfold localPhysicalEnergy
  ring

theorem periodicPhysicalKDensity_integral (par : FieldParameters) (z : FieldCoordinates par) :
    par.h * periodicCoefficientIntegral par.Lx
      (∑ j : Fin par.M, periodicPhysicalKDensity par z.UCoefficient z.wCoefficient j) =
    physicalK par (latticeResolvent par) z := by
  have hdensity : par.h • (∑ j : Fin par.M,
      periodicPhysicalKDensity par z.UCoefficient z.wCoefficient j) =
      hamiltonianDensityW (periodicSpatialEvolution par.Lx)
        (fieldNatExtension z.UCoefficient) (fieldNatExtension z.wCoefficient) par.h par.M -
      par.gamma • (par.h • (∑ j : Fin par.M, z.UCoefficient j)) := by
    apply Subtype.ext
    funext x
    change coefficientEvaluation par.Lx x
      (par.h • ∑ j : Fin par.M, periodicPhysicalKDensity par z.UCoefficient z.wCoefficient j) =
      coefficientEvaluation par.Lx x
        (hamiltonianDensityW (periodicSpatialEvolution par.Lx)
          (fieldNatExtension z.UCoefficient) (fieldNatExtension z.wCoefficient) par.h par.M -
        par.gamma • (par.h • ∑ j : Fin par.M, z.UCoefficient j))
    simp only [map_sub, map_smul, map_sum, coefficientEvaluation_apply, smul_eq_mul]
    simp_rw [periodicPhysicalKDensity_eval]
    rw [physical_hamiltonianDensityW_eval]
    change par.h * (∑ j : Fin par.M, (localPhysicalEnergy z j x - par.gamma * z.U j x)) =
      par.h * (∑ j : Fin par.M, localPhysicalEnergy z j x) -
        par.gamma * (par.h * ∑ j : Fin par.M, z.U j x)
    rw [Finset.sum_sub_distrib, ← Finset.mul_sum]
    ring
  have hU : periodicCoefficientIntegral par.Lx
      (par.h • (∑ j : Fin par.M, z.UCoefficient j)) = z.physicalUIntegral := by
    rw [map_smul, map_sum]
    rfl
  rw [← smul_eq_mul, ← map_smul, hdensity, map_sub, map_smul,
    physical_hamiltonianDensityW_integral, hU]
  rfl

theorem physicalK_affine_polynomial_integral {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) (ε : ℝ) :
    par.h * periodicCoefficientIntegral par.Lx
      ((∑ j : Fin par.M, physicalKDensityPolynomial par z.UCoefficient
        (coordinateUTangent z v) (fun _ => coordinateUQuadratic par v) z.wCoefficient v.2 j).eval
          (algebraMap ℝ (PeriodicCoefficient par.Lx) ε)) =
      physicalK par (latticeResolvent par)
        (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)) := by
  have hU : (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)).UCoefficient =
      fun i => (quadraticCoefficientPolynomial (z.UCoefficient i) (coordinateUTangent z v i)
        (coordinateUQuadratic par v)).eval (algebraMap ℝ (PeriodicCoefficient par.Lx) ε) :=
    funext fun i => coordinateLine_U_polynomial z v ε i
  have hw : (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)).wCoefficient =
      fun i => (linearCoefficientPolynomial (z.wCoefficient i) (v.2 i)).eval
        (algebraMap ℝ (PeriodicCoefficient par.Lx) ε) :=
    funext fun i => coordinateLine_w_polynomial z v ε i
  simp only [Polynomial.eval_finset_sum, physicalKDensityPolynomial_eval]
  rw [← hU, ← hw]
  exact periodicPhysicalKDensity_integral par _

theorem physicalKRaw_integral_eq_gradient {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) :
    par.h * periodicCoefficientIntegral par.Lx
      (∑ j : Fin par.M, physicalKRawCoefficient par z.UCoefficient z.wCoefficient
        (coordinateUTangent z v) v.2 j) =
      coefficientGradientPairing par (physicalKGradient z) v := by
  have hr := physicalK_raw_variation_reduction par z.UCoefficient z.wCoefficient
    (coordinateUTangent z v) v.2
  have heq : (∑ j : Fin par.M,
      ((z.UCoefficient j * z.wCoefficient j -
        (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient j) -
        algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma) * coordinateUTangent z v j +
      ((1 / 2 : ℝ) • (z.UCoefficient j ^ 2) + beta par • (z.wCoefficient j ^ 2) +
        (periodicSpatialEvolution par.Lx).toLinearMap (z.UCoefficient j) +
        periodicHamiltonianResolvent par (fun i =>
          (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient i)) j) * v.2 j)) =
      ∑ j : Fin par.M,
        ((physicalKGradientP z j) * coordinateUTangent z v j + physicalKUnprojectedS z j * v.2 j) := by
    apply Finset.sum_congr rfl
    intro j _
    change ((z.UCoefficient j * z.wCoefficient j -
        (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient j) -
        algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma) * coordinateUTangent z v j +
      physicalKUnprojectedS z j * v.2 j) =
        ((z.UCoefficient j * z.wCoefficient j -
          algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma -
          (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient j)) * coordinateUTangent z v j +
          physicalKUnprojectedS z j * v.2 j)
    ring
  rw [heq] at hr
  change periodicCoefficientIntegral par.Lx
    (∑ j : Fin par.M, physicalKRawCoefficient par z.UCoefficient z.wCoefficient
      (coordinateUTangent z v) v.2 j) = _ at hr
  rw [hr]
  exact physicalK_coordinate_variation_reduction z v

/-- The actual physical Hamiltonian has the claimed reduced variational
gradient on every closed periodic coordinate direction. The proof uses its
literal integral and the exact polynomial affine restriction of the chart. -/
theorem physicalK_hasDerivAt_coordinateLine {par : FieldParameters} (z : FieldCoordinates par)
    (v : ClosedPeriodicPair par) :
    HasDerivAt (fun ε : ℝ => physicalK par (latticeResolvent par)
      (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)))
      (coefficientGradientPairing par (physicalKGradient z) v) 0 := by
  have h := physicalKPolynomialIntegral_hasDerivAt par z.UCoefficient
    (coordinateUTangent z v) (fun _ => coordinateUQuadratic par v) z.wCoefficient v.2
  have hfun : (fun ε : ℝ => par.h * periodicCoefficientIntegral par.Lx
      ((∑ j : Fin par.M, physicalKDensityPolynomial par z.UCoefficient
        (coordinateUTangent z v) (fun _ => coordinateUQuadratic par v) z.wCoefficient v.2 j).eval
          (algebraMap ℝ (PeriodicCoefficient par.Lx) ε))) =
      fun ε => physicalK par (latticeResolvent par)
        (closedPairCoordinates par ((z.closedP, z.closedS) + ε • v)) :=
    funext fun ε => physicalK_affine_polynomial_integral z v ε
  rw [hfun, physicalKRaw_integral_eq_gradient] at h
  exact h

#print axioms physicalK_hasDerivAt_coordinateLine
#print axioms physicalK_affine_polynomial_integral
#print axioms coordinateLine_U_polynomial
#print axioms coordinateLine_w_polynomial
end
end DLWLean
