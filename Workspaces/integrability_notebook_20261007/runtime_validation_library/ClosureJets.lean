import FieldCoordinates

/-! The common time mode in the closed physical equation is derived from
the differentiated mean constraint, using exact finite lattice identities.
The source of the spatial identities is deliberately an explicit input;
this file does not claim a full calculus model of physical trajectories. -/
namespace DLWLean
noncomputable section
open scoped BigOperators

def energyDerivativeJet {M : ℕ} (β : ℝ)
    (U w Ux wx Uxx Rwx Rwxx : Fin M → ℝ) (j : Fin M) : ℝ :=
  U j * Ux j * w j + (U j) ^ 2 * wx j / 2 + β * (w j) ^ 2 * wx j +
    wx j * Ux j + w j * Uxx j + wx j * Rwx j / 2 + w j * Rwxx j / 2

def physicalFluxDerivativeJet {M : ℕ} (β : ℝ)
    (U w Ux wx Uxx Rwxx : Fin M → ℝ) (j : Fin M) : ℝ :=
  U j * Ux j + 2 * β * w j * wx j + Uxx j + Rwxx j

def physicalWTimeJet {M : ℕ} (U w Ux wx wxx : Fin M → ℝ)
    (j : Fin M) : ℝ := wxx j - Ux j * w j - U j * wx j

/-- The local identity whose averaged two remainder terms vanish by the
fixed flux constraint and skewness of the lattice R operator. -/
theorem energy_derivative_jet_identity {M : ℕ} (β : ℝ)
    (U w Ux wx Uxx wxx Rwx Rwxx : Fin M → ℝ) (j : Fin M) :
    2 * energyDerivativeJet β U w Ux wx Uxx Rwx Rwxx j =
      physicalFluxDerivativeJet β U w Ux wx Uxx Rwxx j * w j -
        U j * physicalWTimeJet U w Ux wx wxx j +
          (Uxx j * w j + 2 * Ux j * wx j + U j * wxx j) + wx j * Rwx j := by
  unfold energyDerivativeJet physicalFluxDerivativeJet physicalWTimeJet
  ring

/-- Exact derivation of lambda = 2 Pi(e_x)/c. In particular the common
mode is not silently dropped from the physical U equation. -/
theorem common_time_mode_from_mean_constraint {M : ℕ} (β c lambdaValue : ℝ)
    (hc : c ≠ 0) (U w Ux wx Uxx wxx Rwx Rwxx : Fin M → ℝ)
    (hmeanw : latticeMean w = c)
    (hfluxxx : latticeMean (fun j =>
      Uxx j * w j + 2 * Ux j * wx j + U j * wxx j) = 0)
    (hskew : latticeMean (fun j => wx j * Rwx j) = 0)
    (hmeanTime : latticeMean (fun j =>
      (-physicalFluxDerivativeJet β U w Ux wx Uxx Rwxx j + lambdaValue) * w j +
        U j * physicalWTimeJet U w Ux wx wxx j) = 0) :
    lambdaValue = 2 * latticeMean (energyDerivativeJet β U w Ux wx Uxx Rwx Rwxx) / c := by
  have hmeanF : latticeMean (fun j =>
      physicalFluxDerivativeJet β U w Ux wx Uxx Rwxx j * w j -
        U j * physicalWTimeJet U w Ux wx wxx j) = lambdaValue * c := by
    have hpoint : (fun j =>
        (-physicalFluxDerivativeJet β U w Ux wx Uxx Rwxx j + lambdaValue) * w j +
          U j * physicalWTimeJet U w Ux wx wxx j) =
        (fun j => lambdaValue * w j -
          (physicalFluxDerivativeJet β U w Ux wx Uxx Rwxx j * w j -
            U j * physicalWTimeJet U w Ux wx wxx j)) := by
      funext j
      ring
    rw [hpoint, latticeMean_sub, latticeMean_mul_left, hmeanw] at hmeanTime
    linarith
  have hex := congrArg latticeMean
    (funext (energy_derivative_jet_identity β U w Ux wx Uxx wxx Rwx Rwxx))
  simp only [latticeMean_mul_left, latticeMean_add, hfluxxx, hskew, add_zero] at hex
  rw [hmeanF] at hex
  apply (eq_div_iff hc).2
  linarith

#print axioms common_time_mode_from_mean_constraint
end
end DLWLean
