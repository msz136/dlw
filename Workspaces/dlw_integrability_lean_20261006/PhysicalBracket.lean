import ResidueIntegral
import ReducedPairing
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Tactic

/-! Actual periodic coefficient fields, the reduced constant differential
operator and the translation momentum. The bracket here is evaluated on
variational gradients; it does not by itself assert Jacobi for a chosen
class of nonlinear functionals. -/
namespace DLWLean
noncomputable section
open scoped BigOperators

def zeroMeanCoefficientFields (par : FieldParameters) :
    Submodule ℝ (Fin par.M → PeriodicCoefficient par.Lx) where
  carrier := {f | ∑ j, f j = 0}
  zero_mem' := by simp
  add_mem' := by
    intro f g hf hg
    simp only [Set.mem_ofPred_eq, Pi.add_apply, Finset.sum_add_distrib] at *
    rw [hf, hg, add_zero]
  smul_mem' := by
    intro r f hf
    simp only [Set.mem_ofPred_eq, Pi.smul_apply, ← Finset.smul_sum] at *
    rw [hf, smul_zero]

abbrev ClosedPeriodicField (par : FieldParameters) : Type := ↥(zeroMeanCoefficientFields par)
instance (par : FieldParameters) :
    CoeFun (ClosedPeriodicField par) (fun _ => Fin par.M → PeriodicCoefficient par.Lx) :=
  ⟨fun f => f.val⟩
abbrev ClosedPeriodicPair (par : FieldParameters) :=
  ClosedPeriodicField par × ClosedPeriodicField par

def closedSpatialDerivative (par : FieldParameters) :
    ClosedPeriodicField par →ₗ[ℝ] ClosedPeriodicField par where
  toFun f := ⟨fun j => (periodicSpatialEvolution par.Lx).toLinearMap (f j), by
    change (∑ j, (periodicSpatialEvolution par.Lx).toLinearMap (f j)) = 0
    rw [← map_sum, f.property, map_zero]⟩
  map_add' f g := by
    apply Subtype.ext
    funext j
    exact map_add _ _ _
  map_smul' r f := by
    apply Subtype.ext
    funext j
    exact map_smul (periodicSpatialEvolution par.Lx).toLinearMap r (f j)

/-- On zero-mean fields P0 D is precisely D. -/
theorem closed_derivative_projector (par : FieldParameters)
    (f : ClosedPeriodicField par) (x : ℝ) (j : Fin par.M) :
    latticeP0 (fun i => (closedSpatialDerivative par f i : ℝ → ℝ) x) j =
      (closedSpatialDerivative par f j : ℝ → ℝ) x := by
  have hz := congrArg (fun a : PeriodicCoefficient par.Lx => (a : ℝ → ℝ) x)
    (closedSpatialDerivative par f).property
  have hz' : ∑ i, (closedSpatialDerivative par f i : ℝ → ℝ) x = 0 := by
    simpa using hz
  simp [latticeP0, latticeMean, hz']

def coefficientPairing (par : FieldParameters)
    (f g : ClosedPeriodicField par) : ℝ :=
  par.h * periodicCoefficientIntegral par.Lx (∑ j, f j * g j)

theorem coefficientPairing_symmetric (par : FieldParameters)
    (f g : ClosedPeriodicField par) :
    coefficientPairing par f g = coefficientPairing par g f := by
  simp only [coefficientPairing, mul_comm (f _) (g _)]

theorem coefficientPairing_add_left (par : FieldParameters)
    (f g k : ClosedPeriodicField par) :
    coefficientPairing par (f + g) k =
      coefficientPairing par f k + coefficientPairing par g k := by
  unfold coefficientPairing
  change par.h * periodicCoefficientIntegral par.Lx (∑ j, (f j + g j) * k j) = _
  simp only [add_mul, Finset.sum_add_distrib, map_add]
  ring

theorem coefficientPairing_smul_left (par : FieldParameters)
    (r : ℝ) (f g : ClosedPeriodicField par) :
    coefficientPairing par (r • f) g = r * coefficientPairing par f g := by
  unfold coefficientPairing
  change par.h * periodicCoefficientIntegral par.Lx (∑ j, (r • f j) * g j) = _
  simp only [smul_mul_assoc, ← Finset.smul_sum, map_smul, smul_eq_mul]
  ring

theorem coefficientPairing_add_right (par : FieldParameters)
    (f g k : ClosedPeriodicField par) :
    coefficientPairing par f (g + k) =
      coefficientPairing par f g + coefficientPairing par f k := by
  rw [coefficientPairing_symmetric, coefficientPairing_add_left]
  rw [coefficientPairing_symmetric par g f, coefficientPairing_symmetric par k f]

theorem coefficientPairing_smul_right (par : FieldParameters)
    (r : ℝ) (f g : ClosedPeriodicField par) :
    coefficientPairing par f (r • g) = r * coefficientPairing par f g := by
  rw [coefficientPairing_symmetric, coefficientPairing_smul_left,
    coefficientPairing_symmetric par g f]

theorem coefficientPairing_parts (par : FieldParameters)
    (f g : ClosedPeriodicField par) :
    coefficientPairing par f (closedSpatialDerivative par g) =
      -coefficientPairing par (closedSpatialDerivative par f) g := by
  unfold coefficientPairing
  change par.h * periodicCoefficientIntegral par.Lx
      (∑ j, f j * (periodicSpatialEvolution par.Lx).toLinearMap (g j)) =
    -(par.h * periodicCoefficientIntegral par.Lx
      (∑ j, (periodicSpatialEvolution par.Lx).toLinearMap (f j) * g j))
  simp only [map_sum]
  simp_rw [periodicCoefficientIntegral_parts]
  rw [Finset.sum_neg_distrib]
  ring

def reducedHamiltonianVector (par : FieldParameters)
    (gradient : ClosedPeriodicPair par) : ClosedPeriodicPair par :=
  (-(closedSpatialDerivative par gradient.2), -(closedSpatialDerivative par gradient.1))

def coefficientGradientPairing (par : FieldParameters)
    (gradient tangent : ClosedPeriodicPair par) : ℝ :=
  coefficientPairing par gradient.1 tangent.1 +
    coefficientPairing par gradient.2 tangent.2

def reducedBracketValue (par : FieldParameters)
    (F G : ClosedPeriodicPair par) : ℝ :=
  coefficientGradientPairing par F (reducedHamiltonianVector par G)

theorem coefficientPairing_neg_right (par : FieldParameters)
    (f g : ClosedPeriodicField par) :
    coefficientPairing par f (-g) = -coefficientPairing par f g := by
  have hneg : (-1 : ℝ) • g = -g := by
    apply Subtype.ext
    funext j
    apply Subtype.ext
    funext x
    change (-1 : ℝ) * (g j : ℝ → ℝ) x = -(g j : ℝ → ℝ) x
    ring
  rw [← hneg, coefficientPairing_smul_right]
  ring

theorem reducedBracketValue_skew (par : FieldParameters)
    (F G : ClosedPeriodicPair par) :
    reducedBracketValue par F G = -reducedBracketValue par G F := by
  simp only [reducedBracketValue, coefficientGradientPairing,
    reducedHamiltonianVector, coefficientPairing_neg_right]
  rw [coefficientPairing_parts, coefficientPairing_parts]
  rw [coefficientPairing_symmetric par (closedSpatialDerivative par F.1) G.2,
    coefficientPairing_symmetric par (closedSpatialDerivative par F.2) G.1]
  ring

def FieldCoordinates.closedP {par : FieldParameters} (z : FieldCoordinates par) :
    ClosedPeriodicField par := ⟨fun j => z.p.coefficient j, by
  apply Subtype.ext
  funext x
  have hsum : ∑ j, z.p.value j x = 0 := by
    rw [sum_eq_card_mul_latticeMean par.M_ne_zero, z.p_zero, mul_zero]
  simpa [SmoothPeriodicField.coefficient] using hsum⟩

def FieldCoordinates.closedS {par : FieldParameters} (z : FieldCoordinates par) :
    ClosedPeriodicField par := ⟨fun j => z.s.coefficient j, by
  apply Subtype.ext
  funext x
  have hsum : ∑ j, z.s.value j x = 0 := by
    rw [sum_eq_card_mul_latticeMean par.M_ne_zero, z.s_zero, mul_zero]
  simpa [SmoothPeriodicField.coefficient] using hsum⟩

def closedFieldToSmooth (par : FieldParameters) (f : ClosedPeriodicField par) :
    SmoothPeriodicField par.M par.Lx where
  value j := (f j : ℝ → ℝ)
  smooth j := (f j).property.1
  periodic j := (f j).property.2

def closedPairCoordinates (par : FieldParameters) (z : ClosedPeriodicPair par) :
    FieldCoordinates par where
  p := closedFieldToSmooth par z.1
  s := closedFieldToSmooth par z.2
  p_zero x := by
    have hz := congrArg (fun a : PeriodicCoefficient par.Lx => (a : ℝ → ℝ) x) z.1.property
    have hsum : ∑ j, (z.1 j : ℝ → ℝ) x = 0 := by simpa using hz
    change (∑ j, (z.1 j : ℝ → ℝ) x) / (par.M : ℝ) = 0
    rw [hsum, zero_div]
  s_zero x := by
    have hz := congrArg (fun a : PeriodicCoefficient par.Lx => (a : ℝ → ℝ) x) z.2.property
    have hsum : ∑ j, (z.2 j : ℝ → ℝ) x = 0 := by simpa using hz
    change (∑ j, (z.2 j : ℝ → ℝ) x) / (par.M : ℝ) = 0
    rw [hsum, zero_div]

theorem closedPairCoordinates_closedP (par : FieldParameters)
    (z : ClosedPeriodicPair par) : (closedPairCoordinates par z).closedP = z.1 := rfl

theorem closedPairCoordinates_closedS (par : FieldParameters)
    (z : ClosedPeriodicPair par) : (closedPairCoordinates par z).closedS = z.2 := rfl

theorem FieldCoordinates.closedPairCoordinates_recover {par : FieldParameters}
    (z : FieldCoordinates par) : closedPairCoordinates par (z.closedP, z.closedS) = z := by
  cases z
  rfl

def coefficientMomentum (par : FieldParameters) (z : ClosedPeriodicPair par) : ℝ :=
  coefficientPairing par z.1 z.2

theorem coefficientMomentum_eq_physical (par : FieldParameters)
    (z : FieldCoordinates par) :
    coefficientMomentum par (z.closedP, z.closedS) = z.physicalMomentum := by
  unfold coefficientMomentum coefficientPairing FieldCoordinates.physicalMomentum
  rw [map_sum]
  rfl

def momentumGradient (z : ClosedPeriodicPair par) : ClosedPeriodicPair par := (z.2, z.1)

theorem coefficientMomentum_affine_expansion (par : FieldParameters)
    (z v : ClosedPeriodicPair par) (ε : ℝ) :
    coefficientMomentum par (z + ε • v) = coefficientMomentum par z +
      ε * coefficientGradientPairing par (momentumGradient z) v +
        ε ^ 2 * coefficientMomentum par v := by
  change coefficientPairing par (z.1 + ε • v.1) (z.2 + ε • v.2) = _
  rw [coefficientPairing_add_left, coefficientPairing_add_right,
    coefficientPairing_add_right]
  simp only [coefficientPairing_smul_left, coefficientPairing_smul_right,
    coefficientMomentum, coefficientGradientPairing, momentumGradient]
  rw [coefficientPairing_symmetric par v.1 z.2]
  ring

/-- The variational momentum gradient follows from the actual integral,
by differentiating its exact quadratic restriction to each affine line. -/
theorem coefficientMomentum_hasDerivAt (par : FieldParameters)
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun ε : ℝ => coefficientMomentum par (z + ε • v))
      (coefficientGradientPairing par (momentumGradient z) v) 0 := by
  have h := ((hasDerivAt_const (0 : ℝ) (coefficientMomentum par z)).add
    ((hasDerivAt_id (0 : ℝ)).mul_const
      (coefficientGradientPairing par (momentumGradient z) v))).add
    (((hasDerivAt_id (0 : ℝ)).pow 2).mul_const (coefficientMomentum par v))
  have hfun : (fun ε : ℝ => coefficientMomentum par (z + ε • v)) =
      (fun ε => coefficientMomentum par z +
        ε * coefficientGradientPairing par (momentumGradient z) v +
        ε ^ 2 * coefficientMomentum par v) :=
    funext (coefficientMomentum_affine_expansion par z v)
  rw [hfun]
  convert h using 1 <;> simp <;> rfl

/-- The actual h-weighted momentum generates negative spatial translation. -/
theorem momentum_generates_translation (par : FieldParameters)
    (z : ClosedPeriodicPair par) :
    reducedHamiltonianVector par (momentumGradient z) =
      (-(closedSpatialDerivative par z.1), -(closedSpatialDerivative par z.2)) := rfl

#print axioms reducedBracketValue_skew
#print axioms coefficientMomentum_eq_physical
#print axioms coefficientMomentum_hasDerivAt
#print axioms momentum_generates_translation
end
end DLWLean
