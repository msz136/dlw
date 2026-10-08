import StartPoint
import PhysicalClosure
import FiniteLinearCalculus
import PeriodicCoefficients
import Mathlib.Analysis.Calculus.ContDiff.Operations

/-! The physical source is derived from the original implicit PDE on an
actual smooth trajectory. Differentiated mean constraints and the local
energy derivative are conclusions, not extra source assumptions. -/
namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

theorem StartPoint.p_time_smooth {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) (x : ℝ) :
    ContDiff ℝ ∞ (fun t => (start.trajectory t).p.value j x) := by
  exact (start.joint_smooth_p j).comp (contDiff_id.prodMk contDiff_const)

theorem StartPoint.s_time_smooth {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) (x : ℝ) :
    ContDiff ℝ ∞ (fun t => (start.trajectory t).s.value j x) := by
  exact (start.joint_smooth_s j).comp (contDiff_id.prodMk contDiff_const)

theorem StartPoint.U_time_smooth {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) (x : ℝ) :
    ContDiff ℝ ∞ (fun t => (start.trajectory t).U j x) := by
  unfold FieldCoordinates.U FieldCoordinates.commonU FieldCoordinates.meanPS latticeMean
  exact (start.p_time_smooth j x).add
    ((contDiff_const.sub ((ContDiff.sum fun i _ =>
      (start.p_time_smooth i x).mul (start.s_time_smooth i x)).div_const _)).div_const _)

theorem StartPoint.w_time_smooth {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) (x : ℝ) :
    ContDiff ℝ ∞ (fun t => (start.trajectory t).w j x) := by
  exact contDiff_const.add (start.s_time_smooth j x)

def FieldCoordinates.physicalState {par : FieldParameters} (z : FieldCoordinates par) :
    PeriodicPhysicalState par where
  U := ⟨z.U, z.U_smooth, z.U_periodic⟩
  w := ⟨z.w, z.w_smooth, z.w_periodic⟩
  mean_w := z.mean_w
  mean_Uw := z.mean_Uw

theorem StartPoint.mean_time_constraint {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) :
    latticeMean (fun j =>
      deriv (fun τ => (start.trajectory τ).U j x) t * (start.trajectory t).w j x +
      (start.trajectory t).U j x *
        deriv (fun τ => (start.trajectory τ).w j x) t) = 0 := by
  have hmean := derivative_latticeMean_of_constant
    (fun j τ => (start.trajectory τ).U j x * (start.trajectory τ).w j x)
    (fun j => ((start.U_time_smooth j x).mul (start.w_time_smooth j x)).differentiable
      (by simp)) par.gamma (fun τ => (start.trajectory τ).mean_Uw x) t
  have hd : ∀ j, deriv (fun τ =>
      (start.trajectory τ).U j x * (start.trajectory τ).w j x) t =
      deriv (fun τ => (start.trajectory τ).U j x) t * (start.trajectory t).w j x +
        (start.trajectory t).U j x * deriv (fun τ => (start.trajectory τ).w j x) t := by
    intro j
    exact deriv_fun_mul ((start.U_time_smooth j x).differentiable (by simp) t)
      ((start.w_time_smooth j x).differentiable (by simp) t)
  simpa only [hd] using hmean

theorem second_derivative_add (f g : ℝ → ℝ)
    (hf : ContDiff ℝ ∞ f) (hg : ContDiff ℝ ∞ g) (x : ℝ) :
    deriv (deriv (fun y => f y + g y)) x =
      deriv (deriv f) x + deriv (deriv g) x := by
  have hfirst : deriv (fun y => f y + g y) = fun y => deriv f y + deriv g y := by
    funext y
    exact deriv_fun_add (hf.differentiable (by simp) y) (hg.differentiable (by simp) y)
  rw [hfirst]
  exact deriv_fun_add ((hf.iterate_deriv 1).differentiable (by simp) x)
    ((hg.iterate_deriv 1).differentiable (by simp) x)

theorem smooth_finite_linear_map {M N : ℕ}
    (T : (Fin M → ℝ) →ₗ[ℝ] (Fin N → ℝ))
    (f : Fin M → ℝ → ℝ) (hf : ∀ j, ContDiff ℝ ∞ (f j)) (j : Fin N) :
    ContDiff ℝ ∞ (fun x => T (fun i => f i x) j) := by
  have h := T.toContinuousLinearMap.contDiff.comp (contDiff_pi.mpr hf)
  exact (contDiff_pi.mp h) j

theorem StartPoint.implicit_spatial_jets {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) (j : Fin par.M) :
    deltaMinus par (fun i => deriv (fun τ => (start.trajectory τ).U i x) t +
      (start.trajectory t).U i x * deriv ((start.trajectory t).U i) x +
      2 * beta par * (start.trajectory t).w i x *
        deriv ((start.trajectory t).w i) x) j +
      deltaMinus par (fun i => deriv (deriv ((start.trajectory t).U i)) x) j +
      averageMinus par (fun i => deriv (deriv ((start.trajectory t).w i)) x) j = 0 := by
  have hpde := (start.physical_equations t x j).1
  have hflux : ∀ i, deriv (fun y => (start.trajectory t).U i y ^ 2 / 2 +
      beta par * (start.trajectory t).w i y ^ 2) x =
      (start.trajectory t).U i x * deriv ((start.trajectory t).U i) x +
        2 * beta par * (start.trajectory t).w i x *
          deriv ((start.trajectory t).w i) x := by
    intro i
    exact derivative_physical_flux (beta par) _ _
      ((start.trajectory t).U_smooth i |>.differentiable (by simp))
      ((start.trajectory t).w_smooth i |>.differentiable (by simp)) x
  have hsecond := second_derivative_add
    (fun y => deltaMinus par (fun i => (start.trajectory t).U i y) j)
    (fun y => averageMinus par (fun i => (start.trajectory t).w i y) j)
    (smooth_finite_linear_map (deltaMinusLinearMap par) _
      (start.trajectory t).U_smooth j)
    (smooth_finite_linear_map (averageMinusLinearMap par) _
      (start.trajectory t).w_smooth j) x
  have hd := second_derivative_finite_linear_map (deltaMinusLinearMap par) _
    (start.trajectory t).U_smooth x j
  have ha := second_derivative_finite_linear_map (averageMinusLinearMap par) _
    (start.trajectory t).w_smooth x j
  change deriv (deriv (fun y => deltaMinus par (fun i => (start.trajectory t).U i y) j)) x =
    deltaMinus par (fun i => deriv (deriv ((start.trajectory t).U i)) x) j at hd
  change deriv (deriv (fun y => averageMinus par (fun i => (start.trajectory t).w i y) j)) x =
    averageMinus par (fun i => deriv (deriv ((start.trajectory t).w i)) x) j at ha
  rw [hd, ha] at hsecond
  simp only [hflux, hsecond] at hpde
  simpa only [add_assoc] using hpde

theorem StartPoint.explicit_wt {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) (j : Fin par.M) :
    deriv (fun τ => (start.trajectory τ).w j x) t =
      physicalWTimeJet (fun i => (start.trajectory t).U i x)
        (fun i => (start.trajectory t).w i x)
        (fun i => deriv ((start.trajectory t).U i) x)
        (fun i => deriv ((start.trajectory t).w i) x)
        (fun i => deriv (deriv ((start.trajectory t).w i)) x) j := by
  have hpde := (start.physical_equations t x j).2
  rw [deriv_fun_mul ((start.trajectory t).U_smooth j |>.differentiable (by simp) x)
    ((start.trajectory t).w_smooth j |>.differentiable (by simp) x)] at hpde
  unfold physicalWTimeJet
  linarith

theorem StartPoint.explicit_Ut_jets {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) (j : Fin par.M) :
    deriv (fun τ => (start.trajectory τ).U j x) t =
      -physicalFluxDerivativeJet (beta par)
        (fun i => (start.trajectory t).U i x) (fun i => (start.trajectory t).w i x)
        (fun i => deriv ((start.trajectory t).U i) x)
        (fun i => deriv ((start.trajectory t).w i) x)
        (fun i => deriv (deriv ((start.trajectory t).U i)) x)
        (latticeResolvent par (fun i => deriv (deriv ((start.trajectory t).w i)) x)) j +
      2 * latticeMean (energyDerivativeJet (beta par)
        (fun i => (start.trajectory t).U i x) (fun i => (start.trajectory t).w i x)
        (fun i => deriv ((start.trajectory t).U i) x)
        (fun i => deriv ((start.trajectory t).w i) x)
        (fun i => deriv (deriv ((start.trajectory t).U i)) x)
        (latticeResolvent par (fun i => deriv ((start.trajectory t).w i) x))
        (latticeResolvent par (fun i => deriv (deriv ((start.trajectory t).w i)) x))) /
        par.c := by
  refine physical_Ut_from_implicit_jets par
    (fun i => (start.trajectory t).U i x) (fun i => (start.trajectory t).w i x)
    (fun i => deriv ((start.trajectory t).U i) x)
    (fun i => deriv ((start.trajectory t).w i) x)
    (fun i => deriv (deriv ((start.trajectory t).U i)) x)
    (fun i => deriv (deriv ((start.trajectory t).w i)) x)
    (fun i => deriv (fun τ => (start.trajectory τ).U i x) t)
    (fun i => deriv (fun τ => (start.trajectory τ).w i x) t) ?_ ?_ ?_ ?_ ?_ ?_ j
  · exact (start.trajectory t).mean_w x
  · exact second_derivative_latticeMean_of_constant (start.trajectory t).w
      (start.trajectory t).w_smooth par.c (start.trajectory t).mean_w x
  · exact (start.trajectory t).physicalState.flux_second_mean_zero x
  · exact start.mean_time_constraint t x
  · exact start.explicit_wt t x
  · exact start.implicit_spatial_jets t x

def localPhysicalEnergy {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) : ℝ :=
  z.U j x ^ 2 * z.w j x / 2 + beta par * z.w j x ^ 3 / 3 +
    z.w j x * deriv (z.U j) x +
      z.w j x * latticeResolvent par (fun i => deriv (z.w i) x) j / 2

theorem derivative_localPhysicalEnergy {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) (x : ℝ) :
    deriv (localPhysicalEnergy z j) x =
      energyDerivativeJet (beta par) (fun i => z.U i x) (fun i => z.w i x)
        (fun i => deriv (z.U i) x) (fun i => deriv (z.w i) x)
        (fun i => deriv (deriv (z.U i)) x)
        (latticeResolvent par (fun i => deriv (z.w i) x))
        (latticeResolvent par (fun i => deriv (deriv (z.w i)) x)) j := by
  have hU := (z.U_smooth j).differentiable (by simp) x |>.hasDerivAt
  have hw := (z.w_smooth j).differentiable (by simp) x |>.hasDerivAt
  have hUx := ((z.U_smooth j).iterate_deriv 1).differentiable (by simp) x |>.hasDerivAt
  have hR : HasDerivAt (fun y => latticeResolvent par (fun i => deriv (z.w i) y) j)
      (latticeResolvent par (fun i => deriv (deriv (z.w i)) x) j) x := by
    have h := (smooth_finite_linear_map (latticeResolvent par) (fun i => deriv (z.w i))
      (fun i => (z.w_smooth i).iterate_deriv 1) j).differentiable (by simp) x |>.hasDerivAt
    rw [derivative_finite_linear_map (latticeResolvent par) (fun i => deriv (z.w i))
      (fun i => ((z.w_smooth i).iterate_deriv 1).differentiable (by simp)) x j] at h
    exact h
  have h := ((((hU.pow 2).mul hw).div_const 2).add
    ((hw.pow 3).const_mul (beta par) |>.div_const 3)).add (hw.mul hUx) |>.add
      ((hw.mul hR).div_const 2)
  calc
    _ = _ := h.deriv
    _ = _ := by unfold energyDerivativeJet; norm_num; ring

theorem localPhysicalEnergy_smooth {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) : ContDiff ℝ ∞ (localPhysicalEnergy z j) := by
  exact ((((z.U_smooth j).pow 2 |>.mul (z.w_smooth j)).div_const 2).add
    ((contDiff_const.mul ((z.w_smooth j).pow 3)).div_const 3)).add
      ((z.w_smooth j).mul ((z.U_smooth j).iterate_deriv 1)) |>.add
        (((z.w_smooth j).mul (smooth_finite_linear_map (latticeResolvent par)
          (fun i => deriv (z.w i)) (fun i => (z.w_smooth i).iterate_deriv 1) j)).div_const 2)

def meanLocalPhysicalEnergy {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) : ℝ := latticeMean (fun j => localPhysicalEnergy z j x)

theorem derivative_meanLocalPhysicalEnergy {par : FieldParameters} (z : FieldCoordinates par)
    (x : ℝ) :
    deriv (meanLocalPhysicalEnergy z) x = latticeMean
      (energyDerivativeJet (beta par) (fun i => z.U i x) (fun i => z.w i x)
        (fun i => deriv (z.U i) x) (fun i => deriv (z.w i) x)
        (fun i => deriv (deriv (z.U i)) x)
        (latticeResolvent par (fun i => deriv (z.w i) x))
        (latticeResolvent par (fun i => deriv (deriv (z.w i)) x))) := by
  change deriv (fun y => latticeMean (fun j => localPhysicalEnergy z j y)) x = _
  rw [derivative_latticeMean (localPhysicalEnergy z)
    (fun j => (localPhysicalEnergy_smooth z j).differentiable (by simp))]
  simp_rw [derivative_localPhysicalEnergy]

/-- Actual explicit coefficient source PDE, with the common mode written
as the derivative of the actual local physical energy density. -/
theorem StartPoint.explicit_Ut {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) (j : Fin par.M) :
    deriv (fun τ => (start.trajectory τ).U j x) t =
      -((start.trajectory t).U j x * deriv ((start.trajectory t).U j) x +
        par.h ^ 2 / 16 * (start.trajectory t).w j x *
          deriv ((start.trajectory t).w j) x +
        deriv (deriv ((start.trajectory t).U j)) x +
        latticeResolvent par (fun i => deriv (deriv ((start.trajectory t).w i)) x) j) +
      2 * deriv (meanLocalPhysicalEnergy (start.trajectory t)) x / par.c := by
  rw [derivative_meanLocalPhysicalEnergy]
  have ht := start.explicit_Ut_jets t x j
  convert ht using 1 <;> unfold physicalFluxDerivativeJet beta <;> ring

theorem periodic_finite_linear_map {M N : ℕ} (Lx : ℝ)
    (T : (Fin M → ℝ) →ₗ[ℝ] (Fin N → ℝ)) (f : Fin M → ℝ → ℝ)
    (hf : ∀ j, Function.Periodic (f j) Lx) (j : Fin N) :
    Function.Periodic (fun x => T (fun i => f i x) j) Lx := by
  intro x
  have heq : (fun i => f i (x + Lx)) = fun i => f i x := funext fun i => hf i x
  change T (fun i => f i (x + Lx)) j = T (fun i => f i x) j
  rw [heq]

theorem localPhysicalEnergy_periodic {par : FieldParameters} (z : FieldCoordinates par)
    (j : Fin par.M) : Function.Periodic (localPhysicalEnergy z j) par.Lx := by
  have hU := periodic_derivative_of_periodic (z.U j) par.Lx (z.U_periodic j)
  have hw := periodic_derivative_of_periodic (z.w j) par.Lx (z.w_periodic j)
  have hR := periodic_finite_linear_map par.Lx (latticeResolvent par)
    (fun i => deriv (z.w i))
    (fun i => periodic_derivative_of_periodic (z.w i) par.Lx (z.w_periodic i)) j
  intro x
  have hRx := hR x
  dsimp at hRx
  unfold localPhysicalEnergy
  rw [z.U_periodic j x, z.w_periodic j x, hU x, hRx]

theorem meanLocalPhysicalEnergy_smooth {par : FieldParameters} (z : FieldCoordinates par) :
    ContDiff ℝ ∞ (meanLocalPhysicalEnergy z) := by
  unfold meanLocalPhysicalEnergy latticeMean
  exact (ContDiff.sum fun j _ => localPhysicalEnergy_smooth z j).div_const _

theorem meanLocalPhysicalEnergy_periodic {par : FieldParameters} (z : FieldCoordinates par) :
    Function.Periodic (meanLocalPhysicalEnergy z) par.Lx := by
  intro x
  unfold meanLocalPhysicalEnergy latticeMean
  congr 1
  apply Finset.sum_congr rfl
  intro j _
  exact localPhysicalEnergy_periodic z j x

/-- Periodic heat potential built from the physical fields and the
constructed lattice resolvent. v0 is a spatial constant. -/
def physicalHeatPotential {par : FieldParameters} (z : FieldCoordinates par)
    (v0 : ℝ) (j : Fin par.M) (x : ℝ) : ℝ :=
  latticeHeatPotential par (fun i => deriv (z.w i) x)
    (-meanLocalPhysicalEnergy z x / par.c + v0) j

theorem physicalHeatPotential_smooth {par : FieldParameters} (z : FieldCoordinates par)
    (v0 : ℝ) (j : Fin par.M) : ContDiff ℝ ∞ (physicalHeatPotential z v0 j) := by
  exact (((smooth_finite_linear_map (latticeResolvent par) (fun i => deriv (z.w i))
    (fun i => (z.w_smooth i).iterate_deriv 1) j).div_const 2).sub
      ((contDiff_const.mul ((z.w_smooth j).iterate_deriv 1)).div_const 4)).add
        ((meanLocalPhysicalEnergy_smooth z).neg.div_const par.c |>.add contDiff_const)

theorem physicalHeatPotential_periodic {par : FieldParameters} (z : FieldCoordinates par)
    (v0 : ℝ) (j : Fin par.M) : Function.Periodic (physicalHeatPotential z v0 j) par.Lx := by
  have hw := periodic_derivative_of_periodic (z.w j) par.Lx (z.w_periodic j)
  have hR := periodic_finite_linear_map par.Lx (latticeResolvent par)
    (fun i => deriv (z.w i))
    (fun i => periodic_derivative_of_periodic (z.w i) par.Lx (z.w_periodic i)) j
  intro x
  have hRx := hR x
  dsimp at hRx
  unfold physicalHeatPotential latticeHeatPotential
  dsimp only
  rw [hRx, hw x, meanLocalPhysicalEnergy_periodic z x]

theorem physicalHeatPotential_shift {par : FieldParameters} (z : FieldCoordinates par)
    (v0 : ℝ) (j : Fin par.M) (x : ℝ) :
    physicalHeatPotential z v0 (nextSite par j) x =
      physicalHeatPotential z v0 j x + par.h * deriv (z.w j) x / 2 := by
  have hd := derivative_latticeMean_of_constant z.w
    (fun i => (z.w_smooth i).differentiable (by simp)) par.c z.mean_w x
  have hs := latticeHeatPotential_shift par (fun i => deriv (z.w i) x) hd
    (-meanLocalPhysicalEnergy z x / par.c + v0) j
  change physicalHeatPotential z v0 (nextSite par j) x -
    physicalHeatPotential z v0 j x = par.h * deriv (z.w j) x / 2 at hs
  linarith

#print axioms StartPoint.mean_time_constraint
#print axioms StartPoint.explicit_Ut_jets
#print axioms derivative_localPhysicalEnergy
#print axioms StartPoint.explicit_Ut
#print axioms physicalHeatPotential_shift
end
end DLWLean
