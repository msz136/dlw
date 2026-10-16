import BalancedRealization

namespace DLWLean
noncomputable section
open scoped BigOperators

theorem normalProductCoefficient_delta_both {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (leftOrder : ℤ) (a b : R) (k : ℕ) :
    normalProductCoefficient d leftOrder
      (fun r => if r = 0 then a else 0) (fun r => if r = 0 then b else 0) k =
      algebraMap ℝ R ((Ring.choose leftOrder k : ℤ) : ℝ) * a * (d.toLinearMap)^[k] b := by
  classical
  rw [normalProductCoefficient_delta_left]
  rw [Finset.sum_eq_single (0 : Fin (k + 1))]
  · simp
  · intro s _ hs
    have hsv : s.val ≠ 0 := by intro h; apply hs; exact Fin.ext h
    simp only [hsv, ite_false, evolutionIterate_zero, mul_zero]
  · simp

namespace NormalPDOModel
variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

theorem D_coefficient_commutation (a : R) :
    (model.D : A) * model.coefficient a =
      model.coefficient a * (model.D : A) + model.coefficient (model.d.toLinearMap a) := by
  apply model.ext_coefficients
  intro exponent
  have hD : PDOOrderBound model.coefficients (model.D : A) 1 := by
    simpa using model.D_power_bound 1
  have hprod := model.product_bound (model.D : A) (model.coefficient a) 1 0 hD (model.embedding_bound a)
  by_cases he : 1 < exponent
  · have hright := model.product_bound (model.coefficient a) (model.D : A) 0 1
      (model.embedding_bound a) hD
    have h0 : exponent ≠ 0 := by omega
    simp only [map_add, Pi.add_apply, hprod exponent (by simpa using he),
      hright exponent (by simpa using he), model.coefficient_embedding,
      h0, ite_false, zero_add]
  · let k := (1 - exponent).toNat
    have hk : (k : ℤ) = 1 - exponent := Int.toNat_of_nonneg (by omega)
    have hexp : exponent = 1 + 0 - (k : ℤ) := by omega
    rw [hexp, model.product_coefficient _ _ 1 0 hD (model.embedding_bound a) k]
    have hleft : (fun r : ℕ => model.coefficients (model.D : A) (1 - (r : ℤ))) =
        (fun r => if r = 0 then 1 else 0) := by
      funext r
      have h := model.coefficient_D_power 1 (1 - (r : ℤ))
      simpa using h
    have hright : (fun r : ℕ => model.coefficients (model.coefficient a) (0 - (r : ℤ))) =
        (fun r => if r = 0 then a else 0) := by
      funext r
      rw [model.coefficient_embedding]
      simp
    rw [hleft, hright, normalProductCoefficient_delta_both,
      map_add, Pi.add_apply, model.scalar_left_coefficient, model.coefficient_embedding]
    have hDc := model.coefficient_D_power 1 (1 + 0 - (k : ℤ))
    simp only [zpow_one, Units.val_one] at hDc
    rw [hDc]
    cases k with
    | zero => simp
    | succ k =>
      cases k with
      | zero => simp [Function.iterate_one]
      | succ k =>
        have hc : Ring.choose (1 : ℤ) (k + 1 + 1) = 0 := by
          rw [← Int.natCast_one, Ring.choose_natCast,
            Nat.choose_eq_zero_of_lt (by omega : 1 < k + 1 + 1)]
          simp
        simp only [hc, map_zero, zero_mul]
        split_ifs <;> (first | omega | simp)

theorem differential_residue_zero (n : ℕ) (a : R) :
    model.coefficients ((model.D : A) ^ n * model.coefficient a) (-1) = 0 := by
  have hDn : PDOOrderBound model.coefficients ((model.D : A) ^ n) (n : ℤ) := by
    simpa using model.D_power_bound (n : ℤ)
  have hp := model.product_coefficient ((model.D : A) ^ n) (model.coefficient a)
    (n : ℤ) 0 hDn (model.embedding_bound a) (n + 1)
  have hexp : (n : ℤ) + 0 - ((n + 1 : ℕ) : ℤ) = -1 := by omega
  rw [hexp] at hp
  have hleft : (fun r : ℕ => model.coefficients ((model.D : A) ^ n) ((n : ℤ) - (r : ℤ))) =
      (fun r => if r = 0 then 1 else 0) := by
    funext r
    have h := model.coefficient_D_power (n : ℤ) ((n : ℤ) - (r : ℤ))
    simpa using h
  have hright : (fun r : ℕ => model.coefficients (model.coefficient a) (0 - (r : ℤ))) =
      (fun r => if r = 0 then a else 0) := by
    funext r
    rw [model.coefficient_embedding]
    simp
  rw [hp, hleft, hright, normalProductCoefficient_delta_both, Ring.choose_natCast,
    Nat.choose_eq_zero_of_lt (by omega : n < n + 1)]
  simp

theorem inverse_D_residue (a : R) :
    model.coefficients ((↑model.D⁻¹ : A) * model.coefficient a) (-1) = a := by
  have hDi : PDOOrderBound model.coefficients (↑model.D⁻¹ : A) (-1) := by
    simpa using model.D_power_bound (-1)
  have hp := model.product_leading (↑model.D⁻¹ : A) (model.coefficient a) (-1) 0 hDi
    (model.embedding_bound a)
  have hc := model.coefficient_D_power (-1) (-1)
  simp only [zpow_neg_one] at hc
  rw [hc, model.coefficient_embedding] at hp
  simpa using hp

def periodicResidueModel {Lx : ℝ}
    (model : NormalPDOModel (PeriodicCoefficient Lx) A)
    (spatial : model.d = periodicSpatialEvolution Lx) : PeriodicNormalResidueModel A Lx where
  coefficient := model.coefficient
  D := model.D
  residue := (LinearMap.proj (-1 : ℤ)).comp model.coefficients
  commutation a := by
    rw [← spatial]
    exact model.D_coefficient_commutation a
  left_coefficient a X := model.scalar_left_coefficient a X (-1)
  differential_zero := model.differential_residue_zero
  inverse_leading := model.inverse_D_residue

end NormalPDOModel

#print axioms NormalPDOModel.D_coefficient_commutation
#print axioms NormalPDOModel.periodicResidueModel
end
end DLWLean
