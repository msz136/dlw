import PkgGramDeterminant

noncomputable section
open scoped BigOperators Matrix
open Filter Topology
namespace DLWContract.GramDeterminant

theorem det_rank_two_update {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (u v r b : Fin N → ℝ) (hA : A.det ≠ 0) :
    (A+Matrix.vecMulVec u v+Matrix.vecMulVec r b).det =
      A.det*((1+v ⬝ᵥ (A⁻¹ *ᵥ u))*(1+b ⬝ᵥ (A⁻¹ *ᵥ r))-
        (v ⬝ᵥ (A⁻¹ *ᵥ r))*(b ⬝ᵥ (A⁻¹ *ᵥ u))) := by
  let U : Matrix (Fin N) (Fin 2) ℝ := fun i => ![u i,r i]
  let V : Matrix (Fin 2) (Fin N) ℝ := ![v,b]
  have he : A+U*V=A+Matrix.vecMulVec u v+Matrix.vecMulVec r b := by
    ext i j
    change A i j+(∑ k : Fin 2, U i k*V k j)=A i j+u i*v j+r i*b j
    simp [U,V,Fin.sum_univ_two,add_assoc]
  have H := Matrix.det_add_mul U V (isUnit_iff_ne_zero.mpr hA)
  have hp (i j : Fin 2) : (V*A⁻¹*U) i j = V i ⬝ᵥ (A⁻¹ *ᵥ (fun k => U k j)) := by
    simp only [Matrix.mul_apply,Matrix.dot_mulVec_eq_sum_sum,Finset.sum_mul]
  rw [he] at H
  rw [H,Matrix.det_fin_two]
  congr 1
  simp only [Matrix.add_apply,Matrix.one_apply,hp]
  norm_num [U,V]

theorem continuous_dDet {N : ℕ} :
    Continuous (fun p : Matrix (Fin N) (Fin N) ℝ × Matrix (Fin N) (Fin N) ℝ =>
      dDet p.1 p.2) := by
  unfold dDet
  apply continuous_finset_sum
  intro i hi
  apply Continuous.matrix_det
  apply continuous_pi
  intro j
  apply continuous_pi
  intro k
  by_cases h : j=i
  · subst j
    simp only [Matrix.updateRow,Function.update_self]
    fun_prop
  · simp only [Matrix.updateRow,Function.update_of_ne h]
    fun_prop

end DLWContract.GramDeterminant
