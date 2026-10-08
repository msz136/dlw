import Mathlib.LinearAlgebra.Vandermonde
import Mathlib.LinearAlgebra.Matrix.ToLin
import Mathlib.LinearAlgebra.LinearIndependent.Lemmas
import Mathlib.Basic.Real.Basic
import Mathlib.Tactic.NormNum

/-!
Finite algebra used in the periodic-field independence argument.

This file proves the Vandermonde and covector replacement steps. It does
not construct physical DLW charge differentials or prove their quadratic
Fourier symbols. Those are separate, still required realization steps.
-/
namespace DLWLean

open Matrix Polynomial

/-- Columns are frequency nodes; rows are increasing polynomial orders. -/
def polynomialFrequencyMatrix {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ) : Matrix (Fin N) (Fin N) ℝ :=
  fun i j => (polynomials i).eval (nodes j)

/-- Triangular polynomial changes multiply the Vandermonde determinant by
the product of the diagonal coefficients. No monicity assumption is needed. -/
theorem polynomialFrequencyMatrix_det {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ (i : ℕ)) :
    (polynomialFrequencyMatrix nodes polynomials).det =
      (Matrix.vandermonde nodes).det *
        ∏ i : Fin N, (polynomials i).coeff (i : ℕ) := by
  have ht : polynomialFrequencyMatrix nodes polynomials =
      (Matrix.of (fun i j => (polynomials j).eval (nodes i)))ᵀ := rfl
  rw [ht, Matrix.det_transpose,
    Matrix.eval_matrixOfPolynomials_eq_vandermonde_mul_matrixOfPolynomials
      nodes polynomials hdegree, Matrix.det_mul,
    Matrix.det_of_isUpperTriangular
      (Matrix.matrixOfPolynomials_isUpperTriangular polynomials hdegree)]
  rfl

theorem polynomialFrequencyMatrix_det_ne_zero {N : ℕ} (nodes : Fin N → ℝ)
    (polynomials : Fin N → Polynomial ℝ)
    (hnodes : Function.Injective nodes)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ (i : ℕ))
    (hlead : ∀ i, (polynomials i).coeff (i : ℕ) ≠ 0) :
    (polynomialFrequencyMatrix nodes polynomials).det ≠ 0 := by
  rw [polynomialFrequencyMatrix_det nodes polynomials hdegree]
  exact mul_ne_zero (Matrix.det_vandermonde_ne_zero_iff.mpr hnodes)
    (Finset.prod_ne_zero_iff.mpr fun i _ => hlead i)

theorem positive_frequency_squares_injective {N : ℕ} (frequency : Fin N → ℝ)
    (hpositive : ∀ i, 0 < frequency i)
    (hdistinct : Function.Injective frequency) :
    Function.Injective (fun i => (frequency i) ^ 2) := by
  intro i j hij
  apply hdistinct
  exact (sq_eq_sq₀ (hpositive i).le (hpositive j).le).mp hij

/-- The all-finite-N Vandermonde step for distinct positive spatial frequencies. -/
theorem squaredFrequencyPolynomial_det_ne_zero {N : ℕ}
    (frequency : Fin N → ℝ) (polynomials : Fin N → Polynomial ℝ)
    (hpositive : ∀ i, 0 < frequency i)
    (hdistinct : Function.Injective frequency)
    (hdegree : ∀ i, (polynomials i).natDegree ≤ (i : ℕ))
    (hlead : ∀ i, (polynomials i).coeff (i : ℕ) ≠ 0) :
    (polynomialFrequencyMatrix (fun i => (frequency i) ^ 2) polynomials).det ≠ 0 :=
  polynomialFrequencyMatrix_det_ne_zero _ _
    (positive_frequency_squares_injective frequency hpositive hdistinct) hdegree hlead

theorem squaredFrequency_vandermonde_det_ne_zero {N : ℕ}
    (frequency : Fin N → ℝ)
    (hsquares : Function.Injective (fun i => (frequency i) ^ 2)) :
    (Matrix.vandermonde (fun i => (frequency i) ^ 2)).det ≠ 0 :=
  Matrix.det_vandermonde_ne_zero_iff.mpr hsquares

section Covectors

variable {V : Type*} [AddCommGroup V] [Module ℝ V]

/-- Evaluate a covector on a finite list of tangent directions. -/
def covectorEvaluation {N : ℕ} (directions : Fin N → V) :
    (V →ₗ[ℝ] ℝ) →ₗ[ℝ] (Fin N → ℝ) where
  toFun f i := f (directions i)
  map_add' f g := by ext i; rfl
  map_smul' a f := by ext i; rfl

def covectorMinor {N : ℕ} (covectors : Fin N → V →ₗ[ℝ] ℝ)
    (directions : Fin N → V) : Matrix (Fin N) (Fin N) ℝ :=
  fun i j => covectors i (directions j)

/-- A concrete nonzero Jacobian minor proves independence of the covectors. -/
theorem linearIndependent_of_covectorMinor_det_ne_zero {N : ℕ}
    (covectors : Fin N → V →ₗ[ℝ] ℝ) (directions : Fin N → V)
    (hdet : (covectorMinor covectors directions).det ≠ 0) :
    LinearIndependent ℝ covectors := by
  have hu : IsUnit (covectorMinor covectors directions) :=
    (Matrix.isUnit_iff_isUnit_det _).mpr (isUnit_iff_ne_zero.mpr hdet)
  have hrows := Matrix.linearIndependent_rows_of_isUnit hu
  apply LinearIndependent.of_comp (covectorEvaluation directions)
  exact hrows

/-- The momentum extension from the paper: the new covector annihilates
the invertible spectral test directions, but is nonzero on one extra
direction. All charges here are actual linear covectors on the same space. -/
theorem momentum_augments_covector_independence {N : ℕ}
    (odd : Fin N → V →ₗ[ℝ] ℝ) (directions : Fin N → V)
    (dP : V →ₗ[ℝ] ℝ) (extra : V)
    (hminor : (covectorMinor odd directions).det ≠ 0)
    (hannihilate : ∀ i, dP (directions i) = 0)
    (hextra : dP extra ≠ 0) :
    LinearIndependent ℝ (Fin.cons dP odd) := by
  have hu : IsUnit (covectorMinor odd directions) :=
    (Matrix.isUnit_iff_isUnit_det _).mpr (isUnit_iff_ne_zero.mpr hminor)
  have hrows : LinearIndependent ℝ
      (fun i => covectorEvaluation directions (odd i)) :=
    Matrix.linearIndependent_rows_of_isUnit hu
  have hodd := linearIndependent_of_covectorMinor_det_ne_zero odd directions hminor
  apply hodd.finCons
  intro hspan
  obtain ⟨coefficients, hcombination⟩ :=
    (Submodule.mem_span_range_iff_exists_fun ℝ).mp hspan
  have hevalzero : covectorEvaluation directions dP = 0 := by
    ext i
    exact hannihilate i
  have hsum : ∑ i, coefficients i • covectorEvaluation directions (odd i) = 0 := by
    have heval := congrArg (covectorEvaluation directions) hcombination
    simpa only [map_sum, map_smul, hevalzero] using heval
  have hcoefficients : ∀ i, coefficients i = 0 :=
    Fintype.linearIndependent_iff.mp hrows coefficients hsum
  have hdPzero : dP = 0 := by
    have hz : (0 : V →ₗ[ℝ] ℝ) = dP := by
      simpa [hcoefficients] using hcombination
    exact hz.symm
  apply hextra
  rw [hdPzero]
  rfl

end Covectors

section Replacement

variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

/-- Replace the first independent vector by a nonzero multiple of itself
plus a multiple of the next vector, retaining all later vectors. -/
theorem linearIndependent_cons_shear {N : ℕ} (first : V)
    (remaining : Fin (N + 1) → V) (a b : K) (ha : a ≠ 0)
    (hindependent : LinearIndependent K (Fin.cons first remaining)) :
    LinearIndependent K (Fin.cons (a • first + b • remaining 0) remaining) := by
  obtain ⟨htail, hfirst⟩ := linearIndependent_finCons.mp hindependent
  apply htail.finCons
  intro hshift
  apply hfirst
  let W := Submodule.span K (Set.range remaining)
  have hnext : remaining 0 ∈ W := Submodule.subset_span ⟨0, rfl⟩
  have hscaled : a • first ∈ W := by
    have hsub := W.sub_mem hshift (W.smul_mem b hnext)
    simpa using hsub
  exact (W.smul_mem_iff ha).mp hscaled

end Replacement

theorem linearIndependent_swap_first_two
    {K V : Type*} [Field K] [AddCommGroup V] [Module K V] {N : ℕ}
    (first second : V) (tail : Fin N → V)
    (hindependent : LinearIndependent K (Fin.cons first (Fin.cons second tail))) :
    LinearIndependent K (Fin.cons second (Fin.cons first tail)) := by
  have hswap : LinearIndependent K
      (Matrix.vecCons first (Matrix.vecCons second tail) ∘
        Equiv.swap (0 : Fin (N + 2)) 1) :=
    hindependent.comp _ (Equiv.swap _ _).injective
  rw [Matrix.cons_cons_comp_swap_zero_one] at hswap
  exact hswap

/-- Algebraic differential replacement corresponding to
K = -8 G C1 + velocity P + constant, whose constant differential is zero. -/
theorem physicalHamiltonian_covectors_independent
    {V : Type*} [AddCommGroup V] [Module ℝ V] {N : ℕ}
    (dC₁ : V) (remaining : Fin (N + 1) → V) (G velocity : ℝ)
    (hG : G ≠ 0)
    (hindependent : LinearIndependent ℝ (Fin.cons dC₁ remaining)) :
    LinearIndependent ℝ
      (Fin.cons ((-8 * G) • dC₁ + velocity • remaining 0) remaining) := by
  apply linearIndependent_cons_shear dC₁ remaining (-8 * G) velocity
    (mul_ne_zero (by norm_num) hG) hindependent

/-- Combine the actual odd-charge minor, the extra momentum direction,
and the Hamiltonian differential shear into the displayed final order. -/
theorem physical_covectors_independent_from_odd_minor
    {V : Type*} [AddCommGroup V] [Module ℝ V] {N : ℕ}
    (dC₁ dP : V →ₗ[ℝ] ℝ) (tail : Fin N → V →ₗ[ℝ] ℝ)
    (directions : Fin (N + 1) → V) (extra : V) (G velocity : ℝ)
    (hG : G ≠ 0)
    (hminor : (covectorMinor (Fin.cons dC₁ tail) directions).det ≠ 0)
    (hannihilate : ∀ i, dP (directions i) = 0)
    (hextra : dP extra ≠ 0) :
    LinearIndependent ℝ
      (Fin.cons ((-8 * G) • dC₁ + velocity • dP) (Fin.cons dP tail)) := by
  have hmomentum := momentum_augments_covector_independence
    (Fin.cons dC₁ tail) directions dP extra hminor hannihilate hextra
  have hspectral := linearIndependent_swap_first_two dP dC₁ tail hmomentum
  exact physicalHamiltonian_covectors_independent dC₁ (Fin.cons dP tail)
    G velocity hG hspectral

#print axioms polynomialFrequencyMatrix_det
#print axioms squaredFrequencyPolynomial_det_ne_zero
#print axioms linearIndependent_of_covectorMinor_det_ne_zero
#print axioms momentum_augments_covector_independence
#print axioms physicalHamiltonian_covectors_independent
#print axioms physical_covectors_independent_from_odd_minor

end DLWLean
