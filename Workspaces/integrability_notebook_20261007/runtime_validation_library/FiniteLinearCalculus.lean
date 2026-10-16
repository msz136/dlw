import LatticeResolvent
import DifferentialMean
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Normed.Module.FiniteDimension

namespace DLWLean
noncomputable section
open scoped ContDiff

theorem derivative_finite_linear_map {M N : ℕ}
    (T : (Fin M → ℝ) →ₗ[ℝ] (Fin N → ℝ))
    (f : Fin M → ℝ → ℝ) (hf : ∀ j, Differentiable ℝ (f j))
    (x : ℝ) (j : Fin N) :
    deriv (fun y => T (fun i => f i y) j) x = T (fun i => deriv (f i) x) j := by
  let Tc := T.toContinuousLinearMap
  have hv : HasDerivAt (fun y i => f i y) (fun i => deriv (f i) x) x :=
    hasDerivAt_pi.mpr fun i => (hf i x).hasDerivAt
  have hT := Tc.hasFDerivAt.comp_hasDerivAt x hv
  have hj := hasDerivAt_pi.mp hT j
  simpa [Function.comp_def, Tc] using hj.deriv

def deltaMinusLinearMap (par : FieldParameters) :
    (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ) where
  toFun := deltaMinus par
  map_add' f g := by funext j; simp only [deltaMinus, Pi.add_apply]; ring
  map_smul' r f := by
    funext j
    simp only [deltaMinus, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

def averageMinusLinearMap (par : FieldParameters) :
    (Fin par.M → ℝ) →ₗ[ℝ] (Fin par.M → ℝ) where
  toFun := averageMinus par
  map_add' f g := by funext j; simp only [averageMinus, Pi.add_apply]; ring
  map_smul' r f := by
    funext j
    simp only [averageMinus, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    ring

theorem second_derivative_finite_linear_map {M N : ℕ}
    (T : (Fin M → ℝ) →ₗ[ℝ] (Fin N → ℝ))
    (f : Fin M → ℝ → ℝ) (hf : ∀ j, ContDiff ℝ ∞ (f j))
    (x : ℝ) (j : Fin N) :
    deriv (deriv (fun y => T (fun i => f i y) j)) x =
      T (fun i => deriv (deriv (f i)) x) j := by
  have hfirst : deriv (fun y => T (fun i => f i y) j) =
      fun y => T (fun i => deriv (f i) y) j := by
    funext y
    exact derivative_finite_linear_map T f
      (fun i => (hf i).differentiable (by simp)) y j
  rw [hfirst]
  exact derivative_finite_linear_map T (fun i => deriv (f i))
    (fun i => ((hf i).iterate_deriv 1).differentiable (by simp)) x j

theorem derivative_physical_flux (β : ℝ) (U w : ℝ → ℝ)
    (hU : Differentiable ℝ U) (hw : Differentiable ℝ w) (x : ℝ) :
    deriv (fun y => (U y) ^ 2 / 2 + β * (w y) ^ 2) x =
      U x * deriv U x + 2 * β * w x * deriv w x := by
  have h := ((hU x).hasDerivAt.pow 2).div_const 2 |>.add
    (((hw x).hasDerivAt.pow 2).const_mul β)
  calc
    _ = (2 * U x ^ (2 - 1) * deriv U x) / 2 +
        β * (2 * w x ^ (2 - 1) * deriv w x) := h.deriv
    _ = _ := by norm_num; ring

#print axioms derivative_finite_linear_map
#print axioms second_derivative_finite_linear_map
end
end DLWLean
