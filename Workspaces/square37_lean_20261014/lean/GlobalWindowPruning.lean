import GlobalOverlapWitness

/-! Necessary wall and unit-circle constraints for arbitrary directions.
These certified pruning rules never assume the Cantrell contact pattern. -/
namespace SquarePacking37.WindowPruning
open PackingGeometry OverlapWitness
noncomputable section

theorem containment_bounds_necessary (s : Square) (L : ℝ)
    (h : ∀ p, s.closed p → InContainer L p) :
    (|s.ux|+|s.uy|)/2 ≤ s.cx ∧ s.cx+(|s.ux|+|s.uy|)/2 ≤ L ∧
    (|s.ux|+|s.uy|)/2 ≤ s.cy ∧ s.cy+(|s.ux|+|s.uy|)/2 ≤ L := by
  have hpp := h (s.point (1/2) (1/2)) ⟨1/2,1/2,by norm_num,by norm_num,rfl⟩
  have hpm := h (s.point (1/2) (-1/2)) ⟨1/2,-1/2,by norm_num,by norm_num,rfl⟩
  have hmp := h (s.point (-1/2) (1/2)) ⟨-1/2,1/2,by norm_num,by norm_num,rfl⟩
  have hmm := h (s.point (-1/2) (-1/2)) ⟨-1/2,-1/2,by norm_num,by norm_num,rfl⟩
  dsimp [InContainer, Square.point] at hpp hpm hmp hmm
  rcases le_total 0 s.ux with hx | hx <;> rcases le_total 0 s.uy with hy | hy
  · simp only [abs_of_nonneg hx, abs_of_nonneg hy]
    constructor <;> try constructor <;> try constructor <;> linarith
  · simp only [abs_of_nonneg hx, abs_of_nonpos hy]
    constructor <;> try constructor <;> try constructor <;> linarith
  · simp only [abs_of_nonpos hx, abs_of_nonneg hy]
    constructor <;> try constructor <;> try constructor <;> linarith
  · simp only [abs_of_nonpos hx, abs_of_nonpos hy]
    constructor <;> try constructor <;> try constructor <;> linarith

theorem abs_enclosure (u u0 e : ℝ) (h : |u-u0| ≤ e) :
    |u0|-e ≤ |u| ∧ |u| ≤ |u0|+e := by
  have h₁ := abs_add_le u0 (u-u0)
  have h₂ := abs_sub_le u (u-u0)
  rw [show u0+(u-u0)=u by ring] at h₁
  rw [show u-(u-u0)=u0 by ring] at h₂
  constructor <;> linarith

def WallCertificate (w : Window) (target : ℚ) : Prop :=
  w.cx+w.centerError < (|w.ux|+|w.uy|)/2-w.directionError ∨
  target < w.cx-w.centerError+(|w.ux|+|w.uy|)/2-w.directionError ∨
  w.cy+w.centerError < (|w.ux|+|w.uy|)/2-w.directionError ∨
  target < w.cy-w.centerError+(|w.ux|+|w.uy|)/2-w.directionError

theorem wall_certificate_sound (w : Window) (target : ℚ) (L : ℝ)
    (hL : L ≤ target) (s : Square) (hf : Fits w s)
    (hw : WallCertificate w target) :
    ¬ (∀ p, s.closed p → InContainer L p) := by
  intro hcontain
  obtain ⟨hxl,hxu,hyl,hyu⟩ := containment_bounds_necessary s L hcontain
  obtain ⟨hcx,hcy,hux,huy⟩ := hf
  obtain ⟨hxlo,hxhi⟩ := abs_le.mp hcx
  obtain ⟨hylo,hyhi⟩ := abs_le.mp hcy
  have huxlo := (abs_enclosure s.ux w.ux w.directionError hux).1
  have huylo := (abs_enclosure s.uy w.uy w.directionError huy).1
  rcases hw with hw | hw | hw | hw
  all_goals
    have hr := (Rat.cast_lt (K := ℝ)).mpr hw
    norm_num only [Rat.cast_add, Rat.cast_sub, Rat.cast_mul, Rat.cast_neg,
      Rat.cast_abs, Rat.cast_div, Rat.cast_ofNat, Rat.cast_one] at hr
    linarith

def UnitCertificate (w : Window) : Prop :=
  (|w.ux|+w.directionError)^2+(|w.uy|+w.directionError)^2 < 1 ∨
  (0 ≤ |w.ux|-w.directionError ∧ 0 ≤ |w.uy|-w.directionError ∧
    1 < (|w.ux|-w.directionError)^2+(|w.uy|-w.directionError)^2)

theorem unit_certificate_sound (w : Window) (s : Square) (hf : Fits w s)
    (hc : UnitCertificate w) : ¬ s.IsUnit := by
  intro hs
  have hx := abs_enclosure s.ux w.ux w.directionError hf.2.2.1
  have hy := abs_enclosure s.uy w.uy w.directionError hf.2.2.2
  unfold Square.IsUnit at hs
  rcases hc with hc | ⟨hc0,hc1,hc2⟩
  · have hc' := (Rat.cast_lt (K := ℝ)).mpr hc
    norm_num only [Rat.cast_add, Rat.cast_abs, Rat.cast_pow, Rat.cast_one] at hc'
    have hpx := mul_nonneg (sub_nonneg.mpr hx.2)
      (show 0 ≤ |(w.ux:ℝ)|+w.directionError+|s.ux| by linarith [abs_nonneg s.ux])
    have hpy := mul_nonneg (sub_nonneg.mpr hy.2)
      (show 0 ≤ |(w.uy:ℝ)|+w.directionError+|s.uy| by linarith [abs_nonneg s.uy])
    nlinarith [sq_abs s.ux, sq_abs s.uy]
  · have hc0' := (Rat.cast_le (K := ℝ)).mpr hc0
    have hc1' := (Rat.cast_le (K := ℝ)).mpr hc1
    have hc2' := (Rat.cast_lt (K := ℝ)).mpr hc2
    norm_num only [Rat.cast_sub, Rat.cast_abs, Rat.cast_zero] at hc0' hc1'
    norm_num only [Rat.cast_sub, Rat.cast_add, Rat.cast_abs, Rat.cast_pow, Rat.cast_one] at hc2'
    have hpx := mul_nonneg (sub_nonneg.mpr hx.1)
      (show 0 ≤ |s.ux|+(|(w.ux:ℝ)|-w.directionError) by linarith [abs_nonneg s.ux])
    have hpy := mul_nonneg (sub_nonneg.mpr hy.1)
      (show 0 ≤ |s.uy|+(|(w.uy:ℝ)|-w.directionError) by linarith [abs_nonneg s.uy])
    nlinarith [sq_abs s.ux, sq_abs s.uy]

def wallDemo : Window := ⟨1/2,1,20/29,21/29,1/1000,1/1000⟩
theorem wall_demo_accepts : WallCertificate wallDemo (659/100) := by
  left
  norm_num [wallDemo]

#print axioms containment_bounds_necessary
#print axioms wall_certificate_sound
#print axioms unit_certificate_sound

end
end SquarePacking37.WindowPruning
