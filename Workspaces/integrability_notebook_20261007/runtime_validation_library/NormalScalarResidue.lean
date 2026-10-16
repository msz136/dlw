import NormalModelResidue
import CommonGauge

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem normalProductCoefficient_scalar_right {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (order : ℤ) (a : ℕ → R) (b : R) (k : ℕ) :
    normalProductCoefficient d order a (fun s => if s = 0 then b else 0) k =
      ∑ r : Fin (k + 1), algebraMap ℝ R ((Ring.choose (order - (r.val : ℤ))
        (k - r.val) : ℤ) : ℝ) * a r.val * (d.toLinearMap)^[k - r.val] b := by
  classical
  unfold normalProductCoefficient
  apply Finset.sum_congr rfl
  intro r _
  rw [Finset.sum_eq_single (0 : Fin (k + 1))]
  · simp [Nat.le_of_lt_succ r.isLt]
  · intro s _ hs
    have hs0 : s.val ≠ 0 := by intro h; apply hs; exact Fin.ext h
    simp only [hs0, ite_false, evolutionIterate_zero, mul_zero]
    split_ifs <;> rfl
  · simp

theorem normalProductCoefficient_scalar_right_residue {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (N : ℕ) (a : ℕ → R) (b : R) :
    normalProductCoefficient d (N : ℤ) a (fun s => if s = 0 then b else 0) (N + 1) =
      a (N + 1) * b := by
  classical
  rw [normalProductCoefficient_scalar_right, Finset.sum_eq_single (Fin.last (N + 1))]
  · simp
  · intro r _ hr
    have hrN : r.val ≤ N := by
      have hne : r.val ≠ N + 1 := by intro h; apply hr; exact Fin.ext h
      have hlt := r.isLt
      omega
    have he : (N : ℤ) - (r.val : ℤ) = ((N - r.val : ℕ) : ℤ) := by omega
    have hc : Ring.choose ((N : ℤ) - (r.val : ℤ)) (N + 1 - r.val) = 0 := by
      rw [he, Ring.choose_natCast, Nat.choose_eq_zero_of_lt (by omega)]
      simp
    simp only [hc, Int.cast_zero, map_zero, zero_mul]
  · simp

namespace NormalPDOModel
variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

/-- Scalar right multiplication preserves the residue pointwise. The
vanishing binomial coefficients eliminate every nonnegative D power,
including for a scalar coefficient with a nonperiodic primitive. -/
theorem scalar_right_residue (X : A) (b : R) :
    model.coefficients (X * model.coefficient b) (-1) =
      model.coefficients X (-1) * b := by
  obtain ⟨order, hX⟩ := model.bounded_above X
  let N : ℕ := (max order 0).toNat
  have hN : (N : ℤ) = max order 0 := Int.toNat_of_nonneg (le_max_right _ _)
  have hb : PDOOrderBound model.coefficients X (N : ℤ) :=
    model.bound_mono hX (by rw [hN]; exact le_max_left _ _)
  have hp := model.product_coefficient X (model.coefficient b) (N : ℤ) 0
    hb (model.embedding_bound b) (N + 1)
  have hexp : (N : ℤ) + 0 - ((N + 1 : ℕ) : ℤ) = -1 := by omega
  have hs : (fun s : ℕ => model.coefficients (model.coefficient b) (0 - (s : ℤ))) =
      (fun s => if s = 0 then b else 0) := by
    funext s
    simp [model.coefficient_embedding]
  rw [hexp, hs, normalProductCoefficient_scalar_right_residue] at hp
  have hexp' : (N : ℤ) - ((N + 1 : ℕ) : ℤ) = -1 := by omega
  simpa only [hexp'] using hp

theorem scalar_commutator_residue_zero (b : R) (X : A) :
    model.coefficients (model.coefficient b * X - X * model.coefficient b) (-1) = 0 := by
  simp only [map_sub, Pi.sub_apply, model.scalar_left_coefficient,
    model.scalar_right_residue, mul_comm b, sub_self]

end NormalPDOModel

#print axioms NormalPDOModel.scalar_right_residue
#print axioms NormalPDOModel.scalar_commutator_residue_zero
end
end DLWLean
