import BalancedRealization

namespace DLWLean
noncomputable section
open scoped BigOperators

def normalInverseRemainder {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (H V : ℕ → R) (n : ℕ) : R :=
  ∑ t : Fin (n + 1), ∑ r : Fin (n + 2),
    if r.val + t.val ≤ n + 1 then
      algebraMap ℝ R ((Ring.choose (-1 - (r.val : ℤ))
        (n + 1 - (r.val + t.val)) : ℤ) : ℝ) * H r.val *
          (d.toLinearMap)^[n + 1 - (r.val + t.val)] (V t.val)
    else 0

/-- The only new inverse coefficient occurs at t=n+1,r=0. Every
remaining term uses a strictly earlier inverse coefficient. -/
theorem normalProductCoefficient_isolate_inverse {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (H V : ℕ → R) (n : ℕ) :
    normalProductCoefficient d (-1) H V (n + 1) =
      H 0 * V (n + 1) + normalInverseRemainder d H V n := by
  classical
  unfold normalProductCoefficient
  rw [Finset.sum_comm, Fin.sum_univ_castSucc]
  have hlast : (∑ r : Fin (n + 2),
      if r.val + (Fin.last (n + 1)).val ≤ n + 1 then
        algebraMap ℝ R ((Ring.choose (-1 - (r.val : ℤ))
          (n + 1 - (r.val + (Fin.last (n + 1)).val)) : ℤ) : ℝ) * H r.val *
          (d.toLinearMap)^[n + 1 - (r.val + (Fin.last (n + 1)).val)]
            (V (Fin.last (n + 1)).val)
      else 0) = H 0 * V (n + 1) := by
    rw [Finset.sum_eq_single (⟨0, by omega⟩ : Fin (n + 2))]
    · simp
    · intro r _ hr
      have hr0 : r.val ≠ 0 := by
        intro heq
        apply hr
        exact Fin.ext heq
      have hn : ¬r.val + (Fin.last (n + 1)).val ≤ n + 1 := by
        simp only [Fin.val_last]
        omega
      exact if_neg hn
    · simp
  rw [hlast, add_comm]
  rfl

namespace NormalPDOModel
variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

theorem constantLeading_inverse_bound (u : Aˣ) (h0 : ℝ) (h0ne : h0 ≠ 0)
    (hu : PDOOrderBound model.coefficients (u : A) (-1))
    (hlead : model.coefficients (u : A) (-1) = algebraMap ℝ R h0) :
    PDOOrderBound model.coefficients (↑u⁻¹ : A) 1 := by
  have hunit : IsUnit (model.coefficients (u : A) (-1)) := by
    rw [hlead]
    exact (isUnit_iff_ne_zero.mpr h0ne).map (algebraMap ℝ R)
  simpa using model.inverse_bound u (-1) hu hunit

theorem constantLeading_inverse_zero (u : Aˣ) (h0 : ℝ) (h0ne : h0 ≠ 0)
    (hu : PDOOrderBound model.coefficients (u : A) (-1))
    (hlead : model.coefficients (u : A) (-1) = algebraMap ℝ R h0) :
    model.coefficientBelow (↑u⁻¹ : A) 1 0 = algebraMap ℝ R h0⁻¹ := by
  have h := model.product_leading (u : A) (↑u⁻¹ : A) (-1) 1 hu
    (model.constantLeading_inverse_bound u h0 h0ne hu hlead)
  rw [Units.mul_inv, model.coeff_one, hlead] at h
  simp only [neg_add_cancel, ite_true] at h
  have hi : algebraMap ℝ R h0⁻¹ * algebraMap ℝ R h0 = 1 := by
    rw [← map_mul, inv_mul_cancel₀ h0ne, map_one]
  have h' := congrArg (fun y : R => algebraMap ℝ R h0⁻¹ * y) h
  simpa [NormalPDOModel.coefficientBelow, ← mul_assoc, hi] using h'.symm

theorem constantLeading_inverse_succ (u : Aˣ) (h0 : ℝ) (h0ne : h0 ≠ 0)
    (hu : PDOOrderBound model.coefficients (u : A) (-1))
    (hlead : model.coefficients (u : A) (-1) = algebraMap ℝ R h0) (n : ℕ) :
    model.coefficientBelow (↑u⁻¹ : A) 1 (n + 1) =
      algebraMap ℝ R (-h0⁻¹) * normalInverseRemainder model.d
        (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow (↑u⁻¹ : A) 1) n := by
  have h := model.product_coefficient (u : A) (↑u⁻¹ : A) (-1) 1 hu
    (model.constantLeading_inverse_bound u h0 h0ne hu hlead) (n + 1)
  rw [Units.mul_inv, model.coeff_one, normalProductCoefficient_isolate_inverse] at h
  have hn : (-1 : ℤ) + 1 - ((n + 1 : ℕ) : ℤ) ≠ 0 := by omega
  simp only [hn, ite_false, Nat.cast_zero, sub_zero, hlead] at h
  change 0 = algebraMap ℝ R h0 * model.coefficientBelow (↑u⁻¹ : A) 1 (n + 1) +
    normalInverseRemainder model.d
      (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow (↑u⁻¹ : A) 1) n at h
  have hsolve : algebraMap ℝ R h0 * model.coefficientBelow (↑u⁻¹ : A) 1 (n + 1) =
      -normalInverseRemainder model.d
        (model.coefficientBelow (u : A) (-1)) (model.coefficientBelow (↑u⁻¹ : A) 1) n := by
    exact eq_neg_iff_add_eq_zero.mpr h.symm
  have hi : algebraMap ℝ R h0⁻¹ * algebraMap ℝ R h0 = 1 := by
    rw [← map_mul, inv_mul_cancel₀ h0ne, map_one]
  calc
    model.coefficientBelow (↑u⁻¹ : A) 1 (n + 1) =
        algebraMap ℝ R h0⁻¹ * (algebraMap ℝ R h0 *
          model.coefficientBelow (↑u⁻¹ : A) 1 (n + 1)) := by rw [← mul_assoc, hi, one_mul]
    _ = _ := by rw [hsolve, mul_neg, map_neg, neg_mul]

end NormalPDOModel

#print axioms normalProductCoefficient_isolate_inverse
#print axioms NormalPDOModel.constantLeading_inverse_succ
end
end DLWLean
