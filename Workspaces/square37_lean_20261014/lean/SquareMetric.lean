import PackingGeometry

namespace PackingGeometry

/-! The parameterization used for a unit square preserves Euclidean squared
distances. Thus the coefficient box [-1/2,1/2]^2 is a genuine rotated unit
square, not a weaker surrogate object. -/

theorem square_point_distance_sq (s : Square) (hs : s.IsUnit)
    (a b a' b' : ℝ) :
    ((s.point a b).1 - (s.point a' b').1)^2 +
      ((s.point a b).2 - (s.point a' b').2)^2 = (a-a')^2 + (b-b')^2 := by
  calc
    _ = (s.ux^2 + s.uy^2) * ((a-a')^2 + (b-b')^2) := by
      unfold Square.point
      ring
    _ = _ := by rw [hs, one_mul]

theorem square_parameterization_injective (s : Square) (hs : s.IsUnit)
    (a b a' b' : ℝ) (h : s.point a b = s.point a' b') : a = a' ∧ b = b' := by
  have hid := square_point_distance_sq s hs a b a' b'
  rw [h] at hid
  have h₁ := sq_nonneg (a-a')
  have h₂ := sq_nonneg (b-b')
  constructor <;> nlinarith [sq_nonneg (a-a'), sq_nonneg (b-b')]

#print axioms square_point_distance_sq
#print axioms square_parameterization_injective

end PackingGeometry
