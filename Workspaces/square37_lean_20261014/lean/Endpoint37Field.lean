import CantrellAngle
import Mathlib.Data.Rat.Cast.Order

/-! Sound rational interval evaluation at the exact algebraic crossing.
Lists store polynomial coefficients in ascending degree (constant first).
Thus evalPoly [a,b,c] = a + q*(b + q*c). Source JSON descending lists must
be reversed by the generator before applying these interval lemmas.
All interval arithmetic is ordinary rational arithmetic checked by Lean. -/
namespace Endpoint37
noncomputable section

abbrev q : ℝ := Cantrell37.Angle.root

def lo : ℚ := 3847314469214599/10000000000000000
def hi : ℚ := 3847314469214600/10000000000000000

theorem q_bounds : (lo:ℝ) ≤ q ∧ q ≤ (hi:ℝ) := by
  constructor
  · simpa [lo,Cantrell37.Angle.lowerQ] using Cantrell37.Angle.root_spec.1.1
  · simpa [hi,Cantrell37.Angle.upperQ] using Cantrell37.Angle.root_spec.1.2

theorem q_nonneg : 0 ≤ q := le_trans (by norm_num [lo]) q_bounds.1

theorem root_degree8 : 7*q^8+44*q^6+66*q^4-4*q^2-1=0 := by
  have hp := Cantrell37.Angle.root_spec.2
  rw [Cantrell37.Angle.polynomial_expanded] at hp
  have hb : 4*q^4+12*q^2=Real.sqrt 2*(1+q^2)^2 := by linarith
  have hs : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  have hh : (4*q^4+12*q^2)^2=2*(1+q^2)^4 := by
    rw [hb,mul_pow,hs]
    ring
  linear_combination (1/2)*hh

def evalPoly : List ℚ → ℝ
  | [] => 0
  | a::cs => (a:ℝ)+q*evalPoly cs

def lowerBound : List ℚ → ℚ
  | [] => 0
  | a::cs => a+min (lo*lowerBound cs) (hi*lowerBound cs)

def upperBound : List ℚ → ℚ
  | [] => 0
  | a::cs => a+max (lo*upperBound cs) (hi*upperBound cs)

theorem product_lower (l u x a v : ℝ) (hl : l ≤ x) (hu : x ≤ u)
    (hx : 0 ≤ x) (ha : a ≤ v) : min (l*a) (u*a) ≤ x*v := by
  have hv := mul_le_mul_of_nonneg_left ha hx
  by_cases hapos : 0 ≤ a
  · exact le_trans (min_le_left _ _) (le_trans (mul_le_mul_of_nonneg_right hl hapos) hv)
  · have haneg : a ≤ 0 := le_of_not_ge hapos
    exact le_trans (min_le_right _ _) (le_trans (mul_le_mul_of_nonpos_right hu haneg) hv)

theorem product_upper (l u x a v : ℝ) (hl : l ≤ x) (hu : x ≤ u)
    (hx : 0 ≤ x) (ha : v ≤ a) : x*v ≤ max (l*a) (u*a) := by
  have hv := mul_le_mul_of_nonneg_left ha hx
  by_cases hapos : 0 ≤ a
  · exact le_trans hv (le_trans (mul_le_mul_of_nonneg_right hu hapos) (le_max_right _ _))
  · have haneg : a ≤ 0 := le_of_not_ge hapos
    exact le_trans hv (le_trans (mul_le_mul_of_nonpos_right hl haneg) (le_max_left _ _))

theorem bounds_sound (cs : List ℚ) :
    (lowerBound cs:ℝ) ≤ evalPoly cs ∧ evalPoly cs ≤ (upperBound cs:ℝ) := by
  induction cs with
  | nil => norm_num [lowerBound,upperBound,evalPoly]
  | cons a cs ih =>
    have hl := product_lower (lo:ℝ) (hi:ℝ) q (lowerBound cs:ℝ) (evalPoly cs)
      q_bounds.1 q_bounds.2 q_nonneg ih.1
    have hu := product_upper (lo:ℝ) (hi:ℝ) q (upperBound cs:ℝ) (evalPoly cs)
      q_bounds.1 q_bounds.2 q_nonneg ih.2
    constructor
    · simpa only [lowerBound,evalPoly,Rat.cast_add,Rat.cast_mul,Rat.cast_min] using add_le_add_left hl (a:ℝ)
    · simpa only [upperBound,evalPoly,Rat.cast_add,Rat.cast_mul,Rat.cast_max] using add_le_add_left hu (a:ℝ)

theorem poly_nonneg (cs : List ℚ) (h : 0 ≤ lowerBound cs) : 0 ≤ evalPoly cs := by
  have hc : (0:ℝ) ≤ (lowerBound cs:ℝ) := by exact_mod_cast h
  exact le_trans hc (bounds_sound cs).1

theorem poly_pos (cs : List ℚ) (h : 0 < lowerBound cs) : 0 < evalPoly cs := by
  have hc : (0:ℝ) < (lowerBound cs:ℝ) := by exact_mod_cast h
  exact lt_of_lt_of_le hc (bounds_sound cs).1

#print axioms root_degree8
#print axioms bounds_sound
#print axioms poly_nonneg
#print axioms poly_pos

end
end Endpoint37
