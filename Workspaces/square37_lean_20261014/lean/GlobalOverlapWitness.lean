import PackingGeometry
import Mathlib.Tactic.LinearCombination

/-! Sound orientation-aware rejection of whole real parameter windows.
A rational point strictly inside two real unit squares is a geometric rejection
certificate. Every direction has independent real coordinates; no sign or
common-angle condition is imposed. This is a local rejection rule, not an
exhaustive exclusion of all global windows. -/
namespace SquarePacking37.OverlapWitness
open PackingGeometry
noncomputable section

theorem unit_components (s : Square) (hs : s.IsUnit) :
    |s.ux| ≤ 1 ∧ |s.uy| ≤ 1 := by
  unfold Square.IsUnit at hs
  constructor <;> apply abs_le.mpr <;> constructor <;>
    nlinarith [sq_nonneg s.ux, sq_nonneg s.uy]

theorem inside_of_inverse_bounds (s : Square) (hs : s.IsUnit) (p : Point)
    (ha : |s.ux*(p.1-s.cx)+s.uy*(p.2-s.cy)| < 1/2)
    (hb : |-s.uy*(p.1-s.cx)+s.ux*(p.2-s.cy)| < 1/2) : s.inside p := by
  refine ⟨s.ux*(p.1-s.cx)+s.uy*(p.2-s.cy),
    -s.uy*(p.1-s.cx)+s.ux*(p.2-s.cy), ha, hb, ?_⟩
  apply Prod.ext
  · change p.1 = s.cx+(s.ux*(p.1-s.cx)+s.uy*(p.2-s.cy))*s.ux -
      (-s.uy*(p.1-s.cx)+s.ux*(p.2-s.cy))*s.uy
    calc
      _ = s.cx+(s.ux^2+s.uy^2)*(p.1-s.cx) := by rw [hs]; ring
      _ = _ := by ring
  · change p.2 = s.cy+(s.ux*(p.1-s.cx)+s.uy*(p.2-s.cy))*s.uy +
      (-s.uy*(p.1-s.cx)+s.ux*(p.2-s.cy))*s.ux
    calc
      _ = s.cy+(s.ux^2+s.uy^2)*(p.2-s.cy) := by rw [hs]; ring
      _ = _ := by ring

theorem product_error (u u0 x x0 d e : ℝ)
    (hu : |u| ≤ 1) (hdu : |u-u0| ≤ e) (hdx : |x-x0| ≤ d) :
    |u*x-u0*x0| ≤ d+e*|x0| := by
  have h₁ := mul_le_mul hu hdx (abs_nonneg (x-x0)) (by norm_num : (0:ℝ) ≤ 1)
  have h₂ := mul_le_mul_of_nonneg_right hdu (abs_nonneg x0)
  calc
    |u*x-u0*x0| = |u*(x-x0)+(u-u0)*x0| := by congr 1; ring
    _ ≤ |u*(x-x0)|+|(u-u0)*x0| := abs_add_le _ _
    _ = |u| * |x-x0| + |u-u0| * |x0| := by rw [abs_mul, abs_mul]
    _ ≤ d+e*|x0| := by linarith

theorem linear_form_enclosure (u v u0 v0 x y x0 y0 d e : ℝ)
    (hu : |u| ≤ 1) (hv : |v| ≤ 1)
    (hdu : |u-u0| ≤ e) (hdv : |v-v0| ≤ e)
    (hdx : |x-x0| ≤ d) (hdy : |y-y0| ≤ d) :
    |u*x+v*y| ≤ |u0*x0+v0*y0|+2*d+e*(|x0|+|y0|) := by
  have h₁ := product_error u u0 x x0 d e hu hdu hdx
  have h₂ := product_error v v0 y y0 d e hv hdv hdy
  calc
    |u*x+v*y| = |(u0*x0+v0*y0)+((u*x-u0*x0)+(v*y-v0*y0))| := by congr 1; ring
    _ ≤ |u0*x0+v0*y0|+|((u*x-u0*x0)+(v*y-v0*y0))| := abs_add_le _ _
    _ ≤ |u0*x0+v0*y0|+(|u*x-u0*x0|+|v*y-v0*y0|) := by
      have ht := abs_add_le (u*x-u0*x0) (v*y-v0*y0)
      linarith
    _ ≤ _ := by nlinarith

structure Window where
  cx : ℚ
  cy : ℚ
  ux : ℚ
  uy : ℚ
  centerError : ℚ
  directionError : ℚ

def Fits (w : Window) (s : Square) : Prop :=
  |s.cx-(w.cx:ℝ)| ≤ w.centerError ∧ |s.cy-(w.cy:ℝ)| ≤ w.centerError ∧
  |s.ux-(w.ux:ℝ)| ≤ w.directionError ∧ |s.uy-(w.uy:ℝ)| ≤ w.directionError

def PointCertificate (w : Window) (px py : ℚ) : Prop :=
  |w.ux*(px-w.cx)+w.uy*(py-w.cy)|+2*w.centerError+
      w.directionError*(|px-w.cx|+|py-w.cy|) < 1/2 ∧
  |-w.uy*(px-w.cx)+w.ux*(py-w.cy)|+2*w.centerError+
      w.directionError*(|px-w.cx|+|py-w.cy|) < 1/2

theorem point_certificate_sound (w : Window) (px py : ℚ)
    (hcert : PointCertificate w px py) (s : Square) (hs : s.IsUnit)
    (hfit : Fits w s) : s.inside ((px:ℝ),(py:ℝ)) := by
  obtain ⟨hcx,hcy,hux,huy⟩ := hfit
  have hu := unit_components s hs
  have hx : |((px:ℝ)-s.cx)-((px:ℝ)-w.cx)| ≤ w.centerError := by
    convert hcx using 1
    rw [show (px:ℝ)-s.cx-((px:ℝ)-w.cx) = -(s.cx-w.cx) by ring, abs_neg]
  have hy : |((py:ℝ)-s.cy)-((py:ℝ)-w.cy)| ≤ w.centerError := by
    convert hcy using 1
    rw [show (py:ℝ)-s.cy-((py:ℝ)-w.cy) = -(s.cy-w.cy) by ring, abs_neg]
  have hnuy : |-s.uy-(-(w.uy:ℝ))| ≤ w.directionError := by
    simpa only [neg_sub_neg, abs_sub_comm] using huy
  have ha := linear_form_enclosure s.ux s.uy w.ux w.uy
    ((px:ℝ)-s.cx) ((py:ℝ)-s.cy) ((px:ℝ)-w.cx) ((py:ℝ)-w.cy)
    w.centerError w.directionError hu.1 hu.2 hux huy hx hy
  have hb := linear_form_enclosure (-s.uy) s.ux (-w.uy) w.ux
    ((px:ℝ)-s.cx) ((py:ℝ)-s.cy) ((px:ℝ)-w.cx) ((py:ℝ)-w.cy)
    w.centerError w.directionError (by simpa using hu.2) hu.1 hnuy hux hx hy
  apply inside_of_inverse_bounds s hs
  · apply lt_of_le_of_lt ha
    have hca := (Rat.cast_lt (K := ℝ)).mpr hcert.1
    norm_num only [Rat.cast_add, Rat.cast_sub, Rat.cast_mul, Rat.cast_neg,
      Rat.cast_abs, Rat.cast_div, Rat.cast_ofNat, Rat.cast_one] at hca
    exact hca
  · apply lt_of_le_of_lt hb
    have hcb := (Rat.cast_lt (K := ℝ)).mpr hcert.2
    norm_num only [Rat.cast_add, Rat.cast_sub, Rat.cast_mul, Rat.cast_neg,
      Rat.cast_abs, Rat.cast_div, Rat.cast_ofNat, Rat.cast_one] at hcb
    exact hcb

theorem rejects_packing_window {n : ℕ} (L : ℝ) (squares : Fin n → Square)
    (i j : Fin n) (hij : i < j) (wi wj : Window) (px py : ℚ)
    (hi : Fits wi (squares i)) (hj : Fits wj (squares j))
    (hci : PointCertificate wi px py) (hcj : PointCertificate wj px py) :
    ¬ IsPacking L squares := by
  intro hp
  exact hp.2.2 i j hij ((px:ℝ),(py:ℝ))
    ⟨point_certificate_sound wi px py hci _ (hp.1 i) hi,
     point_certificate_sound wj px py hcj _ (hp.1 j) hj⟩

-- Concrete direction-aware rejection: the nominal centres are 5/4 apart,
-- so the centre-distance >= 1 test alone cannot reject this pair. Windows
-- with unit directions near (20/29,21/29), however, all contain the common point.
def exampleLeft : Window := ⟨1,1,20/29,21/29,1/1000,1/1000⟩
def exampleRight : Window := ⟨9/4,1,20/29,21/29,1/1000,1/1000⟩

theorem example_left_certificate : PointCertificate exampleLeft (13/8) 1 := by
  norm_num [PointCertificate, exampleLeft]

theorem example_right_certificate : PointCertificate exampleRight (13/8) 1 := by
  norm_num [PointCertificate, exampleRight]

theorem example_windows_are_nonempty :
    ∃ s t : Square, s.IsUnit ∧ t.IsUnit ∧ Fits exampleLeft s ∧ Fits exampleRight t ∧
      1 < (s.cx-t.cx)^2+(s.cy-t.cy)^2 := by
  refine ⟨⟨1,1,20/29,21/29⟩,⟨9/4,1,20/29,21/29⟩, ?_⟩
  norm_num [Square.IsUnit, Fits, exampleLeft, exampleRight]

#print axioms inside_of_inverse_bounds
#print axioms point_certificate_sound
#print axioms rejects_packing_window
#print axioms example_left_certificate
#print axioms example_windows_are_nonempty

end
end SquarePacking37.OverlapWitness
