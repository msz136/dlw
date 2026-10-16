import CantrellAlgebra
import Mathlib.Tactic.LinearCombination

/-! Necessary bounds for an explicitly selected Cantrell contact branch.
All directed support assumptions are visible below. Nothing in this file
asserts that arbitrary 37-square packings satisfy those assumptions.
The natural-number indices are the one-based source certificate labels. -/
namespace Cantrell37
noncomputable section

structure FirstChain (L c s : ℝ) (x y : ℕ → ℝ) : Prop where
  x1 : 1/2 ≤ x 1
  x4 : 1 ≤ x 4 - x 1
  x6 : 1 ≤ x 6 - x 4
  y6 : y 6 ≤ L-1/2
  p6_23 : (1+c+s)/2 ≤ s*(x 23-x 6)-c*(y 23-y 6)
  p23_22 : 1 ≤ s*(x 22-x 23)-c*(y 22-y 23)
  p22_24 : 1 ≤ s*(x 24-x 22)-c*(y 24-y 22)
  p24_31 : (1+c+s)/2 ≤ s*(x 31-x 24)-c*(y 31-y 24)
  x26 : x 26 ≤ L-1/2
  x31 : 1 ≤ x 26-x 31
  y29 : 1/2 ≤ y 29
  y30 : 1 ≤ y 30-y 29
  y31 : 1 ≤ y 31-y 30

theorem first_chain_bound (L c s : ℝ) (x y : ℕ → ℝ)
    (hc : 0 ≤ c) (hs : 0 ≤ s) (h : FirstChain L c s x y) :
    3+4*c+5*s ≤ (c+s)*L := by
  have hx : x 31-x 6 ≤ L-4 := by
    linarith [h.x1, h.x4, h.x6, h.x26, h.x31]
  have hy : y 6-y 31 ≤ L-3 := by
    linarith [h.y6, h.y29, h.y30, h.y31]
  have hxs := mul_le_mul_of_nonneg_left hx hs
  have hyc := mul_le_mul_of_nonneg_left hy hc
  have ht : 3+c+s ≤ s*(x 31-x 6)+c*(y 6-y 31) := by
    linarith [h.p6_23, h.p23_22, h.p22_24, h.p24_31]
  nlinarith

structure LeftBrace (L c s : ℝ) (x y : ℕ → ℝ) : Prop where
  x8 : 1/2 ≤ x 8
  y8 : 3/2 ≤ y 8
  x3 : 1/2 ≤ x 3
  y3 : y 3 ≤ L-5/2
  p8_11 : (1+c+s)/2 ≤ s*(x 11-x 8)+c*(y 11-y 8)
  p11_13 : 1 ≤ s*(x 13-x 11)+c*(y 13-y 11)
  p3_14 : (1+c+s)/2 ≤ c*(x 14-x 3)-s*(y 14-y 3)
  p14_13 : 1 ≤ c*(x 13-x 14)-s*(y 13-y 14)

def braceFloor (L c s : ℝ) : ℝ := 3+3*c+s*(c-s)*(5-L)

theorem left_brace_bound (L c s : ℝ) (x y : ℕ → ℝ)
    (hs : 0 ≤ s) (hsc : s ≤ c) (hu : c^2+s^2=1)
    (h : LeftBrace L c s x y) : braceFloor L c s ≤ x 13+y 13 := by
  have hc : 0 ≤ c := le_trans hs hsc
  have hU : c+3*s+3/2-s*L ≤ c*x 13-s*y 13 := by
    have hx := mul_le_mul_of_nonneg_left h.x3 hc
    have hy := mul_le_mul_of_nonneg_left h.y3 hs
    nlinarith [h.p3_14, h.p14_13]
  have hV : s+2*c+3/2 ≤ s*x 13+c*y 13 := by
    have hx := mul_le_mul_of_nonneg_left h.x8 hs
    have hy := mul_le_mul_of_nonneg_left h.y8 hc
    nlinarith [h.p8_11, h.p11_13]
  have hwU := mul_le_mul_of_nonneg_left hU (sub_nonneg.mpr hsc)
  have hwV := mul_le_mul_of_nonneg_left hV (add_nonneg hc hs)
  have hid : (c-s)*(c*x 13-s*y 13)+(c+s)*(s*x 13+c*y 13) =
      x 13+y 13 := by
    calc
      _ = (c^2+s^2)*(x 13+y 13) := by ring
      _ = _ := by rw [hu, one_mul]
  have hlo : (c-s)*(c+3*s+3/2-s*L)+(c+s)*(s+2*c+3/2) =
      braceFloor L c s := by
    unfold braceFloor
    linear_combination 3*hu
  linarith

/- The reflected half is expressed by an explicit coordinate substitution.
This retains every primitive assumption and avoids assuming symmetry of the
actual packing. Only the selected inequalities of the reflected half are used. -/
def reflectedX (L : ℝ) (y : ℕ → ℝ) : ℕ → ℝ := fun i => L-y i
def reflectedY (L : ℝ) (x : ℕ → ℝ) : ℕ → ℝ := fun i => L-x i
def rightLabels (i : ℕ) : ℕ :=
  if i=8 then 17 else if i=11 then 20 else if i=13 then 22
  else if i=3 then 6 else if i=14 then 23 else i

def RightBrace (L c s : ℝ) (x y : ℕ → ℝ) : Prop :=
  LeftBrace L c s (fun i => reflectedX L y (rightLabels i))
    (fun i => reflectedY L x (rightLabels i))

theorem right_brace_bound (L c s : ℝ) (x y : ℕ → ℝ)
    (hs : 0 ≤ s) (hsc : s ≤ c) (hu : c^2+s^2=1)
    (h : RightBrace L c s x y) : x 22+y 22 ≤ 2*L-braceFloor L c s := by
  have hr := left_brace_bound L c s _ _ hs hsc hu h
  norm_num [reflectedX, reflectedY, rightLabels] at hr
  linarith

theorem central_brace_bound (L c s : ℝ) (x y : ℕ → ℝ)
    (hs : 0 ≤ s) (hsc : s ≤ c) (hu : c^2+s^2=1)
    (hl : LeftBrace L c s x y) (hr : RightBrace L c s x y)
    (h13 : Real.sqrt 2/2+c ≤ x 36+y 36-(x 13+y 13))
    (h22 : Real.sqrt 2/2+c ≤ x 22+y 22-(x 36+y 36)) :
    6+8*c+10*s*(c-s)+Real.sqrt 2 ≤ 2*(1+s*(c-s))*L := by
  have hleft := left_brace_bound L c s x y hs hsc hu hl
  have hright := right_brace_bound L c s x y hs hsc hu hr
  unfold braceFloor at hleft hright
  nlinarith

theorem quadratic_common_root (a b c d e f t : ℝ)
    (h₁ : a*t^2+b*t+c=0) (h₂ : d*t^2+e*t+f=0) :
    (a*f-c*d)^2-(a*e-b*d)*(b*f-c*e)=0 := by
  have hlin : (a*e-b*d)*t+(a*f-c*d)=0 := by
    linear_combination a*h₂-d*h₁
  have hquad : (a*e-b*d)*t^2-(b*f-c*e)=0 := by
    linear_combination e*h₁-b*h₂
  calc
    _ = ((a*e-b*d)*t+(a*f-c*d))*
        ((a*f-c*d)-(a*e-b*d)*t) +
        (a*e-b*d)*((a*e-b*d)*t^2-(b*f-c*e)) := by ring
    _ = 0 := by rw [hlin, hquad]; ring

theorem crossing_eliminant (L t r : ℝ) (hr : r^2=2)
    (hf : ((2*L-9)^2+1)*t^2-12*(2*L-9)*t+34=0)
    (hg : 2*(L-5)^2*t^2-14*(L-5)*t+20+r=0) :
    (24-16*r)*(rationalPart L+r*radicalPart L)=0 := by
  have he := quadratic_common_root ((2*L-9)^2+1) (-12*(2*L-9)) 34
    (2*(L-5)^2) (-14*(L-5)) (20+r) t (by nlinarith [hf]) (by nlinarith [hg])
  unfold rationalPart radicalPart
  linear_combination he - (((2*L-9)^2+1)^2 +
    16*(-64*L^3+850*L^2-3658*L+5502))*hr

theorem crossing_is_quartic_root (L t : ℝ)
    (hf : ((2*L-9)^2+1)*t^2-12*(2*L-9)*t+34=0)
    (hg : 2*(L-5)^2*t^2-14*(L-5)*t+20+Real.sqrt 2=0) :
    quartic L=0 := by
  have hr : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  have he := crossing_eliminant L t (Real.sqrt 2) hr hf hg
  have hne : 24-16*Real.sqrt 2 ≠ 0 := by
    intro h
    nlinarith
  exact (mul_eq_zero.mp he).resolve_left hne

theorem support_equalities_give_crossing (L c s r : ℝ)
    (hu : c^2+s^2=1)
    (hfirst : 3+4*c+5*s=(c+s)*L)
    (hsecond : 6+8*c+10*s*(c-s)+r=2*(1+s*(c-s))*L) :
    (((2*L-9)^2+1)*(c+s)^2-12*(2*L-9)*(c+s)+34=0) ∧
    (2*(L-5)^2*(c+s)^2-14*(L-5)*(c+s)+20+r=0) := by
  let t := c+s
  let d := c-s
  have htd : t^2+d^2=2 := by dsimp [t, d]; nlinarith [hu]
  have hd : d=6-(2*L-9)*t := by dsimp [t, d]; nlinarith [hfirst]
  have hf : ((2*L-9)^2+1)*t^2-12*(2*L-9)*t+34=0 := by
    calc
      _ = t^2+(6-(2*L-9)*t)^2-2 := by ring
      _ = 0 := by rw [← hd]; linarith
  have hb : 6+4*(t+d)+5*(t-d)*d+r-2*(1+(t-d)*d/2)*L=0 := by
    dsimp [t, d]
    nlinarith [hsecond]
  have hg : 2*(L-5)^2*t^2-14*(L-5)*t+20+r=0 := by
    rw [hd] at hb
    linear_combination hb-(L-5)*hf
  exact ⟨hf, hg⟩

theorem support_equalities_identify_candidate (L c s : ℝ)
    (hL : L ∈ Set.Icc lower upper) (hu : c^2+s^2=1)
    (hfirst : 3+4*c+5*s=(c+s)*L)
    (hsecond : 6+8*c+10*s*(c-s)+Real.sqrt 2=2*(1+s*(c-s))*L) :
    L=candidateSide := by
  obtain ⟨hf, hg⟩ := support_equalities_give_crossing L c s (Real.sqrt 2)
    hu hfirst hsecond
  have hp := quartic_root_is_polynomial_root L (crossing_is_quartic_root L (c+s) hf hg)
  exact (Classical.choose_spec isolated_root_exists_unique).2 L ⟨hL, hp⟩

#print axioms first_chain_bound
#print axioms central_brace_bound
#print axioms crossing_eliminant
#print axioms crossing_is_quartic_root
#print axioms support_equalities_identify_candidate

end
end Cantrell37
