import PkgAnalyticJets

noncomputable section
namespace DLWContract.CenteredFamily
open UniformAnalytic AnalyticJets
abbrev Space := ℝ × (ℝ × ℝ)
abbrev Full := ℝ × Space

def shift (c : ℝ) (p : Full) : Full := (p.1,p.2.1,p.2.2.1+c*p.1,p.2.2.2)
def uField (A B : Full → ℝ) (p : Full) := 2*A p-B (shift (-1/2) p)-B (shift (1/2) p)
def numerator (A B : Full → ℝ) (p : Full) :=
  A (shift 1 p)-A (shift (-1) p)+(7/2)*(B (shift (1/2) p)-B (shift (-1/2) p))-
    (1/2)*(B (shift (3/2) p)-B (shift (-3/2) p))
def yjet (A : Full → ℝ) (z : Space) := deriv (fun y => A (0,z.1,y,z.2.2)) z.2.1

theorem shift_zero (c : ℝ) (z : Space) : shift c (0,z)=(0,z) := by simp [shift]
theorem shift_analytic (c : ℝ) (p : Full) : AnalyticAt ℝ (shift c) p := by
  apply ContDiffAt.analyticAt
  change ContDiffAt ℝ ⊤ (shift c) p
  unfold shift
  fun_prop
theorem analytic_shift {A : Full → ℝ} {z : Space} (hA : AnalyticAt ℝ A (0,z)) (c : ℝ) :
    AnalyticAt ℝ (fun p => A (shift c p)) (0,z) := by
  apply AnalyticAt.comp _ (shift_analytic c _)
  rwa [shift_zero]

theorem shift_derivative {A : Full → ℝ} {z : Space} (hA : AnalyticAt ℝ A (0,z)) (c : ℝ) :
    HasDerivAt (fun h => A (shift c (h,z))) (dh A (0,z)+c*yjet A z) 0 := by
  have hd := hA.differentiableAt.hasFDerivAt
  have hp : HasDerivAt (fun h : ℝ => shift c (h,z)) ((1,(0,(c,0))) : Full) 0 := by
    unfold shift
    convert! (hasDerivAt_id (0 : ℝ)).prodMk
      ((hasDerivAt_const (0 : ℝ) z.1).prodMk
        ((((hasDerivAt_id (0 : ℝ)).const_mul c).const_add z.2.1).prodMk
          (hasDerivAt_const (0 : ℝ) z.2.2))) using 1 <;> simp
  have hp0 : shift c (0,z)=(0,z) := shift_zero c z
  have H := (hp0.symm ▸ hd).comp_hasDerivAt 0 hp
  have hy := hd.comp_hasDerivAt z.2.1
    ((hasDerivAt_const z.2.1 (0 : ℝ)).prodMk
      ((hasDerivAt_const z.2.1 z.1).prodMk
        ((hasDerivAt_id z.2.1).prodMk (hasDerivAt_const z.2.1 z.2.2))))
  have hy' : yjet A z=fderiv ℝ A (0,z) (0,0,1,0) := hy.deriv
  rw [hy',dh]
  convert! H using 1
  rw [show ((1,(0,(c,0))) : Full)=((1,0) : Full)+c • ((0,0,1,0) : Full) by ext <;> simp,
    map_add,map_smul]
  simp only [shift_zero,smul_eq_mul]

theorem fields_analytic {A B : Full → ℝ} {z : Space}
    (hA : AnalyticAt ℝ A (0,z)) (hB : AnalyticAt ℝ B (0,z)) :
    AnalyticAt ℝ (uField A B) (0,z) ∧ AnalyticAt ℝ (numerator A B) (0,z) := by
  constructor
  · exact ((analyticAt_const.mul hA).sub (analytic_shift hB _)).sub (analytic_shift hB _)
  · exact (((analytic_shift hA _).sub (analytic_shift hA _)).add
      (analyticAt_const.mul ((analytic_shift hB _).sub (analytic_shift hB _)))).sub
        (analyticAt_const.mul ((analytic_shift hB _).sub (analytic_shift hB _)))

theorem field_zero (A B : Full → ℝ) (z : Space) :
    uField A B (0,z)=2*(A (0,z)-B (0,z)) ∧ numerator A B (0,z)=0 := by
  simp only [uField,numerator,shift_zero]
  constructor <;> ring

theorem numerator_derivative {A B : Full → ℝ} {z : Space}
    (hA : AnalyticAt ℝ A (0,z)) (hB : AnalyticAt ℝ B (0,z)) :
    HasDerivAt (fun h => numerator A B (h,z)) (2*(yjet A z+yjet B z)) 0 := by
  have H := (((shift_derivative hA 1).sub (shift_derivative hA (-1))).add
    (((shift_derivative hB (1/2)).sub (shift_derivative hB (-1/2))).const_mul (7/2))).sub
      (((shift_derivative hB (3/2)).sub (shift_derivative hB (-3/2))).const_mul (1/2))
  convert! H using 1 <;> ring

theorem fields_parity (A B : Full → ℝ)
    (hA : ∀ h z, A (-h,z)=A (h,z)) (hB : ∀ h z, B (-h,z)=B (h,z)) (h : ℝ) (z : Space) :
    uField A B (-h,z)=uField A B (h,z) ∧ numerator A B (-h,z)= -numerator A B (h,z) := by
  have hs (C : Full → ℝ) (hc : ∀ h z, C (-h,z)=C (h,z)) (c : ℝ) :
      C (shift c (-h,z))=C (shift (-c) (h,z)) := by
    unfold shift
    rw [hc]
    congr 2 <;> ring
  simp only [uField,numerator,hA,hs A hA,hs B hB,neg_neg]
  constructor <;> ring

end DLWContract.CenteredFamily
