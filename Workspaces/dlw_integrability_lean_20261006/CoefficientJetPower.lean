import CoefficientJetRealization

/-!
All powers of a literal coefficient two-jet with zero first variation.
The second-power recurrence is realized in the same PDO coefficient model;
cyclicity then telescopes its trace. No power-Hessian formula is an input.
-/
namespace DLWLean.BalancedPDO
noncomputable section

variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A) (e : DifferentialJetEvaluation M R model.d)

def coefficientSecondPower (S : A) : ℕ → A
  | 0 => 0
  | n + 1 => coefficientSecondPower S n * (model.D : A) + (model.D : A) ^ n * S

theorem powerCoefficient_jet_realization (Lcoeff : ℕ → Poly M) (S : A)
    (hL : CoefficientJetRealization model e Lcoeff 1 (model.D : A) 0 S) (n : ℕ) :
    CoefficientJetRealization model e (powerCoefficient M Lcoeff n) (n : ℤ)
      ((model.D : A) ^ n) 0 (coefficientSecondPower model S n) := by
  induction n with
  | zero =>
    constructor
    · simpa only [pow_zero, Nat.cast_zero, map_one] using model.embedding_bound (1 : R)
    · intro exponent _
      simp
    · intro exponent _
      simp [coefficientSecondPower]
    · intro k
      simp only [powerCoefficient, NormalPDOModel.coefficientBelow, pow_zero,
        model.coeff_one, Nat.cast_zero, zero_sub]
      have hk : -(k : ℤ) = 0 ↔ k = 0 := by omega
      simp only [hk]
      split_ifs <;> simp
    · intro k
      simp only [powerCoefficient, NormalPDOModel.coefficientBelow, map_zero,
        Pi.zero_apply]
      split_ifs <;> simp [e.jet.first_one]
    · intro k
      simp only [powerCoefficient, NormalPDOModel.coefficientBelow,
        coefficientSecondPower, map_zero, Pi.zero_apply]
      split_ifs <;> simp [e.jet.second_one]
  | succ n ih =>
    have hm := CoefficientJetRealization.mul ih hL
    simpa only [powerCoefficient, Nat.cast_add, Nat.cast_one, pow_succ,
      zero_mul, mul_zero, add_zero, coefficientSecondPower] using hm

theorem coefficientSecondPower_trace_weighted (tr : CyclicTrace A) (S : A) (n k : ℕ) :
    tr.toLinearMap ((model.D : A) ^ k * coefficientSecondPower model S (n + 1)) =
      ((n + 1 : ℕ) : ℝ) * tr.toLinearMap ((model.D : A) ^ (k + n) * S) := by
  induction n generalizing k with
  | zero => simp [coefficientSecondPower]
  | succ n ih =>
    rw [coefficientSecondPower, mul_add, map_add]
    have hcycle : tr.toLinearMap ((model.D : A) ^ k *
        (coefficientSecondPower model S (n + 1) * (model.D : A))) =
      tr.toLinearMap ((model.D : A) ^ (k + 1) * coefficientSecondPower model S (n + 1)) := by
      calc
        tr.toLinearMap ((model.D : A) ^ k *
            (coefficientSecondPower model S (n + 1) * (model.D : A))) =
          tr.toLinearMap (((model.D : A) ^ k * coefficientSecondPower model S (n + 1)) *
            (model.D : A)) := congrArg tr.toLinearMap (mul_assoc _ _ _).symm
        _ = tr.toLinearMap ((model.D : A) *
            ((model.D : A) ^ k * coefficientSecondPower model S (n + 1))) := tr.cyclic _ _
        _ = tr.toLinearMap (((model.D : A) * (model.D : A) ^ k) *
            coefficientSecondPower model S (n + 1)) :=
          congrArg tr.toLinearMap (mul_assoc _ _ _).symm
        _ = tr.toLinearMap ((model.D : A) ^ (k + 1) * coefficientSecondPower model S (n + 1)) := by
          simp only [pow_succ']
    rw [hcycle, ih (k + 1), ← mul_assoc, ← pow_add]
    have hexp : k + 1 + n = k + (n + 1) := by omega
    rw [hexp]
    push_cast
    ring

theorem coefficientSecondPower_trace (tr : CyclicTrace A) (S : A) (n : ℕ) (hn : 0 < n) :
    tr.toLinearMap (coefficientSecondPower model S n) =
      (n : ℝ) * tr.toLinearMap ((model.D : A) ^ (n - 1) * S) := by
  cases n with
  | zero => simp at hn
  | succ n =>
    simpa only [pow_zero, one_mul, zero_add, Nat.add_sub_cancel] using
      coefficientSecondPower_trace_weighted model tr S n 0

theorem powerCoefficient_residue_second (Lcoeff : ℕ → Poly M) (S : A)
    (hL : CoefficientJetRealization model e Lcoeff 1 (model.D : A) 0 S) (n : ℕ) :
    e.jet.second (powerCoefficient M Lcoeff n (n + 1)) =
      model.coefficients (coefficientSecondPower model S n) (-1) := by
  have h := (powerCoefficient_jet_realization model e Lcoeff S hL n).second (n + 1)
  have hexp : (n : ℤ) - ((n + 1 : ℕ) : ℤ) = -1 := by omega
  simpa only [NormalPDOModel.coefficientBelow, hexp] using h

theorem powerCoefficient_spectral_second_trace (tr : CyclicTrace A)
    (residueTrace : R →ₗ[ℝ] ℝ)
    (htrace : ∀ X : A, tr.toLinearMap X = residueTrace (model.coefficients X (-1)))
    (Lcoeff : ℕ → Poly M) (S : A)
    (hL : CoefficientJetRealization model e Lcoeff 1 (model.D : A) 0 S) (n : ℕ) (hn : 0 < n) :
    (n : ℝ)⁻¹ * residueTrace (e.jet.second (powerCoefficient M Lcoeff n (n + 1))) =
      tr.toLinearMap ((model.D : A) ^ (n - 1) * S) := by
  rw [powerCoefficient_residue_second model e Lcoeff S hL, ← htrace,
    coefficientSecondPower_trace model tr S n hn, ← mul_assoc,
    inv_mul_cancel₀ (Nat.cast_ne_zero.mpr (Nat.ne_of_gt hn)), one_mul]

#print axioms powerCoefficient_jet_realization
#print axioms coefficientSecondPower_trace
#print axioms powerCoefficient_spectral_second_trace
end
end DLWLean.BalancedPDO
