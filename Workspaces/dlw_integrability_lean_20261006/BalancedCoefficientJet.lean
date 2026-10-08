import DifferentialJetEvaluation

/-!
The relative coefficient two-jet is constructed from literal epsilon
substitution into an ordinary polynomial. No second variation formula is
assumed. All three maps commute with spatial differentiation by induction
on the coefficient polynomial and the actual field-jet derivative rule.
-/
namespace DLWLean.BalancedPDO
noncomputable section

variable {R : Type*} [CommRing R] [Algebra ℝ R]

def coefficientPerturbationVariable (M : ℕ) (field : Fin M → ℕ → R) :
    JetVariable M → Polynomial R
  | .b => 0
  | .eta => 0
  | .field j k => Polynomial.C (field j k) * Polynomial.X

def coefficientPerturbationEvaluation (M : ℕ) (field : Fin M → ℕ → R) :
    Poly M →ₐ[ℝ] Polynomial R :=
  MvPolynomial.aeval (coefficientPerturbationVariable M field)

def coefficientFirstMap : Polynomial R →ₗ[ℝ] R :=
  (Polynomial.lcoeff R 1).restrictScalars ℝ

def coefficientSecondMap : Polynomial R →ₗ[ℝ] R :=
  (2 : ℝ) • (Polynomial.lcoeff R 2).restrictScalars ℝ

def polynomialCoefficientJet : AlgebraJet2 (Polynomial R) R where
  value := (Polynomial.aeval (0 : R)).restrictScalars ℝ
  first := coefficientFirstMap
  second := coefficientSecondMap
  first_mul p q := by
    change (p * q).coeff 1 = p.coeff 1 * q.eval 0 + p.eval 0 * q.coeff 1
    rw [← Polynomial.coeff_zero_eq_eval_zero, ← Polynomial.coeff_zero_eq_eval_zero]
    rw [Polynomial.mul_coeff_one]
    ring
  second_mul p q := by
    change (2 : ℝ) • (p * q).coeff 2 =
      ((2 : ℝ) • p.coeff 2) * q.eval 0 + p.coeff 1 * q.coeff 1 +
      p.coeff 1 * q.coeff 1 + p.eval 0 * ((2 : ℝ) • q.coeff 2)
    rw [← Polynomial.coeff_zero_eq_eval_zero, ← Polynomial.coeff_zero_eq_eval_zero]
    rw [Polynomial.coeff_mul, Finset.Nat.sum_antidiagonal_eq_sum_range_succ_mk]
    simp only [Finset.sum_range_succ,
      Finset.sum_range_zero, zero_add]
    dsimp
    simp only [Algebra.smul_def, map_ofNat]
    ring

def actualCoefficientJet (M : ℕ) (field : Fin M → ℕ → R) :
    AlgebraJet2 (Poly M) R where
  value := polynomialCoefficientJet.value.comp (coefficientPerturbationEvaluation M field)
  first := polynomialCoefficientJet.first.comp
    (coefficientPerturbationEvaluation M field).toLinearMap
  second := polynomialCoefficientJet.second.comp
    (coefficientPerturbationEvaluation M field).toLinearMap
  first_mul p q := by
    simp only [LinearMap.comp_apply, AlgHom.toLinearMap_apply, map_mul]
    exact polynomialCoefficientJet.first_mul _ _
  second_mul p q := by
    simp only [LinearMap.comp_apply, AlgHom.toLinearMap_apply, map_mul]
    exact polynomialCoefficientJet.second_mul _ _

theorem actualCoefficientJet_value_eq_coeff0 (M : ℕ) (field : Fin M → ℕ → R)
    (p : Poly M) :
    (actualCoefficientJet M field).value p =
      (coefficientPerturbationEvaluation M field p).coeff 0 := by
  change Polynomial.eval 0 (coefficientPerturbationEvaluation M field p) = _
  rw [← Polynomial.coeff_zero_eq_eval_zero]

theorem actualCoefficientJet_first_eq_coeff1 (M : ℕ) (field : Fin M → ℕ → R)
    (p : Poly M) :
    (actualCoefficientJet M field).first p =
      (coefficientPerturbationEvaluation M field p).coeff 1 := rfl

theorem actualCoefficientJet_second_eq_coeff2 (M : ℕ) (field : Fin M → ℕ → R)
    (p : Poly M) :
    (actualCoefficientJet M field).second p =
      (2 : ℝ) • (coefficientPerturbationEvaluation M field p).coeff 2 := rfl

@[simp] theorem actualCoefficientJet_value_C (M : ℕ) (field : Fin M → ℕ → R) (r : ℝ) :
    (actualCoefficientJet M field).value (MvPolynomial.C r) = algebraMap ℝ R r := by
  simpa only [MvPolynomial.algebraMap_eq] using (actualCoefficientJet M field).value.commutes r

@[simp] theorem actualCoefficientJet_first_C (M : ℕ) (field : Fin M → ℕ → R) (r : ℝ) :
    (actualCoefficientJet M field).first (MvPolynomial.C r) = 0 := by
  rw [actualCoefficientJet_first_eq_coeff1]
  simp [coefficientPerturbationEvaluation]

@[simp] theorem actualCoefficientJet_second_C (M : ℕ) (field : Fin M → ℕ → R) (r : ℝ) :
    (actualCoefficientJet M field).second (MvPolynomial.C r) = 0 := by
  rw [actualCoefficientJet_second_eq_coeff2]
  simp [coefficientPerturbationEvaluation]

@[simp] theorem actualCoefficientJet_value_X (M : ℕ) (field : Fin M → ℕ → R)
    (i : JetVariable M) : (actualCoefficientJet M field).value (MvPolynomial.X i) = 0 := by
  rw [actualCoefficientJet_value_eq_coeff0]
  simp only [coefficientPerturbationEvaluation, MvPolynomial.aeval_X]
  cases i <;> simp [coefficientPerturbationVariable]

@[simp] theorem actualCoefficientJet_first_X_b (M : ℕ) (field : Fin M → ℕ → R) :
    (actualCoefficientJet M field).first (MvPolynomial.X .b) = 0 := by
  rw [actualCoefficientJet_first_eq_coeff1]
  simp [coefficientPerturbationEvaluation, coefficientPerturbationVariable]

@[simp] theorem actualCoefficientJet_first_X_eta (M : ℕ) (field : Fin M → ℕ → R) :
    (actualCoefficientJet M field).first (MvPolynomial.X .eta) = 0 := by
  rw [actualCoefficientJet_first_eq_coeff1]
  simp [coefficientPerturbationEvaluation, coefficientPerturbationVariable]

@[simp] theorem actualCoefficientJet_first_X_field (M : ℕ) (field : Fin M → ℕ → R)
    (j : Fin M) (k : ℕ) :
    (actualCoefficientJet M field).first (MvPolynomial.X (.field j k)) = field j k := by
  rw [actualCoefficientJet_first_eq_coeff1]
  simp [coefficientPerturbationEvaluation, coefficientPerturbationVariable]

@[simp] theorem actualCoefficientJet_second_X (M : ℕ) (field : Fin M → ℕ → R)
    (i : JetVariable M) : (actualCoefficientJet M field).second (MvPolynomial.X i) = 0 := by
  rw [actualCoefficientJet_second_eq_coeff2]
  simp only [coefficientPerturbationEvaluation, MvPolynomial.aeval_X]
  cases i <;> simp [coefficientPerturbationVariable]

theorem actualCoefficientJet_value_spatial (M : ℕ) (field : Fin M → ℕ → R)
    (d : AlgebraEvolution R) (p : Poly M) :
    (actualCoefficientJet M field).value (spatialDerivative M p) =
      d.toLinearMap ((actualCoefficientJet M field).value p) := by
  let jet := actualCoefficientJet M field
  change jet.value (spatialDerivative M p) = d.toLinearMap (jet.value p)
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero]
    simp only [jet, actualCoefficientJet_value_C]
    rw [
      Algebra.algebraMap_eq_smul_one, map_smul, evolution_map_one, smul_zero]
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p i hp =>
    have hXi : spatialDerivative M (MvPolynomial.X i) = generatorDerivative M i :=
      MvPolynomial.mkDerivation_X ℝ (generatorDerivative M) i
    rw [Derivation.leibniz, hXi]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      map_add, map_mul, hp, d.leibniz]
    cases i <;> simp [jet, generatorDerivative]

theorem actualCoefficientJet_first_spatial (M : ℕ) (field : Fin M → ℕ → R)
    (d : AlgebraEvolution R)
    (hfield : ∀ j k, d.toLinearMap (field j k) = field j (k + 1)) (p : Poly M) :
    (actualCoefficientJet M field).first (spatialDerivative M p) =
      d.toLinearMap ((actualCoefficientJet M field).first p) := by
  let jet := actualCoefficientJet M field
  have hv := actualCoefficientJet_value_spatial M field d
  change jet.first (spatialDerivative M p) = d.toLinearMap (jet.first p)
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero]
    simp [jet]
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p i hp =>
    have hXi : spatialDerivative M (MvPolynomial.X i) = generatorDerivative M i :=
      MvPolynomial.mkDerivation_X ℝ (generatorDerivative M) i
    rw [Derivation.leibniz, hXi]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      map_add, jet.first_mul, jet.value.map_mul, hp, hv, d.leibniz]
    cases i <;> simp [jet, generatorDerivative, hfield, hv, d.leibniz] <;> ring

theorem actualCoefficientJet_second_spatial (M : ℕ) (field : Fin M → ℕ → R)
    (d : AlgebraEvolution R)
    (hfield : ∀ j k, d.toLinearMap (field j k) = field j (k + 1)) (p : Poly M) :
    (actualCoefficientJet M field).second (spatialDerivative M p) =
      d.toLinearMap ((actualCoefficientJet M field).second p) := by
  let jet := actualCoefficientJet M field
  have hv := actualCoefficientJet_value_spatial M field d
  have hf := actualCoefficientJet_first_spatial M field d hfield
  change jet.second (spatialDerivative M p) = d.toLinearMap (jet.second p)
  induction p using MvPolynomial.induction_on with
  | C r =>
    rw [MvPolynomial.derivation_C, map_zero]
    simp [jet]
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p i hp =>
    have hXi : spatialDerivative M (MvPolynomial.X i) = generatorDerivative M i :=
      MvPolynomial.mkDerivation_X ℝ (generatorDerivative M) i
    rw [Derivation.leibniz, hXi]
    simp only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      map_add, jet.second_mul, jet.first_mul, jet.value.map_mul, hp, hv, hf,
      d.leibniz]
    cases i <;> simp [jet, generatorDerivative, hfield, hv, hf, d.leibniz] <;> ring

def actualDifferentialJetEvaluation (M : ℕ) (field : Fin M → ℕ → R)
    (d : AlgebraEvolution R)
    (hfield : ∀ j k, d.toLinearMap (field j k) = field j (k + 1)) :
    DifferentialJetEvaluation M R d where
  jet := actualCoefficientJet M field
  value_spatial := actualCoefficientJet_value_spatial M field d
  first_spatial := actualCoefficientJet_first_spatial M field d hfield
  second_spatial := actualCoefficientJet_second_spatial M field d hfield

theorem coefficientPerturbationEvaluation_real_eq (M : ℕ) (field : Fin M → ℕ → ℝ)
    (p : Poly M) :
    coefficientPerturbationEvaluation M field p = perturbationPolynomial M p 0 0 field := by
  change MvPolynomial.eval₂ (algebraMap ℝ (Polynomial ℝ))
      (coefficientPerturbationVariable M field) p = _
  unfold perturbationPolynomial
  congr 1
  funext i
  cases i <;> simp [coefficientPerturbationVariable, perturbationVariable]

theorem actualCoefficientJet_real_second_eq (M : ℕ) (field : Fin M → ℕ → ℝ)
    (p : Poly M) :
    (actualCoefficientJet M field).second p =
      2 * (perturbationPolynomial M p 0 0 field).coeff 2 := by
  rw [actualCoefficientJet_second_eq_coeff2, coefficientPerturbationEvaluation_real_eq,
    smul_eq_mul]

#print axioms actualCoefficientJet_second_eq_coeff2
#print axioms actualDifferentialJetEvaluation
#print axioms actualCoefficientJet_real_second_eq
end
end DLWLean.BalancedPDO
