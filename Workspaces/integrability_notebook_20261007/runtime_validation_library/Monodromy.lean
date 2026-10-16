import CyclicTrace
import Mathlib.Algebra.Group.Units.Basic
import Mathlib.Algebra.Ring.Commute

/-!
Finite transfer products and rational normalization in an arbitrary
associative real algebra. The link equations and the invertibility of
monodromy minus one are explicit starting hypotheses.
-/

namespace DLWLean

noncomputable section

variable {A : Type*} [Ring A] [Algebra ℝ A]

/-- The ordered prefix T_(n-1) ... T_0, with empty prefix one. -/
def transferProduct (T : ℕ → A) : ℕ → A
  | 0 => 1
  | n + 1 => T n * transferProduct T n

/-- Every finite transfer product inherits its two endpoint evolutions. -/
theorem transfer_product_evolution (d : AlgebraEvolution A)
    (T Q : ℕ → A) (n : ℕ)
    (hlink : ∀ j < n, d.toLinearMap (T j) = Q (j + 1) * T j - T j * Q j) :
    d.toLinearMap (transferProduct T n) =
      Q n * transferProduct T n - transferProduct T n * Q 0 := by
  induction n with
  | zero => simp [transferProduct, evolution_map_one]
  | succ n ih =>
    have hprefix : ∀ j < n,
        d.toLinearMap (T j) = Q (j + 1) * T j - T j * Q j :=
      fun j hj => hlink j (Nat.lt_succ_of_lt hj)
    rw [transferProduct, d.leibniz, hlink n (Nat.lt_succ_self n), ih hprefix]
    noncomm_ring

/-- Closing the endpoints gives the monodromy Lax equation for arbitrary
finite lattice length; no matrix dimension is used. -/
theorem periodic_monodromy_lax (d : AlgebraEvolution A)
    (T Q : ℕ → A) (n : ℕ)
    (hlink : ∀ j < n, d.toLinearMap (T j) = Q (j + 1) * T j - T j * Q j)
    (hclose : Q n = Q 0) :
    d.toLinearMap (transferProduct T n) =
      Q 0 * transferProduct T n - transferProduct T n * Q 0 := by
  rw [transfer_product_evolution d T Q n hlink, hclose]

/-- The noncommutative inverse differentiation identity follows from
Leibniz and the two unit identities. -/
theorem unit_inverse_evolution (d : AlgebraEvolution A) (u : Aˣ) :
    d.toLinearMap (↑u⁻¹ : A) =
      -(↑u⁻¹ : A) * d.toLinearMap (u : A) * (↑u⁻¹ : A) := by
  have h : d.toLinearMap (u : A) * (↑u⁻¹ : A) +
      (u : A) * d.toLinearMap (↑u⁻¹ : A) = 0 := by
    rw [← d.leibniz, Units.mul_inv, evolution_map_one]
  have hi := congrArg (fun a : A => (↑u⁻¹ : A) * a) h
  simp only [mul_add, ← mul_assoc, Units.inv_mul, one_mul, mul_zero] at hi
  simpa only [neg_mul, mul_assoc] using eq_neg_of_add_eq_zero_right hi

theorem unit_inverse_lax (d : AlgebraEvolution A) (u : Aˣ) (Q : A)
    (hu : d.toLinearMap (u : A) = Q * (u : A) - (u : A) * Q) :
    d.toLinearMap (↑u⁻¹ : A) = Q * (↑u⁻¹ : A) - (↑u⁻¹ : A) * Q := by
  rw [unit_inverse_evolution, hu]
  simp only [mul_sub, sub_mul, neg_mul,
    mul_assoc, Units.mul_inv, mul_one]
  rw [← mul_assoc, Units.inv_mul, one_mul]
  abel

/-- G and B are fixed real normalization constants. The unit u represents
the operator M-1, hence its inverse is the resolvent in the manuscript. -/
def normalizedL (G B : ℝ) (u : Aˣ) : A :=
  (-G) • (↑u⁻¹ : A) + (B - G / 2) • (1 : A)

theorem normalizedL_lax (d : AlgebraEvolution A) (M Q : A)
    (G B : ℝ) (u : Aˣ) (hu : (u : A) = M - 1)
    (hM : d.toLinearMap M = Q * M - M * Q) :
    d.toLinearMap (normalizedL G B u) =
      Q * normalizedL G B u - normalizedL G B u * Q := by
  have huLax : d.toLinearMap (u : A) = Q * (u : A) - (u : A) * Q := by
    rw [hu, map_sub, evolution_map_one, hM]
    noncomm_ring
  have hinv := unit_inverse_lax d u Q huLax
  simp only [normalizedL, map_add, map_smul, hinv, evolution_map_one,
    smul_zero, add_zero, mul_add, add_mul, Algebra.mul_smul_comm, Algebra.smul_mul_assoc,
    mul_one, one_mul, smul_sub]
  abel

theorem inverse_commutes_monodromy (M : A) (u : Aˣ)
    (hu : (u : A) = M - 1) :
    M * (↑u⁻¹ : A) = (↑u⁻¹ : A) * M := by
  have hM : M = (u : A) + 1 := by rw [hu, sub_add_cancel]
  rw [hM]
  simp [add_mul, mul_add]

theorem normalizedL_commutes_monodromy (M : A) (G B : ℝ)
    (u : Aˣ) (hu : (u : A) = M - 1) :
    M * normalizedL G B u = normalizedL G B u * M := by
  simp only [normalizedL, mul_add, add_mul, Algebra.mul_smul_comm,
    Algebra.smul_mul_assoc, mul_one, one_mul, inverse_commutes_monodromy M u hu]

/-- The manuscript's rational spectral-gradient expression. -/
def rationalGradient (G B : ℝ) (u : Aˣ) (n : ℕ) : A :=
  G • ((↑u⁻¹ : A) * normalizedL G B u ^ (n - 1) * (↑u⁻¹ : A))

/-- This proves commutation of the explicit expression. Identifying it
with a functional derivative requires the spectral variation theorem. -/
theorem rationalGradient_commutes_monodromy (M : A) (G B : ℝ)
    (u : Aˣ) (hu : (u : A) = M - 1) (n : ℕ) :
    M * rationalGradient G B u n = rationalGradient G B u n * M := by
  have hA : Commute M (↑u⁻¹ : A) := inverse_commutes_monodromy M u hu
  have hL : Commute M (normalizedL G B u) :=
    normalizedL_commutes_monodromy M G B u hu
  have hp := (hA.mul_right (hL.pow_right (n - 1))).mul_right hA
  simpa only [rationalGradient, Algebra.mul_smul_comm, Algebra.smul_mul_assoc]
    using congrArg (fun a : A => G • a) hp.eq

theorem rationalGradients_adler_involution (tr : CyclicTrace A)
    (plus : A →ₗ[ℝ] A) (M : A) (G B : ℝ) (u : Aˣ)
    (hu : (u : A) = M - 1) (m n : ℕ) :
    tr.toLinearMap (rationalGradient G B u m *
      adler plus M (rationalGradient G B u n)) = 0 := by
  apply adler_commuting_gradients_involution
  · exact rationalGradient_commutes_monodromy M G B u hu n
  · exact rationalGradient_commutes_monodromy M G B u hu m

/-- Finite periodic link equations and a unit for M-1 give every normalized
spectral rate zero, through the explicit monodromy and resolvent construction. -/
theorem normalized_periodic_spectral_rates_zero (tr : CyclicTrace A)
    (d : AlgebraEvolution A) (T Q : ℕ → A) (N : ℕ)
    (hlink : ∀ j < N, d.toLinearMap (T j) = Q (j + 1) * T j - T j * Q j)
    (hclose : Q N = Q 0) (G B : ℝ) (u : Aˣ)
    (hu : (u : A) = transferProduct T N - 1) (n : ℕ) :
    spectralInvariantRate tr d (normalizedL G B u) n = 0 := by
  apply spectralInvariantRate_eq_zero tr d (normalizedL G B u) (Q 0)
  exact normalizedL_lax d (transferProduct T N) (Q 0) G B u hu
    (periodic_monodromy_lax d T Q N hlink hclose)

#print axioms periodic_monodromy_lax
#print axioms unit_inverse_evolution
#print axioms normalizedL_lax
#print axioms rationalGradients_adler_involution
#print axioms normalized_periodic_spectral_rates_zero

end

end DLWLean
