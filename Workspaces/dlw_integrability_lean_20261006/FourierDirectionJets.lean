import GlobalBalancedSliceBridge
import FourierAmplitudeWitness

namespace DLWLean
noncomputable section

theorem coefficientSpatialJet_integral_zero_of_integral_zero (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (hf : periodicCoefficientIntegral par.Lx f = 0) (k : ℕ) :
    periodicCoefficientIntegral par.Lx (coefficientSpatialJet par k f) = 0 := by
  cases k with
  | zero => exact hf
  | succ k => exact periodicCoefficientIntegral_space_zero par.Lx _

theorem balancedMomentumState_fieldJet_integral_zero (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (hf : periodicCoefficientIntegral par.Lx f = 0)
    (i : FieldJetIndex par) :
    periodicCoefficientIntegral par.Lx (fieldJet par i (balancedMomentumState par f)) = 0 := by
  rcases i with ⟨component, j, k⟩
  cases component with
  | false => simp [fieldJet, closedPairComponent, balancedMomentumState]
  | true =>
    change periodicCoefficientIntegral par.Lx
      (coefficientSpatialJet par k ((2 : ℝ) • balancedCoefficientField par f j)) = 0
    rw [balancedCoefficientField_eq_sign_smul, smul_smul, map_smul, map_smul,
      coefficientSpatialJet_integral_zero_of_integral_zero par f hf k, smul_zero]

theorem Fourier_direction_fieldJet_integral_zero (par : FieldParameters)
    (mode : ℕ) (hmode : 0 < mode) (i : FieldJetIndex par) :
    periodicCoefficientIntegral par.Lx
      (fieldJet par i (balancedMomentumState par (periodicCosineCoefficient par mode))) = 0 := by
  apply balancedMomentumState_fieldJet_integral_zero
  exact integral_periodicCosine_zero par.Lx par.Lx_pos mode hmode

theorem balancedMomentumState_add (par : FieldParameters)
    (f g : PeriodicCoefficient par.Lx) :
    balancedMomentumState par (f + g) = balancedMomentumState par f + balancedMomentumState par g := by
  apply Prod.ext
  · apply Subtype.ext
    funext j
    change (2 : ℝ) • balancedCoefficientField par (f + g) j =
      (2 : ℝ) • balancedCoefficientField par f j + (2 : ℝ) • balancedCoefficientField par g j
    simp only [balancedCoefficientField_eq_sign_smul, smul_add]
  · simp [balancedMomentumState]

theorem balancedMomentumState_smul (par : FieldParameters)
    (r : ℝ) (f : PeriodicCoefficient par.Lx) :
    balancedMomentumState par (r • f) = r • balancedMomentumState par f := by
  apply Prod.ext
  · apply Subtype.ext
    funext j
    change (2 : ℝ) • balancedCoefficientField par (r • f) j =
      r • ((2 : ℝ) • balancedCoefficientField par f j)
    simp only [balancedCoefficientField_eq_sign_smul, smul_smul]
    congr 1
    ring
  · simp [balancedMomentumState]

#print axioms Fourier_direction_fieldJet_integral_zero
#print axioms balancedMomentumState_add
#print axioms balancedMomentumState_smul
end
end DLWLean
