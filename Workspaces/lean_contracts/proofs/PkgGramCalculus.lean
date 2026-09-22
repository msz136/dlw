import PkgGramDeterminant
import Mathlib.Analysis.Calculus.Deriv.Prod

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.GramDeterminant

theorem det_two_proportional_rows {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (i j : Fin N) (hij : i ≠ j) (a b : ℝ) (v : Fin N → ℝ) :
    ((A.updateRow i (a • v)).updateRow j (b • v)).det=0 := by
  rw [Matrix.det_updateRow_smul]
  have he : (A.updateRow i (a • v)).updateRow j v =
      (A.updateRow j v).updateRow i (a • v) := by
    exact Matrix.updateRow_comm A hij (a • v) v
  rw [he,Matrix.det_updateRow_smul]
  have hz : ((A.updateRow j v).updateRow i v).det=0 := by
    apply Matrix.det_zero_of_row_eq (i := i) (j := j)
    · exact hij
    · rw [Matrix.updateRow_self,Matrix.updateRow_ne (Ne.symm hij),Matrix.updateRow_self]
  rw [hz]
  ring

theorem hasDerivAt_updateRow {N : ℕ} (A V : ℝ → Matrix (Fin N) (Fin N) ℝ)
    (A' V' : Matrix (Fin N) (Fin N) ℝ) (x : ℝ) (i : Fin N)
    (hA : HasDerivAt A A' x) (hV : HasDerivAt V V' x) :
    HasDerivAt (fun y => (A y).updateRow i (V y i)) (A'.updateRow i (V' i)) x := by
  apply hasDerivAt_pi.mpr
  intro j
  by_cases h : j=i
  · subst j
    simpa only [Matrix.updateRow_self] using (hasDerivAt_pi.mp hV i)
  · simpa only [Matrix.updateRow_ne h] using (hasDerivAt_pi.mp hA j)

theorem dDet_derivative_rank_one {N : ℕ}
    (A V : ℝ → Matrix (Fin N) (Fin N) ℝ) (V' : Matrix (Fin N) (Fin N) ℝ)
    (x : ℝ) (r c : Fin N → ℝ)
    (hA : HasDerivAt A (Matrix.vecMulVec r c) x) (hV : HasDerivAt V V' x)
    (hVx : V x=Matrix.vecMulVec r c) :
    HasDerivAt (fun y => dDet (A y) (V y)) (dDet (A x) V') x := by
  have H (i : Fin N) := det_derivative
    (fun y => (A y).updateRow i (V y i))
    ((Matrix.vecMulVec r c).updateRow i (V' i)) x
    (hasDerivAt_updateRow A V _ V' x i hA hV)
  have Hi (i : Fin N) : HasDerivAt
      (fun y => ((A y).updateRow i (V y i)).det) ((A x).updateRow i (V' i)).det x := by
    convert H i using 1
    symm
    rw [Finset.sum_eq_single i]
    · rw [Matrix.updateRow_self,Matrix.updateRow_idem]
    · intro j hj hji
      rw [hVx]
      rw [Matrix.updateRow_ne hji]
      change (((A x).updateRow i ((r i) • c)).updateRow j ((r j) • c)).det=0
      exact
        det_two_proportional_rows (A x) i j (Ne.symm hji) (r i) (r j) c
    · simp
  simpa only [dDet] using HasDerivAt.fun_sum (u := Finset.univ) (fun i _ => Hi i)

theorem det_second_derivative_rank_one {N : ℕ}
    (A V : ℝ → Matrix (Fin N) (Fin N) ℝ) (V' : Matrix (Fin N) (Fin N) ℝ)
    (x : ℝ) (r c : Fin N → ℝ)
    (hA : ∀ y, HasDerivAt A (V y) y) (hV : HasDerivAt V V' x)
    (hVx : V x=Matrix.vecMulVec r c) :
    HasDerivAt (deriv (fun y => (A y).det)) (dDet (A x) V') x := by
  have he : deriv (fun y => (A y).det)=fun y => dDet (A y) (V y) := by
    funext y
    exact (det_derivative A (V y) y (hA y)).deriv
  rw [he]
  apply dDet_derivative_rank_one A V V' x r c _ hV hVx
  simpa [hVx] using hA x

end DLWContract.GramDeterminant
