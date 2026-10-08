import PeriodicCoefficients
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Prod

namespace DLWLean
noncomputable section
open scoped ContDiff

def spacetimeSpaceDerivative (f : ℝ × ℝ → ℝ) (tx : ℝ × ℝ) : ℝ :=
  deriv (fun x => f (tx.1, x)) tx.2

def spacetimeTimeDerivative (f : ℝ × ℝ → ℝ) (tx : ℝ × ℝ) : ℝ :=
  deriv (fun t => f (t, tx.2)) tx.1

theorem spacetimeSpaceDerivative_eq_fderiv (f : ℝ × ℝ → ℝ)
    (hf : ContDiff ℝ ∞ f) (tx : ℝ × ℝ) :
    spacetimeSpaceDerivative f tx = fderiv ℝ f tx (0, 1) := by
  have h := (hf.differentiable (by simp) tx).hasFDerivAt.comp_hasDerivAt tx.2
    ((hasDerivAt_const tx.2 tx.1).prodMk (hasDerivAt_id tx.2))
  simpa only [spacetimeSpaceDerivative, Function.comp_def, Prod.eta, id_eq] using h.deriv

theorem spacetimeTimeDerivative_eq_fderiv (f : ℝ × ℝ → ℝ)
    (hf : ContDiff ℝ ∞ f) (tx : ℝ × ℝ) :
    spacetimeTimeDerivative f tx = fderiv ℝ f tx (1, 0) := by
  have h := (hf.differentiable (by simp) tx).hasFDerivAt.comp_hasDerivAt tx.1
    ((hasDerivAt_id tx.1).prodMk (hasDerivAt_const tx.1 tx.2))
  simpa only [spacetimeTimeDerivative, Function.comp_def, Prod.eta, id_eq] using h.deriv

theorem spacetimeSpaceDerivative_smooth (f : ℝ × ℝ → ℝ)
    (hf : ContDiff ℝ ∞ f) : ContDiff ℝ ∞ (spacetimeSpaceDerivative f) := by
  have heq : spacetimeSpaceDerivative f = fun tx => fderiv ℝ f tx (0, 1) :=
    funext (spacetimeSpaceDerivative_eq_fderiv f hf)
  rw [heq]
  exact (contDiff_infty_iff_fderiv.mp hf).2.clm_apply contDiff_const

theorem spacetimeTimeDerivative_smooth (f : ℝ × ℝ → ℝ)
    (hf : ContDiff ℝ ∞ f) : ContDiff ℝ ∞ (spacetimeTimeDerivative f) := by
  have heq : spacetimeTimeDerivative f = fun tx => fderiv ℝ f tx (1, 0) :=
    funext (spacetimeTimeDerivative_eq_fderiv f hf)
  rw [heq]
  exact (contDiff_infty_iff_fderiv.mp hf).2.clm_apply contDiff_const

/-- Genuine smooth spacetime coefficients, periodic in the spatial
variable. Both source derivatives act before any time evaluation. -/
def periodicSpacetimeCoefficientAlgebra (Lx : ℝ) : Subalgebra ℝ (ℝ × ℝ → ℝ) where
  carrier := {f | ContDiff ℝ ∞ f ∧ ∀ t, Function.Periodic (fun x => f (t, x)) Lx}
  algebraMap_mem' r := ⟨contDiff_const, fun _ _ => rfl⟩
  add_mem' := by
    intro f g hf hg
    refine ⟨hf.1.add hg.1, ?_⟩
    intro t x
    change f (t, x + Lx) + g (t, x + Lx) = f (t, x) + g (t, x)
    exact congrArg₂ (fun a b : ℝ => a + b) (hf.2 t x) (hg.2 t x)
  mul_mem' := by
    intro f g hf hg
    refine ⟨hf.1.mul hg.1, ?_⟩
    intro t x
    change f (t, x + Lx) * g (t, x + Lx) = f (t, x) * g (t, x)
    exact congrArg₂ (fun a b : ℝ => a * b) (hf.2 t x) (hg.2 t x)

abbrev PeriodicSpacetimeCoefficient (Lx : ℝ) := periodicSpacetimeCoefficientAlgebra Lx

theorem PeriodicSpacetimeCoefficient.space_slice_smooth {Lx : ℝ}
    (f : PeriodicSpacetimeCoefficient Lx) (t : ℝ) :
    ContDiff ℝ ∞ (fun x => (f : ℝ × ℝ → ℝ) (t, x)) :=
  f.property.1.comp (contDiff_const.prodMk contDiff_id)

theorem PeriodicSpacetimeCoefficient.time_slice_smooth {Lx : ℝ}
    (f : PeriodicSpacetimeCoefficient Lx) (x : ℝ) :
    ContDiff ℝ ∞ (fun t => (f : ℝ × ℝ → ℝ) (t, x)) :=
  f.property.1.comp (contDiff_id.prodMk contDiff_const)

def PeriodicSpacetimeCoefficient.spaceDerivative {Lx : ℝ}
    (f : PeriodicSpacetimeCoefficient Lx) : PeriodicSpacetimeCoefficient Lx :=
  ⟨spacetimeSpaceDerivative (f : ℝ × ℝ → ℝ),
    spacetimeSpaceDerivative_smooth _ f.property.1,
    fun t => periodic_derivative_of_periodic _ Lx (f.property.2 t)⟩

def PeriodicSpacetimeCoefficient.timeDerivative {Lx : ℝ}
    (f : PeriodicSpacetimeCoefficient Lx) : PeriodicSpacetimeCoefficient Lx :=
  ⟨spacetimeTimeDerivative (f : ℝ × ℝ → ℝ),
    spacetimeTimeDerivative_smooth _ f.property.1, by
      intro t x
      change deriv (fun τ => (f : ℝ × ℝ → ℝ) (τ, x + Lx)) t =
        deriv (fun τ => (f : ℝ × ℝ → ℝ) (τ, x)) t
      congr 1
      funext τ
      exact f.property.2 τ x⟩

def periodicSpacetimeSpaceEvolution (Lx : ℝ) :
    AlgebraEvolution (PeriodicSpacetimeCoefficient Lx) where
  toLinearMap :=
    { toFun := PeriodicSpacetimeCoefficient.spaceDerivative
      map_add' := by
        intro f g
        apply Subtype.ext
        funext tx
        exact ((PeriodicSpacetimeCoefficient.space_slice_smooth f tx.1).differentiable (by simp) tx.2 |>.hasDerivAt).add
          ((PeriodicSpacetimeCoefficient.space_slice_smooth g tx.1).differentiable (by simp) tx.2 |>.hasDerivAt) |>.deriv
      map_smul' := by
        intro r f
        apply Subtype.ext
        funext tx
        exact ((PeriodicSpacetimeCoefficient.space_slice_smooth f tx.1).differentiable (by simp) tx.2 |>.hasDerivAt).const_mul r |>.deriv }
  leibniz := by
    intro f g
    apply Subtype.ext
    funext tx
    exact ((PeriodicSpacetimeCoefficient.space_slice_smooth f tx.1).differentiable (by simp) tx.2 |>.hasDerivAt).mul
      ((PeriodicSpacetimeCoefficient.space_slice_smooth g tx.1).differentiable (by simp) tx.2 |>.hasDerivAt) |>.deriv

def periodicSpacetimeTimeEvolution (Lx : ℝ) :
    AlgebraEvolution (PeriodicSpacetimeCoefficient Lx) where
  toLinearMap :=
    { toFun := PeriodicSpacetimeCoefficient.timeDerivative
      map_add' := by
        intro f g
        apply Subtype.ext
        funext tx
        exact ((PeriodicSpacetimeCoefficient.time_slice_smooth f tx.2).differentiable (by simp) tx.1 |>.hasDerivAt).add
          ((PeriodicSpacetimeCoefficient.time_slice_smooth g tx.2).differentiable (by simp) tx.1 |>.hasDerivAt) |>.deriv
      map_smul' := by
        intro r f
        apply Subtype.ext
        funext tx
        exact ((PeriodicSpacetimeCoefficient.time_slice_smooth f tx.2).differentiable (by simp) tx.1 |>.hasDerivAt).const_mul r |>.deriv }
  leibniz := by
    intro f g
    apply Subtype.ext
    funext tx
    exact ((PeriodicSpacetimeCoefficient.time_slice_smooth f tx.2).differentiable (by simp) tx.1 |>.hasDerivAt).mul
      ((PeriodicSpacetimeCoefficient.time_slice_smooth g tx.2).differentiable (by simp) tx.1 |>.hasDerivAt) |>.deriv

#print axioms periodicSpacetimeSpaceEvolution
#print axioms periodicSpacetimeTimeEvolution
end
end DLWLean

