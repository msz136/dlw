import CantrellAngle
import CantrellBranch

/-! The proved endpoint bound applies to the explicit support class only.
It is not the unrestricted packing lower bound in ResearchTarget.lean. -/
namespace Cantrell37
noncomputable section

theorem crossing_parameter_range :
    19/50 ≤ Angle.root ∧ Angle.root ≤ 2/5 := by
  constructor
  · exact le_trans (by norm_num [Angle.lowerQ]) Angle.root_spec.1.1
  · exact le_trans Angle.root_spec.1.2 (by norm_num [Angle.upperQ])

theorem crossing_first_value : Minimax.first Angle.root=candidateSide :=
  Angle.side_root_eq_candidate

theorem crossing_values_equal : Minimax.first Angle.root=Minimax.second Angle.root := by
  have hq0 : 0 ≤ Angle.root := by linarith [crossing_parameter_range.1]
  have hqhalf : Angle.root ≤ 1/2 := by linarith [crossing_parameter_range.2]
  have he := Minimax.first_den_pos Angle.root hq0 hqhalf
  have hb := Minimax.second_den_pos Angle.root hq0 hqhalf
  unfold Minimax.first Minimax.second
  apply (div_eq_div_iff (ne_of_gt he) (ne_of_gt hb)).2
  have hid : (7+10*Angle.root-Angle.root^2)*Minimax.secondDenominator Angle.root -
      Minimax.secondNumerator (Real.sqrt 2) Angle.root*(1+2*Angle.root-Angle.root^2) =
      Angle.polynomial Angle.root*(1+2*Angle.root-Angle.root^2) := by
    unfold Minimax.secondDenominator Minimax.secondNumerator Angle.polynomial
    ring
  rw [Angle.root_spec.2, zero_mul] at hid
  exact sub_eq_zero.mp hid

theorem support_model_minimum (q : ℝ) (hq0 : 0 ≤ q)
    (hqU : q ≤ Real.sqrt 2-1) :
    candidateSide ≤ max (Minimax.first q) (Minimax.second q) := by
  have h := Minimax.crossing_minimax Angle.root q crossing_parameter_range.1
    crossing_parameter_range.2 hq0 hqU crossing_values_equal
  rw [← crossing_values_equal, max_self, crossing_first_value] at h
  exact h

theorem support_model_attains_minimum :
    ∃ q : ℝ, 0 ≤ q ∧ q ≤ Real.sqrt 2-1 ∧
      Minimax.first q=candidateSide ∧ Minimax.second q=candidateSide := by
  refine ⟨Angle.root, ?_, ?_, crossing_first_value, ?_⟩
  · linarith [crossing_parameter_range.1]
  · linarith [crossing_parameter_range.2, Minimax.sqrt_two_bounds.1]
  · rw [← crossing_values_equal, crossing_first_value]

/-- Conditional lower bound for every direction and every coordinate array
satisfying the displayed primitive support conditions. The arrays are labelled
with the one-based source indices. This statement does not assert that every
packing admits those labels and support inequalities. -/
theorem conditional_branch_lower_bound (L c s : ℝ) (x y : ℕ → ℝ)
    (hs : 0 ≤ s) (hsc : s ≤ c) (hu : c^2+s^2=1)
    (hfirst : FirstChain L c s x y)
    (hleft : LeftBrace L c s x y) (hright : RightBrace L c s x y)
    (h13 : Real.sqrt 2/2+c ≤ x 36+y 36-(x 13+y 13))
    (h22 : Real.sqrt 2/2+c ≤ x 22+y 22-(x 36+y 36)) :
    candidateSide ≤ L := by
  obtain ⟨q,hq0,hqU,hcq,hsq⟩ := Angle.half_angle_representation c s hs hsc hu
  have hcB : Branch.c q=c := hcq
  have hsB : Branch.s q=s := hsq
  have h := Branch.geometric_branch_lower_bound L Angle.root q x y
    crossing_parameter_range.1 crossing_parameter_range.2 hq0 hqU crossing_values_equal
    (by simpa only [hcB, hsB] using hfirst)
    (by simpa only [hcB, hsB] using hleft)
    (by simpa only [hcB, hsB] using hright)
    (by simpa only [hcB, hsB] using h13)
    (by simpa only [hcB, hsB] using h22)
  rw [crossing_first_value] at h
  exact h

#print axioms support_model_minimum
#print axioms support_model_attains_minimum
#print axioms conditional_branch_lower_bound

end
end Cantrell37
