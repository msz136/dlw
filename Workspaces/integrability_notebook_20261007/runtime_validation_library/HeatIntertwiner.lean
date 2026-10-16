import Monodromy
import Mathlib.Algebra.Algebra.Hom
import Mathlib.Tactic.Ring

/-!
Actual differential-operator heat intertwiners, followed by an inverse-factor
transfer identity. The coefficient algebra can be smooth periodic functions;
it is not restricted to pointwise scalar test jets.
-/

namespace DLWLean

noncomputable section

variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]

/-- The coefficient embedding and spatial commutator law are the foundation
needed for finite differential-operator computations. Time preserves D and
acts on embedded coefficients by the supplied coefficient derivation. -/
structure CoefficientOperatorModel (R A : Type*)
    [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A] where
  coeff : R →ₐ[ℝ] A
  space : AlgebraEvolution R
  time : AlgebraEvolution R
  evolution : AlgebraEvolution A
  D : A
  space_commutation : ∀ r : R,
    D * coeff r - coeff r * D = coeff (space.toLinearMap r)
  evolution_D : evolution.toLinearMap D = 0
  evolution_coeff : ∀ r : R,
    evolution.toLinearMap (coeff r) = coeff (time.toLinearMap r)

namespace CoefficientOperatorModel

variable (model : CoefficientOperatorModel R A)

def factor (r : R) : A := model.D - model.coeff r

def heat (V : R) : A := -(model.D ^ 2) - model.coeff V

theorem D_mul_coeff (r : R) :
    model.D * model.coeff r =
      model.coeff r * model.D + model.coeff (model.space.toLinearMap r) := by
  have h := model.space_commutation r
  have ha := congrArg (fun a : A => a + model.coeff r * model.D) h
  have ha' : model.D * model.coeff r =
      model.coeff (model.space.toLinearMap r) + model.coeff r * model.D := by
    simpa only [sub_add_cancel] using ha
  exact ha'.trans (add_comm _ _)

theorem D_sq_mul_coeff (r : R) :
    model.D ^ 2 * model.coeff r = model.coeff r * model.D ^ 2 +
      model.coeff (model.space.toLinearMap r) * model.D +
      model.coeff (model.space.toLinearMap r) * model.D +
      model.coeff (model.space.toLinearMap (model.space.toLinearMap r)) := by
  calc
    model.D ^ 2 * model.coeff r = model.D * (model.D * model.coeff r) := by
      noncomm_ring
    _ = model.D * (model.coeff r * model.D +
        model.coeff (model.space.toLinearMap r)) := by rw [model.D_mul_coeff]
    _ = (model.D * model.coeff r) * model.D +
        model.D * model.coeff (model.space.toLinearMap r) := by noncomm_ring
    _ = (model.coeff r * model.D + model.coeff (model.space.toLinearMap r)) *
        model.D + (model.coeff (model.space.toLinearMap r) * model.D +
        model.coeff (model.space.toLinearMap (model.space.toLinearMap r))) := by
      rw [model.D_mul_coeff, model.D_mul_coeff]
    _ = _ := by noncomm_ring

theorem coeff_mul_comm (r s : R) : model.coeff r * model.coeff s =
    model.coeff s * model.coeff r := by
  rw [← map_mul, ← map_mul, mul_comm r s]

/-- Exact operator defect, before using a potential shift or Riccati source. -/
theorem heat_factor_defect (r Vin Vout : R) :
    model.heat Vout * model.factor r - model.factor r * model.heat Vin =
      (model.coeff (model.space.toLinearMap r) +
        model.coeff (model.space.toLinearMap r) + model.coeff Vin -
        model.coeff Vout) * model.D +
      model.coeff (model.space.toLinearMap (model.space.toLinearMap r)) +
      model.coeff (model.space.toLinearMap Vin) +
      model.coeff Vout * model.coeff r - model.coeff r * model.coeff Vin := by
  calc
    model.heat Vout * model.factor r - model.factor r * model.heat Vin =
      (model.D ^ 2 * model.coeff r - model.coeff r * model.D ^ 2) +
      (model.D * model.coeff Vin - model.coeff Vout * model.D) +
      (model.coeff Vout * model.coeff r - model.coeff r * model.coeff Vin) := by
      simp only [heat, factor]
      noncomm_ring
    _ = _ := by
      rw [model.D_sq_mul_coeff, model.D_mul_coeff]
      noncomm_ring

/-- A potential shift and a coefficient Riccati identity imply the full
operator heat intertwiner, with the actual time derivation on D-r. -/
theorem heat_factor_link (r Vin Vout : R)
    (hshift : Vout = Vin + 2 * model.space.toLinearMap r)
    (hriccati : model.time.toLinearMap r +
      model.space.toLinearMap (model.space.toLinearMap r) +
      2 * r * model.space.toLinearMap r + model.space.toLinearMap Vin = 0) :
    model.evolution.toLinearMap (model.factor r) =
      model.heat Vout * model.factor r - model.factor r * model.heat Vin := by
  have hcshift : model.coeff Vout = model.coeff Vin +
      model.coeff (model.space.toLinearMap r) +
      model.coeff (model.space.toLinearMap r) := by
    rw [hshift, two_mul, map_add, map_add]
    abel
  have hres := congrArg model.coeff hriccati
  simp only [map_add, map_mul, map_ofNat, map_zero] at hres
  have hdef := model.heat_factor_defect r Vin Vout
  rw [hcshift] at hdef
  simp only [add_mul] at hdef
  rw [model.coeff_mul_comm Vin r,
    model.coeff_mul_comm (model.space.toLinearMap r) r] at hdef
  rw [hdef]
  simp only [factor, map_sub, model.evolution_D, model.evolution_coeff, zero_sub]
  have hz : model.coeff (model.time.toLinearMap r) +
      (model.coeff (model.space.toLinearMap (model.space.toLinearMap r)) +
        2 * model.coeff r * model.coeff (model.space.toLinearMap r) +
        model.coeff (model.space.toLinearMap Vin)) = 0 := by
    calc
      _ = model.coeff (model.time.toLinearMap r) +
        model.coeff (model.space.toLinearMap (model.space.toLinearMap r)) +
        2 * model.coeff r * model.coeff (model.space.toLinearMap r) +
        model.coeff (model.space.toLinearMap Vin) := by abel
      _ = 0 := hres
  rw [eq_neg_of_add_eq_zero_left hz]
  noncomm_ring

end CoefficientOperatorModel

/-- The transfer quotient follows from two full factor links with the same
intermediate heat generator; no spectral or flow conclusion is assumed. -/
theorem transfer_from_two_factor_links (v : AlgebraEvolution A)
    (u : Aˣ) (Fa QF Qin Qplus : A)
    (hFa : v.toLinearMap Fa = QF * Fa - Fa * Qin)
    (hFb : v.toLinearMap (u : A) = QF * (u : A) - (u : A) * Qplus) :
    v.toLinearMap ((↑u⁻¹ : A) * Fa) =
      Qplus * ((↑u⁻¹ : A) * Fa) - ((↑u⁻¹ : A) * Fa) * Qin := by
  rw [v.leibniz, unit_inverse_evolution, hFa, hFb]
  simp only [mul_sub, sub_mul, neg_mul, mul_assoc, Units.mul_inv,
    mul_one, Units.inv_mul_cancel_left]
  noncomm_ring

theorem heat_transfer_lax (model : CoefficientOperatorModel R A)
    (alpha beta Vin Vplus VF : R) (u : Aˣ)
    (hu : (u : A) = model.factor beta)
    (hshiftAlpha : VF = Vin + 2 * model.space.toLinearMap alpha)
    (hshiftBeta : VF = Vplus + 2 * model.space.toLinearMap beta)
    (hricAlpha : model.time.toLinearMap alpha +
      model.space.toLinearMap (model.space.toLinearMap alpha) +
      2 * alpha * model.space.toLinearMap alpha + model.space.toLinearMap Vin = 0)
    (hricBeta : model.time.toLinearMap beta +
      model.space.toLinearMap (model.space.toLinearMap beta) +
      2 * beta * model.space.toLinearMap beta + model.space.toLinearMap Vplus = 0) :
    model.evolution.toLinearMap ((↑u⁻¹ : A) * model.factor alpha) =
      model.heat Vplus * ((↑u⁻¹ : A) * model.factor alpha) -
        ((↑u⁻¹ : A) * model.factor alpha) * model.heat Vin := by
  apply transfer_from_two_factor_links
  · exact model.heat_factor_link alpha Vin VF hshiftAlpha hricAlpha
  · rw [hu]
    exact model.heat_factor_link beta Vplus VF hshiftBeta hricBeta

/-- A real-linear derivation fixes every scalar coefficient. -/
theorem evolution_algebraMap_zero (v : AlgebraEvolution R) (s : ℝ) :
    v.toLinearMap (algebraMap ℝ R s) = 0 := by
  rw [Algebra.algebraMap_eq_smul_one, map_smul, evolution_map_one, smul_zero]

def halfCoefficient : R := algebraMap ℝ R ((1 : ℝ) / 2)

def latticeQuarter (h : ℝ) : R := algebraMap ℝ R (h / 4)

def meanReciprocal (c : ℝ) : R := algebraMap ℝ R c⁻¹

theorem two_mul_halfCoefficient : 2 * (halfCoefficient : R) = 1 := by
  change (2 : R) * algebraMap ℝ R ((1 : ℝ) / 2) = 1
  rw [← map_ofNat (algebraMap ℝ R) 2, ← map_mul]
  norm_num

/-- Source coefficients and their physical PDE and spatial derivative data.
The entries can be whole periodic functions. Riccati and Lax conclusions
are deliberately absent from these source fields. -/
structure PhysicalCoefficientJet (model : CoefficientOperatorModel R A) (h c : ℝ) where
  U : R
  w : R
  Ux : R
  wx : R
  Uxx : R
  wxx : R
  Rwx : R
  Rwxx : R
  ebar : R
  ebarx : R
  v0 : R
  space_U : model.space.toLinearMap U = Ux
  space_w : model.space.toLinearMap w = wx
  space_Ux : model.space.toLinearMap Ux = Uxx
  space_wx : model.space.toLinearMap wx = wxx
  space_Rwx : model.space.toLinearMap Rwx = Rwxx
  space_ebar : model.space.toLinearMap ebar = ebarx
  space_v0 : model.space.toLinearMap v0 = 0
  physical_Ut : model.time.toLinearMap U =
    -(U * Ux + latticeQuarter h ^ 2 * w * wx + Uxx + Rwxx) +
      2 * meanReciprocal c * ebarx
  physical_wt : model.time.toLinearMap w = wxx - (Ux * w + U * wx)

namespace PhysicalCoefficientJet

variable {model : CoefficientOperatorModel R A} {h c : ℝ}
variable (z : PhysicalCoefficientJet model h c)

def alpha : R := halfCoefficient * (z.U + latticeQuarter h * z.w)

def beta : R := halfCoefficient * (z.U - latticeQuarter h * z.w)

def potential : R := halfCoefficient * z.Rwx - latticeQuarter h * z.wx -
  meanReciprocal c * z.ebar + z.v0

def potentialPlus : R := z.potential + 2 * latticeQuarter h * z.wx

def potentialIntermediate : R := z.potential + 2 * model.space.toLinearMap z.alpha

theorem space_alpha : model.space.toLinearMap z.alpha =
    halfCoefficient * (z.Ux + latticeQuarter h * z.wx) := by
  simp only [alpha, halfCoefficient, latticeQuarter, model.space.leibniz,
    map_add, evolution_algebraMap_zero, zero_mul, zero_add, z.space_U, z.space_w]

theorem space_beta : model.space.toLinearMap z.beta =
    halfCoefficient * (z.Ux - latticeQuarter h * z.wx) := by
  simp only [beta, halfCoefficient, latticeQuarter, model.space.leibniz,
    map_sub, evolution_algebraMap_zero, zero_mul, zero_add, z.space_U, z.space_w]

theorem space_alpha_twice :
    model.space.toLinearMap (model.space.toLinearMap z.alpha) =
      halfCoefficient * (z.Uxx + latticeQuarter h * z.wxx) := by
  rw [z.space_alpha]
  simp only [halfCoefficient, latticeQuarter, model.space.leibniz,
    map_add, evolution_algebraMap_zero, zero_mul, zero_add, z.space_Ux, z.space_wx]

theorem space_beta_twice :
    model.space.toLinearMap (model.space.toLinearMap z.beta) =
      halfCoefficient * (z.Uxx - latticeQuarter h * z.wxx) := by
  rw [z.space_beta]
  simp only [halfCoefficient, latticeQuarter, model.space.leibniz,
    map_sub, evolution_algebraMap_zero, zero_mul, zero_add, z.space_Ux, z.space_wx]

theorem time_alpha : model.time.toLinearMap z.alpha =
    halfCoefficient * (model.time.toLinearMap z.U +
      latticeQuarter h * model.time.toLinearMap z.w) := by
  simp only [alpha, halfCoefficient, latticeQuarter, model.time.leibniz,
    map_add, evolution_algebraMap_zero, zero_mul, zero_add]

theorem time_beta : model.time.toLinearMap z.beta =
    halfCoefficient * (model.time.toLinearMap z.U -
      latticeQuarter h * model.time.toLinearMap z.w) := by
  simp only [beta, halfCoefficient, latticeQuarter, model.time.leibniz,
    map_sub, evolution_algebraMap_zero, zero_mul, zero_add]

theorem space_potential : model.space.toLinearMap z.potential =
    halfCoefficient * z.Rwxx - latticeQuarter h * z.wxx -
      meanReciprocal c * z.ebarx := by
  simp only [potential, halfCoefficient, latticeQuarter, meanReciprocal,
    model.space.leibniz, map_add, map_sub, evolution_algebraMap_zero,
    zero_mul, zero_add, add_zero, z.space_Rwx, z.space_wx, z.space_ebar, z.space_v0]

theorem space_potentialPlus : model.space.toLinearMap z.potentialPlus =
    halfCoefficient * z.Rwxx + latticeQuarter h * z.wxx -
      meanReciprocal c * z.ebarx := by
  have htwo : model.space.toLinearMap (2 : R) = 0 := by
    rw [show (2 : R) = 1 + 1 by norm_num, map_add, evolution_map_one, add_zero]
  rw [potentialPlus, map_add, z.space_potential]
  simp only [model.space.leibniz, htwo, evolution_algebraMap_zero,
    latticeQuarter, zero_mul, zero_add, z.space_wx]
  ring

/-- The first coefficient-function Riccati identity follows from physical
U_t,w_t and derivative source equations, uniformly over commutative R. -/
theorem alpha_riccati_from_physical_source : model.time.toLinearMap z.alpha +
    model.space.toLinearMap (model.space.toLinearMap z.alpha) +
    2 * z.alpha * model.space.toLinearMap z.alpha +
      model.space.toLinearMap z.potential = 0 := by
  rw [z.time_alpha, z.space_alpha_twice, z.space_alpha, z.space_potential,
    z.physical_Ut, z.physical_wt]
  calc
    _ = (2 * (halfCoefficient : R) - 1) *
      (halfCoefficient * (z.U + latticeQuarter h * z.w) *
        (z.Ux + latticeQuarter h * z.wx) +
        latticeQuarter h * z.wxx + meanReciprocal c * z.ebarx) := by
      unfold alpha
      ring
    _ = 0 := by rw [two_mul_halfCoefficient, sub_self, zero_mul]

theorem beta_riccati_from_physical_source : model.time.toLinearMap z.beta +
    model.space.toLinearMap (model.space.toLinearMap z.beta) +
    2 * z.beta * model.space.toLinearMap z.beta +
      model.space.toLinearMap z.potentialPlus = 0 := by
  rw [z.time_beta, z.space_beta_twice, z.space_beta, z.space_potentialPlus,
    z.physical_Ut, z.physical_wt]
  calc
    _ = (2 * (halfCoefficient : R) - 1) *
      (halfCoefficient * (z.U - latticeQuarter h * z.w) *
        (z.Ux - latticeQuarter h * z.wx) -
        latticeQuarter h * z.wxx + meanReciprocal c * z.ebarx) := by
      unfold beta
      ring
    _ = 0 := by rw [two_mul_halfCoefficient, sub_self, zero_mul]

theorem common_intermediate_from_physical_source :
    z.potentialIntermediate = z.potentialPlus +
      2 * model.space.toLinearMap z.beta := by
  rw [potentialIntermediate, potentialPlus, z.space_alpha, z.space_beta]
  calc
    _ = z.potential + 2 * latticeQuarter h * z.wx +
      2 * halfCoefficient * (z.Ux - latticeQuarter h * z.wx) +
      (2 * (halfCoefficient : R) - 1) * (2 * latticeQuarter h * z.wx) := by ring
    _ = _ := by
      have hzero : (2 * (halfCoefficient : R) - 1) *
          (2 * latticeQuarter h * z.wx) = 0 := by
        rw [two_mul_halfCoefficient, sub_self, zero_mul]
      rw [hzero, add_zero]
      ring

/-- The actual transfer operator satisfies the link equation, derived from
physical PDE data rather than assumed as a Lax or Riccati premise. -/
theorem transfer_lax_from_physical_source (u : Aˣ)
    (hu : (u : A) = model.factor z.beta) :
    model.evolution.toLinearMap ((↑u⁻¹ : A) * model.factor z.alpha) =
      model.heat z.potentialPlus * ((↑u⁻¹ : A) * model.factor z.alpha) -
        ((↑u⁻¹ : A) * model.factor z.alpha) * model.heat z.potential := by
  apply heat_transfer_lax model z.alpha z.beta z.potential z.potentialPlus
    z.potentialIntermediate u hu
  · rfl
  · exact z.common_intermediate_from_physical_source
  · exact z.alpha_riccati_from_physical_source
  · exact z.beta_riccati_from_physical_source

end PhysicalCoefficientJet

#print axioms CoefficientOperatorModel.heat_factor_link
#print axioms transfer_from_two_factor_links
#print axioms heat_transfer_lax
#print axioms PhysicalCoefficientJet.alpha_riccati_from_physical_source
#print axioms PhysicalCoefficientJet.transfer_lax_from_physical_source

end

end DLWLean
