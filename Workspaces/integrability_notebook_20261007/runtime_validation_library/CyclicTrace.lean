import Mathlib.Basic.Real.Basic
import Mathlib.Algebra.Algebra.Defs
import Mathlib.Algebra.Module.LinearMap.Basic
import Mathlib.Tactic.NoncommRing

/-!
Algebraic trace and Adler identities used by the DLW formalization.

The operator algebra, its cyclic trace, and its time evolution are explicit
inputs. This module does not construct a periodic pseudo-differential algebra
or identify an Adler pairing with the physical reduced bracket.
-/

namespace DLWLean

noncomputable section

variable {A : Type*} [Ring A] [Algebra ℝ A]

/-- An arbitrary real-linear cyclic trace on an associative real algebra. -/
structure CyclicTrace (A : Type*) [Ring A] [Algebra ℝ A] where
  toLinearMap : A →ₗ[ℝ] ℝ
  cyclic : ∀ a b : A, toLinearMap (a * b) = toLinearMap (b * a)

/-- An arbitrary real-linear noncommutative derivation. -/
structure AlgebraEvolution (A : Type*) [Ring A] [Algebra ℝ A] where
  toLinearMap : A →ₗ[ℝ] A
  leibniz : ∀ a b : A,
    toLinearMap (a * b) = toLinearMap a * b + a * toLinearMap b

theorem evolution_map_one (d : AlgebraEvolution A) : d.toLinearMap 1 = 0 := by
  have h := d.leibniz (1 : A) 1
  simp only [one_mul, mul_one] at h
  have hs := congrArg (fun a : A => a - d.toLinearMap 1) h
  simpa only [sub_self, add_sub_cancel_right] using hs.symm

/-- The Lax equation propagates to every natural power in a genuine
noncommutative algebra, including the zeroth power. -/
theorem lax_power_evolution (d : AlgebraEvolution A) (L Q : A)
    (hL : d.toLinearMap L = Q * L - L * Q) (n : ℕ) :
    d.toLinearMap (L ^ n) = Q * L ^ n - L ^ n * Q := by
  induction n with
  | zero => simp [evolution_map_one]
  | succ n ih =>
    rw [pow_succ, d.leibniz, ih, hL]
    noncomm_ring

theorem trace_commutator_zero (tr : CyclicTrace A) (a b : A) :
    tr.toLinearMap (a * b - b * a) = 0 := by
  rw [map_sub, tr.cyclic, sub_self]

/-- The algebraic derivative of every trace power vanishes along a Lax
evolution. Periodic residue trace is one intended model of the interface. -/
theorem trace_lax_power_zero (tr : CyclicTrace A) (d : AlgebraEvolution A)
    (L Q : A) (hL : d.toLinearMap L = Q * L - L * Q) (n : ℕ) :
    tr.toLinearMap (d.toLinearMap (L ^ n)) = 0 := by
  rw [lax_power_evolution d L Q hL n]
  exact trace_commutator_zero tr Q (L ^ n)

/-- The spectral functional with the document's normalization. -/
def spectralInvariant (tr : CyclicTrace A) (L : A) (n : ℕ) : ℝ :=
  (n : ℝ)⁻¹ * tr.toLinearMap (L ^ n)

/-- Its formal time rate under the supplied operator derivation. -/
def spectralInvariantRate (tr : CyclicTrace A) (d : AlgebraEvolution A)
    (L : A) (n : ℕ) : ℝ :=
  (n : ℝ)⁻¹ * tr.toLinearMap (d.toLinearMap (L ^ n))

theorem spectralInvariantRate_eq_zero (tr : CyclicTrace A)
    (d : AlgebraEvolution A) (L Q : A)
    (hL : d.toLinearMap L = Q * L - L * Q) (n : ℕ) :
    spectralInvariantRate tr d L n = 0 := by
  simp [spectralInvariantRate, trace_lax_power_zero tr d L Q hL n]

/-- The Adler expression; the supplied linear map represents the plus part.
The identities below require neither idempotence nor an r-matrix axiom. -/
def adler (plus : A →ₗ[ℝ] A) (L X : A) : A :=
  plus (L * X) * L - L * plus (X * L)

/-- The purely algebraic product identity behind Adler factorization. -/
theorem adler_product (plus : A →ₗ[ℝ] A) (a b X : A) :
    adler plus (a * b) X =
      adler plus a (b * X) * b + a * adler plus b (X * a) := by
  simp only [adler, mul_assoc]
  noncomm_ring

theorem adler_eq_commutator_of_commutes (plus : A →ₗ[ℝ] A)
    (L X : A) (hX : L * X = X * L) :
    adler plus L X = plus (L * X) * L - L * plus (L * X) := by
  simp only [adler, ← hX]

/-- Pairing an inner evolution of L with any element commuting with L
gives zero, by cyclicity alone. -/
theorem trace_commutator_pairing_zero (tr : CyclicTrace A) (L Y Q : A)
    (hY : L * Y = Y * L) :
    tr.toLinearMap (Y * (Q * L - L * Q)) = 0 := by
  rw [mul_sub, map_sub]
  have ht : tr.toLinearMap (Y * (Q * L)) =
      tr.toLinearMap (Y * (L * Q)) := by
    calc
      tr.toLinearMap (Y * (Q * L)) =
          tr.toLinearMap ((Y * Q) * L) := by rw [mul_assoc]
      _ = tr.toLinearMap (L * (Y * Q)) := tr.cyclic _ _
      _ = tr.toLinearMap ((L * Y) * Q) := by rw [mul_assoc]
      _ = tr.toLinearMap ((Y * L) * Q) := by rw [hY]
      _ = tr.toLinearMap (Y * (L * Q)) := by rw [mul_assoc]
  rw [ht, sub_self]

/-- Two gradients commuting with L have zero Adler trace pairing.
Physical Poisson involution additionally needs a proved bracket transport. -/
theorem adler_commuting_gradients_involution (tr : CyclicTrace A)
    (plus : A →ₗ[ℝ] A) (L X Y : A)
    (hX : L * X = X * L) (hY : L * Y = Y * L) :
    tr.toLinearMap (Y * adler plus L X) = 0 := by
  rw [adler_eq_commutator_of_commutes plus L X hX]
  exact trace_commutator_pairing_zero tr L Y (plus (L * X)) hY

#print axioms lax_power_evolution
#print axioms trace_lax_power_zero
#print axioms spectralInvariantRate_eq_zero
#print axioms adler_product
#print axioms adler_commuting_gradients_involution

end

end DLWLean
