import ActualPhysicalSource
import PeriodicSpacetimeCoefficients
import HeatIntertwiner

namespace DLWLean
noncomputable section
open scoped BigOperators ContDiff

theorem StartPoint.joint_smooth_U {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) : ContDiff ℝ ∞ (fun tx : ℝ × ℝ => (start.trajectory tx.1).U j tx.2) := by
  unfold FieldCoordinates.U FieldCoordinates.commonU FieldCoordinates.meanPS latticeMean
  exact (start.joint_smooth_p j).add
    ((contDiff_const.sub ((ContDiff.sum fun i _ =>
      (start.joint_smooth_p i).mul (start.joint_smooth_s i)).div_const _)).div_const _)

theorem StartPoint.joint_smooth_w {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) : ContDiff ℝ ∞ (fun tx : ℝ × ℝ => (start.trajectory tx.1).w j tx.2) :=
  contDiff_const.add (start.joint_smooth_s j)

def StartPoint.UCoefficient {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) : PeriodicSpacetimeCoefficient par.Lx :=
  ⟨fun tx => (start.trajectory tx.1).U j tx.2, start.joint_smooth_U j,
    fun t => (start.trajectory t).U_periodic j⟩

def StartPoint.wCoefficient {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) : PeriodicSpacetimeCoefficient par.Lx :=
  ⟨fun tx => (start.trajectory tx.1).w j tx.2, start.joint_smooth_w j,
    fun t => (start.trajectory t).w_periodic j⟩

def spacetimeFiniteLinearMap {M N : ℕ} {Lx : ℝ}
    (T : (Fin M → ℝ) →ₗ[ℝ] (Fin N → ℝ))
    (f : Fin M → PeriodicSpacetimeCoefficient Lx) (j : Fin N) :
    PeriodicSpacetimeCoefficient Lx :=
  ⟨fun tx => T (fun i => (f i : ℝ × ℝ → ℝ) tx) j,
    (contDiff_pi.mp (T.toContinuousLinearMap.contDiff.comp
      (contDiff_pi.mpr fun i => (f i).property.1))) j, by
      intro t x
      change T (fun i => (f i : ℝ × ℝ → ℝ) (t, x + Lx)) j =
        T (fun i => (f i : ℝ × ℝ → ℝ) (t, x)) j
      have h : (fun i => (f i : ℝ × ℝ → ℝ) (t, x + Lx)) =
          fun i => (f i : ℝ × ℝ → ℝ) (t, x) :=
        funext fun i => (f i).property.2 t x
      rw [h]⟩

def spacetimeLatticeMean {M : ℕ} {Lx : ℝ}
    (f : Fin M → PeriodicSpacetimeCoefficient Lx) : PeriodicSpacetimeCoefficient Lx :=
  ⟨fun tx => latticeMean (fun i => (f i : ℝ × ℝ → ℝ) tx),
    (ContDiff.sum fun i _ => (f i).property.1).div_const M, by
      intro t x
      change latticeMean (fun i => (f i : ℝ × ℝ → ℝ) (t, x + Lx)) =
        latticeMean (fun i => (f i : ℝ × ℝ → ℝ) (t, x))
      congr 1
      funext i
      exact (f i).property.2 t x⟩

def StartPoint.energyCoefficient {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) : PeriodicSpacetimeCoefficient par.Lx :=
  let Dx := (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap
  let Rwx := spacetimeFiniteLinearMap (latticeResolvent par) (fun i => Dx (start.wCoefficient i)) j
  (1 / 2 : ℝ) • (start.UCoefficient j ^ 2 * start.wCoefficient j) +
    (beta par / 3) • (start.wCoefficient j ^ 3) +
    start.wCoefficient j * Dx (start.UCoefficient j) +
    (1 / 2 : ℝ) • (start.wCoefficient j * Rwx)

def StartPoint.meanEnergyCoefficient {par : FieldParameters} (start : StartPoint par) :
    PeriodicSpacetimeCoefficient par.Lx := spacetimeLatticeMean start.energyCoefficient

theorem StartPoint.energyCoefficient_eval {par : FieldParameters} (start : StartPoint par)
    (j : Fin par.M) (t x : ℝ) :
    (start.energyCoefficient j : ℝ × ℝ → ℝ) (t, x) =
      localPhysicalEnergy (start.trajectory t) j x := by
  change (1 / 2 : ℝ) * ((start.trajectory t).U j x ^ 2 * (start.trajectory t).w j x) +
    (beta par / 3) * ((start.trajectory t).w j x ^ 3) +
    (start.trajectory t).w j x * deriv ((start.trajectory t).U j) x +
    (1 / 2 : ℝ) * ((start.trajectory t).w j x *
      latticeResolvent par (fun i => deriv ((start.trajectory t).w i) x) j) = _
  unfold localPhysicalEnergy
  ring

theorem StartPoint.meanEnergyCoefficient_eval {par : FieldParameters} (start : StartPoint par)
    (t x : ℝ) : (start.meanEnergyCoefficient : ℝ × ℝ → ℝ) (t, x) =
      meanLocalPhysicalEnergy (start.trajectory t) x := by
  change latticeMean (fun i => (start.energyCoefficient i : ℝ × ℝ → ℝ) (t, x)) = _
  simp_rw [start.energyCoefficient_eval]
  rfl

/-- All source data are the actual spacetime fields and their actual
derivatives. The operator representation identifies its coefficient
derivations with these constructed spatial/time derivations. -/
def StartPoint.coefficientSource {par : FieldParameters} (start : StartPoint par)
    {A : Type*} [Ring A] [Algebra ℝ A]
    (model : CoefficientOperatorModel (PeriodicSpacetimeCoefficient par.Lx) A)
    (hspace : model.space = periodicSpacetimeSpaceEvolution par.Lx)
    (htime : model.time = periodicSpacetimeTimeEvolution par.Lx)
    (v0 : ℝ) (j : Fin par.M) : PhysicalCoefficientJet model par.h par.c where
  U := start.UCoefficient j
  w := start.wCoefficient j
  Ux := (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (start.UCoefficient j)
  wx := (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (start.wCoefficient j)
  Uxx := (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap
    ((periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (start.UCoefficient j))
  wxx := (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap
    ((periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (start.wCoefficient j))
  Rwx := spacetimeFiniteLinearMap (latticeResolvent par) (fun i =>
    (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (start.wCoefficient i)) j
  Rwxx := spacetimeFiniteLinearMap (latticeResolvent par) (fun i =>
    (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap
      ((periodicSpacetimeSpaceEvolution par.Lx).toLinearMap (start.wCoefficient i))) j
  ebar := start.meanEnergyCoefficient
  ebarx := (periodicSpacetimeSpaceEvolution par.Lx).toLinearMap start.meanEnergyCoefficient
  v0 := algebraMap ℝ (PeriodicSpacetimeCoefficient par.Lx) v0
  space_U := by rw [hspace]
  space_w := by rw [hspace]
  space_Ux := by rw [hspace]
  space_wx := by rw [hspace]
  space_Rwx := by
    rw [hspace]
    apply Subtype.ext
    funext tx
    change deriv (fun y => latticeResolvent par
        (fun i => deriv ((start.trajectory tx.1).w i) y) j) tx.2 =
      latticeResolvent par (fun i => deriv (deriv ((start.trajectory tx.1).w i)) tx.2) j
    exact derivative_finite_linear_map (latticeResolvent par)
      (fun i => deriv ((start.trajectory tx.1).w i))
      (fun i => (((start.trajectory tx.1).w_smooth i).iterate_deriv 1).differentiable (by simp)) tx.2 j
  space_ebar := by rw [hspace]
  space_v0 := evolution_algebraMap_zero model.space v0
  physical_Ut := by
    rw [htime]
    apply Subtype.ext
    funext tx
    change deriv (fun τ => (start.trajectory τ).U j tx.2) tx.1 =
      -((start.trajectory tx.1).U j tx.2 * deriv ((start.trajectory tx.1).U j) tx.2 +
        (par.h / 4) ^ 2 * (start.trajectory tx.1).w j tx.2 *
          deriv ((start.trajectory tx.1).w j) tx.2 +
        deriv (deriv ((start.trajectory tx.1).U j)) tx.2 +
        latticeResolvent par (fun i => deriv (deriv ((start.trajectory tx.1).w i)) tx.2) j) +
      2 * par.c⁻¹ * deriv (fun y => (start.meanEnergyCoefficient : ℝ × ℝ → ℝ) (tx.1, y)) tx.2
    have he : (fun y => (start.meanEnergyCoefficient : ℝ × ℝ → ℝ) (tx.1, y)) =
        meanLocalPhysicalEnergy (start.trajectory tx.1) :=
      funext fun y => start.meanEnergyCoefficient_eval tx.1 y
    rw [he]
    convert start.explicit_Ut tx.1 tx.2 j using 1 <;> ring
  physical_wt := by
    rw [htime]
    apply Subtype.ext
    funext tx
    change deriv (fun τ => (start.trajectory τ).w j tx.2) tx.1 =
      deriv (deriv ((start.trajectory tx.1).w j)) tx.2 -
        (deriv ((start.trajectory tx.1).U j) tx.2 * (start.trajectory tx.1).w j tx.2 +
          (start.trajectory tx.1).U j tx.2 * deriv ((start.trajectory tx.1).w j) tx.2)
    simpa only [physicalWTimeJet, sub_add_eq_sub_sub] using start.explicit_wt tx.1 tx.2 j

theorem StartPoint.coefficientSource_potential_eval {par : FieldParameters} (start : StartPoint par)
    {A : Type*} [Ring A] [Algebra ℝ A]
    (model : CoefficientOperatorModel (PeriodicSpacetimeCoefficient par.Lx) A)
    (hspace : model.space = periodicSpacetimeSpaceEvolution par.Lx)
    (htime : model.time = periodicSpacetimeTimeEvolution par.Lx)
    (v0 : ℝ) (j : Fin par.M) (t x : ℝ) :
    ((start.coefficientSource model hspace htime v0 j).potential : ℝ × ℝ → ℝ) (t, x) =
      physicalHeatPotential (start.trajectory t) v0 j x := by
  change (1 / 2 : ℝ) * latticeResolvent par (fun i => deriv ((start.trajectory t).w i) x) j -
    par.h / 4 * deriv ((start.trajectory t).w j) x -
    par.c⁻¹ * (start.meanEnergyCoefficient : ℝ × ℝ → ℝ) (t, x) + v0 = _
  rw [start.meanEnergyCoefficient_eval]
  unfold physicalHeatPotential latticeHeatPotential
  ring

/-- The adjacent-site identity closes the actual periodic lattice chain;
it is proved from the constructed resolvent and fixed spatial mean. -/
theorem StartPoint.coefficientSource_potential_next {par : FieldParameters} (start : StartPoint par)
    {A : Type*} [Ring A] [Algebra ℝ A]
    (model : CoefficientOperatorModel (PeriodicSpacetimeCoefficient par.Lx) A)
    (hspace : model.space = periodicSpacetimeSpaceEvolution par.Lx)
    (htime : model.time = periodicSpacetimeTimeEvolution par.Lx)
    (v0 : ℝ) (j : Fin par.M) :
    (start.coefficientSource model hspace htime v0 j).potentialPlus =
      (start.coefficientSource model hspace htime v0 (nextSite par j)).potential := by
  apply Subtype.ext
  funext tx
  change ((start.coefficientSource model hspace htime v0 j).potential : ℝ × ℝ → ℝ) tx +
    2 * (par.h / 4) * deriv ((start.trajectory tx.1).w j) tx.2 =
      ((start.coefficientSource model hspace htime v0 (nextSite par j)).potential : ℝ × ℝ → ℝ) tx
  rcases tx with ⟨t, x⟩
  rw [start.coefficientSource_potential_eval, start.coefficientSource_potential_eval]
  rw [physicalHeatPotential_shift]
  ring

/-- Full transfer link on the original physical trajectory. The only
factor premise is its formal invertibility in the operator representation;
the source PDE and the adjacent heat potentials have been derived. -/
theorem StartPoint.transfer_lax_from_physical_equations {par : FieldParameters}
    (start : StartPoint par) {A : Type*} [Ring A] [Algebra ℝ A]
    (model : CoefficientOperatorModel (PeriodicSpacetimeCoefficient par.Lx) A)
    (hspace : model.space = periodicSpacetimeSpaceEvolution par.Lx)
    (htime : model.time = periodicSpacetimeTimeEvolution par.Lx)
    (v0 : ℝ) (j : Fin par.M) (u : Aˣ)
    (hu : (u : A) = model.factor
      (start.coefficientSource model hspace htime v0 j).beta) :
    model.evolution.toLinearMap ((↑u⁻¹ : A) * model.factor
      (start.coefficientSource model hspace htime v0 j).alpha) =
      model.heat (start.coefficientSource model hspace htime v0 (nextSite par j)).potential *
        ((↑u⁻¹ : A) * model.factor (start.coefficientSource model hspace htime v0 j).alpha) -
      ((↑u⁻¹ : A) * model.factor (start.coefficientSource model hspace htime v0 j).alpha) *
        model.heat (start.coefficientSource model hspace htime v0 j).potential := by
  have h := (start.coefficientSource model hspace htime v0 j).transfer_lax_from_physical_source u hu
  rw [start.coefficientSource_potential_next] at h
  exact h

#print axioms StartPoint.coefficientSource
#print axioms StartPoint.coefficientSource_potential_next
#print axioms StartPoint.transfer_lax_from_physical_equations
end
end DLWLean
