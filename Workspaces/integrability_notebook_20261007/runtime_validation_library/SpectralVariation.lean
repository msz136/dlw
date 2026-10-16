import Monodromy
import Mathlib.Tactic.Ring

/-!
Spectral variation and the rational gradient are derived from Leibniz,
cyclicity, and the unit identity. No gradient formula is an input.
-/

namespace DLWLean

noncomputable section

variable {A : Type*} [Ring A] [Algebra ℝ A]

/-- A weighted trace variation; the extra power makes the induction close
without any commutativity assumption on the operator algebra. -/
theorem trace_power_variation_weighted (tr : CyclicTrace A)
    (v : AlgebraEvolution A) (L : A) (n k : ℕ) :
    tr.toLinearMap (L ^ k * v.toLinearMap (L ^ (n + 1))) =
      ((n + 1 : ℕ) : ℝ) * tr.toLinearMap (L ^ (k + n) * v.toLinearMap L) := by
  induction n generalizing k with
  | zero => simp
  | succ n ih =>
    rw [pow_succ, v.leibniz, mul_add, map_add]
    have hcycle : tr.toLinearMap (L ^ k *
        (v.toLinearMap (L ^ (n + 1)) * L)) =
        tr.toLinearMap (L ^ (k + 1) * v.toLinearMap (L ^ (n + 1))) := by
      calc
        tr.toLinearMap (L ^ k * (v.toLinearMap (L ^ (n + 1)) * L)) =
            tr.toLinearMap ((L ^ k * v.toLinearMap (L ^ (n + 1))) * L) :=
          congrArg tr.toLinearMap (mul_assoc _ _ _).symm
        _ = tr.toLinearMap (L * (L ^ k * v.toLinearMap (L ^ (n + 1)))) :=
          tr.cyclic _ _
        _ = tr.toLinearMap ((L * L ^ k) * v.toLinearMap (L ^ (n + 1))) :=
          congrArg tr.toLinearMap (mul_assoc _ _ _).symm
        _ = tr.toLinearMap (L ^ (k + 1) * v.toLinearMap (L ^ (n + 1))) := by
          simp only [pow_succ']
    rw [hcycle, ih (k + 1), ← mul_assoc, ← pow_add]
    have hexp : k + 1 + n = k + (n + 1) := by omega
    rw [hexp]
    push_cast
    ring

theorem trace_power_variation (tr : CyclicTrace A)
    (v : AlgebraEvolution A) (L : A) (n : ℕ) (hn : 0 < n) :
    tr.toLinearMap (v.toLinearMap (L ^ n)) =
      (n : ℝ) * tr.toLinearMap (L ^ (n - 1) * v.toLinearMap L) := by
  cases n with
  | zero => simp at hn
  | succ k =>
    simpa only [Nat.succ_eq_add_one, Nat.add_sub_cancel, zero_add,
      pow_zero, one_mul] using trace_power_variation_weighted tr v L k 0

/-- The normalization 1/n cancels the number of Leibniz terms. -/
theorem spectralInvariantRate_variation (tr : CyclicTrace A)
    (v : AlgebraEvolution A) (L : A) (n : ℕ) (hn : 0 < n) :
    spectralInvariantRate tr v L n =
      tr.toLinearMap (L ^ (n - 1) * v.toLinearMap L) := by
  unfold spectralInvariantRate
  rw [trace_power_variation tr v L n hn, ← mul_assoc,
    inv_mul_cancel₀ (Nat.cast_ne_zero.mpr (Nat.ne_of_gt hn)), one_mul]

/-- G and B are fixed by real-linearity; differentiating the resolvent gives
the precise variation of the normalized L operator. -/
theorem normalizedL_variation (v : AlgebraEvolution A) (M : A)
    (G B : ℝ) (u : Aˣ) (hu : (u : A) = M - 1) :
    v.toLinearMap (normalizedL G B u) =
      G • ((↑u⁻¹ : A) * v.toLinearMap M * (↑u⁻¹ : A)) := by
  unfold normalizedL
  rw [map_add, map_smul, map_smul, evolution_map_one,
    smul_zero, add_zero, unit_inverse_evolution, hu, map_sub,
    evolution_map_one, sub_zero]
  simp only [neg_mul, neg_smul, smul_neg, neg_neg]

/-- The rationalGradient definition is now proved to represent spectral
variation through the trace pairing, for every positive order. -/
theorem rationalGradient_represents_spectral_variation (tr : CyclicTrace A)
    (v : AlgebraEvolution A) (M : A) (G B : ℝ) (u : Aˣ)
    (hu : (u : A) = M - 1) (n : ℕ) (hn : 0 < n) :
    spectralInvariantRate tr v (normalizedL G B u) n =
      tr.toLinearMap (rationalGradient G B u n * v.toLinearMap M) := by
  rw [spectralInvariantRate_variation tr v (normalizedL G B u) n hn,
    normalizedL_variation v M G B u hu]
  simp only [rationalGradient, Algebra.mul_smul_comm, Algebra.smul_mul_assoc,
    map_smul, smul_eq_mul]
  congr 1
  calc
    tr.toLinearMap (normalizedL G B u ^ (n - 1) *
        ((↑u⁻¹ : A) * v.toLinearMap M * (↑u⁻¹ : A))) =
      tr.toLinearMap ((normalizedL G B u ^ (n - 1) *
        (↑u⁻¹ : A) * v.toLinearMap M) * (↑u⁻¹ : A)) := by
        simp only [mul_assoc]
    _ = tr.toLinearMap ((↑u⁻¹ : A) *
        (normalizedL G B u ^ (n - 1) * (↑u⁻¹ : A) * v.toLinearMap M)) :=
      tr.cyclic _ _
    _ = tr.toLinearMap (((↑u⁻¹ : A) *
        normalizedL G B u ^ (n - 1) * (↑u⁻¹ : A)) * v.toLinearMap M) := by
      simp only [mul_assoc]

theorem trace_unit_conjugation (tr : CyclicTrace A) (u : Aˣ) (a : A) :
    tr.toLinearMap ((u : A) * a * (↑u⁻¹ : A)) = tr.toLinearMap a := by
  rw [tr.cyclic ((u : A) * a) (↑u⁻¹ : A), ← mul_assoc,
    Units.inv_mul, one_mul]

theorem unit_conjugation_pow (u : Aˣ) (a : A) (n : ℕ) :
    ((u : A) * a * (↑u⁻¹ : A)) ^ n =
      (u : A) * a ^ n * (↑u⁻¹ : A) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [pow_succ, ih, pow_succ]
    simp only [mul_assoc, Units.inv_mul_cancel_left]

theorem spectralInvariant_unit_conjugation (tr : CyclicTrace A)
    (u : Aˣ) (L : A) (n : ℕ) :
    spectralInvariant tr ((u : A) * L * (↑u⁻¹ : A)) n =
      spectralInvariant tr L n := by
  simp only [spectralInvariant, unit_conjugation_pow, trace_unit_conjugation]

#print axioms trace_power_variation
#print axioms normalizedL_variation
#print axioms rationalGradient_represents_spectral_variation
#print axioms spectralInvariant_unit_conjugation

end

end DLWLean
