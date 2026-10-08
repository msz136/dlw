import BalancedCoefficientRecurrence
import NormalResidueBridge
import EtaLimit

/-!
A single normal-form PDO model specification and its coefficient
realization consequences. Model fields express the defining coefficient
rules; correspondence with the constructed balanced recurrences is
proved from those rules, rather than supplied as a target hypothesis.
-/

namespace DLWLean
noncomputable section
open scoped BigOperators

def normalProductCoefficient {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (leftOrder : ℤ) (a b : ℕ → R) (k : ℕ) : R :=
  ∑ r : Fin (k + 1), ∑ s : Fin (k + 1),
    if r.val + s.val ≤ k then
      algebraMap ℝ R (((Ring.choose (leftOrder - (r.val : ℤ))
        (k - (r.val + s.val)) : ℤ) : ℝ)) * a r.val *
          (d.toLinearMap)^[k - (r.val + s.val)] (b s.val)
    else 0

theorem evolutionIterate_zero {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (k : ℕ) : (d.toLinearMap)^[k] (0 : R) = 0 := by
  induction k with
  | zero => rfl
  | succ k ih => simp only [Function.iterate_succ_apply', ih, map_zero]

theorem ringChoose_zero (k : ℕ) : Ring.choose (0 : ℤ) k = if k = 0 then 1 else 0 := by
  cases k with
  | zero => simp
  | succ k =>
    change Ring.choose ((0 : ℕ) : ℤ) (k + 1) = _
    rw [Ring.choose_natCast, Nat.choose_eq_zero_of_lt (Nat.succ_pos k)]
    simp

theorem normalProductCoefficient_delta_left {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (leftOrder : ℤ) (a : R) (b : ℕ → R) (k : ℕ) :
    normalProductCoefficient d leftOrder (fun r => if r = 0 then a else 0) b k =
      ∑ s : Fin (k + 1),
        algebraMap ℝ R ((Ring.choose leftOrder (k - s.val) : ℤ) : ℝ) * a *
          (d.toLinearMap)^[k - s.val] (b s.val) := by
  classical
  unfold normalProductCoefficient
  rw [Finset.sum_eq_single (0 : Fin (k + 1))]
  · apply Finset.sum_congr rfl
    intro s _
    simp [Nat.le_of_lt_succ s.isLt]
  · intro r _ hr
    have hrv : r.val ≠ 0 := by intro h; apply hr; exact Fin.ext h
    apply Finset.sum_eq_zero
    intro s _
    split_ifs <;> simp [hrv]
  · simp

theorem normalProductCoefficient_scalar_left {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (a : R) (b : ℕ → R) (k : ℕ) :
    normalProductCoefficient d 0 (fun r => if r = 0 then a else 0) b k = a * b k := by
  classical
  rw [normalProductCoefficient_delta_left]
  rw [Finset.sum_eq_single (Fin.last k)]
  · simp [Function.iterate_zero_apply]
  · intro s _ hs
    have hsv : s.val ≠ k := by intro h; apply hs; exact Fin.ext (by simpa using h)
    have hsub : k - s.val ≠ 0 := by have := s.isLt; omega
    simp [ringChoose_zero, hsub]
  · simp

theorem normalProductCoefficient_add_left {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (order : ℤ) (a₁ a₂ b : ℕ → R) (k : ℕ) :
    normalProductCoefficient d order (fun r => a₁ r + a₂ r) b k =
      normalProductCoefficient d order a₁ b k + normalProductCoefficient d order a₂ b k := by
  classical
  unfold normalProductCoefficient
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s _
  split_ifs <;> ring

theorem normalProductCoefficient_first_order_delta {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (b : ℕ → R) (n : ℕ) :
    normalProductCoefficient d 1 (fun r => if r = 0 then 1 else 0) b (n + 1) =
      b (n + 1) + d.toLinearMap (b n) := by
  classical
  rw [normalProductCoefficient_delta_left]
  let last : Fin (n + 2) := ⟨n + 1, by omega⟩
  let prev : Fin (n + 2) := ⟨n, by omega⟩
  let term := fun s : Fin (n + 2) =>
    algebraMap ℝ R ((Ring.choose (1 : ℤ) (n + 1 - s.val) : ℤ) : ℝ) * (1 : R) *
      (d.toLinearMap)^[n + 1 - s.val] (b s.val)
  change (∑ s, term s) = _
  have hne : last ≠ prev := by intro h; have := congrArg Fin.val h; dsimp [last, prev] at this; omega
  have hs : (∑ s, term s) = ∑ s ∈ ({last, prev} : Finset (Fin (n + 2))), term s := by
    symm
    apply Finset.sum_subset (by simp)
    intro s _ hnot
    have hsl : s.val ≠ n + 1 := by
      intro h
      have hEq : s = last := Fin.ext h
      simp [hEq] at hnot
    have hsp : s.val ≠ n := by
      intro h
      have hEq : s = prev := Fin.ext h
      simp [hEq] at hnot
    have hsub : 1 < n + 1 - s.val := by have := s.isLt; omega
    unfold term
    have hchoose : Ring.choose (1 : ℤ) (n + 1 - s.val) = 0 := by
      change Ring.choose ((1 : ℕ) : ℤ) (n + 1 - s.val) = 0
      rw [Ring.choose_natCast, Nat.choose_eq_zero_of_lt hsub]
      simp
    rw [hchoose]
    simp
  rw [hs]
  simp [hne, term, last, prev, Ring.choose_one_right,
    Function.iterate_zero_apply, Function.iterate_one]

theorem normalProductCoefficient_first_order_shift {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (a : R) (b : ℕ → R) (n : ℕ) :
    normalProductCoefficient d 1 (fun r => if r = 1 then a else 0) b (n + 1) = a * b n := by
  classical
  let oneIndex : Fin (n + 2) := ⟨1, by omega⟩
  let targetIndex : Fin (n + 2) := ⟨n, by omega⟩
  unfold normalProductCoefficient
  rw [Finset.sum_eq_single oneIndex]
  · rw [Finset.sum_eq_single targetIndex]
    · simp [oneIndex, targetIndex, Function.iterate_zero_apply, Nat.add_comm]
    · intro s _ hs
      have hsv : s.val ≠ n := by intro h; apply hs; exact Fin.ext h
      simp only [oneIndex, Fin.val_mk, Nat.cast_one, sub_self]
      split_ifs with hle
      · have hsub : n + 1 - (1 + s.val) ≠ 0 := by omega
        simp [ringChoose_zero, hsub]
      · rfl
    · simp
  · intro r _ hr
    have hrv : r.val ≠ 1 := by intro h; apply hr; exact Fin.ext h
    apply Finset.sum_eq_zero
    intro s _
    split_ifs <;> simp [hrv]
  · simp

theorem normalProductCoefficient_first_order {R : Type*} [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) (beta : R) (b : ℕ → R) (n : ℕ) :
    normalProductCoefficient d 1
      (fun r => if r = 0 then 1 else if r = 1 then -beta else 0) b (n + 1) =
        b (n + 1) + d.toLinearMap (b n) - beta * b n := by
  have hseq : (fun r : ℕ => if r = 0 then (1 : R) else if r = 1 then -beta else 0) =
      (fun r => (if r = 0 then 1 else 0) + (if r = 1 then -beta else 0)) := by
    funext r
    split_ifs <;> simp_all
  rw [hseq, normalProductCoefficient_add_left, normalProductCoefficient_first_order_delta,
    normalProductCoefficient_first_order_shift]
  ring

def PDOOrderBound {R A : Type*} [CommRing R] [Algebra ℝ R]
    [Ring A] [Algebra ℝ A] (coefficients : A →ₗ[ℝ] (ℤ → R))
    (X : A) (order : ℤ) : Prop :=
  ∀ exponent, order < exponent → coefficients X exponent = 0

/-- A normal-form PDO representation over one coefficient differential
algebra. These fields specify coefficients and their multiplication;
they do not prescribe spectral charges or their Hessians. -/
structure NormalPDOModel (R A : Type*) [CommRing R] [Algebra ℝ R]
    [Ring A] [Algebra ℝ A] where
  d : AlgebraEvolution R
  coefficient : R →ₐ[ℝ] A
  D : Aˣ
  coefficients : A →ₗ[ℝ] (ℤ → R)
  ext_coefficients : ∀ X Y, (∀ exponent, coefficients X exponent = coefficients Y exponent) → X = Y
  bounded_above : ∀ X, ∃ order, PDOOrderBound coefficients X order
  coefficient_embedding : ∀ a exponent,
    coefficients (coefficient a) exponent = if exponent = 0 then a else 0
  coefficient_D_power : ∀ (n : ℤ) exponent,
    coefficients ((↑(D ^ n) : A)) exponent = if exponent = n then 1 else 0
  product_bound : ∀ X Y oX oY,
    PDOOrderBound coefficients X oX → PDOOrderBound coefficients Y oY →
      PDOOrderBound coefficients (X * Y) (oX + oY)
  product_coefficient : ∀ X Y oX oY,
    PDOOrderBound coefficients X oX → PDOOrderBound coefficients Y oY → ∀ k : ℕ,
      coefficients (X * Y) (oX + oY - (k : ℤ)) =
        normalProductCoefficient d oX
          (fun r => coefficients X (oX - (r : ℤ)))
          (fun s => coefficients Y (oY - (s : ℤ))) k
  inverse_bound : ∀ (u : Aˣ) order,
    PDOOrderBound coefficients (u : A) order → IsUnit (coefficients (u : A) order) →
      PDOOrderBound coefficients (↑u⁻¹ : A) (-order)

namespace BalancedPDO

structure DifferentialEvaluation (M : ℕ) (R : Type*) [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) where
  evaluation : Poly M →ₐ[ℝ] R
  derivative_compatible : ∀ p, evaluation (spatialDerivative M p) = d.toLinearMap (evaluation p)

namespace DifferentialEvaluation

variable {M : ℕ} {R : Type*} [CommRing R] [Algebra ℝ R]
    {d : AlgebraEvolution R} (e : DifferentialEvaluation M R d)

theorem C_eval (r : ℝ) : e.evaluation (MvPolynomial.C r) = algebraMap ℝ R r :=
  e.evaluation.commutes r

theorem spatialIterate_eval (k : ℕ) (p : Poly M) :
    e.evaluation (spatialIterate M k p) = (d.toLinearMap)^[k] (e.evaluation p) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [spatialIterate, Function.iterate_succ_apply', e.derivative_compatible]
    rw [← spatialIterate, ih]

theorem normalProduct_eval (leftOrder : ℤ) (a b : ℕ → Poly M) (k : ℕ) :
    e.evaluation (normalProduct M leftOrder a b k) =
      normalProductCoefficient d leftOrder
        (fun r => e.evaluation (a r)) (fun s => e.evaluation (b s)) k := by
  classical
  unfold normalProduct normalProductCoefficient
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro r _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro s _
  split_ifs
  · rw [map_mul, map_mul, e.C_eval, e.spatialIterate_eval]
  · rw [map_zero]

end DifferentialEvaluation
end BalancedPDO

namespace NormalPDOModel

variable {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]
    (model : NormalPDOModel R A)

def coefficientBelow (X : A) (order : ℤ) (k : ℕ) : R :=
  model.coefficients X (order - (k : ℤ))

theorem embedding_bound (a : R) : PDOOrderBound model.coefficients (model.coefficient a) 0 := by
  intro exponent he
  rw [model.coefficient_embedding]
  simp [ne_of_gt he]

theorem D_power_bound (n : ℤ) :
    PDOOrderBound model.coefficients (↑(model.D ^ n) : A) n := by
  intro exponent he
  rw [model.coefficient_D_power]
  simp [ne_of_gt he]

theorem coeff_one (exponent : ℤ) :
    model.coefficients (1 : A) exponent = if exponent = 0 then 1 else 0 := by
  simpa only [map_one] using model.coefficient_embedding (1 : R) exponent

theorem add_bound {X Y : A} {order : ℤ}
    (hX : PDOOrderBound model.coefficients X order)
    (hY : PDOOrderBound model.coefficients Y order) :
    PDOOrderBound model.coefficients (X + Y) order := by
  intro exponent he
  simp only [map_add, Pi.add_apply, hX exponent he, hY exponent he, add_zero]

theorem sub_bound {X Y : A} {order : ℤ}
    (hX : PDOOrderBound model.coefficients X order)
    (hY : PDOOrderBound model.coefficients Y order) :
    PDOOrderBound model.coefficients (X - Y) order := by
  intro exponent he
  simp only [map_sub, Pi.sub_apply, hX exponent he, hY exponent he, sub_self]

theorem smul_bound (c : ℝ) {X : A} {order : ℤ}
    (hX : PDOOrderBound model.coefficients X order) :
    PDOOrderBound model.coefficients (c • X) order := by
  intro exponent he
  simp only [map_smul, Pi.smul_apply, hX exponent he, smul_zero]

theorem bound_mono {X : A} {o₁ o₂ : ℤ}
    (hX : PDOOrderBound model.coefficients X o₁) (ho : o₁ ≤ o₂) :
    PDOOrderBound model.coefficients X o₂ := by
  intro exponent he
  exact hX exponent (lt_of_le_of_lt ho he)

/-- Left multiplication by any smooth scalar coefficient preserves each
normal coefficient pointwise. No cyclic trace or periodic primitive is
used. In a smooth coefficient extension this applies also to a
nonperiodic scalar gauge primitive. -/
theorem scalar_left_coefficient (a : R) (X : A) (exponent : ℤ) :
    model.coefficients (model.coefficient a * X) exponent =
      a * model.coefficients X exponent := by
  obtain ⟨order, hX⟩ := model.bounded_above X
  by_cases he : order < exponent
  · have hprod := model.product_bound (model.coefficient a) X 0 order
      (model.embedding_bound a) hX
    simpa only [zero_add, hX exponent he, mul_zero] using hprod exponent (by simpa using he)
  · have hle : exponent ≤ order := le_of_not_gt he
    let k := (order - exponent).toNat
    have hk : (k : ℤ) = order - exponent := Int.toNat_of_nonneg (sub_nonneg.mpr hle)
    have hexp : exponent = 0 + order - (k : ℤ) := by omega
    rw [hexp, model.product_coefficient _ _ 0 order (model.embedding_bound a) hX k]
    have ha : (fun r : ℕ => model.coefficients (model.coefficient a) (0 - (r : ℤ))) =
        (fun r => if r = 0 then a else 0) := by
      funext r
      rw [model.coefficient_embedding]
      simp
    rw [ha, normalProductCoefficient_scalar_left]
    simp

theorem product_leading (X Y : A) (oX oY : ℤ)
    (hX : PDOOrderBound model.coefficients X oX)
    (hY : PDOOrderBound model.coefficients Y oY) :
    model.coefficients (X * Y) (oX + oY) =
      model.coefficients X oX * model.coefficients Y oY := by
  have h := model.product_coefficient X Y oX oY hX hY 0
  simpa [normalProductCoefficient] using h

end NormalPDOModel

namespace BalancedPDO

variable {M : ℕ} {R A : Type*} [CommRing R] [Algebra ℝ R] [Ring A] [Algebra ℝ A]

/-- The actual affine first-order factors. Formal inverse existence is
given by units; inverse coefficient formulas are conclusions below. -/
structure FactorRealization (model : NormalPDOModel R A)
    (e : DifferentialEvaluation M R model.d) where
  denominator : Fin M → Aˣ
  denominator_eq : ∀ j, (denominator j : A) = (model.D : A) -
    model.coefficient (e.evaluation (balancedBeta M j))

namespace FactorRealization

variable {model : NormalPDOModel R A} {e : DifferentialEvaluation M R model.d}
    (factors : FactorRealization model e)

theorem denominator_bound (j : Fin M) :
    PDOOrderBound model.coefficients (factors.denominator j : A) 1 := by
  rw [factors.denominator_eq]
  apply model.sub_bound
  · simpa using model.D_power_bound 1
  · exact model.bound_mono (model.embedding_bound _) (by norm_num)

theorem denominator_coefficient (j : Fin M) (k : ℕ) :
    model.coefficientBelow (factors.denominator j : A) 1 k =
      if k = 0 then 1 else if k = 1 then -e.evaluation (balancedBeta M j) else 0 := by
  unfold NormalPDOModel.coefficientBelow
  rw [factors.denominator_eq, map_sub]
  simp only [Pi.sub_apply]
  have hD : model.coefficients (model.D : A) (1 - (k : ℤ)) =
      if 1 - (k : ℤ) = 1 then 1 else 0 := by
    simpa using model.coefficient_D_power 1 (1 - (k : ℤ))
  rw [hD, model.coefficient_embedding]
  have hk0 : 1 - (k : ℤ) = 1 ↔ k = 0 := by omega
  have hk1 : 1 - (k : ℤ) = 0 ↔ k = 1 := by omega
  simp only [hk0, hk1]
  split_ifs <;> simp_all

theorem inverse_bound (j : Fin M) :
    PDOOrderBound model.coefficients (↑(factors.denominator j)⁻¹ : A) (-1) := by
  apply model.inverse_bound (factors.denominator j) 1 (factors.denominator_bound j)
  have h := factors.denominator_coefficient j 0
  simp only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero, if_pos rfl] at h
  rw [h]
  exact isUnit_one

def inverseBelow (j : Fin M) (k : ℕ) : R :=
  model.coefficientBelow (↑(factors.denominator j)⁻¹ : A) (-1) k

theorem inverseBelow_zero (j : Fin M) : factors.inverseBelow j 0 = 1 := by
  have h := model.product_leading (factors.denominator j : A)
    (↑(factors.denominator j)⁻¹ : A) 1 (-1)
    (factors.denominator_bound j) (factors.inverse_bound j)
  rw [Units.mul_inv, model.coeff_one] at h
  have hlead := factors.denominator_coefficient j 0
  simp only [NormalPDOModel.coefficientBelow, Nat.cast_zero, sub_zero, if_pos rfl] at hlead
  rw [hlead] at h
  simpa [inverseBelow, NormalPDOModel.coefficientBelow] using h.symm

theorem inverseBelow_succ (j : Fin M) (n : ℕ) :
    factors.inverseBelow j (n + 1) =
      e.evaluation (balancedBeta M j) * factors.inverseBelow j n -
        model.d.toLinearMap (factors.inverseBelow j n) := by
  have h := model.product_coefficient (factors.denominator j : A)
    (↑(factors.denominator j)⁻¹ : A) 1 (-1)
    (factors.denominator_bound j) (factors.inverse_bound j) (n + 1)
  rw [Units.mul_inv, model.coeff_one] at h
  have hseq : (fun r : ℕ => model.coefficients (factors.denominator j : A) (1 - (r : ℤ))) =
      (fun r => if r = 0 then 1 else if r = 1 then -e.evaluation (balancedBeta M j) else 0) := by
    funext r
    exact factors.denominator_coefficient j r
  rw [hseq, normalProductCoefficient_first_order] at h
  have hnonzero : 1 + (-1 : ℤ) - ((n + 1 : ℕ) : ℤ) ≠ 0 := by omega
  simp only [hnonzero, if_false] at h
  change 0 = factors.inverseBelow j (n + 1) +
    model.d.toLinearMap (factors.inverseBelow j n) -
      e.evaluation (balancedBeta M j) * factors.inverseBelow j n at h
  linear_combination -h

/-- Actual inverse coefficients coincide with the independently
constructed polynomial recurrence, by its proved uniqueness. -/
theorem inverse_coefficient_realization (j : Fin M) (k : ℕ) :
    factors.inverseBelow j k = e.evaluation (resolventCoefficient M j k) := by
  induction k with
  | zero => simpa [resolventCoefficient] using factors.inverseBelow_zero j
  | succ k ih =>
    rw [factors.inverseBelow_succ, resolventCoefficient, map_sub, map_mul,
      e.derivative_compatible, ih]

end FactorRealization
end BalancedPDO

#print axioms BalancedPDO.DifferentialEvaluation.normalProduct_eval
#print axioms NormalPDOModel.scalar_left_coefficient
#print axioms BalancedPDO.FactorRealization.inverse_coefficient_realization
end
end DLWLean
