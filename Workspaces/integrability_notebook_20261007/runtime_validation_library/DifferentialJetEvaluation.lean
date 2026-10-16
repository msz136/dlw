import BalancedRealization
import NormalInverseRecurrence

namespace DLWLean
noncomputable section
open scoped BigOperators

namespace AlgebraJet2
variable {A R : Type*} [Ring A] [Algebra ℝ A] [Ring R] [Algebra ℝ R]
    (j : AlgebraJet2 A R)

theorem first_algebraMap (r : ℝ) : j.first (algebraMap ℝ A r) = 0 := by
  rw [Algebra.algebraMap_eq_smul_one, map_smul, j.first_one, smul_zero]

theorem second_algebraMap (r : ℝ) : j.second (algebraMap ℝ A r) = 0 := by
  rw [Algebra.algebraMap_eq_smul_one, map_smul, j.second_one, smul_zero]
end AlgebraJet2

namespace BalancedPDO

def spatialEvolution (M : ℕ) : AlgebraEvolution (Poly M) where
  toLinearMap :=
    { toFun := fun p => spatialDerivative M p
      map_add' := (spatialDerivative M).map_add
      map_smul' := (spatialDerivative M).map_smul }
  leibniz p q := by
    change spatialDerivative M (p * q) = spatialDerivative M p * q + p * spatialDerivative M q
    simpa only [Algebra.smul_def, Algebra.algebraMap_self, RingHom.id_apply,
      smul_eq_mul, add_comm, mul_comm] using (spatialDerivative M).leibniz p q

theorem inverseCoefficient_succ (M : ℕ) (H : ℕ → Poly M) (a0 : ℝ) (n : ℕ) :
    inverseCoefficient M H a0 (n + 1) = MvPolynomial.C (-a0) *
      normalInverseRemainder (spatialEvolution M) H (inverseCoefficient M H a0) n := by
  rw [inverseCoefficient]
  rfl

structure DifferentialJetEvaluation (M : ℕ) (R : Type*) [CommRing R] [Algebra ℝ R]
    (d : AlgebraEvolution R) where
  jet : AlgebraJet2 (Poly M) R
  value_spatial : ∀ p, jet.value (spatialDerivative M p) = d.toLinearMap (jet.value p)
  first_spatial : ∀ p, jet.first (spatialDerivative M p) = d.toLinearMap (jet.first p)
  second_spatial : ∀ p, jet.second (spatialDerivative M p) = d.toLinearMap (jet.second p)

namespace DifferentialJetEvaluation
variable {M : ℕ} {R : Type*} [CommRing R] [Algebra ℝ R]
    {d : AlgebraEvolution R} (e : DifferentialJetEvaluation M R d)

theorem value_C (r : ℝ) : e.jet.value (MvPolynomial.C r) = algebraMap ℝ R r :=
  e.jet.value.commutes r

theorem first_C (r : ℝ) : e.jet.first (MvPolynomial.C r) = 0 :=
  e.jet.first_algebraMap r

theorem second_C (r : ℝ) : e.jet.second (MvPolynomial.C r) = 0 :=
  e.jet.second_algebraMap r

theorem value_iterate (k : ℕ) (p : Poly M) :
    e.jet.value (spatialIterate M k p) = (d.toLinearMap)^[k] (e.jet.value p) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [spatialIterate, Function.iterate_succ_apply', e.value_spatial]
    rw [← spatialIterate, ih, Function.iterate_succ_apply']

theorem first_iterate (k : ℕ) (p : Poly M) :
    e.jet.first (spatialIterate M k p) = (d.toLinearMap)^[k] (e.jet.first p) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [spatialIterate, Function.iterate_succ_apply', e.first_spatial]
    rw [← spatialIterate, ih, Function.iterate_succ_apply']

theorem second_iterate (k : ℕ) (p : Poly M) :
    e.jet.second (spatialIterate M k p) = (d.toLinearMap)^[k] (e.jet.second p) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [spatialIterate, Function.iterate_succ_apply', e.second_spatial]
    rw [← spatialIterate, ih, Function.iterate_succ_apply']

theorem normalProduct_value (order : ℤ) (a b : ℕ → Poly M) (k : ℕ) :
    e.jet.value (normalProduct M order a b k) =
      normalProductCoefficient d order (fun r => e.jet.value (a r)) (fun s => e.jet.value (b s)) k := by
  classical
  unfold normalProduct normalProductCoefficient
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro r _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro s _
  split_ifs
  · rw [map_mul, map_mul, e.value_C, e.value_iterate]
  · rw [map_zero]

theorem normalProduct_first (order : ℤ) (a b : ℕ → Poly M) (k : ℕ) :
    e.jet.first (normalProduct M order a b k) =
      normalProductCoefficient d order (fun r => e.jet.first (a r)) (fun s => e.jet.value (b s)) k +
      normalProductCoefficient d order (fun r => e.jet.value (a r)) (fun s => e.jet.first (b s)) k := by
  classical
  unfold normalProduct normalProductCoefficient
  rw [map_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _
  rw [map_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s _
  split_ifs
  · simp only [e.jet.first_mul, map_mul, e.first_C, zero_mul, zero_add,
      e.value_C, e.value_iterate, e.first_iterate] <;> ring
  · simp

theorem normalProduct_second (order : ℤ) (a b : ℕ → Poly M) (k : ℕ) :
    e.jet.second (normalProduct M order a b k) =
      normalProductCoefficient d order (fun r => e.jet.second (a r)) (fun s => e.jet.value (b s)) k +
      normalProductCoefficient d order (fun r => e.jet.first (a r)) (fun s => e.jet.first (b s)) k +
      normalProductCoefficient d order (fun r => e.jet.first (a r)) (fun s => e.jet.first (b s)) k +
      normalProductCoefficient d order (fun r => e.jet.value (a r)) (fun s => e.jet.second (b s)) k := by
  classical
  unfold normalProduct normalProductCoefficient
  rw [map_sum]
  repeat rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _
  rw [map_sum]
  repeat rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s _
  split_ifs
  · simp only [e.jet.second_mul, e.jet.first_mul, map_mul,
      e.first_C, e.second_C, zero_mul, zero_add, e.value_C,
      e.value_iterate, e.first_iterate, e.second_iterate] <;> ring
  · simp

theorem inverseRemainder_value (H V : ℕ → Poly M) (n : ℕ) :
    e.jet.value (normalInverseRemainder (spatialEvolution M) H V n) =
      normalInverseRemainder d (fun r => e.jet.value (H r)) (fun s => e.jet.value (V s)) n := by
  classical
  unfold normalInverseRemainder
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro s _
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro r _
  split_ifs
  · change e.jet.value (MvPolynomial.C _ * H r.val * spatialIterate M _ (V s.val)) = _
    rw [map_mul, map_mul, e.value_C, e.value_iterate]
  · rw [map_zero]

theorem inverseRemainder_first (H V : ℕ → Poly M) (n : ℕ) :
    e.jet.first (normalInverseRemainder (spatialEvolution M) H V n) =
      normalInverseRemainder d (fun r => e.jet.first (H r)) (fun s => e.jet.value (V s)) n +
      normalInverseRemainder d (fun r => e.jet.value (H r)) (fun s => e.jet.first (V s)) n := by
  classical
  unfold normalInverseRemainder
  rw [map_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s _
  rw [map_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _
  split_ifs
  · change e.jet.first (MvPolynomial.C _ * H r.val * spatialIterate M _ (V s.val)) = _
    simp only [e.jet.first_mul, map_mul, e.first_C, zero_mul, zero_add,
      e.value_C, e.value_iterate, e.first_iterate] <;> ring
  · simp

theorem inverseRemainder_second (H V : ℕ → Poly M) (n : ℕ) :
    e.jet.second (normalInverseRemainder (spatialEvolution M) H V n) =
      normalInverseRemainder d (fun r => e.jet.second (H r)) (fun s => e.jet.value (V s)) n +
      normalInverseRemainder d (fun r => e.jet.first (H r)) (fun s => e.jet.first (V s)) n +
      normalInverseRemainder d (fun r => e.jet.first (H r)) (fun s => e.jet.first (V s)) n +
      normalInverseRemainder d (fun r => e.jet.value (H r)) (fun s => e.jet.second (V s)) n := by
  classical
  unfold normalInverseRemainder
  rw [map_sum]
  repeat rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro s _
  rw [map_sum]
  repeat rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro r _
  split_ifs
  · change e.jet.second (MvPolynomial.C _ * H r.val * spatialIterate M _ (V s.val)) = _
    simp only [e.jet.second_mul, e.jet.first_mul, map_mul,
      e.first_C, e.second_C, zero_mul, zero_add, e.value_C,
      e.value_iterate, e.first_iterate, e.second_iterate] <;> ring
  · simp

end DifferentialJetEvaluation

end BalancedPDO
#print axioms BalancedPDO.DifferentialJetEvaluation.normalProduct_second
end
end DLWLean
