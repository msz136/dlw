import FieldGenericity
import PeriodicVariationalCalculus
import VariationalReduction
import Mathlib.Algebra.MvPolynomial.PDeriv
import AmbientEulerVariational

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem coefficientSpatialJet_eq_iterate (par : FieldParameters) (n : ℕ)
    (f : PeriodicCoefficient par.Lx) :
    coefficientSpatialJet par n f = periodicSpatialIterate n f := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change (periodicSpatialEvolution par.Lx).toLinearMap (coefficientSpatialJet par n f) = _
    rw [ih]
    exact (Function.iterate_succ_apply' _ n f).symm

theorem coefficientSpatialJet_integral_parts (par : FieldParameters) (n : ℕ)
    (a b : PeriodicCoefficient par.Lx) :
    periodicCoefficientIntegral par.Lx (a * coefficientSpatialJet par n b) =
      periodicCoefficientIntegral par.Lx
        (((-1 : ℝ) ^ n • coefficientSpatialJet par n a) * b) := by
  rw [coefficientSpatialJet_eq_iterate, coefficientSpatialJet_eq_iterate,
    periodicCoefficientIntegral_iterated_parts, smul_mul_assoc, map_smul, smul_eq_mul]

theorem projectedCoefficientGradient_pairing (par : FieldParameters)
    (f : Fin par.M → PeriodicCoefficient par.Lx) (v : ClosedPeriodicField par) :
    coefficientPairing par (projectedCoefficientGradient par f) v =
      par.h * periodicCoefficientIntegral par.Lx (∑ j, f j * v j) := by
  unfold coefficientPairing
  change par.h * periodicCoefficientIntegral par.Lx
    (∑ j, (f j - coefficientLatticeMean par f) * v j) = _
  have hv : (∑ j, v j) = 0 := v.property
  simp only [sub_mul, Finset.sum_sub_distrib, ← Finset.mul_sum, hv, mul_zero, sub_zero]

theorem coefficientGradientPairing_add_left (par : FieldParameters)
    (f g v : ClosedPeriodicPair par) :
    coefficientGradientPairing par (f + g) v =
      coefficientGradientPairing par f v + coefficientGradientPairing par g v := by
  simp only [coefficientGradientPairing, Prod.fst_add, Prod.snd_add,
    coefficientPairing_add_left]
  ring

theorem coefficientGradientPairing_sum_left (par : FieldParameters) {σ : Type*}
    (s : Finset σ) (f : σ → ClosedPeriodicPair par) (v : ClosedPeriodicPair par) :
    coefficientGradientPairing par (∑ i ∈ s, f i) v =
      ∑ i ∈ s, coefficientGradientPairing par (f i) v := by
  classical
  induction s using Finset.induction_on with
  | empty => simp [coefficientGradientPairing, coefficientPairing]
  | @insert i s hi ih =>
    simp only [Finset.sum_insert hi, coefficientGradientPairing_add_left, ih]

/-- A projected single-site Euler term represents one jet covector on the
actual closed tangent space. -/
def eulerJetGradient (par : FieldParameters) (i : FieldJetIndex par)
    (a : PeriodicCoefficient par.Lx) : ClosedPeriodicPair par :=
  if i.1 then
    (projectedCoefficientGradient par (Pi.single i.2.1 (par.h⁻¹ • a)), 0)
  else
    (0, projectedCoefficientGradient par (Pi.single i.2.1 (par.h⁻¹ • a)))

theorem eulerJetGradient_pairing (par : FieldParameters) (i : FieldJetIndex par)
    (a : PeriodicCoefficient par.Lx) (v : ClosedPeriodicPair par) :
    coefficientGradientPairing par (eulerJetGradient par i a) v =
      periodicCoefficientIntegral par.Lx (a * closedPairComponent par i.1 i.2.1 v) := by
  classical
  have hzero (w : ClosedPeriodicField par) : coefficientPairing par 0 w = 0 := by
    change par.h * periodicCoefficientIntegral par.Lx
      (∑ j : Fin par.M, (0 : PeriodicCoefficient par.Lx) * w j) = 0
    simp
  obtain ⟨b, j, n⟩ := i
  cases b <;>
    simp only [eulerJetGradient, Bool.false_eq_true, ↓reduceIte,
      coefficientGradientPairing, projectedCoefficientGradient_pairing,
      hzero, add_zero, zero_add,
      closedPairComponent, LinearMap.coe_mk, AddHom.coe_mk]
  all_goals
    simp only [Pi.single_apply, ite_mul, zero_mul, Finset.sum_ite_eq',
      Finset.mem_univ, ↓reduceIte, smul_mul_assoc, map_smul, smul_eq_mul]
    rw [← mul_assoc, mul_inv_cancel₀ (ne_of_gt par.h_pos), one_mul]

def fieldEulerTerm (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) (i : FieldJetIndex par) : PeriodicCoefficient par.Lx :=
  (-1 : ℝ) ^ i.2.2 • coefficientSpatialJet par i.2.2
    (fieldDifferentialPolynomial par (MvPolynomial.pderiv i p) z)

/-- Constructed, smooth and mean-zero Euler gradient for every finite
differential polynomial on the true periodic fields. -/
def fieldEulerGradient (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z : ClosedPeriodicPair par) : ClosedPeriodicPair par :=
  ∑ i ∈ p.vars, eulerJetGradient par i (fieldEulerTerm par p z i)

theorem fieldEulerGradient_pairing (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    coefficientGradientPairing par (fieldEulerGradient par p z) v =
      fieldPolynomialDifferential par p z v := by
  classical
  rw [fieldEulerGradient, coefficientGradientPairing_sum_left]
  simp_rw [eulerJetGradient_pairing]
  change (∑ i ∈ p.vars, periodicCoefficientIntegral par.Lx
    (fieldEulerTerm par p z i * closedPairComponent par i.1 i.2.1 v)) =
    periodicCoefficientIntegral par.Lx
      (fieldDifferentialPolynomial par (fieldPolynomialVariation par v p) z)
  unfold fieldPolynomialVariation
  rw [ambient_variation_eq_sum_pderiv]
  simp only [fieldDifferentialPolynomial, map_sum,
    MvPolynomial.eval_mul, MvPolynomial.eval_C, map_sum]
  apply Finset.sum_congr rfl
  intro i hi
  rw [mul_comm (fieldJet par i v)]
  exact (coefficientSpatialJet_integral_parts par i.2.2
    (MvPolynomial.eval (fun i => fieldJet par i z) (MvPolynomial.pderiv i p))
    (closedPairComponent par i.1 i.2.1 v)).symm

theorem fieldEulerGradient_hasDerivAt (par : FieldParameters)
    (p : MvPolynomial (FieldJetIndex par) (PeriodicCoefficient par.Lx))
    (z v : ClosedPeriodicPair par) :
    HasDerivAt (fun t : ℝ => fieldPolynomialIntegral par p (z + t • v))
      (coefficientGradientPairing par (fieldEulerGradient par p z) v) 0 := by
  rw [fieldEulerGradient_pairing]
  exact fieldPolynomialDifferential_hasDerivAt par p z v

#print axioms fieldEulerGradient_pairing
#print axioms fieldEulerGradient_hasDerivAt
end
end DLWLean
