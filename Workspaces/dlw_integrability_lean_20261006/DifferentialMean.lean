import FieldCoordinates
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Mul

namespace DLWLean
noncomputable section
open scoped BigOperators
open scoped ContDiff

theorem derivative_latticeMean {M : ℕ} (f : Fin M → ℝ → ℝ)
    (hf : ∀ j, Differentiable ℝ (f j)) (x : ℝ) :
    deriv (fun y => latticeMean (fun j => f j y)) x =
      latticeMean (fun j => deriv (f j) x) := by
  unfold latticeMean
  rw [deriv_div_const, deriv_fun_sum]
  intro j hj
  exact (hf j) x

theorem derivative_latticeMean_of_constant {M : ℕ} (f : Fin M → ℝ → ℝ)
    (hf : ∀ j, Differentiable ℝ (f j)) (a : ℝ)
    (ha : ∀ x, latticeMean (fun j => f j x) = a) (x : ℝ) :
    latticeMean (fun j => deriv (f j) x) = 0 := by
  rw [← derivative_latticeMean f hf x]
  have heq : (fun y => latticeMean (fun j => f j y)) = fun _ => a := funext ha
  rw [heq, deriv_const]

theorem second_derivative_latticeMean_of_constant {M : ℕ} (f : Fin M → ℝ → ℝ)
    (hf : ∀ j, ContDiff ℝ ∞ (f j)) (a : ℝ)
    (ha : ∀ x, latticeMean (fun j => f j x) = a) (x : ℝ) :
    latticeMean (fun j => deriv (deriv (f j)) x) = 0 := by
  apply derivative_latticeMean_of_constant (fun j => deriv (f j))
    (fun j => ((hf j).iterate_deriv 1).differentiable (by simp)) 0
  intro y
  exact derivative_latticeMean_of_constant f
    (fun j => (hf j).differentiable (by simp)) a ha y

theorem second_derivative_product (f g : ℝ → ℝ)
    (hf : ContDiff ℝ ∞ f) (hg : ContDiff ℝ ∞ g) (x : ℝ) :
    deriv (deriv (fun y => f y * g y)) x =
      deriv (deriv f) x * g x + 2 * deriv f x * deriv g x +
        f x * deriv (deriv g) x := by
  have df : Differentiable ℝ f := hf.differentiable (by simp)
  have dg : Differentiable ℝ g := hg.differentiable (by simp)
  have ddf : Differentiable ℝ (deriv f) := (hf.iterate_deriv 1).differentiable (by simp)
  have ddg : Differentiable ℝ (deriv g) := (hg.iterate_deriv 1).differentiable (by simp)
  have hfirst : deriv (fun y => f y * g y) =
      fun y => deriv f y * g y + f y * deriv g y := by
    funext y
    exact deriv_fun_mul (df y) (dg y)
  rw [hfirst]
  have hsecond := ((ddf x).hasDerivAt.mul (dg x).hasDerivAt).add
    ((df x).hasDerivAt.mul (ddg x).hasDerivAt)
  calc
    _ = (deriv (deriv f) x * g x + deriv f x * deriv g x) +
        (deriv f x * deriv g x + f x * deriv (deriv g) x) := hsecond.deriv
    _ = _ := by ring

/-- The required differentiated flux constraint is proved for actual
smooth closed periodic physical fields, not asserted as a jet premise. -/
theorem PeriodicPhysicalState.flux_second_mean_zero {par : FieldParameters}
    (state : PeriodicPhysicalState par) (x : ℝ) :
    latticeMean (fun j => deriv (deriv (state.U.value j)) x * state.w.value j x +
      2 * deriv (state.U.value j) x * deriv (state.w.value j) x +
        state.U.value j x * deriv (deriv (state.w.value j)) x) = 0 := by
  have hmean := second_derivative_latticeMean_of_constant
    (fun j y => state.U.value j y * state.w.value j y)
    (fun j => (state.U.smooth j).mul (state.w.smooth j))
    par.gamma state.mean_Uw x
  simpa only [second_derivative_product _ _ (state.U.smooth _) (state.w.smooth _) x]
    using hmean

theorem PeriodicPhysicalState.w_derivative_mean_zero {par : FieldParameters}
    (state : PeriodicPhysicalState par) (x : ℝ) :
    latticeMean (fun j => deriv (state.w.value j) x) = 0 :=
  derivative_latticeMean_of_constant state.w.value
    (fun j => (state.w.smooth j).differentiable (by simp)) par.c state.mean_w x

#print axioms PeriodicPhysicalState.flux_second_mean_zero
#print axioms PeriodicPhysicalState.w_derivative_mean_zero
end
end DLWLean
