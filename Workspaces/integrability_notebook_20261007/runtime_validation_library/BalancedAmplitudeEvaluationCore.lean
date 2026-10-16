import GlobalBalancedSliceBridge
import CoefficientJetPointwise

namespace DLWLean
noncomputable section
open scoped BigOperators

def balancedPeriodicPerturbationVariable (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) : BalancedPDO.JetVariable par.M → Polynomial (PeriodicCoefficient par.Lx)
  | .b => Polynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) par.B)
  | .eta => Polynomial.C (algebraMap ℝ (PeriodicCoefficient par.Lx) (balancedEta par))
  | .field j k => Polynomial.C (periodicSpatialIterate k (balancedCoefficientField par f j)) * Polynomial.X

def balancedPeriodicPerturbationEvaluation (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) : BalancedPDO.Poly par.M →ₐ[ℝ] Polynomial (PeriodicCoefficient par.Lx) :=
  MvPolynomial.aeval (balancedPeriodicPerturbationVariable par f)

theorem balancedCoefficientField_smul (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (eps : ℝ) (j : Fin par.M) :
    balancedCoefficientField par (eps • f) j = eps • balancedCoefficientField par f j := by
  rw [balancedCoefficientField_eq_sign_smul, balancedCoefficientField_eq_sign_smul]
  exact smul_comm _ _ _

theorem balancedMomentumState_smul_amplitude (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (eps : ℝ) :
    eps • balancedMomentumState par f = balancedMomentumState par (eps • f) := by
  apply Prod.ext
  · apply Subtype.ext
    funext j
    change eps • ((2 : ℝ) • balancedCoefficientField par f j) =
      (2 : ℝ) • balancedCoefficientField par (eps • f) j
    rw [balancedCoefficientField_smul]
    exact smul_comm _ _ _
  · simp [balancedMomentumState]

theorem balancedPeriodicPerturbationEvaluation_eval (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (p : BalancedPDO.Poly par.M) (eps : ℝ) :
    (balancedPeriodicPerturbationEvaluation par f p).eval
      (algebraMap ℝ (PeriodicCoefficient par.Lx) eps) =
        balancedPeriodicEvaluation par (eps • f) p := by
  let φ : Polynomial (PeriodicCoefficient par.Lx) →ₐ[ℝ] PeriodicCoefficient par.Lx :=
    (Polynomial.aeval (algebraMap ℝ (PeriodicCoefficient par.Lx) eps)).restrictScalars ℝ
  have hhom : φ.comp (balancedPeriodicPerturbationEvaluation par f) =
      balancedPeriodicEvaluation par (eps • f) := by
    apply MvPolynomial.algHom_ext
    intro i
    simp only [AlgHom.comp_apply, balancedPeriodicPerturbationEvaluation, MvPolynomial.aeval_X,
      balancedPeriodicEvaluation_X]
    cases i with
    | b => simp [φ, balancedPeriodicPerturbationVariable, balancedPeriodicJet]
    | eta => simp [φ, balancedPeriodicPerturbationVariable, balancedPeriodicJet]
    | field j k =>
      simp only [φ, balancedPeriodicPerturbationVariable, balancedPeriodicJet,
        Polynomial.aeval_def, AlgHom.restrictScalars_apply,
        Polynomial.eval₂_mul, Polynomial.eval₂_C, Polynomial.eval₂_X,
        Algebra.algebraMap_self, RingHom.id_apply]
      rw [balancedCoefficientField_smul, periodicSpatialIterate_eq_coefficientSpatialJet,
        periodicSpatialIterate_eq_coefficientSpatialJet, map_smul]
      simp only [Algebra.smul_def, mul_comm]
  exact congrArg (fun q : BalancedPDO.Poly par.M →ₐ[ℝ] PeriodicCoefficient par.Lx => q p) hhom

theorem constructedCharge_balanced_density (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (n : ℕ) :
    GlobalPDO.constructedCharge par n (balancedMomentumState par f) =
      periodicCoefficientIntegral par.Lx (balancedPeriodicEvaluation par f
        (BalancedPDO.balancedSpectralDensityPolynomial par.M n)) := by
  rw [GlobalBalancedSlice.constructedCharge_balanced_slice]
  rw [BalancedPDO.balancedSpectralDensityPolynomial, map_mul,
    balancedPeriodicEvaluation_C]
  change _ = periodicCoefficientIntegral par.Lx
    ((n : ℝ)⁻¹ • balancedPeriodicEvaluation par f (BalancedPDO.balancedResiduePolynomial par.M n))
  rw [map_smul, smul_eq_mul]

theorem balancedPeriodicPerturbationEvaluation_pointwise (par : FieldParameters)
    (f : PeriodicCoefficient par.Lx) (p : BalancedPDO.Poly par.M) (q : ℕ) (x : ℝ) :
    ((balancedPeriodicPerturbationEvaluation par f p).coeff q : ℝ → ℝ) x =
      (BalancedPDO.perturbationPolynomial par.M p par.B (balancedEta par)
        (fun j k => balancedLatticeSign par j * iteratedDeriv k (f : ℝ → ℝ) x)).coeff q := by
  let φ := BalancedPDO.periodicPointEvaluation par.Lx x
  have hhom : (Polynomial.mapAlgHom φ).comp (balancedPeriodicPerturbationEvaluation par f) =
      MvPolynomial.aeval (BalancedPDO.perturbationVariable par.M par.B (balancedEta par)
        (fun j k => balancedLatticeSign par j * iteratedDeriv k (f : ℝ → ℝ) x)) := by
    apply MvPolynomial.algHom_ext
    intro i
    simp only [AlgHom.comp_apply, balancedPeriodicPerturbationEvaluation, MvPolynomial.aeval_X]
    cases i with
    | b => simp [balancedPeriodicPerturbationVariable, BalancedPDO.perturbationVariable,
        Polynomial.coe_mapAlgHom, φ]
    | eta => simp [balancedPeriodicPerturbationVariable, BalancedPDO.perturbationVariable,
        Polynomial.coe_mapAlgHom, φ]
    | field j k =>
      simp only [balancedPeriodicPerturbationVariable, BalancedPDO.perturbationVariable,
        map_mul, Polynomial.coe_mapAlgHom, Polynomial.map_C, Polynomial.map_X]
      rw [← Polynomial.C_mul]
      exact congrArg (fun r : ℝ => Polynomial.C r * Polynomial.X)
        (balancedCoefficientField_spatial_jet par f j k x)
  have hpoly := congrArg (fun H : BalancedPDO.Poly par.M →ₐ[ℝ] Polynomial ℝ => H p) hhom
  simp only [AlgHom.comp_apply] at hpoly
  change φ ((balancedPeriodicPerturbationEvaluation par f p).coeff q) = _
  rw [← Polynomial.coeff_mapAlgHom_apply φ, hpoly]
  rfl

end
end DLWLean
