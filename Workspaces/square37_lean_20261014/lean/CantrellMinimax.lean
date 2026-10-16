import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Positivity

/-! Conditional minimax theorem for the two selected Cantrell support bounds.
No assertion here forces an arbitrary packing to have this support branch. -/
namespace Cantrell37.Minimax
noncomputable section

def first (q : ℝ) : ℝ := (7+10*q-q^2)/(1+2*q-q^2)

def secondNumerator (r q : ℝ) : ℝ :=
  r*q^4-2*q^4-20*q^3+2*r*q^2-28*q^2+20*q+r+14

def secondDenominator (q : ℝ) : ℝ := 2*(q-1)*(q+1)*(q^2-2*q-1)

def second (q : ℝ) : ℝ := secondNumerator (Real.sqrt 2) q / secondDenominator q

theorem sqrt_two_bounds : (7:ℝ)/5 ≤ Real.sqrt 2 ∧ Real.sqrt 2 ≤ 3/2 := by
  have hs : (Real.sqrt 2)^2=2 := Real.sq_sqrt (by norm_num)
  have hn := Real.sqrt_nonneg (2:ℝ)
  constructor <;> nlinarith

theorem first_den_pos (q : ℝ) (hq0 : 0 ≤ q) (hqU : q ≤ 1/2) :
    0 < 1+2*q-q^2 := by
  have hp := mul_nonneg hq0 (show 0 ≤ 2-q by linarith)
  nlinarith

theorem second_den_pos (q : ℝ) (hq0 : 0 ≤ q) (hqU : q ≤ 1/2) :
    0 < secondDenominator q := by
  have hd := first_den_pos q hq0 hqU
  have h₁ : 0 < 1-q := by linarith
  have h₂ : 0 < q+1 := by linarith
  calc
    secondDenominator q = 2*(1-q)*(q+1)*(1+2*q-q^2) := by
      unfold secondDenominator
      ring
    _ > 0 := by positivity

theorem first_increases_after_crossing (a q : ℝ) (haL : 19/50 ≤ a)
    (haU : a ≤ 2/5) (haq : a ≤ q) (hqU : q ≤ 1/2) : first a ≤ first q := by
  have ha0 : 0 ≤ a := by linarith
  have hq0 : 0 ≤ q := le_trans ha0 haq
  have hda := first_den_pos a ha0 (by linarith)
  have hdq := first_den_pos q hq0 hqU
  unfold first
  apply (div_le_div_iff₀ hda hdq).2
  have hap := mul_nonneg ha0 hq0
  have hbr : 0 ≤ 4*a*q+3*a+3*q-2 := by nlinarith
  have hprod := mul_nonneg (sub_nonneg.mpr haq) hbr
  have hid : (7+10*q-q^2)*(1+2*a-a^2)-(7+10*a-a^2)*(1+2*q-q^2) =
      2*(q-a)*(4*a*q+3*a+3*q-2) := by ring
  nlinarith

def B0 (q : ℝ) : ℝ := (2-5*q)^3
def B1 (q : ℝ) : ℝ := 3*(5*q)*(2-5*q)^2
def B2 (q : ℝ) : ℝ := 3*(5*q)^2*(2-5*q)
def B3 (q : ℝ) : ℝ := (5*q)^3

theorem basis_nonneg (q : ℝ) (hq0 : 0 ≤ q) (hqU : q ≤ 2/5) :
    0 ≤ B0 q ∧ 0 ≤ B1 q ∧ 0 ≤ B2 q ∧ 0 ≤ B3 q := by
  have hc : 0 ≤ 2-5*q := by linarith
  refine ⟨?_, ?_, ?_, ?_⟩ <;> dsimp [B0, B1, B2, B3] <;> positivity

def bernsteinWitness (r q a : ℝ) : ℝ :=
  (140625*r+140625)*B0 q*B0 a +
  (103125*r+140625)*(B0 q*B1 a+B1 q*B0 a) +
  (58125*r+110625)*(B0 q*B2 a+B2 q*B0 a) +
  (5625*r+122625)*(B0 q*B3 a+B3 q*B0 a) +
  (58125*r+150625)*B1 q*B1 a +
  (5625*r+138625)*(B1 q*B2 a+B2 q*B1 a) +
  (191025-55575*r)*(B1 q*B3 a+B3 q*B1 a) +
  (160625-55575*r)*B2 q*B2 a +
  (269745-126915*r)*(B2 q*B3 a+B3 q*B2 a) +
  (444033-208539*r)*B3 q*B3 a

theorem bernstein_nonneg (r q a : ℝ) (hrL : 7/5 ≤ r) (hrU : r ≤ 3/2)
    (hq0 : 0 ≤ q) (hqU : q ≤ 2/5) (ha0 : 0 ≤ a) (haU : a ≤ 2/5) :
    0 ≤ bernsteinWitness r q a := by
  obtain ⟨hq₀, hq₁, hq₂, hq₃⟩ := basis_nonneg q hq0 hqU
  obtain ⟨ha₀, ha₁, ha₂, ha₃⟩ := basis_nonneg a ha0 haU
  have hr0 : 0 ≤ r := by linarith
  have hc₁ : 0 ≤ 191025-55575*r := by linarith
  have hc₂ : 0 ≤ 160625-55575*r := by linarith
  have hc₃ : 0 ≤ 269745-126915*r := by linarith
  have hc₄ : 0 ≤ 444033-208539*r := by linarith
  unfold bernsteinWitness
  positivity

theorem second_difference_certificate (r q a : ℝ) :
    2250000*(secondNumerator r q*secondDenominator a -
      secondNumerator r a*secondDenominator q) =
      (a-q)*(27000000+bernsteinWitness r q a) := by
  unfold secondNumerator secondDenominator bernsteinWitness B0 B1 B2 B3
  ring

theorem second_decreases_before_crossing (a q : ℝ) (ha0 : 0 ≤ a)
    (haU : a ≤ 2/5) (hq0 : 0 ≤ q) (hqa : q ≤ a) : second a ≤ second q := by
  have hqU : q ≤ 2/5 := le_trans hqa haU
  have hda := second_den_pos a ha0 (by linarith)
  have hdq := second_den_pos q hq0 (by linarith)
  unfold second
  apply (div_le_div_iff₀ hda hdq).2
  have hw := bernstein_nonneg (Real.sqrt 2) q a sqrt_two_bounds.1 sqrt_two_bounds.2
    hq0 hqU ha0 haU
  have hprod := mul_nonneg (sub_nonneg.mpr hqa) (show 0 ≤ 27000000+bernsteinWitness (Real.sqrt 2) q a by linarith)
  have hid := second_difference_certificate (Real.sqrt 2) q a
  nlinarith

theorem crossing_minimax (a q : ℝ) (haL : 19/50 ≤ a) (haU : a ≤ 2/5)
    (hq0 : 0 ≤ q) (hqU : q ≤ Real.sqrt 2-1) (hcross : first a=second a) :
    max (first a) (second a) ≤ max (first q) (second q) := by
  have hqhalf : q ≤ 1/2 := by linarith [sqrt_two_bounds.2]
  by_cases hqa : q ≤ a
  · rw [hcross, max_self]
    exact le_trans (second_decreases_before_crossing a q (by linarith) haU hq0 hqa)
      (le_max_right _ _)
  · rw [← hcross, max_self]
    exact le_trans (first_increases_after_crossing a q haL haU (le_of_not_ge hqa) hqhalf)
      (le_max_left _ _)

#print axioms second_difference_certificate
#print axioms crossing_minimax

end
end Cantrell37.Minimax
