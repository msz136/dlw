import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Tactic

/-!
Pure algebra for replacing the first spectral charge by the physical
Hamiltonian. This module does not assert that a physical DLW realization
of its bilinear bracket or its spectral charges has been constructed.
-/
namespace DLWLean

variable {F : Type*} [AddCommGroup F] [Module ℝ F]

/-- An explicit bilinear bracket interface. The results below use only
bilinearity, skew symmetry and the stated central constant. -/
structure BracketData (F : Type*) [AddCommGroup F] [Module ℝ F] where
  bracket : F →ₗ[ℝ] F →ₗ[ℝ] F
  skew : ∀ f g, bracket f g = -bracket g f

def physicalHamiltonian (G velocity : ℝ) (C₁ P constant : F) : F :=
  (-8 * G) • C₁ + velocity • P + constant

def physicalFamily (G velocity : ℝ) (C : ℕ → F) (P constant : F) : ℕ → F
  | 0 => physicalHamiltonian G velocity (C 1) P constant
  | 1 => P
  | n + 2 => C (2 * n + 3)

theorem physicalHamiltonian_bracket_charge
    (J : BracketData F) (G velocity : ℝ) (C : ℕ → F) (P constant : F)
    (hCC : ∀ m n, 0 < m → 0 < n → J.bracket (C m) (C n) = 0)
    (hPC : ∀ n, 0 < n → J.bracket P (C n) = 0)
    (hcentral : ∀ f, J.bracket constant f = 0)
    (n : ℕ) (hn : 0 < n) :
    J.bracket (physicalHamiltonian G velocity (C 1) P constant) (C n) = 0 := by
  simp [physicalHamiltonian, hCC 1 n (by omega) hn, hPC n hn, hcentral]

theorem physicalHamiltonian_bracket_momentum
    (J : BracketData F) (G velocity : ℝ) (C : ℕ → F) (P constant : F)
    (hPC : ∀ n, 0 < n → J.bracket P (C n) = 0)
    (hPP : J.bracket P P = 0)
    (hcentral : ∀ f, J.bracket constant f = 0) :
    J.bracket (physicalHamiltonian G velocity (C 1) P constant) P = 0 := by
  have hCP : J.bracket (C 1) P = 0 := by
    rw [J.skew, hPC 1 (by omega), neg_zero]
  simp [physicalHamiltonian, hCP, hPP, hcentral]

theorem bracket_self_eq_zero (J : BracketData F) (f : F) :
    J.bracket f f = 0 := by
  have h : J.bracket f f + J.bracket f f = 0 := by
    conv_lhs => lhs; rw [J.skew]
    simp
  have h₂ : (2 : ℝ) • J.bracket f f = 0 := by simpa [two_smul] using h
  exact (smul_eq_zero.mp h₂).resolve_left (by norm_num)

theorem physical_family_commutes
    (J : BracketData F) (G velocity : ℝ) (C : ℕ → F) (P constant : F)
    (hCC : ∀ m n, 0 < m → 0 < n → J.bracket (C m) (C n) = 0)
    (hPC : ∀ n, 0 < n → J.bracket P (C n) = 0)
    (hcentral : ∀ f, J.bracket constant f = 0) :
    ∀ m n, J.bracket (physicalFamily G velocity C P constant m)
      (physicalFamily G velocity C P constant n) = 0 := by
  intro m n
  have hself := bracket_self_eq_zero J
  rcases m with _ | _ | m
  · rcases n with _ | _ | n
    · exact hself _
    · exact physicalHamiltonian_bracket_momentum J G velocity C P constant hPC
        (hself P) hcentral
    · exact physicalHamiltonian_bracket_charge J G velocity C P constant
        hCC hPC hcentral _ (by omega)
  · rcases n with _ | _ | n
    · rw [J.skew]
      simp only [physicalFamily]
      rw [physicalHamiltonian_bracket_momentum J G velocity C P constant hPC
        (hself P) hcentral, neg_zero]
    · exact hself P
    · exact hPC _ (by omega)
  · rcases n with _ | _ | n
    · rw [J.skew]
      simp only [physicalFamily]
      rw [physicalHamiltonian_bracket_charge J G velocity C P constant
        hCC hPC hcentral _ (by omega), neg_zero]
    · simp only [physicalFamily]
      rw [J.skew, hPC _ (by omega), neg_zero]
    · exact hCC _ _ (by omega) (by omega)

/-- Conservation along a given differentiable trajectory is a consequence
of the Hamilton differentiation rule and a zero bracket. -/
theorem conserved_of_hamilton_rule
    {X : Type*} (J : BracketData (X → ℝ)) (K f : X → ℝ) (z : ℝ → X)
    (hamilton_rule : ∀ t, HasDerivAt (fun τ => f (z τ)) (J.bracket f K (z t)) t)
    (hcomm : J.bracket f K = 0) :
    ∀ t, HasDerivAt (fun τ => f (z τ)) 0 t := by
  intro t
  simpa [hcomm] using hamilton_rule t

theorem trace_one_energy_to_physical
    (G B γ c h M Lx H₀ P C₁ : ℝ) (hc : c ≠ 0) (hG : G ≠ 0)
    (htrace : C₁ = -H₀ / (8 * G) + (G ^ 2 / 12 + B ^ 2) * Lx) :
    H₀ - γ * (h * M * Lx * (γ / c) - P / c) =
      -8 * G * C₁ + (γ / c) * P +
        (8 * G * (G ^ 2 / 12 + B ^ 2) * Lx - γ ^ 2 * h * M * Lx / c) := by
  rw [htrace]
  field_simp
  ring

#print axioms physical_family_commutes
#print axioms conserved_of_hamilton_rule
#print axioms trace_one_energy_to_physical

end DLWLean
