import PkgGramPlucker
import Mathlib.Analysis.Calculus.Deriv.Prod

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.GramDeterminant

theorem dDet_shift_rank_one {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (r b u v : Fin N → ℝ) (hA : A.det ≠ 0) :
    dDet (A-Matrix.vecMulVec r b) (Matrix.vecMulVec u v) =
      A.det*((1-b ⬝ᵥ (A⁻¹ *ᵥ r))*(v ⬝ᵥ (A⁻¹ *ᵥ u))+
        (b ⬝ᵥ (A⁻¹ *ᵥ u))*(v ⬝ᵥ (A⁻¹ *ᵥ r))) := by
  let B := A-Matrix.vecMulVec r b
  let W := Matrix.vecMulVec u v
  let d := A.det
  let z := b ⬝ᵥ (A⁻¹ *ᵥ r)
  let k := v ⬝ᵥ (A⁻¹ *ᵥ u)
  let l := b ⬝ᵥ (A⁻¹ *ᵥ u)
  let m := v ⬝ᵥ (A⁻¹ *ᵥ r)
  have he (e : ℝ) : (B+e • W).det=d*(1-z)+e*(d*((1-z)*k+l*m)) := by
    have hm : B+e • W=A+Matrix.vecMulVec (-r) b+Matrix.vecMulVec (e • u) v := by
      ext i j
      simp [B,W,Matrix.vecMulVec]
      ring
    rw [hm,det_rank_two_update A (-r) b (e • u) v hA]
    simp only [Matrix.mulVec_neg,Matrix.mulVec_smul,dotProduct_neg,
      dotProduct_smul,smul_eq_mul]
    dsimp [d,z,k,l,m]
    ring
  have hpath : HasDerivAt (fun e : ℝ => B+e • W) W 0 := by
    apply hasDerivAt_pi.mpr
    intro i
    apply hasDerivAt_pi.mpr
    intro j
    change HasDerivAt (fun e : ℝ => B i j+e*W i j) (W i j) 0
    convert! ((hasDerivAt_id (0 : ℝ)).mul_const (W i j)).const_add (B i j) using 1 <;>
      simp
  have hf := det_derivative (fun e : ℝ => B+e • W) W 0 hpath
  have hg : HasDerivAt (fun e : ℝ => d*(1-z)+e*(d*((1-z)*k+l*m)))
      (d*((1-z)*k+l*m)) 0 := by
    convert! ((hasDerivAt_id (0 : ℝ)).mul_const (d*((1-z)*k+l*m))).const_add (d*(1-z)) using 1 <;>
      simp
  have hfun : (fun e : ℝ => (B+e • W).det)=
      (fun e : ℝ => d*(1-z)+e*(d*((1-z)*k+l*m))) := funext he
  rw [hfun] at hf
  simpa only [zero_smul,add_zero,dDet,B,W,d,z,k,l,m] using hf.unique hg

theorem plucker_identity {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (r b u v : Fin N → ℝ) :
    A.det*dDet (A-Matrix.vecMulVec r b) (Matrix.vecMulVec u v)-
      (A-Matrix.vecMulVec r b).det*dDet A (Matrix.vecMulVec u v)=
      dDet (A-Matrix.vecMulVec r b) (Matrix.vecMulVec u b)*
        dDet A (Matrix.vecMulVec r v) := by
  apply continuous_identity_of_invertible
    (fun A => A.det*dDet (A-Matrix.vecMulVec r b) (Matrix.vecMulVec u v)-
      (A-Matrix.vecMulVec r b).det*dDet A (Matrix.vecMulVec u v))
    (fun A => dDet (A-Matrix.vecMulVec r b) (Matrix.vecMulVec u b)*
      dDet A (Matrix.vecMulVec r v))
  · exact (continuous_id.matrix_det.mul
      (continuous_dDet.comp ((continuous_id.sub continuous_const).prodMk continuous_const))).sub
      ((continuous_id.sub continuous_const).matrix_det.mul
        (continuous_dDet.comp (continuous_id.prodMk continuous_const)))
  · exact (continuous_dDet.comp
      ((continuous_id.sub continuous_const).prodMk continuous_const)).mul
      (continuous_dDet.comp (continuous_id.prodMk continuous_const))
  · intro M hM
    rw [dDet_shift_rank_one M r b u v hM,det_rank_one_update M r b hM,
      dDet_rank_one M u v hM,dDet_shift_rank_one M r b u b hM,
      dDet_rank_one M r v hM]
    ring

#print axioms plucker_identity
end DLWContract.GramDeterminant
