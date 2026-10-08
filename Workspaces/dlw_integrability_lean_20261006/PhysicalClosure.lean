import LatticeResolvent
import ClosureJets
import DifferentialMean

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem latticeResolvent_quadratic_mean_zero (par : FieldParameters)
    (f : Fin par.M → ℝ) : latticeMean (fun j => f j * latticeResolvent par f j) = 0 := by
  have hs := latticeResolvent_skew par f f
  have heq : (∑ j, latticeResolvent par f j * f j) =
      ∑ j, f j * latticeResolvent par f j := by
    apply Finset.sum_congr rfl
    intro j hj
    ring
  rw [heq] at hs
  have hz : (∑ j, f j * latticeResolvent par f j) = 0 := by linarith
  simp [latticeMean, hz]

/-- The original implicit difference equation and differentiated fixed
mean constraints imply the full explicit common-mode U equation.
All R terms are the previously constructed finite lattice operator.
These are physical PDE jet premises, not any Lax or spectral conclusion. -/
theorem physical_Ut_from_implicit_jets (par : FieldParameters)
    (U w Ux wx Uxx wxx Ut wt : Fin par.M → ℝ)
    (hmeanw : latticeMean w = par.c)
    (hwxxzero : latticeMean wxx = 0)
    (hfluxxx : latticeMean (fun j =>
      Uxx j * w j + 2 * Ux j * wx j + U j * wxx j) = 0)
    (hmeanTime : latticeMean (fun j => Ut j * w j + U j * wt j) = 0)
    (hwt : ∀ j, wt j = physicalWTimeJet U w Ux wx wxx j)
    (himplicit : ∀ j,
      deltaMinus par (fun i => Ut i + U i * Ux i +
        2 * beta par * w i * wx i) j + deltaMinus par Uxx j +
          averageMinus par wxx j = 0) :
    ∀ j, Ut j = -physicalFluxDerivativeJet (beta par) U w Ux wx Uxx
      (latticeResolvent par wxx) j +
        2 * latticeMean (energyDerivativeJet (beta par) U w Ux wx Uxx
          (latticeResolvent par wx) (latticeResolvent par wxx)) / par.c := by
  let F := physicalFluxDerivativeJet (beta par) U w Ux wx Uxx (latticeResolvent par wxx)
  let common := latticeMean (fun i => Ut i + F i)
  have hproject : latticeP0 wxx = wxx := by
    funext j
    simp [latticeP0, hwxxzero]
  have hdeltaR : ∀ j,
      deltaMinus par (latticeResolvent par wxx) j = averageMinus par wxx j := by
    intro j
    rw [deltaMinus_latticeResolvent, hproject]
  have hkernel : ∀ j, deltaMinus par (fun i => Ut i + F i) j = 0 := by
    intro j
    have hcombine : deltaMinus par (fun i => Ut i + F i) j =
        deltaMinus par (fun i => Ut i + U i * Ux i +
          2 * beta par * w i * wx i) j + deltaMinus par Uxx j +
            deltaMinus par (latticeResolvent par wxx) j := by
      unfold deltaMinus
      dsimp [F, physicalFluxDerivativeJet]
      ring
    rw [hcombine, hdeltaR j]
    exact himplicit j
  have hUt : ∀ j, Ut j = -F j + common := by
    intro j
    have hc := kernel_deltaMinus par (fun i => Ut i + F i) hkernel j
    change Ut j + F j = common at hc
    linarith
  have hmeanTime' : latticeMean (fun j =>
      (-F j + common) * w j + U j * physicalWTimeJet U w Ux wx wxx j) = 0 := by
    have hfun : (fun j => (-F j + common) * w j +
        U j * physicalWTimeJet U w Ux wx wxx j) =
        (fun j => Ut j * w j + U j * wt j) := by
      funext j
      rw [← hUt j, hwt j]
    rw [hfun]
    exact hmeanTime
  have hcommon := common_time_mode_from_mean_constraint (beta par) par.c common
    par.c_ne_zero U w Ux wx Uxx wxx (latticeResolvent par wx)
      (latticeResolvent par wxx) hmeanw hfluxxx
        (latticeResolvent_quadratic_mean_zero par wx) hmeanTime'
  intro j
  rw [hUt j, hcommon]

#print axioms physical_Ut_from_implicit_jets
end
end DLWLean
