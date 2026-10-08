import Contracts
import Mathlib.Analysis.Calculus.FDeriv.Analytic
import Mathlib.Topology.Instances.Matrix
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Analysis.Polynomial.Basic
import Mathlib.Tactic

noncomputable section
open scoped BigOperators Matrix
open Filter Topology
namespace DLWContract
namespace GramDeterminant

def detMap (N : ℕ) : ContinuousMultilinearMap ℝ (fun _ : Fin N => Fin N → ℝ) ℝ :=
  { Matrix.detRowAlternating.toMultilinearMap with
    cont := continuous_id.matrix_det }

theorem det_derivative {N : ℕ} (M : ℝ → Matrix (Fin N) (Fin N) ℝ)
    (V : Matrix (Fin N) (Fin N) ℝ) (x : ℝ) (hM : HasDerivAt M V x) :
    HasDerivAt (fun t => (M t).det)
      (∑ i, (Matrix.updateRow (M x) i (V i)).det) x := by
  have H := ((detMap N).hasFDerivAt (M x)).comp_hasDerivAt x hM
  convert H using 1
  · rfl
  · exact (ContinuousMultilinearMap.linearDeriv_apply (detMap N) (M x) V).symm

theorem det_rank_one_update {N : ℕ} (M : Matrix (Fin N) (Fin N) ℝ)
    (r b : Fin N → ℝ) (hM : M.det ≠ 0) :
    (M-Matrix.vecMulVec r b).det = M.det*(1-b ⬝ᵥ (M⁻¹ *ᵥ r)) := by
  have H := Matrix.det_add_mul (A := M)
    (Matrix.replicateCol (Fin 1) (-r)) (Matrix.replicateRow (Fin 1) b)
    (isUnit_iff_ne_zero.mpr hM)
  have heq : M+Matrix.replicateCol (Fin 1) (-r)*Matrix.replicateRow (Fin 1) b =
      M-Matrix.vecMulVec r b := by
    ext i j
    simp [Matrix.mul_apply,Matrix.vecMulVec,sub_eq_add_neg]
  rw [heq] at H
  rw [H]
  congr 1
  rw [Matrix.det_unique (n := Fin 1)]
  simp only [Matrix.add_apply, Matrix.one_apply_eq, Matrix.mul_apply,Matrix.mulVec,dotProduct,Finset.mul_sum,Finset.sum_mul,
    Matrix.replicateCol,Matrix.replicateRow,Matrix.of_apply]
  simp only [Pi.neg_apply, mul_neg, Finset.sum_neg_distrib, ← sub_eq_add_neg]
  congr 1
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

def dDet {N : ℕ} (A V : Matrix (Fin N) (Fin N) ℝ) : ℝ :=
  ∑ i, (A.updateRow i (V i)).det

theorem dDet_eq_linearDeriv {N : ℕ} (A V : Matrix (Fin N) (Fin N) ℝ) :
    dDet A V = (detMap N).linearDeriv A V :=
  (ContinuousMultilinearMap.linearDeriv_apply (detMap N) A V).symm

theorem dDet_add {N : ℕ} (A V W : Matrix (Fin N) (Fin N) ℝ) :
    dDet A (V+W) = dDet A V+dDet A W := by
  simp only [dDet_eq_linearDeriv]
  exact ((detMap N).linearDeriv A).map_add V W

theorem dDet_smul {N : ℕ} (A V : Matrix (Fin N) (Fin N) ℝ) (s : ℝ) :
    dDet A (s • V) = s*dDet A V := by
  simp only [dDet_eq_linearDeriv]
  exact ((detMap N).linearDeriv A).map_smul s V

theorem det_updateRow_inverse {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (i : Fin N) (w : Fin N → ℝ) (hA : A.det ≠ 0) :
    (A.updateRow i w).det = (w ᵥ* A⁻¹) i*A.det := by
  have hrow : ∑ k, (w ᵥ* A⁻¹) k • A k = w := by
    rw [← Matrix.vecMul_eq_sum, Matrix.vecMul_vecMul,
      Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hA),Matrix.vecMul_one]
  simpa only [hrow,smul_eq_mul] using Matrix.det_updateRow_sum A i (w ᵥ* A⁻¹)

theorem dDet_rank_one {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (r b : Fin N → ℝ) (hA : A.det ≠ 0) :
    dDet A (Matrix.vecMulVec r b) = A.det*(b ⬝ᵥ (A⁻¹ *ᵥ r)) := by
  simp only [dDet,det_updateRow_inverse A _ _ hA,Matrix.vecMulVec,
    Matrix.of_apply,Matrix.vecMul, dotProduct, Matrix.mulVec, Finset.sum_mul,Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i hi
  apply Finset.sum_congr rfl
  intro j hj
  ring

/-- Invertibility is available arbitrarily close to every matrix, including
singular matrices. The characteristic polynomial has only finitely many roots.
This is the device for removing the temporary inverse in algebraic identities. -/
theorem invertible_shift_eventually {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ) :
    ∀ᶠ z : ℝ in nhdsWithin 0 ({0}ᶜ), (A+Matrix.scalar (Fin N) z).det ≠ 0 := by
  have H := (Polynomial.eventually_cofinite_not_isRoot
    ((-A).charpoly_monic.ne_zero)).filter_mono (nhdsNE_le_cofinite (0 : ℝ))
  simpa only [Polynomial.IsRoot, Matrix.eval_charpoly,sub_neg_eq_add,add_comm] using H

/-- A continuous identity verified on nonsingular matrices holds everywhere. -/
theorem continuous_identity_of_invertible {N : ℕ}
    (f g : Matrix (Fin N) (Fin N) ℝ → ℝ) (hf : Continuous f) (hg : Continuous g)
    (hfg : ∀ A, A.det ≠ 0 → f A=g A) (A : Matrix (Fin N) (Fin N) ℝ) : f A=g A := by
  have hc : Continuous (fun z : ℝ => A+Matrix.scalar (Fin N) z) := by
    apply continuous_const.add
    apply continuous_pi
    intro i
    apply continuous_pi
    intro j
    by_cases h : i=j <;> simp [Matrix.scalar_apply,Matrix.diagonal,h] <;> fun_prop
  have he : ∀ᶠ z : ℝ in nhdsWithin 0 ({0}ᶜ),
      f (A+Matrix.scalar (Fin N) z)=g (A+Matrix.scalar (Fin N) z) :=
    (invertible_shift_eventually A).mono (fun z hz => hfg _ hz)
  have hf' : Tendsto (fun z : ℝ => f (A+Matrix.scalar (Fin N) z))
      (nhdsWithin 0 ({0}ᶜ)) (nhds (f A)) := by
    simpa [Function.comp_def] using ((hf.comp hc).tendsto 0).mono_left
      (nhdsWithin_le_nhds (s := ({0}ᶜ : Set ℝ)) (a := (0 : ℝ)))
  have hg' : Tendsto (fun z : ℝ => g (A+Matrix.scalar (Fin N) z))
      (nhdsWithin 0 ({0}ᶜ)) (nhds (g A)) := by
    simpa [Function.comp_def] using ((hg.comp hc).tendsto 0).mono_left
      (nhdsWithin_le_nhds (s := ({0}ᶜ : Set ℝ)) (a := (0 : ℝ)))
  have H := tendsto_nhds_unique hf' (hg'.congr' (he.mono fun _ h => h.symm))
  simpa using H

#print axioms continuous_identity_of_invertible

end GramDeterminant
end DLWContract
