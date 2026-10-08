import PolynomialMatrixWitness
import PhysicalEnergyEndpoint
import FourierMomentum

/-!
The finite amplitude backend. Literal polynomial differential entries,
their computed zero and linear epsilon coefficients, and the computed
frequency-polynomial leading coefficients yield a genuine arbitrarily
small field witness. Independence itself is never a premise.
-/
namespace DLWLean
noncomputable section
open scoped BigOperators DLWFieldTopology

theorem amplitudeFrequencyMatrix_det_ne_zero {N : ℕ}
    (frequency : Fin N → ℝ) (polynomials : Fin N → Polynomial ℝ)
    (amplitude : Fin N → ℝ) (hpositive : ∀ j, 0 < frequency j)
    (hdistinct : Function.Injective frequency)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ i.val)
    (hlead : ∀ i, (polynomials i).coeff i.val ≠ 0)
    (hamplitude : ∀ j, amplitude j ≠ 0) :
    (Matrix.det (fun i j => 2 * amplitude j * (polynomials i).eval (frequency j ^ 2))) ≠ 0 := by
  have hfactor : (fun i j => 2 * amplitude j * (polynomials i).eval (frequency j ^ 2)) =
      polynomialFrequencyMatrix (fun j => frequency j ^ 2) polynomials *
        Matrix.diagonal (fun j => 2 * amplitude j) := by
    ext i j
    simp only [Matrix.mul_diagonal, polynomialFrequencyMatrix]
    ring
  rw [hfactor, Matrix.det_mul, Matrix.det_diagonal]
  apply mul_ne_zero
  · exact squaredFrequencyPolynomial_det_ne_zero frequency polynomials hpositive hdistinct hdegree hlead
  · exact Finset.prod_ne_zero_iff.mpr (fun j _ => mul_ne_zero (by norm_num) (hamplitude j))

theorem actualAmplitudeMinor_small_positive_witness {N : ℕ}
    {V : Type*} [AddCommGroup V] [Module ℝ V]
    (covectors : ℝ → Fin N → V →ₗ[ℝ] ℝ) (directions : Fin N → V)
    (entries : Matrix (Fin N) (Fin N) (Polynomial ℝ))
    (hactual : ∀ eps i j, covectors eps i (directions j) = (entries i j).eval eps)
    (hzero : ∀ i j, (entries i j).coeff 0 = 0)
    (frequency : Fin N → ℝ) (polynomials : Fin N → Polynomial ℝ)
    (amplitude : Fin N → ℝ)
    (hlinear : ∀ i j, (entries i j).coeff 1 =
      2 * amplitude j * (polynomials i).eval (frequency j ^ 2))
    (hpositive : ∀ j, 0 < frequency j) (hdistinct : Function.Injective frequency)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ i.val)
    (hlead : ∀ i, (polynomials i).coeff i.val ≠ 0)
    (hamplitude : ∀ j, amplitude j ≠ 0) (radius : ℝ) (hradius : 0 < radius) :
    ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
      (covectorMinor (covectors eps) directions).det ≠ 0 := by
  have hentry : (fun i j => (entries i j).coeff 1) =
      (fun i j => 2 * amplitude j * (polynomials i).eval (frequency j ^ 2)) := by
    ext i j
    exact hlinear i j
  have hdet : (Matrix.det (fun i j => (entries i j).coeff 1)) ≠ 0 := by
    rw [hentry]
    exact amplitudeFrequencyMatrix_det_ne_zero frequency polynomials amplitude hpositive
      hdistinct hdegree hlead hamplitude
  obtain ⟨eps, heps, hsmall, hminor⟩ :=
    polynomialMatrixDet_small_positive_witness entries hzero hdet radius hradius
  refine ⟨eps, heps, hsmall, ?_⟩
  have hm : covectorMinor (covectors eps) directions = fun i j => (entries i j).eval eps := by
    ext i j
    exact hactual eps i j
  rwa [hm]

def periodicCosineSumCoefficient {N : ℕ} (par : FieldParameters)
    (mode : Fin N → ℕ) (amplitude : Fin N → ℝ) : PeriodicCoefficient par.Lx :=
  ⟨periodicCosineSum par.Lx mode amplitude,
    periodicCosineSum_smooth par.Lx mode amplitude,
    periodicCosineSum_periodic par.Lx (ne_of_gt par.Lx_pos) mode amplitude⟩

theorem periodicCosineSumCoefficient_integral_square {N : ℕ} (par : FieldParameters)
    (mode : Fin N → ℕ) (hmode : ∀ j, 0 < mode j) (hdistinct : Function.Injective mode)
    (amplitude : Fin N → ℝ) :
    periodicCoefficientIntegral par.Lx
      (periodicCosineSumCoefficient par mode amplitude * periodicCosineSumCoefficient par mode amplitude) =
      (par.Lx / 2) * ∑ j, amplitude j ^ 2 := by
  change (∫ x in (0 : ℝ)..par.Lx,
    periodicCosineSum par.Lx mode amplitude x * periodicCosineSum par.Lx mode amplitude x) = _
  simpa only [pow_two] using
    integral_periodicCosineSum_pair par.Lx par.Lx_pos mode hmode hdistinct amplitude amplitude

theorem periodicCosineSumCoefficient_scaled_integral_square_nonzero {N : ℕ}
    (par : FieldParameters) (mode : Fin (N + 1) → ℕ) (hmode : ∀ j, 0 < mode j)
    (hdistinct : Function.Injective mode) (amplitude : Fin (N + 1) → ℝ)
    (hamplitude : ∀ j, amplitude j ≠ 0) (eps : ℝ) (heps : eps ≠ 0) :
    periodicCoefficientIntegral par.Lx
      ((eps • periodicCosineSumCoefficient par mode amplitude) *
        (eps • periodicCosineSumCoefficient par mode amplitude)) ≠ 0 := by
  have hsum : 0 < ∑ j : Fin (N + 1), amplitude j ^ 2 := by
    apply Finset.sum_pos'
    · intro j _
      exact sq_nonneg (amplitude j)
    · exact ⟨0, Finset.mem_univ _, sq_pos_of_ne_zero (hamplitude 0)⟩
  have hfactor : (eps • periodicCosineSumCoefficient par mode amplitude) *
      (eps • periodicCosineSumCoefficient par mode amplitude) =
      (eps ^ 2) • (periodicCosineSumCoefficient par mode amplitude *
        periodicCosineSumCoefficient par mode amplitude) := by
    simp only [Algebra.smul_mul_assoc, Algebra.mul_smul_comm, smul_smul, pow_two]
  rw [hfactor, map_smul, periodicCosineSumCoefficient_integral_square par mode hmode hdistinct]
  change eps ^ 2 * ((par.Lx / 2) * ∑ j, amplitude j ^ 2) ≠ 0
  exact mul_ne_zero (pow_ne_zero 2 heps) (ne_of_gt (mul_pos (half_pos par.Lx_pos) hsum))

def balancedFourierDirection {N : ℕ} (par : FieldParameters) (mode : Fin N → ℕ)
    (j : Fin N) : ClosedPeriodicPair par :=
  balancedMomentumState par (periodicCosineCoefficient par (mode j))

theorem actualPhysicalFamily_small_Fourier_witness (par : FieldParameters) {N : ℕ}
    (mode : Fin (N + 1) → ℕ) (hmode : ∀ j, 0 < mode j) (hdistinct : Function.Injective mode)
    (amplitude : Fin (N + 1) → ℝ) (hamplitude : ∀ j, amplitude j ≠ 0)
    (polynomials : Fin (N + 1) → Polynomial ℝ)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ i.val)
    (hlead : ∀ i, (polynomials i).coeff i.val ≠ 0)
    (entries : Matrix (Fin (N + 1)) (Fin (N + 1)) (Polynomial ℝ))
    (hactual : ∀ eps i j, fieldPolynomialDifferential par
      (GlobalPDO.periodicDensityPolynomial par (2 * i.val + 1))
      (balancedMomentumState par (eps • periodicCosineSumCoefficient par mode amplitude))
      (balancedFourierDirection par mode j) = (entries i j).eval eps)
    (hzero : ∀ i j, (entries i j).coeff 0 = 0)
    (hlinear : ∀ i j, (entries i j).coeff 1 =
      2 * amplitude j * (polynomials i).eval (periodicFourierFrequency par.Lx (mode j) ^ 2))
    (radius : ℝ) (hradius : 0 < radius) :
    ∃ eps : ℝ, 0 < eps ∧ eps < radius ∧
      LinearIndependent ℝ (fun i : Fin (N + 2) => gradientCovector par
        (actualPhysicalFamilyGradient par i.val
          (balancedMomentumState par (eps • periodicCosineSumCoefficient par mode amplitude)))) := by
  let f := periodicCosineSumCoefficient par mode amplitude
  let z := fun eps : ℝ => balancedMomentumState par (eps • f)
  let odd := fun eps : ℝ => fun i : Fin (N + 1) => gradientCovector par
    (GlobalPDO.constructedChargeGradient par (2 * i.val + 1) (z eps))
  have hactual' : ∀ eps i j, odd eps i (balancedFourierDirection par mode j) =
      (entries i j).eval eps := by
    intro eps i j
    rw [show odd eps i = fieldPolynomialDifferential par
      (GlobalPDO.periodicDensityPolynomial par (2 * i.val + 1)) (z eps) from
      constructedCharge_gradientCovector par _ _]
    exact hactual eps i j
  obtain ⟨eps, heps, hsmall, hminor⟩ := actualAmplitudeMinor_small_positive_witness
    odd (balancedFourierDirection par mode) entries hactual' hzero
    (fun j => periodicFourierFrequency par.Lx (mode j)) polynomials amplitude hlinear
    (fun j => periodicFourierFrequency_pos par.Lx par.Lx_pos (mode j) (hmode j))
    ((periodicFourierFrequency_injective par.Lx (ne_of_gt par.Lx_pos)).comp hdistinct)
    hdegree hlead hamplitude radius hradius
  refine ⟨eps, heps, hsmall, ?_⟩
  apply actualPhysicalFamily_independent_from_odd_minor par (z eps)
    (balancedFourierDirection par mode) (balancedMomentumExtra par (eps • f)) hminor
  · intro j
    exact balancedMomentum_slice_derivative_zero par (eps • f)
      ((2 : ℝ) • balancedCoefficientField par (periodicCosineCoefficient par (mode j)))
  · exact balancedMomentum_extra_nonzero par (eps • f)
      (periodicCosineSumCoefficient_scaled_integral_square_nonzero par mode hmode hdistinct
        amplitude hamplitude eps (ne_of_gt heps))

#print axioms amplitudeFrequencyMatrix_det_ne_zero
#print axioms actualAmplitudeMinor_small_positive_witness
#print axioms actualPhysicalFamily_small_Fourier_witness
end
end DLWLean
