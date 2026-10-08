import PkgGramIdentity
import PkgGramCalculus

noncomputable section
open scoped BigOperators Matrix
namespace DLWContract.GramDeterminant

/-- Algebraic Hirota identity. The only inputs are the rank-one layer change
and the two linear flow identities; invertibility is not assumed. -/
theorem matrix_hirota {N : ℕ} (A : Matrix (Fin N) (Fin N) ℝ)
    (r b u c : Fin N → ℝ) (s : ℝ)
    (WA TA WB TB : Matrix (Fin N) (Fin N) ℝ)
    (hA : WA-TA-(2*s) • Matrix.vecMulVec r c = (-2 : ℝ) • Matrix.vecMulVec u c)
    (hB : WB+TB+(2*s) • Matrix.vecMulVec u b = (2 : ℝ) • Matrix.vecMulVec u c) :
    let B := A-Matrix.vecMulVec r b
    dDet B WB*A.det-2*dDet B (Matrix.vecMulVec u b)*dDet A (Matrix.vecMulVec r c)+
      B.det*dDet A WA+dDet B TB*A.det-B.det*dDet A TA+
      (2*s)*(dDet B (Matrix.vecMulVec u b)*A.det-B.det*dDet A (Matrix.vecMulVec r c))=0 := by
  let B := A-Matrix.vecMulVec r b
  have H := plucker_identity A r b u c
  have ha := congrArg (dDet A) hA
  have hb := congrArg (dDet B) hB
  have sub (M V W : Matrix (Fin N) (Fin N) ℝ) :
      dDet M (V-W)=dDet M V-dDet M W := by
    simp only [dDet_eq_linearDeriv]
    exact ((detMap N).linearDeriv M).map_sub V W
  simp only [sub,dDet_add,dDet_smul] at ha hb
  dsimp only
  dsimp [B] at hb
  linear_combination A.det*hb+(A-Matrix.vecMulVec r b).det*ha+2*H

/-- The algebraic engine applied to actual derivatives of two matrix fields. -/
theorem bil_det_of_jets {N : ℕ} (s : ℝ)
    (A B VA VB WA WB TA TB : ℝ → ℝ → Matrix (Fin N) (Fin N) ℝ)
    (hAx : ∀ x t, HasDerivAt (fun z => A z t) (VA x t) x)
    (hBx : ∀ x t, HasDerivAt (fun z => B z t) (VB x t) x)
    (hVA : ∀ x t, HasDerivAt (fun z => VA z t) (WA x t) x)
    (hVB : ∀ x t, HasDerivAt (fun z => VB z t) (WB x t) x)
    (hAt : ∀ x t, HasDerivAt (A x) (TA x t) t)
    (hBt : ∀ x t, HasDerivAt (B x) (TB x t) t)
    (x t : ℝ) (r b u c : Fin N → ℝ)
    (hshift : B x t=A x t-Matrix.vecMulVec r b)
    (hra : VA x t=Matrix.vecMulVec r c)
    (hrb : VB x t=Matrix.vecMulVec u b)
    (ha : WA x t-TA x t-(2*s) • VA x t=(-2 : ℝ) • Matrix.vecMulVec u c)
    (hb : WB x t+TB x t+(2*s) • VB x t=(2 : ℝ) • Matrix.vecMulVec u c) :
    bil s (fun x t => (B x t).det) (fun x t => (A x t).det) x t=0 := by
  have dax := (det_derivative (fun z => A z t) (VA x t) x (hAx x t)).deriv
  have dbx := (det_derivative (fun z => B z t) (VB x t) x (hBx x t)).deriv
  have daxx := (det_second_derivative_rank_one
    (fun z => A z t) (fun z => VA z t) (WA x t) x r c
    (fun z => hAx z t) (hVA x t) hra).deriv
  have dbxx := (det_second_derivative_rank_one
    (fun z => B z t) (fun z => VB z t) (WB x t) x u b
    (fun z => hBx z t) (hVB x t) hrb).deriv
  have dat := (det_derivative (A x) (TA x t) t (hAt x t)).deriv
  have dbt := (det_derivative (B x) (TB x t) t (hBt x t)).deriv
  change _ = 0
  simp only [bil,hx,xx,dx,dt,Pi.add_apply,Pi.sub_apply,Pi.mul_apply,
    Pi.smul_apply,Pi.ofNat_apply,smul_eq_mul]
  rw [dax,dbx,daxx,dbxx,dat,dbt]
  change dDet (B x t) (WB x t)*(A x t).det-
    2*dDet (B x t) (VB x t)*dDet (A x t) (VA x t)+
    (B x t).det*dDet (A x t) (WA x t)+dDet (B x t) (TB x t)*(A x t).det-
    (B x t).det*dDet (A x t) (TA x t)+
    (2*s)*(dDet (B x t) (VB x t)*(A x t).det-(B x t).det*dDet (A x t) (VA x t))=0
  rw [hshift,hra,hrb]
  exact matrix_hirota (A x t) r b u c s (WA x t) (TA x t) (WB x t) (TB x t)
    (by simpa only [hra] using ha) (by simpa only [hrb] using hb)

end DLWContract.GramDeterminant
