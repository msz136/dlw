import MomentumWitness
import QuadraticResolvent

namespace DLWLean
noncomputable section

def periodicCosineCoefficient (par : FieldParameters) (mode : ℕ) :
    PeriodicCoefficient par.Lx :=
  ⟨periodicCosine par.Lx mode, periodicCosine_smooth par.Lx mode,
    periodicCosine_periodic par.Lx (ne_of_gt par.Lx_pos) mode⟩

theorem periodicCosineCoefficient_integral_square (par : FieldParameters)
    (mode : ℕ) (hmode : 0 < mode) :
    periodicCoefficientIntegral par.Lx
      (periodicCosineCoefficient par mode * periodicCosineCoefficient par mode) =
      par.Lx / 2 := by
  change (∫ x in (0 : ℝ)..par.Lx, periodicCosine par.Lx mode x *
    periodicCosine par.Lx mode x) = _
  simpa only [pow_two] using integral_periodicCosine_sq par.Lx par.Lx_pos mode hmode

/-- The extra direction is nonzero on an explicit actual Fourier field,
for every allowed period and every positive integer spatial mode. -/
theorem Fourier_momentum_extra_nonzero (par : FieldParameters)
    (mode : ℕ) (hmode : 0 < mode) :
    coefficientGradientPairing par
      (momentumGradient (balancedMomentumState par (periodicCosineCoefficient par mode)))
      (balancedMomentumExtra par (periodicCosineCoefficient par mode)) ≠ 0 := by
  apply balancedMomentum_extra_nonzero
  rw [periodicCosineCoefficient_integral_square par mode hmode]
  exact ne_of_gt (half_pos par.Lx_pos)

theorem Fourier_momentum_extra_derivative (par : FieldParameters)
    (mode : ℕ) (hmode : 0 < mode) :
    HasDerivAt (fun ε : ℝ => coefficientMomentum par
      (balancedMomentumState par (periodicCosineCoefficient par mode) +
        ε • balancedMomentumExtra par (periodicCosineCoefficient par mode)))
      (2 * par.h * par.Lx) 0 := by
  have h := balancedMomentum_hasDerivAt par (periodicCosineCoefficient par mode)
  rw [periodicCosineCoefficient_integral_square par mode hmode] at h
  convert h using 1 <;> ring

#print axioms Fourier_momentum_extra_nonzero
#print axioms Fourier_momentum_extra_derivative
end
end DLWLean
