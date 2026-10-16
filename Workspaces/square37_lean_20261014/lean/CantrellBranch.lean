import CantrellSupports
import CantrellMinimax
import Mathlib.Tactic.FieldSimp

/-! Geometric support assumptions imply the conditional Cantrell minimax bound.
The branch assumptions remain explicit; no exhaustive classification of arbitrary
37-square packings is asserted here. -/
namespace Cantrell37.Branch
noncomputable section

def c (q : ℝ) : ℝ := (1-q^2)/(1+q^2)
def s (q : ℝ) : ℝ := 2*q/(1+q^2)

theorem denominator_pos (q : ℝ) : 0 < 1+q^2 := by positivity

theorem half_angle_unit (q : ℝ) : (c q)^2+(s q)^2=1 := by
  have hd : 1+q^2 ≠ 0 := ne_of_gt (denominator_pos q)
  unfold c s
  field_simp
  <;> ring

theorem half_angle_regime (q : ℝ) (hq0 : 0 ≤ q)
    (hqU : q ≤ Real.sqrt 2-1) : 0 ≤ s q ∧ s q ≤ c q := by
  have hd := denominator_pos q
  have hr : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  have hsum : 0 ≤ Real.sqrt 2+q+1 := by positivity
  have hp := mul_nonneg (sub_nonneg.mpr hqU) hsum
  have hn : 2*q ≤ 1-q^2 := by nlinarith
  constructor
  · unfold s; positivity
  · unfold s c
    exact (div_le_div_iff_of_pos_right hd).2 hn

theorem first_from_raw (L q : ℝ) (hq0 : 0 ≤ q) (hqU : q ≤ 1/2)
    (h : 3+4*c q+5*s q ≤ (c q+s q)*L) : Minimax.first q ≤ L := by
  have hd := denominator_pos q
  have hne : 1+q^2 ≠ 0 := ne_of_gt hd
  have hmul := mul_le_mul_of_nonneg_right h hd.le
  have hleft : (3+4*c q+5*s q)*(1+q^2)=7+10*q-q^2 := by
    unfold c s
    field_simp
    <;> ring
  have hright : (c q+s q)*L*(1+q^2)=(1+2*q-q^2)*L := by
    unfold c s
    field_simp
    <;> ring
  rw [hleft, hright] at hmul
  unfold Minimax.first
  apply (div_le_iff₀ (Minimax.first_den_pos q hq0 hqU)).2
  nlinarith [hmul]

theorem second_from_raw (L q : ℝ) (hq0 : 0 ≤ q) (hqU : q ≤ 1/2)
    (h : 6+8*c q+10*s q*(c q-s q)+Real.sqrt 2 ≤
      2*(1+s q*(c q-s q))*L) : Minimax.second q ≤ L := by
  have hd := denominator_pos q
  have hne : 1+q^2 ≠ 0 := ne_of_gt hd
  have hmul := mul_le_mul_of_nonneg_right h (sq_nonneg (1+q^2))
  have hleft : (6+8*c q+10*s q*(c q-s q)+Real.sqrt 2)*(1+q^2)^2=
      Minimax.secondNumerator (Real.sqrt 2) q := by
    unfold c s Minimax.secondNumerator
    field_simp
    <;> ring
  have hright : (2*(1+s q*(c q-s q))*L)*(1+q^2)^2=
      Minimax.secondDenominator q*L := by
    unfold c s Minimax.secondDenominator
    field_simp
    <;> ring
  rw [hleft, hright] at hmul
  unfold Minimax.second
  apply (div_le_iff₀ (Minimax.second_den_pos q hq0 hqU)).2
  nlinarith [hmul]

theorem raw_supports_lower_bound (L a q : ℝ)
    (haL : 19/50 ≤ a) (haU : a ≤ 2/5)
    (hq0 : 0 ≤ q) (hqU : q ≤ Real.sqrt 2-1)
    (hcross : Minimax.first a=Minimax.second a)
    (hfirst : 3+4*c q+5*s q ≤ (c q+s q)*L)
    (hsecond : 6+8*c q+10*s q*(c q-s q)+Real.sqrt 2 ≤
      2*(1+s q*(c q-s q))*L) : Minimax.first a ≤ L := by
  have hqhalf : q ≤ 1/2 := by linarith [Minimax.sqrt_two_bounds.2]
  have hf := first_from_raw L q hq0 hqhalf hfirst
  have hs := second_from_raw L q hq0 hqhalf hsecond
  calc
    Minimax.first a ≤ max (Minimax.first a) (Minimax.second a) := le_max_left _ _
    _ ≤ max (Minimax.first q) (Minimax.second q) :=
      Minimax.crossing_minimax a q haL haU hq0 hqU hcross
    _ ≤ L := max_le hf hs

theorem geometric_branch_lower_bound (L a q : ℝ) (x y : ℕ → ℝ)
    (haL : 19/50 ≤ a) (haU : a ≤ 2/5)
    (hq0 : 0 ≤ q) (hqU : q ≤ Real.sqrt 2-1)
    (hcross : Minimax.first a=Minimax.second a)
    (hfirst : FirstChain L (c q) (s q) x y)
    (hleft : LeftBrace L (c q) (s q) x y)
    (hright : RightBrace L (c q) (s q) x y)
    (h13 : Real.sqrt 2/2+c q ≤ x 36+y 36-(x 13+y 13))
    (h22 : Real.sqrt 2/2+c q ≤ x 22+y 22-(x 36+y 36)) :
    Minimax.first a ≤ L := by
  obtain ⟨hs,hsc⟩ := half_angle_regime q hq0 hqU
  have hc : 0 ≤ c q := le_trans hs hsc
  have hf := first_chain_bound L (c q) (s q) x y hc hs hfirst
  have hb := central_brace_bound L (c q) (s q) x y hs hsc
    (half_angle_unit q) hleft hright h13 h22
  exact raw_supports_lower_bound L a q haL haU hq0 hqU hcross hf hb

#print axioms half_angle_unit
#print axioms raw_supports_lower_bound
#print axioms geometric_branch_lower_bound

end
end Cantrell37.Branch
