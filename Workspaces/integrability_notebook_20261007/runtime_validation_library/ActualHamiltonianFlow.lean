import ActualHamiltonianDerivative
import ActualPhysicalSource

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

theorem coefficientLatticeMean_space (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) :
    (periodicSpatialEvolution par.Lx).toLinearMap (coefficientLatticeMean par f) =
      coefficientLatticeMean par (fun i => (periodicSpatialEvolution par.Lx).toLinearMap (f i)) := by
  unfold coefficientLatticeMean
  rw [map_smul, map_sum]

theorem physicalKUnprojectedS_space_eval {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) :
    ((periodicSpatialEvolution par.Lx).toLinearMap (physicalKUnprojectedS z j) : ℝ → ℝ) x =
      physicalFluxDerivativeJet (beta par) (fun i => z.U i x) (fun i => z.w i x)
        (fun i => deriv (z.U i) x) (fun i => deriv (z.w i) x)
        (fun i => deriv (deriv (z.U i)) x)
        (latticeResolvent par (fun i => deriv (deriv (z.w i)) x)) j := by
  simp only [physicalKUnprojectedS, map_add, map_smul, pow_two,
    (periodicSpatialEvolution par.Lx).leibniz, periodicHamiltonianResolvent_space]
  change (1 / 2 : ℝ) * (deriv (z.U j) x * z.U j x + z.U j x * deriv (z.U j) x) +
      beta par * (deriv (z.w j) x * z.w j x + z.w j x * deriv (z.w j) x) +
      deriv (deriv (z.U j)) x +
      latticeResolvent par (fun i => deriv (deriv (z.w i)) x) j = _
  unfold physicalFluxDerivativeJet
  ring

theorem physicalKGradientS_space_eval {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) :
    (closedSpatialDerivative par (physicalKGradientS z) j : ℝ → ℝ) x =
      latticeP0 (physicalFluxDerivativeJet (beta par)
        (fun i => z.U i x) (fun i => z.w i x)
        (fun i => deriv (z.U i) x) (fun i => deriv (z.w i) x)
        (fun i => deriv (deriv (z.U i)) x)
        (latticeResolvent par (fun i => deriv (deriv (z.w i)) x))) j := by
  change ((periodicSpatialEvolution par.Lx).toLinearMap
    (physicalKUnprojectedS z j - coefficientLatticeMean par (physicalKUnprojectedS z)) : ℝ → ℝ) x = _
  rw [map_sub, coefficientLatticeMean_space]
  change ((periodicSpatialEvolution par.Lx).toLinearMap (physicalKUnprojectedS z j) : ℝ → ℝ) x -
    (coefficientLatticeMean par (fun i =>
      (periodicSpatialEvolution par.Lx).toLinearMap (physicalKUnprojectedS z i)) : ℝ → ℝ) x = _
  rw [coefficientLatticeMean_eval]
  simp_rw [physicalKUnprojectedS_space_eval]
  rfl

theorem physicalKGradientP_space_eval {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) :
    (closedSpatialDerivative par (physicalKGradientP z) j : ℝ → ℝ) x =
      deriv (z.U j) x * z.w j x + z.U j x * deriv (z.w j) x -
        deriv (deriv (z.w j)) x := by
  change ((periodicSpatialEvolution par.Lx).toLinearMap
    (z.UCoefficient j * z.wCoefficient j -
      algebraMap ℝ (PeriodicCoefficient par.Lx) par.gamma -
      (periodicSpatialEvolution par.Lx).toLinearMap (z.wCoefficient j)) : ℝ → ℝ) x = _
  rw [map_sub, map_sub, (periodicSpatialEvolution par.Lx).leibniz,
    evolution_algebraMap_zero]
  rw [sub_zero]
  rfl

theorem StartPoint.p_time_derivative_from_U {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) (j : Fin par.M) :
    deriv (fun τ => (start.trajectory τ).p.value j x) t =
      deriv (fun τ => (start.trajectory τ).U j x) t -
        latticeMean (fun i => deriv (fun τ => (start.trajectory τ).U i x) t) := by
  have heq : (fun τ => (start.trajectory τ).p.value j x) = fun τ =>
      (start.trajectory τ).U j x - latticeMean (fun i => (start.trajectory τ).U i x) := by
    funext τ
    exact ((start.trajectory τ).recover_p j x).symm
  have hm : ContDiff ℝ ∞ (fun τ => latticeMean (fun i => (start.trajectory τ).U i x)) := by
    unfold latticeMean
    exact (ContDiff.sum fun i _ => start.U_time_smooth i x).div_const _
  rw [heq, deriv_fun_sub ((start.U_time_smooth j x).differentiable (by simp) t)
    (hm.differentiable (by simp) t)]
  rw [derivative_latticeMean (fun i τ => (start.trajectory τ).U i x)
    (fun i => (start.U_time_smooth i x).differentiable (by simp))]

theorem StartPoint.s_time_derivative_from_w {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) (j : Fin par.M) :
    deriv (fun τ => (start.trajectory τ).s.value j x) t =
      deriv (fun τ => (start.trajectory τ).w j x) t := by
  change deriv (fun τ => (start.trajectory τ).s.value j x) t =
    deriv (fun τ => par.c + (start.trajectory τ).s.value j x) t
  rw [deriv_const_add]

/-- The reduced Hamiltonian vector of the gradient computed from the
actual K integral is exactly the original physical trajectory in closed
coordinates. This proves the actual time-generator identification. -/
theorem StartPoint.physicalK_generates_coordinates {par : FieldParameters}
    (start : StartPoint par) (t x : ℝ) (j : Fin par.M) :
    ((reducedHamiltonianVector par (physicalKGradient (start.trajectory t))).1 j : ℝ → ℝ) x =
        deriv (fun τ => (start.trajectory τ).p.value j x) t ∧
      ((reducedHamiltonianVector par (physicalKGradient (start.trajectory t))).2 j : ℝ → ℝ) x =
        deriv (fun τ => (start.trajectory τ).s.value j x) t := by
  let F := physicalFluxDerivativeJet (beta par)
    (fun i => (start.trajectory t).U i x) (fun i => (start.trajectory t).w i x)
    (fun i => deriv ((start.trajectory t).U i) x)
    (fun i => deriv ((start.trajectory t).w i) x)
    (fun i => deriv (deriv ((start.trajectory t).U i)) x)
    (latticeResolvent par (fun i => deriv (deriv ((start.trajectory t).w i)) x))
  let commonMode := 2 * latticeMean (energyDerivativeJet (beta par)
    (fun i => (start.trajectory t).U i x) (fun i => (start.trajectory t).w i x)
    (fun i => deriv ((start.trajectory t).U i) x)
    (fun i => deriv ((start.trajectory t).w i) x)
    (fun i => deriv (deriv ((start.trajectory t).U i)) x)
    (latticeResolvent par (fun i => deriv ((start.trajectory t).w i) x))
    (latticeResolvent par (fun i => deriv (deriv ((start.trajectory t).w i)) x))) / par.c
  have hUt : (fun i => deriv (fun τ => (start.trajectory τ).U i x) t) =
      fun i => -F i + commonMode := funext (start.explicit_Ut_jets t x)
  have hmeanUt : latticeMean (fun i => deriv (fun τ => (start.trajectory τ).U i x) t) =
      -latticeMean F + commonMode := by
    rw [hUt, latticeMean_add, latticeMean_const par.M_ne_zero]
    unfold latticeMean
    rw [Finset.sum_neg_distrib]
    ring
  constructor
  · change -(closedSpatialDerivative par (physicalKGradientS (start.trajectory t)) j : ℝ → ℝ) x = _
    rw [physicalKGradientS_space_eval, start.p_time_derivative_from_U,
      congrFun hUt j, hmeanUt]
    change -(F j - latticeMean F) = -F j + commonMode - (-latticeMean F + commonMode)
    ring
  · change -(closedSpatialDerivative par (physicalKGradientP (start.trajectory t)) j : ℝ → ℝ) x = _
    rw [physicalKGradientP_space_eval, start.s_time_derivative_from_w, start.explicit_wt]
    unfold physicalWTimeJet
    ring

#print axioms StartPoint.physicalK_generates_coordinates
end
end DLWLean

