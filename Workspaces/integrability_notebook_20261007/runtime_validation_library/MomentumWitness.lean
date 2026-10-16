import PhysicalBracket
import Mathlib.Tactic

namespace DLWLean
noncomputable section
open scoped BigOperators

def firstLatticeSite (par : FieldParameters) : Fin par.M := ⟨0, by have := par.M_ge_two; omega⟩
def secondLatticeSite (par : FieldParameters) : Fin par.M := ⟨1, by have := par.M_ge_two; omega⟩

theorem first_ne_second (par : FieldParameters) : firstLatticeSite par ≠ secondLatticeSite par := by
  intro h
  have := congrArg Fin.val h
  simp [firstLatticeSite, secondLatticeSite] at this

def balancedCoefficientField (par : FieldParameters) (f : PeriodicCoefficient par.Lx) :
    ClosedPeriodicField par :=
  ⟨fun j => (if j = firstLatticeSite par then f else 0) -
      (if j = secondLatticeSite par then f else 0), by
    change (∑ j : Fin par.M, ((if j = firstLatticeSite par then f else 0) -
      (if j = secondLatticeSite par then f else 0))) = 0
    simp [Finset.sum_sub_distrib]⟩

theorem balancedCoefficientField_square_sum (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) :
    (∑ j, balancedCoefficientField par f j * balancedCoefficientField par f j) =
      2 * (f * f) := by
  have hpoint (j : Fin par.M) :
      balancedCoefficientField par f j * balancedCoefficientField par f j =
      (if j = firstLatticeSite par then f * f else 0) +
        (if j = secondLatticeSite par then f * f else 0) := by
    change ((if j = firstLatticeSite par then f else 0) -
      (if j = secondLatticeSite par then f else 0)) *
      ((if j = firstLatticeSite par then f else 0) -
      (if j = secondLatticeSite par then f else 0)) = _
    by_cases h0 : j = firstLatticeSite par
    · have h1 : j ≠ secondLatticeSite par := by simpa [h0] using first_ne_second par
      simp [h0, first_ne_second par]
    · by_cases h1 : j = secondLatticeSite par
      · simp only [h1, Ne.symm (first_ne_second par), if_false, if_true,
          zero_sub, zero_add]
        ring
      · simp [h0, h1]
  simp_rw [hpoint]
  simp [Finset.sum_add_distrib, two_mul]

def balancedMomentumState (par : FieldParameters) (f : PeriodicCoefficient par.Lx) :
    ClosedPeriodicPair par := ((2 : ℝ) • balancedCoefficientField par f, 0)

def balancedMomentumExtra (par : FieldParameters) (f : PeriodicCoefficient par.Lx) :
    ClosedPeriodicPair par := (0, balancedCoefficientField par f)

/-- The document's extra direction is an actual closed periodic field.
The factor 4h follows from the actual momentum's affine derivative. -/
theorem balancedMomentum_extra_derivative (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) :
    coefficientGradientPairing par (momentumGradient (balancedMomentumState par f))
      (balancedMomentumExtra par f) =
      4 * par.h * periodicCoefficientIntegral par.Lx (f * f) := by
  change coefficientPairing par 0 0 +
    coefficientPairing par ((2 : ℝ) • balancedCoefficientField par f) (balancedCoefficientField par f) = _
  rw [coefficientPairing_smul_left]
  have hz : coefficientPairing par 0 0 = 0 := by
    simp [coefficientPairing]
  rw [hz, zero_add]
  unfold coefficientPairing
  rw [balancedCoefficientField_square_sum]
  have htwo : (2 : PeriodicCoefficient par.Lx) * (f * f) = f * f + f * f := by ring
  rw [htwo, map_add]
  ring

theorem balancedMomentum_slice_derivative_zero (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (dp : ClosedPeriodicField par) :
    coefficientGradientPairing par (momentumGradient (balancedMomentumState par f))
      (dp, 0) = 0 := by
  change coefficientPairing par 0 dp + coefficientPairing par ((2 : ℝ) • balancedCoefficientField par f) 0 = 0
  have hleft : coefficientPairing par 0 dp = 0 := by
    change par.h * periodicCoefficientIntegral par.Lx (∑ j, (0 : PeriodicCoefficient par.Lx) * dp j) = 0
    simp
  have hright : coefficientPairing par ((2 : ℝ) • balancedCoefficientField par f) 0 = 0 := by
    change par.h * periodicCoefficientIntegral par.Lx
      (∑ j, ((2 : ℝ) • balancedCoefficientField par f) j * (0 : PeriodicCoefficient par.Lx)) = 0
    simp
  rw [hleft, hright, add_zero]

theorem balancedMomentum_extra_nonzero (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx)
    (hf : periodicCoefficientIntegral par.Lx (f * f) ≠ 0) :
    coefficientGradientPairing par (momentumGradient (balancedMomentumState par f))
      (balancedMomentumExtra par f) ≠ 0 := by
  rw [balancedMomentum_extra_derivative]
  exact mul_ne_zero (mul_ne_zero (by norm_num) (ne_of_gt par.h_pos)) hf

theorem balancedMomentum_hasDerivAt (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) :
    HasDerivAt (fun ε : ℝ => coefficientMomentum par
      (balancedMomentumState par f + ε • balancedMomentumExtra par f))
      (4 * par.h * periodicCoefficientIntegral par.Lx (f * f)) 0 := by
  rw [← balancedMomentum_extra_derivative]
  exact coefficientMomentum_hasDerivAt par _ _

#print axioms balancedMomentum_hasDerivAt
#print axioms balancedMomentum_extra_nonzero
end
end DLWLean
