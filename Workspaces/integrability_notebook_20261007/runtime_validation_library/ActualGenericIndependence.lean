import ActualFourierMatrix
import ActualBalancedAmplitudeBridge
import ActualFrequencyLeading

namespace DLWLean
noncomputable section
open scoped DLWFieldTopology

theorem actualFourierMatrix_coeff_one {N : ℕ} (par : FieldParameters)
    (mode : Fin N → ℕ) (hmode : ∀ j, 0 < mode j) (hdistinct : Function.Injective mode)
    (amplitude : Fin N → ℝ) (i j : Fin N) :
    (actualFourierMatrix par mode amplitude i j).coeff 1 =
      2 * amplitude j * (actualOddFrequencyPolynomial par i.val).eval
        (periodicFourierFrequency par.Lx (mode j) ^ 2) :=
  actualBalancedAmplitudeDifferential_coeff_one par i.val mode hmode hdistinct amplitude j

theorem actualOdd_small_Fourier_minor (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) {N : ℕ}
    (mode : Fin N → ℕ) (hmode : ∀ j, 0 < mode j) (hdistinct : Function.Injective mode)
    (amplitude : Fin N → ℝ) (hamplitude : ∀ j, amplitude j ≠ 0)
    (radius : ℝ) (hradius : 0 < radius) :
    ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
      (covectorMinor (fun i : Fin N => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1)
          (balancedMomentumState par (eps • periodicCosineSumCoefficient par mode amplitude))))
        (balancedFourierDirection par mode)).det ≠ 0 := by
  apply actualAmplitudeMinor_small_positive_witness
    (fun eps i => gradientCovector par (GlobalPDO.constructedChargeGradient par (2 * i.val + 1)
      (balancedMomentumState par (eps • periodicCosineSumCoefficient par mode amplitude))))
    (balancedFourierDirection par mode) (actualFourierMatrix par mode amplitude)
    _ (actualFourierMatrix_coeff_zero par mode hmode amplitude)
    (fun j => periodicFourierFrequency par.Lx (mode j))
    (fun i => actualOddFrequencyPolynomial par i.val) amplitude
    (actualFourierMatrix_coeff_one par mode hmode hdistinct amplitude)
    (fun j => periodicFourierFrequency_pos par.Lx par.Lx_pos (mode j) (hmode j))
    ((periodicFourierFrequency_injective par.Lx (ne_of_gt par.Lx_pos)).comp hdistinct)
    (fun i => actualOddFrequencyPolynomial_degree par i.val)
    (fun i => actualOddFrequencyPolynomial_leading_ne_zero par foundation i.val)
    hamplitude radius hradius
  intro eps i j
  rw [constructedCharge_gradientCovector]
  exact actualFourierMatrix_eval par mode amplitude eps i j

def canonicalWitnessMode {N : ℕ} (j : Fin N) : ℕ := j.val + 1

theorem canonicalWitnessMode_pos {N : ℕ} (j : Fin N) : 0 < canonicalWitnessMode j := by
  unfold canonicalWitnessMode
  omega

theorem canonicalWitnessMode_injective (N : ℕ) :
    Function.Injective (canonicalWitnessMode (N := N)) := by
  intro i j h
  apply Fin.ext
  unfold canonicalWitnessMode at h
  omega

/-- Every finite odd prefix is independent on an open dense subset of
the actual compact-jet smooth periodic field topology. The witness and
its complete nonlinear derivative minor have both been constructed. -/
theorem actualOdd_generically_independent (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (N : ℕ) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N => gradientCovector par
        (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) z)) := by
  let mode : Fin N → ℕ := canonicalWitnessMode
  let amplitude : Fin N → ℝ := fun _ => 1
  obtain ⟨eps, heps, _, hminor⟩ := actualOdd_small_Fourier_minor par foundation mode
    canonicalWitnessMode_pos (canonicalWitnessMode_injective N) amplitude
    (fun _ => by norm_num) 1 (by norm_num)
  let witness := balancedMomentumState par (eps • periodicCosineSumCoefficient par mode amplitude)
  let charges := fun i : Fin N => GlobalPDO.periodicDensityPolynomial par (2 * i.val + 1)
  have hw : fieldPolynomialDerivativeMinor par charges (balancedFourierDirection par mode) witness ≠ 0 := by
    change (covectorMinor (fun i => fieldPolynomialDifferential par (charges i) witness)
      (balancedFourierDirection par mode)).det ≠ 0
    simpa only [constructedCharge_gradientCovector] using hminor
  obtain ⟨S, ho, hd, hi⟩ := fieldPolynomialDifferentials_generically_independent par
    charges (balancedFourierDirection par mode) witness hw
  refine ⟨S, ho, hd, ?_⟩
  intro z hz
  simpa only [constructedCharge_gradientCovector] using hi z hz

theorem actualPhysicalFamily_independent_witness (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (N : ℕ) :
    ∃ witness : ClosedPeriodicPair par, LinearIndependent ℝ (fun i : Fin (N + 2) =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val witness)) := by
  let mode : Fin (N + 1) → ℕ := canonicalWitnessMode
  let amplitude : Fin (N + 1) → ℝ := fun _ => 1
  obtain ⟨eps, _, _, hw⟩ := actualPhysicalFamily_small_Fourier_witness par mode
    canonicalWitnessMode_pos (canonicalWitnessMode_injective (N + 1)) amplitude
    (fun _ => by norm_num) (fun i => actualOddFrequencyPolynomial par i.val)
    (fun i => actualOddFrequencyPolynomial_degree par i.val)
    (fun i => actualOddFrequencyPolynomial_leading_ne_zero par foundation i.val)
    (actualFourierMatrix par mode amplitude) (actualFourierMatrix_eval par mode amplitude)
    (actualFourierMatrix_coeff_zero par mode canonicalWitnessMode_pos amplitude)
    (actualFourierMatrix_coeff_one par mode canonicalWitnessMode_pos
      (canonicalWitnessMode_injective (N + 1)) amplitude) 1 (by norm_num)
  exact ⟨_, hw⟩

/-- The final physical Hamiltonian/momentum/odd-charge family has every
finite prefix generically independent, with no witness or independence
premise in the theorem. -/
theorem actualPhysicalFamily_generically_independent (par : FieldParameters)
    (foundation : ActualSpectralFoundation par) (N : ℕ) :
    ∃ S : Set (ClosedPeriodicPair par), IsOpen S ∧ Dense S ∧
      ∀ z ∈ S, LinearIndependent ℝ (fun i : Fin N =>
        gradientCovector par (actualPhysicalFamilyGradient par i.val z)) := by
  obtain ⟨witness, hw⟩ := actualPhysicalFamily_independent_witness par foundation N
  have hN : N ≤ N + 2 := by omega
  have hsmall : LinearIndependent ℝ (fun i : Fin N =>
      gradientCovector par (actualPhysicalFamilyGradient par i.val witness)) :=
    hw.comp (Fin.castLE hN) (Fin.castLE_injective hN)
  exact actualPhysicalFamily_generically_independent_from_witness par witness hsmall

#print axioms actualOdd_generically_independent
#print axioms actualPhysicalFamily_independent_witness
#print axioms actualPhysicalFamily_generically_independent
end
end DLWLean
