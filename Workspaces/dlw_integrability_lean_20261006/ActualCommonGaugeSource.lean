import PeriodicSpacetimeCoefficients
import SmoothPrimitive
import CommonGauge

namespace DLWLean
noncomputable section
open scoped ContDiff

/-- All jointly smooth coefficient functions. A common-U gauge primitive
belongs here even when its spatial mean is nonzero. -/
def smoothSpacetimeCoefficientAlgebra : Subalgebra ℝ (ℝ × ℝ → ℝ) where
  carrier := {f | ContDiff ℝ ∞ f}
  algebraMap_mem' r := by
    change ContDiff ℝ ∞ (fun _ : ℝ × ℝ => r)
    exact contDiff_const
  add_mem' := by
    intro f g hf hg
    change ContDiff ℝ ∞ f at hf
    change ContDiff ℝ ∞ g at hg
    exact hf.add hg
  mul_mem' := by
    intro f g hf hg
    change ContDiff ℝ ∞ f at hf
    change ContDiff ℝ ∞ g at hg
    exact hf.mul hg

abbrev SmoothSpacetimeCoefficient := smoothSpacetimeCoefficientAlgebra

theorem SmoothSpacetimeCoefficient.joint_smooth (f : SmoothSpacetimeCoefficient) :
    ContDiff ℝ ∞ (f : ℝ × ℝ → ℝ) := f.property

theorem SmoothSpacetimeCoefficient.space_slice_smooth (f : SmoothSpacetimeCoefficient) (t : ℝ) :
    ContDiff ℝ ∞ (fun x => (f : ℝ × ℝ → ℝ) (t, x)) :=
  (SmoothSpacetimeCoefficient.joint_smooth f).comp (contDiff_const.prodMk contDiff_id)

theorem SmoothSpacetimeCoefficient.time_slice_smooth (f : SmoothSpacetimeCoefficient) (x : ℝ) :
    ContDiff ℝ ∞ (fun t => (f : ℝ × ℝ → ℝ) (t, x)) :=
  (SmoothSpacetimeCoefficient.joint_smooth f).comp (contDiff_id.prodMk contDiff_const)

def SmoothSpacetimeCoefficient.spaceDerivative (f : SmoothSpacetimeCoefficient) :
    SmoothSpacetimeCoefficient :=
  ⟨spacetimeSpaceDerivative f, spacetimeSpaceDerivative_smooth _
    (SmoothSpacetimeCoefficient.joint_smooth f)⟩

def SmoothSpacetimeCoefficient.timeDerivative (f : SmoothSpacetimeCoefficient) :
    SmoothSpacetimeCoefficient :=
  ⟨spacetimeTimeDerivative f, spacetimeTimeDerivative_smooth _
    (SmoothSpacetimeCoefficient.joint_smooth f)⟩

def smoothSpacetimeSpaceEvolution : AlgebraEvolution SmoothSpacetimeCoefficient where
  toLinearMap :=
    { toFun := SmoothSpacetimeCoefficient.spaceDerivative
      map_add' := by
        intro f g
        apply Subtype.ext
        funext tx
        exact ((SmoothSpacetimeCoefficient.space_slice_smooth f tx.1).differentiable (by simp) tx.2 |>.hasDerivAt).add
          ((SmoothSpacetimeCoefficient.space_slice_smooth g tx.1).differentiable (by simp) tx.2 |>.hasDerivAt) |>.deriv
      map_smul' := by
        intro r f
        apply Subtype.ext
        funext tx
        exact ((SmoothSpacetimeCoefficient.space_slice_smooth f tx.1).differentiable (by simp) tx.2 |>.hasDerivAt).const_mul r |>.deriv }
  leibniz := by
    intro f g
    apply Subtype.ext
    funext tx
    exact ((SmoothSpacetimeCoefficient.space_slice_smooth f tx.1).differentiable (by simp) tx.2 |>.hasDerivAt).mul
      ((SmoothSpacetimeCoefficient.space_slice_smooth g tx.1).differentiable (by simp) tx.2 |>.hasDerivAt) |>.deriv

def smoothSpacetimeTimeEvolution : AlgebraEvolution SmoothSpacetimeCoefficient where
  toLinearMap :=
    { toFun := SmoothSpacetimeCoefficient.timeDerivative
      map_add' := by
        intro f g
        apply Subtype.ext
        funext tx
        exact ((SmoothSpacetimeCoefficient.time_slice_smooth f tx.2).differentiable (by simp) tx.1 |>.hasDerivAt).add
          ((SmoothSpacetimeCoefficient.time_slice_smooth g tx.2).differentiable (by simp) tx.1 |>.hasDerivAt) |>.deriv
      map_smul' := by
        intro r f
        apply Subtype.ext
        funext tx
        exact ((SmoothSpacetimeCoefficient.time_slice_smooth f tx.2).differentiable (by simp) tx.1 |>.hasDerivAt).const_mul r |>.deriv }
  leibniz := by
    intro f g
    apply Subtype.ext
    funext tx
    exact ((SmoothSpacetimeCoefficient.time_slice_smooth f tx.2).differentiable (by simp) tx.1 |>.hasDerivAt).mul
      ((SmoothSpacetimeCoefficient.time_slice_smooth g tx.2).differentiable (by simp) tx.1 |>.hasDerivAt) |>.deriv

def smoothStaticCoefficient {Lx : ℝ} (f : PeriodicCoefficient Lx) : SmoothSpacetimeCoefficient :=
  ⟨fun tx => (f : ℝ → ℝ) tx.2, f.property.1.comp contDiff_snd⟩

def smoothCommonUCoefficient {Lx : ℝ} (U a : PeriodicCoefficient Lx) :
    SmoothSpacetimeCoefficient :=
  ⟨fun tx => (U : ℝ → ℝ) tx.2 + tx.1 * (a : ℝ → ℝ) tx.2,
    (U.property.1.comp contDiff_snd).add (contDiff_fst.mul (a.property.1.comp contDiff_snd))⟩

def actualGaugePrimitive {Lx : ℝ} (a : PeriodicCoefficient Lx) : SmoothSpacetimeCoefficient :=
  ⟨fun tx => (1 / 2 : ℝ) * smoothSpatialPrimitive a tx.2,
    contDiff_const.mul ((smoothSpatialPrimitive_smooth a).comp contDiff_snd)⟩

def commonGaugeSite (par : FieldParameters) (j : ℕ) : Fin par.M :=
  ⟨j % par.M, Nat.mod_lt _ (Nat.pos_of_ne_zero par.M_ne_zero)⟩

theorem smoothCommonUCoefficient_time {Lx : ℝ} (U a : PeriodicCoefficient Lx) :
    smoothSpacetimeTimeEvolution.toLinearMap (smoothCommonUCoefficient U a) =
      smoothStaticCoefficient a := by
  apply Subtype.ext
  funext tx
  change deriv (fun t => (U : ℝ → ℝ) tx.2 + t * (a : ℝ → ℝ) tx.2) tx.1 =
    (a : ℝ → ℝ) tx.2
  simp

theorem smoothStaticCoefficient_time {Lx : ℝ} (w : PeriodicCoefficient Lx) :
    smoothSpacetimeTimeEvolution.toLinearMap (smoothStaticCoefficient w) = 0 := by
  apply Subtype.ext
  funext tx
  change deriv (fun _ : ℝ => (w : ℝ → ℝ) tx.2) tx.1 = 0
  simp

theorem actualGaugePrimitive_space {Lx : ℝ} (a : PeriodicCoefficient Lx) :
    2 * smoothSpacetimeSpaceEvolution.toLinearMap (actualGaugePrimitive a) =
      smoothStaticCoefficient a := by
  apply Subtype.ext
  funext tx
  change (2 : ℝ) * deriv (fun x => (1 / 2 : ℝ) * smoothSpatialPrimitive a x) tx.2 =
    (a : ℝ → ℝ) tx.2
  rw [((smoothSpatialPrimitive_hasDerivAt a tx.2).const_mul (1 / 2)).deriv]
  ring

/-- For every actual smooth periodic common direction, source derivatives
and scalar normal-form cancellation imply zero residue variation of each
normalized spectral power. No periodic trace is used on the primitive. -/
theorem actualCommonGauge_residue_rate_zero {par : FieldParameters}
    {A : Type*} [Ring A] [Algebra ℝ A]
    (model : CoefficientOperatorModel SmoothSpacetimeCoefficient A)
    (normal : ScalarNormalResidueModel model)
    (hspace : model.space = smoothSpacetimeSpaceEvolution)
    (htime : model.time = smoothSpacetimeTimeEvolution)
    (U w : Fin par.M → PeriodicCoefficient par.Lx) (a : PeriodicCoefficient par.Lx)
    (denominator : ℕ → Aˣ)
    (hdenominator : ∀ (j : ℕ) (hj : j < par.M), (denominator j : A) = model.factor
      (commonGaugeCoefficient par.h
        (smoothCommonUCoefficient (U ⟨j, hj⟩) a)
        (smoothStaticCoefficient (w ⟨j, hj⟩)) (-1)))
    (difference : Aˣ)
    (hdifference : (difference : A) = transferProduct
      (fun j => (↑(denominator j)⁻¹ : A) * model.factor
        (commonGaugeCoefficient par.h
          (smoothCommonUCoefficient (U (commonGaugeSite par j)) a)
          (smoothStaticCoefficient (w (commonGaugeSite par j))) 1)) par.M - 1)
    (n : ℕ) :
    normal.residue (model.evolution.toLinearMap
      (normalizedL par.G par.B difference ^ n)) = 0 := by
  refine commonGauge_normalized_spectral_residue_rate_zero model normal
    par.h par.G par.B
    (fun j => smoothCommonUCoefficient (U (commonGaugeSite par j)) a)
    (fun j => smoothStaticCoefficient (w (commonGaugeSite par j)))
    (actualGaugePrimitive a) par.M ?_ ?_ denominator ?_ difference hdifference n
  · intro j hj
    rw [htime, hspace, smoothCommonUCoefficient_time, actualGaugePrimitive_space]
  · intro j hj
    rw [htime, smoothStaticCoefficient_time]
  · intro j hj
    have hsite : commonGaugeSite par j = ⟨j, hj⟩ := by
      apply Fin.ext
      exact Nat.mod_eq_of_lt hj
    simpa only [hsite] using hdenominator j hj

#print axioms actualGaugePrimitive_space
#print axioms actualCommonGauge_residue_rate_zero
end
end DLWLean
