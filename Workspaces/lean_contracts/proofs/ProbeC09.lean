/-
Scratch probe for C09: discover exact Mathlib lemma names/signatures.
NOT a deliverable. Delete at the end.
-/
import Contracts
import Mathlib.LinearAlgebra.Matrix.SchurComplement
import Mathlib.LinearAlgebra.Matrix.Charpoly.Coeff
import Mathlib.Tactic

noncomputable section
open scoped BigOperators
namespace DLWContract

#check @ContDiff.sum
#check @contDiff_prod
#check @contDiff_prod'
#check @ContDiff.prod
#check @ContDiff.const_mul
#check @ContDiff.mul
#check @contDiff_const
#check @contDiff_fst
#check @contDiff_snd
#check @Real.contDiff_exp
#check @Matrix.det_apply
#check @Matrix.det_apply'
#check @AlternatingMap.map_add_univ
#check @Matrix.detRowAlternating
#check @Matrix.det_piecewise_one_eq_submatrix_det
#check @Matrix.det_of_isLowerTriangular
#check @Matrix.det_of_isUpperTriangular
#check @Matrix.det_mul_column
#check @Matrix.det_mul_row
#check @Matrix.det_eq_of_eq_mul_det_one
#check @Matrix.det_eq_of_eq_det_one_mul
#check @Matrix.det_succ_row_zero
#check @Matrix.det_submatrix_equiv_self
#check @Matrix.submatrix_submatrix
#check @Matrix.det_diagonal
#check @Matrix.diagonal_mul_diagonal
#check @Matrix.diagonal_mul
#check @Matrix.mul_diagonal
#check @Matrix.submatrix_mul_equiv
#check @Matrix.det_fin_zero
#check @Matrix.det_one_add_mul_comm
#check @Matrix.det_add_mul_comm
#check @Matrix.det_one_add_smul
#check @Finset.orderIsoOfFin
#check @Finset.orderEmbOfFin
#check @Finset.coe_orderIsoOfFin_apply
#check @OrderEmbedding.lt_iff_lt
#check @OrderEmbedding.toStrictMono
#check @OrderEmbedding.strictMono
#check @Finset.prod_neg
#check @Finset.prod_inv_distrib
#check @Finset.prod_pos
#check @Finset.sum_pos
#check @Finset.sum_pos'
#check @Fin.prod_univ_succ
#check @Fin.sum_univ_succ
#check @Even.neg_one_pow
#check @mul_zpow
#check @inv_zpow
#check @inv_zpow'
#check @zpow_neg
#check @zpow_neg'
#check @zpow_pos
#check @zpow_ne_zero
#check @zpow_zero
#check @zpow_one
#check @div_eq_mul_inv
#check @mul_inv_rev
#check @Real.exp_add
#check @Real.exp_pos
#check @Real.exp_ne_zero
#check @Units.smul_def
#check @Matrix.det_congr
#check @Matrix.submatrix_mul
#check @Finset.sum_eq_single
#check @Finset.sum_ite_eq
#check @Finset.sum_ite_eq'

/-! ### attempt: ContDiff of det -/
example {N : ℕ} {M : Fin N → Fin N → (ℝ × ℝ) → ℝ}
    (hM : ∀ i k, ContDiff ℝ ⊤ (M i k)) :
    ContDiff ℝ ⊤ (fun z : ℝ × ℝ => Matrix.det (fun i k => M i k z)) := by
  rw [show (fun z : ℝ × ℝ => Matrix.det (fun i k => M i k z))
      = fun z => ∑ σ : Equiv.Perm (Fin N), ((Equiv.Perm.sign σ : ℤ) : ℝ) * ∏ i, M (σ i) i z from by
        funext z
        rw [Matrix.det_apply]
        refine Finset.sum_congr rfl fun σ _ => ?_
        rw [Units.smul_def]]
  refine ContDiff.sum fun σ _ => ?_
  exact contDiff_const.mul (contDiff_prod fun i _ => hM (σ i) i)

/-! ### attempt: entry is ContDiff via fun_prop -/
example {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (i k : Fin N) :
    ContDiff ℝ ⊤ (fun z : ℝ × ℝ => entry D h s n j i k z.1 z.2) := by
  unfold entry
  fun_prop

/-! ### attempt: entry is ContDiff explicitly -/
example {N : ℕ} (D : Data N) (h s : ℝ) (n j : ℤ) (i k : Fin N) :
    ContDiff ℝ ⊤ (fun z : ℝ × ℝ => entry D h s n j i k z.1 z.2) := by
  unfold entry
  refine ContDiff.add contDiff_const ?_
  refine ContDiff.mul ?_ ?_
  · refine ContDiff.mul ?_ contDiff_const
    exact ContDiff.mul contDiff_const contDiff_const
  · exact Real.contDiff_exp.comp (by fun_prop)

/-! ### attempt: Admissible -/
theorem c09_admissible_probe {N : ℕ} (D : Data N) (h : ℝ) (hD : PositiveData D h) :
    Admissible D h := by
  obtain ⟨hh, hp, hq, hdata⟩ := hD
  refine ⟨ne_of_gt hh, ?_, ?_, ?_⟩
  · intro i k
    have h1 : 0 < D.p i := (hdata i).1
    have h2 : 0 < D.q k := (hdata k).2.2.1
    linarith
  · intro i
    have h1 : D.p i < D.a - h / 2 := (hdata i).2.1
    constructor <;> linarith
  · intro k
    have h1 : 0 < D.p k := (hdata k).1
    have h2 : D.p k < D.a - h / 2 := (hdata k).2.1
    have h3 : 0 < D.q k := (hdata k).2.2.1
    constructor <;> linarith

end DLWContract
