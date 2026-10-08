import PkgCenteredFamily

noncomputable section
open Set
namespace DLWContract.CenteredFamily
open UniformAnalytic AnalyticJets

def residual (J : Full → ℝ) (p : Full) := J p-p.1*dh J (0,p.2)

theorem residual_analytic {J : Full → ℝ} {z : Space} (hJ : AnalyticAt ℝ J (0,z)) :
    AnalyticAt ℝ (residual J) (0,z) := by
  have hp : AnalyticAt ℝ (fun p : Full => ((0,p.2) : Full)) (0,z) := by
    apply ContDiffAt.analyticAt
    change ContDiffAt ℝ ⊤ (fun p : Full => ((0,p.2) : Full)) (0,z)
    fun_prop
  have hc : AnalyticAt ℝ (fun p : Full => dh J (0,p.2)) (0,z) :=
    AnalyticAt.comp (f := fun p : Full => (0,p.2)) (x := (0,z)) (analytic_dh hJ) hp
  exact hJ.sub (analyticAt_fst.mul hc)

theorem residual_first_zero {J : Full → ℝ} {z : Space} (hJ : AnalyticAt ℝ J (0,z)) :
    dh (residual J) (0,z)=0 := by
  have H := (dh_hasDerivAt 0 z hJ).sub
    ((hasDerivAt_id (0 : ℝ)).mul_const (dh J (0,z)))
  have H' : HasDerivAt (fun h => residual J (h,z)) 0 0 := by
    convert! H using 1 <;> ring
  exact (dh_eq (residual_analytic hJ)).trans H'.deriv

theorem uniform_fields (A B : Full → ℝ)
    (hA : ∀ z, AnalyticAt ℝ A (0,z)) (hB : ∀ z, AnalyticAt ℝ B (0,z))
    (heA : ∀ h z, A (-h,z)=A (h,z)) (heB : ∀ h z, B (-h,z)=B (h,z)) :
    UniformBoxO2 (fun h x y t => uField A B (h,x,y,t)-2*(A (0,x,y,t)-B (0,x,y,t))) ∧
    UniformBoxO2 (fun h x y t => numerator A B (h,x,y,t)/h-
      2*(yjet A (x,y,t)+yjet B (x,y,t))) := by
  let U := uField A B
  let J := numerator A B
  have hU (z : Space) := (fields_analytic (hA z) (hB z)).1
  have hJ (z : Space) := (fields_analytic (hA z) (hB z)).2
  have hUz (z : Space) : dh U (0,z)=0 := by
    rw [dh_eq (hU z)]
    exact even_deriv_zero _ (fun h => (fields_parity A B heA heB h z).1)
  have hR2 (z : Space) : dh (dh (residual J)) (0,z)=0 := by
    rw [dh_dh_eq (residual_analytic (hJ z))]
    apply odd_second_zero
    intro h
    dsimp [residual]
    rw [(fields_parity A B heA heB h z).2]
    ring
  have hJd (z : Space) : dh J (0,z)=2*(yjet A z+yjet B z) :=
    (dh_eq (hJ z)).trans (numerator_derivative (hA z) (hB z)).deriv
  constructor
  · intro R hR
    let K : Set Space := Icc (-R) R ×ˢ (Icc (-R) R ×ˢ Icc (-R) R)
    have hK : IsCompact K := isCompact_Icc.prod (isCompact_Icc.prod isCompact_Icc)
    obtain ⟨C,hC,d,hd,hb⟩ := uniform_second_order U K hK (fun z _ => hU z) (fun z _ => hUz z)
    refine ⟨C,hC,d,hd,?_⟩
    intro h x y t hh hhd hx hy ht
    have H := hb h ⟨hh.le,hhd.le⟩ (x,y,t) ⟨abs_le.mp hx,abs_le.mp hy,abs_le.mp ht⟩
    simpa only [U,(field_zero A B (x,y,t)).1] using H
  · intro R hR
    let K : Set Space := Icc (-R) R ×ˢ (Icc (-R) R ×ˢ Icc (-R) R)
    have hK : IsCompact K := isCompact_Icc.prod (isCompact_Icc.prod isCompact_Icc)
    obtain ⟨C,hC,d,hd,hb⟩ := uniform_third_order (residual J) K hK
      (fun z _ => residual_analytic (hJ z)) (fun z _ => residual_first_zero (hJ z)) (fun z _ => hR2 z)
    refine ⟨C,hC,d,hd,?_⟩
    intro h x y t hh hhd hx hy ht
    have H := hb h ⟨hh.le,hhd.le⟩ (x,y,t) ⟨abs_le.mp hx,abs_le.mp hy,abs_le.mp ht⟩
    have hz : residual J (0,(x,y,t))=0 := by
      dsimp [residual,J]
      rw [(field_zero A B (x,y,t)).2]
      ring
    rw [hz,sub_zero] at H
    have he : numerator A B (h,x,y,t)/h-2*(yjet A (x,y,t)+yjet B (x,y,t))=
        residual J (h,(x,y,t))/h := by
      dsimp [residual]
      rw [hJd]
      dsimp [J]
      field_simp
    change |numerator A B (h,x,y,t)/h-2*(yjet A (x,y,t)+yjet B (x,y,t))|≤C*h^2
    rw [he,abs_div,abs_of_pos hh]
    apply (div_le_iff₀ hh).mpr
    calc |residual J (h,(x,y,t))| ≤ C*h^3 := H
      _ = C*h^2*h := by ring

#print axioms uniform_fields
end DLWContract.CenteredFamily
