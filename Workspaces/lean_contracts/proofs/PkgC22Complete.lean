import PkgGramExtensionAnalytic
import PkgCenteredUniform

noncomputable section
namespace DLWContract
namespace GramInterpolation

def fullA {N : ℕ} (D : Data N) (p : Full) := ax D p.1 p.2.1 p.2.2.1 p.2.2.2
def fullB {N : ℕ} (D : Data N) (p : Full) := bx D p.1 p.2.1 p.2.2.1 p.2.2.2

theorem interpU_ext {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0)
    (h x y t : ℝ) : interpU h (extF D h) (extG D h) x y t=
      2*ax D h x y t-bx D h x (y-h/2) t-bx D h x (y+h/2) t := by
  have hs := logs_smooth D h0 hD h
  have H := ((((c02_diff_x _ hs.1 x y t).hasDerivAt).const_mul 2).sub
    (c02_diff_x _ hs.2 x (y-h/2) t).hasDerivAt).sub
      (c02_diff_x _ hs.2 x (y+h/2) t).hasDerivAt
  exact H.deriv

theorem uField_eq {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0)
    (h x y t : ℝ) : CenteredFamily.uField (fullA D) (fullB D) (h,x,y,t)=
      interpU h (extF D h) (extG D h) x y t := by
  rw [interpU_ext D h0 hD]
  simp only [CenteredFamily.uField,CenteredFamily.shift,fullA,fullB]
  rw [show y+(-1/2)*h=y-h/2 by ring,show y+(1/2)*h=y+h/2 by ring]

theorem vField_eq {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0)
    (h x y t : ℝ) (hh : h ≠ 0) : CenteredFamily.numerator (fullA D) (fullB D) (h,x,y,t)/h=
      interpV h (extF D h) (extG D h) x y t := by
  have hs := (logs_smooth D h0 hD h).2
  have H := ((c02_diff_x _ hs x (y+h/2) t).hasDerivAt.sub
    (c02_diff_x _ hs x (y-h/2) t).hasDerivAt).deriv
  change deriv (fun z => Real.log (extG D h z (y+h/2) t)-Real.log (extG D h z (y-h/2) t)) x=
    bx D h x (y+h/2) t-bx D h x (y-h/2) t at H
  simp only [interpV,Pi.add_apply,Pi.smul_apply,smul_eq_mul]
  change _=(4/h)*deriv (fun z => Real.log (extG D h z (y+h/2) t)-Real.log (extG D h z (y-h/2) t)) x+
    (interpU h (extF D h) (extG D h) x (y+h) t-interpU h (extF D h) (extG D h) x (y-h) t)/(2*h)
  rw [H,interpU_ext D h0 hD,interpU_ext D h0 hD]
  simp only [CenteredFamily.numerator,CenteredFamily.shift,fullA,fullB,one_mul,neg_one_mul]
  rw [show y+ -h=y-h by ring,
    show y+(-1/2)*h=y-h/2 by ring,show y+(1/2)*h=y+h/2 by ring,
    show y+(-3/2)*h=y-3*h/2 by ring,show y+(3/2)*h=y+3*h/2 by ring,
    show y+h-h/2=y+h/2 by ring,show y+h+h/2=y+3*h/2 by ring,
    show y-h-h/2=y-3*h/2 by ring,show y-h+h/2=y-h/2 by ring]
  field_simp
  <;> ring

theorem continuous_fields {N : ℕ} (D : Data N) (h0 : ℝ) (hD : PositiveData D h0) (x y t : ℝ) :
    2*(fullA D (0,x,y,t)-fullB D (0,x,y,t))=cu (tau0 D 1) (tau0 D 0) x y t ∧
    2*(CenteredFamily.yjet (fullA D) (x,y,t)+CenteredFamily.yjet (fullB D) (x,y,t))=
      cv (tau0 D 1) (tau0 D 0) x y t := by
  have hs := logs_smooth D h0 hD 0
  have hz := extension_zero D h0 hD
  have hu : cu (extF D 0) (extG D 0)=(2 : ℝ) • (sx (logF D 0)-sx (logG D 0)) := by
    change 2*sx (logF D 0-logG D 0)=(2 : ℝ) • (sx (logF D 0)-sx (logG D 0))
    rw [c02_sx_sub _ _ hs.1 hs.2]
    funext x y t
    simp only [Pi.mul_apply,Pi.smul_apply,smul_eq_mul,c02_ofNat_apply]
  have hv : cv (extF D 0) (extG D 0)=(2 : ℝ) • (sy (sx (logF D 0))+sy (sx (logG D 0))) := by
    change 2*sx (sy (logF D 0+logG D 0))=_
    rw [← c02_sy_sx _ (c02_smooth_add hs.1 hs.2),c02_sx_add _ _ hs.1 hs.2,
      c02_sy_add _ _ (c02_smooth_sx hs.1) (c02_smooth_sx hs.2)]
    funext x y t
    simp only [Pi.mul_apply,Pi.smul_apply,smul_eq_mul,c02_ofNat_apply]
  rw [hz.1,hz.2] at hu hv
  constructor
  · rw [hu]
    rfl
  · rw [hv]
    rfl

theorem box_transfer (e f : ℝ → XYT) (h0 : ℝ) (hh0 : 0<h0)
    (he : UniformBoxO2 e) (hef : ∀ h, 0<h → h<h0 → e h=f h) : UniformBoxO2 f := by
  intro R hR
  obtain ⟨C,hC,d,hd,hb⟩ := he R hR
  refine ⟨C,hC,min d h0,lt_min hd hh0,?_⟩
  intro h x y t hh hhd hx hy ht
  rw [← hef h hh (lt_of_lt_of_le hhd (min_le_right _ _))]
  exact hb h x y t hh (lt_of_lt_of_le hhd (min_le_left _ _)) hx hy ht

end GramInterpolation

theorem c22_proved : C22 := by
  intro N D h0 hD
  have H := CenteredFamily.uniform_fields (GramInterpolation.fullA D) (GramInterpolation.fullB D)
    (fun z => (GramInterpolation.jets_analytic D h0 hD z).1)
    (fun z => (GramInterpolation.jets_analytic D h0 hD z).2)
    (fun h z => congrFun (congrFun (congrFun (GramInterpolation.jets_even D h).1 z.1) z.2.1) z.2.2)
    (fun h z => congrFun (congrFun (congrFun (GramInterpolation.jets_even D h).2 z.1) z.2.1) z.2.2)
  constructor
  · apply GramInterpolation.box_transfer _ _ h0 hD.1 H.1
    intro h hh hhh
    funext x y t
    have he := GramInterpolation.extension_eq D h0 h hD hh hhh.le
    simp only [Pi.sub_apply,he.1,he.2]
    rw [GramInterpolation.uField_eq D h0 hD,(GramInterpolation.continuous_fields D h0 hD x y t).1]
  · apply GramInterpolation.box_transfer _ _ h0 hD.1 H.2
    intro h hh hhh
    funext x y t
    have he := GramInterpolation.extension_eq D h0 h hD hh hhh.le
    simp only [Pi.sub_apply,he.1,he.2]
    rw [GramInterpolation.vField_eq D h0 hD h x y t (ne_of_gt hh),
      (GramInterpolation.continuous_fields D h0 hD x y t).2]

#print axioms c22_proved
end DLWContract
