import PackingGeometry
import Mathlib.Order.Fin.Basic

/-! Unrestricted consequences of IsPacking. Every square has its own unit
direction; there is no common-angle or contact-branch hypothesis. -/
namespace PackingGeometry.Global
noncomputable section

def localA (s : Square) (p : Point) : ℝ := s.ux*(p.1-s.cx)+s.uy*(p.2-s.cy)
def localB (s : Square) (p : Point) : ℝ := -s.uy*(p.1-s.cx)+s.ux*(p.2-s.cy)
def centerDistanceSq (s : Square) (p : Point) : ℝ := (p.1-s.cx)^2+(p.2-s.cy)^2

theorem local_coordinates_reconstruct (s : Square) (hs : s.IsUnit) (p : Point) :
    p = s.point (localA s p) (localB s p) := by
  apply Prod.ext
  · change p.1 = s.cx + localA s p*s.ux-localB s p*s.uy
    calc
      p.1 = s.cx+(s.ux^2+s.uy^2)*(p.1-s.cx) := by rw [hs]; ring
      _ = _ := by unfold localA localB; ring
  · change p.2 = s.cy + localA s p*s.uy+localB s p*s.ux
    calc
      p.2 = s.cy+(s.ux^2+s.uy^2)*(p.2-s.cy) := by rw [hs]; ring
      _ = _ := by unfold localA localB; ring

theorem local_coordinates_norm (s : Square) (hs : s.IsUnit) (p : Point) :
    (localA s p)^2+(localB s p)^2=centerDistanceSq s p := by
  calc
    _ = (s.ux^2+s.uy^2)*centerDistanceSq s p := by
      unfold localA localB centerDistanceSq
      ring
    _ = _ := by rw [hs,one_mul]

theorem closed_of_center_dist_sq_le (s : Square) (hs : s.IsUnit) (p : Point)
    (hp : centerDistanceSq s p ≤ 1/4) : s.closed p := by
  have he := local_coordinates_norm s hs p
  have ha : |localA s p| ≤ 1/2 := by
    nlinarith [sq_abs (localA s p), abs_nonneg (localA s p), sq_nonneg (localB s p)]
  have hb : |localB s p| ≤ 1/2 := by
    nlinarith [sq_abs (localB s p), abs_nonneg (localB s p), sq_nonneg (localA s p)]
  exact ⟨localA s p,localB s p,ha,hb,local_coordinates_reconstruct s hs p⟩

theorem inside_of_center_dist_sq_lt (s : Square) (hs : s.IsUnit) (p : Point)
    (hp : centerDistanceSq s p < 1/4) : s.inside p := by
  have he := local_coordinates_norm s hs p
  have ha : |localA s p| < 1/2 := by
    nlinarith [sq_abs (localA s p), abs_nonneg (localA s p), sq_nonneg (localB s p)]
  have hb : |localB s p| < 1/2 := by
    nlinarith [sq_abs (localB s p), abs_nonneg (localB s p), sq_nonneg (localA s p)]
  exact ⟨localA s p,localB s p,ha,hb,local_coordinates_reconstruct s hs p⟩

theorem center_bound {n : ℕ} {L : ℝ} {squares : Fin n → Square}
    (h : IsPacking L squares) (i : Fin n) :
    1/2 ≤ (squares i).cx ∧ (squares i).cx ≤ L-1/2 ∧
    1/2 ≤ (squares i).cy ∧ (squares i).cy ≤ L-1/2 := by
  have hleft := h.2.1 i ((squares i).cx-1/2,(squares i).cy)
    (closed_of_center_dist_sq_le _ (h.1 i) _ (by dsimp [centerDistanceSq]; ring_nf; norm_num))
  have hright := h.2.1 i ((squares i).cx+1/2,(squares i).cy)
    (closed_of_center_dist_sq_le _ (h.1 i) _ (by dsimp [centerDistanceSq]; ring_nf; norm_num))
  have hbottom := h.2.1 i ((squares i).cx,(squares i).cy-1/2)
    (closed_of_center_dist_sq_le _ (h.1 i) _ (by dsimp [centerDistanceSq]; ring_nf; norm_num))
  have htop := h.2.1 i ((squares i).cx,(squares i).cy+1/2)
    (closed_of_center_dist_sq_le _ (h.1 i) _ (by dsimp [centerDistanceSq]; ring_nf; norm_num))
  dsimp [InContainer] at hleft hright hbottom htop
  constructor
  · linarith [hleft.1]
  constructor
  · linarith [hright.2.1]
  constructor
  · linarith [hbottom.2.2.1]
  · linarith [htop.2.2.2]

theorem centers_distance_sq {n : ℕ} {L : ℝ} {squares : Fin n → Square}
    (h : IsPacking L squares) (i j : Fin n) (hij : i ≠ j) :
    1 ≤ ((squares i).cx-(squares j).cx)^2+((squares i).cy-(squares j).cy)^2 := by
  by_contra hn
  have hd : ((squares i).cx-(squares j).cx)^2+((squares i).cy-(squares j).cy)^2 < 1 :=
    lt_of_not_ge hn
  let midpoint : Point := (((squares i).cx+(squares j).cx)/2,
    ((squares i).cy+(squares j).cy)/2)
  have hi : (squares i).inside midpoint := by
    apply inside_of_center_dist_sq_lt _ (h.1 i)
    dsimp [centerDistanceSq,midpoint]
    nlinarith [hd]
  have hj : (squares j).inside midpoint := by
    apply inside_of_center_dist_sq_lt _ (h.1 j)
    dsimp [centerDistanceSq,midpoint]
    nlinarith [hd]
  rcases lt_or_gt_of_ne hij with hij' | hji'
  · exact h.2.2 i j hij' midpoint ⟨hi,hj⟩
  · exact h.2.2 j i hji' midpoint ⟨hj,hi⟩

#print axioms closed_of_center_dist_sq_le
#print axioms inside_of_center_dist_sq_lt
#print axioms center_bound
#print axioms centers_distance_sq

end
end PackingGeometry.Global
