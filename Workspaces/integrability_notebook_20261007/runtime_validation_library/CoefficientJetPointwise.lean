import BalancedCoefficientJet
import PeriodicCoefficients
import Mathlib.Algebra.Polynomial.AlgebraMap

namespace DLWLean.BalancedPDO
noncomputable section
variable {R S : Type*} [CommRing R] [Algebra ℝ R] [CommRing S] [Algebra ℝ S]

theorem coefficientPerturbationEvaluation_natural (M : ℕ)
    (field : Fin M → ℕ → R) (φ : R →ₐ[ℝ] S) (p : Poly M) :
    Polynomial.mapAlgHom φ (coefficientPerturbationEvaluation M field p) =
      coefficientPerturbationEvaluation M (fun j k => φ (field j k)) p := by
  have hh : (Polynomial.mapAlgHom φ).comp (coefficientPerturbationEvaluation M field) =
      coefficientPerturbationEvaluation M (fun j k => φ (field j k)) := by
    ext i
    simp only [AlgHom.comp_apply, coefficientPerturbationEvaluation, MvPolynomial.aeval_X]
    cases i <;> simp [coefficientPerturbationVariable, Polynomial.coe_mapAlgHom]
  exact congrArg (fun f : Poly M →ₐ[ℝ] Polynomial S => f p) hh

theorem coefficientPerturbationEvaluation_coefficient_natural (M : ℕ)
    (field : Fin M → ℕ → R) (φ : R →ₐ[ℝ] S) (p : Poly M) (n : ℕ) :
    φ ((coefficientPerturbationEvaluation M field p).coeff n) =
      (coefficientPerturbationEvaluation M (fun j k => φ (field j k)) p).coeff n := by
  rw [← Polynomial.coeff_mapAlgHom_apply φ,
    coefficientPerturbationEvaluation_natural M field φ p]

theorem actualCoefficientJet_second_natural (M : ℕ)
    (field : Fin M → ℕ → R) (φ : R →ₐ[ℝ] S) (p : Poly M) :
    φ ((actualCoefficientJet M field).second p) =
      (actualCoefficientJet M (fun j k => φ (field j k))).second p := by
  rw [actualCoefficientJet_second_eq_coeff2, map_smul,
    coefficientPerturbationEvaluation_coefficient_natural,
    actualCoefficientJet_second_eq_coeff2]

def periodicPointEvaluation (Lx x : ℝ) : PeriodicCoefficient Lx →ₐ[ℝ] ℝ :=
  (Pi.evalAlgHom ℝ (fun _ : ℝ => ℝ) x).comp (periodicCoefficientAlgebra Lx).val

theorem actualCoefficientJet_second_pointwise (M : ℕ) (Lx : ℝ)
    (field : Fin M → ℕ → PeriodicCoefficient Lx) (p : Poly M) (x : ℝ) :
    ((actualCoefficientJet M field).second p : ℝ → ℝ) x =
      2 * (perturbationPolynomial M p 0 0
        (fun j k => (field j k : ℝ → ℝ) x)).coeff 2 := by
  change periodicPointEvaluation Lx x ((actualCoefficientJet M field).second p) = _
  rw [actualCoefficientJet_second_natural,
    actualCoefficientJet_real_second_eq]
  rfl

#print axioms coefficientPerturbationEvaluation_coefficient_natural
#print axioms actualCoefficientJet_second_pointwise
end
end DLWLean.BalancedPDO
